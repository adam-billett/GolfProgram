import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

import customtkinter as ctk
import psycopg2


class GolfApp:
    def __init__(self, app):
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

    def on_close(self): # Method for all .protocols on new windows
        self.app.quit()

    def login_menu(self):
        # withdrawing the root frame then creating a new window
        self.login_window = ctk.CTkToplevel(self.app)
        # setting the title size and a protocol for the new window
        self.login_window.title("Login")
        self.login_window.geometry("325x375")
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
        self.create_btn = ctk.CTkButton(self.login_frame, text='Create User')
        self.create_btn.pack(pady=12, padx=10)

    def login(self): # Method to login
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



def main():
    golf = ctk.CTk()
    app = GolfApp(golf)
    golf.mainloop()

if __name__ == "__main__":
    main()
