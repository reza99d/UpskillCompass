-- =====================================================================
-- UpskillCompass — Seed v3: European exec ed + HR + SAFe + Cloud/Data
--
-- Adds 1 new category (Human Resources), 6 new ghost instructors,
-- and 12 courses spanning HEC Paris, Scaled Agile (SAFe), Microsoft,
-- AWS DevOps, Tableau, SHRM and ICAgile. All durations 1-20 days,
-- all >$50/day equivalent.
--
-- Idempotent: ON CONFLICT DO NOTHING on email/slug, safe to re-run.
-- =====================================================================

BEGIN;

-- ---------------------------------------------------------------------
-- 1. New category
-- ---------------------------------------------------------------------
INSERT INTO categories (name, slug, icon, description) VALUES
  ('Human Resources', 'human-resources', '👥',
   'SHRM, HRCI, and CIPD credentials for HR practitioners and people leaders.')
ON CONFLICT (slug) DO NOTHING;


-- ---------------------------------------------------------------------
-- 2. New ghost instructor users (reuses aws-training@amazon.com)
-- ---------------------------------------------------------------------
INSERT INTO users (email, first_name, last_name, role, company, title, bio, created_at, updated_at)
VALUES
  ('info@hec.edu', 'HEC Paris', 'Executive Education', 'instructor',
    'HEC Paris',
    'Executive Education Faculty',
    'HEC Paris is consistently ranked among the top European business schools and runs a portfolio of executive short programs (1-5 days) for senior managers, taught in French and English at the Jouy-en-Josas campus.',
    now(), now()),

  ('training@scaledagile.com', 'Scaled Agile', 'SPC Trainers', 'instructor',
    'Scaled Agile, Inc.',
    'SAFe Program Consultants (SPCs)',
    'Scaled Agile, Inc. is the body behind the Scaled Agile Framework (SAFe). SPC-certified trainers deliver Leading SAFe and the role-specific SAFe credentials worldwide. SAFe credentials are valid for one year and renewed via the SAFe Community Platform ($295/yr).',
    now(), now()),

  ('info@shrm.org', 'SHRM', 'Faculty', 'instructor',
    'Society for Human Resource Management',
    'SHRM-Certified HR Faculty',
    'SHRM is the largest HR professional association globally. Its SHRM-CP and SHRM-SCP credentials are the dominant HR certifications in the U.S. and are increasingly recognized internationally.',
    now(), now()),

  ('training@microsoft.com', 'Microsoft', 'Learning Partners', 'instructor',
    'Microsoft Learn',
    'Microsoft Certified Trainers (MCTs)',
    'Microsoft Learn delivers official certifications for Azure, Microsoft 365, Power Platform, Dynamics 365, and security. Boot camps are delivered by Microsoft Certified Trainers at Microsoft Learning Partners.',
    now(), now()),

  ('training@tableau.com', 'Tableau', 'Authorized Trainers', 'instructor',
    'Tableau (Salesforce)',
    'Tableau Authorized Trainers',
    'Tableau is the leading data-visualization platform in enterprise BI. Its Specialist, Certified Data Analyst, and Architect credentials are delivered by authorized trainers worldwide.',
    now(), now()),

  ('info@icagile.com', 'ICAgile', 'Authorized Instructors', 'instructor',
    'International Consortium for Agile (ICAgile)',
    'ICAgile-Authorized Instructors',
    'ICAgile is a vendor-neutral agile certification body whose ICP-ACC (Agile Coaching) and ICP-ATF (Agile Team Facilitation) credentials are widely held by enterprise agile coaches.',
    now(), now())
ON CONFLICT (email) DO NOTHING;


