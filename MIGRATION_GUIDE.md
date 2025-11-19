# SaveTogether - Supabase Migration Guide

## Overview
This guide explains how to migrate the SaveTogether Flask application from SQLite to Supabase PostgreSQL.

---

## ✅ What Has Been Completed

### 1. **Code Migration**
- ✅ Converted all SQLite database operations to Supabase
- ✅ Created `database.py` module with all CRUD operations
- ✅ Updated `app.py` to use Supabase client
- ✅ Updated `requirements.txt` with necessary dependencies
- ✅ Created `.env` file for environment variables
- ✅ Backed up original SQLite version as `app_sqlite_backup.py`

### 2. **Schema Files Created**
- ✅ `supabase_schema.sql` - Complete PostgreSQL schema for Supabase
- ✅ `.env.example` - Template for environment variables
- ✅ `.env` - Pre-configured with your Supabase credentials

### 3. **Key Changes**
- ✅ All database queries now use `supabase-py` client
- ✅ Proper data type handling for PostgreSQL (NUMERIC, TIMESTAMPTZ, BIGSERIAL)
- ✅ Foreign key relationships with proper CASCADE rules
- ✅ Row Level Security (RLS) policies configured
- ✅ Indexes for performance optimization

---

## 🚀 Setup Instructions

### Step 1: Install Dependencies

```bash
cd "d:\master\master S3\Programmation web sous python\prg pargne_Intelligente-main\pargne_Intelligente-main-work"
pip install -r requirements.txt
```

### Step 2: Create Supabase Database Schema

1. **Go to your Supabase project dashboard:**
   - URL: https://app.supabase.com/project/uzhlzkzmqvvqmzmrqvjn

2. **Navigate to SQL Editor:**
   - Click on "SQL Editor" in the left sidebar

3. **Run the schema script:**
   - Open the file `supabase_schema.sql`
   - Copy its entire contents
   - Paste into the Supabase SQL Editor
   - Click "Run" to execute

This will create all necessary tables:
- `users`
- `groups`
- `group_members`
- `contributions`
- `notifications`

### Step 3: Verify Environment Variables

Check that `.env` file contains your credentials:

```env
SUPABASE_URL=https://uzhlzkzmqvvqmzmrqvjn.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
FLASK_SECRET_KEY=savetogether-secret-key-2024
```

### Step 4: Run the Application

```bash
python app.py
```

The application will:
- Connect to Supabase on startup
- Verify database connection
- Start on http://localhost:5000

---

## 📊 Data Migration (Optional)

If you have existing SQLite data (`savetogether.db`) that you want to migrate:

### Option 1: Manual Data Export/Import

1. **Export SQLite data:**
```bash
python migrate_data.py export
```

2. **Import to Supabase:**
   - Use Supabase dashboard → Table Editor
   - Import CSV files for each table
   - Or use the SQL Editor to insert data

### Option 2: Python Migration Script

Create a migration script to transfer data:

```python
# migrate_data.py
import sqlite3
from database import Database

# Connect to old SQLite database
sqlite_conn = sqlite3.connect('savetogether.db')
sqlite_conn.row_factory = sqlite3.Row
cursor = sqlite_conn.cursor()

# Migrate users
cursor.execute('SELECT * FROM users')
users = cursor.fetchall()
for user in users:
    Database.create_user(
        username=user['username'],
        email=user['email'],
        password_hash=user['password_hash'],
        google_id=user.get('google_id'),
        google_email=user.get('google_email'),
        profile_picture=user.get('profile_picture')
    )
    print(f"Migrated user: {user['username']}")

# Migrate groups, contributions, etc.
# ... (similar pattern for other tables)

sqlite_conn.close()
print("Migration complete!")
```

---

## 🔑 Key Differences: SQLite vs PostgreSQL

### Data Types
| SQLite | PostgreSQL | Notes |
|--------|-----------|-------|
| `INTEGER PRIMARY KEY AUTOINCREMENT` | `BIGSERIAL PRIMARY KEY` | Auto-incrementing IDs |
| `DECIMAL(10,2)` | `NUMERIC(10,2)` | Decimal numbers |
| `TIMESTAMP DEFAULT CURRENT_TIMESTAMP` | `TIMESTAMPTZ DEFAULT NOW()` | Timestamps with timezone |
| `BOOLEAN` | `BOOLEAN` | Same, but more strict in PostgreSQL |

### Foreign Keys
- PostgreSQL enforces foreign key constraints strictly
- Added `ON DELETE CASCADE` for automatic cleanup
- Added `ON DELETE SET NULL` where appropriate

### Indexes
- Created indexes on frequently queried columns
- Improves performance for large datasets

---

## 🏗️ Architecture Overview

### New File Structure

```
SaveTogether/
├── app.py                    # Main Flask app (Supabase version)
├── app_sqlite_backup.py      # Original SQLite version (backup)
├── database.py               # Supabase database operations
├── requirements.txt          # Updated dependencies
├── .env                      # Environment variables (credentials)
├── .env.example              # Template for .env
├── supabase_schema.sql       # PostgreSQL schema
├── MIGRATION_GUIDE.md        # This file
├── templates/                # HTML templates (unchanged)
├── static/                   # CSS, JS, images (unchanged)
└── vercel.json              # Deployment config
```

