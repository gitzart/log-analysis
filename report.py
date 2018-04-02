#!/usr/bin/env python3

import os

from functools import wraps
from pprint import pprint

import psycopg2


DSN = os.getenv('DATABASE_URL')


def connect(f):
    '''Manage database connection and cursor.'''
    @wraps(f)
    def wrapper(*args, **kwargs):
        conn = psycopg2.connect(DSN)
        cursor = conn.cursor()
        f(cursor, *args, **kwargs)
        cursor.close()
        conn.close()
    return wrapper


@connect
def top_articles(cursor, limit=3):
    query = '''
        SELECT articles.title, count(log.path) AS views
        FROM articles
        LEFT JOIN log
        ON articles.slug = split_part(log.path, '/', 3)
        GROUP BY articles.id
        ORDER BY views DESC
        LIMIT %s;
    '''
    cursor.execute(query, (limit,))
    data = cursor.fetchall()
    pprint(data)


@connect
def top_authors(cursor, limit=3):
    query = '''
        SELECT authors.name, sum(views)::int
        FROM authors, (
            SELECT articles.author, count(log.path) AS views
            FROM articles
            LEFT JOIN log
            ON articles.slug = split_part(log.path, '/', 3)
            GROUP BY articles.id
        ) AS top_articles
        WHERE authors.id = top_articles.author
        GROUP BY authors.id
        LIMIT %s;
    '''
    cursor.execute(query, (limit,))
    data = cursor.fetchall()
    pprint(data)
