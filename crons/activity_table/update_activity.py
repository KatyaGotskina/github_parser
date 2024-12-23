from datetime import datetime, timedelta, date
import os

import psycopg2
from psycopg2 import pool
import requests


postgresql_pool = psycopg2.pool.SimpleConnectionPool(
    1,  # min
    20,  # max
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT'),
    database=os.getenv('DB_NAME')
)

update_activity_sql = """
INSERT INTO activity (git_id, date, authors, commits)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (git_id, date) DO UPDATE SET
        commits = EXCLUDED.commits,
        authors = EXCLUDED.authors
"""

get_repos_sql = "SELECT id, repo, owner FROM top100 LIMIT 100"


def fetch_repo_commits(user: str, repo_name: str, date: date):
    url = f'https://api.github.com/search/commits?q={user}+user:{user}+repo:{repo_name}+author-date:{date}'
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def update_activity() -> None:
    data_for_insert = []
    connection = postgresql_pool.getconn()
    cursor = connection.cursor()
    try:
        cursor.execute(get_repos_sql)
        results = cursor.fetchall()
        for git_id, name, user in results:
            today = datetime.now().date()
            response_data = fetch_repo_commits(repo_name=name.split('/')[-1], user=user, date=today)
            if not response_data['items']:
                continue
            authors = {item["commit"]["author"]["name"] for item in response_data['items']}
            data_for_insert.append(
                    (
                        git_id,
                        today,
                        list[authors],
                        response_data['total_count']
                    )
                )
        cursor.executemany(update_activity_sql, data_for_insert)
    except psycopg2.Error as e:
        print(f"Database error: {e}")
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 403:
            cursor.executemany(update_activity_sql, data_for_insert)
            reset_timestamp = e.response.headers.get('X-RateLimit-Reset')
            print(f"Rate limit reset timestamp: {datetime(1970, 1, 1) + timedelta(seconds=int(reset_timestamp))}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        connection.commit()
        cursor.close()
        connection.close()
        postgresql_pool.putconn(connection)
