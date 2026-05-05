-- =====================================================================
-- UpskillCompass — Seed v4: Negotiation, board governance, executive
-- finance, and storytelling — leadership-adjacent and economy-of-leadership
-- programs from public provider pages. All durations 1-20 days, all
-- well above the >$50/day threshold.
--
-- No new categories — these slot into existing Communication,
-- Executive Leadership, and Strategic Thinking categories.
--
-- Idempotent: ON CONFLICT DO NOTHING on email/slug. Safe to re-run.
-- =====================================================================

BEGIN;

-- ---------------------------------------------------------------------
-- 1. New ghost instructor users (INSEAD reuses faculty@insead.edu)
-- ---------------------------------------------------------------------
INSERT INTO users (email, first_name, last_name, role, company, title, bio, created_at, updated_at)
VALUES
  ('info@pon.harvard.edu', 'Harvard PON', 'Faculty', 'instructor',
    'Program on Negotiation at Harvard Law School',
    'PON Faculty (HLS / HBS / HKS)',
    'The Program on Negotiation (PON) is a consortium of negotiation faculty across Harvard Law School, Harvard Business School, and Harvard Kennedy School. Its open-enrollment programs have trained leaders, diplomats, and commercial negotiators since 1983.',
    now(), now()),

  ('info@karrass.com', 'KARRASS', 'Senior Trainers', 'instructor',
    'KARRASS',
    'Effective Negotiating® Master Facilitators',
    'KARRASS, founded by Chester L. Karrass, has trained over a million professionals in its Effective Negotiating® methodology since 1968. Programs run year-round in 50+ U.S. and international cities.',
    now(), now()),

  ('training@duarte.com', 'Duarte', 'Master Facilitators', 'instructor',
    'Duarte, Inc.',
    'Communication & Storytelling Coaches',
    'Duarte built its reputation designing presentations for Al Gore (An Inconvenient Truth), Apple, and the World Bank. Its public workshops codify the same persuasive-storytelling and slide-design methodology into 2-day open-enrollment programs.',
    now(), now()),

  ('info@nacdonline.org', 'NACD', 'Faculty', 'instructor',
    'National Association of Corporate Directors',
    'NACD Faculty & Subject-Matter Experts',
    'The National Association of Corporate Directors is the largest member organization for corporate-board directors in the U.S. NACD.DC is the premier U.S. board credential, and Director Professionalism is its required foundation course on board oversight, strategy, risk, and governance.',
    now(), now()),

  ('execed@wharton.upenn.edu', 'Wharton', 'Executive Education', 'instructor',
    'Wharton School, University of Pennsylvania',
    'Wharton Executive Education Faculty',
    'Wharton Executive Education runs open-enrollment programs at the Steinberg Conference Center in Philadelphia and on its San Francisco campus. Its finance and leadership programs draw on Wharton''s rank as a top-tier U.S. business school.',
    now(), now())
ON CONFLICT (email) DO NOTHING;


-- ---------------------------------------------------------------------
-- 2. New courses
-- ---------------------------------------------------------------------
INSERT INTO courses
  (instructor_id, category_id, title, slug, description, short_description,
   price, currency, level, format, duration_hours,
   status, is_featured, is_bestseller,
   source_url, source_domain, claim_email,
   created_at, updated_at)
SELECT u.id, c.id,
       t.title, t.slug, t.description, t.short_description,
       t.price, t.currency, t.level, t.format, t.duration_hours,
       'published', t.is_featured, t.is_bestseller,
       t.source_url, t.source_domain, t.claim_email,
       now(), now()
