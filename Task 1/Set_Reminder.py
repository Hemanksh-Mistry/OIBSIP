import sqlite3
import datetime

def set_reminder(reminder_text, reminder_time):
        conn = sqlite3.connect('reminders.db')
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS reminders (id INTEGER PRIMARY KEY, text TEXT, time TEXT)')
        cursor.execute('INSERT INTO reminders (text, time) VALUES (?, ?)', (reminder_text, reminder_time))
        conn.commit()
        conn.close()