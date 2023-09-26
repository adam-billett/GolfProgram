from tkinter import messagebox

import psycopg2


class DatabaseManager:
    def __init__(self, dbname, user, password, host, port):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port

        try:
            self.connection = psycopg2.connect(
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port
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

    # Login method with logic to ensure they are a user
    def login(self, username, password):
        try:
            self.cursor.execute("SELECT password FROM users WHERE username = %s",
                                (username,))
            db_password = self.cursor.fetchone()

            if db_password and db_password[0] == password:
                return True  # Login successful
            else:
                return False  # Login failed

        except psycopg2.Error as e:
            messagebox.showerror("Error", str(e))
            return False  # Login Failed

    # Create method database side
    def create(self, username, password, confirm, name):
        self.cursor.execute("SELECT username FROM users WHERE username = %s",
                            (username,))
        existing_user = self.cursor.fetchone()  # grabbing a user if one exists

        if existing_user:  # checking to see if that username is taken
            messagebox.showerror("Username already exists")
            return False

        if password != confirm:
            messagebox.showerror("Passwords do not match")

            return False

        self.cursor.execute("INSERT INTO users (username, password, confirm_pass, full_name, connections, created_at) "
                            "VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP)",
                            (username, password, confirm, name, "None"))
        self.connection.commit()

        return True  # Creation successful