FROM (VALUES

  -- ── Communication: negotiation + persuasive storytelling ────
  ('info@pon.harvard.edu', 'communication',
    'Negotiation and Leadership (Harvard PON)',
    'harvard-pon-negotiation-and-leadership',
    'Harvard PON''s flagship 3-day open-enrollment program on negotiation and leadership. Faculty drawn from Harvard Law School, Harvard Business School, and Harvard Kennedy School. Group-of-2+ discount of $500 per registrant available.',
    'Harvard PON 3-day program with HLS / HBS / HKS faculty.',
    5497.00, 'USD', 'advanced', 'live', 24,
    true, true,
    'https://www.pon.harvard.edu/executive-education/', 'pon.harvard.edu', 'info@pon.harvard.edu'),

  ('info@karrass.com', 'communication',
    'Effective Negotiating® Seminar (KARRASS)',
    'karrass-effective-negotiating',
    '2-day in-person seminar on the Effective Negotiating® methodology. Runs in 50+ cities across the U.S., Canada, Mexico, and Europe; includes the Effective Negotiating Workbook, KARRASS Audio Series, and two books. Group discounts available ($1,374 for 2+ registrants, $1,311 for 5+).',
    '2-day KARRASS Effective Negotiating® seminar in 50+ cities worldwide.',
    1489.00, 'USD', 'intermediate', 'live', 16,
    false, true,
    'https://www.karrass.com/', 'karrass.com', 'info@karrass.com'),

  ('training@duarte.com', 'communication',
    'Persuasive Storytelling Workshop (Duarte)',
    'duarte-persuasive-storytelling-workshop',
    '2-day live workshop on Duarte''s persuasive-storytelling methodology, derived from 35+ years of designing presentations for executives, Al Gore (An Inconvenient Truth), and Fortune 500s. Available virtually or at Duarte HQ. Pricing approximate per Duarte''s public workshop catalog; contact provider for current rates and seasonal promotions.',
    'Duarte 2-day workshop on persuasive storytelling and slide design.',
    2495.00, 'USD', 'advanced', 'live', 16,
    false, false,
    'https://www.duarte.com/training/', 'duarte.com', 'training@duarte.com'),

  -- ── Executive Leadership: board governance ──────────────────
  ('info@nacdonline.org', 'executive-leadership',
    'NACD Director Professionalism Course',
    'nacd-director-professionalism',
    'NACD''s required foundation course for the NACD.DC credential — the premier U.S. board credential. 10 integrated on-demand modules covering strategy, risk, audit, culture, ethics, human capital, and stakeholder oversight. 180 days of access; equivalent to roughly 4 days of focused study. Membership pricing: $3,000 NACD individual / $1,500 NACD corporate / $3,995 nonmember.',
    'NACD foundation course for the NACD.DC board credential. 10 modules, 180-day access.',
    3995.00, 'USD', 'executive', 'self-paced', 30,
    true, false,
    'https://www.nacdonline.org/nacd-events/national-events/elearning-courses/on-demand/director-professionalism/', 'nacdonline.org', 'info@nacdonline.org'),

  ('faculty@insead.edu', 'executive-leadership',
    'Aspiring Directors Programme (INSEAD)',
    'insead-aspiring-directors-programme',
    'INSEAD''s 5-day program at the Fontainebleau campus for high-potential professionals preparing for their first board mandate. Covers board effectiveness, oversight, decision-making, and director responsibilities. Multiple 2026 intakes (Jan, Apr, Jun); leads toward the INSEAD Certificate in Corporate Governance.',
    'INSEAD 5-day program for first-time board directors. €11,800.',
    11800.00, 'EUR', 'advanced', 'live', 40,
    false, false,
    'https://www.insead.edu/executive-education/corporate-governance/aspiring-directors-programme/dates-fees', 'insead.edu', 'info@insead.edu'),

  -- ── Strategic Thinking: finance for non-finance leaders ─────
  ('execed@wharton.upenn.edu', 'strategic-thinking',
    'Finance and Accounting for the Non-Financial Manager (Wharton)',
    'wharton-finance-accounting-non-financial-manager',
    'Wharton Executive Education''s 5-day flagship program for functional managers without formal finance training. Covers reading financial statements, capital budgeting, valuation, and financial decision-making. 2026 cohort: April 27 - May 1, in-person at the Steinberg Conference Center, Philadelphia.',
    'Wharton 5-day finance program for non-finance managers. $12,875.',
    12875.00, 'USD', 'executive', 'live', 40,
    true, false,
    'https://executiveeducation.wharton.upenn.edu/for-individuals/all-programs/finance-and-accounting-for-the-non-financial-manager/', 'wharton.upenn.edu', 'execed@wharton.upenn.edu')

) AS t(inst_email, cat_slug,
       title, slug, description, short_description,
       price, currency, level, format, duration_hours,
       is_featured, is_bestseller,
       source_url, source_domain, claim_email)
JOIN users u      ON u.email = t.inst_email
JOIN categories c ON c.slug  = t.cat_slug
ON CONFLICT (slug) DO NOTHING;

COMMIT;