-- ---------------------------------------------------------------------
-- 3. New courses
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

  -- ── Strategic Thinking ──────────────────────────────────────
  ('info@hec.edu', 'strategic-thinking',
    'Leadership Stratégique (HEC Paris)',
    'hec-leadership-strategique',
    'HEC Paris''s 4-day flagship strategic-leadership short program for senior managers. Combines case work, executive coaching, and applied strategy frameworks. Delivered in French at the Jouy-en-Josas campus; English-language equivalents (Strategic Leadership) run on alternating dates.',
    'HEC Paris 4-day strategic-leadership short program. €6,100.',
    6100.00, 'EUR', 'advanced', 'live', 32,
    true, false,
    'https://www.hec.edu/en/executive-education/leadership-strategique', 'hec.edu', 'info@hec.edu'),

  ('info@hec.edu', 'strategic-thinking',
    'Innovation et Leadership (HEC Paris)',
    'hec-innovation-et-leadership',
    'HEC Paris 2-day intensive on leading through innovation and ambiguity. Frameworks for strategic experimentation, fast decision-making under uncertainty, and energising teams through change.',
    'HEC Paris 2-day intensive on leading innovation. €3,100.',
    3100.00, 'EUR', 'advanced', 'live', 16,
    false, false,
    'https://www.hec.edu/en/executive-education/innovation-et-leadership-paris', 'hec.edu', 'info@hec.edu'),

  -- ── Executive Leadership ────────────────────────────────────
  ('info@hec.edu', 'executive-leadership',
    'Leadership for Executives (HEC Paris)',
    'hec-leadership-for-executives',
    'HEC Paris 4-day program for senior executives focused on personal leadership effectiveness, influence under pressure, and leading senior teams. Delivered in English with international cohorts on the Jouy-en-Josas campus.',
    'HEC Paris 4-day senior-executive program. €6,100.',
    6100.00, 'EUR', 'executive', 'live', 32,
    false, false,
    'https://www.hec.edu/en/executive-education/leadership-executives', 'hec.edu', 'info@hec.edu'),

  -- ── Agile & Scrum ───────────────────────────────────────────
  ('training@scaledagile.com', 'agile-scrum',
    'Leading SAFe® — SAFe® Agilist (SA)',
    'safe-leading-safe-agilist',
    '2-day Scaled Agile Framework foundational course. Delivered by an SPC-certified trainer; covers SAFe principles, ARTs, PI Planning, and the role of the SAFe Agilist. First exam attempt included; cert valid 1 year, renewal $295/yr via the SAFe Community Platform.',
    'Scaled Agile 2-day Leading SAFe course with SAFe Agilist exam included.',
    595.00, 'USD', 'intermediate', 'live', 16,
    true, true,
    'https://www.scaledagile.com/training/leading-safe/', 'scaledagile.com', 'training@scaledagile.com'),

  ('training@scaledagile.com', 'agile-scrum',
    'SAFe® Product Owner / Product Manager (POPM)',
    'safe-product-owner-product-manager',
    '2-day SAFe role-specific course for product owners and product managers. Covers ART-aligned product strategy, backlog management, and PI Planning from the PO/PM perspective. Includes the POPM exam attempt; cert valid 1 year.',
    'Scaled Agile 2-day POPM course covering ART-aligned product management.',
    595.00, 'USD', 'intermediate', 'live', 16,
    false, false,
    'https://www.scaledagile.com/training/safe-product-owner-product-manager/', 'scaledagile.com', 'training@scaledagile.com'),

  -- ── IT & Cybersecurity ──────────────────────────────────────
  ('training@microsoft.com', 'it-cybersecurity',
    'Microsoft Azure Solutions Architect Expert (AZ-305) Boot Camp',
    'microsoft-azure-solutions-architect-az-305',
    '5-day instructor-led boot camp aligned to AZ-305 (Designing Microsoft Azure Infrastructure Solutions). Covers identity, governance, data, infrastructure, and business-continuity design. Prerequisite: AZ-104 Azure Administrator Associate. Boot camps include the $165 AZ-305 exam voucher; total exam fees $330 with the prereq.',
    '5-day Azure Solutions Architect (AZ-305) boot camp. Requires AZ-104 prereq.',
    2795.00, 'USD', 'advanced', 'live', 40,
    true, false,
    'https://learn.microsoft.com/en-us/credentials/certifications/azure-solutions-architect/', 'learn.microsoft.com', 'training@microsoft.com'),

  ('aws-training@amazon.com', 'it-cybersecurity',
    'AWS Certified DevOps Engineer — Professional Boot Camp',
    'aws-certified-devops-engineer-professional',
    '5-day intensive boot camp covering CI/CD, configuration management, monitoring, incident response, and security automation in AWS. Prerequisite: AWS Solutions Architect Associate or Developer Associate. Delivered by AWS Authorized Training Partners; the DOP-C02 exam fee is $300.',
    '5-day AWS DevOps Pro boot camp covering CI/CD, monitoring, and security automation.',
    2995.00, 'USD', 'advanced', 'live', 40,
    false, false,
    'https://aws.amazon.com/certification/certified-devops-engineer-professional/', 'aws.amazon.com', 'aws-training@amazon.com'),

  -- ── Innovation & Digital ────────────────────────────────────
  ('training@microsoft.com', 'innovation-digital',
    'Microsoft Power BI Data Analyst (PL-300) Boot Camp',
    'microsoft-power-bi-data-analyst-pl-300',
    '4-day instructor-led boot camp aligned to PL-300. Covers Power BI data modeling, DAX, visualization, and report deployment. Includes the PL-300 exam voucher and labs against real datasets.',
    '4-day Power BI Data Analyst (PL-300) boot camp with exam voucher.',
    2295.00, 'USD', 'intermediate', 'live', 32,
    false, true,
    'https://learn.microsoft.com/en-us/credentials/certifications/data-analyst-associate/', 'learn.microsoft.com', 'training@microsoft.com'),

  ('training@tableau.com', 'innovation-digital',
    'Tableau Desktop Specialist Training',
    'tableau-desktop-specialist-training',
    '3-day instructor-led course preparing for the Tableau Desktop Specialist exam. Covers data connections, visual analytics, dashboards, and storytelling. Suited for analysts moving from Excel/SQL into a BI workflow. Tableau Authorized Trainers deliver this course in 30+ countries.',
    'Tableau Desktop Specialist 3-day course with hands-on dashboard building.',
    1295.00, 'USD', 'beginner', 'live', 24,
    false, false,
    'https://www.tableau.com/learn/certification/desktop-specialist', 'tableau.com', 'training@tableau.com'),

  -- ── Coaching & Mentoring ────────────────────────────────────
  ('info@icagile.com', 'coaching-mentoring',
    'ICAgile Certified Professional — Agile Coaching (ICP-ACC)',
    'icagile-icp-acc',
    '3-day intensive on professional agile coaching. Covers stance and presence, mentoring vs. coaching vs. teaching vs. facilitating, and ethics. Highly regarded prerequisite for the ICAgile Expert in Agile Coaching (ICE-AC) credential.',
    'ICAgile 3-day ICP-ACC course on professional agile coaching.',
    1795.00, 'USD', 'intermediate', 'live', 24,
    false, false,
    'https://www.icagile.com/certifications/agile-coaching/icp-acc-agile-coaching', 'icagile.com', 'info@icagile.com'),

  -- ── Human Resources (new) ───────────────────────────────────
  ('info@shrm.org', 'human-resources',
    'SHRM Certification Prep+ — SHRM-CP',
    'shrm-certification-prep-cp',
    'SHRM''s instructor-led prep program for the SHRM Certified Professional (SHRM-CP) exam. Live cohort over 12 weeks (typically one 3-hour class per week, ~36 contact hours). Includes the SHRM Learning System, practice exams, and faculty support. Targeted at HR practitioners with 1-3 years of experience.',
    'SHRM-CP exam prep, 12-week instructor-led program with the SHRM Learning System.',
    1499.00, 'USD', 'intermediate', 'live', 36,
    true, true,
    'https://www.shrm.org/events-education/education/seminars/shrm-certification-exam-prep/shrm-cp-shrm-scp-certification-prep', 'shrm.org', 'info@shrm.org'),

  ('info@shrm.org', 'human-resources',
    'SHRM Certification Prep+ — SHRM-SCP',
    'shrm-certification-prep-scp',
    'SHRM''s instructor-led prep program for the SHRM Senior Certified Professional (SHRM-SCP) exam. Same 12-week cadence as SHRM-CP Prep, but targeted at senior HR leaders with 4+ years of strategic HR experience. Covers HR strategy, leadership, and analytics.',
    'SHRM-SCP exam prep, 12-week program for senior HR leaders.',
    1499.00, 'USD', 'advanced', 'live', 36,
    false, false,
    'https://www.shrm.org/events-education/education/seminars/shrm-certification-exam-prep/shrm-cp-shrm-scp-certification-prep', 'shrm.org', 'info@shrm.org')

) AS t(inst_email, cat_slug,
       title, slug, description, short_description,
       price, currency, level, format, duration_hours,
       is_featured, is_bestseller,
       source_url, source_domain, claim_email)
JOIN users u      ON u.email = t.inst_email
JOIN categories c ON c.slug  = t.cat_slug
ON CONFLICT (slug) DO NOTHING;

COMMIT;
