"""
Generate sitemap.xml from Supabase and write it to ./sitemap.xml.

Includes:
  - homepage, /courses, /for-instructors
  - one URL per published course at /courses/<slug>
  - one URL per category landing at /courses?category=<slug>
  - one URL per instructor with at least one published course at /instructors/<id>

Re-run this any time new courses or instructors get published, then scp the
output to the server (see README "Deploy").
"""
import os
import psycopg2

SITE = 'https://upskillcompass.com'


def load_db_url():
    for line in open('.env'):
        if line.startswith('DATABASE_URL='):
            return line.split('=', 1)[1].strip()
    raise SystemExit('DATABASE_URL not in .env')


def main():
    conn = psycopg2.connect(load_db_url())
    cur = conn.cursor()

    cur.execute("""
        SELECT slug, GREATEST(updated_at, created_at)::date AS lastmod
          FROM courses
         WHERE status = 'published' AND slug IS NOT NULL
         ORDER BY id
    """)
    courses = cur.fetchall()

    cur.execute("SELECT slug FROM categories ORDER BY id")
    categories = cur.fetchall()

    cur.execute("""
        SELECT DISTINCT u.id
          FROM users u
          JOIN courses c ON c.instructor_id = u.id
         WHERE u.role = 'instructor' AND c.status = 'published'
         ORDER BY u.id
    """)
    instructors = cur.fetchall()

    cur.close()
    conn.close()

    out = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        f'  <url><loc>{SITE}/</loc><changefreq>daily</changefreq><priority>1.0</priority></url>',
        f'  <url><loc>{SITE}/courses</loc><changefreq>daily</changefreq><priority>0.9</priority></url>',
        f'  <url><loc>{SITE}/for-instructors</loc><changefreq>monthly</changefreq><priority>0.5</priority></url>',
    ]
    for (slug,) in categories:
        out.append(
            f'  <url><loc>{SITE}/courses?category={slug}</loc>'
            '<changefreq>weekly</changefreq><priority>0.7</priority></url>'
        )
    for (slug, lastmod) in courses:
        out.append(
            f'  <url><loc>{SITE}/courses/{slug}</loc>'
            f'<lastmod>{lastmod.isoformat()}</lastmod>'
            '<changefreq>weekly</changefreq><priority>0.7</priority></url>'
        )
    for (uid,) in instructors:
        out.append(
            f'  <url><loc>{SITE}/instructors/{uid}</loc>'
            '<changefreq>monthly</changefreq><priority>0.5</priority></url>'
        )
    out.append('</urlset>')

    with open('sitemap.xml', 'w') as f:
        f.write('\n'.join(out) + '\n')

    print(
        f'Wrote sitemap.xml: {len(courses)} courses, '
        f'{len(categories)} categories, {len(instructors)} instructors '
        f'({sum(1 for _ in out)} total lines)'
    )


if __name__ == '__main__':
    main()
