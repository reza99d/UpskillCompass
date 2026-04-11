"""
UpskillCompass — Backend API (Supabase Edition)
Flask backend using Supabase PostgreSQL via REST API.
"""

import os
import secrets
from datetime import datetime, timedelta
from functools import wraps

import jwt
import bcrypt
from flask import Flask, request, jsonify, g, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

import supabase_client as db

load_dotenv()

# ── Config ──────────────────────────────────────────────────────────
app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_hex(32))


# ── Auth helpers ────────────────────────────────────────────────────
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))


def create_token(user_id, role):
    payload = {
        'user_id': user_id,
        'role': role,
        'exp': datetime.utcnow() + timedelta(days=7),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return jsonify({'error': 'Authentication required'}), 401
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            users = db.select('users', filters=[('id', 'eq', payload['user_id'])])
            if not users:
                return jsonify({'error': 'User not found'}), 401
            g.current_user = users[0]
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        return f(*args, **kwargs)
    return decorated


def instructor_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if g.current_user['role'] != 'instructor':
            return jsonify({'error': 'Instructor access required'}), 403
        return f(*args, **kwargs)
    return decorated


# ══════════════════════════════════════════════════════════════════════
# ROUTES
# ══════════════════════════════════════════════════════════════════════

# ── Static files ────────────────────────────────────────────────────
@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')


# ── AUTH ────────────────────────────────────────────────────────────
@app.route('/api/auth/signup', methods=['POST'])
def signup():
    data = request.json
    required = ['email', 'password', 'first_name', 'last_name']
    if not all(data.get(f) for f in required):
        return jsonify({'error': 'Missing required fields'}), 400

    existing = db.select('users', columns='id', filters=[('email', 'eq', data['email'])])
    if existing:
        return jsonify({'error': 'Email already registered'}), 409

    role = data.get('role', 'learner')
    if role not in ('learner', 'instructor'):
        role = 'learner'

    user = db.insert('users', {
        'email': data['email'],
        'password_hash': hash_password(data['password']),
        'first_name': data['first_name'],
        'last_name': data['last_name'],
        'role': role,
        'company': data.get('company')
    })

    token = create_token(user['id'], role)
    return jsonify({
        'token': token,
        'user': {'id': user['id'], 'email': data['email'], 'first_name': data['first_name'],
                 'last_name': data['last_name'], 'role': role}
    }), 201


@app.route('/api/auth/signin', methods=['POST'])
def signin():
    data = request.json
    if not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password required'}), 400

    users = db.select('users', filters=[('email', 'eq', data['email'])])
    if not users or not check_password(data['password'], users[0]['password_hash']):
        return jsonify({'error': 'Invalid email or password'}), 401

    user = users[0]
    token = create_token(user['id'], user['role'])
    return jsonify({
        'token': token,
        'user': {
            'id': user['id'], 'email': user['email'],
            'first_name': user['first_name'], 'last_name': user['last_name'],
            'role': user['role']
        }
    })


@app.route('/api/auth/me')
@token_required
def get_me():
    u = g.current_user
    return jsonify({
        'id': u['id'], 'email': u['email'], 'first_name': u['first_name'],
        'last_name': u['last_name'], 'role': u['role'], 'company': u.get('company'),
        'bio': u.get('bio'), 'title': u.get('title'), 'avatar_url': u.get('avatar_url')
    })


# ── CATEGORIES ──────────────────────────────────────────────────────
@app.route('/api/categories')
def get_categories():
    cats = db.select('categories', columns='*', order='name.asc')
    # Get course counts per category
    for cat in cats:
        courses = db.select('courses', columns='id',
                            filters=[('category_id', 'eq', cat['id']), ('status', 'eq', 'published')])
        cat['course_count'] = len(courses) if courses else 0
    return jsonify(cats)


# ── COURSES ─────────────────────────────────────────────────────────
@app.route('/api/courses')
def get_courses():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 12, type=int)
    category = request.args.get('category')
    level = request.args.get('level')
    fmt = request.args.get('format')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    sort = request.args.get('sort', 'popular')
    search = request.args.get('search', '').strip()
    featured = request.args.get('featured', type=int)
    country = request.args.get('country', '').strip()       # 'sweden' or 'international'
    price_range = request.args.get('price_range', '').strip()  # e.g. '0-200', '200-500', '500+'
    instructor = request.args.get('instructor', '').strip()

    filters = [('status', 'eq', 'published')]

    if level:
        filters.append(('level', 'eq', level))
    if fmt:
        filters.append(('format', 'eq', fmt))
    if min_price is not None:
        filters.append(('price', 'gte', str(min_price)))
    if max_price is not None:
        filters.append(('price', 'lte', str(max_price)))
    if featured:
        filters.append(('is_featured', 'eq', 'true'))
    if search:
        filters.append(f'or=(title.ilike.%25{search}%25,description.ilike.%25{search}%25)')

    # Price range filter
    if price_range:
        if price_range == '500+':
            filters.append(('price', 'gte', '500'))
        elif '-' in price_range:
            parts = price_range.split('-')
            if len(parts) == 2:
                filters.append(('price', 'gte', parts[0]))
                filters.append(('price', 'lte', parts[1]))

    if category:
        cat_data = db.select('categories', columns='id', filters=[('slug', 'eq', category)])
        if cat_data:
            filters.append(('category_id', 'eq', str(cat_data[0]['id'])))

    order_map = {
        'popular': 'created_at.desc',
        'price_asc': 'price.asc',
        'price_desc': 'price.desc',
        'newest': 'created_at.desc',
    }
    order = order_map.get(sort, 'created_at.desc')

    # Swedish course slug prefixes
    SWEDISH_PREFIXES = ('wenell-', 'hjartum-', 'advantum-', 'fu-', 'ihm-', 'canea-',
                        'chefakademin-', 'efl-', 'berghs-', 'sse-', 'kth-')

    # For country / instructor filtering we need to fetch more and filter in Python
    # because Supabase REST doesn't support complex slug prefix filters
    use_post_filter = bool(country) or bool(instructor)

    if use_post_filter:
        # Fetch all matching courses (up to 200)
        courses = db.select('courses', columns='*,categories(name,slug),users!courses_instructor_id_fkey(id,first_name,last_name)',
                            filters=filters, order=order, limit=200, offset=0)
    else:
        offset = (page - 1) * per_page
        courses = db.select('courses', columns='*,categories(name,slug),users!courses_instructor_id_fkey(id,first_name,last_name)',
                            filters=filters, order=order, limit=per_page, offset=offset)

    # Enrich with reviews and enrollment counts
    for course in (courses or []):
        reviews = db.select('reviews', columns='rating', filters=[('course_id', 'eq', course['id'])])
        enrollments = db.select('enrollments', columns='id', filters=[('course_id', 'eq', course['id'])])
        ratings = [r['rating'] for r in (reviews or [])]
        course['avg_rating'] = round(sum(ratings) / len(ratings), 1) if ratings else 0
        course['review_count'] = len(ratings)
        course['enrollment_count'] = len(enrollments or [])
        # Flatten nested data
        if course.get('categories'):
            course['category_name'] = course['categories']['name']
            course['category_slug'] = course['categories']['slug']
        if course.get('users'):
            course['instructor_name'] = f"{course['users']['first_name']} {course['users']['last_name']}"
            course['instructor_user_id'] = course['users']['id']
        # Tag country
        course['country'] = 'sweden' if course.get('slug', '').startswith(SWEDISH_PREFIXES) else 'international'

    # Post-filter by country
    if country:
        courses = [c for c in (courses or []) if c.get('country') == country]

    # Post-filter by instructor name
    if instructor:
        courses = [c for c in (courses or []) if c.get('instructor_name') == instructor]

    # Sort by popularity (enrollment count) if requested
    if sort == 'popular':
        courses = sorted(courses or [], key=lambda x: x.get('enrollment_count', 0), reverse=True)
    elif sort == 'rating':
        courses = sorted(courses or [], key=lambda x: x.get('avg_rating', 0), reverse=True)

    # Paginate post-filtered results
    if use_post_filter:
        total = len(courses or [])
        offset = (page - 1) * per_page
        courses = (courses or [])[offset:offset + per_page]
    else:
        # Count total with same filters
        count_filters = [f for f in filters]
        all_courses = db.select('courses', columns='id', filters=count_filters)
        total = len(all_courses or [])

    return jsonify({
        'courses': courses or [],
        'total': total,
        'page': page,
        'per_page': per_page,
        'total_pages': (total + per_page - 1) // per_page
    })


