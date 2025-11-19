"""
Database module for Supabase PostgreSQL
Handles all database operations using Supabase Python client
"""

import os
from supabase import create_client, Client
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Supabase configuration
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_ANON_KEY = os.getenv('SUPABASE_ANON_KEY')

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)


class Database:
    """Database operations wrapper for Supabase"""
    
    @staticmethod
    def init_db():
        """
        Initialize database - verify connection
        Schema should be created manually in Supabase SQL Editor using supabase_schema.sql
        """
        try:
            # Test connection by querying users table
            supabase.table('users').select('id').limit(1).execute()
            print("✓ Supabase connection successful")
        except Exception as e:
            print(f"✗ Supabase connection failed: {str(e)}")
            raise
    
    # ==================== USER OPERATIONS ====================
    
    @staticmethod
    def create_user(username, email, password_hash, google_id=None, google_email=None, profile_picture=None):
        """Create a new user"""
        data = {
            'username': username,
            'email': email,
            'password_hash': password_hash or '',
            'google_id': google_id,
            'google_email': google_email,
            'profile_picture': profile_picture
        }
        result = supabase.table('users').insert(data).execute()
        return result.data[0] if result.data else None
    
    @staticmethod
    def get_user_by_id(user_id):
        """Get user by ID"""
        result = supabase.table('users').select('*').eq('id', user_id).execute()
        return result.data[0] if result.data else None
    
    @staticmethod
    def get_user_by_username(username):
        """Get user by username"""
        result = supabase.table('users').select('*').eq('username', username).execute()
        return result.data[0] if result.data else None
    
    @staticmethod
    def get_user_by_email(email):
        """Get user by email"""
        result = supabase.table('users').select('*').eq('email', email).execute()
        return result.data[0] if result.data else None
    
    @staticmethod
    def get_user_by_google_id(google_id):
        """Get user by Google ID"""
        result = supabase.table('users').select('*').eq('google_id', google_id).execute()
        return result.data[0] if result.data else None
    
    @staticmethod
    def update_user(user_id, **kwargs):
        """Update user information"""
        result = supabase.table('users').update(kwargs).eq('id', user_id).execute()
        return result.data[0] if result.data else None
    
    @staticmethod
    def update_user_premium(user_id, is_premium):
        """Update user premium status"""
        result = supabase.table('users').update({'is_premium': is_premium}).eq('id', user_id).execute()
        return result.data[0] if result.data else None
    
    # ==================== GROUP OPERATIONS ====================
    
    @staticmethod
    def create_group(name, description, category, target_amount, deadline, created_by, invite_code):
        """Create a new group"""
        data = {
            'name': name,
            'description': description,
            'category': category,
            'target_amount': target_amount,
            'deadline': deadline,
            'created_by': created_by,
            'invite_code': invite_code
        }
        result = supabase.table('groups').insert(data).execute()
        return result.data[0] if result.data else None
    
    @staticmethod
    def get_group_by_id(group_id):
        """Get group by ID"""
        result = supabase.table('groups').select('*').eq('id', group_id).execute()
        return result.data[0] if result.data else None
    
    @staticmethod
    def get_group_by_invite_code(invite_code):
        """Get group by invite code"""
        result = supabase.table('groups').select('*').eq('invite_code', invite_code).execute()
        return result.data[0] if result.data else None
    
    @staticmethod
    def get_user_groups(user_id):
        """Get all groups for a user (only active memberships)"""
        # First get group IDs where user is active member
        memberships = supabase.table('group_members')\
            .select('group_id')\
            .eq('user_id', user_id)\
            .eq('status', 'active')\
            .execute()
        
        if not memberships.data:
            return []
        
        group_ids = [m['group_id'] for m in memberships.data]
        
        # Get groups with additional info
        groups = []
        for group_id in group_ids:
            # Get group details
            group_result = supabase.table('groups').select('*').eq('id', group_id).execute()
            if not group_result.data:
                continue
            
            group = group_result.data[0]
            
            # Get total contributed (approved only)
            contrib_result = supabase.table('contributions')\
                .select('amount')\
                .eq('group_id', group_id)\
                .eq('status', 'approved')\
                .execute()
            
            total_contributed = sum(float(c['amount']) for c in contrib_result.data) if contrib_result.data else 0
            
            # Get member count (active only)
            member_result = supabase.table('group_members')\
                .select('user_id', count='exact')\
                .eq('group_id', group_id)\
                .eq('status', 'active')\
                .execute()
            
            member_count = member_result.count if hasattr(member_result, 'count') else len(member_result.data)
            
            # Combine data
            group['total_contributed'] = total_contributed
            group['member_count'] = member_count
            groups.append(group)
        
        return sorted(groups, key=lambda x: x['created_at'], reverse=True)
    
    # ==================== GROUP MEMBER OPERATIONS ====================
    
    @staticmethod
    def add_group_member(group_id, user_id, status='active'):
        """Add a member to a group"""
        data = {
            'group_id': group_id,
            'user_id': user_id,
            'status': status
        }
        result = supabase.table('group_members').insert(data).execute()
        return result.data[0] if result.data else None
    
    @staticmethod
    def get_group_membership(group_id, user_id):
        """Check if user is member of group"""
        result = supabase.table('group_members')\
            .select('*')\
            .eq('group_id', group_id)\
            .eq('user_id', user_id)\
            .execute()
        return result.data[0] if result.data else None
    
    @staticmethod
    def get_group_members(group_id, status='active'):
        """Get all members of a group with specific status"""
        result = supabase.table('group_members')\
            .select('*, users(*)')\
            .eq('group_id', group_id)\
            .eq('status', status)\
            .order('joined_at')\
            .execute()
        return result.data if result.data else []
    
    @staticmethod
    def get_pending_and_rejected_members(group_id):
        """Get pending and rejected members"""
        result = supabase.table('group_members')\
            .select('*, users(*)')\
            .eq('group_id', group_id)\
            .in_('status', ['pending', 'rejected'])\
            .order('joined_at', desc=True)\
            .execute()
        return result.data if result.data else []
    
    @staticmethod
    def update_member_status(group_id, user_id, status):
        """Update member status"""
        result = supabase.table('group_members')\
            .update({'status': status})\
            .eq('group_id', group_id)\
            .eq('user_id', user_id)\
            .execute()
        return result.data[0] if result.data else None
    
    @staticmethod
    def get_active_member_count(group_id):
        """Get count of active members"""
        result = supabase.table('group_members')\
            .select('id', count='exact')\
            .eq('group_id', group_id)\
            .eq('status', 'active')\
            .execute()
        return result.count if hasattr(result, 'count') else len(result.data)
    
    # ==================== CONTRIBUTION OPERATIONS ====================
    
    @staticmethod
    def create_contribution(group_id, user_id, amount, description, proof_image, status='pending'):
        """Create a new contribution"""
        data = {
            'group_id': group_id,
            'user_id': user_id,
            'amount': amount,
            'description': description,
            'proof_image': proof_image,
            'status': status
        }
        result = supabase.table('contributions').insert(data).execute()
        return result.data[0] if result.data else None
    
    @staticmethod
    def get_contribution_by_id(contribution_id):
        """Get contribution by ID"""
        result = supabase.table('contributions').select('*').eq('id', contribution_id).execute()
        return result.data[0] if result.data else None
    
    @staticmethod
    def get_group_contributions(group_id, status='approved'):
        """Get contributions for a group"""
        result = supabase.table('contributions')\
            .select('*, users(username, profile_picture)')\
            .eq('group_id', group_id)\
            .eq('status', status)\
            .order('contribution_date', desc=True)\
            .execute()
        return result.data if result.data else []
    
    @staticmethod
    def get_pending_contributions(group_id):
        """Get pending contributions for a group"""
        result = supabase.table('contributions')\
            .select('*, users(username, profile_picture)')\
            .eq('group_id', group_id)\
            .eq('status', 'pending')\
            .order('contribution_date', desc=True)\
            .execute()
        return result.data if result.data else []
    
    @staticmethod
    def get_recent_contributions(user_id, limit=10):
        """Get recent approved contributions for user's groups"""
        # Get user's group IDs
        memberships = supabase.table('group_members')\
            .select('group_id')\
            .eq('user_id', user_id)\
            .execute()
        
        if not memberships.data:
            return []
        
        group_ids = [m['group_id'] for m in memberships.data]
        
        # Get contributions
        result = supabase.table('contributions')\
            .select('*, groups(name), users(username)')\
            .in_('group_id', group_ids)\
            .eq('status', 'approved')\
            .order('contribution_date', desc=True)\
            .limit(limit)\
            .execute()
        
        return result.data if result.data else []
    
    @staticmethod
    def update_contribution_status(contribution_id, status):
        """Update contribution status"""
        result = supabase.table('contributions')\
            .update({'status': status})\
            .eq('id', contribution_id)\
            .execute()
        return result.data[0] if result.data else None
    
    @staticmethod
    def get_total_contributions(group_id, status='approved'):
        """Get total contributions for a group"""
        result = supabase.table('contributions')\
            .select('amount')\
            .eq('group_id', group_id)\
            .eq('status', status)\
            .execute()
        
        total = sum(float(c['amount']) for c in result.data) if result.data else 0
        return total
    
    @staticmethod
    def get_all_contributions_for_analytics(group_id):
        """Get all approved contributions for analytics"""
        result = supabase.table('contributions')\
            .select('*, users(username, profile_picture)')\
            .eq('group_id', group_id)\
            .eq('status', 'approved')\
            .order('contribution_date')\
            .execute()
        return result.data if result.data else []
    
    @staticmethod
    def get_member_contribution_stats(group_id):
        """Get contribution statistics by member"""
        # Get all active members
        members = supabase.table('group_members')\
            .select('user_id, users(username, profile_picture)')\
            .eq('group_id', group_id)\
            .eq('status', 'active')\
            .execute()
        
        if not members.data:
            return []
        
        stats = []
        for member in members.data:
            user_id = member['user_id']
            
            # Get contributions for this member
            contribs = supabase.table('contributions')\
                .select('amount, contribution_date')\
                .eq('group_id', group_id)\
                .eq('user_id', user_id)\
                .eq('status', 'approved')\
                .execute()
            
            total = sum(float(c['amount']) for c in contribs.data) if contribs.data else 0
            count = len(contribs.data) if contribs.data else 0
            last_date = max([c['contribution_date'] for c in contribs.data]) if contribs.data else None
            
            stats.append({
                'username': member['users']['username'],
                'profile_picture': member['users']['profile_picture'],
                'total': total,
                'count': count,
                'last_date': last_date
            })
        
        return sorted(stats, key=lambda x: x['total'], reverse=True)
    
    # ==================== NOTIFICATION OPERATIONS ====================
    
    @staticmethod
    def create_notification(user_id, group_id, message):
        """Create a new notification"""
        data = {
            'user_id': user_id,
            'group_id': group_id,
            'message': message
        }
        result = supabase.table('notifications').insert(data).execute()
        return result.data[0] if result.data else None
    
    @staticmethod
    def get_user_notifications(user_id, is_read=False):
        """Get notifications for a user"""
        result = supabase.table('notifications')\
            .select('*')\
            .eq('user_id', user_id)\
            .eq('is_read', is_read)\
            .order('created_at', desc=True)\
            .execute()
        return result.data if result.data else []
    
    @staticmethod
    def mark_notification_read(notification_id, user_id):
        """Mark notification as read"""
        result = supabase.table('notifications')\
            .update({'is_read': True})\
            .eq('id', notification_id)\
            .eq('user_id', user_id)\
            .execute()
        return result.data[0] if result.data else None
    
    # ==================== EXPORT OPERATIONS ====================
    
    @staticmethod
    def get_group_export_data(group_id):
        """Get all data for group export"""
        # Get group
        group = Database.get_group_by_id(group_id)
        
        # Get contributions
        contributions = supabase.table('contributions')\
            .select('amount, description, contribution_date, users(username)')\
            .eq('group_id', group_id)\
            .order('contribution_date', desc=True)\
            .execute()
        
        return {
            'group': group,
            'contributions': contributions.data if contributions.data else []
        }


# Singleton instance
db = Database()
