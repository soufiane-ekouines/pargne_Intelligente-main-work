"""
SaveTogether - Smart Community Savings Platform
Main Flask application file
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import sqlite3
import os
import json
from functools import wraps
from flask_dance.contrib.google import make_google_blueprint, google
import uuid

app = Flask(__name__)
app.secret_key = 'savetogether-secret-key-2024'

# Google OAuth Configuration
# NOTE: Set these environment variables or update with your Google OAuth credentials
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID', 'your-google-client-id')
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET', 'your-google-client-secret')

google_bp = make_google_blueprint(
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    scope=['openid', 'https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile'],
    redirect_to='google_login'
)
app.register_blueprint(google_bp, url_prefix='/login')

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Database configuration
DATABASE = 'savetogether.db'

def init_db():
    """Initialize the database with required tables"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT,
            is_premium BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            google_id TEXT UNIQUE,
            google_email TEXT,
            profile_picture TEXT
        )
    ''')
    
    # Add new columns to existing users table if they don't exist
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN google_id TEXT UNIQUE')
    except:
        pass
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN google_email TEXT')
    except:
        pass
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN profile_picture TEXT')
    except:
        pass
    
    # Groups table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS groups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            target_amount DECIMAL(10,2) NOT NULL,
            deadline DATE,
            created_by INTEGER,
            invite_code TEXT UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            category TEXT,
            FOREIGN KEY (created_by) REFERENCES users (id)
        )
    ''')
    
    # Add category column if it doesn't exist
    try:
        cursor.execute('ALTER TABLE groups ADD COLUMN category TEXT')
    except:
        pass
    
    # Group members table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS group_members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_id INTEGER,
            user_id INTEGER,
            status TEXT DEFAULT 'active',
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (group_id) REFERENCES groups (id),
            FOREIGN KEY (user_id) REFERENCES users (id),
            UNIQUE(group_id, user_id)
        )
    ''')
    
    # Add status column if it doesn't exist
    try:
        cursor.execute('ALTER TABLE group_members ADD COLUMN status TEXT DEFAULT "active"')
        # Update existing records to have status 'active'
        cursor.execute('UPDATE group_members SET status = "active" WHERE status IS NULL')
    except:
        pass
    
    # Contributions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contributions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_id INTEGER,
            user_id INTEGER,
            amount DECIMAL(10,2) NOT NULL,
            description TEXT,
            proof_image TEXT,
            status TEXT DEFAULT 'pending',
            contribution_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (group_id) REFERENCES groups (id),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Add columns if they don't exist (for existing databases)
    try:
        cursor.execute('ALTER TABLE contributions ADD COLUMN proof_image TEXT')
    except:
        pass
    try:
        cursor.execute('ALTER TABLE contributions ADD COLUMN status TEXT DEFAULT "pending"')
    except:
        pass
    
    # Notifications table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            group_id INTEGER,
            message TEXT NOT NULL,
            is_read BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (group_id) REFERENCES groups (id)
        )
    ''')
    
    conn.commit()
    conn.close()

class User(UserMixin):
    def __init__(self, id, username, email, is_premium=False, profile_picture=None):
        self.id = id
        self.username = username
        self.email = email
        self.is_premium = is_premium
        self.profile_picture = profile_picture

