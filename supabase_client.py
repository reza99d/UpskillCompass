"""
Supabase REST API client for UpskillCompass.
Thin wrapper around urllib to avoid extra dependencies.
"""

import json
import urllib.request
import urllib.parse
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL', '').rstrip('/')
SUPABASE_KEY = os.getenv('SUPABASE_KEY', '')


def _headers(prefer=None):
    h = {
        'apikey': SUPABASE_KEY,
        'Authorization': f'Bearer {SUPABASE_KEY}',
        'Content-Type': 'application/json',
    }
    if prefer:
        h['Prefer'] = prefer
    return h


def _request(method, path, data=None, headers_extra=None):
    url = f'{SUPABASE_URL}/rest/v1/{path}'
    h = _headers()
    if headers_extra:
        h.update(headers_extra)
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=h, method=method)
    try:
        resp = urllib.request.urlopen(req)
        content = resp.read().decode()
        if content:
            return json.loads(content)
        return None
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        raise Exception(f'Supabase error {e.code}: {error_body}')


# ── SELECT ──────────────────────────────────────────────────────────
def select(table, columns='*', filters=None, order=None, limit=None, offset=None, single=False):
    """
    SELECT from a table.
    filters: list of tuples like ('column', 'eq', 'value') or raw filter strings like 'column=eq.value'
    """
    params = [f'select={columns}']
    if filters:
        for f in filters:
            if isinstance(f, str):
                params.append(f)
            elif len(f) == 3:
                col, op, val = f
                params.append(f'{col}={op}.{val}')
    if order:
        params.append(f'order={order}')
    if limit is not None:
        params.append(f'limit={limit}')
    if offset is not None:
        params.append(f'offset={offset}')

    path = f'{table}?{"&".join(params)}'
    headers_extra = {}
    if single:
        headers_extra['Accept'] = 'application/vnd.pgrst.object+json'
    result = _request('GET', path, headers_extra=headers_extra)
    return result


def select_raw(table, query_string):
    """SELECT with a raw query string appended."""
    path = f'{table}?{query_string}'
    return _request('GET', path)


def count(table, filters=None):
    """Count rows in a table."""
    params = ['select=count']
    if filters:
        for f in filters:
            if isinstance(f, str):
                params.append(f)
            elif len(f) == 3:
                col, op, val = f
                params.append(f'{col}={op}.{val}')
    path = f'{table}?{"&".join(params)}'
    h = _headers()
    h['Prefer'] = 'count=exact'
    h['Range-Unit'] = 'items'
    h['Range'] = '0-0'
    url = f'{SUPABASE_URL}/rest/v1/{path}'
    req = urllib.request.Request(url, headers=h, method='GET')
    try:
        resp = urllib.request.urlopen(req)
        content_range = resp.headers.get('Content-Range', '*/0')
        total = content_range.split('/')[-1]
        return int(total) if total != '*' else 0
    except urllib.error.HTTPError:
        return 0


# ── INSERT ──────────────────────────────────────────────────────────
def insert(table, data, return_data=True):
    """INSERT one or more rows. data can be a dict or list of dicts."""
    prefer = 'return=representation' if return_data else 'return=minimal'
    h = _headers(prefer=prefer)
    body = json.dumps(data).encode()
    url = f'{SUPABASE_URL}/rest/v1/{table}'
    req = urllib.request.Request(url, data=body, headers=h, method='POST')
    try:
        resp = urllib.request.urlopen(req)
        content = resp.read().decode()
        if content:
            result = json.loads(content)
            if isinstance(data, dict) and isinstance(result, list) and len(result) == 1:
                return result[0]
            return result
        return None
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        raise Exception(f'Insert error {e.code}: {error_body}')


# ── UPDATE ──────────────────────────────────────────────────────────
def update(table, data, filters):
    """UPDATE rows matching filters."""
    params = []
    for f in filters:
        if isinstance(f, str):
            params.append(f)
        elif len(f) == 3:
            col, op, val = f
            params.append(f'{col}={op}.{val}')

    path = f'{table}?{"&".join(params)}'
    h = _headers(prefer='return=representation')
    body = json.dumps(data).encode()
    url = f'{SUPABASE_URL}/rest/v1/{path}'
    req = urllib.request.Request(url, data=body, headers=h, method='PATCH')
    try:
        resp = urllib.request.urlopen(req)
        content = resp.read().decode()
        return json.loads(content) if content else None
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        raise Exception(f'Update error {e.code}: {error_body}')


# ── DELETE ──────────────────────────────────────────────────────────
def delete(table, filters):
    """DELETE rows matching filters."""
    params = []
    for f in filters:
        if isinstance(f, str):
            params.append(f)
        elif len(f) == 3:
            col, op, val = f
            params.append(f'{col}={op}.{val}')

    path = f'{table}?{"&".join(params)}'
    url = f'{SUPABASE_URL}/rest/v1/{path}'
    req = urllib.request.Request(url, headers=_headers(), method='DELETE')
    try:
        resp = urllib.request.urlopen(req)
        return True
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        raise Exception(f'Delete error {e.code}: {error_body}')


# ── RPC (stored procedures) ────────────────────────────────────────
def rpc(fn_name, params=None):
    """Call a Supabase RPC function."""
    url = f'{SUPABASE_URL}/rest/v1/rpc/{fn_name}'
    h = _headers()
    body = json.dumps(params or {}).encode()
    req = urllib.request.Request(url, data=body, headers=h, method='POST')
    try:
        resp = urllib.request.urlopen(req)
        content = resp.read().decode()
        return json.loads(content) if content else None
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        raise Exception(f'RPC error {e.code}: {error_body}')