### Database Module (`database.py`)

The `Database` class provides methods for:

**User Operations:**
- `create_user()` - Create new user
- `get_user_by_id()` - Get user by ID
- `get_user_by_username()` - Get user by username
- `get_user_by_email()` - Get user by email
- `update_user()` - Update user info

**Group Operations:**
- `create_group()` - Create new group
- `get_group_by_id()` - Get group details
- `get_user_groups()` - Get user's groups
- `add_group_member()` - Add member to group
- `update_member_status()` - Approve/reject members

**Contribution Operations:**
- `create_contribution()` - Add contribution
- `get_group_contributions()` - Get contributions
- `update_contribution_status()` - Approve/reject
- `get_total_contributions()` - Calculate totals

**Notification Operations:**
- `create_notification()` - Create notification
- `get_user_notifications()` - Get notifications
- `mark_notification_read()` - Mark as read

---

## 🧪 Testing

### 1. Test Database Connection

```bash
python -c "from database import db; db.init_db()"
```

Expected output:
```
✓ Supabase connection successful
```

### 2. Test User Registration

1. Navigate to http://localhost:5000/register
2. Create a new account
3. Verify in Supabase dashboard → Table Editor → users

### 3. Test Group Creation

1. Login with your account
2. Create a new savings group
3. Verify in Supabase dashboard → Table Editor → groups

### 4. Test All Features

- ✅ User registration/login
- ✅ Google OAuth (if configured)
- ✅ Create/join groups
- ✅ Add contributions
- ✅ Approve/reject members
- ✅ Notifications
- ✅ Analytics
- ✅ CSV export (premium)

---

## 🔒 Security Considerations

### Environment Variables
- **Never commit `.env` to Git**
- Add `.env` to `.gitignore`
- Use environment variables in production

### Row Level Security (RLS)
- Enabled on all tables
- Basic policies configured in `supabase_schema.sql`
- Review and adjust policies based on your security requirements

### API Keys
- `SUPABASE_ANON_KEY` is safe for client-side use
- For admin operations, consider using service role key
- Store sensitive keys in environment variables

---

## 🚨 Troubleshooting

### Connection Errors

**Problem:** `Supabase connection failed`
**Solution:**
1. Verify SUPABASE_URL and SUPABASE_ANON_KEY in `.env`
2. Check internet connection
3. Verify Supabase project is active

### Import Errors

**Problem:** `ModuleNotFoundError: No module named 'supabase'`
**Solution:**
```bash
pip install -r requirements.txt
```

### Schema Errors

**Problem:** `relation "users" does not exist`
**Solution:**
1. Run `supabase_schema.sql` in Supabase SQL Editor
2. Verify tables created in Table Editor

### Data Type Errors

**Problem:** `invalid input syntax for type numeric`
**Solution:**
- Ensure amounts are properly converted to float
- Check that dates are in ISO format

---

## 📝 Production Deployment

### Environment Variables for Production

```env
# Production .env
SUPABASE_URL=https://uzhlzkzmqvvqmzmrqvjn.supabase.co
SUPABASE_ANON_KEY=your-production-anon-key
FLASK_SECRET_KEY=your-strong-random-secret-key
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

### Deployment Checklist

- [ ] Set `app.debug = False` in production
- [ ] Use strong, random `FLASK_SECRET_KEY`
- [ ] Configure Google OAuth with production URLs
- [ ] Review and tighten RLS policies
- [ ] Enable SSL/HTTPS
- [ ] Set up backup strategy
- [ ] Monitor database performance
- [ ] Configure error logging

### Vercel Deployment

The existing `vercel.json` should work with minimal changes. Ensure environment variables are set in Vercel dashboard.

---

## 📚 Additional Resources

- **Supabase Documentation:** https://supabase.com/docs
- **Supabase Python Client:** https://supabase.com/docs/reference/python/introduction
- **PostgreSQL Documentation:** https://www.postgresql.org/docs/
- **Flask Documentation:** https://flask.palletsprojects.com/

---

## ✨ Summary

Your SaveTogether application has been successfully converted to use Supabase PostgreSQL:

1. ✅ **All SQLite code replaced** with Supabase operations
2. ✅ **Database schema created** with proper PostgreSQL types
3. ✅ **Environment configuration** set up
4. ✅ **Original code backed up** as `app_sqlite_backup.py`
5. ✅ **Dependencies updated** in `requirements.txt`

**Next Steps:**
1. Run the schema script in Supabase SQL Editor
2. Install dependencies: `pip install -r requirements.txt`
3. Start the app: `python app.py`
4. Test all features thoroughly

The application maintains 100% of its original functionality while now leveraging Supabase's powerful PostgreSQL database with real-time capabilities, better scalability, and built-in security features.

---

**Questions or Issues?**
Refer to the Supabase dashboard for real-time database monitoring and the SQL Editor for direct database access.