@app.route('/api/instructors-list')
def get_instructors_list():
    """Return list of instructors with published course counts."""
    users = db.select('users', columns='id,first_name,last_name', filters=[('role', 'eq', 'instructor')])
    result = []
    for u in (users or []):
        name = f"{u['first_name']} {u['last_name']}"
        courses = db.select('courses', columns='id', filters=[('instructor_id', 'eq', u['id']), ('status', 'eq', 'published')])
        count = len(courses or [])
        if count > 0:
            result.append({'name': name, 'id': u['id'], 'course_count': count})
    result.sort(key=lambda x: x['course_count'], reverse=True)
    return jsonify(result)


@app.route('/api/courses/<int:course_id>')
def get_course(course_id):
    courses = db.select('courses',
                        columns='*,categories(name,slug),users!courses_instructor_id_fkey(id,first_name,last_name,bio,title)',
                        filters=[('id', 'eq', course_id)])
    if not courses:
        return jsonify({'error': 'Course not found'}), 404

    course = courses[0]

    # Flatten
    if course.get('categories'):
        course['category_name'] = course['categories']['name']
        course['category_slug'] = course['categories']['slug']
    if course.get('users'):
        course['instructor_name'] = f"{course['users']['first_name']} {course['users']['last_name']}"
        course['instructor_user_id'] = course['users']['id']
        course['instructor_bio'] = course['users'].get('bio')
        course['instructor_title'] = course['users'].get('title')

    # Reviews
    reviews = db.select('reviews', columns='rating', filters=[('course_id', 'eq', course_id)])
    ratings = [r['rating'] for r in (reviews or [])]
    course['avg_rating'] = round(sum(ratings) / len(ratings), 1) if ratings else 0
    course['review_count'] = len(ratings)

    # Enrollments
    enrollments = db.select('enrollments', columns='id', filters=[('course_id', 'eq', course_id)])
    course['enrollment_count'] = len(enrollments or [])

    # Curriculum
    modules = db.select('modules', filters=[('course_id', 'eq', course_id)], order='sort_order.asc')
    for mod in (modules or []):
        mod['lessons'] = db.select('lessons', filters=[('module_id', 'eq', mod['id'])], order='sort_order.asc') or []

    # Rating breakdown
    rating_breakdown = {}
    for i in range(1, 6):
        rating_breakdown[str(i)] = len([r for r in ratings if r == i])

    course['modules'] = modules or []
    course['rating_breakdown'] = rating_breakdown
    return jsonify(course)


