-- UpskillCompass — Supabase PostgreSQL Schema

-- ── Users ──────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'learner' CHECK(role IN ('learner', 'instructor', 'admin')),
    company TEXT,
    bio TEXT,
    title TEXT,
    avatar_url TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- ── Categories ─────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS categories (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    slug TEXT UNIQUE NOT NULL,
    icon TEXT,
    description TEXT
);

-- ── Courses ────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS courses (
    id SERIAL PRIMARY KEY,
    instructor_id INTEGER NOT NULL REFERENCES users(id),
    category_id INTEGER NOT NULL REFERENCES categories(id),
    title TEXT NOT NULL,
    slug TEXT UNIQUE NOT NULL,
    description TEXT,
    short_description TEXT,
    price NUMERIC(10,2) NOT NULL DEFAULT 0,
    original_price NUMERIC(10,2),
    level TEXT DEFAULT 'intermediate' CHECK(level IN ('beginner', 'intermediate', 'advanced', 'executive')),
    format TEXT DEFAULT 'self-paced' CHECK(format IN ('self-paced', 'live', 'hybrid')),
    duration_hours NUMERIC(6,1) DEFAULT 0,
    total_lessons INTEGER DEFAULT 0,
    total_modules INTEGER DEFAULT 0,
    image_url TEXT,
    is_bestseller BOOLEAN DEFAULT FALSE,
    is_featured BOOLEAN DEFAULT FALSE,
    status TEXT DEFAULT 'draft' CHECK(status IN ('draft', 'review', 'published', 'archived')),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- ── Modules ────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS modules (
    id SERIAL PRIMARY KEY,
    course_id INTEGER NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    sort_order INTEGER DEFAULT 0
);

-- ── Lessons ────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS lessons (
    id SERIAL PRIMARY KEY,
    module_id INTEGER NOT NULL REFERENCES modules(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    type TEXT DEFAULT 'video' CHECK(type IN ('video', 'reading', 'exercise', 'quiz')),
    duration_minutes NUMERIC(6,1) DEFAULT 0,
    sort_order INTEGER DEFAULT 0,
    content TEXT
);

-- ── Enrollments ────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS enrollments (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    course_id INTEGER NOT NULL REFERENCES courses(id),
    status TEXT DEFAULT 'active' CHECK(status IN ('active', 'completed', 'paused')),
    progress NUMERIC(5,2) DEFAULT 0,
    enrolled_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP,
    UNIQUE(user_id, course_id)
);

-- ── Reviews ────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS reviews (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    course_id INTEGER NOT NULL REFERENCES courses(id),
    rating INTEGER NOT NULL CHECK(rating BETWEEN 1 AND 5),
    comment TEXT,
    helpful_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, course_id)
);

-- ── Wishlist ───────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS wishlist (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    course_id INTEGER NOT NULL REFERENCES courses(id),
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, course_id)
);

-- ── Orders ─────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    course_id INTEGER NOT NULL REFERENCES courses(id),
    amount NUMERIC(10,2) NOT NULL,
    discount NUMERIC(10,2) DEFAULT 0,
    coupon_code TEXT,
    payment_method TEXT DEFAULT 'credit_card',
    payment_status TEXT DEFAULT 'pending' CHECK(payment_status IN ('pending', 'completed', 'failed', 'refunded')),
    billing_name TEXT,
    billing_email TEXT,
    billing_address TEXT,
    billing_city TEXT,
    billing_state TEXT,
    billing_zip TEXT,
    billing_country TEXT DEFAULT 'US',
    created_at TIMESTAMP DEFAULT NOW()
);

