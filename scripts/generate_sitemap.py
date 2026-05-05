"""
Generate sitemap.xml from Supabase and write it to ./sitemap.xml.

Each <url> entry includes <xhtml:link rel="alternate" hreflang="..."/>
entries for the four supported languages (en at /, then /sv, /de, /fr)
plus an x-default pointing at the en version. This is the URL-set form
of hreflang and is the recommended way to declare alternates to Google.

Re-run any time new courses or instructors get published, then scp the
output to the server (see README "Deploy").
"""
import psycopg2

SITE = 'https://upskillcompass.com'
LANGS = ['en', 'sv', 'de', 'fr']


def lang_prefix(code):
    return '' if code == 'en' else f'/{code}'


def lang_url(code, base_path):
    """SITE-rooted URL in the given lang. base_path has no lang prefix."""
    prefix = lang_prefix(code)
    if base_path == '/' or base_path == '':
        return SITE + (prefix or '/')
    return SITE + prefix + base_path


def url_block(base_path, *, lastmod=None, changefreq='weekly', priority='0.7'):
    parts = ['  <url>']
    parts.append(f'    <loc>{lang_url("en", base_path)}</loc>')
    if lastmod:
        parts.append(f'    <lastmod>{lastmod}</lastmod>')
    parts.append(f'    <changefreq>{changefreq}</changefreq>')
    parts.append(f'    <priority>{priority}</priority>')
    for code in LANGS:
        parts.append(
            f'    <xhtml:link rel="alternate" hreflang="{code}" '
            f'href="{lang_url(code, base_path)}"/>'
        )
    parts.append(
        f'    <xhtml:link rel="alternate" hreflang="x-default" '
        f'href="{lang_url("en", base_path)}"/>'
    )
    parts.append('  </url>')
    return parts


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
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml">',
    ]
    out += url_block('/',                changefreq='daily',   priority='1.0')
    out += url_block('/courses',         changefreq='daily',   priority='0.9')
    out += url_block('/for-instructors', changefreq='monthly', priority='0.5')
    for (slug,) in categories:
        out += url_block(f'/courses?category={slug}', changefreq='weekly', priority='0.7')
    for (slug, lastmod) in courses:
        out += url_block(f'/courses/{slug}', lastmod=lastmod.isoformat(), changefreq='weekly', priority='0.7')
    for (uid,) in instructors:
        out += url_block(f'/instructors/{uid}', changefreq='monthly', priority='0.5')
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