@app.route('/api/courses/<int:course_id>/reviews')
def get_course_reviews(course_id):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    offset = (page - 1) * per_page

    reviews = db.select('reviews',
                        columns='*,users!reviews_user_id_fkey(first_name,last_name,avatar_url)',
                        filters=[('course_id', 'eq', course_id)],
                        order='created_at.desc', limit=per_page, offset=offset)

    for r in (reviews or []):
        if r.get('users'):
            r['first_name'] = r['users']['first_name']
            r['last_name'] = r['users']['last_name']
            r['avatar_url'] = r['users'].get('avatar_url')

    all_reviews = db.select('reviews', columns='id', filters=[('course_id', 'eq', course_id)])
    total = len(all_reviews or [])

    return jsonify({'reviews': reviews or [], 'total': total, 'page': page})


@app.route('/api/courses/<int:course_id>/reviews', methods=['POST'])
@token_required
def create_review(course_id):
    data = request.json
    rating = data.get('rating')
    if not rating or rating < 1 or rating > 5:
        return jsonify({'error': 'Rating must be 1-5'}), 400

    enrolled = db.select('enrollments', columns='id',
                         filters=[('user_id', 'eq', g.current_user['id']), ('course_id', 'eq', course_id)])
    if not enrolled:
        return jsonify({'error': 'Must be enrolled to review'}), 403

    existing = db.select('reviews', columns='id',
                         filters=[('user_id', 'eq', g.current_user['id']), ('course_id', 'eq', course_id)])
    if existing:
        return jsonify({'error': 'Already reviewed this course'}), 409

    review = db.insert('reviews', {
        'user_id': g.current_user['id'],
        'course_id': course_id,
        'rating': rating,
        'comment': data.get('comment')
    })
    return jsonify({'id': review['id'], 'message': 'Review created'}), 201


