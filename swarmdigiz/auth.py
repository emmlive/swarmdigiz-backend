
import sqlite3
import pandas as pd
import streamlit_authenticator as stauth

def db(db_path):
    return sqlite3.connect(db_path, check_same_thread=False)

def get_credentials(db_path):
    conn = db(db_path)
    df = pd.read_sql("SELECT username,email,name,password FROM users WHERE active=1", conn)
    conn.close()
    return {
        "usernames": {
            r["username"]: {
                "email": r["email"],
                "name": r["name"],
                "password": r["password"]
            } for _, r in df.iterrows()
        }
    }

def build_authenticator(db_path, cookie_name, cookie_key, days):
    return stauth.Authenticate(
        get_credentials(db_path),
        cookie_name,
        cookie_key,
        days
    )