@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT id, username, email, is_premium, profile_picture FROM users WHERE id = ?', (user_id,))
    user_data = cursor.fetchone()
    conn.close()
    
    if user_data:
        return User(user_data['id'], user_data['username'], user_data['email'], 
                   user_data['is_premium'], user_data['profile_picture'] if user_data['profile_picture'] else None)
    return None

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

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
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if user already exists
        cursor.execute('SELECT id FROM users WHERE username = ? OR email = ?', (username, email))
        if cursor.fetchone():
            flash('Le nom d\'utilisateur ou l\'email existe déjà', 'error')
            conn.close()
            return render_template('register.html')
        
        # Create new user
        password_hash = generate_password_hash(password)
        cursor.execute(
            'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
            (username, email, password_hash)
        )
        conn.commit()
        conn.close()
        
        flash('Inscription réussie ! Veuillez vous connecter.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT id, username, email, password_hash, is_premium FROM users WHERE username = ?',
            (username,)
        )
        user_data = cursor.fetchone()
        conn.close()
        
        if user_data and check_password_hash(user_data[3], password):
            user = User(user_data[0], user_data[1], user_data[2], user_data[4])
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
    if not google.authorized:
        return redirect(url_for('google.login'))
    
    try:
        resp = google.get('/oauth2/v2/userinfo')
        if resp.ok:
            google_data = resp.json()
            google_id = google_data.get('id')
            email = google_data.get('email')
            name = google_data.get('name', email.split('@')[0])
            profile_picture = google_data.get('picture')
            
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Check if user exists by google_id or email
            cursor.execute(
                'SELECT id, username, email, is_premium, profile_picture FROM users WHERE google_id = ? OR email = ?',
                (google_id, email)
            )
            user_data = cursor.fetchone()
            
            if user_data:
                # User exists, update google info if needed
                cursor.execute(
                    'UPDATE users SET google_id = ?, google_email = ?, profile_picture = ? WHERE id = ?',
                    (google_id, email, profile_picture, user_data['id'])
                )
                user = User(user_data['id'], user_data['username'], user_data['email'], 
                          user_data['is_premium'], profile_picture or user_data['profile_picture'])
            else:
                # Create new user
                username = name
                # Ensure username is unique
                base_username = username
                counter = 1
                while True:
                    cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
                    if not cursor.fetchone():
                        break
                    username = f"{base_username}{counter}"
                    counter += 1
                
                cursor.execute(
                    'INSERT INTO users (username, email, google_id, google_email, profile_picture, password_hash) VALUES (?, ?, ?, ?, ?, ?)',
                    (username, email, google_id, email, profile_picture, '')  # Empty password for OAuth users
                )
                user_id = cursor.lastrowid
                user = User(user_id, username, email, False, profile_picture)
            
            conn.commit()
            conn.close()
            
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
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get user's groups (only active memberships)
    cursor.execute('''
        SELECT g.id, g.name, g.description, g.target_amount, g.deadline, g.created_at,
               COALESCE(contrib.total_contributed, 0) as total_contributed,
               COUNT(DISTINCT CASE WHEN gm2.status = 'active' THEN gm2.user_id END) as member_count
        FROM groups g
        INNER JOIN group_members gm ON g.id = gm.group_id AND gm.user_id = ? AND gm.status = 'active'
        LEFT JOIN group_members gm2 ON g.id = gm2.group_id
        LEFT JOIN (
            SELECT group_id, SUM(amount) as total_contributed
            FROM contributions
            WHERE status = 'approved'
            GROUP BY group_id
        ) contrib ON g.id = contrib.group_id
        GROUP BY g.id, g.name, g.description, g.target_amount, g.deadline, g.created_at, contrib.total_contributed
        ORDER BY g.created_at DESC
    ''', (current_user.id,))
    
    groups = cursor.fetchall()
    
    # Get recent approved contributions only
    cursor.execute('''
        SELECT c.amount, c.description, c.contribution_date, g.name as group_name, u.username
        FROM contributions c
        JOIN groups g ON c.group_id = g.id
        JOIN users u ON c.user_id = u.id
        WHERE c.group_id IN (
            SELECT group_id FROM group_members WHERE user_id = ?
        ) AND c.status = 'approved'
        ORDER BY c.contribution_date DESC
        LIMIT 10
    ''', (current_user.id,))
    
    recent_contributions = cursor.fetchall()
    
    # Get unread notifications
    cursor.execute('''
        SELECT * FROM notifications 
        WHERE user_id = ? AND is_read = FALSE 
        ORDER BY created_at DESC
    ''', (current_user.id,))
    
    notifications = cursor.fetchall()
    
    conn.close()
    
    return render_template('dashboard.html', groups=groups, recent_contributions=recent_contributions, notifications=notifications)

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
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Generate invite code
        invite_code = str(uuid.uuid4())[:8]
        
        # Create group
        cursor.execute('''
            INSERT INTO groups (name, description, category, target_amount, deadline, created_by, invite_code)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (name, description, category, target_amount, deadline, current_user.id, invite_code))
        
        group_id = cursor.lastrowid
        
        # Add creator as member with 'active' status
        cursor.execute('''
            INSERT INTO group_members (group_id, user_id, status)
            VALUES (?, ?, ?)
        ''', (group_id, current_user.id, 'active'))
        
        conn.commit()
        conn.close()
        
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
        # Check if it's an AJAX request
        if request.is_json or request.content_type == 'application/json':
            data = request.get_json()
            invite_code = data.get('invite_code')
        else:
            invite_code = request.form['invite_code']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Find group by invite code
        cursor.execute('SELECT id, created_by, name FROM groups WHERE invite_code = ?', (invite_code,))
        group = cursor.fetchone()
        
        if not group:
            if request.is_json or request.content_type == 'application/json':
                return jsonify({'status': 'error', 'message': 'Code d\'invitation invalide'}), 400
            flash('Code d\'invitation invalide', 'error')
            conn.close()
            return render_template('join_group.html')
        
        group_id = group['id']
        admin_id = group['created_by']
        group_name = group['name']
        
        # Check if user is already a member (any status)
        cursor.execute('SELECT id, status FROM group_members WHERE group_id = ? AND user_id = ?', (group_id, current_user.id))
        existing = cursor.fetchone()
        
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
            
            conn.close()
            if request.is_json or request.content_type == 'application/json':
                return jsonify({'status': 'error', 'message': message}), 400
            flash(message, 'error')
            return render_template('join_group.html')
        
        # Add user to group with 'pending' status
        cursor.execute('INSERT INTO group_members (group_id, user_id, status) VALUES (?, ?, ?)', 
                      (group_id, current_user.id, 'pending'))
        
        # Notify the admin
        cursor.execute('''
            INSERT INTO notifications (user_id, group_id, message)
            VALUES (?, ?, ?)
        ''', (admin_id, group_id, f'{current_user.username} souhaite rejoindre le groupe "{group_name}". Attendez l\'approbation.'))
        
        # Notify the user
        cursor.execute('''
            INSERT INTO notifications (user_id, group_id, message)
            VALUES (?, ?, ?)
        ''', (current_user.id, group_id, f'Votre demande pour rejoindre "{group_name}" est en attente d\'approbation.'))
        
        conn.commit()
        conn.close()
        
        success_message = 'Demande envoyée ! Vous serez notifié lorsque l\'admin approuvera votre demande.'
        if request.is_json or request.content_type == 'application/json':
            return jsonify({'status': 'success', 'message': success_message})
        
        flash(success_message, 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('join_group.html')

@app.route('/groups/<int:group_id>/manage-requests')
@login_required
def manage_requests(group_id):
    """Manage group join requests (admin only)"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get group details
    cursor.execute('SELECT * FROM groups WHERE id = ?', (group_id,))
    group = cursor.fetchone()
    
    if not group:
        flash('Groupe introuvable', 'error')
        return redirect(url_for('dashboard'))
    
    # Check if user is admin
    if group['created_by'] != current_user.id:
        flash('Accès non autorisé. Seul l\'administrateur peut gérer les demandes.', 'error')
        return redirect(url_for('group_detail', group_id=group_id))
    
    # Get all pending and rejected members
    cursor.execute('''
        SELECT gm.id as membership_id, u.id as user_id, u.username, u.email, 
               u.profile_picture, gm.joined_at, gm.status
        FROM group_members gm
        JOIN users u ON gm.user_id = u.id
        WHERE gm.group_id = ? AND gm.status IN ('pending', 'rejected')
        ORDER BY 
            CASE gm.status 
                WHEN 'pending' THEN 1 
                WHEN 'rejected' THEN 2 
            END,
            gm.joined_at DESC
    ''', (group_id,))
    
    all_requests = cursor.fetchall()
    
    # Separate pending and rejected
    pending_members = [m for m in all_requests if m['status'] == 'pending']
    rejected_members = [m for m in all_requests if m['status'] == 'rejected']
    
    # Get active members count
    cursor.execute('SELECT COUNT(*) FROM group_members WHERE group_id = ? AND status = ?', 
                  (group_id, 'active'))
    active_count = cursor.fetchone()[0]
    
    conn.close()
    
    return render_template('manage_requests.html', 
                         group=group, 
                         pending_members=pending_members,
                         rejected_members=rejected_members,
                         active_count=active_count)

@app.route('/groups/<int:group_id>')
@login_required
def group_detail(group_id):
    """Group detail page with progress and contributions"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if user is active member of this group
    cursor.execute('SELECT id FROM group_members WHERE group_id = ? AND user_id = ? AND status = ?', 
                  (group_id, current_user.id, 'active'))
    if not cursor.fetchone():
        flash('Vous n\'êtes pas membre actif de ce groupe', 'error')
        return redirect(url_for('dashboard'))
    
    # Get group details
    cursor.execute('SELECT * FROM groups WHERE id = ?', (group_id,))
    group = cursor.fetchone()
    
    # Get group members (only active)
    cursor.execute('''
        SELECT u.username, u.email, u.profile_picture, gm.joined_at, gm.status
        FROM group_members gm
        JOIN users u ON gm.user_id = u.id
        WHERE gm.group_id = ? AND gm.status = 'active'
        ORDER BY gm.joined_at
    ''', (group_id,))
    
    members = cursor.fetchall()
    
    # Get pending and rejected members (only for admin)
    pending_members = []
    rejected_members = []
    is_admin = (group['created_by'] == current_user.id)
    if is_admin:
        cursor.execute('''
            SELECT gm.id as membership_id, u.id as user_id, u.username, u.email, u.profile_picture, gm.joined_at, gm.status
            FROM group_members gm
            JOIN users u ON gm.user_id = u.id
            WHERE gm.group_id = ? AND gm.status IN ('pending', 'rejected')
            ORDER BY gm.status, gm.joined_at
        ''', (group_id,))
        all_requests = cursor.fetchall()
        
        # Separate pending and rejected
        pending_members = [m for m in all_requests if m['status'] == 'pending']
        rejected_members = [m for m in all_requests if m['status'] == 'rejected']
    
    # Get total approved contributions only
    cursor.execute('SELECT COALESCE(SUM(amount), 0) FROM contributions WHERE group_id = ? AND status = "approved"', (group_id,))
    total_contributed = cursor.fetchone()[0]
    
    # Get pending contributions (only for admin)
    pending_contributions = []
    if is_admin:
        cursor.execute('''
            SELECT c.id, c.amount, c.description, c.proof_image, c.contribution_date, c.user_id, u.username, u.profile_picture
            FROM contributions c
            JOIN users u ON c.user_id = u.id
            WHERE c.group_id = ? AND c.status = 'pending'
            ORDER BY c.contribution_date DESC
        ''', (group_id,))
        pending_contributions = cursor.fetchall()
    
    # Get approved contributions history only
    cursor.execute('''
        SELECT c.amount, c.description, c.contribution_date, u.username, u.profile_picture, c.proof_image
        FROM contributions c
        JOIN users u ON c.user_id = u.id
        WHERE c.group_id = ? AND c.status = 'approved'
        ORDER BY c.contribution_date DESC
    ''', (group_id,))
    
    contributions = cursor.fetchall()
    
    # Calculate progress percentage
    progress_percentage = (total_contributed / group['target_amount']) * 100 if group['target_amount'] > 0 else 0

    conn.close()
    
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
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if user is active member of this group
        cursor.execute('SELECT id FROM group_members WHERE group_id = ? AND user_id = ? AND status = ?', 
                      (group_id, current_user.id, 'active'))
        if not cursor.fetchone():
            flash('Vous n\'êtes pas membre actif de ce groupe', 'error')
            conn.close()
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
        # If proof image provided, requires admin approval
        # If no proof image, auto-approved
        status = 'pending' if proof_image else 'approved'
        
        # Add contribution
        cursor.execute('''
            INSERT INTO contributions (group_id, user_id, amount, description, proof_image, status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (group_id, current_user.id, amount, description, proof_image, status))
        
        # Get group info
        cursor.execute('SELECT name, created_by FROM groups WHERE id = ?', (group_id,))
        group_data = cursor.fetchone()
        group_name = group_data['name']
        admin_id = group_data['created_by']
        
        if status == 'pending':
            # Notify admin to review the contribution
            cursor.execute('''
                INSERT INTO notifications (user_id, group_id, message)
                VALUES (?, ?, ?)
            ''', (admin_id, group_id, f'{current_user.username} submitted a contribution of {amount} MAD with proof image for review in "{group_name}"'))
            flash(f'Contribution de {amount} MAD soumise ! En attente de l\'approbation de l\'admin.', 'info')
        else:
            # Auto-approved, create notifications for other members
            cursor.execute('''
                SELECT user_id FROM group_members 
                WHERE group_id = ? AND user_id != ? AND status = 'active'
            ''', (group_id, current_user.id))
            
            for member in cursor.fetchall():
                cursor.execute('''
                    INSERT INTO notifications (user_id, group_id, message)
                    VALUES (?, ?, ?)
                ''', (member['user_id'], group_id, f'{current_user.username} contributed {amount} MAD to "{group_name}"'))
            
            flash(f'Contribution de {amount} MAD ajoutée avec succès !', 'success')
        
        conn.commit()
        conn.close()
        
        return redirect(url_for('group_detail', group_id=group_id))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM groups WHERE id = ?', (group_id,))
    group = cursor.fetchone()
    conn.close()
    
    return render_template('contribute.html', group=group)

@app.route('/groups/<int:group_id>/contributions/<int:contribution_id>/approve', methods=['POST'])
@login_required
def approve_contribution(group_id, contribution_id):
    """Approve a pending contribution (admin only)"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if current user is admin of the group
    cursor.execute('SELECT created_by, name FROM groups WHERE id = ?', (group_id,))
    group = cursor.fetchone()
    
    if not group or group['created_by'] != current_user.id:
        conn.close()
        return jsonify({'status': 'error', 'message': 'Accès non autorisé'}), 403
    
    # Check if contribution exists and is pending
    cursor.execute('SELECT id, user_id, amount, status FROM contributions WHERE id = ? AND group_id = ? AND status = ?', 
                  (contribution_id, group_id, 'pending'))
    contribution = cursor.fetchone()
    
    if not contribution:
        conn.close()
        return jsonify({'status': 'error', 'message': 'Contribution introuvable'}), 404
    
    # Update status to approved
    cursor.execute('UPDATE contributions SET status = ? WHERE id = ?', ('approved', contribution_id))
    
    # Get contributor info
    cursor.execute('SELECT username FROM users WHERE id = ?', (contribution['user_id'],))
    username = cursor.fetchone()['username']
    
    # Notify the contributor
    cursor.execute('''
        INSERT INTO notifications (user_id, group_id, message)
        VALUES (?, ?, ?)
    ''', (contribution['user_id'], group_id, f'Your contribution of {contribution["amount"]} MAD to "{group["name"]}" has been approved!'))
    
    # Notify other group members
    cursor.execute('''
        SELECT user_id FROM group_members 
        WHERE group_id = ? AND user_id != ? AND user_id != ? AND status = 'active'
    ''', (group_id, contribution['user_id'], current_user.id))
    
    for member in cursor.fetchall():
        cursor.execute('''
            INSERT INTO notifications (user_id, group_id, message)
            VALUES (?, ?, ?)
        ''', (member['user_id'], group_id, f'{username} contributed {contribution["amount"]} MAD to "{group["name"]}"'))
    
    conn.commit()
    conn.close()
    
    return jsonify({'status': 'success', 'message': 'Contribution approuvée avec succès !'})

@app.route('/groups/<int:group_id>/contributions/<int:contribution_id>/reject', methods=['POST'])
@login_required
def reject_contribution(group_id, contribution_id):
    """Reject a pending contribution (admin only)"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if current user is admin of the group
    cursor.execute('SELECT created_by, name FROM groups WHERE id = ?', (group_id,))
    group = cursor.fetchone()
    
    if not group or group['created_by'] != current_user.id:
        conn.close()
        return jsonify({'status': 'error', 'message': 'Accès non autorisé'}), 403
    
    # Check if contribution exists and is pending
    cursor.execute('SELECT id, user_id, amount FROM contributions WHERE id = ? AND group_id = ? AND status = ?', 
                  (contribution_id, group_id, 'pending'))
    contribution = cursor.fetchone()
    
    if not contribution:
        conn.close()
        return jsonify({'status': 'error', 'message': 'Contribution introuvable'}), 404
    
    # Update status to rejected
    cursor.execute('UPDATE contributions SET status = ? WHERE id = ?', ('rejected', contribution_id))
    
    # Notify the contributor
    cursor.execute('''
        INSERT INTO notifications (user_id, group_id, message)
        VALUES (?, ?, ?)
    ''', (contribution['user_id'], group_id, f'Your contribution of {contribution["amount"]} MAD to "{group["name"]}" has been rejected. Please contact the admin for more info.'))
    
    conn.commit()
    conn.close()
    
    return jsonify({'status': 'success', 'message': 'Contribution rejetée'})

@app.route('/notifications/mark_read/<int:notification_id>')
@login_required
def mark_notification_read(notification_id):
    """Mark a notification as read"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE notifications SET is_read = TRUE 
        WHERE id = ? AND user_id = ?
    ''', (notification_id, current_user.id))
    conn.commit()
    conn.close()
    
    return jsonify({'status': 'success'})

@app.route('/export/<int:group_id>')
@login_required
@premium_required
def export_group_data(group_id):
    """Export group data as CSV (Premium feature)"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if user is member of this group
    cursor.execute('SELECT id FROM group_members WHERE group_id = ? AND user_id = ?', (group_id, current_user.id))
    if not cursor.fetchone():
        flash('Vous n\'êtes pas membre de ce groupe', 'error')
        return redirect(url_for('dashboard'))
    
    # Get group data
    cursor.execute('SELECT * FROM groups WHERE id = ?', (group_id,))
    group = cursor.fetchone()
    
    cursor.execute('''
        SELECT c.amount, c.description, c.contribution_date, u.username
        FROM contributions c
        JOIN users u ON c.user_id = u.id
        WHERE c.group_id = ?
        ORDER BY c.contribution_date DESC
    ''', (group_id,))
    
    contributions = cursor.fetchall()
    conn.close()
    
    # Generate CSV content
    csv_content = f"Group: {group['name']}\n"
    csv_content += f"Target Amount: {group['target_amount']} MAD\n"
    csv_content += f"Deadline: {group['deadline'] or 'No deadline'}\n\n"
    csv_content += "Amount,Description,Date,Contributor\n"
    
    for contribution in contributions:
        csv_content += f"{contribution['amount']},{contribution['description']},{contribution['contribution_date']},{contribution['username']}\n"
    
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
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET is_premium = TRUE WHERE id = ?', (current_user.id,))
    conn.commit()
    conn.close()
    
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
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if username is taken by another user
        cursor.execute('SELECT id FROM users WHERE username = ? AND id != ?', (username, current_user.id))
        if cursor.fetchone():
            flash('Username already taken by another user', 'error')
            conn.close()
            return redirect(url_for('settings'))
        
        # Check if email is taken by another user
        cursor.execute('SELECT id FROM users WHERE email = ? AND id != ?', (email, current_user.id))
        if cursor.fetchone():
            flash('Email already taken by another user', 'error')
            conn.close()
            return redirect(url_for('settings'))
        
        # Update user information
        cursor.execute('UPDATE users SET username = ?, email = ? WHERE id = ?',
                      (username, email, current_user.id))
        rows_affected = cursor.rowcount
        conn.commit()
        
        # Verify update was successful
        if rows_affected == 0:
            flash('Error: Profile update failed', 'error')
            conn.close()
            return redirect(url_for('settings'))
        
        # Reload user from database
        cursor.execute('SELECT id, username, email, is_premium, profile_picture FROM users WHERE id = ?', (current_user.id,))
        user_data = cursor.fetchone()
        conn.close()
        
        if user_data:
            from flask_login import logout_user, login_user
            updated_user = User(user_data['id'], user_data['username'], user_data['email'], 
                               user_data['is_premium'], user_data['profile_picture'])
            logout_user()
            login_user(updated_user)
            flash('Profile updated successfully!', 'success')
        else:
            flash('Error reloading user data', 'error')
        
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
        filename = secure_filename(file.filename)
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
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET profile_picture = ? WHERE id = ?', 
                      (profile_picture_path, current_user.id))
        conn.commit()
        conn.close()
        
        # Force reload user from database
        from flask_login import logout_user, login_user
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, username, email, is_premium, profile_picture FROM users WHERE id = ?', (current_user.id,))
        user_data = cursor.fetchone()
        conn.close()
        
        if user_data:
            updated_user = User(user_data['id'], user_data['username'], user_data['email'], 
                               user_data['is_premium'], user_data['profile_picture'])
            logout_user()
            login_user(updated_user)
        
        flash('Profile picture updated successfully!', 'success')
        return redirect(url_for('settings'))
        
    except Exception as e:
        flash(f'Error uploading picture: {str(e)}', 'error')
        return redirect(url_for('settings'))

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
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if user is member
    cursor.execute('SELECT id FROM group_members WHERE group_id = ? AND user_id = ?', (group_id, current_user.id))
    if not cursor.fetchone():
        return jsonify({'error': 'Access denied'}), 403
    
    cursor.execute('SELECT target_amount FROM groups WHERE id = ?', (group_id,))
    target_amount = cursor.fetchone()[0]
    
    cursor.execute('SELECT COALESCE(SUM(amount), 0) FROM contributions WHERE group_id = ?', (group_id,))
    total_contributed = cursor.fetchone()[0]
    
    conn.close()
    
    return jsonify({
        'target': float(target_amount),
        'contributed': float(total_contributed),
        'percentage': float((total_contributed / target_amount) * 100) if target_amount > 0 else 0
    })