# ── INSTRUCTOR course management ───────────────────────────────────
@app.route('/api/instructor/courses', methods=['POST'])
@token_required
@instructor_required
def create_course():
    data = request.json
    if not all(data.get(f) for f in ['title', 'category_id', 'price']):
        return jsonify({'error': 'Missing required fields'}), 400

    slug = data['title'].lower().replace(' ', '-').replace("'", '')
    existing = db.select('courses', columns='id', filters=[('slug', 'eq', slug)])
    if existing:
        slug = f"{slug}-{secrets.token_hex(3)}"

    course = db.insert('courses', {
        'instructor_id': g.current_user['id'],
        'category_id': data['category_id'],
        'title': data['title'],
        'slug': slug,
        'description': data.get('description'),
        'short_description': data.get('short_description'),
        'price': data['price'],
        'original_price': data.get('original_price'),
        'level': data.get('level', 'intermediate'),
        'format': data.get('format', 'self-paced'),
        'duration_hours': data.get('duration_hours', 0),
        'image_url': data.get('image_url'),
        'status': data.get('status', 'draft')
    })
    return jsonify({'id': course['id'], 'slug': slug}), 201


@app.route('/api/instructor/courses/<int:course_id>', methods=['PUT'])
@token_required
@instructor_required
def update_course(course_id):
    courses = db.select('courses', columns='id',
                        filters=[('id', 'eq', course_id), ('instructor_id', 'eq', g.current_user['id'])])
    if not courses:
        return jsonify({'error': 'Course not found'}), 404

    data = request.json
    allowed = ['title', 'description', 'short_description', 'price', 'original_price',
               'level', 'format', 'duration_hours', 'image_url', 'status', 'category_id']
    updates = {k: v for k, v in data.items() if k in allowed}
    if updates:
        updates['updated_at'] = datetime.utcnow().isoformat()
        db.update('courses', updates, [('id', 'eq', course_id)])
    return jsonify({'message': 'Course updated'})


@app.route('/api/instructor/courses/<int:course_id>', methods=['DELETE'])
@token_required
@instructor_required
def delete_course(course_id):
    courses = db.select('courses', columns='id',
                        filters=[('id', 'eq', course_id), ('instructor_id', 'eq', g.current_user['id'])])
    if not courses:
        return jsonify({'error': 'Course not found'}), 404
    db.delete('courses', [('id', 'eq', course_id)])
    return jsonify({'message': 'Course deleted'})


# ── Modules & Lessons ──────────────────────────────────────────────
@app.route('/api/instructor/courses/<int:course_id>/modules', methods=['POST'])
@token_required
@instructor_required
def create_module(course_id):
    courses = db.select('courses', columns='id',
                        filters=[('id', 'eq', course_id), ('instructor_id', 'eq', g.current_user['id'])])
    if not courses:
        return jsonify({'error': 'Course not found'}), 404

    data = request.json
    existing = db.select('modules', columns='sort_order',
                         filters=[('course_id', 'eq', course_id)], order='sort_order.desc', limit=1)
    max_order = existing[0]['sort_order'] if existing else 0

    module = db.insert('modules', {
        'course_id': course_id,
        'title': data['title'],
        'sort_order': max_order + 1
    })
    return jsonify({'id': module['id']}), 201


@app.route('/api/instructor/modules/<int:module_id>/lessons', methods=['POST'])
@token_required
@instructor_required
def create_lesson(module_id):
    data = request.json
    existing = db.select('lessons', columns='sort_order',
                         filters=[('module_id', 'eq', module_id)], order='sort_order.desc', limit=1)
    max_order = existing[0]['sort_order'] if existing else 0

    lesson = db.insert('lessons', {
        'module_id': module_id,
        'title': data['title'],
        'type': data.get('type', 'video'),
        'duration_minutes': data.get('duration_minutes', 0),
        'sort_order': max_order + 1,
        'content': data.get('content')
    })
    return jsonify({'id': lesson['id']}), 201


