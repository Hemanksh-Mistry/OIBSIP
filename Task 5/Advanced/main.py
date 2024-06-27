import tkinter as tk
from tkinter import messagebox, scrolledtext
import mysql.connector

# Database connection
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",  # Replace with your MySQL username
    password="1234",  # Replace with your MySQL password
    database="chatapp_db"
)
cursor = db_connection.cursor()

# Tkinter setup
root = tk.Tk()
root.title("Chat Application")

# Global variables
current_user = None
current_room_id = None

# Function to register a new user
def register_user():
        username = reg_username.get()
        password = reg_password.get()

        if not username or not password:
                messagebox.showerror("Error", "Please enter both username and password.")
                return

        try:
                # Insert new user into the database
                cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
                db_connection.commit()
                messagebox.showinfo("Success", "Registration successful.")
        except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error: {err}")

# Function to handle user login
def login_user():
        global current_user
        username = login_username.get()
        password = login_password.get()

        if not username or not password:
                messagebox.showerror("Error", "Please enter both username and password.")
                return

        # Query the database for the user credentials
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()

        if user:
                current_user = user
                messagebox.showinfo("Success", f"Welcome, {username}!")
                show_chat_interface()
        else:
                messagebox.showerror("Error", "Invalid username or password.")

# Function to create a new chat room
def create_chat_room():
        room_name = room_name_entry.get()

        if not room_name:
                messagebox.showerror("Error", "Please enter a room name.")
                return

        try:
                # Insert new room into the database
                cursor.execute("INSERT INTO chat_rooms (room_name) VALUES (%s)", (room_name,))
                db_connection.commit()
                messagebox.showinfo("Success", "Chat room created successfully.")
                load_chat_rooms()
        except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error: {err}")

# Function to load available chat rooms
def load_chat_rooms():
        cursor.execute("SELECT * FROM chat_rooms")
        rooms = cursor.fetchall()

        room_listbox.delete(0, tk.END)  # Clear current list

        for room in rooms:
                room_listbox.insert(tk.END, room[1])  # Display room names

# Function to join a selected chat room
def join_chat_room():
        global current_room_id
        selected_room_index = room_listbox.curselection()

        if selected_room_index:
                room_name = room_listbox.get(selected_room_index)
                cursor.execute("SELECT * FROM chat_rooms WHERE room_name = %s", (room_name,))
                room = cursor.fetchone()

                if room:
                        current_room_id = room[0]  # Set current room ID
                        messagebox.showinfo("Success", f"Joined chat room: {room_name}")
                        show_chat_messages()

# Function to send a message
def send_message():
        message = message_entry.get("1.0", tk.END).strip()

        if not message:
                messagebox.showerror("Error", "Message cannot be empty.")
                return

        try:
                # Insert message into the database
                cursor.execute("INSERT INTO messages (sender_id, message, room_id) VALUES (%s, %s, %s)",
                               (current_user[0], message, current_room_id))
                db_connection.commit()
                message_entry.delete("1.0", tk.END)  # Clear message input
                show_chat_messages()
        except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error: {err}")

# Function to display chat messages
def show_chat_messages():
        message_text.config(state=tk.NORMAL)
        message_text.delete("1.0", tk.END)  # Clear previous messages

        cursor.execute("SELECT * FROM messages WHERE room_id = %s ORDER BY timestamp", (current_room_id,))
        messages = cursor.fetchall()

        for msg in messages:
                sender_name = get_username_by_id(msg[1])
                message_text.insert(tk.END, f"{sender_name}: {msg[2]}\n")

        message_text.config(state=tk.DISABLED)  # Disable editing

# Function to get username by ID
def get_username_by_id(user_id):
        cursor.execute("SELECT username FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        return user[0] if user else "Unknown"

# Function to display the chat interface
def show_chat_interface():
        login_frame.pack_forget()  # Hide login frame

        chat_frame.pack(fill=tk.BOTH, expand=True)

        load_chat_rooms()  # Load available chat rooms

        # Display welcome message
        welcome_label.config(text=f"Welcome, {current_user[1]}!")

# GUI elements
login_frame = tk.Frame(root)
login_frame.pack(fill=tk.BOTH, expand=True)

reg_label = tk.Label(login_frame, text="Register")
reg_label.grid(row=0, column=0, columnspan=2)

reg_username_label = tk.Label(login_frame, text="Username:")
reg_username_label.grid(row=1, column=0)
reg_username = tk.Entry(login_frame)
reg_username.grid(row=1, column=1)

reg_password_label = tk.Label(login_frame, text="Password:")
reg_password_label.grid(row=2, column=0)
reg_password = tk.Entry(login_frame, show="*")
reg_password.grid(row=2, column=1)

reg_button = tk.Button(login_frame, text="Register", command=register_user)
reg_button.grid(row=3, column=0, columnspan=2)

login_label = tk.Label(login_frame, text="Login")
login_label.grid(row=4, column=0, columnspan=2)

login_username_label = tk.Label(login_frame, text="Username:")
login_username_label.grid(row=5, column=0)
login_username = tk.Entry(login_frame)
login_username.grid(row=5, column=1)

login_password_label = tk.Label(login_frame, text="Password:")
login_password_label.grid(row=6, column=0)
login_password = tk.Entry(login_frame, show="*")
login_password.grid(row=6, column=1)

login_button = tk.Button(login_frame, text="Login", command=login_user)
login_button.grid(row=7, column=0, columnspan=2)

# Chat interface elements
chat_frame = tk.Frame(root)

room_label = tk.Label(chat_frame, text="Chat Rooms")
room_label.pack()

room_listbox = tk.Listbox(chat_frame, height=5)
room_listbox.pack()

create_room_label = tk.Label(chat_frame, text="Create New Room")
create_room_label.pack()

room_name_entry = tk.Entry(chat_frame)
room_name_entry.pack()

create_room_button = tk.Button(chat_frame, text="Create Room", command=create_chat_room)
create_room_button.pack()

join_room_label = tk.Label(chat_frame, text="Join Room")
join_room_label.pack()

join_room_button = tk.Button(chat_frame, text="Join Room", command=join_chat_room)
join_room_button.pack()

welcome_label = tk.Label(chat_frame, text="")
welcome_label.pack()

message_text = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD, width=50, height=20)
message_text.pack()

message_entry = tk.Text(chat_frame, wrap=tk.WORD, width=50, height=5)
message_entry.pack()

send_button = tk.Button(chat_frame, text="Send", command=send_message)
send_button.pack()

# Start the GUI main loop
root.mainloop()