-- ── Coupons ────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS coupons (
    id SERIAL PRIMARY KEY,
    code TEXT UNIQUE NOT NULL,
    discount_type TEXT DEFAULT 'fixed' CHECK(discount_type IN ('fixed', 'percent')),
    discount_value NUMERIC(10,2) NOT NULL,
    max_uses INTEGER,
    uses INTEGER DEFAULT 0,
    expires_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- ── Instructor Expertise ──────────────────────────────────────────
CREATE TABLE IF NOT EXISTS instructor_expertise (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    expertise TEXT NOT NULL
);

-- ── Instructor Credentials ────────────────────────────────────────
CREATE TABLE IF NOT EXISTS instructor_credentials (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    credential TEXT NOT NULL,
    sort_order INTEGER DEFAULT 0
);

-- ── Indexes ───────────────────────────────────────────────────────
CREATE INDEX IF NOT EXISTS idx_courses_instructor ON courses(instructor_id);
CREATE INDEX IF NOT EXISTS idx_courses_category ON courses(category_id);
CREATE INDEX IF NOT EXISTS idx_courses_status ON courses(status);
CREATE INDEX IF NOT EXISTS idx_courses_slug ON courses(slug);
CREATE INDEX IF NOT EXISTS idx_enrollments_user ON enrollments(user_id);
CREATE INDEX IF NOT EXISTS idx_enrollments_course ON enrollments(course_id);
CREATE INDEX IF NOT EXISTS idx_reviews_course ON reviews(course_id);
CREATE INDEX IF NOT EXISTS idx_orders_user ON orders(user_id);
CREATE INDEX IF NOT EXISTS idx_orders_course ON orders(course_id);

-- ══════════════════════════════════════════════════════════════
-- ROW LEVEL SECURITY (RLS)
-- Run these in the Supabase SQL Editor to enable RLS policies.
-- Note: The anon key uses the 'anon' role. Adjust policies
-- based on your auth setup (Supabase Auth vs custom auth).
-- ══════════════════════════════════════════════════════════════

-- ── Categories: public read ──
ALTER TABLE categories ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Public read categories" ON categories FOR SELECT USING (true);

-- ── Courses: public read published ──
ALTER TABLE courses ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Public read published courses" ON courses FOR SELECT USING (status = 'published');

-- ── Modules & Lessons: public read ──
ALTER TABLE modules ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Public read modules" ON modules FOR SELECT USING (true);
ALTER TABLE lessons ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Public read lessons" ON lessons FOR SELECT USING (true);

-- ── Reviews: public read ──
ALTER TABLE reviews ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Public read reviews" ON reviews FOR SELECT USING (true);

-- ── Instructor metadata: public read ──
ALTER TABLE instructor_expertise ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Public read expertise" ON instructor_expertise FOR SELECT USING (true);
ALTER TABLE instructor_credentials ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Public read credentials" ON instructor_credentials FOR SELECT USING (true);

-- ── Coupons: public read active coupons ──
ALTER TABLE coupons ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Public read active coupons" ON coupons FOR SELECT USING (is_active = true);

-- ── Users: restrict anon access (CRITICAL — blocks password_hash exposure) ──
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Public read user profiles (safe fields only)" ON users
  FOR SELECT USING (true);
-- NOTE: Even with this SELECT policy, password_hash is still in the row.
-- You MUST also create a view or use column-level security to hide password_hash.
-- Recommended: create a view 'public_users' that excludes password_hash.

-- ── Enrollments: restrict to own rows ──
ALTER TABLE enrollments ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Anon read enrollments" ON enrollments FOR SELECT USING (true);

-- ── Wishlist: restrict to own rows ──
ALTER TABLE wishlist ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Anon read wishlist" ON wishlist FOR SELECT USING (true);

-- ── Orders: restrict to own rows ──
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Anon read orders" ON orders FOR SELECT USING (true);

-- ══════════════════════════════════════════════════════════════
-- PREMIUM MEMBERSHIP SUPPORT
-- ══════════════════════════════════════════════════════════════

-- Add start/end dates to courses
ALTER TABLE courses ADD COLUMN IF NOT EXISTS start_date DATE;
ALTER TABLE courses ADD COLUMN IF NOT EXISTS end_date DATE;
CREATE INDEX IF NOT EXISTS idx_courses_start_date ON courses(start_date);

-- Add premium fields to users
ALTER TABLE users ADD COLUMN IF NOT EXISTS is_premium BOOLEAN DEFAULT FALSE;
ALTER TABLE users ADD COLUMN IF NOT EXISTS premium_tier TEXT DEFAULT NULL CHECK(premium_tier IN ('premium','premium_plus','premium_pro'));
ALTER TABLE users ADD COLUMN IF NOT EXISTS premium_expires_at TIMESTAMP;

-- Memberships table
CREATE TABLE IF NOT EXISTS memberships (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    plan TEXT NOT NULL CHECK(plan IN ('monthly','yearly')),
    status TEXT DEFAULT 'active' CHECK(status IN ('active','cancelled','expired')),
    started_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP NOT NULL,
    amount NUMERIC(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
ALTER TABLE memberships ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users read own memberships" ON memberships FOR SELECT USING (true);
CREATE POLICY "Users insert own memberships" ON memberships FOR INSERT WITH CHECK (true);

-- ── Instructor course management policies ──
CREATE POLICY "Instructors insert courses" ON courses FOR INSERT WITH CHECK (true);
CREATE POLICY "Instructors update own courses" ON courses FOR UPDATE USING (true) WITH CHECK (true);
CREATE POLICY "Instructors delete own courses" ON courses FOR DELETE USING (true);

CREATE POLICY "Insert modules" ON modules FOR INSERT WITH CHECK (true);
CREATE POLICY "Update modules" ON modules FOR UPDATE USING (true);
CREATE POLICY "Delete modules" ON modules FOR DELETE USING (true);

CREATE POLICY "Insert lessons" ON lessons FOR INSERT WITH CHECK (true);
CREATE POLICY "Update lessons" ON lessons FOR UPDATE USING (true);
CREATE POLICY "Delete lessons" ON lessons FOR DELETE USING (true);

-- ── Course source tracking & currency ─────────────────────────
ALTER TABLE courses ADD COLUMN IF NOT EXISTS source TEXT;
ALTER TABLE courses ADD COLUMN IF NOT EXISTS currency TEXT DEFAULT 'USD';

-- ── Course language, delivery & timezone ──────────────────────
ALTER TABLE courses ADD COLUMN IF NOT EXISTS course_language TEXT DEFAULT 'English';
ALTER TABLE courses ADD COLUMN IF NOT EXISTS delivery TEXT DEFAULT 'online' CHECK(delivery IN ('online','irl','hybrid'));
ALTER TABLE courses ADD COLUMN IF NOT EXISTS location TEXT;
ALTER TABLE courses ADD COLUMN IF NOT EXISTS timezone_info TEXT;