# ── ENROLLMENT ─────────────────────────────────────────────────────
@app.route('/api/enrollments', methods=['POST'])
@token_required
def enroll():
    course_id = request.json.get('course_id')
    if not course_id:
        return jsonify({'error': 'course_id required'}), 400

    existing = db.select('enrollments', columns='id',
                         filters=[('user_id', 'eq', g.current_user['id']), ('course_id', 'eq', course_id)])
    if existing:
        return jsonify({'error': 'Already enrolled'}), 409

    enrollment = db.insert('enrollments', {
        'user_id': g.current_user['id'],
        'course_id': course_id
    })
    return jsonify({'id': enrollment['id'], 'message': 'Enrolled successfully'}), 201


@app.route('/api/enrollments')
@token_required
def get_my_enrollments():
    enrollments = db.select('enrollments',
                            columns='*,courses(title,slug,image_url,categories(name),users!courses_instructor_id_fkey(first_name,last_name))',
                            filters=[('user_id', 'eq', g.current_user['id'])],
                            order='enrolled_at.desc')
    return jsonify(enrollments or [])


# ── WISHLIST ───────────────────────────────────────────────────────
@app.route('/api/wishlist', methods=['POST'])
@token_required
def add_to_wishlist():
    course_id = request.json.get('course_id')
    existing = db.select('wishlist', columns='id',
                         filters=[('user_id', 'eq', g.current_user['id']), ('course_id', 'eq', course_id)])
    if existing:
        db.delete('wishlist', [('id', 'eq', existing[0]['id'])])
        return jsonify({'message': 'Removed from wishlist', 'wishlisted': False})

    db.insert('wishlist', {'user_id': g.current_user['id'], 'course_id': course_id})
    return jsonify({'message': 'Added to wishlist', 'wishlisted': True}), 201


@app.route('/api/wishlist')
@token_required
def get_wishlist():
    items = db.select('wishlist',
                      columns='*,courses(id,title,slug,price,original_price,image_url,users!courses_instructor_id_fkey(first_name,last_name))',
                      filters=[('user_id', 'eq', g.current_user['id'])],
                      order='created_at.desc')
    return jsonify(items or [])


# ── ORDERS / CHECKOUT ──────────────────────────────────────────────
@app.route('/api/orders', methods=['POST'])
@token_required
def create_order():
    data = request.json
    course_id = data.get('course_id')
    if not course_id:
        return jsonify({'error': 'course_id required'}), 400

    courses = db.select('courses', filters=[('id', 'eq', course_id), ('status', 'eq', 'published')])
    if not courses:
        return jsonify({'error': 'Course not found'}), 404

    course = courses[0]
    amount = float(course['price'])
    discount = 0
    coupon_code = data.get('coupon_code')

    if coupon_code:
        coupons = db.select('coupons', filters=[('code', 'eq', coupon_code), ('is_active', 'eq', 'true')])
        if coupons:
            coupon = coupons[0]
            if coupon.get('expires_at') and coupon['expires_at'] < datetime.utcnow().isoformat():
                return jsonify({'error': 'Coupon expired'}), 400
            if coupon.get('max_uses') and coupon['uses'] >= coupon['max_uses']:
                return jsonify({'error': 'Coupon usage limit reached'}), 400
            if coupon['discount_type'] == 'fixed':
                discount = float(coupon['discount_value'])
            else:
                discount = amount * (float(coupon['discount_value']) / 100)
            db.update('coupons', {'uses': coupon['uses'] + 1}, [('id', 'eq', coupon['id'])])

    final_amount = max(0, amount - discount)

    order = db.insert('orders', {
        'user_id': g.current_user['id'],
        'course_id': course_id,
        'amount': final_amount,
        'discount': discount,
        'coupon_code': coupon_code,
        'payment_method': data.get('payment_method', 'credit_card'),
        'payment_status': 'completed',
        'billing_name': data.get('billing_name'),
        'billing_email': data.get('billing_email'),
        'billing_address': data.get('billing_address'),
        'billing_city': data.get('billing_city'),
        'billing_state': data.get('billing_state'),
        'billing_zip': data.get('billing_zip'),
        'billing_country': data.get('billing_country', 'US')
    })

    # Auto-enroll
    existing = db.select('enrollments', columns='id',
                         filters=[('user_id', 'eq', g.current_user['id']), ('course_id', 'eq', course_id)])
    if not existing:
        db.insert('enrollments', {'user_id': g.current_user['id'], 'course_id': course_id})

    return jsonify({'id': order['id'], 'amount': final_amount, 'message': 'Order completed'}), 201


