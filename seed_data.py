"""
Seed the Supabase database with sample data matching the wireframes.
Expanded catalog with 9 categories, 13 instructors, and 41 courses.
"""

import random
from datetime import datetime, timedelta
import bcrypt
import supabase_client as db


def hash_pw(pw):
    return bcrypt.hashpw(pw.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def clear_all():
    """Clear all tables in dependency order."""
    print('Clearing existing data...')
    tables = ['orders', 'reviews', 'enrollments', 'wishlist', 'lessons', 'modules',
              'instructor_expertise', 'instructor_credentials', 'courses', 'coupons',
              'categories', 'users']
    for t in tables:
        try:
            db.delete(t, [('id', 'gt', '0')])
            print(f'  Cleared {t}')
        except Exception:
            # Table might be empty or not exist
            try:
                db.delete(t, [('id', 'gte', '0')])
                print(f'  Cleared {t}')
            except Exception as e2:
                print(f'  Skipped {t}: {e2}')


def seed():
    clear_all()
    now = datetime.utcnow()
    pw = hash_pw('password123')

    # ============================================================
    # CATEGORIES (9)
    # ============================================================
    print('Seeding categories...')
    categories = [
        {'name': 'Executive Leadership', 'slug': 'executive-leadership', 'icon': '🎯', 'description': 'Master the art of leading at the highest levels'},
        {'name': 'Communication', 'slug': 'communication', 'icon': '💬', 'description': 'Build powerful communication and influence skills'},
        {'name': 'Strategic Thinking', 'slug': 'strategic-thinking', 'icon': '♟️', 'description': 'Develop frameworks for strategic decision-making'},
        {'name': 'Team Building', 'slug': 'team-building', 'icon': '👥', 'description': 'Create and lead high-performing teams'},
        {'name': 'Change Management', 'slug': 'change-management', 'icon': '🔄', 'description': 'Lead organizational transformation effectively'},
        {'name': 'Coaching & Mentoring', 'slug': 'coaching-mentoring', 'icon': '🏆', 'description': 'Develop others through coaching and mentoring'},
        {'name': 'Emotional Intelligence', 'slug': 'emotional-intelligence', 'icon': '🧠', 'description': 'Develop self-awareness, empathy, and interpersonal effectiveness'},
        {'name': 'Innovation & Digital', 'slug': 'innovation-digital', 'icon': '🚀', 'description': 'Lead innovation, digital transformation, and disruptive change'},
        {'name': 'Personal Development', 'slug': 'personal-development', 'icon': '🌱', 'description': 'Build foundational leadership habits and career growth skills'},
    ]
    inserted_cats = db.insert('categories', categories)
    cat_map = {c['slug']: c['id'] for c in inserted_cats}
    print(f'  {len(inserted_cats)} categories created')

    # ============================================================
    # INSTRUCTORS (13)
    # ============================================================
    print('Seeding instructors...')
    instructors = [
        {'email': 'sarah.mitchell@leadershippro.com', 'password_hash': pw, 'first_name': 'Sarah', 'last_name': 'Mitchell', 'role': 'instructor',
         'bio': 'Dr. Sarah Mitchell is a renowned executive leadership coach with over 20 years of experience. Previously VP of Strategy at a Fortune 500 technology company. Ph.D. from Harvard, MBA from Wharton.',
         'title': 'Executive Leadership Coach & Former Fortune 500 VP'},
        {'email': 'james.rodriguez@leadershippro.com', 'password_hash': pw, 'first_name': 'James', 'last_name': 'Rodriguez', 'role': 'instructor',
         'bio': 'Executive communication expert with 15 years coaching Fortune 500 leaders.',
         'title': 'Executive Communication Expert'},
        {'email': 'linda.zhao@leadershippro.com', 'password_hash': pw, 'first_name': 'Linda', 'last_name': 'Zhao', 'role': 'instructor',
         'bio': 'Distinguished professor of Organizational Behavior at Stanford University.',
         'title': 'Professor of Organizational Behavior, Stanford'},
        {'email': 'michael.thompson@leadershippro.com', 'password_hash': pw, 'first_name': 'Michael', 'last_name': 'Thompson', 'role': 'instructor',
         'bio': 'Change management specialist who has led transformations at 3 Fortune 500 companies.',
         'title': 'Change Management Specialist'},
        {'email': 'emma.sullivan@leadershippro.com', 'password_hash': pw, 'first_name': 'Emma', 'last_name': 'Sullivan', 'role': 'instructor',
         'bio': 'ICF-certified executive coach with a focus on senior leadership development.',
         'title': 'Executive Coach & Leadership Consultant'},
        {'email': 'alan.park@leadershippro.com', 'password_hash': pw, 'first_name': 'Alan', 'last_name': 'Park', 'role': 'instructor',
         'bio': 'Specializes in strategic decision-making and risk management. Former McKinsey partner.',
         'title': 'Former McKinsey Partner & Strategy Expert'},
        {'email': 'catherine.ng@leadershippro.com', 'password_hash': pw, 'first_name': 'Catherine', 'last_name': 'Ng', 'role': 'instructor',
         'bio': 'Leadership development expert focused on diversity, equity, and inclusion.',
         'title': 'DEI Leadership Consultant'},
        {'email': 'marcus.reeves@leadershippro.com', 'password_hash': pw, 'first_name': 'Marcus', 'last_name': 'Reeves', 'role': 'instructor',
         'bio': 'Conflict resolution and mediation expert with 18 years of experience.',
         'title': 'Conflict Resolution & Mediation Expert'},
        {'email': 'sophia.andersen@leadershippro.com', 'password_hash': pw, 'first_name': 'Sophia', 'last_name': 'Andersen', 'role': 'instructor',
         'bio': 'Remote work and distributed team expert. Helped 100+ organizations build remote cultures.',
         'title': 'Remote Work & Distributed Teams Expert'},
        # --- New instructors ---
        {'email': 'priya.kapoor@leadershippro.com', 'password_hash': pw, 'first_name': 'Priya', 'last_name': 'Kapoor', 'role': 'instructor',
         'bio': 'Dr. Priya Kapoor is a clinical psychologist turned leadership consultant specializing in emotional intelligence and resilience. Author of two bestselling books on workplace psychology. Former Head of Leadership Development at Deloitte.',
         'title': 'Workplace Psychologist & EI Leadership Expert'},
        {'email': 'david.chen@leadershippro.com', 'password_hash': pw, 'first_name': 'David', 'last_name': 'Chen', 'role': 'instructor',
         'bio': 'David Chen is a serial entrepreneur and digital transformation advisor. Former CTO at two unicorn startups and innovation fellow at MIT Sloan. Has guided over 50 organizations through digital disruption.',
         'title': 'Digital Transformation Advisor & Former Startup CTO'},
        {'email': 'rachel.okonkwo@leadershippro.com', 'password_hash': pw, 'first_name': 'Rachel', 'last_name': 'Okonkwo', 'role': 'instructor',
         'bio': 'Rachel Okonkwo is a leadership development facilitator specializing in emerging leaders and first-time managers. 12 years in talent development at Google and Salesforce. Certified in strengths-based coaching.',
         'title': 'Emerging Leaders Coach & Talent Development Expert'},
        {'email': 'thomas.bergmann@leadershippro.com', 'password_hash': pw, 'first_name': 'Thomas', 'last_name': 'Bergmann', 'role': 'instructor',
         'bio': 'Thomas Bergmann is a former NATO crisis management advisor and organizational resilience consultant. Led crisis response strategy for multinational organizations across 30 countries.',
         'title': 'Crisis Leadership & Organizational Resilience Consultant'},
        # --- Swedish instructors ---
        {'email': 'anna.lindqvist@leadershippro.com', 'password_hash': pw, 'first_name': 'Anna', 'last_name': 'Lindqvist', 'role': 'instructor',
         'bio': 'Anna Lindqvist är en av Sveriges mest erfarna UGL-handledare med över 15 års erfarenhet. Legitimerad psykolog och certifierad i Utvecklande Ledarskap (UL). Tidigare chef för ledarutveckling på Ericsson.',
         'title': 'UGL-handledare & Legitimerad Psykolog'},
        {'email': 'erik.johansson@leadershippro.com', 'password_hash': pw, 'first_name': 'Erik', 'last_name': 'Johansson', 'role': 'instructor',
         'bio': 'Erik Johansson är ledarskapscoach och föreläsare med bakgrund från Handelshögskolan i Stockholm. Specialist på situationsanpassat ledarskap och förändringsledning. Tidigare managementkonsult på McKinsey Nordics.',
         'title': 'Ledarskapscoach & Fd. McKinsey-konsult'},
        {'email': 'maria.bergstrom@leadershippro.com', 'password_hash': pw, 'first_name': 'Maria', 'last_name': 'Bergström', 'role': 'instructor',
         'bio': 'Maria Bergström är expert på coachande ledarskap och teamutveckling. ICF-certifierad coach (PCC) med 20 års erfarenhet av chefsutbildning. Tidigare HR-direktör på Volvo Cars.',
         'title': 'ICF-certifierad Coach & Teamutvecklare'},
        {'email': 'anders.nystrom@leadershippro.com', 'password_hash': pw, 'first_name': 'Anders', 'last_name': 'Nyström', 'role': 'instructor',
         'bio': 'Anders Nyström är docent i ledarskap vid Lunds universitet och konsult inom executive education. Forskar om nordiskt ledarskap och har publicerat tre böcker om skandinavisk ledarskapsstil.',
         'title': 'Docent i Ledarskap & Executive Education-konsult'},
        {'email': 'karin.svensson@leadershippro.com', 'password_hash': pw, 'first_name': 'Karin', 'last_name': 'Svensson', 'role': 'instructor',
         'bio': 'Karin Svensson specialiserar sig på digital transformation och innovationsledarskap. Tidigare CTO på Klarna och innovationschef på Spotify. Rådgivare till svenska startups och storföretag.',
         'title': 'Innovationsledare & Fd. CTO Klarna'},
    ]
    inserted_instructors = db.insert('users', instructors)
    inst_map = {f"{i['first_name']} {i['last_name']}": i['id'] for i in inserted_instructors}
    print(f'  {len(inserted_instructors)} instructors created')

    # ============================================================
    # LEARNERS (8)
    # ============================================================
    print('Seeding learners...')
    learners = [
        {'email': 'amanda.whitfield@mercer.com', 'password_hash': pw, 'first_name': 'Amanda', 'last_name': 'Whitfield', 'role': 'learner', 'company': 'Mercer Corp', 'title': 'VP Operations'},
        {'email': 'robert.chen@techvista.com', 'password_hash': pw, 'first_name': 'Robert', 'last_name': 'Chen', 'role': 'learner', 'company': 'TechVista', 'title': 'Director of HR'},
        {'email': 'patricia.okafor@bridgepoint.com', 'password_hash': pw, 'first_name': 'Patricia', 'last_name': 'Okafor', 'role': 'learner', 'company': 'BridgePoint Advisory', 'title': 'CEO'},
        {'email': 'david.park@acme.com', 'password_hash': pw, 'first_name': 'David', 'last_name': 'Park', 'role': 'learner', 'company': 'Acme Corp', 'title': 'Senior Manager'},
        {'email': 'lisa.martinez@techco.com', 'password_hash': pw, 'first_name': 'Lisa', 'last_name': 'Martinez', 'role': 'learner', 'company': 'TechCo', 'title': 'Team Lead'},
        {'email': 'john.smith@company.com', 'password_hash': pw, 'first_name': 'John', 'last_name': 'Smith', 'role': 'learner', 'company': 'GlobalTech', 'title': 'Director'},
        {'email': 'emily.johnson@corp.com', 'password_hash': pw, 'first_name': 'Emily', 'last_name': 'Johnson', 'role': 'learner', 'company': 'StartupXYZ', 'title': 'COO'},
        {'email': 'admin@upskillcompass.com', 'password_hash': pw, 'first_name': 'Admin', 'last_name': 'User', 'role': 'admin', 'company': 'UpskillCompass', 'title': 'Platform Admin'},
    ]
    inserted_learners = db.insert('users', learners)
    learner_map = {f"{l['first_name']} {l['last_name']}": l['id'] for l in inserted_learners}
    print(f'  {len(inserted_learners)} learners created')

    # ============================================================
    # CREDENTIALS & EXPERTISE
    # ============================================================
    sarah_id = inst_map['Sarah Mitchell']
    print('Seeding credentials & expertise...')
    db.insert('instructor_credentials', [
        {'user_id': sarah_id, 'credential': 'Ph.D. Organizational Leadership — Harvard University', 'sort_order': 1},
        {'user_id': sarah_id, 'credential': 'MBA — Wharton School of Business', 'sort_order': 2},
        {'user_id': sarah_id, 'credential': 'Certified Executive Coach (ICF-PCC)', 'sort_order': 3},
        {'user_id': sarah_id, 'credential': 'Former VP Strategy, Meridian Technologies (Fortune 500)', 'sort_order': 4},
        {'user_id': sarah_id, 'credential': "Published Author: The Strategic Leader's Playbook", 'sort_order': 5},
    ])
    db.insert('instructor_expertise', [
        {'user_id': sarah_id, 'expertise': e}
        for e in ['Executive Leadership', 'Strategic Planning', 'Organizational Change', 'Team Development',
                  'Stakeholder Management', 'Decision Making', 'Executive Coaching', 'Communication']
    ])

    # Credentials for new instructors
    priya_id = inst_map['Priya Kapoor']
    db.insert('instructor_credentials', [
        {'user_id': priya_id, 'credential': 'Ph.D. Clinical Psychology — University of Cambridge', 'sort_order': 1},
        {'user_id': priya_id, 'credential': 'Certified Emotional Intelligence Practitioner (EQ-i 2.0)', 'sort_order': 2},
        {'user_id': priya_id, 'credential': 'Former Head of Leadership Development, Deloitte', 'sort_order': 3},
        {'user_id': priya_id, 'credential': 'Author: The Emotionally Intelligent Leader & Leading with Heart', 'sort_order': 4},
    ])
    db.insert('instructor_expertise', [
        {'user_id': priya_id, 'expertise': e}
        for e in ['Emotional Intelligence', 'Workplace Psychology', 'Resilience', 'Mindfulness', 'Leadership Development', 'Stress Management']
    ])

    david_c_id = inst_map['David Chen']
    db.insert('instructor_credentials', [
        {'user_id': david_c_id, 'credential': 'M.S. Computer Science — MIT', 'sort_order': 1},
        {'user_id': david_c_id, 'credential': 'Innovation Fellow — MIT Sloan School of Management', 'sort_order': 2},
        {'user_id': david_c_id, 'credential': 'Former CTO, Nexus Technologies (Unicorn Startup)', 'sort_order': 3},
        {'user_id': david_c_id, 'credential': 'Board Advisor, 3 Fortune 500 Digital Transformation Programs', 'sort_order': 4},
    ])
    db.insert('instructor_expertise', [
        {'user_id': david_c_id, 'expertise': e}
        for e in ['Digital Transformation', 'Innovation Strategy', 'AI & Technology', 'Startup Leadership', 'Product Strategy', 'Agile Leadership']
    ])

    rachel_id = inst_map['Rachel Okonkwo']
    db.insert('instructor_credentials', [
        {'user_id': rachel_id, 'credential': 'M.A. Organizational Development — Columbia University', 'sort_order': 1},
        {'user_id': rachel_id, 'credential': 'Gallup Certified Strengths Coach', 'sort_order': 2},
        {'user_id': rachel_id, 'credential': 'Former Director of Talent Development, Google', 'sort_order': 3},
        {'user_id': rachel_id, 'credential': 'Former Senior Manager, Leadership Programs, Salesforce', 'sort_order': 4},
    ])
    db.insert('instructor_expertise', [
        {'user_id': rachel_id, 'expertise': e}
        for e in ['Emerging Leaders', 'First-Time Managers', 'Personal Development', 'Strengths-Based Coaching', 'Talent Development', 'Career Growth']
    ])

    thomas_id = inst_map['Thomas Bergmann']
    db.insert('instructor_credentials', [
        {'user_id': thomas_id, 'credential': 'M.A. International Security — King\'s College London', 'sort_order': 1},
        {'user_id': thomas_id, 'credential': 'Former NATO Crisis Management Advisor', 'sort_order': 2},
        {'user_id': thomas_id, 'credential': 'Certified Business Continuity Professional (CBCP)', 'sort_order': 3},
        {'user_id': thomas_id, 'credential': 'Author: Leading Through the Storm', 'sort_order': 4},
    ])
    db.insert('instructor_expertise', [
        {'user_id': thomas_id, 'expertise': e}
        for e in ['Crisis Leadership', 'Organizational Resilience', 'Geopolitical Risk', 'Strategic Planning', 'Change Management', 'Risk Assessment']
    ])

    # Swedish instructor credentials & expertise
    anna_id = inst_map['Anna Lindqvist']
    db.insert('instructor_credentials', [
        {'user_id': anna_id, 'credential': 'Legitimerad Psykolog — Uppsala universitet', 'sort_order': 1},
        {'user_id': anna_id, 'credential': 'Certifierad UGL-handledare — Försvarshögskolan', 'sort_order': 2},
        {'user_id': anna_id, 'credential': 'Certifierad i Utvecklande Ledarskap (UL)', 'sort_order': 3},
        {'user_id': anna_id, 'credential': 'Fd. Chef Ledarutveckling, Ericsson', 'sort_order': 4},
    ])
    db.insert('instructor_expertise', [
        {'user_id': anna_id, 'expertise': e}
        for e in ['UGL', 'Gruppdynamik', 'FIRO-modellen', 'Utvecklande Ledarskap', 'Psykologi', 'Självkännedom']
    ])

    erik_id = inst_map['Erik Johansson']
    db.insert('instructor_credentials', [
        {'user_id': erik_id, 'credential': 'MBA — Handelshögskolan i Stockholm', 'sort_order': 1},
        {'user_id': erik_id, 'credential': 'Certifierad i Situationsanpassat Ledarskap (SLII)', 'sort_order': 2},
        {'user_id': erik_id, 'credential': 'Fd. Managementkonsult, McKinsey & Company Nordics', 'sort_order': 3},
        {'user_id': erik_id, 'credential': 'Författare: Ledarskap i förändring', 'sort_order': 4},
    ])
    db.insert('instructor_expertise', [
        {'user_id': erik_id, 'expertise': e}
        for e in ['Situationsanpassat Ledarskap', 'Förändringsledning', 'Strategiskt Ledarskap', 'Management', 'Organisationsutveckling']
    ])

    maria_id = inst_map['Maria Bergström']
    db.insert('instructor_credentials', [
        {'user_id': maria_id, 'credential': 'ICF Professional Certified Coach (PCC)', 'sort_order': 1},
        {'user_id': maria_id, 'credential': 'M.Sc. Organisationspsykologi — Göteborgs universitet', 'sort_order': 2},
        {'user_id': maria_id, 'credential': 'Fd. HR-direktör, Volvo Cars', 'sort_order': 3},
        {'user_id': maria_id, 'credential': 'Certifierad MBTI-praktiker', 'sort_order': 4},
    ])
    db.insert('instructor_expertise', [
        {'user_id': maria_id, 'expertise': e}
        for e in ['Coachande Ledarskap', 'Teamutveckling', 'HR-ledarskap', 'Feedback', 'MBTI', 'Medarbetarsamtal']
    ])

    anders_id = inst_map['Anders Nyström']
    db.insert('instructor_credentials', [
        {'user_id': anders_id, 'credential': 'Docent i Ledarskap — Lunds universitet', 'sort_order': 1},
        {'user_id': anders_id, 'credential': 'Ph.D. Företagsekonomi — Handelshögskolan i Göteborg', 'sort_order': 2},
        {'user_id': anders_id, 'credential': 'Författare: Den skandinaviska ledarskapsmodellen (3 böcker)', 'sort_order': 3},
        {'user_id': anders_id, 'credential': 'Rådgivare, EFL Executive Education Lund', 'sort_order': 4},
    ])
    db.insert('instructor_expertise', [
        {'user_id': anders_id, 'expertise': e}
        for e in ['Nordiskt Ledarskap', 'Organisationsteori', 'Executive Education', 'Ledarskap i organisationer', 'Forskning']
    ])

    karin_id = inst_map['Karin Svensson']
    db.insert('instructor_credentials', [
        {'user_id': karin_id, 'credential': 'M.Sc. Datateknik — KTH', 'sort_order': 1},
        {'user_id': karin_id, 'credential': 'Fd. CTO, Klarna', 'sort_order': 2},
        {'user_id': karin_id, 'credential': 'Fd. Innovationschef, Spotify', 'sort_order': 3},
        {'user_id': karin_id, 'credential': 'Styrelseledamot, tre svenska techbolag', 'sort_order': 4},
    ])
    db.insert('instructor_expertise', [
        {'user_id': karin_id, 'expertise': e}
        for e in ['Digital Transformation', 'Innovationsledarskap', 'Agilt Ledarskap', 'Tech-ledarskap', 'Startup-kultur', 'AI-strategi']
    ])

    # ============================================================
    # COURSES (63 total: 61 published, 1 draft, 1 review)
    # ============================================================
    print('Seeding courses...')
    courses_data = [
        # --- Original 16 courses ---
        ('Sarah Mitchell', 'executive-leadership', 'Strategic Leadership Masterclass', 'strategic-leadership-masterclass',
         'Master the art of strategic leadership with proven frameworks used by Fortune 500 executives. Learn to craft organizational vision, manage stakeholders, build high-performing teams, and drive lasting change.', 299, 499, 'advanced', 'self-paced', 18.5, 5, 32, True, True, 'published'),
        ('Sarah Mitchell', 'executive-leadership', 'Leading with Emotional Intelligence', 'leading-with-emotional-intelligence',
         'Harness the power of emotional intelligence to become a more effective leader. Explore self-awareness, empathy, and relationship management in executive contexts.', 249, None, 'intermediate', 'self-paced', 14, 4, 24, False, True, 'published'),
        ('Sarah Mitchell', 'communication', 'C-Suite Communication', 'c-suite-communication',
         'Master the communication skills needed to succeed in the executive suite. From boardroom presentations to crisis communications.', 199, None, 'advanced', 'hybrid', 10, 3, 18, False, False, 'published'),
        ('Sarah Mitchell', 'change-management', 'Change Management Fundamentals', 'change-management-fundamentals',
         'Learn the foundations of leading organizational change effectively. Covers Kotter, ADKAR, and Lewin models with real-world case studies.', 179, None, 'intermediate', 'self-paced', 12, 4, 20, False, False, 'published'),
        ('Sarah Mitchell', 'executive-leadership', 'Executive Decision Making', 'executive-decision-making',
         'Apply data-driven frameworks to make better strategic decisions. Learn to navigate ambiguity, manage risk, and align decisions with organizational goals.', 269, None, 'advanced', 'self-paced', 11, 3, 22, False, False, 'published'),
        ('Sarah Mitchell', 'executive-leadership', 'Board-Level Leadership', 'board-level-leadership',
         'Prepare for board-level responsibilities and governance. Covers fiduciary duties, board dynamics, strategic oversight, and stakeholder accountability.', 349, None, 'executive', 'live', 8, 3, 16, False, False, 'published'),
        ('James Rodriguez', 'communication', 'Executive Communication & Influence', 'executive-communication-influence',
         'Build powerful communication and persuasion skills for leadership contexts. Master storytelling, presence, and influence without authority.', 249, None, 'intermediate', 'self-paced', 12, 4, 24, False, True, 'published'),
        ('Linda Zhao', 'team-building', 'High-Performance Team Leadership', 'high-performance-team-leadership',
         'Build and lead teams that consistently deliver exceptional results. Grounded in organizational behavior research from Stanford.', 199, 349, 'intermediate', 'self-paced', 15, 5, 28, False, True, 'published'),
        ('Michael Thompson', 'change-management', 'Leading Organizational Change', 'leading-organizational-change',
         'Master proven methodologies for driving successful organizational transformation. Real case studies from Fortune 500 transformations.', 349, None, 'advanced', 'hybrid', 16, 5, 30, True, True, 'published'),
        ('Emma Sullivan', 'coaching-mentoring', 'Coaching for Senior Leaders', 'coaching-for-senior-leaders',
         'Develop coaching skills to unlock the potential of your senior team members. ICF-aligned coaching frameworks and practice.', 279, None, 'advanced', 'self-paced', 10, 3, 20, False, False, 'published'),
        ('Alan Park', 'strategic-thinking', 'Strategic Decision Making', 'strategic-decision-making',
         'Apply rigorous analytical frameworks to complex strategic challenges. Scenario planning, game theory, and competitive analysis.', 319, None, 'advanced', 'self-paced', 13, 4, 22, False, False, 'published'),
        ('Catherine Ng', 'executive-leadership', 'Women in Leadership', 'women-in-leadership',
         'Develop leadership skills and strategies for women in corporate leadership. Address bias, build networks, and amplify your impact.', 259, None, 'intermediate', 'self-paced', 11, 4, 20, False, False, 'published'),
        ('Marcus Reeves', 'communication', 'Conflict Resolution Mastery', 'conflict-resolution-mastery',
         'Master the art of resolving conflicts and turning disagreements into opportunities for growth and stronger relationships.', 189, None, 'intermediate', 'self-paced', 9, 3, 18, False, False, 'published'),
        ('Sophia Andersen', 'team-building', 'Remote Team Leadership', 'remote-team-leadership',
         'Build and manage high-performing distributed teams across time zones. Communication cadence, tools, and culture-building for remote-first organizations.', 229, None, 'intermediate', 'self-paced', 10, 4, 20, False, False, 'published'),
        ('Sarah Mitchell', 'communication', 'Advanced Negotiation Tactics', 'advanced-negotiation-tactics',
         'Master advanced negotiation strategies for high-stakes business deals.', 299, None, 'executive', 'live', 8, 0, 0, False, False, 'draft'),
        ('Sarah Mitchell', 'executive-leadership', 'Leadership in Crisis', 'leadership-in-crisis',
         'Lead effectively during organizational crises and uncertainty.', 259, None, 'advanced', 'self-paced', 10, 0, 0, False, False, 'review'),

        # --- NEW: Beginner courses (6) ---
        ('Rachel Okonkwo', 'personal-development', 'Leadership Foundations: Your First 90 Days', 'leadership-foundations-first-90-days',
         'A practical roadmap for new and aspiring leaders covering essential skills like delegation, feedback, one-on-ones, and building credibility with your team from day one.', 149, None, 'beginner', 'self-paced', 8, 3, 18, False, True, 'published'),
        ('Rachel Okonkwo', 'communication', 'Communication Essentials for New Leaders', 'communication-essentials-new-leaders',
         'Learn the core communication skills every leader needs including active listening, giving clear direction, running effective meetings, and delivering constructive feedback.', 159, None, 'beginner', 'self-paced', 7.5, 3, 16, False, False, 'published'),
        ('Priya Kapoor', 'emotional-intelligence', 'Emotional Intelligence 101: The Leader\'s Edge', 'emotional-intelligence-101',
         'Understand the five pillars of emotional intelligence and how self-awareness, self-regulation, motivation, empathy, and social skill form the foundation of effective leadership.', 169, None, 'beginner', 'self-paced', 8.5, 3, 18, True, True, 'published'),
        ('Linda Zhao', 'team-building', 'Building Your First Team', 'building-your-first-team',
         'A step-by-step guide to hiring, onboarding, and developing your first direct reports into a cohesive, high-performing team.', 149, None, 'beginner', 'self-paced', 7, 3, 16, False, False, 'published'),
        ('Rachel Okonkwo', 'personal-development', 'Time Management and Productivity for Leaders', 'time-management-productivity-leaders',
         'Master prioritization frameworks, energy management, and delegation strategies to maximize your impact as a leader without burning out.', 129, None, 'beginner', 'self-paced', 6, 3, 14, False, False, 'published'),
        ('David Chen', 'innovation-digital', 'Digital Literacy for Leaders', 'digital-literacy-for-leaders',
         'Understand the technology landscape every modern leader needs to navigate, from data analytics to cloud platforms, AI, and cybersecurity fundamentals.', 159, None, 'beginner', 'self-paced', 7, 3, 16, False, False, 'published'),

        # --- NEW: Intermediate courses (7) ---
        ('Priya Kapoor', 'emotional-intelligence', 'Resilience and Stress Management for Leaders', 'resilience-stress-management-leaders',
         'Build mental toughness and sustainable performance habits to lead effectively through pressure, setbacks, and organizational turbulence.', 219, None, 'intermediate', 'self-paced', 10, 4, 20, False, False, 'published'),
        ('Catherine Ng', 'team-building', 'Leading Diverse and Inclusive Teams', 'leading-diverse-inclusive-teams',
         'Develop practical skills for creating psychologically safe, inclusive team cultures where diverse perspectives drive better business outcomes.', 229, None, 'intermediate', 'hybrid', 11, 4, 22, False, True, 'published'),
        ('Sophia Andersen', 'team-building', 'Hybrid Workplace Leadership', 'hybrid-workplace-leadership',
         'Master the unique challenges of leading teams split across office and remote settings, including communication cadence, equitable practices, and culture building.', 199, None, 'intermediate', 'self-paced', 9, 3, 18, False, False, 'published'),
        ('David Chen', 'innovation-digital', 'Leading Digital Transformation', 'leading-digital-transformation',
         'A comprehensive framework for driving technology-enabled business transformation including roadmap creation, stakeholder alignment, and change adoption.', 249, 399, 'intermediate', 'self-paced', 12, 4, 24, True, True, 'published'),
        ('Emma Sullivan', 'coaching-mentoring', 'Mentoring Skills for Mid-Level Managers', 'mentoring-skills-mid-level-managers',
         'Develop structured mentoring capabilities to accelerate the growth of high-potential talent and build a leadership pipeline in your organization.', 199, None, 'intermediate', 'self-paced', 9, 3, 18, False, False, 'published'),
        ('James Rodriguez', 'communication', 'Storytelling for Business Leaders', 'storytelling-business-leaders',
         'Harness the power of narrative to inspire teams, pitch ideas to stakeholders, and communicate your vision with clarity and emotional resonance.', 209, None, 'intermediate', 'self-paced', 10, 4, 20, False, False, 'published'),
        ('Marcus Reeves', 'communication', 'Difficult Conversations at Work', 'difficult-conversations-at-work',
         'Gain confidence and skill in navigating tough workplace discussions including performance issues, interpersonal conflict, and delivering unwelcome news.', 189, None, 'intermediate', 'self-paced', 8, 3, 16, False, False, 'published'),

        # --- NEW: Advanced courses (8) ---
        ('Priya Kapoor', 'emotional-intelligence', 'Advanced Emotional Intelligence for Senior Leaders', 'advanced-emotional-intelligence-senior',
         'Take your emotional intelligence to the next level with advanced techniques for reading organizational dynamics, managing complex stakeholder emotions, and leading with authenticity.', 289, None, 'advanced', 'hybrid', 12, 4, 22, False, False, 'published'),
        ('Thomas Bergmann', 'change-management', 'Crisis Leadership and Organizational Resilience', 'crisis-leadership-organizational-resilience',
         'Prepare for and lead through organizational crises with proven frameworks for rapid decision-making, stakeholder communication, and post-crisis recovery.', 299, None, 'advanced', 'hybrid', 14, 4, 26, False, True, 'published'),
        ('Alan Park', 'strategic-thinking', 'Competitive Strategy and Market Positioning', 'competitive-strategy-market-positioning',
         'Apply advanced strategic analysis tools including blue ocean strategy, competitive intelligence, and scenario planning to position your organization for sustained advantage.', 279, None, 'advanced', 'self-paced', 13, 4, 24, False, False, 'published'),
        ('David Chen', 'innovation-digital', 'Innovation Leadership: From Idea to Execution', 'innovation-leadership-idea-execution',
         'Build and lead innovation teams using design thinking, lean startup methods, and portfolio management to turn creative ideas into scalable business outcomes.', 269, None, 'advanced', 'self-paced', 11, 4, 22, False, False, 'published'),
        ('Michael Thompson', 'change-management', 'Mergers, Acquisitions, and Cultural Integration', 'mergers-acquisitions-cultural-integration',
         'Navigate the human side of M&A with frameworks for cultural assessment, integration planning, communication strategy, and retention of key talent.', 319, None, 'advanced', 'hybrid', 14, 5, 28, False, False, 'published'),
        ('Linda Zhao', 'team-building', 'Scaling Teams from 10 to 1000', 'scaling-teams-10-to-1000',
         'Learn the organizational design principles, hiring strategies, and management structures needed to scale teams through rapid growth without losing culture or quality.', 269, None, 'advanced', 'self-paced', 12, 4, 22, False, False, 'published'),
        ('Emma Sullivan', 'coaching-mentoring', 'Executive Coaching Certification Prep', 'executive-coaching-certification-prep',
         'Intensive preparation for ICF coaching certification covering core competencies, coaching models, practice sessions, and mentor coaching hours.', 349, None, 'advanced', 'live', 16, 5, 30, False, False, 'published'),
        ('Thomas Bergmann', 'strategic-thinking', 'Geopolitical Risk and Strategic Decision Making', 'geopolitical-risk-strategic-decisions',
         'Analyze how geopolitical trends, trade dynamics, and regulatory shifts impact strategic planning, and develop frameworks for decision-making under deep uncertainty.', 299, None, 'advanced', 'self-paced', 11, 4, 20, False, False, 'published'),

        # --- NEW: Executive courses (4) ---
        ('Alan Park', 'executive-leadership', 'CEO Transition and First Year Playbook', 'ceo-transition-first-year-playbook',
         'A structured program for newly appointed or aspiring CEOs covering the critical first-year priorities: board relationships, executive team alignment, stakeholder communication, and strategic agenda setting.', 399, None, 'executive', 'live', 10, 4, 18, False, False, 'published'),
        ('Thomas Bergmann', 'executive-leadership', 'Leading in Uncertainty: The Executive Resilience Program', 'leading-in-uncertainty-executive-resilience',
         'An advanced program for senior executives on maintaining strategic clarity, organizational morale, and personal effectiveness during prolonged periods of uncertainty and disruption.', 379, None, 'executive', 'hybrid', 12, 4, 20, False, True, 'published'),
        ('Priya Kapoor', 'personal-development', 'The Mindful Executive', 'the-mindful-executive',
         'Integrate mindfulness practices into executive leadership to improve decision quality, reduce stress, strengthen presence, and build more authentic relationships with your teams.', 299, None, 'executive', 'live', 8, 3, 16, False, False, 'published'),
        ('David Chen', 'innovation-digital', 'AI Strategy for Senior Leaders', 'ai-strategy-senior-leaders',
         'A non-technical executive guide to artificial intelligence covering strategic opportunities, governance frameworks, talent implications, and responsible AI deployment.', 349, None, 'executive', 'hybrid', 9, 3, 18, False, False, 'published'),

        # ================================================================
        # SVENSKA LEDARSKAPSUTBILDNINGAR (22 riktiga kurser)
        # Verifierade kurser från svenska leverantörer med källänkar
        # ================================================================

        # --- Ny som chef / Grundläggande (6 kurser) ---
        ('Erik Johansson', 'personal-development', 'Ny som chef', 'wenell-ny-som-chef',
         'Wenell Managements kurs för nya chefer. Gå från expert till ledare med verktyg för kommunikation, coaching, motivation, arbetsrätt, delegering och teamutveckling. 2 dagars klassrumsutbildning. Leverantör: Wenell Management | Pris: 13 999 SEK exkl. moms | https://www.wenell.se/utbildning/ledarskap/ny-som-chef', 199, None, 'beginner', 'live', 16, 3, 16, False, True, 'published'),
        ('Anna Lindqvist', 'personal-development', 'Ny som chef (Hjärtum)', 'hjartum-ny-som-chef',
         'Hjärtum Utbildnings grundkurs för nya chefer. Beslutsfattande, konflikthantering, medarbetarmotivation, kommunikationsteknik, arbetsrätt och AI i ledarskapet. Inkluderar uppföljningsmöte 4-6 veckor efter. Leverantör: Hjärtum Utbildning | Pris: 11 980 SEK exkl. moms | https://www.hjartum.se/kurs/ledarskapsutbildning/ny-som-chef', 169, None, 'beginner', 'live', 16, 3, 16, False, False, 'published'),
        ('Maria Bergström', 'personal-development', 'Ny som chef (Advantum)', 'advantum-ny-som-chef',
         'Advantum Kompetens praktiska ledarskapsutbildning för nya och blivande chefer. Case-baserade övningar i delegering, feedback, coaching, prioritering och svåra samtal. Inkluderar personlig handlingsplan och uppföljningsmöte 3 månader efter. Leverantör: Advantum Kompetens | Pris: 24 900 SEK exkl. moms | https://www.advantumkompetens.se/oppna-utbildningar/ledarskap/ny-som-chef/', 249, None, 'beginner', 'live', 24, 3, 18, False, False, 'published'),
        ('Anna Lindqvist', 'executive-leadership', 'Att leda utan att vara chef', 'hjartum-leda-utan-chef',
         'Hjärtum Utbildnings kurs för dig som leder utan formell chefsroll. Bygga förtroende, hantera konflikter, delegera, övertyga och coacha i en informell ledarroll. Leverantör: Hjärtum Utbildning | Pris: 9 980 SEK exkl. moms | https://www.hjartum.se/kurs/ledarskapsutbildning/att-leda-utan-att-vara-chef', 149, None, 'beginner', 'live', 16, 3, 14, False, False, 'published'),
        ('Maria Bergström', 'coaching-mentoring', 'Coachande ledarskap', 'wenell-coachande-ledarskap',
         'Wenell Managements utbildning i coachande ledarskap. Träna på att utveckla dina medarbetare genom coaching istället för direkt styrning. Verktyg och metoder för det coachande förhållningssättet. Leverantör: Wenell Management | Pris: 13 999 SEK exkl. moms | https://www.wenell.se/utbildning/ledarskap/coachande-ledarskap', 199, None, 'beginner', 'live', 16, 3, 16, True, True, 'published'),
        ('Karin Svensson', 'innovation-digital', 'AI för framtidens ledare', 'berghs-ai-framtidens-ledare',
         'Berghs School of Communications intensivkurs i AI för ledare. Lär dig integrera AI strategiskt i din organisation: prompt engineering, beslutsfattande, riskhantering och att bygga lärande kulturer. Max 14 deltagare. Leverantör: Berghs School of Communication | Pris: 19 000 SEK exkl. moms | https://www.berghs.se/kurs/ai-for-framtidens-ledare-kurs-dagtid-berghs/', 199, None, 'beginner', 'live', 12, 3, 14, False, False, 'published'),

        # --- Intermediate (9 kurser) ---
        ('Anna Lindqvist', 'personal-development', 'UGL — Utveckling av Grupp och Ledare', 'fu-ugl-utveckling-grupp-ledare',
         'Sveriges mest kända ledarskapsutbildning via Företagsuniversitetet. Upplevelsebaserat lärande med fokus på gruppdynamik, ledarstilar, konflikthantering och självinsikt. Max 12 deltagare, två handledare. 5 dagars internat på Lejondals slott. Leverantör: Företagsuniversitetet | Pris: 32 900 SEK inkl. kost och logi | https://www.foretagsuniversitetet.se/oeppna-kurser/kompetensutveckling/Ledarskap/UGL-utveckling-grupp-och-ledare', 349, None, 'intermediate', 'live', 40, 5, 30, True, True, 'published'),
        ('Erik Johansson', 'executive-leadership', 'Utvecklande Ledarskap UL (IHM)', 'ihm-utvecklande-ledarskap-ul',
         'IHM Business Schools forskningsbaserade ledarskapsutbildning byggd på Försvarshögskolans UL-modell. Inkluderar 360-graders feedback (ULL-bedömning), två feedbacksessioner och praktiska övningar. Lär dig motivera medarbetare och bygga starka teamrelationer. Leverantör: IHM Business School | Pris: 28 500 SEK exkl. moms | https://www.ihm.se/utbildningar/management/utvecklande-ledarskap/', 299, None, 'intermediate', 'live', 32, 4, 24, True, True, 'published'),
        ('Maria Bergström', 'communication', 'Ledarskap och Kommunikation', 'wenell-ledarskap-kommunikation',
         'Wenell Managements kombinerade ledarskaps- och kommunikationsprogram. Integrerar ledarskapsutveckling med avancerade kommunikationsfärdigheter genom rollspel och gruppövningar. 4 dagars klassrumsutbildning. Leverantör: Wenell Management | Pris: 29 999 SEK exkl. moms | https://www.wenell.se/utbildning/ledarskap/ledarskap-och-kommunikation', 299, None, 'intermediate', 'live', 32, 4, 24, False, False, 'published'),
        ('Erik Johansson', 'executive-leadership', 'Leda genom andra chefer', 'wenell-leda-genom-andra',
         'Wenell Managements kurs för seniora ledare som leder andra chefer. Fokuserar på utmaningarna med att leda genom ytterligare ett organisatoriskt lager — att skapa riktning, bygga ledarskapskultur och stärka mellanchefer. Leverantör: Wenell Management | Pris: 13 999 SEK exkl. moms | https://www.wenell.se/utbildning/ledarskap/leda-genom-andra-chefer', 199, None, 'intermediate', 'live', 16, 3, 18, False, False, 'published'),
        ('Anna Lindqvist', 'communication', 'Konflikthantering och svåra samtal', 'fu-konflikthantering-svara-samtal',
         'Företagsuniversitetets kurs i professionell kommunikation och konfliktlösning för chefer. Feedbacktekniker, svåra samtal, konfliktfaser och lösningsstrategier. Leds av legitimerad psykolog. Leverantör: Företagsuniversitetet | Pris: 16 900 SEK | https://www.foretagsuniversitetet.se/oeppna-kurser/kompetensutveckling/Ledarskap/Konflikthantering-och-svaara-samtal', 199, None, 'intermediate', 'live', 16, 3, 18, False, False, 'published'),
        ('Maria Bergström', 'communication', 'Kommunikation i ledarskapet', 'fu-kommunikation-ledarskapet',
         'Företagsuniversitetets utbildning i ledarskapskommunikation för chefer, teamledare och projektledare. Fokuserar på effektiv kommunikation inom ledarskapsrollen. Leverantör: Företagsuniversitetet | Pris: 16 900 SEK | https://www.foretagsuniversitetet.se/oeppna-kurser/kompetensutveckling/Ledarskap/Kommunikation-i-ledarskapet', 199, None, 'intermediate', 'live', 16, 3, 16, False, False, 'published'),
        ('Anna Lindqvist', 'executive-leadership', 'Certifierad ledare', 'hjartum-certifierad-ledare',
         'Hjärtum Utbildnings certifieringsprogram i ledarskap. Fördjupade ledarskapskompetenser med formell certifiering. 2 dagars utbildning. Leverantör: Hjärtum Utbildning | Pris: 11 980 SEK exkl. moms | https://www.hjartum.se/kurs/ledarskapsutbildning/certifierad-ledare', 179, None, 'intermediate', 'live', 16, 3, 16, False, False, 'published'),
        ('Erik Johansson', 'change-management', 'Förändringsledning och förändringsledarskap', 'canea-forandringsledning',
         'CANEA:s utbildning i förändringsledning som täcker både processverktyg och ledarskapsaspekter av förändring — att leda människor och kultur genom transformation. 3 dagars klassrumsutbildning. Leverantör: CANEA | Pris: 21 800 SEK exkl. moms | https://www.canea.se/utbildningar/forandringsledning-forandringsledarskap', 229, None, 'intermediate', 'live', 24, 4, 20, False, False, 'published'),
        ('Anders Nyström', 'executive-leadership', 'Leda utan att vara chef (Chefakademin)', 'chefakademin-leda-utan-chef',
         'Chefakademins certifierade ledarskapsutbildning för projektledare och teamledare utan formell chefsroll. Självkännedom, psykologisk trygghet, gruppdynamik, coaching och svåra samtal. Betyg 4.7/5. Leverantör: Chefakademin (Chef.se) | Pris: 29 950 SEK exkl. moms | https://chef.se/chefakademin/ledarskapsutbildningar/leda-utan-att-vara-chef/', 299, None, 'intermediate', 'hybrid', 40, 4, 22, False, True, 'published'),

        # --- Advanced (4 kurser) ---
        ('Anders Nyström', 'personal-development', 'Ledarskap i praktiken', 'fu-ledarskap-i-praktiken',
         'Företagsuniversitetets praktiska ledarskapsutbildning som kombinerar vetenskaplig grund med konkreta verktyg. Inkluderar Values Online-bedömning, 360-graders feedback (IDI) och digital coaching efter kurs. Leverantör: Företagsuniversitetet | Pris: 49 500 SEK exkl. moms | https://www.foretagsuniversitetet.se/oeppna-kurser/kompetensutveckling/Ledarskap/Ledarskap-i-praktiken', 349, None, 'advanced', 'live', 24, 4, 22, False, True, 'published'),
        ('Anders Nyström', 'executive-leadership', 'EFL Ledarskap i organisationer', 'efl-ledarskap-organisationer',
         'EFL Executive Educations ledarskapsutbildning vid Lunds universitet. Ledarskap i organisationsstrategi, förändringsledning, coaching och gruppdynamik. Leds av professor Stefan Sveningsson. 6 dagar under 5 månader. Leverantör: EFL Executive Education / Lunds universitet | Pris: 46 900 SEK exkl. moms | https://www.efl.se/program/affarsmannaskap/efl-ledarskap-i-organisationer/', 379, None, 'advanced', 'live', 48, 4, 24, False, False, 'published'),
        ('Erik Johansson', 'change-management', 'Leading Change — Framgångsrikt förändringsledarskap', 'efl-leading-change',
         'EFL Executive Educations avancerade förändringsledarskapsutbildning. Förändringspsykologi, motståndshantering, organisatoriskt lärande och ledarens roll i transformation. Betyg 9.3/10 av deltagare. 9 dagar över 3 internat. Leverantör: EFL Executive Education / Lunds universitet | Pris: 63 000 SEK exkl. moms | https://www.efl.se/program/affarsmannaskap/leading-change-framgangsrikt-forandringsledarskap/', 449, None, 'advanced', 'live', 72, 3, 24, False, False, 'published'),
        ('Karin Svensson', 'innovation-digital', 'AI för förändringsledare', 'berghs-ai-forandringsledare',
         'Berghs School of Communications fördjupningskurs för erfarna ledare som vill driva AI-driven organisationsförändring. AI-verktyg, avancerad prompting och att leda transformationsinitiativ. Kräver minst 5 års yrkeserfarenhet. Max 14 deltagare. Leverantör: Berghs School of Communication | Pris: 45 500 SEK exkl. moms | https://www.berghs.se/kurs/ai-for-forandringsledare-professional-dagtid/', 399, None, 'advanced', 'hybrid', 34, 4, 22, False, False, 'published'),

        # --- Executive (3 kurser) ---
        ('Anders Nyström', 'executive-leadership', 'Chef och ledare (SSE)', 'sse-chef-och-ledare',
         'SSE Executive Educations program för operativa chefer med 2+ års erfarenhet. Integrerar affärsstrategi, finansiell styrning och personlig ledarskapsutveckling. 12 dagar uppdelade i 4 moduler över 4 månader vid Campus Kampasten, Sigtuna. Leverantör: SSE Executive Education / Handelshögskolan i Stockholm | Pris: 116 000 SEK exkl. moms | https://www.exedsse.se/program/chef-och-ledare/', 599, None, 'executive', 'live', 96, 4, 24, False, True, 'published'),
        ('Anders Nyström', 'executive-leadership', 'Executive Leadership Program (SSE)', 'sse-executive-leadership-program',
         'SSE Executive Educations mest omfattande general management-program för seniora ledare. Personligt ledarskap, konkurrensfördelar, innovation, finansiell styrning, organisationsförändring och framtidsstrategi. 25 dagar, 6 moduler över 7 månader. Leverantör: SSE Executive Education / Handelshögskolan i Stockholm | Pris: 265 000 SEK exkl. moms | https://www.exedsse.se/program/executive-leadership-program/', 999, None, 'executive', 'live', 200, 6, 36, False, True, 'published'),
        ('Karin Svensson', 'innovation-digital', 'Executive Program in Industrial Management', 'kth-executive-industrial-management',
         'KTH Executive Schools transformativa program för seniora chefer i teknikdrivna företag. Digital disruption, AI-implementering, affärsstrategi, innovation och förändringsledarskap. Deltagare från ABB, Scania, Volvo Cars. 7 månader. Leverantör: KTH Executive School | Pris: 185 000 SEK exkl. moms | https://kthexecutiveschool.se/executive-program-in-industrial-management-2026-spring/', 899, None, 'executive', 'hybrid', 96, 4, 24, False, False, 'published'),
    ]

    course_inserts = []
    for c in courses_data:
        inst_name, cat_slug, title, slug, desc, price, orig, level, fmt, hours, mods, lessons, best, feat, status = c
        course_inserts.append({
            'instructor_id': inst_map[inst_name], 'category_id': cat_map[cat_slug],
            'title': title, 'slug': slug, 'description': desc, 'short_description': desc,
            'price': price, 'original_price': orig, 'level': level, 'format': fmt,
            'duration_hours': hours, 'total_modules': mods, 'total_lessons': lessons,
            'is_bestseller': best, 'is_featured': feat, 'status': status,
            'created_at': (now - timedelta(days=random.randint(30, 365))).isoformat()
        })

    inserted_courses = db.insert('courses', course_inserts)
    course_map = {c['slug']: c['id'] for c in inserted_courses}
    print(f'  {len(inserted_courses)} courses created')

    # ============================================================
    # CURRICULUM: Modules & Lessons for ALL published courses
    # ============================================================
    print('Seeding curriculum...')

    # Full curriculum data: slug -> list of (module_title, [(lesson_title, type, duration_min), ...])
    curriculum = {
        'strategic-leadership-masterclass': [
            ('Module 1: Foundations of Strategic Leadership', [
                ('Introduction to Strategic Leadership', 'video', 12.5),
                ('The Leadership Mindset Shift', 'video', 22.25),
                ('Reading: Strategic Thinking Frameworks', 'reading', 15),
                ('Defining Your Leadership Philosophy', 'video', 28.67),
                ('Exercise: Personal Leadership Assessment', 'exercise', 30),
                ('Module Recap & Key Takeaways', 'video', 8.17),
            ]),
            ('Module 2: Vision & Strategy Development', [
                ('Crafting Organizational Vision', 'video', 25),
                ('Strategic Planning Frameworks', 'video', 30),
                ('Aligning Vision with Execution', 'video', 20),
                ('Case Study: Vision-Led Transformation', 'reading', 20),
                ('Workshop: Building Your Strategic Plan', 'exercise', 45),
                ('Communicating Strategy Effectively', 'video', 22),
                ('Module Review', 'video', 8),
            ]),
            ('Module 3: Stakeholder Management & Influence', [
                ('Understanding Stakeholder Dynamics', 'video', 25),
                ('Power Mapping & Influence Strategies', 'video', 28),
                ('Building Executive Presence', 'video', 22),
                ('Negotiation for Leaders', 'video', 30),
                ('Exercise: Stakeholder Mapping', 'exercise', 35),
                ('Module Review', 'video', 8),
            ]),
            ('Module 4: Leading High-Performance Teams', [
                ('Team Formation & Development Stages', 'video', 20),
                ('Building Psychological Safety', 'video', 25),
                ('Delegation & Empowerment', 'video', 22),
                ('Managing Diverse Teams', 'video', 28),
                ('Performance Management Frameworks', 'video', 25),
                ('Exercise: Team Assessment', 'exercise', 40),
                ('Module Review', 'video', 8),
            ]),
            ('Module 5: Driving Organizational Change', [
                ('Change Management Models', 'video', 25),
                ('Leading Through Resistance', 'video', 22),
                ('Building a Change-Ready Culture', 'video', 20),
                ('Measuring Change Impact', 'video', 18),
                ('Final Case Study: Enterprise Transformation', 'exercise', 45),
                ('Course Summary & Next Steps', 'video', 10),
            ]),
        ],
        'leading-with-emotional-intelligence': [
            ('Module 1: The EI Advantage in Leadership', [
                ('Why Emotional Intelligence Matters', 'video', 18),
                ('The Neuroscience of Emotions at Work', 'video', 22),
                ('Reading: EI Research in Leadership', 'reading', 15),
                ('Self-Assessment: Your EI Baseline', 'exercise', 25),
                ('The Four Quadrants of EI', 'video', 20),
                ('Module Recap', 'video', 8),
            ]),
            ('Module 2: Self-Awareness & Self-Regulation', [
                ('Recognizing Your Emotional Patterns', 'video', 20),
                ('Triggers, Reactions, and Responses', 'video', 25),
                ('Mindfulness for Leaders', 'video', 18),
                ('Exercise: Emotional Journaling', 'exercise', 30),
                ('Managing Stress Under Pressure', 'video', 22),
                ('Module Review', 'video', 8),
            ]),
            ('Module 3: Empathy & Social Awareness', [
                ('Active Listening Deep Dive', 'video', 20),
                ('Reading Organizational Emotions', 'video', 22),
                ('Cross-Cultural Emotional Intelligence', 'video', 18),
                ('Reading: Empathy in Action Case Studies', 'reading', 15),
                ('Exercise: Perspective-Taking Scenarios', 'exercise', 35),
                ('Module Review', 'video', 8),
            ]),
            ('Module 4: Relationship Management', [
                ('Influence Through Connection', 'video', 22),
                ('Coaching Conversations with EI', 'video', 25),
                ('Navigating Difficult Team Dynamics', 'video', 20),
                ('Building Trust at Scale', 'video', 18),
                ('Final Exercise: Your EI Development Plan', 'exercise', 35),
                ('Course Summary', 'video', 10),
            ]),
        ],
        'c-suite-communication': [
            ('Module 1: Executive Communication Foundations', [
                ('The Language of the C-Suite', 'video', 18),
                ('Structuring Executive Messages', 'video', 22),
                ('Reading: Communication Frameworks', 'reading', 12),
                ('Brevity, Clarity, Impact', 'video', 20),
                ('Exercise: Executive Summary Writing', 'exercise', 25),
                ('Module Recap', 'video', 8),
            ]),
            ('Module 2: Boardroom Presentations', [
                ('Presenting to the Board', 'video', 25),
                ('Data Visualization for Executives', 'video', 20),
                ('Handling Tough Questions', 'video', 22),
                ('Reading: Boardroom Case Studies', 'reading', 15),
                ('Exercise: Build Your Board Deck', 'exercise', 35),
                ('Module Review', 'video', 8),
            ]),
            ('Module 3: Crisis & Stakeholder Communication', [
                ('Crisis Communication Principles', 'video', 22),
                ('Media Training for Executives', 'video', 20),
                ('Internal Communication in Crisis', 'video', 18),
                ('Stakeholder Communication Planning', 'video', 22),
                ('Exercise: Crisis Response Simulation', 'exercise', 35),
                ('Course Summary', 'video', 10),
            ]),
        ],
        'change-management-fundamentals': [
            ('Module 1: Foundations of Change', [
                ('Why Organizations Must Change', 'video', 18),
                ('The Psychology of Change', 'video', 22),
                ('Reading: Change Management History', 'reading', 12),
                ('Assessing Change Readiness', 'video', 20),
                ('Exercise: Change Impact Assessment', 'exercise', 25),
            ]),
            ('Module 2: Change Frameworks', [
                ('Kotter\'s 8-Step Model', 'video', 25),
                ('The ADKAR Model', 'video', 22),
                ('Lewin\'s Change Model', 'video', 18),
                ('Reading: Comparing Frameworks', 'reading', 15),
                ('Exercise: Choose Your Framework', 'exercise', 30),
            ]),
            ('Module 3: Managing Resistance', [
                ('Understanding Resistance', 'video', 20),
                ('Communication During Change', 'video', 22),
                ('Building a Coalition of Support', 'video', 18),
                ('Reading: Resistance Case Studies', 'reading', 15),
                ('Exercise: Resistance Strategy Plan', 'exercise', 30),
            ]),
            ('Module 4: Sustaining Change', [
                ('Embedding Change in Culture', 'video', 22),
                ('Measuring Change Success', 'video', 18),
                ('Continuous Improvement Cycles', 'video', 20),
                ('Reading: Long-Term Change Studies', 'reading', 12),
                ('Final Exercise: Your Change Plan', 'exercise', 35),
            ]),
        ],
        'executive-decision-making': [
            ('Module 1: Decision-Making Foundations', [
                ('The Anatomy of Executive Decisions', 'video', 20),
                ('Cognitive Biases in Decision Making', 'video', 25),
                ('Reading: Behavioral Economics for Leaders', 'reading', 15),
                ('Data-Driven vs. Intuitive Decisions', 'video', 22),
                ('Exercise: Bias Identification', 'exercise', 25),
                ('Module Recap', 'video', 8),
                ('Decision Quality Frameworks', 'video', 18),
            ]),
            ('Module 2: Risk & Uncertainty', [
                ('Navigating Ambiguity', 'video', 22),
                ('Risk Assessment Frameworks', 'video', 25),
                ('Scenario Planning Basics', 'video', 20),
                ('Reading: Risk in Practice', 'reading', 15),
                ('Exercise: Risk Matrix Workshop', 'exercise', 30),
                ('Decision Trees & Expected Value', 'video', 18),
                ('Module Review', 'video', 8),
            ]),
            ('Module 3: Strategic Decision Alignment', [
                ('Aligning Decisions with Strategy', 'video', 22),
                ('Stakeholder Impact Analysis', 'video', 20),
                ('Speed vs. Quality Tradeoffs', 'video', 18),
                ('Group Decision Making', 'video', 22),
                ('Reading: Decision Case Studies', 'reading', 15),
                ('Exercise: Decision Audit', 'exercise', 35),
                ('Final Summary: Your Decision Framework', 'video', 12),
                ('Course Wrap-up', 'video', 8),
            ]),
        ],
        'board-level-leadership': [
            ('Module 1: Board Governance Essentials', [
                ('The Role of the Board', 'video', 20),
                ('Fiduciary Duties & Legal Framework', 'video', 25),
                ('Board Composition & Dynamics', 'video', 22),
                ('Reading: Governance Best Practices', 'reading', 15),
                ('Exercise: Board Readiness Self-Assessment', 'exercise', 25),
            ]),
            ('Module 2: Strategic Oversight', [
                ('Strategic Review Processes', 'video', 22),
                ('Financial Oversight for Board Members', 'video', 25),
                ('Risk Oversight & Compliance', 'video', 20),
                ('Reading: Board Failure Case Studies', 'reading', 15),
                ('Exercise: Strategic Review Simulation', 'exercise', 30),
            ]),
            ('Module 3: Board Effectiveness', [
                ('CEO-Board Relationship', 'video', 22),
                ('Succession Planning', 'video', 20),
                ('Shareholder & Stakeholder Engagement', 'video', 18),
                ('Board Evaluation & Improvement', 'video', 20),
                ('Reading: High-Performing Boards', 'reading', 12),
                ('Final Exercise: Your Board Development Plan', 'exercise', 30),
            ]),
        ],
        'executive-communication-influence': [
            ('Module 1: Foundations of Influence', [
                ('The Science of Persuasion', 'video', 20),
                ('Building Credibility & Trust', 'video', 22),
                ('Reading: Cialdini\'s Influence Principles', 'reading', 15),
                ('Your Communication Style Profile', 'video', 18),
                ('Exercise: Influence Style Assessment', 'exercise', 25),
                ('Module Recap', 'video', 8),
            ]),
            ('Module 2: Executive Storytelling', [
                ('The Power of Narrative', 'video', 22),
                ('Story Structures for Business', 'video', 25),
                ('Data + Story: Making Numbers Sing', 'video', 20),
                ('Reading: Great Business Narratives', 'reading', 15),
                ('Exercise: Craft Your Leadership Story', 'exercise', 30),
                ('Module Review', 'video', 8),
            ]),
            ('Module 3: Presence & Delivery', [
                ('Executive Presence Defined', 'video', 22),
                ('Body Language & Non-Verbal Cues', 'video', 18),
                ('Voice, Tone & Pacing', 'video', 20),
                ('Handling Q&A with Confidence', 'video', 22),
                ('Exercise: Presentation Practice', 'exercise', 35),
                ('Module Review', 'video', 8),
            ]),
            ('Module 4: Strategic Communication', [
                ('Communicating Change', 'video', 22),
                ('Cross-Functional Influence', 'video', 20),
                ('Difficult Messages & Bad News', 'video', 18),
                ('Virtual Communication Mastery', 'video', 20),
                ('Final Exercise: Communication Strategy Plan', 'exercise', 35),
                ('Course Summary', 'video', 10),
            ]),
        ],
        'high-performance-team-leadership': [
            ('Module 1: Team Foundations', [
                ('What Makes a Team High-Performing', 'video', 18),
                ('Tuckman\'s Stages of Team Development', 'video', 22),
                ('Reading: Google\'s Project Aristotle', 'reading', 15),
                ('Team Charter Creation', 'video', 20),
                ('Exercise: Team Diagnostic', 'exercise', 25),
                ('Module Recap', 'video', 8),
            ]),
            ('Module 2: Psychological Safety', [
                ('Understanding Psychological Safety', 'video', 22),
                ('Creating Safe-to-Fail Environments', 'video', 20),
                ('Feedback Culture Building', 'video', 18),
                ('Reading: Amy Edmondson\'s Research', 'reading', 15),
                ('Exercise: Safety Audit', 'exercise', 30),
            ]),
            ('Module 3: Role Clarity & Accountability', [
                ('Defining Roles & Responsibilities', 'video', 20),
                ('RACI and Accountability Frameworks', 'video', 22),
                ('Delegation That Works', 'video', 18),
                ('Reading: Accountability Case Studies', 'reading', 12),
                ('Exercise: RACI Matrix Workshop', 'exercise', 30),
                ('Module Review', 'video', 8),
            ]),
            ('Module 4: Collaboration & Conflict', [
                ('Cross-Functional Collaboration', 'video', 22),
                ('Healthy Conflict vs. Dysfunction', 'video', 20),
                ('Resolving Team Tensions', 'video', 18),
                ('Reading: Patrick Lencioni\'s 5 Dysfunctions', 'reading', 15),
                ('Exercise: Conflict Resolution Roleplay', 'exercise', 30),
                ('Module Review', 'video', 8),
            ]),
            ('Module 5: Performance & Growth', [
                ('Setting Team Goals & OKRs', 'video', 22),
                ('Performance Reviews That Work', 'video', 20),
                ('Developing Team Members', 'video', 18),
                ('Celebrating Wins & Learning from Losses', 'video', 15),
                ('Final Exercise: Team Development Plan', 'exercise', 35),
                ('Course Summary', 'video', 10),
            ]),
        ],
        'leading-organizational-change': [
            ('Module 1: The Case for Change', [
                ('Building the Business Case', 'video', 22),
                ('Stakeholder Analysis for Change', 'video', 25),
                ('Reading: Transformation Success Rates', 'reading', 15),
                ('Creating Urgency Without Panic', 'video', 20),
                ('Exercise: Business Case Builder', 'exercise', 30),
                ('Module Recap', 'video', 8),
            ]),
            ('Module 2: Designing the Change', [
                ('Vision & Roadmap for Change', 'video', 25),
                ('Organizational Readiness Assessment', 'video', 22),
                ('Change Architecture', 'video', 20),
                ('Reading: Change Design Principles', 'reading', 15),
                ('Exercise: Change Roadmap Workshop', 'exercise', 35),
                ('Module Review', 'video', 8),
            ]),
            ('Module 3: Leading Through Transition', [
                ('The Human Side of Change', 'video', 22),
                ('Communication Strategies', 'video', 25),
                ('Managing Resistance & Emotions', 'video', 20),
                ('Middle Manager Engagement', 'video', 18),
                ('Exercise: Transition Plan', 'exercise', 30),
                ('Module Review', 'video', 8),
            ]),
            ('Module 4: Embedding & Sustaining', [
                ('Culture Change Mechanisms', 'video', 22),
                ('Reinforcing New Behaviors', 'video', 20),
                ('Measuring Transformation Progress', 'video', 18),
                ('Reading: Sustaining Change Studies', 'reading', 15),
                ('Exercise: Sustainability Dashboard', 'exercise', 30),
                ('Module Review', 'video', 8),
            ]),
            ('Module 5: Advanced Transformation', [
                ('Enterprise-Wide Transformation', 'video', 25),
                ('Digital Transformation & Change', 'video', 22),
                ('Global Change Management', 'video', 20),
                ('Reading: Fortune 500 Case Study', 'reading', 18),
                ('Final Exercise: Transformation Blueprint', 'exercise', 40),
                ('Course Summary', 'video', 10),
            ]),
        ],
        'coaching-for-senior-leaders': [
            ('Module 1: The Coaching Leader', [
                ('Why Leaders Must Coach', 'video', 20),
                ('Coaching vs. Managing vs. Mentoring', 'video', 22),
                ('Reading: ICF Core Competencies', 'reading', 15),
                ('The GROW Coaching Model', 'video', 25),
                ('Exercise: Coaching Style Self-Assessment', 'exercise', 25),
                ('Module Recap', 'video', 8),
            ]),
            ('Module 2: Coaching Conversations', [
                ('Powerful Questions', 'video', 22),
                ('Active Listening in Coaching', 'video', 20),
                ('Giving Feedback as a Coach', 'video', 18),
                ('Reading: Coaching Conversation Examples', 'reading', 12),
                ('Exercise: Practice Coaching Session', 'exercise', 35),
                ('Module Review', 'video', 8),
                ('Overcoming Coaching Resistance', 'video', 18),
            ]),
            ('Module 3: Advanced Coaching Techniques', [
                ('Coaching for Performance Improvement', 'video', 22),
                ('Coaching High-Potential Leaders', 'video', 25),
                ('Team Coaching Approaches', 'video', 20),
                ('Reading: Coaching ROI Studies', 'reading', 15),
                ('Exercise: Coaching Plan for Your Team', 'exercise', 35),
                ('Final Summary: Building a Coaching Culture', 'video', 12),
                ('Course Wrap-up', 'video', 8),
            ]),
        ],
        'strategic-decision-making': [
            ('Module 1: Strategic Analysis Tools', [
                ('Porter\'s Five Forces in Practice', 'video', 25),
                ('PESTEL & Macro Environment', 'video', 22),
                ('SWOT: Beyond the Basics', 'video', 20),
                ('Reading: Strategy Analysis Frameworks', 'reading', 15),
                ('Exercise: Industry Analysis', 'exercise', 30),
            ]),
            ('Module 2: Competitive Intelligence', [
                ('Understanding Competitive Dynamics', 'video', 22),
                ('Blue Ocean Strategy', 'video', 25),
                ('Reading: Competitive Advantage Cases', 'reading', 15),
                ('Competitor Profiling Techniques', 'video', 20),
                ('Exercise: Competitive Landscape Map', 'exercise', 30),
                ('Module Review', 'video', 8),
            ]),
            ('Module 3: Scenario Planning', [
                ('Introduction to Scenario Planning', 'video', 22),
                ('Building Scenarios Step by Step', 'video', 25),
                ('Using Scenarios for Strategy', 'video', 20),
                ('Reading: Shell Scenario Planning Case', 'reading', 15),
                ('Exercise: Build Your Scenarios', 'exercise', 35),
                ('Module Review', 'video', 8),
            ]),
            ('Module 4: Decision Under Uncertainty', [
                ('Real Options Thinking', 'video', 22),
                ('Game Theory for Strategists', 'video', 25),
                ('Decision Quality & Governance', 'video', 20),
                ('Reading: Strategic Decision Failures', 'reading', 15),
                ('Exercise: Strategic Decision Simulation', 'exercise', 35),
                ('Course Summary', 'video', 10),
            ]),
        ],
        'women-in-leadership': [
            ('Module 1: The Leadership Landscape', [
                ('Women in Leadership: Current State', 'video', 22),
                ('Understanding Systemic Barriers', 'video', 20),
                ('Reading: Research on Gender & Leadership', 'reading', 15),
                ('Your Leadership Identity', 'video', 18),
                ('Exercise: Personal Brand Assessment', 'exercise', 25),
            ]),
            ('Module 2: Building Confidence & Presence', [
                ('Overcoming Imposter Syndrome', 'video', 22),
                ('Executive Presence for Women', 'video', 25),
                ('Negotiating Your Value', 'video', 20),
                ('Reading: Lean In & Beyond', 'reading', 12),
                ('Exercise: Confidence Action Plan', 'exercise', 30),
            ]),
            ('Module 3: Networks & Sponsorship', [
                ('Strategic Networking', 'video', 20),
                ('Mentors vs. Sponsors', 'video', 18),
                ('Building Your Board of Advisors', 'video', 22),
                ('Reading: Sponsorship Research', 'reading', 12),
                ('Exercise: Network Mapping', 'exercise', 28),
            ]),
            ('Module 4: Leading Change for Equity', [
                ('Advocating for Inclusion', 'video', 22),
                ('Allyship & Amplification', 'video', 18),
                ('Work-Life Integration', 'video', 20),
                ('Reading: Organizations Leading the Way', 'reading', 15),
                ('Final Exercise: Your Leadership Action Plan', 'exercise', 30),
            ]),
        ],
        'conflict-resolution-mastery': [
            ('Module 1: Understanding Conflict', [
                ('The Nature of Workplace Conflict', 'video', 20),
                ('Conflict Styles Assessment', 'video', 22),
                ('Reading: Thomas-Kilmann Model', 'reading', 12),
                ('When Conflict is Healthy', 'video', 18),
                ('Exercise: Your Conflict Profile', 'exercise', 25),
                ('Module Recap', 'video', 8),
            ]),
            ('Module 2: Core Resolution Skills', [
                ('Active Listening in Conflict', 'video', 22),
                ('De-escalation Techniques', 'video', 20),
                ('Finding Common Ground', 'video', 18),
                ('Reading: Mediation Principles', 'reading', 12),
                ('Exercise: Mediation Roleplay', 'exercise', 30),
                ('Module Review', 'video', 8),
            ]),
            ('Module 3: Advanced Conflict Scenarios', [
                ('Team Conflict & Group Dynamics', 'video', 22),
                ('Cross-Cultural Conflict', 'video', 18),
                ('Conflict with Senior Stakeholders', 'video', 20),
                ('Reading: Conflict Resolution Case Studies', 'reading', 15),
                ('Final Exercise: Conflict Resolution Playbook', 'exercise', 30),
                ('Course Summary', 'video', 10),
            ]),
        ],
        'remote-team-leadership': [
            ('Module 1: Remote Leadership Fundamentals', [
                ('The Remote Leadership Mindset', 'video', 18),
                ('Trust & Autonomy in Remote Teams', 'video', 22),
                ('Reading: Remote Work Research', 'reading', 12),
                ('Communication Cadence Design', 'video', 20),
                ('Exercise: Remote Team Audit', 'exercise', 25),
            ]),
            ('Module 2: Communication & Collaboration', [
                ('Asynchronous vs. Synchronous Work', 'video', 22),
                ('Meeting Design for Remote Teams', 'video', 20),
                ('Tools & Technology Stack', 'video', 18),
                ('Reading: Best Practices from GitLab & Automattic', 'reading', 15),
                ('Exercise: Communication Plan', 'exercise', 28),
            ]),
            ('Module 3: Culture & Engagement', [
                ('Building Culture Remotely', 'video', 22),
                ('Onboarding Remote Team Members', 'video', 20),
                ('Preventing Isolation & Burnout', 'video', 18),
                ('Reading: Remote Culture Case Studies', 'reading', 12),
                ('Exercise: Culture-Building Activities', 'exercise', 25),
            ]),
            ('Module 4: Performance & Growth', [
                ('Managing Performance Remotely', 'video', 22),
                ('Developing Remote Talent', 'video', 20),
                ('Cross-Timezone Coordination', 'video', 18),
                ('Reading: Remote Performance Metrics', 'reading', 12),
                ('Final Exercise: Remote Team Playbook', 'exercise', 30),
            ]),
        ],
        # --- NEW COURSES CURRICULUM ---
        'leadership-foundations-first-90-days': [
            ('Module 1: Your Leadership Launchpad', [
                ('Welcome & What to Expect', 'video', 10),
                ('The Transition from Individual Contributor', 'video', 18),
                ('Reading: The First 90 Days Framework', 'reading', 12),
                ('Building Credibility Early', 'video', 22),
                ('Exercise: Your First-Week Action Plan', 'exercise', 25),
                ('Module Recap', 'video', 8),
            ]),
            ('Module 2: Essential Leadership Skills', [
                ('Running Effective One-on-Ones', 'video', 22),
                ('Delegation 101: What, When, and How', 'video', 20),
                ('Giving Feedback That Lands', 'video', 18),
                ('Reading: Situational Leadership Basics', 'reading', 12),
                ('Exercise: Delegation Practice Scenarios', 'exercise', 28),
                ('Module Review', 'video', 8),
            ]),
            ('Module 3: Building Relationships & Momentum', [
                ('Mapping Your Stakeholders', 'video', 20),
                ('Managing Up: Working with Your Boss', 'video', 18),
                ('Building Team Trust Quickly', 'video', 22),
                ('Reading: Quick Wins That Matter', 'reading', 12),
                ('Exercise: Your 90-Day Plan', 'exercise', 30),
                ('Course Summary & Next Steps', 'video', 10),
            ]),
        ],
        'communication-essentials-new-leaders': [
            ('Module 1: Communication Foundations', [
                ('Why Communication is Your #1 Skill', 'video', 15),
                ('Listening Before Speaking', 'video', 20),
                ('Clarity: Saying What You Mean', 'video', 18),
                ('Reading: Communication Styles Overview', 'reading', 12),
                ('Exercise: Active Listening Practice', 'exercise', 25),
            ]),
            ('Module 2: Everyday Leader Communication', [
                ('Running Effective Meetings', 'video', 22),
                ('Writing Clear Emails & Messages', 'video', 18),
                ('Giving Direction Without Micromanaging', 'video', 20),
                ('Reading: Meeting Best Practices', 'reading', 12),
                ('Exercise: Meeting Redesign Workshop', 'exercise', 25),
                ('Module Review', 'video', 8),
            ]),
            ('Module 3: Feedback & Difficult Messages', [
                ('The Art of Constructive Feedback', 'video', 22),
                ('Receiving Feedback Gracefully', 'video', 18),
                ('Having Your First Tough Conversation', 'video', 20),
                ('Reading: Feedback Models (SBI, COIN)', 'reading', 12),
                ('Exercise: Feedback Practice Scenarios', 'exercise', 28),
                ('Course Wrap-up', 'video', 10),
            ]),
        ],
        'emotional-intelligence-101': [
            ('Module 1: Understanding Emotional Intelligence', [
                ('What Is Emotional Intelligence?', 'video', 12),
                ('The Science Behind EI', 'video', 18),
                ('Reading: Goleman\'s EI Framework', 'reading', 15),
                ('Self-Awareness: Know Your Triggers', 'video', 22),
                ('Exercise: Personal EI Assessment', 'exercise', 30),
                ('Module Recap', 'video', 8),
            ]),
            ('Module 2: Managing Yourself and Others', [
                ('Self-Regulation Strategies', 'video', 20),
                ('Motivation and Internal Drive', 'video', 18),
                ('Empathy in the Workplace', 'video', 25),
                ('Reading: Empathy vs. Sympathy in Leadership', 'reading', 12),
                ('Social Skills for Leaders', 'video', 22),
                ('Exercise: EI in Difficult Situations', 'exercise', 35),
            ]),
            ('Module 3: Applying EI to Leadership', [
                ('EI and Decision Making', 'video', 20),
                ('Building Emotionally Intelligent Teams', 'video', 25),
                ('Reading: Case Studies in EI Leadership', 'reading', 18),
                ('Handling Emotional Conflict', 'video', 22),
                ('Exercise: Your EI Development Plan', 'exercise', 40),
                ('Course Summary and Next Steps', 'video', 10),
            ]),
        ],
        'building-your-first-team': [
            ('Module 1: Team Planning', [
                ('Defining Your Team\'s Purpose', 'video', 18),
                ('Hiring: What to Look For', 'video', 22),
                ('Reading: Team Composition Research', 'reading', 12),
                ('Writing Job Descriptions That Attract Talent', 'video', 18),
                ('Exercise: Team Structure Blueprint', 'exercise', 25),
            ]),
            ('Module 2: Onboarding & Integration', [
                ('The First-Day Experience', 'video', 18),
                ('Setting Expectations Early', 'video', 20),
                ('Building Team Norms', 'video', 22),
                ('Reading: Onboarding Best Practices', 'reading', 12),
                ('Exercise: Onboarding Checklist Creation', 'exercise', 25),
                ('Module Review', 'video', 8),
            ]),
            ('Module 3: Growing Your Team', [
                ('Creating Development Plans', 'video', 20),
                ('Giving Feedback to New Team Members', 'video', 18),
                ('Building Team Identity', 'video', 22),
                ('Reading: First-Time Manager Lessons', 'reading', 12),
                ('Final Exercise: 6-Month Team Development Plan', 'exercise', 30),
            ]),
        ],
        'time-management-productivity-leaders': [
            ('Module 1: Priorities & Focus', [
                ('The Eisenhower Matrix for Leaders', 'video', 18),
                ('Identifying Your High-Impact Activities', 'video', 20),
                ('Reading: Deep Work for Managers', 'reading', 12),
                ('Exercise: Weekly Priority Audit', 'exercise', 22),
            ]),
            ('Module 2: Delegation & Energy Management', [
                ('Effective Delegation Framework', 'video', 22),
                ('Energy Management vs. Time Management', 'video', 18),
                ('Protecting Your Calendar', 'video', 15),
                ('Reading: Manager\'s Schedule Research', 'reading', 10),
                ('Exercise: Delegation Decision Tree', 'exercise', 25),
            ]),
            ('Module 3: Systems & Sustainability', [
                ('Building Personal Productivity Systems', 'video', 20),
                ('Meeting Hygiene for Leaders', 'video', 18),
                ('Avoiding Burnout', 'video', 15),
                ('Reading: Sustainable Productivity', 'reading', 10),
                ('Final Exercise: Your Productivity Playbook', 'exercise', 25),
                ('Course Summary', 'video', 8),
            ]),
        ],
        'digital-literacy-for-leaders': [
            ('Module 1: The Digital Landscape', [
                ('Technology Trends Every Leader Must Know', 'video', 22),
                ('Cloud Computing Demystified', 'video', 18),
                ('Data Analytics: What Leaders Need to Know', 'video', 20),
                ('Reading: Digital Transformation Overview', 'reading', 12),
                ('Exercise: Your Digital Fluency Assessment', 'exercise', 22),
            ]),
            ('Module 2: AI, Automation & Cybersecurity', [
                ('Artificial Intelligence Explained Simply', 'video', 22),
                ('Automation & Its Impact on Your Team', 'video', 18),
                ('Cybersecurity Basics for Non-Technical Leaders', 'video', 20),
                ('Reading: AI in the Enterprise', 'reading', 12),
                ('Exercise: Technology Opportunity Scan', 'exercise', 25),
                ('Module Review', 'video', 8),
            ]),
            ('Module 3: Leading in a Digital World', [
                ('Digital Communication & Collaboration Tools', 'video', 18),
                ('Data-Driven Decision Making', 'video', 22),
                ('Building a Tech-Savvy Team Culture', 'video', 18),
                ('Reading: Digital Leadership Case Studies', 'reading', 12),
                ('Final Exercise: Your Digital Leadership Plan', 'exercise', 25),
                ('Course Summary', 'video', 8),
            ]),
        ],
        'resilience-stress-management-leaders': [
            ('Module 1: Understanding Stress & Resilience', [
                ('The Stress-Performance Curve', 'video', 20),
                ('What Resilience Really Means', 'video', 18),
                ('Reading: Resilience Research in Leadership', 'reading', 15),
                ('Your Stress Triggers & Patterns', 'video', 22),
                ('Exercise: Stress Inventory', 'exercise', 25),
            ]),
            ('Module 2: Building Mental Toughness', [
                ('Cognitive Reframing Techniques', 'video', 22),
                ('Growth Mindset in Practice', 'video', 20),
                ('Bouncing Back from Setbacks', 'video', 18),
                ('Reading: Post-Traumatic Growth in Leaders', 'reading', 12),
                ('Exercise: Reframing Practice', 'exercise', 28),
            ]),
            ('Module 3: Sustainable Performance Habits', [
                ('Recovery & Renewal Cycles', 'video', 20),
                ('Boundaries for Leaders', 'video', 18),
                ('Mindfulness & Meditation Basics', 'video', 22),
                ('Reading: High-Performance Habits Research', 'reading', 15),
                ('Exercise: Your Recovery Plan', 'exercise', 25),
            ]),
            ('Module 4: Leading Resilient Teams', [
                ('Creating a Resilient Team Culture', 'video', 22),
                ('Supporting Struggling Team Members', 'video', 18),
                ('Organizational Resilience Strategies', 'video', 20),
                ('Reading: Team Resilience Case Studies', 'reading', 12),
                ('Final Exercise: Team Resilience Plan', 'exercise', 30),
                ('Course Summary', 'video', 10),
            ]),
        ],
        'leading-diverse-inclusive-teams': [
            ('Module 1: The Business Case for Inclusion', [
                ('Why Diversity Drives Performance', 'video', 22),
                ('Understanding Bias: Conscious & Unconscious', 'video', 25),
                ('Reading: McKinsey Diversity Research', 'reading', 15),
                ('Inclusive Leadership Behaviors', 'video', 20),
                ('Exercise: Bias Awareness Assessment', 'exercise', 25),
                ('Module Recap', 'video', 8),
            ]),
            ('Module 2: Creating Psychological Safety', [
                ('What Psychological Safety Looks Like', 'video', 22),
                ('Inclusive Communication Practices', 'video', 20),
                ('Microaggressions: Recognizing & Addressing', 'video', 18),
                ('Reading: Belonging at Work', 'reading', 12),
                ('Exercise: Team Inclusion Audit', 'exercise', 28),
            ]),
            ('Module 3: Equitable Processes', [
                ('Hiring for Diversity', 'video', 22),
                ('Equitable Performance Reviews', 'video', 20),
                ('Sponsorship & Advancement Equity', 'video', 18),
                ('Reading: Equity vs. Equality in Leadership', 'reading', 12),
                ('Exercise: Process Equity Review', 'exercise', 25),
                ('Module Review', 'video', 8),
            ]),
            ('Module 4: Sustaining an Inclusive Culture', [
                ('Allyship in Action', 'video', 22),
                ('Measuring Inclusion Progress', 'video', 18),
                ('Cross-Cultural Team Leadership', 'video', 20),
                ('Reading: Inclusive Culture Case Studies', 'reading', 15),
                ('Final Exercise: Your Inclusion Action Plan', 'exercise', 30),
                ('Course Summary', 'video', 10),
            ]),
        ],
        'hybrid-workplace-leadership': [
            ('Module 1: The Hybrid Reality', [
                ('Understanding Hybrid Work Models', 'video', 20),
                ('Equity Between Remote & In-Office', 'video', 22),
                ('Reading: Hybrid Work Research', 'reading', 12),
                ('Setting Hybrid Team Norms', 'video', 18),
                ('Exercise: Hybrid Readiness Assessment', 'exercise', 25),
                ('Module Recap', 'video', 8),
            ]),
            ('Module 2: Communication in Hybrid', [
                ('Inclusive Meeting Design', 'video', 22),
                ('Async Communication Mastery', 'video', 20),
                ('Documentation & Knowledge Sharing', 'video', 18),
                ('Reading: Hybrid Communication Best Practices', 'reading', 12),
                ('Exercise: Communication Cadence Design', 'exercise', 25),
                ('Module Review', 'video', 8),
            ]),
            ('Module 3: Culture & Performance', [
                ('Building Hybrid Team Culture', 'video', 22),
                ('Performance Management in Hybrid', 'video', 20),
                ('Preventing Proximity Bias', 'video', 18),
                ('Reading: Hybrid Culture Case Studies', 'reading', 12),
                ('Final Exercise: Hybrid Team Playbook', 'exercise', 28),
                ('Course Summary', 'video', 10),
            ]),
        ],
        'leading-digital-transformation': [
            ('Module 1: Digital Strategy Foundations', [
                ('What Digital Transformation Really Means', 'video', 22),
                ('Assessing Digital Maturity', 'video', 25),
                ('Reading: Digital Transformation Failures & Lessons', 'reading', 15),
                ('Creating the Digital Vision', 'video', 20),
                ('Exercise: Digital Maturity Assessment', 'exercise', 28),
                ('Module Recap', 'video', 8),
            ]),
            ('Module 2: Building the Roadmap', [
                ('Prioritizing Digital Initiatives', 'video', 22),
                ('Technology Selection Frameworks', 'video', 25),
                ('Building the Business Case', 'video', 20),
                ('Reading: Digital Roadmap Examples', 'reading', 15),
                ('Exercise: Roadmap Workshop', 'exercise', 30),
                ('Module Review', 'video', 8),
            ]),
            ('Module 3: People & Change', [
                ('Digital Skills Gap Analysis', 'video', 22),
                ('Change Management for Digital', 'video', 20),
                ('Building Digital Culture', 'video', 18),
                ('Reading: People-Centered Digital Transformation', 'reading', 15),
                ('Exercise: Change Adoption Plan', 'exercise', 28),
                ('Module Review', 'video', 8),
            ]),
            ('Module 4: Execution & Scaling', [
                ('Agile Delivery at Scale', 'video', 22),
                ('Measuring Digital ROI', 'video', 20),
                ('Scaling Successful Pilots', 'video', 18),
                ('Reading: Scaling Digital Case Studies', 'reading', 15),
                ('Final Exercise: Your Digital Transformation Plan', 'exercise', 35),
                ('Course Summary', 'video', 10),
            ]),
        ],
        'mentoring-skills-mid-level-managers': [
            ('Module 1: The Mentoring Mindset', [
                ('Mentoring vs. Coaching vs. Sponsoring', 'video', 18),
                ('The Business Impact of Mentoring', 'video', 20),
                ('Reading: Mentoring Research & ROI', 'reading', 12),
                ('Your Mentoring Style', 'video', 18),
                ('Exercise: Mentoring Readiness Assessment', 'exercise', 22),
                ('Module Recap', 'video', 8),
            ]),
            ('Module 2: Building the Mentoring Relationship', [
                ('Setting Expectations & Goals', 'video', 20),
                ('Building Trust with Mentees', 'video', 18),
                ('Effective Mentoring Conversations', 'video', 22),
                ('Reading: Mentoring Relationship Models', 'reading', 12),
                ('Exercise: First Mentoring Session Plan', 'exercise', 25),
                ('Module Review', 'video', 8),
            ]),
            ('Module 3: Advanced Mentoring Practice', [
                ('Career Development Guidance', 'video', 22),
                ('Mentoring Across Differences', 'video', 18),
                ('Group & Peer Mentoring', 'video', 20),
                ('Reading: Mentoring Program Design', 'reading', 12),
                ('Final Exercise: 6-Month Mentoring Plan', 'exercise', 28),
                ('Course Summary', 'video', 10),
            ]),
        ],
        'storytelling-business-leaders': [
            ('Module 1: The Power of Story', [
                ('Why Stories Move People', 'video', 20),
                ('Story Structures for Business', 'video', 22),
                ('Reading: The Science of Storytelling', 'reading', 15),
                ('Finding Your Stories', 'video', 18),
                ('Exercise: Story Mining Workshop', 'exercise', 25),
            ]),
            ('Module 2: Crafting Your Narratives', [
                ('The Vision Story', 'video', 22),
                ('The Change Story', 'video', 20),
                ('The Values Story', 'video', 18),
                ('Reading: Great Business Storytellers', 'reading', 15),
                ('Exercise: Craft Your Three Stories', 'exercise', 30),
            ]),
            ('Module 3: Data + Story', [
                ('Making Numbers Come Alive', 'video', 22),
                ('Visual Storytelling in Presentations', 'video', 20),
                ('Reading: Data Storytelling Best Practices', 'reading', 12),
                ('Storytelling in Difficult Situations', 'video', 18),
                ('Exercise: Data Story Presentation', 'exercise', 30),
            ]),
            ('Module 4: Delivery & Practice', [
                ('Voice, Pace, and Presence', 'video', 22),
                ('Adapting Stories to Your Audience', 'video', 18),
                ('Storytelling in Virtual Settings', 'video', 15),
                ('Reading: Audience Engagement Techniques', 'reading', 12),
                ('Final Exercise: Your Storytelling Portfolio', 'exercise', 30),
                ('Course Summary', 'video', 10),
            ]),
        ],
        'difficult-conversations-at-work': [
            ('Module 1: Why We Avoid & How to Prepare', [
                ('The Cost of Avoiding Difficult Conversations', 'video', 18),
                ('Psychological Barriers to Honest Talk', 'video', 20),
                ('Reading: Crucial Conversations Framework', 'reading', 12),
                ('Preparation: The Conversation Planner', 'video', 22),
                ('Exercise: Conversation Preparation Worksheet', 'exercise', 25),
            ]),
            ('Module 2: Having the Conversation', [
                ('Opening the Conversation Safely', 'video', 22),
                ('Staying in Dialogue Under Pressure', 'video', 20),
                ('Listening When It\'s Hard', 'video', 18),
                ('Reading: De-escalation Techniques', 'reading', 12),
                ('Exercise: Roleplay Scenarios', 'exercise', 30),
                ('Module Review', 'video', 8),
            ]),
            ('Module 3: Specific Scenarios & Follow-Through', [
                ('Performance Conversations', 'video', 22),
                ('Delivering Bad News', 'video', 18),
                ('Addressing Interpersonal Conflict', 'video', 20),
                ('Reading: Difficult Conversation Case Studies', 'reading', 12),
                ('Final Exercise: Your Difficult Conversation Playbook', 'exercise', 28),
                ('Course Summary', 'video', 10),
            ]),
        ],
        'advanced-emotional-intelligence-senior': [
            ('Module 1: EI at the Senior Level', [
                ('EI Challenges for Senior Leaders', 'video', 22),
                ('Reading Organizational Emotions', 'video', 25),
                ('Reading: Advanced EI Research', 'reading', 15),
                ('The EI-Strategy Connection', 'video', 20),
                ('Exercise: Senior Leader EI Audit', 'exercise', 28),
            ]),
            ('Module 2: Emotional Agility', [
                ('Emotional Agility in High-Stakes Situations', 'video', 25),
                ('Managing Your Emotional Reputation', 'video', 22),
                ('Authentic Leadership & Vulnerability', 'video', 20),
                ('Reading: Susan David\'s Emotional Agility', 'reading', 15),
                ('Exercise: Emotional Agility Practice', 'exercise', 30),
                ('Module Review', 'video', 8),
            ]),
            ('Module 3: Influence & Stakeholder Emotions', [
                ('Emotional Influence in Boardrooms', 'video', 25),
                ('Managing Up with Emotional Intelligence', 'video', 22),
                ('Cross-Cultural Emotional Intelligence', 'video', 20),
                ('Reading: Global EI Leadership', 'reading', 15),
                ('Exercise: Stakeholder Emotion Mapping', 'exercise', 28),
            ]),
            ('Module 4: Building EI Organizations', [
                ('Creating Emotionally Intelligent Teams', 'video', 22),
                ('EI in Organizational Design', 'video', 20),
                ('Measuring Organizational EI', 'video', 18),
                ('Reading: EI Culture Case Studies', 'reading', 12),
                ('Final Exercise: Organizational EI Strategy', 'exercise', 35),
                ('Course Summary', 'video', 10),
            ]),
        ],
        'crisis-leadership-organizational-resilience': [
            ('Module 1: Crisis Fundamentals', [
                ('Types of Organizational Crises', 'video', 22),
                ('Crisis Leadership vs. Normal Leadership', 'video', 25),
                ('Reading: Crisis Management Frameworks', 'reading', 15),
                ('The Psychology of Crisis', 'video', 20),
                ('Exercise: Crisis Vulnerability Assessment', 'exercise', 28),
                ('Module Recap', 'video', 8),
            ]),
            ('Module 2: Crisis Preparedness', [
                ('Building Crisis Plans', 'video', 25),
                ('Scenario Planning for Crises', 'video', 22),
                ('Crisis Communication Plans', 'video', 20),
                ('Reading: Crisis Preparedness Checklist', 'reading', 12),
                ('Exercise: Crisis Simulation Tabletop', 'exercise', 35),
                ('Module Review', 'video', 8),
            ]),
            ('Module 3: Leading During Crisis', [
                ('Decision Making Under Extreme Pressure', 'video', 25),
                ('Communicating in the Storm', 'video', 22),
                ('Team Management in Crisis', 'video', 20),
                ('Reading: Real-World Crisis Leadership Cases', 'reading', 18),
                ('Exercise: Crisis Response Simulation', 'exercise', 35),
                ('Module Review', 'video', 8),
            ]),
            ('Module 4: Recovery & Resilience', [
                ('Post-Crisis Recovery Planning', 'video', 22),
                ('Learning from Crisis: After-Action Reviews', 'video', 20),
                ('Building Organizational Resilience', 'video', 25),
                ('Reading: Organizational Resilience Research', 'reading', 15),
                ('Final Exercise: Resilience Blueprint', 'exercise', 35),
                ('Course Summary', 'video', 10),
            ]),
        ],
        'competitive-strategy-market-positioning': [
            ('Module 1: Strategic Analysis', [
                ('Industry Analysis: Beyond Porter\'s Five Forces', 'video', 25),
                ('Value Chain Analysis', 'video', 22),
                ('Reading: Competitive Strategy Classics', 'reading', 15),
                ('Identifying Competitive Advantages', 'video', 20),
                ('Exercise: Industry Structure Analysis', 'exercise', 30),
                ('Module Recap', 'video', 8),
            ]),
            ('Module 2: Competitive Positioning', [
                ('Blue Ocean Strategy in Practice', 'video', 25),
                ('Positioning Frameworks', 'video', 22),
                ('Disruptive Innovation Theory', 'video', 20),
                ('Reading: Positioning Case Studies', 'reading', 15),
                ('Exercise: Positioning Map Creation', 'exercise', 28),
                ('Module Review', 'video', 8),
            ]),
            ('Module 3: Competitive Intelligence', [
                ('Gathering Competitive Intelligence Ethically', 'video', 22),
                ('Competitor Profiling Techniques', 'video', 25),
                ('War Gaming & Competitor Simulation', 'video', 20),
                ('Reading: CI Best Practices', 'reading', 12),
                ('Exercise: Competitor Profile Build', 'exercise', 30),
            ]),
            ('Module 4: Strategy Execution', [
                ('From Strategy to Action', 'video', 22),
                ('Scenario Planning for Strategy', 'video', 25),
                ('Dynamic Strategy Adjustment', 'video', 20),
                ('Reading: Strategy Execution Failures', 'reading', 15),
                ('Final Exercise: Competitive Strategy Plan', 'exercise', 35),
                ('Course Summary', 'video', 10),
            ]),
        ],
        'innovation-leadership-idea-execution': [
            ('Module 1: Innovation Mindset', [
                ('What Innovation Really Means', 'video', 20),
                ('Types of Innovation', 'video', 22),
                ('Reading: Christensen\'s Innovation Framework', 'reading', 15),
                ('Creating a Culture of Innovation', 'video', 18),
                ('Exercise: Innovation Culture Audit', 'exercise', 25),
            ]),
            ('Module 2: Ideation & Design Thinking', [
                ('Design Thinking for Leaders', 'video', 25),
                ('Problem Framing & Opportunity Identification', 'video', 22),
                ('Ideation Techniques That Work', 'video', 20),
                ('Reading: Design Thinking Case Studies', 'reading', 15),
                ('Exercise: Design Sprint Planning', 'exercise', 30),
                ('Module Review', 'video', 8),
            ]),
            ('Module 3: Validation & Experimentation', [
                ('Lean Startup for Enterprises', 'video', 22),
                ('Building MVPs & Prototypes', 'video', 20),
                ('Testing & Learning Cycles', 'video', 18),
                ('Reading: Experimentation at Amazon & Google', 'reading', 15),
                ('Exercise: Experiment Design', 'exercise', 28),
            ]),
            ('Module 4: Scaling Innovation', [
                ('From Pilot to Scale', 'video', 22),
                ('Innovation Portfolio Management', 'video', 25),
                ('Overcoming Organizational Antibodies', 'video', 20),
                ('Reading: Scaling Innovation Case Studies', 'reading', 15),
                ('Final Exercise: Innovation Pipeline Plan', 'exercise', 30),
                ('Course Summary', 'video', 10),
            ]),
        ],
        'mergers-acquisitions-cultural-integration': [
            ('Module 1: The Human Side of M&A', [
                ('Why Culture Kills Deals', 'video', 22),
                ('Cultural Due Diligence', 'video', 25),
                ('Reading: M&A Failure Research', 'reading', 15),
                ('Stakeholder Impact Analysis', 'video', 20),
                ('Exercise: Cultural Assessment Framework', 'exercise', 28),
            ]),
            ('Module 2: Pre-Merger Planning', [
                ('Integration Strategy Design', 'video', 25),
                ('Communication Planning for M&A', 'video', 22),
                ('Talent Assessment & Retention', 'video', 20),
                ('Reading: Integration Planning Best Practices', 'reading', 15),
                ('Exercise: Integration Playbook', 'exercise', 30),
                ('Module Review', 'video', 8),
            ]),
            ('Module 3: Day One & Beyond', [
                ('The First 100 Days Post-Merger', 'video', 25),
                ('Managing Anxiety & Uncertainty', 'video', 22),
                ('Quick Wins & Symbol Management', 'video', 18),
                ('Reading: Day One Case Studies', 'reading', 12),
                ('Exercise: Day One Checklist', 'exercise', 25),
                ('Module Review', 'video', 8),
            ]),
            ('Module 4: Cultural Integration', [
                ('Building a Shared Culture', 'video', 25),
                ('Resolving Cultural Clashes', 'video', 22),
                ('Systems & Process Integration', 'video', 20),
                ('Reading: Cultural Integration Success Stories', 'reading', 15),
                ('Exercise: Cultural Integration Roadmap', 'exercise', 30),
            ]),
            ('Module 5: Long-Term Success', [
                ('Measuring Integration Success', 'video', 22),
                ('Rebuilding Engagement Post-Merger', 'video', 20),
                ('Lessons Learned & After-Action Review', 'video', 18),
                ('Reading: Long-Term M&A Outcomes', 'reading', 15),
                ('Final Exercise: Full Integration Plan', 'exercise', 35),
                ('Course Summary', 'video', 10),
            ]),
        ],
        'scaling-teams-10-to-1000': [
            ('Module 1: Growing Pains', [
                ('Recognizing Scaling Challenges', 'video', 22),
                ('Organizational Design Principles', 'video', 25),
                ('Reading: Scaling Organizations Research', 'reading', 15),
                ('When to Add Management Layers', 'video', 20),
                ('Exercise: Organizational Diagnostic', 'exercise', 25),
            ]),
            ('Module 2: Hiring at Scale', [
                ('Building a Hiring Machine', 'video', 22),
                ('Maintaining Culture While Hiring Fast', 'video', 20),
                ('Interview Process Design', 'video', 18),
                ('Reading: Hiring Playbooks from Hyper-Growth Companies', 'reading', 15),
                ('Exercise: Hiring Process Audit', 'exercise', 28),
                ('Module Review', 'video', 8),
            ]),
            ('Module 3: Systems & Processes', [
                ('Building Scalable Processes', 'video', 22),
                ('Communication at Scale', 'video', 20),
                ('Decision-Making Frameworks for Large Orgs', 'video', 18),
                ('Reading: Process Scaling Case Studies', 'reading', 12),
                ('Exercise: Process Design Workshop', 'exercise', 28),
                ('Module Review', 'video', 8),
            ]),
            ('Module 4: Culture & Leadership at Scale', [
                ('Preserving Culture Through Growth', 'video', 25),
                ('Developing Leaders Internally', 'video', 22),
                ('Managing Through Middle Managers', 'video', 20),
                ('Reading: Culture at Scale Case Studies', 'reading', 15),
                ('Final Exercise: Scaling Playbook', 'exercise', 30),
                ('Course Summary', 'video', 10),
            ]),
        ],
        'executive-coaching-certification-prep': [
            ('Module 1: Coaching Foundations & Ethics', [
                ('ICF Core Competency Framework', 'video', 25),
                ('Coaching Ethics & Standards', 'video', 22),
                ('Reading: ICF Code of Ethics', 'reading', 15),
                ('Establishing Coaching Agreements', 'video', 20),
                ('Exercise: Ethics Case Studies', 'exercise', 30),
                ('Module Recap', 'video', 8),
            ]),
            ('Module 2: Core Coaching Skills', [
                ('Powerful Questioning Techniques', 'video', 25),
                ('Direct Communication in Coaching', 'video', 22),
                ('Active Listening at a Deeper Level', 'video', 20),
                ('Creating Awareness in Clients', 'video', 18),
                ('Exercise: Coaching Skills Practice', 'exercise', 35),
                ('Module Review', 'video', 8),
            ]),
            ('Module 3: Advanced Coaching Models', [
                ('GROW, CLEAR, and OSCAR Models', 'video', 25),
                ('Systemic Coaching Approaches', 'video', 22),
                ('Somatic & Embodied Coaching', 'video', 20),
                ('Reading: Advanced Coaching Research', 'reading', 15),
                ('Exercise: Model Application Practice', 'exercise', 30),
                ('Module Review', 'video', 8),
            ]),
            ('Module 4: Coaching Practice Sessions', [
                ('Observed Coaching Session 1', 'exercise', 45),
                ('Feedback & Reflection', 'video', 20),
                ('Observed Coaching Session 2', 'exercise', 45),
                ('Reading: Coaching Supervision Framework', 'reading', 12),
                ('Peer Coaching Practice', 'exercise', 40),
                ('Module Review', 'video', 8),
            ]),
            ('Module 5: Certification Preparation', [
                ('Coaching Log & Documentation', 'video', 20),
                ('Mentor Coaching Overview', 'video', 18),
                ('Performance Evaluation Criteria', 'video', 22),
                ('Reading: ICF Certification Guide', 'reading', 15),
                ('Final Exercise: Mock Certification Assessment', 'exercise', 45),
                ('Course Summary & Next Steps', 'video', 12),
            ]),
        ],
        'geopolitical-risk-strategic-decisions': [
            ('Module 1: Geopolitical Landscape', [
                ('Understanding Geopolitical Risk', 'video', 22),
                ('Major Global Trends & Fault Lines', 'video', 25),
                ('Reading: Geopolitical Risk Frameworks', 'reading', 15),
                ('How Geopolitics Impacts Business', 'video', 20),
                ('Exercise: Geopolitical Risk Scan', 'exercise', 25),
            ]),
            ('Module 2: Trade & Regulatory Risk', [
                ('Global Trade Dynamics', 'video', 22),
                ('Sanctions, Tariffs & Trade Wars', 'video', 25),
                ('Regulatory Environment Mapping', 'video', 20),
                ('Reading: Trade Disruption Case Studies', 'reading', 15),
                ('Exercise: Regulatory Impact Assessment', 'exercise', 25),
            ]),
            ('Module 3: Decision Making Under Uncertainty', [
                ('Scenario Planning for Geopolitical Risk', 'video', 25),
                ('Building Organizational Agility', 'video', 22),
                ('Supply Chain Resilience', 'video', 20),
                ('Reading: Decision Making in Uncertain Times', 'reading', 15),
                ('Exercise: Scenario Development Workshop', 'exercise', 30),
            ]),
            ('Module 4: Strategic Positioning', [
                ('Geographic Diversification Strategies', 'video', 22),
                ('Political Risk Insurance & Hedging', 'video', 20),
                ('Building Geopolitical Intelligence Capabilities', 'video', 18),
                ('Reading: Global Strategy Case Studies', 'reading', 15),
                ('Final Exercise: Geopolitical Strategy Plan', 'exercise', 30),
                ('Course Summary', 'video', 10),
            ]),
        ],
        'ceo-transition-first-year-playbook': [
            ('Module 1: The CEO Transition', [
                ('The Unique Challenges of CEO Transitions', 'video', 25),
                ('Stakeholder Landscape Mapping', 'video', 22),
                ('Reading: CEO Transition Research', 'reading', 15),
                ('Your First 30 Days', 'video', 20),
                ('Exercise: Transition Assessment', 'exercise', 25),
            ]),
            ('Module 2: Board & Executive Team', [
                ('Building the Board Relationship', 'video', 25),
                ('Assembling Your Executive Team', 'video', 22),
                ('Reading: CEO-Board Dynamics', 'reading', 15),
                ('Managing Inherited Teams', 'video', 20),
                ('Exercise: Executive Team Assessment', 'exercise', 28),
            ]),
            ('Module 3: Strategic Agenda Setting', [
                ('Crafting Your Strategic Priorities', 'video', 22),
                ('Quick Wins vs. Long-Term Bets', 'video', 20),
                ('Communication Strategy', 'video', 18),
                ('Reading: First-Year CEO Playbooks', 'reading', 15),
                ('Exercise: 100-Day Strategic Plan', 'exercise', 30),
            ]),
            ('Module 4: Sustaining Momentum', [
                ('Building Organizational Credibility', 'video', 22),
                ('Culture Shaping as CEO', 'video', 20),
                ('Personal Resilience & Support', 'video', 18),
                ('Reading: CEO Longevity Studies', 'reading', 12),
                ('Final Exercise: First-Year Roadmap', 'exercise', 30),
            ]),
        ],
        'leading-in-uncertainty-executive-resilience': [
            ('Module 1: The Nature of Uncertainty', [
                ('VUCA World: Understanding Today\'s Environment', 'video', 25),
                ('The Leader\'s Role in Uncertain Times', 'video', 22),
                ('Reading: Uncertainty & Decision Research', 'reading', 15),
                ('Personal Response to Uncertainty', 'video', 20),
                ('Exercise: Uncertainty Tolerance Assessment', 'exercise', 25),
            ]),
            ('Module 2: Strategic Clarity in Fog', [
                ('Maintaining Strategic Focus', 'video', 25),
                ('Adaptive Strategy Frameworks', 'video', 22),
                ('Communication in Uncertainty', 'video', 20),
                ('Reading: Leading Through Ambiguity', 'reading', 15),
                ('Exercise: Adaptive Strategy Workshop', 'exercise', 28),
            ]),
            ('Module 3: Organizational Morale & Culture', [
                ('Keeping Teams Engaged & Motivated', 'video', 22),
                ('Transparent Leadership in Crisis', 'video', 20),
                ('Building Organizational Resilience', 'video', 25),
                ('Reading: Morale & Performance Research', 'reading', 15),
                ('Exercise: Resilience Culture Plan', 'exercise', 28),
            ]),
            ('Module 4: Personal Effectiveness', [
                ('Executive Self-Care & Recovery', 'video', 20),
                ('Decision Fatigue & Cognitive Load', 'video', 22),
                ('Building Your Support Network', 'video', 18),
                ('Reading: Executive Burnout Prevention', 'reading', 12),
                ('Final Exercise: Personal Resilience Blueprint', 'exercise', 30),
                ('Course Summary', 'video', 10),
            ]),
        ],
        'the-mindful-executive': [
            ('Module 1: Mindfulness Foundations', [
                ('What Mindfulness Is (and Isn\'t)', 'video', 18),
                ('The Neuroscience of Mindfulness', 'video', 22),
                ('Reading: Mindfulness Research in Leadership', 'reading', 15),
                ('Your First Mindfulness Practice', 'video', 20),
                ('Exercise: 7-Day Mindfulness Challenge', 'exercise', 25),
            ]),
            ('Module 2: Mindful Decision Making', [
                ('Pausing Before Reacting', 'video', 22),
                ('Mindful Communication', 'video', 20),
                ('Presence in High-Stakes Meetings', 'video', 18),
                ('Reading: Mindful Leadership Case Studies', 'reading', 12),
                ('Exercise: Mindful Meeting Practice', 'exercise', 25),
                ('Module Review', 'video', 8),
            ]),
            ('Module 3: Sustainable Leadership', [
                ('Energy Management & Renewal', 'video', 22),
                ('Compassionate Leadership', 'video', 20),
                ('Work-Life Integration', 'video', 18),
                ('Reading: Sustainable Performance Research', 'reading', 12),
                ('Final Exercise: Your Mindfulness Practice Plan', 'exercise', 25),
                ('Course Summary', 'video', 10),
            ]),
        ],
        'ai-strategy-senior-leaders': [
            ('Module 1: AI Landscape for Executives', [
                ('AI, ML, and GenAI: What You Need to Know', 'video', 22),
                ('Where AI Creates Business Value', 'video', 25),
                ('Reading: AI Strategy Frameworks', 'reading', 15),
                ('AI Readiness Assessment', 'video', 20),
                ('Exercise: AI Opportunity Identification', 'exercise', 25),
                ('Module Recap', 'video', 8),
            ]),
            ('Module 2: AI Governance & Ethics', [
                ('Responsible AI Principles', 'video', 22),
                ('AI Risk & Compliance', 'video', 25),
                ('Data Privacy & AI', 'video', 20),
                ('Reading: AI Governance Frameworks', 'reading', 15),
                ('Exercise: AI Governance Checklist', 'exercise', 25),
                ('Module Review', 'video', 8),
            ]),
            ('Module 3: Implementation & Talent', [
                ('Building AI Teams', 'video', 22),
                ('AI Vendor & Partner Selection', 'video', 20),
                ('Change Management for AI Adoption', 'video', 18),
                ('Reading: AI Implementation Case Studies', 'reading', 15),
                ('Final Exercise: Your AI Strategy Roadmap', 'exercise', 30),
                ('Course Summary', 'video', 10),
            ]),
        ],
        # ================================================================
        # SVENSKA KURSER — CURRICULUM
        # ================================================================
        # --- Wenell: Ny som chef ---
        'wenell-ny-som-chef': [
            ('Modul 1: Från expert till ledare', [
                ('Chefsrollens krav och möjligheter', 'video', 18),
                ('Kommunikation som ny chef', 'video', 22),
                ('Läsning: Wenells ledarskapsmodell', 'reading', 15),
                ('Coaching-verktyg för vardagen', 'video', 20),
                ('Övning: Din handlingsplan vecka 1', 'exercise', 25),
                ('Modulsammanfattning', 'video', 8),
            ]),
            ('Modul 2: Motivation och delegering', [
                ('Motivationsteorier i praktiken', 'video', 22),
                ('Delegering: Vad, när och hur', 'video', 20),
                ('Arbetsrätt för nya chefer', 'video', 18),
                ('Läsning: Situationsanpassat ledarskap — intro', 'reading', 12),
                ('Övning: Delegeringsscenarier', 'exercise', 28),
            ]),
            ('Modul 3: Teamutveckling', [
                ('Bygga förtroende i ditt team', 'video', 20),
                ('Effektiva medarbetarsamtal', 'video', 22),
                ('Feedback som utvecklar', 'video', 18),
                ('Läsning: Quick wins som ny chef', 'reading', 12),
                ('Övning: Din 90-dagarsplan', 'exercise', 30),
                ('Kurssammanfattning', 'video', 10),
            ]),
        ],
        # --- Hjärtum: Ny som chef ---
        'hjartum-ny-som-chef': [
            ('Modul 1: Chefsrollens grunder', [
                ('Välkommen till chefsrollen', 'video', 15),
                ('Beslutsfattande som ny chef', 'video', 22),
                ('Läsning: Hjärtums ledarskapsramverk', 'reading', 12),
                ('Kommunikationsteknik', 'video', 20),
                ('Övning: Självskattning som chef', 'exercise', 22),
                ('Modulsammanfattning', 'video', 8),
            ]),
            ('Modul 2: Konflikter och motivation', [
                ('Konflikthantering i vardagen', 'video', 22),
                ('Medarbetarmotivation', 'video', 20),
                ('Arbetsrätt — grunderna', 'video', 18),
                ('Läsning: AI i ledarskapet', 'reading', 12),
                ('Övning: Motivationsscenarier', 'exercise', 25),
            ]),
            ('Modul 3: Uppföljning och utveckling', [
                ('Ditt ledarskap i praktiken', 'video', 20),
                ('Sätta mål och följa upp', 'video', 18),
                ('Nästa steg — din utvecklingsplan', 'video', 15),
                ('Läsning: Uppföljningsmöte — förberedelse', 'reading', 12),
                ('Övning: Personlig handlingsplan', 'exercise', 28),
            ]),
        ],
        # --- Advantum: Ny som chef ---
        'advantum-ny-som-chef': [
            ('Modul 1: Ledarskapsrollen', [
                ('Från kollega till chef', 'video', 20),
                ('Förväntningar och mandat', 'video', 22),
                ('Läsning: Advantums ledarskapsmodell', 'reading', 15),
                ('Praktiska case-övningar', 'exercise', 30),
                ('Delegering i praktiken', 'video', 18),
                ('Modulsammanfattning', 'video', 8),
            ]),
            ('Modul 2: Kommunikation och feedback', [
                ('Feedbackmodeller som fungerar', 'video', 22),
                ('Coaching-samtal steg för steg', 'video', 25),
                ('Svåra samtal — förberedelse och genomförande', 'video', 20),
                ('Läsning: SBI-modellen i svenska organisationer', 'reading', 12),
                ('Övning: Feedback-träning', 'exercise', 30),
                ('Modulsammanfattning', 'video', 8),
            ]),
            ('Modul 3: Prioritering och uppföljning', [
                ('Prioritering som chef', 'video', 20),
                ('Sätta tydliga mål', 'video', 18),
                ('Personlig handlingsplan', 'video', 15),
                ('Läsning: 3-månaders uppföljning — förberedelse', 'reading', 12),
                ('Övning: Din utvecklingsplan', 'exercise', 30),
                ('Kurssammanfattning', 'video', 10),
            ]),
        ],
        # --- Hjärtum: Att leda utan att vara chef ---
        'hjartum-leda-utan-chef': [
            ('Modul 1: Ledarskap utan mandat', [
                ('Vad innebär det att leda utan chefsroll?', 'video', 18),
                ('Bygga förtroende och auktoritet', 'video', 22),
                ('Läsning: Informellt ledarskap — forskning', 'reading', 12),
                ('Övning: Din ledarskapskartläggning', 'exercise', 22),
            ]),
            ('Modul 2: Påverkan och kommunikation', [
                ('Övertyga utan formell makt', 'video', 22),
                ('Hantera konflikter som informell ledare', 'video', 20),
                ('Delegera utan att vara chef', 'video', 18),
                ('Övning: Påverkansscenarier', 'exercise', 25),
                ('Modulsammanfattning', 'video', 8),
            ]),
            ('Modul 3: Coaching och utveckling', [
                ('Coachande förhållningssätt', 'video', 20),
                ('Ge feedback som kollega', 'video', 18),
                ('Läsning: Teamledarens verktygslåda', 'reading', 12),
                ('Övning: Din handlingsplan', 'exercise', 25),
                ('Kurssammanfattning', 'video', 10),
            ]),
        ],
        # --- Wenell: Coachande ledarskap ---
        'wenell-coachande-ledarskap': [
            ('Modul 1: Vad är coachande ledarskap?', [
                ('Coaching vs. styrning vs. mentorskap', 'video', 18),
                ('Varför coaching fungerar', 'video', 20),
                ('Läsning: ICF:s kärnkompetenser', 'reading', 15),
                ('GROW-modellen steg för steg', 'video', 25),
                ('Övning: Självskattning av coachingstil', 'exercise', 22),
            ]),
            ('Modul 2: Coachingverktyg', [
                ('Kraftfulla frågor', 'video', 22),
                ('Aktivt lyssnande på djupare nivå', 'video', 20),
                ('Att ge feedback som coach', 'video', 18),
                ('Läsning: Coachingexempel', 'reading', 12),
                ('Övning: Coachingsamtal i par', 'exercise', 30),
                ('Modulsammanfattning', 'video', 8),
            ]),
            ('Modul 3: Coaching i vardagen', [
                ('Coaching i medarbetarsamtal', 'video', 22),
                ('Hantera motstånd mot coaching', 'video', 18),
                ('Bygga en coachingkultur', 'video', 20),
                ('Läsning: Coaching-ROI och forskning', 'reading', 12),
                ('Övning: Din coachingplan', 'exercise', 28),
                ('Kurssammanfattning', 'video', 10),
            ]),
        ],
        # --- Berghs: AI för framtidens ledare ---
        'berghs-ai-framtidens-ledare': [
            ('Modul 1: AI-grunder för ledare', [
                ('AI, ML och GenAI — vad du behöver veta', 'video', 20),
                ('Prompt engineering för chefer', 'video', 22),
                ('Läsning: AI-trender 2025–2026', 'reading', 12),
                ('Övning: Ditt första AI-projekt', 'exercise', 25),
            ]),
            ('Modul 2: AI i organisationen', [
                ('Strategisk AI-integration', 'video', 22),
                ('Beslutsfattande med AI-stöd', 'video', 20),
                ('Riskhantering och etik', 'video', 18),
                ('Övning: AI-möjlighetsanalys', 'exercise', 25),
                ('Modulsammanfattning', 'video', 8),
            ]),
            ('Modul 3: Bygga lärande kulturer', [
                ('Leda AI-förändringsarbete', 'video', 22),
                ('Bygga AI-kompetens i teamet', 'video', 18),
                ('Läsning: Svenska företags AI-resor', 'reading', 12),
                ('Övning: Din AI-handlingsplan', 'exercise', 25),
                ('Kurssammanfattning', 'video', 10),
            ]),
        ],
        # --- Företagsuniversitetet: UGL ---
        'fu-ugl-utveckling-grupp-ledare': [
            ('Modul 1: Gruppdynamikens grunder', [
                ('Välkommen till UGL', 'video', 15),
                ('FIRO-modellen: Tillhörighet', 'video', 25),
                ('Grupputvecklingens faser', 'video', 22),
                ('Läsning: Will Schutz och FIRO-teorin', 'reading', 18),
                ('Övning: Gruppövning — Tillhörighet', 'exercise', 40),
                ('Reflektion dag 1', 'video', 10),
            ]),
            ('Modul 2: Rollsökning och kontroll', [
                ('FIRO: Kontroll och makt', 'video', 25),
                ('Konflikt och rollfördelning i gruppen', 'video', 22),
                ('Makt och inflytande', 'video', 20),
                ('Övning: Rollsökningsövningar', 'exercise', 45),
                ('Läsning: Konflikter i grupper', 'reading', 15),
                ('Reflektion dag 2', 'video', 10),
            ]),
            ('Modul 3: Öppenhet och tillit', [
                ('FIRO: Öppenhet — den mogna gruppen', 'video', 25),
                ('Feedback: Att ge och ta emot', 'video', 22),
                ('Självkännedom och Johari-fönstret', 'video', 20),
                ('Övning: Feedback-träning i grupp', 'exercise', 45),
                ('Läsning: Psykologisk trygghet', 'reading', 15),
                ('Reflektion dag 3', 'video', 10),
            ]),
            ('Modul 4: Kommunikation och ledarskap', [
                ('Kommunikationsstilar och deras effekt', 'video', 25),
                ('Aktivt lyssnande — fördjupning', 'video', 20),
                ('Ledarstilar och situationsanpassning', 'video', 22),
                ('Övning: Ledarskapsövningar', 'exercise', 45),
                ('Läsning: Ledarskapsforskning i Norden', 'reading', 15),
                ('Reflektion dag 4', 'video', 10),
            ]),
            ('Modul 5: Integration och handlingsplan', [
                ('Att förstå din grupp — sammanfattning av FIRO', 'video', 22),
                ('Din personliga ledarskapsprofil', 'video', 20),
                ('Läsning: Från UGL till vardagen', 'reading', 15),
                ('Övning: Personlig handlingsplan', 'exercise', 40),
                ('Avslutning och nästa steg', 'video', 12),
            ]),
        ],
        # --- IHM: Utvecklande Ledarskap UL ---
        'ihm-utvecklande-ledarskap-ul': [
            ('Modul 1: UL-modellen', [
                ('Introduktion till Utvecklande Ledarskap', 'video', 22),
                ('De tre ledarskapsstilarna: Destruktivt, Konventionellt, Utvecklande', 'video', 28),
                ('Läsning: Försvarshögskolans forskning', 'reading', 18),
                ('Grundstenarna i utvecklande ledarskap', 'video', 25),
                ('Övning: Självskattning — vilken stil har du?', 'exercise', 30),
                ('Modulsammanfattning', 'video', 10),
            ]),
            ('Modul 2: 360-graders feedback (ULL)', [
                ('Förstå din ULL-bedömning', 'video', 25),
                ('Tolka resultaten', 'video', 22),
                ('Vanliga mönster och blinda fläckar', 'video', 20),
                ('Läsning: 360-feedback i praktiken', 'reading', 15),
                ('Övning: Reflektionsjournal', 'exercise', 35),
                ('Modulsammanfattning', 'video', 8),
            ]),
            ('Modul 3: Personlig utvecklingsplan', [
                ('Från insikt till handling', 'video', 22),
                ('Sätt utvecklingsmål', 'video', 20),
                ('Bygga stödsystem', 'video', 18),
                ('Läsning: Handlingsplanering — metodik', 'reading', 15),
                ('Övning: Skriv din personliga utvecklingsplan', 'exercise', 40),
                ('Modulsammanfattning', 'video', 8),
            ]),
            ('Modul 4: Fördjupning och tillämpning', [
                ('Utvecklande ledarskap i vardagen', 'video', 25),
                ('Leda med föredöme', 'video', 22),
                ('Individuell omtanke och inspiration', 'video', 20),
                ('Läsning: UL i svenska organisationer — case', 'reading', 18),
                ('Övning: Tillämpa UL med ditt team', 'exercise', 35),
                ('Kurssammanfattning', 'video', 12),
            ]),
        ],
        # --- Wenell: Ledarskap och Kommunikation ---
        'wenell-ledarskap-kommunikation': [
            ('Modul 1: Kommunikationens grunder', [
                ('Varför kommunikation är din viktigaste kompetens', 'video', 18),
                ('Aktivt lyssnande i praktiken', 'video', 22),
                ('Tydlighet: Säg vad du menar', 'video', 20),
                ('Läsning: Kommunikationsstilar', 'reading', 12),
                ('Övning: Lyssnande-träning', 'exercise', 25),
                ('Modulsammanfattning', 'video', 8),
            ]),
            ('Modul 2: Ledarens vardagskommunikation', [
                ('Effektiva möten — planering till uppföljning', 'video', 22),
                ('Ge tydliga instruktioner utan att detaljstyra', 'video', 20),
                ('Rollspel: Kommunikationsövningar', 'exercise', 30),
                ('Läsning: Möteskultur i Sverige', 'reading', 12),
                ('Övning: Mötesdesign-workshop', 'exercise', 25),
                ('Modulsammanfattning', 'video', 8),
            ]),
            ('Modul 3: Feedback och svåra budskap', [
                ('Konsten att ge konstruktiv feedback', 'video', 22),
                ('Att ta emot feedback med öppenhet', 'video', 18),
                ('Svåra samtal — förberedelse och struktur', 'video', 20),
                ('Läsning: SBI- och COIN-modellerna', 'reading', 12),
                ('Övning: Feedback-scenarier', 'exercise', 28),
            ]),
            ('Modul 4: Ledarskap och integration', [
                ('Integrerat ledarskap och kommunikation', 'video', 22),
                ('Gruppdynamik och kommunikation', 'video', 20),
                ('Läsning: Gruppövningar i praktiken', 'reading', 12),
                ('Övning: Din kommunikationsplan', 'exercise', 30),
                ('Kurssammanfattning', 'video', 10),
            ]),
        ],
        # --- Wenell: Leda genom andra chefer ---
        'wenell-leda-genom-andra': [
            ('Modul 1: Ledarskap på nästa nivå', [
                ('Från chef till chef för chefer', 'video', 20),
                ('Utmaningar med att leda genom ett extra lager', 'video', 22),
                ('Läsning: Multilevel leadership — forskning', 'reading', 15),
                ('Övning: Din ledarskapsutmaning', 'exercise', 22),
                ('Modulsammanfattning', 'video', 8),
            ]),
            ('Modul 2: Bygga ledarskapskultur', [
                ('Skapa riktning och alignment', 'video', 22),
                ('Stärka mellanchefer', 'video', 20),
                ('Delegera ansvar nedåt', 'video', 18),
                ('Övning: Ledarskapskultur-workshop', 'exercise', 28),
                ('Modulsammanfattning', 'video', 8),
            ]),
            ('Modul 3: Strategisk överblick', [
                ('Strategiskt tänkande som senior ledare', 'video', 22),
                ('Kommunicera vision genom organisationen', 'video', 18),
                ('Läsning: Case — svenska organisationer', 'reading', 12),
                ('Övning: Din strategi för att leda genom andra', 'exercise', 28),
                ('Kurssammanfattning', 'video', 10),
            ]),
        ],
        # --- Företagsuniversitetet: Konflikthantering och svåra samtal ---
        'fu-konflikthantering-svara-samtal': [
            ('Modul 1: Konfliktens dynamik', [
                ('Konflikter på arbetsplatsen — varför de uppstår', 'video', 20),
                ('Konfliktfaser och eskalering', 'video', 22),
                ('Läsning: Konflikthanteringsmodeller', 'reading', 15),
                ('Övning: Identifiera konfliktstilar', 'exercise', 22),
                ('Modulsammanfattning', 'video', 8),
            ]),
            ('Modul 2: Svåra samtal', [
                ('Förberedelse: Samtalsplaneraren', 'video', 22),
                ('Öppna samtalet tryggt', 'video', 20),
                ('Stanna i dialogen under press', 'video', 18),
                ('Övning: Rollspel — svåra samtal', 'exercise', 30),
                ('Modulsammanfattning', 'video', 8),
            ]),
            ('Modul 3: Lösningsstrategier', [
                ('Feedbacktekniker för chefer', 'video', 22),
                ('De-eskalering och medling', 'video', 20),
                ('Läsning: Case-studier — konflikter i Sverige', 'reading', 12),
                ('Övning: Din konflikthanteringsplan', 'exercise', 25),
                ('Kurssammanfattning', 'video', 10),
            ]),
        ],
        # --- Företagsuniversitetet: Kommunikation i ledarskapet ---
        'fu-kommunikation-ledarskapet': [
            ('Modul 1: Ledarskapskommunikation', [
                ('Varför kommunikation avgör ditt ledarskap', 'video', 18),
                ('Tydlighet och transparens', 'video', 22),
                ('Läsning: Kommunikationsteorier', 'reading', 12),
                ('Aktivt lyssnande i praktiken', 'video', 20),
                ('Övning: Kommunikationsscenarier', 'exercise', 22),
            ]),
            ('Modul 2: Möten och presentationer', [
                ('Effektiva möten', 'video', 22),
                ('Presentera med genomslagskraft', 'video', 20),
                ('Skriftlig kommunikation som chef', 'video', 18),
                ('Övning: Mötesdesign', 'exercise', 25),
                ('Modulsammanfattning', 'video', 8),
            ]),
            ('Modul 3: Feedback och dialog', [
                ('Ge och ta emot feedback', 'video', 22),
                ('Svåra budskap — struktur och empati', 'video', 18),
                ('Läsning: Kommunikation i nordiska organisationer', 'reading', 12),
                ('Övning: Feedback-träning', 'exercise', 25),
                ('Kurssammanfattning', 'video', 10),
            ]),
        ],
        # --- Hjärtum: Certifierad ledare ---
        'hjartum-certifierad-ledare': [
            ('Modul 1: Fördjupade ledarskapskompetenser', [
                ('Ledarskap bortom grunderna', 'video', 20),
                ('Strategisk självinsikt', 'video', 22),
                ('Läsning: Certifieringsramverket', 'reading', 15),
                ('Avancerad kommunikationsteknik', 'video', 18),
                ('Övning: Ledarskaps-case', 'exercise', 25),
            ]),
            ('Modul 2: Teamutveckling och förändring', [
                ('Leda genom förändring', 'video', 22),
                ('Bygga högpresterande team', 'video', 20),
                ('Coaching i vardagen', 'video', 18),
                ('Övning: Teamutvecklingsplan', 'exercise', 25),
                ('Modulsammanfattning', 'video', 8),
            ]),
            ('Modul 3: Certifiering och handlingsplan', [
                ('Certifieringskrav och bedömning', 'video', 18),
                ('Din personliga ledarskapsplan', 'video', 20),
                ('Läsning: Nästa steg som certifierad ledare', 'reading', 12),
                ('Övning: Certifieringsuppgift', 'exercise', 30),
                ('Kurssammanfattning', 'video', 10),
            ]),
        ],
        # --- CANEA: Förändringsledning ---
        'canea-forandringsledning': [
            ('Modul 1: Förändringsgrunder', [
                ('Varför förändring misslyckas', 'video', 22),
                ('Psykologin bakom motstånd', 'video', 25),
                ('Läsning: Förändringsmodeller i jämförelse', 'reading', 15),
                ('Övning: Förändringsberedskap-analys', 'exercise', 28),
                ('Modulsammanfattning', 'video', 8),
            ]),
            ('Modul 2: Processverktyg', [
                ('Förändringens faser och milstolpar', 'video', 22),
                ('Kommunikationsstrategier vid förändring', 'video', 20),
                ('Intressenthantering', 'video', 18),
                ('Övning: Förändrings-roadmap', 'exercise', 30),
                ('Modulsammanfattning', 'video', 8),
            ]),
            ('Modul 3: Ledarskapsaspekten', [
                ('Leda människor genom transformation', 'video', 25),
                ('Kultur och förändring', 'video', 22),
                ('Läsning: Svenska förändringscase', 'reading', 15),
                ('Övning: Din förändringsledningsplan', 'exercise', 30),
                ('Kurssammanfattning', 'video', 10),
            ]),
            ('Modul 4: Förankra och mäta', [
                ('Mäta förändringsframgång', 'video', 20),
                ('Förankra förändring i kulturen', 'video', 22),
                ('Kontinuerlig förbättring', 'video', 18),
                ('Övning: Mätplan och uppföljning', 'exercise', 25),
                ('Kurssammanfattning', 'video', 10),
            ]),
        ],
        # --- Chefakademin: Leda utan att vara chef ---
        'chefakademin-leda-utan-chef': [
            ('Modul 1: Självkännedom och ledarskap', [
                ('Ledarskap utan formell roll', 'video', 22),
                ('Självkännedom som grund', 'video', 25),
                ('Läsning: Psykologisk trygghet i team', 'reading', 15),
                ('Gruppdynamik och roller', 'video', 20),
                ('Övning: Självinsiktövning', 'exercise', 28),
                ('Modulsammanfattning', 'video', 8),
            ]),
            ('Modul 2: Kommunikation och coaching', [
                ('Coachande samtal', 'video', 22),
                ('Svåra samtal som informell ledare', 'video', 20),
                ('Feedback utan makt', 'video', 18),
                ('Läsning: Coaching-modeller', 'reading', 12),
                ('Övning: Samtalsträning', 'exercise', 30),
                ('Modulsammanfattning', 'video', 8),
            ]),
            ('Modul 3: Påverkan och mandat', [
                ('Bygga informellt mandat', 'video', 22),
                ('Påverkansstrategier', 'video', 20),
                ('Hantera konflikter utan chefsroll', 'video', 18),
                ('Övning: Påverkansscenarier', 'exercise', 25),
            ]),
            ('Modul 4: Certifiering och handlingsplan', [
                ('Certifieringskrav och process', 'video', 18),
                ('Din personliga utvecklingsplan', 'video', 20),
                ('Läsning: Nästa steg som teamledare', 'reading', 12),
                ('Övning: Certifieringsuppgift', 'exercise', 35),
                ('Programsammanfattning', 'video', 10),
            ]),
        ],
        # --- Företagsuniversitetet: Ledarskap i praktiken ---
        'fu-ledarskap-i-praktiken': [
            ('Modul 1: Vetenskaplig grund', [
                ('Ledarskapsteori och forskning', 'video', 22),
                ('Values Online-bedömning — introduktion', 'video', 20),
                ('Läsning: Forskningsbaserat ledarskap', 'reading', 15),
                ('Självinsikt och personliga värderingar', 'video', 18),
                ('Övning: Values Online-tolkning', 'exercise', 30),
                ('Modulsammanfattning', 'video', 8),
            ]),
            ('Modul 2: 360-graders feedback (IDI)', [
                ('Förstå din IDI-profil', 'video', 25),
                ('Blinda fläckar och utvecklingsområden', 'video', 22),
                ('Läsning: IDI i praktiken', 'reading', 15),
                ('Övning: Reflektionsjournal', 'exercise', 30),
                ('Modulsammanfattning', 'video', 8),
            ]),
            ('Modul 3: Praktiska verktyg', [
                ('Kommunikation och feedback', 'video', 22),
                ('Coaching och medarbetarsamtal', 'video', 20),
                ('Konflikthantering', 'video', 18),
                ('Övning: Ledarskapssituationer', 'exercise', 30),
                ('Modulsammanfattning', 'video', 8),
            ]),
            ('Modul 4: Digital coaching och handlingsplan', [
                ('Digital coaching — ditt stöd efter kursen', 'video', 18),
                ('Personlig handlingsplan', 'video', 20),
                ('Läsning: Hållbar ledarskapsutveckling', 'reading', 12),
                ('Övning: Din ledarskapsplan', 'exercise', 35),
                ('Kurssammanfattning', 'video', 10),
            ]),
        ],
        # --- EFL: Ledarskap i organisationer ---
        'efl-ledarskap-organisationer': [
            ('Modul 1: Ledarskap och strategi', [
                ('Organisationsstrategi för ledare', 'video', 25),
                ('Ledarskap i komplexa organisationer', 'video', 22),
                ('Läsning: Stefan Sveningssons forskning', 'reading', 18),
                ('Strategisk omvärldsanalys', 'video', 20),
                ('Övning: Strategisk kartläggning', 'exercise', 30),
                ('Modulsammanfattning', 'video', 8),
            ]),
            ('Modul 2: Förändringsledarskap', [
                ('Leda förändring i organisationer', 'video', 25),
                ('Motstånd och psykologiska processer', 'video', 22),
                ('Kommunikation vid förändring', 'video', 20),
                ('Övning: Förändringscase', 'exercise', 30),
                ('Modulsammanfattning', 'video', 8),
            ]),
            ('Modul 3: Coaching och gruppdynamik', [
                ('Coachande ledarskap på avancerad nivå', 'video', 22),
                ('Gruppdynamik och teamutveckling', 'video', 25),
                ('Läsning: Grupprocesser — forskning', 'reading', 15),
                ('Övning: Coaching-träning', 'exercise', 35),
                ('Modulsammanfattning', 'video', 8),
            ]),
            ('Modul 4: Integration och personlig utveckling', [
                ('Integrerat ledarskap', 'video', 22),
                ('Din ledarskapsprofil', 'video', 20),
                ('Personlig handlingsplan', 'video', 18),
                ('Övning: Slutuppgift och presentation', 'exercise', 35),
                ('Programsammanfattning', 'video', 12),
            ]),
        ],
        # --- EFL: Leading Change ---
        'efl-leading-change': [
            ('Modul 1: Förändringspsykologi', [
                ('Varför människor motstår förändring', 'video', 25),
                ('Förändringsprocessens faser', 'video', 22),
                ('Läsning: Kotter, Lewin och moderna modeller', 'reading', 18),
                ('Ledarens roll i förändring', 'video', 22),
                ('Övning: Analys av egen förändringssituation', 'exercise', 30),
                ('Modulsammanfattning', 'video', 8),
            ]),
            ('Modul 2: Motståndshantering', [
                ('Identifiera och hantera motstånd', 'video', 25),
                ('Kommunikationsstrategier för förändring', 'video', 22),
                ('Organisatoriskt lärande', 'video', 20),
                ('Övning: Motståndsstrategier', 'exercise', 30),
                ('Läsning: Nordiska förändringscase', 'reading', 15),
                ('Modulsammanfattning', 'video', 8),
            ]),
            ('Modul 3: Ledarens verktygslåda', [
                ('Skapa förändringsvision', 'video', 22),
                ('Bygga koalitioner och allianser', 'video', 25),
                ('Mellanchefers roll i förändring', 'video', 20),
                ('Kulturförändring och värderingar', 'video', 22),
                ('Övning: Förändringsplan — slutprojekt', 'exercise', 40),
                ('Övning: Internat 3 — integration', 'exercise', 35),
                ('Kurssammanfattning', 'video', 12),
                ('Avslutning och certifiering', 'video', 10),
            ]),
        ],
        # --- Berghs: AI för förändringsledare ---
        'berghs-ai-forandringsledare': [
            ('Modul 1: AI för erfarna ledare', [
                ('AI-landskapet 2025–2026', 'video', 22),
                ('Avancerad prompting och AI-verktyg', 'video', 25),
                ('Läsning: AI i organisationsförändring', 'reading', 15),
                ('Övning: AI-verktygsanalys', 'exercise', 28),
                ('Modulsammanfattning', 'video', 8),
            ]),
            ('Modul 2: AI-driven transformation', [
                ('Leda AI-transformationsinitiativ', 'video', 25),
                ('Förändringspsykologi vid AI-införande', 'video', 22),
                ('Riskhantering och etik', 'video', 20),
                ('Övning: AI-transformationsplan', 'exercise', 30),
                ('Modulsammanfattning', 'video', 8),
            ]),
            ('Modul 3: Implementering och kultur', [
                ('Bygga AI-kompetens i organisationen', 'video', 22),
                ('AI-governance och policies', 'video', 20),
                ('Läsning: AI i svenska storföretag', 'reading', 15),
                ('Övning: Din AI-förändringsplan', 'exercise', 30),
                ('Kurssammanfattning', 'video', 10),
            ]),
            ('Modul 4: Framtidsstrategi', [
                ('AI-trender och framtidens arbetsplats', 'video', 22),
                ('Skala AI-initiativ', 'video', 20),
                ('Hållbar AI-strategi', 'video', 18),
                ('Övning: Slutprojekt och presentation', 'exercise', 35),
                ('Programsammanfattning', 'video', 10),
            ]),
        ],
        # --- SSE: Chef och ledare ---
        'sse-chef-och-ledare': [
            ('Modul 1: Affärsutveckling och styrning', [
                ('Affärsdriven ledarskap', 'video', 25),
                ('Finansiell styrning för chefer', 'video', 22),
                ('Läsning: SSE-forskning om ledarskap och resultat', 'reading', 18),
                ('Strategisk affärsplanering', 'video', 20),
                ('Övning: Affärsplan-workshop', 'exercise', 35),
            ]),
            ('Modul 2: Ledarskap och kommunikation', [
                ('Personligt ledarskap på executive-nivå', 'video', 25),
                ('Kommunikation med styrelse och ägare', 'video', 22),
                ('Förhandling och inflytande', 'video', 20),
                ('Läsning: Executive communication — forskning', 'reading', 15),
                ('Övning: Styrelse-presentation', 'exercise', 30),
            ]),
            ('Modul 3: Organisation och kultur', [
                ('Organisationsdesign för tillväxt', 'video', 25),
                ('Kulturbygge och värdegrundsledarskap', 'video', 22),
                ('Talangstrategi och succession', 'video', 20),
                ('Läsning: Organisationskultur i svenska storföretag', 'reading', 15),
                ('Övning: Kultur-roadmap', 'exercise', 28),
            ]),
            ('Modul 4: Personlig utveckling', [
                ('Executive presence och autenticitet', 'video', 22),
                ('Hälsa och hållbarhet som ledare', 'video', 20),
                ('Din ledarskapsvision', 'video', 18),
                ('Läsning: Hållbart ledarskap — forskning', 'reading', 15),
                ('Övning: Personlig utvecklingsplan — executive', 'exercise', 35),
                ('Programsammanfattning', 'video', 12),
            ]),
        ],
        # --- SSE: Executive Leadership Program ---
        'sse-executive-leadership-program': [
            ('Modul 1: Personligt ledarskap', [
                ('Ditt ledarskap på executive-nivå', 'video', 25),
                ('Självinsikt och personlig effektivitet', 'video', 22),
                ('Läsning: Executive leadership — forskning', 'reading', 18),
                ('Övning: Personlig ledarskapsprofil', 'exercise', 30),
                ('Reflektion och coaching', 'video', 15),
            ]),
            ('Modul 2: Konkurrensfördelar och innovation', [
                ('Strategisk positionering', 'video', 25),
                ('Innovation som konkurrensfördel', 'video', 22),
                ('Disruptiv innovation', 'video', 20),
                ('Läsning: Innovationsstrategier — case', 'reading', 15),
                ('Övning: Innovationsstrategi-workshop', 'exercise', 35),
                ('Modulsammanfattning', 'video', 10),
            ]),
            ('Modul 3: Finansiell styrning', [
                ('Finansiell analys för seniora ledare', 'video', 25),
                ('Värdeskapande och investeringsbeslut', 'video', 22),
                ('Budgetering och prognoser', 'video', 20),
                ('Övning: Finansiell case-analys', 'exercise', 35),
                ('Modulsammanfattning', 'video', 10),
            ]),
            ('Modul 4: Organisationsförändring', [
                ('Organisationsdesign och transformation', 'video', 25),
                ('Kulturförändring på enterprise-nivå', 'video', 22),
                ('Talent management och succession', 'video', 20),
                ('Läsning: Stora svenska transformationer', 'reading', 18),
                ('Övning: Transformationsplan', 'exercise', 35),
                ('Modulsammanfattning', 'video', 10),
            ]),
            ('Modul 5: Framtidsstrategi', [
                ('Geopolitik och makrotrender', 'video', 22),
                ('Digitalisering och AI-strategi', 'video', 25),
                ('Hållbarhet som strategisk drivkraft', 'video', 20),
                ('Övning: Framtidsscenario-workshop', 'exercise', 35),
                ('Modulsammanfattning', 'video', 10),
            ]),
            ('Modul 6: Integration och slutprojekt', [
                ('Integrerat ledarskap', 'video', 22),
                ('Slutprojekt: Strategisk handlingsplan', 'exercise', 45),
                ('Presentation och peer feedback', 'exercise', 30),
                ('Läsning: Livslångt lärande som executive', 'reading', 15),
                ('Programsammanfattning och alumninätverk', 'video', 15),
                ('Avslutning och certifiering', 'video', 10),
            ]),
        ],
        # --- KTH: Executive Program in Industrial Management ---
        'kth-executive-industrial-management': [
            ('Modul 1: Digital disruption och AI', [
                ('Digitala trender i industrin', 'video', 25),
                ('AI-implementering i teknikföretag', 'video', 22),
                ('Läsning: Case — ABB, Scania, Volvo Cars', 'reading', 18),
                ('Industri 4.0 och smart manufacturing', 'video', 20),
                ('Övning: Digital mognadsanalys', 'exercise', 30),
                ('Modulsammanfattning', 'video', 10),
            ]),
            ('Modul 2: Affärsstrategi', [
                ('Strategiskt ledarskap i teknikdrivna företag', 'video', 25),
                ('Affärsmodellsinnovation', 'video', 22),
                ('Globala marknader och konkurrensanalys', 'video', 20),
                ('Övning: Strategisk affärsplan', 'exercise', 35),
                ('Modulsammanfattning', 'video', 10),
            ]),
            ('Modul 3: Innovation och förändring', [
                ('Innovationsprocesser och ledning', 'video', 22),
                ('Förändringsledarskap i storföretag', 'video', 25),
                ('Hållbar innovation', 'video', 20),
                ('Läsning: Svenska industriföretags transformationer', 'reading', 15),
                ('Övning: Innovationscase', 'exercise', 30),
                ('Modulsammanfattning', 'video', 10),
            ]),
            ('Modul 4: Ledarskap och slutprojekt', [
                ('Executive ledarskap i industrin', 'video', 22),
                ('Personlig ledarskapsutveckling', 'video', 20),
                ('Slutprojekt: Transformationsplan', 'exercise', 45),
                ('Presentation och peer review', 'exercise', 30),
                ('Programsammanfattning och certifiering', 'video', 12),
            ]),
        ],
    }

    total_modules = 0
    total_lessons = 0
    for course_slug, modules in curriculum.items():
        course_id = course_map.get(course_slug)
        if not course_id:
            continue
        for i, (mod_title, lessons_list) in enumerate(modules):
            mod = db.insert('modules', {'course_id': course_id, 'title': mod_title, 'sort_order': i + 1})
            lesson_inserts = [
                {'module_id': mod['id'], 'title': t, 'type': typ, 'duration_minutes': dur, 'sort_order': j + 1}
                for j, (t, typ, dur) in enumerate(lessons_list)
            ]
            db.insert('lessons', lesson_inserts)
            total_modules += 1
            total_lessons += len(lessons_list)
    print(f'  {total_modules} modules, {total_lessons} lessons created')

    # ============================================================
    # ENROLLMENTS
    # ============================================================
    print('Seeding enrollments...')
    published_ids = [cid for slug, cid in course_map.items()
                     if any(c[14] == 'published' and c[3] == slug for c in courses_data)]
    all_learner_ids = list(learner_map.values())

    enrollment_inserts = []
    for cid in published_ids:
        for lid in all_learner_ids:
            if random.random() < 0.6:
                enrollment_inserts.append({
                    'user_id': lid, 'course_id': cid,
                    'enrolled_at': (now - timedelta(days=random.randint(1, 180))).isoformat()
                })

    if enrollment_inserts:
        db.insert('enrollments', enrollment_inserts)
    print(f'  {len(enrollment_inserts)} enrollments created')

    # ============================================================
    # REVIEWS
    # ============================================================
    print('Seeding reviews...')
    review_texts_5 = [
        'Absolutely transformative. The frameworks are immediately applicable.',
        'Best leadership course I\'ve ever taken. Worth every penny.',
        'Incredible content. The instructor\'s experience really shines through.',
        'This course completely changed how I approach leadership challenges.',
        'Exceptional quality. The case studies are incredibly relevant.',
    ]
    review_texts_4 = [
        'Very comprehensive course. Excellent content but could use more Q&A.',
        'Great material, well-structured. Would love more live sessions.',
        'Solid course with actionable frameworks. Minor pacing issues.',
    ]

    # Specific reviews matching wireframes
    specific_reviews = [
        {'user_id': learner_map['Amanda Whitfield'], 'course_id': course_map['strategic-leadership-masterclass'], 'rating': 5,
         'comment': 'Absolutely transformative. The frameworks taught here are immediately applicable. I\'ve already started implementing the stakeholder mapping exercise with my team and seeing results.',
         'helpful_count': 12, 'created_at': (now - timedelta(days=14)).isoformat()},
        {'user_id': learner_map['Robert Chen'], 'course_id': course_map['strategic-leadership-masterclass'], 'rating': 5,
         'comment': 'Dr. Mitchell\'s experience really shines through. The case studies are incredibly relevant and the peer discussions added so much value. Worth every penny.',
         'helpful_count': 8, 'created_at': (now - timedelta(days=30)).isoformat()},
        {'user_id': learner_map['Patricia Okafor'], 'course_id': course_map['strategic-leadership-masterclass'], 'rating': 4,
         'comment': 'Very comprehensive course. The content is excellent but I wish there were more live Q&A sessions. The materials and exercises are top-notch though.',
         'helpful_count': 5, 'created_at': (now - timedelta(days=60)).isoformat()},
        {'user_id': learner_map['David Park'], 'course_id': course_map['strategic-leadership-masterclass'], 'rating': 5,
         'comment': 'Dr. Mitchell is hands down the best leadership instructor I\'ve encountered. Her real-world experience makes every concept relatable and actionable.',
         'helpful_count': 10, 'created_at': (now - timedelta(days=20)).isoformat()},
        {'user_id': learner_map['Lisa Martinez'], 'course_id': course_map['strategic-leadership-masterclass'], 'rating': 5,
         'comment': 'I\'ve taken 4 of her courses and each one builds on the last beautifully. Her teaching style is engaging, structured, and incredibly professional.',
         'helpful_count': 7, 'created_at': (now - timedelta(days=45)).isoformat()},
    ]
    db.insert('reviews', specific_reviews)

    # Additional reviews
    additional_reviews = []
    used_pairs = {(r['user_id'], r['course_id']) for r in specific_reviews}
    for cid in published_ids:
        for lid in all_learner_ids:
            if (lid, cid) in used_pairs:
                continue
            if random.random() < 0.3:
                rating = random.choices([5, 4, 3, 2, 1], weights=[60, 25, 10, 3, 2])[0]
                comment = random.choice(review_texts_5) if rating == 5 else random.choice(review_texts_4) if rating == 4 else 'Decent course with some good takeaways.'
                additional_reviews.append({
                    'user_id': lid, 'course_id': cid, 'rating': rating,
                    'comment': comment, 'helpful_count': random.randint(0, 12),
                    'created_at': (now - timedelta(days=random.randint(1, 120))).isoformat()
                })
                used_pairs.add((lid, cid))

    if additional_reviews:
        db.insert('reviews', additional_reviews)
    print(f'  {len(specific_reviews) + len(additional_reviews)} reviews created')

    # ============================================================
    # ORDERS
    # ============================================================
    print('Seeding orders...')
    order_inserts = []
    for cid in published_ids:
        price = next((c[5] for c in courses_data if course_map.get(c[3]) == cid), 200)
        for lid in all_learner_ids:
            # Check if enrolled
            enrolled = any(e['user_id'] == lid and e['course_id'] == cid for e in enrollment_inserts)
            if enrolled and random.random() < 0.8:
                order_inserts.append({
                    'user_id': lid, 'course_id': cid, 'amount': price,
                    'payment_status': 'completed', 'payment_method': 'credit_card',
                    'created_at': (now - timedelta(days=random.randint(1, 180))).isoformat()
                })

    if order_inserts:
        db.insert('orders', order_inserts)
    print(f'  {len(order_inserts)} orders created')

    # ============================================================
    # COUPONS
    # ============================================================
    print('Seeding coupons...')
    coupons = [
        {'code': 'LEAD30', 'discount_type': 'fixed', 'discount_value': 30, 'max_uses': 1000, 'expires_at': (now + timedelta(days=30)).isoformat(), 'is_active': True},
        {'code': 'SAVE20', 'discount_type': 'percent', 'discount_value': 20, 'max_uses': 500, 'expires_at': (now + timedelta(days=60)).isoformat(), 'is_active': True},
        {'code': 'FIRST50', 'discount_type': 'fixed', 'discount_value': 50, 'max_uses': 100, 'expires_at': (now + timedelta(days=14)).isoformat(), 'is_active': True},
        {'code': 'WELCOME10', 'discount_type': 'percent', 'discount_value': 10, 'max_uses': None, 'expires_at': None, 'is_active': True},
    ]
    db.insert('coupons', coupons)
    print(f'  {len(coupons)} coupons created')

    print('\nDatabase seeded successfully!')
    print(f'\nCatalog: {len(categories)} categories, {len(instructors)} instructors, {len(courses_data)} courses')
    print(f'Curriculum: {total_modules} modules, {total_lessons} lessons')
    print('\nTest accounts:')
    print('  Instructor: sarah.mitchell@leadershippro.com / password123')
    print('  Learner:    amanda.whitfield@mercer.com / password123')
    print('  Admin:      admin@leadershippro.com / password123')


if __name__ == '__main__':
    seed()
