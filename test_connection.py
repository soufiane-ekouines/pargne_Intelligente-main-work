"""
Quick test script to verify Supabase connection and basic operations
"""

from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

print("=" * 60)
print("SaveTogether - Supabase Connection Test")
print("=" * 60)
print()

# Test 1: Environment Variables
print("1️⃣  Testing Environment Variables...")
supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_ANON_KEY')

if supabase_url and supabase_key:
    print(f"   ✓ SUPABASE_URL: {supabase_url}")
    print(f"   ✓ SUPABASE_ANON_KEY: {supabase_key[:20]}...")
    print()
else:
    print("   ✗ Environment variables not found!")
    print("   Make sure .env file exists with SUPABASE_URL and SUPABASE_ANON_KEY")
    exit(1)

# Test 2: Import database module
print("2️⃣  Testing Database Module Import...")
try:
    from database import Database, db
    print("   ✓ Database module imported successfully")
    print()
except ImportError as e:
    print(f"   ✗ Failed to import database module: {e}")
    print("   Run: pip install -r requirements.txt")
    exit(1)

# Test 3: Supabase Connection
print("3️⃣  Testing Supabase Connection...")
try:
    db.init_db()
    print("   ✓ Connected to Supabase successfully!")
    print()
except Exception as e:
    print(f"   ✗ Connection failed: {e}")
    print()
    print("   Troubleshooting:")
    print("   1. Make sure you've run supabase_schema.sql in Supabase SQL Editor")
    print("   2. Verify your SUPABASE_URL and SUPABASE_ANON_KEY are correct")
    print("   3. Check internet connection")
    exit(1)

# Test 4: Test basic operations
print("4️⃣  Testing Basic Database Operations...")
try:
    # Test read operation
    from supabase import create_client
    supabase = create_client(supabase_url, supabase_key)
    
    # Check if tables exist
    tables_to_check = ['users', 'groups', 'group_members', 'contributions', 'notifications']
    print("   Checking database tables:")
    
    for table in tables_to_check:
        try:
            result = supabase.table(table).select('id').limit(1).execute()
            print(f"   ✓ Table '{table}' exists")
        except Exception as e:
            print(f"   ✗ Table '{table}' not found or error: {str(e)[:50]}...")
    
    print()
except Exception as e:
    print(f"   ✗ Error testing operations: {e}")
    print()

# Summary
print("=" * 60)
print("✅ Connection Test Complete!")
print("=" * 60)
print()
print("Next Steps:")
print("1. If all tests passed, run: python app.py")
print("2. If tables not found, run supabase_schema.sql in Supabase SQL Editor")
print("3. Access your app at: http://localhost:5000")
print()
print("For detailed setup instructions, see MIGRATION_GUIDE.md")
print("=" * 60)
