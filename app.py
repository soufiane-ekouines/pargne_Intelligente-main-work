"""
SaveTogether - Smart Community Savings Platform
Main Flask application file - Supabase PostgreSQL Version
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
import json
from functools import wraps
from flask_dance.contrib.google import make_google_blueprint, google
import uuid
from dotenv import load_dotenv
from database import db, Database

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'savetogether-secret-key-2024')

# Google OAuth Configuration
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID', 'your-google-client-id')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET', 'your-google-client-secret')

# Only register Google OAuth if credentials are provided
if GOOGLE_CLIENT_ID != 'your-google-client-id' and GOOGLE_CLIENT_SECRET != 'your-google-client-secret':
    try:
        google_bp = make_google_blueprint(
            client_id=GOOGLE_CLIENT_ID,
            client_secret=GOOGLE_CLIENT_SECRET,
            scope=['openid', 'https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile'],
            redirect_to='google_login'
        )
        app.register_blueprint(google_bp, url_prefix='/login')
    except Exception as e:
        print(f"Warning: Google OAuth setup failed: {str(e)}")
else:
    print("Warning: Google OAuth not configured (missing credentials)")

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # type: ignore

# Database configuration (Supabase)
# All database operations now handled by database.py module

class User(UserMixin):
    def __init__(self, id, username, email, is_premium=False, profile_picture=None):
        self.id = id
        self.username = username
        self.email = email
        self.is_premium = is_premium
        self.profile_picture = profile_picture

@login_manager.user_loader
def load_user(user_id):
    user_data = Database.get_user_by_id(user_id)
    
    if user_data:
        return User(user_data['id'], user_data['username'], user_data['email'], 
                   user_data['is_premium'], user_data.get('profile_picture'))
    return None

def premium_required(f):
    """Decorator to require premium subscription"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_premium:
            flash('Cette fonctionnalité nécessite un abonnement premium (19 MAD/mois)', 'warning')
            return redirect(url_for('pricing'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def index():
    """Landing page - accessible to everyone"""
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Check if user already exists
        if Database.get_user_by_username(username) or Database.get_user_by_email(email):
            flash('Le nom d\'utilisateur ou l\'email existe déjà', 'error')
            return render_template('register.html')
        
        # Create new user
        password_hash = generate_password_hash(password)
        Database.create_user(username, email, password_hash)
        
        flash('Inscription réussie ! Veuillez vous connecter.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user_data = Database.get_user_by_username(username)
        
        if user_data and check_password_hash(user_data['password_hash'], password):
            user = User(user_data['id'], user_data['username'], user_data['email'], user_data['is_premium'])
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Nom d\'utilisateur ou mot de passe invalide', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    return redirect(url_for('index'))

@app.route('/login/google')
def google_login():
    """Handle Google OAuth login"""
    # Check if Google OAuth is configured
    if GOOGLE_CLIENT_ID == 'your-google-client-id' or GOOGLE_CLIENT_SECRET == 'your-google-client-secret':
        flash('Google OAuth n\'est pas configuré', 'error')
        return redirect(url_for('login'))
    
    if not google.authorized:
        return redirect(url_for('google.login'))
    
    try:
        resp = google.get('/oauth2/v2/userinfo')
        if resp.ok:
            google_data = resp.json()
            google_id = google_data.get('id')
            email = google_data.get('email')
            name = google_data.get('name', email.split('@')[0] if email else 'user')
            profile_picture = google_data.get('picture')
            
            # Check if user exists by google_id or email
            user_data = Database.get_user_by_google_id(google_id)
            if not user_data:
                user_data = Database.get_user_by_email(email)
            
            if user_data:
                # User exists, update google info if needed
                Database.update_user(user_data['id'], 
                                    google_id=google_id, 
                                    google_email=email, 
                                    profile_picture=profile_picture)
                user = User(user_data['id'], user_data['username'], user_data['email'], 
                          user_data['is_premium'], profile_picture or user_data.get('profile_picture'))
            else:
                # Create new user
                username = name
                # Ensure username is unique
                base_username = username
                counter = 1
                while Database.get_user_by_username(username):
                    username = f"{base_username}{counter}"
                    counter += 1
                
                new_user = Database.create_user(username, email, '', google_id, email, profile_picture)
                user = User(new_user['id'], username, email, False, profile_picture)
            
            login_user(user)
            flash(f'Connecté avec succès via Google !', 'success')
            return redirect(url_for('dashboard'))
    except Exception as e:
        flash(f'Erreur lors de la connexion Google: {str(e)}', 'error')
    
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard showing user's groups and progress"""
    # Get user's groups (only active memberships)
    groups = Database.get_user_groups(current_user.id)
    
    # Get recent approved contributions
    recent_contributions = Database.get_recent_contributions(current_user.id, limit=10)
    
    # Format for template
    formatted_contributions = []
    for contrib in recent_contributions:
        formatted_contributions.append({
            'amount': contrib['amount'],
            'description': contrib['description'],
            'contribution_date': contrib['contribution_date'],
            'group_name': contrib['groups']['name'],
            'username': contrib['users']['username']
        })
    
    # Get unread notifications
    notifications = Database.get_user_notifications(current_user.id, is_read=False)
    
    return render_template('dashboard.html', groups=groups, 
                         recent_contributions=formatted_contributions, 
                         notifications=notifications)

@app.route('/groups/create', methods=['GET', 'POST'])
@login_required
def create_group():
    """Create a new savings group"""
    if request.method == 'POST':
        # Check if it's an AJAX request
        if request.is_json or request.content_type == 'application/json':
            data = request.get_json()
            name = data.get('name')
            description = data.get('description', '')
            category = data.get('category', 'Autre')
            target_amount = float(data.get('target_amount', 0))
            deadline = data.get('deadline') if data.get('deadline') else None
        else:
            name = request.form['name']
            description = request.form.get('description', '')
            category = request.form.get('category', 'Autre')
            target_amount = float(request.form['target_amount'])
            deadline = request.form.get('deadline') if request.form.get('deadline') else None
        
        if not name or target_amount <= 0:
            if request.is_json or request.content_type == 'application/json':
                return jsonify({'status': 'error', 'message': 'Nom et montant requis'}), 400
            flash('Nom et montant requis', 'error')
            return render_template('create_group.html')
        
        # Generate invite code
        invite_code = str(uuid.uuid4())[:8]
        
        # Create group
        group = Database.create_group(name, description, category, target_amount, 
                                     deadline, current_user.id, invite_code)
        
        if group:
            group_id = group['id']
            
            # Add creator as member with 'active' status
            Database.add_group_member(group_id, current_user.id, 'active')
            
            # Return JSON for AJAX requests
            if request.is_json or request.content_type == 'application/json':
                return jsonify({
                    'status': 'success',
                    'message': f'Groupe "{name}" créé avec succès !',
                    'group_id': group_id,
                    'group_name': name,
                    'invite_code': invite_code
                })
            
            flash(f'Groupe "{name}" créé avec succès ! Code d\'invitation : {invite_code}', 'success')
            return redirect(url_for('group_detail', group_id=group_id))
    
    return render_template('create_group.html')

@app.route('/groups/join', methods=['GET', 'POST'])
@login_required
def join_group():
    """Join a group using invite code - now requires admin approval"""
    if request.method == 'POST':
        try:
            # Check if it's an AJAX request
            if request.is_json or request.content_type == 'application/json':
                data = request.get_json()
                invite_code = data.get('invite_code')
            else:
                invite_code = request.form['invite_code']
            
            if not invite_code:
                flash('Please enter an invite code', 'error')
                return render_template('join_group.html')
            
            # Find group by invite code
            group = Database.get_group_by_invite_code(invite_code)
            
            if not group:
                if request.is_json or request.content_type == 'application/json':
                    return jsonify({'status': 'error', 'message': 'Code d\'invitation invalide'}), 400
                flash('Code d\'invitation invalide', 'error')
                return render_template('join_group.html')
            
            group_id = group['id']
            admin_id = group['created_by']
            group_name = group['name']
            
            # Check if user is already a member (any status)
            existing = Database.get_group_membership(group_id, current_user.id)
            
            if existing:
                status = existing['status']
                if status == 'active':
                    message = 'Vous êtes déjà membre actif de ce groupe'
                elif status == 'pending':
                    message = 'Votre demande est en attente d\'approbation'
                elif status == 'rejected':
                    message = 'Votre demande a été refusée'
                else:
                    message = 'Vous avez déjà une demande en cours'
                
                if request.is_json or request.content_type == 'application/json':
                    return jsonify({'status': 'error', 'message': message}), 400
                flash(message, 'error')
                return render_template('join_group.html')
            
            # Add user to group with 'pending' status
            Database.add_group_member(group_id, current_user.id, 'pending')
            
            # Notify the admin
            Database.create_notification(admin_id, group_id, 
                f'{current_user.username} souhaite rejoindre le groupe "{group_name}". Attendez l\'approbation.')
            
            # Notify the user
            Database.create_notification(current_user.id, group_id, 
                f'Votre demande pour rejoindre "{group_name}" est en attente d\'approbation.')
            
            success_message = 'Demande envoyée ! Vous serez notifié lorsque l\'admin approuvera votre demande.'
            if request.is_json or request.content_type == 'application/json':
                return jsonify({'status': 'success', 'message': success_message})
            
            flash(success_message, 'success')
            return redirect(url_for('dashboard'))
        
        except Exception as e:
            print(f"Error in join_group: {str(e)}")
            import traceback
            traceback.print_exc()
            flash(f'An error occurred: {str(e)}', 'error')
            return render_template('join_group.html')
    
    return render_template('join_group.html')

@app.route('/groups/<int:group_id>/manage-requests')
@login_required
def manage_requests(group_id):
    """Manage group join requests (admin only)"""
    # Get group details
    group = Database.get_group_by_id(group_id)
    
    if not group:
        flash('Groupe introuvable', 'error')
        return redirect(url_for('dashboard'))
    
    # Check if user is admin
    if group['created_by'] != current_user.id:
        flash('Accès non autorisé. Seul l\'administrateur peut gérer les demandes.', 'error')
        return redirect(url_for('group_detail', group_id=group_id))
    
    # Get all pending and rejected members
    all_requests = Database.get_pending_and_rejected_members(group_id)
    
    # Separate pending and rejected
    pending_members = []
    rejected_members = []
    
    for req in all_requests:
        member_data = {
            'membership_id': req['id'],
            'user_id': req['user_id'],
            'username': req['users']['username'],
            'email': req['users']['email'],
            'profile_picture': req['users'].get('profile_picture'),
            'joined_at': req['joined_at'],
            'status': req['status']
        }
        
        if req['status'] == 'pending':
            pending_members.append(member_data)
        else:
            rejected_members.append(member_data)
    
    # Get active members count
    active_count = Database.get_active_member_count(group_id)
    
    return render_template('manage_requests.html', 
                         group=group, 
                         pending_members=pending_members,
                         rejected_members=rejected_members,
                         active_count=active_count)

@app.route('/groups/<int:group_id>')
@login_required
def group_detail(group_id):
    """Group detail page with progress and contributions"""
    # Check if user is active member of this group
    membership = Database.get_group_membership(group_id, current_user.id)
    if not membership or membership['status'] != 'active':
        flash('Vous n\'êtes pas membre actif de ce groupe', 'error')
        return redirect(url_for('dashboard'))
    
    # Get group details
    group = Database.get_group_by_id(group_id)
    
    # Get group members (only active)
    member_list = Database.get_group_members(group_id, 'active')
    members = []
    for m in member_list:
        members.append({
            'username': m['users']['username'],
            'email': m['users']['email'],
            'profile_picture': m['users'].get('profile_picture'),
            'joined_at': m['joined_at'],
            'status': m['status']
        })
    
    # Check if current user is admin
    is_admin = (group['created_by'] == current_user.id)
    
    # Get pending and rejected members (only for admin)
    pending_members = []
    rejected_members = []
    if is_admin:
        all_requests = Database.get_pending_and_rejected_members(group_id)
        for req in all_requests:
            member_data = {
                'membership_id': req['id'],
                'user_id': req['user_id'],
                'username': req['users']['username'],
                'email': req['users']['email'],
                'profile_picture': req['users'].get('profile_picture'),
                'joined_at': req['joined_at'],
                'status': req['status']
            }
            
            if req['status'] == 'pending':
                pending_members.append(member_data)
            else:
                rejected_members.append(member_data)
    
    # Get total approved contributions
    total_contributed = Database.get_total_contributions(group_id, 'approved')
    
    # Get pending contributions (only for admin)
    pending_contributions = []
    if is_admin:
        pending_contribs = Database.get_pending_contributions(group_id)
        for pc in pending_contribs:
            pending_contributions.append({
                'id': pc['id'],
                'amount': pc['amount'],
                'description': pc['description'],
                'proof_image': pc['proof_image'],
                'contribution_date': pc['contribution_date'],
                'user_id': pc['user_id'],
                'username': pc['users']['username'],
                'profile_picture': pc['users'].get('profile_picture')
            })
    
    # Get approved contributions history
    approved_contribs = Database.get_group_contributions(group_id, 'approved')
    contributions = []
    for ac in approved_contribs:
        contributions.append({
            'amount': ac['amount'],
            'description': ac['description'],
            'contribution_date': ac['contribution_date'],
            'username': ac['users']['username'],
            'profile_picture': ac['users'].get('profile_picture'),
            'proof_image': ac.get('proof_image')
        })
    
    # Calculate progress percentage
    progress_percentage = (total_contributed / group['target_amount']) * 100 if group['target_amount'] > 0 else 0

    return render_template('group_detail.html', group=group, members=members, 
                         total_contributed=total_contributed, contributions=contributions,
                         progress_percentage=progress_percentage, is_admin=is_admin,
                         pending_members=pending_members, rejected_members=rejected_members,
                         pending_contributions=pending_contributions)

@app.route('/groups/<int:group_id>/contribute', methods=['GET', 'POST'])
@login_required
def contribute(group_id):
    """Add a contribution to a group"""
    if request.method == 'POST':
        amount = float(request.form['amount'])
        description = request.form.get('description', '')
        
        # Check if user is active member of this group
        membership = Database.get_group_membership(group_id, current_user.id)
        if not membership or membership['status'] != 'active':
            flash('Vous n\'êtes pas membre actif de ce groupe', 'error')
            return redirect(url_for('dashboard'))
        
        # Handle proof image upload (optional)
        proof_image = None
        if 'proof_image' in request.files:
            file = request.files['proof_image']
            if file and file.filename and file.filename != '':
                # Secure the filename
                import os
                from werkzeug.utils import secure_filename
                filename = secure_filename(file.filename)
                # Add timestamp to make unique
                import time
                unique_filename = f"{int(time.time())}_{filename}"
                # Save to uploads folder
                upload_folder = os.path.join('static', 'uploads', 'proofs')
                os.makedirs(upload_folder, exist_ok=True)
                file_path = os.path.join(upload_folder, unique_filename)
                file.save(file_path)
                proof_image = f"uploads/proofs/{unique_filename}"
        
        # Determine initial status based on proof image
        status = 'pending' if proof_image else 'approved'
        
        # Add contribution
        Database.create_contribution(group_id, current_user.id, amount, description, proof_image, status)
        
        # Get group info
        group = Database.get_group_by_id(group_id)
        group_name = group['name']
        admin_id = group['created_by']
        
        if status == 'pending':
            # Notify admin to review the contribution
            Database.create_notification(admin_id, group_id, 
                f'{current_user.username} submitted a contribution of {amount} MAD with proof image for review in "{group_name}"')
            flash(f'Contribution de {amount} MAD soumise ! En attente de l\'approbation de l\'admin.', 'info')
        else:
            # Auto-approved, create notifications for other members
            active_members = Database.get_group_members(group_id, 'active')
            
            for member in active_members:
                if member['user_id'] != current_user.id:
                    Database.create_notification(member['user_id'], group_id, 
                        f'{current_user.username} contributed {amount} MAD to "{group_name}"')
            
            flash(f'Contribution de {amount} MAD ajoutée avec succès !', 'success')
        
        return redirect(url_for('group_detail', group_id=group_id))
    
    group = Database.get_group_by_id(group_id)
    return render_template('contribute.html', group=group)

@app.route('/groups/<int:group_id>/contributions/<int:contribution_id>/approve', methods=['POST'])
@login_required
def approve_contribution(group_id, contribution_id):
    """Approve a pending contribution (admin only)"""
    # Check if current user is admin of the group
    group = Database.get_group_by_id(group_id)
    
    if not group or group['created_by'] != current_user.id:
        return jsonify({'status': 'error', 'message': 'Accès non autorisé'}), 403
    
    # Check if contribution exists and is pending
    contribution = Database.get_contribution_by_id(contribution_id)
    
    if not contribution or contribution['group_id'] != group_id or contribution['status'] != 'pending':
        return jsonify({'status': 'error', 'message': 'Contribution introuvable'}), 404
    
    # Update status to approved
    Database.update_contribution_status(contribution_id, 'approved')
    
    # Get contributor info
    contributor = Database.get_user_by_id(contribution['user_id'])
    username = contributor['username']
    
    # Notify the contributor
    Database.create_notification(contribution['user_id'], group_id, 
        f'Your contribution of {contribution["amount"]} MAD to "{group["name"]}" has been approved!')
    
    # Notify other group members
    active_members = Database.get_group_members(group_id, 'active')
    
    for member in active_members:
        if member['user_id'] != contribution['user_id'] and member['user_id'] != current_user.id:
            Database.create_notification(member['user_id'], group_id, 
                f'{username} contributed {contribution["amount"]} MAD to "{group["name"]}"')
    
    return jsonify({'status': 'success', 'message': 'Contribution approuvée avec succès !'})

@app.route('/groups/<int:group_id>/contributions/<int:contribution_id>/reject', methods=['POST'])
@login_required
def reject_contribution(group_id, contribution_id):
    """Reject a pending contribution (admin only)"""
    # Check if current user is admin of the group
    group = Database.get_group_by_id(group_id)
    
    if not group or group['created_by'] != current_user.id:
        return jsonify({'status': 'error', 'message': 'Accès non autorisé'}), 403
    
    # Check if contribution exists and is pending
    contribution = Database.get_contribution_by_id(contribution_id)
    
    if not contribution or contribution['group_id'] != group_id or contribution['status'] != 'pending':
        return jsonify({'status': 'error', 'message': 'Contribution introuvable'}), 404
    
    # Update status to rejected
    Database.update_contribution_status(contribution_id, 'rejected')
    
    # Notify the contributor
    Database.create_notification(contribution['user_id'], group_id, 
        f'Your contribution of {contribution["amount"]} MAD to "{group["name"]}" has been rejected. Please contact the admin for more info.')
    
    return jsonify({'status': 'success', 'message': 'Contribution rejetée'})

@app.route('/notifications/mark_read/<int:notification_id>')
@login_required
def mark_notification_read(notification_id):
    """Mark a notification as read"""
    Database.mark_notification_read(notification_id, current_user.id)
    return jsonify({'status': 'success'})

@app.route('/export/<int:group_id>')
@login_required
@premium_required
def export_group_data(group_id):
    """Export group data as CSV (Premium feature)"""
    # Check if user is member of this group
    membership = Database.get_group_membership(group_id, current_user.id)
    if not membership:
        flash('Vous n\'êtes pas membre de ce groupe', 'error')
        return redirect(url_for('dashboard'))
    
    # Get group data
    export_data = Database.get_group_export_data(group_id)
    group = export_data['group']
    contributions = export_data['contributions']
    
    # Generate CSV content
    csv_content = f"Group: {group['name']}\n"
    csv_content += f"Target Amount: {group['target_amount']} MAD\n"
    csv_content += f"Deadline: {group['deadline'] or 'No deadline'}\n\n"
    csv_content += "Amount,Description,Date,Contributor\n"
    
    for contribution in contributions:
        csv_content += f"{contribution['amount']},{contribution['description']},{contribution['contribution_date']},{contribution['users']['username']}\n"
    
    from flask import Response
    return Response(
        csv_content,
        mimetype='text/csv',
        headers={'Content-Disposition': f'attachment; filename=group_{group_id}_data.csv'}
    )

@app.route('/pricing')
def pricing():
    """Pricing page"""
    return render_template('pricing.html')

@app.route('/upgrade')
@login_required
def upgrade():
    """Upgrade to premium (simulated)"""
    Database.update_user_premium(current_user.id, True)
    flash('Félicitations ! Vous avez été mis à niveau vers Premium !', 'success')
    return redirect(url_for('dashboard'))

@app.route('/update-profile', methods=['POST'])
@login_required
def update_profile():
    """Update user profile information"""
    try:
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        
        if not username or not email:
            flash('Username and email are required', 'error')
            return redirect(url_for('settings'))
        
        # Check if username is taken by another user
        existing_user = Database.get_user_by_username(username)
        if existing_user and existing_user['id'] != current_user.id:
            flash('Username already taken by another user', 'error')
            return redirect(url_for('settings'))
        
        # Check if email is taken by another user
        existing_email = Database.get_user_by_email(email)
        if existing_email and existing_email['id'] != current_user.id:
            flash('Email already taken by another user', 'error')
            return redirect(url_for('settings'))
        
        # Update user information
        updated_user = Database.update_user(current_user.id, username=username, email=email)
        
        if updated_user:
            # Reload user from database
            user_data = Database.get_user_by_id(current_user.id)
            
            if user_data:
                from flask_login import logout_user, login_user
                new_user = User(user_data['id'], user_data['username'], user_data['email'], 
                               user_data['is_premium'], user_data.get('profile_picture'))
                logout_user()
                login_user(new_user)
                flash('Profile updated successfully!', 'success')
            else:
                flash('Error reloading user data', 'error')
        else:
            flash('Error: Profile update failed', 'error')
        
        return redirect(url_for('settings'))
        
    except Exception as e:
        flash(f'Error updating profile: {str(e)}', 'error')
        return redirect(url_for('settings'))

@app.route('/upload-profile-picture', methods=['POST'])
@login_required
def upload_profile_picture():
    """Upload user profile picture"""
    try:
        if 'profile_picture' not in request.files:
            flash('No file selected', 'error')
            return redirect(url_for('settings'))
        
        file = request.files['profile_picture']
        
        if not file or file.filename == '':
            flash('No file selected', 'error')
            return redirect(url_for('settings'))
        
        # Secure the filename
        import os
        from werkzeug.utils import secure_filename
        
        # Check file extension
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
        filename = secure_filename(file.filename) if file.filename else 'profile.jpg'
        file_ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        
        if file_ext not in allowed_extensions:
            flash('Invalid file type. Please upload an image (PNG, JPG, JPEG, GIF, WEBP)', 'error')
            return redirect(url_for('settings'))
        
        # Add timestamp to make unique
        import time
        unique_filename = f"{current_user.id}_{int(time.time())}.{file_ext}"
        
        # Get absolute path for uploads folder
        base_dir = os.path.dirname(os.path.abspath(__file__))
        upload_folder = os.path.join(base_dir, 'static', 'uploads', 'profiles')
        
        # Create directory if it doesn't exist
        os.makedirs(upload_folder, exist_ok=True)
        
        # Full file path
        file_path = os.path.join(upload_folder, unique_filename)
        
        # Save the file
        file.save(file_path)
        
        # Database path (relative to static folder)
        profile_picture_path = f"uploads/profiles/{unique_filename}"
        
        # Update database
        Database.update_user(current_user.id, profile_picture=profile_picture_path)
        
        # Force reload user from database
        from flask_login import logout_user, login_user
        user_data = Database.get_user_by_id(current_user.id)
        
        if user_data:
            updated_user = User(user_data['id'], user_data['username'], user_data['email'], 
                               user_data['is_premium'], user_data.get('profile_picture'))
            logout_user()
            login_user(updated_user)
        
        flash('Profile picture updated successfully!', 'success')
        return redirect(url_for('settings'))
        
    except Exception as e:
        flash(f'Error uploading picture: {str(e)}', 'error')
        return redirect(url_for('settings'))

@app.route('/groups/<int:group_id>/analytics')
@login_required
def group_analytics(group_id):
    """Group analytics page with charts and predictions"""
    # Check if user is member of this group
    membership = Database.get_group_membership(group_id, current_user.id)
    if not membership or membership['status'] != 'active':
        flash('Vous n\'êtes pas membre de ce groupe', 'error')
        return redirect(url_for('dashboard'))
    
    # Get group info
    group = Database.get_group_by_id(group_id)
    
    # Get all approved contributions
    contributions = Database.get_all_contributions_for_analytics(group_id)
    
    # Format contributions for template
    formatted_contribs = []
    for c in contributions:
        formatted_contribs.append({
            'amount': c['amount'],
            'contribution_date': c['contribution_date'],
            'username': c['users']['username'],
            'profile_picture': c['users'].get('profile_picture')
        })
    
    # Get total contributed
    total_contributed = Database.get_total_contributions(group_id, 'approved')
    
    # Calculate progress percentage
    progress_percentage = (total_contributed / group['target_amount']) * 100 if group['target_amount'] > 0 else 0
    
    # Calculate statistics
    import statistics
    from datetime import datetime, timedelta
    
    contribution_amounts = [float(c['amount']) for c in formatted_contribs]
    
    avg_contribution = round(statistics.mean(contribution_amounts), 2) if contribution_amounts else 0
    median_contribution = round(statistics.median(contribution_amounts), 2) if contribution_amounts else 0
    std_dev = round(statistics.stdev(contribution_amounts), 2) if len(contribution_amounts) > 1 else 0
    
    # Calculate days active
    if formatted_contribs:
        first_contribution = datetime.fromisoformat(formatted_contribs[0]['contribution_date'].replace('Z', '+00:00'))
        days_active = (datetime.now() - first_contribution.replace(tzinfo=None)).days + 1
    else:
        days_active = 1
    
    # Progress over time data
    progress_dates = []
    progress_amounts = []
    cumulative = 0
    for contrib in formatted_contribs:
        cumulative += float(contrib['amount'])
        date_str = contrib['contribution_date'][:10] if isinstance(contrib['contribution_date'], str) else str(contrib['contribution_date'])[:10]
        progress_dates.append(date_str)
        progress_amounts.append(cumulative)
    
    # Member statistics
    member_stats_data = Database.get_member_contribution_stats(group_id)
    
    member_stats = []
    member_names = []
    member_totals = []
    
    for member in member_stats_data:
        total = float(member['total'])
        count = member['count']
        average = round(total / count, 2) if count > 0 else 0
        last_date = member['last_date'][:10] if member['last_date'] else 'Never'
        rate = round((total / total_contributed * 100), 1) if total_contributed > 0 else 0
        
        rate_color = 'success' if rate >= 30 else 'warning' if rate >= 15 else 'danger'
        
        member_stats.append({
            'username': member['username'],
            'profile_picture': member['profile_picture'],
            'total': round(total, 2),
            'count': count,
            'average': average,
            'last_date': last_date,
            'rate': rate,
            'rate_color': rate_color
        })
        
        member_names.append(member['username'])
        member_totals.append(round(total, 2))
    
    # Monthly trend - simplified for Supabase
    monthly_labels = []
    monthly_amounts = []
    
    if formatted_contribs:
        from collections import defaultdict
        monthly_data = defaultdict(float)
        
        for contrib in formatted_contribs:
            date_str = contrib['contribution_date'][:7] if isinstance(contrib['contribution_date'], str) else str(contrib['contribution_date'])[:7]
            monthly_data[date_str] += float(contrib['amount'])
        
        monthly_labels = sorted(monthly_data.keys())
        monthly_amounts = [monthly_data[month] for month in monthly_labels]
    
    # Predictive analysis
    current_monthly = round(sum(monthly_amounts) / len(monthly_amounts), 2) if monthly_amounts else 0
    remaining = float(group['target_amount']) - total_contributed
    
    if current_monthly > 0:
        months_needed = remaining / current_monthly
        estimated_completion = (datetime.now() + timedelta(days=int(months_needed * 30))).strftime('%B %Y')
    else:
        estimated_completion = 'Unknown'
        months_needed = 999
    
    required_monthly = 0
    if group['deadline']:
        deadline_date = datetime.fromisoformat(str(group['deadline']))
        months_remaining = max(1, (deadline_date.year - datetime.now().year) * 12 + (deadline_date.month - datetime.now().month))
        required_monthly = round(remaining / months_remaining, 2)
    
    # Prediction status
    if progress_percentage >= 100:
        prediction_status = 'success'
        prediction_icon = 'check-circle'
        prediction_message = 'Congratulations! Goal achieved!'
    elif current_monthly >= required_monthly:
        prediction_status = 'success'
        prediction_icon = 'chart-line'
        prediction_message = f'On track! At current rate, you\'ll reach your goal by {estimated_completion}.'
    elif current_monthly >= required_monthly * 0.7:
        prediction_status = 'warning'
        prediction_icon = 'exclamation-triangle'
        prediction_message = f'Slightly behind schedule. Increase contributions to {required_monthly} MAD/month to stay on track.'
    else:
        prediction_status = 'danger'
        prediction_icon = 'exclamation-circle'
        prediction_message = f'Behind schedule. Need {required_monthly} MAD/month to meet deadline.'
    
    # Patterns and trends
    patterns = []
    
    # Check consistency
    consistency = round((1 - (std_dev / avg_contribution if avg_contribution > 0 else 1)) * 100, 1)
    if consistency > 70:
        patterns.append({'icon': 'check', 'color': 'success', 'text': f'Highly consistent contributions ({consistency}% consistency score)'})
    else:
        patterns.append({'icon': 'chart-line', 'color': 'warning', 'text': f'Variable contribution patterns ({consistency}% consistency score)'})
    
    # Check trend
    if len(monthly_amounts) >= 2:
        if monthly_amounts[-1] > monthly_amounts[-2]:
            patterns.append({'icon': 'arrow-up', 'color': 'success', 'text': 'Increasing trend in recent months'})
        elif monthly_amounts[-1] < monthly_amounts[-2]:
            patterns.append({'icon': 'arrow-down', 'color': 'danger', 'text': 'Decreasing trend in recent months'})
        else:
            patterns.append({'icon': 'minus', 'color': 'info', 'text': 'Stable contribution pattern'})
    
    # Check participation
    active_members = len([m for m in member_stats if m['count'] > 0])
    total_members = len(member_stats)
    participation_rate = round((active_members / total_members * 100), 1) if total_members > 0 else 0
    patterns.append({'icon': 'users', 'color': 'info', 'text': f'{participation_rate}% member participation rate'})
    
    # Frequency distribution
    high_freq = len([m for m in member_stats if m['count'] >= len(monthly_labels) * 2])
    mid_freq = len([m for m in member_stats if len(monthly_labels) <= m['count'] < len(monthly_labels) * 2])
    low_freq = total_members - high_freq - mid_freq
    
    frequency = {
        'active': round((high_freq / total_members * 100), 1) if total_members > 0 else 0,
        'moderate': round((mid_freq / total_members * 100), 1) if total_members > 0 else 0,
        'low': round((low_freq / total_members * 100), 1) if total_members > 0 else 0
    }
    
    return render_template('group_analytics.html',
                         group=group,
                         total_contributed=round(total_contributed, 2),
                         progress_percentage=round(progress_percentage, 2),
                         avg_contribution=avg_contribution,
                         days_active=days_active,
                         progress_dates=progress_dates,
                         progress_amounts=progress_amounts,
                         member_names=member_names,
                         member_totals=member_totals,
                         monthly_labels=monthly_labels,
                         monthly_amounts=monthly_amounts,
                         member_stats=member_stats,
                         estimated_completion=estimated_completion,
                         required_monthly=required_monthly,
                         current_monthly=current_monthly,
                         prediction_status=prediction_status,
                         prediction_icon=prediction_icon,
                         prediction_message=prediction_message,
                         patterns=patterns,
                         frequency=frequency,
                         stats={
                             'mean': avg_contribution,
                             'median': median_contribution,
                             'std_dev': std_dev,
                             'consistency': consistency
                         })

@app.route('/settings')
@login_required
def settings():
    """User settings page"""
    return render_template('settings.html')

# API endpoints for Chart.js
@app.route('/api/group_progress/<int:group_id>')
@login_required
def api_group_progress(group_id):
    """API endpoint for group progress data"""
    # Check if user is member
    membership = Database.get_group_membership(group_id, current_user.id)
    if not membership:
        return jsonify({'error': 'Access denied'}), 403
    
    group = Database.get_group_by_id(group_id)
    target_amount = group['target_amount']
    
    total_contributed = Database.get_total_contributions(group_id)
    
    return jsonify({
        'target': float(target_amount),
        'contributed': float(total_contributed),
        'percentage': float((total_contributed / target_amount) * 100) if target_amount > 0 else 0
    })

@app.route('/groups/<int:group_id>/approve/<int:user_id>', methods=['POST'])
@login_required
def approve_member(group_id, user_id):
    """Approve a pending or rejected member request (admin only)"""
    # Check if current user is admin of the group
    group = Database.get_group_by_id(group_id)
    
    if not group or group['created_by'] != current_user.id:
        return jsonify({'status': 'error', 'message': 'Accès non autorisé'}), 403
    
    # Check if membership exists and is pending or rejected
    membership = Database.get_group_membership(group_id, user_id)
    
    if not membership or membership['status'] not in ['pending', 'rejected']:
        return jsonify({'status': 'error', 'message': 'Demande introuvable'}), 404
    
    # Update status to active
    Database.update_member_status(group_id, user_id, 'active')
    
    # Get group name and user info for notification
    group_name = group['name']
    
    user = Database.get_user_by_id(user_id)
    username = user['username']
    
    # Notify the user
    Database.create_notification(user_id, group_id, 
        f'Votre demande pour rejoindre "{group_name}" a été approuvée !')
    
    return jsonify({'status': 'success', 'message': f'{username} a été ajouté au groupe avec succès'})

@app.route('/groups/<int:group_id>/reject/<int:user_id>', methods=['POST'])
@login_required
def reject_member(group_id, user_id):
    """Reject a pending member request (admin only)"""
    # Check if current user is admin of the group
    group = Database.get_group_by_id(group_id)
    
    if not group or group['created_by'] != current_user.id:
        return jsonify({'status': 'error', 'message': 'Accès non autorisé'}), 403
    
    # Check if membership exists and is pending
    membership = Database.get_group_membership(group_id, user_id)
    
    if not membership or membership['status'] != 'pending':
        return jsonify({'status': 'error', 'message': 'Demande introuvable ou déjà traitée'}), 404
    
    # Update status to rejected
    Database.update_member_status(group_id, user_id, 'rejected')
    
    # Get group name and user info for notification
    group_name = group['name']
    
    user = Database.get_user_by_id(user_id)
    username = user['username']
    
    # Notify the user
    Database.create_notification(user_id, group_id, 
        f'Votre demande pour rejoindre "{group_name}" a été refusée.')
    
    return jsonify({'status': 'success', 'message': f'La demande de {username} a été refusée'})

if __name__ == '__main__':
    db.init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
else:
    # For Vercel serverless deployment
    try:
        db.init_db()
    except Exception as e:
        print(f"Warning: Database initialization failed: {str(e)}")
        # Continue anyway - connection will be tested on first request

# Export app for Vercel
app = app
