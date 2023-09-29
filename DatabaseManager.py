from tkinter import messagebox

import psycopg2


class DatabaseManager:
    def __init__(self, dbname, user, password, host, port):
        self.current_user = None
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
                        username VARCHAR(255) NOT NULL UNIQUE,
                        password VARCHAR(255) NOT NULL,
                        confirm_pass VARCHAR(255),
                        role VARCHAR(255),
                        full_name VARCHAR(255),
                        connections VARCHAR(255),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')

        self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS courses (
                        course_id SERIAL PRIMARY KEY,
                        course_name VARCHAR(255) NOT NULL,
                        location VARCHAR(255),
                        rates DECIMAL(10, 2),
                        par INT,
                        tee_times BIGINT
                    )
                ''')

        self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS holes (
                        hole_id SERIAL PRIMARY KEY,
                        course_id INT,
                        hole_num INT,
                        par INT,
                        distance INT,
                        handicap INT,
                        UNIQUE(course_id, hole_num),
                        FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE
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
                    CREATE TABLE IF NOT EXISTS round_hole (
                        round_hole_id SERIAL PRIMARY KEY,
                        round_id INT REFERENCES rounds(round_id),
                        hole_id INT REFERENCES holes(hole_id),
                        score INT,
                        CONSTRAINT uq_round_hole UNIQUE (round_id, hole_id)
                    )
                ''')

        self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS monitor (
                        session_id SERIAL PRIMARY KEY,
                        user_id INT REFERENCES users(user_id),
                        club_speed DECIMAL(6,2),
                        ball_speed DECIMAL(6,2),
                        spin_rate DECIMAL(6,2),
                        carry DECIMAL(6,2),
                        total DECIMAL(6,2),
                        smash_factor DECIMAL(6,2),
                        launch_angle DECIMAL(6,2),
                        FOREIGN KEY (user_id) REFERENCES users(user_id)                           
                    )
                ''')

        self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS fitness (
                        exercise_id SERIAL PRIMARY KEY,
                        user_id INT REFERENCES users(user_id),
                        sets INT,
                        reps INT,
                        type VARCHAR(255),
                        completed BOOLEAN
                    )
                ''')

        self.connection.commit()

    # GRABBING ALL METHODS
    # Method to populate a list of users
    def get_all_users(self):
        self.cursor.execute("SELECT username FROM users")
        users = self.cursor.fetchall()
        usernames = [user[0] for user in users]
        return usernames

    # Method to grab the users role
    def get_role(self):
        self.cursor.execute("SELECT role FROM users WHERE username = %s", (str(self.current_user),))
        return self.cursor.fetchone()

    # Method to get the current users ID
    def get_curr_user_id(self):
        self.cursor.execute("SELECT user_id FROM users WHERE username = %s", (str(self.current_user),))
        return self.cursor.fetchone()

    # Method to get all the courses
    def get_courses(self):
        self.cursor.execute("SELECT course_name FROM courses")
        return self.cursor.fetchall()

    # Method to load in all the info on the course
    def load_course(self, selected_option):
        self.cursor.execute("SELECT * FROM courses WHERE course_name = %s", (selected_option,))
        return self.cursor.fetchall()

    # Login method with logic to ensure they are a user
    def login(self, username, password):
        try:
            self.cursor.execute("SELECT password, role FROM users WHERE username = %s AND password = %s",
                                (username, password))
            result = self.cursor.fetchone()

            if result:
                role = result[1]
                self.current_user = username
                return role  # Login Successful

            return None  # Login Failed

        except psycopg2.Error as e:
            messagebox.showerror("Error", str(e))
            return None  # Login Failed

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

    # ADMIN METHODS
    def user_roles(self, role, username):  # Admin method to adjust users roles
        try:
            self.cursor.execute("UPDATE users SET role = %s WHERE username = %s",
                                (role, username))
            self.connection.commit()
            return True
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def add_course(self, name, location, rate, par, tee_time):  # Admin method to add a course
        try:
            self.cursor.execute("INSERT INTO courses (course_name, location, rates, par, tee_times) VALUES (%s, %s, %s, %s, %s)",
                                (name, location, rate, par, tee_time))
            self.connection.commit()
            return True
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def add_hole(self, hole_num, par, distance, handicap):  # Admin method to add a hole
        try:
            self.cursor.execute("INSERT INTO holes (hole_num, par, distance, handicap) VALUES (%s, %s, %s, %s)",
                                (hole_num, par, distance, handicap))
            self.connection.commit()
            return True
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # USER METHODS
    def play_golf(self, holes, score, par, difference):  # User method to play a round of golf
        pass

    def golf_rounds(self):  # User method to check past rounds of golf
        pass

    def golf_sim(self):  # User method to go into the golf simulator
        pass

    def swing_analysis(self):  # User method to get a swing analysis
        pass

    def fitness_golf(self):  # User method to get into the fitness portion
        pass

    def golf_insights(self):  # User method to get tips/ insights of their golf game
        pass