@app.route('/api/coupons/validate', methods=['POST'])
def validate_coupon():
    code = request.json.get('code')
    coupons = db.select('coupons', filters=[('code', 'eq', code), ('is_active', 'eq', 'true')])
    if not coupons:
        return jsonify({'valid': False, 'error': 'Invalid coupon'}), 404

    coupon = coupons[0]
    if coupon.get('expires_at') and coupon['expires_at'] < datetime.utcnow().isoformat():
        return jsonify({'valid': False, 'error': 'Coupon expired'}), 400

    return jsonify({
        'valid': True,
        'discount_type': coupon['discount_type'],
        'discount_value': float(coupon['discount_value'])
    })


# ── INSTRUCTOR PROFILE ─────────────────────────────────────────────
@app.route('/api/instructors/<int:instructor_id>')
def get_instructor(instructor_id):
    users = db.select('users', columns='id,first_name,last_name,bio,title,avatar_url,created_at',
                      filters=[('id', 'eq', instructor_id), ('role', 'eq', 'instructor')])
    if not users:
        return jsonify({'error': 'Instructor not found'}), 404

    instructor = users[0]

    # Stats
    courses = db.select('courses', columns='id',
                         filters=[('instructor_id', 'eq', instructor_id), ('status', 'eq', 'published')])
    course_ids = [c['id'] for c in (courses or [])]
    instructor['course_count'] = len(course_ids)

    total_students = 0
    total_reviews = 0
    all_ratings = []
    for cid in course_ids:
        enrollments = db.select('enrollments', columns='id', filters=[('course_id', 'eq', cid)])
        reviews = db.select('reviews', columns='rating', filters=[('course_id', 'eq', cid)])
        total_students += len(enrollments or [])
        total_reviews += len(reviews or [])
        all_ratings.extend([r['rating'] for r in (reviews or [])])

    instructor['total_students'] = total_students
    instructor['total_reviews'] = total_reviews
    instructor['avg_rating'] = round(sum(all_ratings) / len(all_ratings), 1) if all_ratings else 0

    # Expertise & credentials
    instructor['expertise'] = db.select('instructor_expertise', columns='expertise',
                                         filters=[('user_id', 'eq', instructor_id)]) or []
    instructor['credentials'] = db.select('instructor_credentials', columns='credential',
                                           filters=[('user_id', 'eq', instructor_id)],
                                           order='sort_order.asc') or []

    # Courses with stats
    instructor_courses = db.select('courses',
                                    columns='*,categories(name)',
                                    filters=[('instructor_id', 'eq', instructor_id), ('status', 'eq', 'published')])
    for c in (instructor_courses or []):
        reviews = db.select('reviews', columns='rating', filters=[('course_id', 'eq', c['id'])])
        enrollments = db.select('enrollments', columns='id', filters=[('course_id', 'eq', c['id'])])
        ratings = [r['rating'] for r in (reviews or [])]
        c['avg_rating'] = round(sum(ratings) / len(ratings), 1) if ratings else 0
        c['review_count'] = len(ratings)
        c['enrollment_count'] = len(enrollments or [])
        if c.get('categories'):
            c['category_name'] = c['categories']['name']

    instructor['courses'] = instructor_courses or []
    return jsonify(instructor)