@app.route('/groups/<int:group_id>/approve/<int:user_id>', methods=['POST'])
@login_required
def approve_member(group_id, user_id):
    """Approve a pending or rejected member request (admin only)"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if current user is admin of the group
    cursor.execute('SELECT created_by FROM groups WHERE id = ?', (group_id,))
    group = cursor.fetchone()
    
    if not group or group['created_by'] != current_user.id:
        conn.close()
        return jsonify({'status': 'error', 'message': 'Accès non autorisé'}), 403
    
    # Check if membership exists and is pending or rejected
    cursor.execute('SELECT id, status FROM group_members WHERE group_id = ? AND user_id = ? AND status IN (?, ?)', 
                  (group_id, user_id, 'pending', 'rejected'))
    membership = cursor.fetchone()
    
    if not membership:
        conn.close()
        return jsonify({'status': 'error', 'message': 'Demande introuvable'}), 404
    
    # Update status to active
    cursor.execute('UPDATE group_members SET status = ? WHERE group_id = ? AND user_id = ?', 
                  ('active', group_id, user_id))
    
    # Get group name and user info for notification
    cursor.execute('SELECT name FROM groups WHERE id = ?', (group_id,))
    group_name = cursor.fetchone()['name']
    
    cursor.execute('SELECT username FROM users WHERE id = ?', (user_id,))
    username = cursor.fetchone()['username']
    
    # Notify the user
    cursor.execute('''
        INSERT INTO notifications (user_id, group_id, message)
        VALUES (?, ?, ?)
    ''', (user_id, group_id, f'Votre demande pour rejoindre "{group_name}" a été approuvée !'))
    
    conn.commit()
    conn.close()
    
    return jsonify({'status': 'success', 'message': f'{username} a été ajouté au groupe avec succès'})

@app.route('/groups/<int:group_id>/reject/<int:user_id>', methods=['POST'])
@login_required
def reject_member(group_id, user_id):
    """Reject a pending member request (admin only)"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if current user is admin of the group
    cursor.execute('SELECT created_by FROM groups WHERE id = ?', (group_id,))
    group = cursor.fetchone()
    
    if not group or group['created_by'] != current_user.id:
        conn.close()
        return jsonify({'status': 'error', 'message': 'Accès non autorisé'}), 403
    
    # Check if membership exists and is pending (can only reject pending requests)
    cursor.execute('SELECT id, status FROM group_members WHERE group_id = ? AND user_id = ? AND status = ?', 
                  (group_id, user_id, 'pending'))
    membership = cursor.fetchone()
    
    if not membership:
        conn.close()
        return jsonify({'status': 'error', 'message': 'Demande introuvable ou déjà traitée'}), 404
    
    # Update status to rejected
    cursor.execute('UPDATE group_members SET status = ? WHERE group_id = ? AND user_id = ?', 
                  ('rejected', group_id, user_id))
    
    # Get group name and user info for notification
    cursor.execute('SELECT name FROM groups WHERE id = ?', (group_id,))
    group_name = cursor.fetchone()['name']
    
    cursor.execute('SELECT username FROM users WHERE id = ?', (user_id,))
    username = cursor.fetchone()['username']
    
    # Notify the user
    cursor.execute('''
        INSERT INTO notifications (user_id, group_id, message)
        VALUES (?, ?, ?)
    ''', (user_id, group_id, f'Votre demande pour rejoindre "{group_name}" a été refusée.'))
    
    conn.commit()
    conn.close()
    
    return jsonify({'status': 'success', 'message': f'La demande de {username} a été refusée'})

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
