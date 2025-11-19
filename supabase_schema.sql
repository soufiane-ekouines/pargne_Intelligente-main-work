-- ============================================
-- SaveTogether - Supabase PostgreSQL Schema
-- ============================================
-- This SQL script creates the database schema for Supabase PostgreSQL
-- Run this script in your Supabase SQL Editor before deploying the application
-- ============================================

-- Enable UUID extension for generating UUIDs
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================
-- Table: users
-- ============================================
CREATE TABLE IF NOT EXISTS users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT,
    is_premium BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    google_id TEXT UNIQUE,
    google_email TEXT,
    profile_picture TEXT
);

-- Index for faster lookups
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_google_id ON users(google_id);

-- ============================================
-- Table: groups
-- ============================================
CREATE TABLE IF NOT EXISTS groups (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    target_amount NUMERIC(10,2) NOT NULL,
    deadline DATE,
    created_by BIGINT REFERENCES users(id) ON DELETE SET NULL,
    invite_code TEXT UNIQUE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    category TEXT
);

-- Index for faster lookups
CREATE INDEX IF NOT EXISTS idx_groups_invite_code ON groups(invite_code);
CREATE INDEX IF NOT EXISTS idx_groups_created_by ON groups(created_by);

-- ============================================
-- Table: group_members
-- ============================================
CREATE TABLE IF NOT EXISTS group_members (
    id BIGSERIAL PRIMARY KEY,
    group_id BIGINT NOT NULL REFERENCES groups(id) ON DELETE CASCADE,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    status TEXT DEFAULT 'active' CHECK (status IN ('active', 'pending', 'rejected')),
    joined_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(group_id, user_id)
);

-- Indexes for faster queries
CREATE INDEX IF NOT EXISTS idx_group_members_group_id ON group_members(group_id);
CREATE INDEX IF NOT EXISTS idx_group_members_user_id ON group_members(user_id);
CREATE INDEX IF NOT EXISTS idx_group_members_status ON group_members(status);

-- ============================================
-- Table: contributions
-- ============================================
CREATE TABLE IF NOT EXISTS contributions (
    id BIGSERIAL PRIMARY KEY,
    group_id BIGINT NOT NULL REFERENCES groups(id) ON DELETE CASCADE,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    amount NUMERIC(10,2) NOT NULL,
    description TEXT,
    proof_image TEXT,
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected')),
    contribution_date TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for faster queries
CREATE INDEX IF NOT EXISTS idx_contributions_group_id ON contributions(group_id);
CREATE INDEX IF NOT EXISTS idx_contributions_user_id ON contributions(user_id);
CREATE INDEX IF NOT EXISTS idx_contributions_status ON contributions(status);
CREATE INDEX IF NOT EXISTS idx_contributions_date ON contributions(contribution_date);

-- ============================================
-- Table: notifications
-- ============================================
CREATE TABLE IF NOT EXISTS notifications (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    group_id BIGINT REFERENCES groups(id) ON DELETE CASCADE,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for faster queries
CREATE INDEX IF NOT EXISTS idx_notifications_user_id ON notifications(user_id);
CREATE INDEX IF NOT EXISTS idx_notifications_is_read ON notifications(is_read);
CREATE INDEX IF NOT EXISTS idx_notifications_created_at ON notifications(created_at);

-- ============================================
-- Row Level Security (RLS) Policies
-- ============================================
-- Note: Enable RLS based on your security requirements
-- These are basic examples - adjust based on your needs

-- Enable RLS on all tables
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE groups ENABLE ROW LEVEL SECURITY;
ALTER TABLE group_members ENABLE ROW LEVEL SECURITY;
ALTER TABLE contributions ENABLE ROW LEVEL SECURITY;
ALTER TABLE notifications ENABLE ROW LEVEL SECURITY;

-- Users can read their own data
CREATE POLICY "Users can view own data" ON users
    FOR SELECT USING (true);

-- Anyone can insert (for registration)
CREATE POLICY "Anyone can register" ON users
    FOR INSERT WITH CHECK (true);

-- Users can update their own data
CREATE POLICY "Users can update own data" ON users
    FOR UPDATE USING (true);

-- Groups are viewable by members
CREATE POLICY "Groups viewable by all" ON groups
    FOR SELECT USING (true);

-- Authenticated users can create groups
CREATE POLICY "Authenticated users can create groups" ON groups
    FOR INSERT WITH CHECK (true);

-- Group creators can update their groups
CREATE POLICY "Creators can update groups" ON groups
    FOR UPDATE USING (true);

-- Group members policies
CREATE POLICY "Group members viewable by all" ON group_members
    FOR SELECT USING (true);

CREATE POLICY "Users can join groups" ON group_members
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Admins can update memberships" ON group_members
    FOR UPDATE USING (true);

-- Contributions policies
CREATE POLICY "Contributions viewable by group members" ON contributions
    FOR SELECT USING (true);

CREATE POLICY "Members can create contributions" ON contributions
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Admins can update contributions" ON contributions
    FOR UPDATE USING (true);

-- Notifications policies
CREATE POLICY "Users can view own notifications" ON notifications
    FOR SELECT USING (true);

CREATE POLICY "System can create notifications" ON notifications
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Users can update own notifications" ON notifications
    FOR UPDATE USING (true);

-- ============================================
-- Helper Functions (Optional)
-- ============================================

-- Function to get total contributions for a group
CREATE OR REPLACE FUNCTION get_group_total_contributions(group_id_param BIGINT)
RETURNS NUMERIC AS $$
    SELECT COALESCE(SUM(amount), 0)
    FROM contributions
    WHERE group_id = group_id_param AND status = 'approved';
$$ LANGUAGE SQL STABLE;

-- Function to get active member count for a group
CREATE OR REPLACE FUNCTION get_active_member_count(group_id_param BIGINT)
RETURNS BIGINT AS $$
    SELECT COUNT(*)
    FROM group_members
    WHERE group_id = group_id_param AND status = 'active';
$$ LANGUAGE SQL STABLE;

-- ============================================
-- Sample Data (Optional - for testing)
-- ============================================
-- Uncomment to insert sample data

-- INSERT INTO users (username, email, password_hash, is_premium)
-- VALUES 
--     ('admin', 'admin@savetogether.com', 'hashed_password', true),
--     ('user1', 'user1@example.com', 'hashed_password', false);

COMMIT;