# ── DASHBOARD ──────────────────────────────────────────────────────
@app.route('/api/instructor/dashboard')
@token_required
@instructor_required
def instructor_dashboard():
    uid = g.current_user['id']

    courses = db.select('courses', filters=[('instructor_id', 'eq', uid)])
    course_ids = [c['id'] for c in (courses or [])]

    total_revenue = 0
    total_students = 0
    all_ratings = []
    top_courses = []

    for c in (courses or []):
        cid = c['id']
        orders = db.select('orders', columns='amount',
                           filters=[('course_id', 'eq', cid), ('payment_status', 'eq', 'completed')])
        enrollments = db.select('enrollments', columns='id', filters=[('course_id', 'eq', cid)])
        reviews = db.select('reviews', columns='rating', filters=[('course_id', 'eq', cid)])

        revenue = sum(float(o['amount']) for o in (orders or []))
        students = len(enrollments or [])
        ratings = [r['rating'] for r in (reviews or [])]
        avg_rating = round(sum(ratings) / len(ratings), 1) if ratings else 0

        total_revenue += revenue
        total_students += students
        all_ratings.extend(ratings)

        top_courses.append({
            'id': cid, 'title': c['title'], 'status': c['status'],
            'students': students, 'avg_rating': avg_rating, 'revenue': revenue
        })

    top_courses.sort(key=lambda x: x['revenue'], reverse=True)

    # Recent activity
    recent_enrollments = []
    recent_reviews = []
    recent_orders = []
    for cid in course_ids[:5]:
        enrolls = db.select('enrollments',
                            columns='enrolled_at,courses(title)',
                            filters=[('course_id', 'eq', cid)], order='enrolled_at.desc', limit=2)
        for e in (enrolls or []):
            recent_enrollments.append({
                'type': 'enrollment',
                'course_title': e.get('courses', {}).get('title', ''),
                'timestamp': e['enrolled_at']
            })

        revs = db.select('reviews',
                         columns='rating,created_at,courses(title)',
                         filters=[('course_id', 'eq', cid)], order='created_at.desc', limit=2)
        for r in (revs or []):
            recent_reviews.append({
                'type': 'review', 'rating': r['rating'],
                'course_title': r.get('courses', {}).get('title', ''),
                'timestamp': r['created_at']
            })

        ords = db.select('orders',
                         columns='amount,created_at,courses(title)',
                         filters=[('course_id', 'eq', cid), ('payment_status', 'eq', 'completed')],
                         order='created_at.desc', limit=2)
        for o in (ords or []):
            recent_orders.append({
                'type': 'payment', 'amount': float(o['amount']),
                'course_title': o.get('courses', {}).get('title', ''),
                'timestamp': o['created_at']
            })

    activity = sorted(
        recent_enrollments + recent_reviews + recent_orders,
        key=lambda x: x.get('timestamp') or '', reverse=True
    )[:10]

    return jsonify({
        'stats': {
            'total_revenue': total_revenue,
            'total_students': total_students,
            'total_courses': len(courses or []),
            'avg_rating': round(sum(all_ratings) / len(all_ratings), 1) if all_ratings else 0
        },
        'recent_activity': activity,
        'top_courses': top_courses
    })


# ── SEARCH ─────────────────────────────────────────────────────────
@app.route('/api/search')
def search():
    q = request.args.get('q', '').strip()
    if len(q) < 2:
        return jsonify({'courses': [], 'instructors': []})

    courses = db.select('courses',
                        columns='id,title,slug,price,image_url,categories(name),users!courses_instructor_id_fkey(first_name,last_name)',
                        filters=[('status', 'eq', 'published'), f'or=(title.ilike.%25{q}%25,description.ilike.%25{q}%25)'],
                        limit=10)

    for c in (courses or []):
        if c.get('categories'):
            c['category_name'] = c['categories']['name']
        if c.get('users'):
            c['instructor_name'] = f"{c['users']['first_name']} {c['users']['last_name']}"

    instructors = db.select('users', columns='id,first_name,last_name,title',
                            filters=[('role', 'eq', 'instructor'),
                                     f'or=(first_name.ilike.%25{q}%25,last_name.ilike.%25{q}%25)'],
                            limit=5)

    return jsonify({'courses': courses or [], 'instructors': instructors or []})


# ── USER PROFILE ───────────────────────────────────────────────────
@app.route('/api/users/profile', methods=['PUT'])
@token_required
def update_profile():
    data = request.json
    allowed = ['first_name', 'last_name', 'company', 'bio', 'title']
    updates = {k: v for k, v in data.items() if k in allowed}
    if updates:
        updates['updated_at'] = datetime.utcnow().isoformat()
        db.update('users', updates, [('id', 'eq', g.current_user['id'])])
    return jsonify({'message': 'Profile updated'})


# ══════════════════════════════════════════════════════════════════════
if __name__ == '__main__':
    print('\n  UpskillCompass API (Supabase) running at http://localhost:5001')
    print('  API docs: /api/... endpoints\n')
    app.run(debug=True, port=5001)
