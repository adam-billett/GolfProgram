import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

import customtkinter as ctk
import psycopg2


class GolfApp:
    def __init__(self, app):
        self.datetime = None
        ctk.set_appearance_mode("dark")

        self.app = app
        self.app.geometry("200x200")
        self.app.title("Golf")

        self.login_menu()

        # attempt a connection with the DB
        try:
            self.connection = psycopg2.connect(
                dbname="GolfApp",
                user="postgres",
                password="Bearcat",
                host="localhost",
                port="5432"
            )
            self.cursor = self.connection.cursor()
        except psycopg2.Error as e:
            messagebox.showerror("Error", str(e))

        self.create_tables()

        # SQL TABLE INITIATE

    def create_tables(self):
        self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        user_id SERIAL PRIMARY KEY,
                        username VARCHAR,
                        password VARCHAR,
                        confirm_pass VARCHAR,
                        full_name VARCHAR,
                        connections VARCHAR,
                        created_at TIMESTAMP
                        )
                    ''')

        self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS courses (
                        course_id SERIAL PRIMARY KEY,
                        course_name VARCHAR,
                        location VARCHAR,
                        rates BIGINT,
                        par INT,
                        tee_times BIGINT
                        )
                    ''')

        self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS rounds (
                        round_id SERIAL PRIMARY KEY,
                        course_id INT REFERENCES courses(course_id),
                        user_id INT REFERENCES users(user_id),
                        holes_played INT,
                        score INT,
                        par INT,
                        difference INT
                    )
                ''')

        self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS monitor (
                        session_id SERIAL PRIMARY KEY,
                        user_id INT REFERENCES users(user_id),
                        club_speed BIGINT,
                        ball_speed BIGINT,
                        spin_rate BIGINT,
                        carry BIGINT,
                        total BIGINT,
                        smash_factor BIGINT,
                        launch_angle BIGINT                           
                    )
                ''')

        self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS fitness (
                    exercise_id SERIAL PRIMARY KEY,
                    user_id INT REFERENCES users(user_id),
                    sets INT,
                    reps INT,
                    type VARCHAR,
                    completed boolean
                    )
                ''')

        self.connection.commit()

    # Go back to main menu
    def back_to_login(self):
        if self.create_frame:
            self.create_frame.withdraw()
        self.login_menu()

    def on_close(self):  # Method for all .protocols on new windows
        self.app.quit()

        # LOGIN AND CREATE USER MENU

    # LOGIN MENU
    def login_menu(self):
        # withdrawing the root frame then creating a new window
        self.login_window = ctk.CTkToplevel(self.app)
        # setting the title size and a protocol for the new window
        self.login_window.title("Login")
        self.login_window.geometry("300x250")
        self.login_window.protocol("WM_DELETE_WINDOW", self.on_close)
        self.app.withdraw()

        # Creating a frame inside the window
        self.login_frame = ctk.CTkFrame(master=self.login_window)
        self.login_frame.pack(pady=20, padx=40, fill='both', expand=True)

        # Username entry box
        self.username = ctk.CTkEntry(self.login_frame, placeholder_text="Username")
        self.username.pack(pady=12, padx=10)

        # Password entry box
        self.password = ctk.CTkEntry(self.login_frame, placeholder_text="Password")
        self.password.pack(pady=12, padx=10)

        # Login button
        self.login_btn = ctk.CTkButton(self.login_frame, text='Login', command=self.login)
        self.login_btn.pack(pady=12, padx=10)

        # Create a user button
        self.create_btn = ctk.CTkButton(self.login_frame, text='Create User', command=self.create_menu)
        self.create_btn.pack(pady=12, padx=10)

    # CREATE MENU
    def create_menu(self):
        self.app.withdraw()
        self.login_window.withdraw()

        self.create_frame = ctk.CTkToplevel(self.app)
        self.create_frame.title("Create")
        self.create_frame.geometry("275x300")
        self.create_frame.protocol("WM_DELETE_WINDOW", self.on_close)

        # username entry
        self.username_create = ctk.CTkEntry(self.create_frame, placeholder_text="Username")
        self.username_create.pack(pady=8, padx=4)

        # password entry
        self.password_create = ctk.CTkEntry(self.create_frame, placeholder_text="Password")
        self.password_create.pack(pady=8, padx=4)

        # Confirm password entry
        self.password_confirm = ctk.CTkEntry(self.create_frame, placeholder_text="Password")
        self.password_confirm.pack(pady=8, padx=4)

        # full name entry
        self.full_name = ctk.CTkEntry(self.create_frame, placeholder_text="Full Name")
        self.full_name.pack(pady=8, padx=4)

        # Create submit button
        self.submit = ctk.CTkButton(self.create_frame, text="Submit", command=self.create)
        self.submit.pack(pady=8, padx=4)

        # back to the login page button
        self.back = ctk.CTkButton(self.create_frame, text="Back", command=self.back_to_login)
        self.back.pack(pady=8, padx=4)

        # LOGIN AND CREATE METHODS

    # LOGIN
    def login(self):  # Method to login
        username = self.username.get()
        password = self.password.get()

        if not username or not password:
            messagebox.showerror("Missing Info, try again")
            return

        try:
            self.cursor.execute("SELECT password FROM users WHERE username = %s",
                                (username,))
            db_password = self.cursor.fetchone()

            if db_password and db_password[0] == password:
                self.current_user = username
                self.app.withdraw()
                self.password.delete(0, tk.END)

                self.main_menu(username)

            else:
                messagebox.showerror("Invalid username or password")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # CREATE
    def create(self):
        username = self.username_create.get()
        password = self.password_create.get()
        password_confirm = self.password_confirm.get()
        full_name = self.full_name.get()

        self.cursor.execute("SELECT username FROM users WHERE username = %s",
                            (username,))
        existing_user = self.cursor.fetchone()  # grabbing a user if one exists

        if existing_user:  # checking to see if that username is taken
            messagebox.showerror("Username already exists")
            return

        if password != password_confirm:
            messagebox.showerror("Passwords do not match")
            self.password.delete(0, tk.END)
            self.password_confirm.delete(0, tk.END)
            return

        self.cursor.execute("INSERT INTO users (username, password, confirm_pass, full_name, connections, created_at) "
                            "VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP)",
                            (username, password, password_confirm, full_name, "None"))
        self.connection.commit()
        messagebox.showinfo("Account created")

        self.create_frame.withdraw()
        self.login_menu()

        # MAIN MENU

    def main_menu(self, current_user):
        self.login_window.withdraw()

        self.main_frame = ctk.CTkToplevel(self.app)
        self.main_frame.title("Golf Now")
        self.main_frame.geometry("500x500")
        self.main_frame.protocol("WM_DELETE_WINDOW", self.on_close)

        # Play golf Button
        self.play = ctk.CTkButton(self.main_frame, text="Play Golf")
        self.play.pack(pady=8, padx=4)

        # Check past rounds of golf button
        self.history = ctk.CTkButton(self.main_frame, text="History")
        self.history.pack(pady=8, padx=4)

        # Golf Simulator button
        self.launch = ctk.CTkButton(self.main_frame, text="Golf Simulator")
        self.launch.pack(pady=8, padx=4)

        # Swing analysis button
        self.analysis = ctk.CTkButton(self.main_frame, text="Swing Analysis")
        self.analysis.pack(pady=8, padx=4)

        # Fitness button
        self.fitness = ctk.CTkButton(self.main_frame, text="Fitness")
        self.fitness.pack(pady=8, padx=4)

        # Game insights/tips button
        self.tips = ctk.CTkButton(self.main_frame, text="Game Insights")
        self.tips.pack(pady=8, padx=4)

        # Exit button
        self.exit = ctk.CTkButton(self.main_frame, text="Exit")
        self.exit.pack(pady=8, padx=4)




def main():
    golf = ctk.CTk()
    app = GolfApp(golf)
    golf.mainloop()


if __name__ == "__main__":
    main()