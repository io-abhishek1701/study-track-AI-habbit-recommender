import random
import smtplib
import sqlite3
import os
from email.message import EmailMessage
from datetime import datetime, timedelta
import streamlit as st

DB_NAME = "studytrack_ai.db"
OTP_RATE_LIMIT_WINDOW_MINUTES = 15
OTP_MAX_REQUESTS_PER_WINDOW = 3
OTP_REQUEST_COOLDOWN_SECONDS = 60


def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)


def init_otp_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS email_otp (
            email TEXT PRIMARY KEY,
            otp TEXT NOT NULL,
            expires_at TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS otp_request_limits (
            email TEXT PRIMARY KEY,
            request_count INTEGER NOT NULL,
            window_started_at TEXT NOT NULL,
            last_requested_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def generate_otp():
    return str(random.randint(100000, 999999))


def otp_expiry(minutes=5):
    return (datetime.now() + timedelta(minutes=minutes)).isoformat()


def store_otp(email, otp, expiry):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR REPLACE INTO email_otp (email, otp, expires_at) VALUES (?, ?, ?)",
        (email, otp, expiry)
    )
    conn.commit()
    conn.close()


def delete_otp(email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM email_otp WHERE email = ?", (email,))
    conn.commit()
    conn.close()


def check_otp_request_limit(email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT request_count, window_started_at, last_requested_at
        FROM otp_request_limits
        WHERE email = ?
        """,
        (email,)
    )
    row = cursor.fetchone()
    conn.close()

    if not row:
        return True, None

    request_count, window_started_at, last_requested_at = row
    now = datetime.now()
    window_start = datetime.fromisoformat(window_started_at)
    last_request = datetime.fromisoformat(last_requested_at)

    cooldown_until = last_request + timedelta(seconds=OTP_REQUEST_COOLDOWN_SECONDS)
    if now < cooldown_until:
        seconds_left = int((cooldown_until - now).total_seconds()) + 1
        return False, f"Please wait {seconds_left} seconds before requesting another OTP."

    window_until = window_start + timedelta(minutes=OTP_RATE_LIMIT_WINDOW_MINUTES)
    if now < window_until and request_count >= OTP_MAX_REQUESTS_PER_WINDOW:
        minutes_left = int((window_until - now).total_seconds() // 60) + 1
        return False, f"Too many OTP requests. Try again in {minutes_left} minutes."

    return True, None


def record_otp_request(email):
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now()
    cursor.execute(
        """
        SELECT request_count, window_started_at
        FROM otp_request_limits
        WHERE email = ?
        """,
        (email,)
    )
    row = cursor.fetchone()

    if not row:
        cursor.execute(
            """
            INSERT INTO otp_request_limits (
                email, request_count, window_started_at, last_requested_at
            )
            VALUES (?, ?, ?, ?)
            """,
            (email, 1, now.isoformat(), now.isoformat())
        )
    else:
        request_count, window_started_at = row
        window_start = datetime.fromisoformat(window_started_at)
        if now >= window_start + timedelta(minutes=OTP_RATE_LIMIT_WINDOW_MINUTES):
            request_count = 1
            window_started_at = now.isoformat()
        else:
            request_count += 1

        cursor.execute(
            """
            UPDATE otp_request_limits
            SET request_count = ?, window_started_at = ?, last_requested_at = ?
            WHERE email = ?
            """,
            (request_count, window_started_at, now.isoformat(), email)
        )

    conn.commit()
    conn.close()


def verify_otp(email, entered_otp):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT otp, expires_at FROM email_otp WHERE email = ?",
        (email,)
    )
    row = cursor.fetchone()
    conn.close()

    if not row:
        return False

    stored_otp, expires_at = row

    if datetime.now() > datetime.fromisoformat(expires_at):
        delete_otp(email)
        return False

    if stored_otp != entered_otp:
        return False

    delete_otp(email)
    return True


def get_secret(name):
    value = os.getenv(name)
    if value:
        return value

    try:
        return st.secrets.get(name)
    except Exception:
        return None


def get_email_credentials():
    email_user = get_secret("EMAIL_USER")
    email_password = get_secret("EMAIL_PASSWORD")

    if not email_user or not email_password:
        raise RuntimeError(
            "Email OTP is unavailable because EMAIL_USER and EMAIL_PASSWORD are not configured."
        )

    return email_user, email_password


def send_otp_email(to_email, otp):
    email_user, email_password = get_email_credentials()

    msg = EmailMessage()
    msg.set_content(
        f"Your StudyTrack AI verification OTP is: {otp}\n\n"
        "This OTP is valid for 5 minutes."
    )
    msg["Subject"] = "StudyTrack AI – Email Verification"
    msg["From"] = email_user
    msg["To"] = to_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(email_user, email_password)
        server.send_message(msg)
