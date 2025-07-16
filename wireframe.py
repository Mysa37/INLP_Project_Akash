import tkinter as tk
from tkinter import messagebox


class WireframeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chatbot Hub - Wireframe")
        self.root.geometry("800x600")

        self.create_login_page()

    def create_admin_page(self):
        """Simulating the Admin Page with Users List"""
        # Header
        header_frame = tk.Frame(self.root, bg="#f56565")
        header_frame.pack(fill="x", padx=10, pady=10)

        title_label = tk.Label(header_frame, text="Admin Dashboard", font=("Arial", 24), bg="#f56565", fg="white")
        title_label.pack(pady=5)

        subtitle_label = tk.Label(header_frame, text="Manage users and access chatbot functionalities.", font=("Arial", 14), bg="#f56565", fg="white")
        subtitle_label.pack()

        logout_button = tk.Button(header_frame, text="Logout", bg="#f56565", fg="white", command=self.logout)
        logout_button.pack(side="right", padx=10, pady=5)

        # User Table (list of registered users)
        table_frame = tk.Frame(self.root)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        table_title = tk.Label(table_frame, text="Registered Users", font=("Arial", 18))
        table_title.pack()

        self.user_table = tk.Listbox(table_frame, height=10, width=50)
        self.user_table.pack(pady=10)

        for user in users:
            self.user_table.insert(tk.END, f"ID: {user['id']} | Username: {user['username']}")

        # Chatbot Buttons
        chatbot_frame = tk.Frame(self.root)
        chatbot_frame.pack(fill="x", padx=10, pady=20)

        dialogflow_button = tk.Button(chatbot_frame, text="Open Dialogflow", bg="#3182ce", fg="white", command=self.show_dialogflow)
        dialogflow_button.pack(side="left", padx=10, pady=5)

        mistral_button = tk.Button(chatbot_frame, text="Open Mistral", bg="#38a169", fg="white", command=self.show_mistral)
        mistral_button.pack(side="left", padx=10, pady=5)

    def show_dialogflow(self):
        """Simulate opening Dialogflow Chatbot"""
        messagebox.showinfo("Dialogflow", "Dialogflow Chatbot opened.")

    def show_mistral(self):
        """Simulate opening Mistral Chatbot"""
        messagebox.showinfo("Mistral", "Mistral Chatbot opened.")

    def logout(self):
        """Simulate user logout"""
        response = messagebox.askquestion("Logout", "Are you sure you want to log out?")
        if response == "yes":
            self.create_login_page()

    def create_user_page(self, username):
        """Simulating the User Page"""
        user = next(u for u in users if u['username'] == username)
        
        # Header
        header_frame = tk.Frame(self.root, bg="#38a169")
        header_frame.pack(fill="x", padx=10, pady=10)

        title_label = tk.Label(header_frame, text=f"Welcome {user['username']}!", font=("Arial", 24), bg="#38a169", fg="white")
        title_label.pack(pady=5)

        profile_frame = tk.Frame(self.root)
        profile_frame.pack(fill="both", expand=True, padx=10, pady=10)

        profile_title = tk.Label(profile_frame, text="Profile Details", font=("Arial", 18))
        profile_title.pack()

        user_profile = tk.Label(profile_frame, text=f"Username: {user['username']}\nEmail: {user['email']}", font=("Arial", 14))
        user_profile.pack(pady=10)

        chatbot_frame = tk.Frame(self.root)
        chatbot_frame.pack(fill="x", padx=10, pady=20)

        dialogflow_button = tk.Button(chatbot_frame, text="Open Dialogflow", bg="#3182ce", fg="white", command=self.show_dialogflow)
        dialogflow_button.pack(side="left", padx=10, pady=5)

        mistral_button = tk.Button(chatbot_frame, text="Open Mistral", bg="#38a169", fg="white", command=self.show_mistral)
        mistral_button.pack(side="left", padx=10, pady=5)

    def create_login_page(self):
        """Simulate the Login Page"""
        login_frame = tk.Frame(self.root)
        login_frame.pack(fill="both", expand=True, padx=20, pady=20)

        login_title = tk.Label(login_frame, text="Login to Chatbot Hub", font=("Arial", 24))
        login_title.pack(pady=20)

        username_label = tk.Label(login_frame, text="Username", font=("Arial", 14))
        username_label.pack()
        self.username_entry = tk.Entry(login_frame, font=("Arial", 14))
        self.username_entry.pack(pady=5)

        password_label = tk.Label(login_frame, text="Password", font=("Arial", 14))
        password_label.pack()
        self.password_entry = tk.Entry(login_frame, show="*", font=("Arial", 14))
        self.password_entry.pack(pady=5)

        login_button = tk.Button(login_frame, text="Login", bg="#3182ce", fg="white", command=self.login)
        login_button.pack(pady=10)

        register_button = tk.Button(login_frame, text="Register", bg="#38a169", fg="white", command=self.create_register_page)
        register_button.pack(pady=5)

    def login(self):
        """Simulate the login functionality"""
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Checking if the username exists and the password matches
        user = next((u for u in users if u['username'] == username), None)
        
        if user and user['password'] == password:
            if user['role'] == 'admin':
                self.create_admin_page()
            else:
                self.create_user_page(username)
        else:
            messagebox.showerror("Login", "Invalid username or password")

    def create_register_page(self):
        """Simulate the Register Page"""
        register_frame = tk.Frame(self.root)
        register_frame.pack(fill="both", expand=True, padx=20, pady=20)

        register_title = tk.Label(register_frame, text="Sign Up for Chatbot Hub", font=("Arial", 24))
        register_title.pack(pady=20)

        username_label = tk.Label(register_frame, text="Username", font=("Arial", 14))
        username_label.pack()
        self.register_username_entry = tk.Entry(register_frame, font=("Arial", 14))
        self.register_username_entry.pack(pady=5)

        email_label = tk.Label(register_frame, text="Email", font=("Arial", 14))
        email_label.pack()
        self.register_email_entry = tk.Entry(register_frame, font=("Arial", 14))
        self.register_email_entry.pack(pady=5)

        password_label = tk.Label(register_frame, text="Password", font=("Arial", 14))
        password_label.pack()
        self.register_password_entry = tk.Entry(register_frame, show="*", font=("Arial", 14))
        self.register_password_entry.pack(pady=5)

        confirm_password_label = tk.Label(register_frame, text="Confirm Password", font=("Arial", 14))
        confirm_password_label.pack()
        self.confirm_password_entry = tk.Entry(register_frame, show="*", font=("Arial", 14))
        self.confirm_password_entry.pack(pady=5)

        register_button = tk.Button(register_frame, text="Register", bg="#38a169", fg="white", command=self.register)
        register_button.pack(pady=10)

    def register(self):
        """Simulate user registration"""
        username = self.register_username_entry.get()
        email = self.register_email_entry.get()
        password = self.register_password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if password == confirm_password:
            users.append({'id': len(users) + 1, 'username': username, 'email': email, 'password': password, 'role': 'user'})
            messagebox.showinfo("Register", "Registration successful!")
            self.create_login_page()
        else:
            messagebox.showerror("Register", "Passwords do not match.")

# Simulating a list of registered users
users = [
    {'id': 1, 'username': 'admin', 'email': 'admin@example.com', 'password': 'admin', 'role': 'admin'},
    {'id': 2, 'username': 'user1', 'email': 'user1@example.com', 'password': 'password', 'role': 'user'},
    {'id': 3, 'username': 'user2', 'email': 'user2@example.com', 'password': 'password', 'role': 'user'},
]

# Create the main window
root = tk.Tk()
app = WireframeApp(root)
root.mainloop()
