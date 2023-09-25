import json

import customtkinter as ctk
class GolfApp:
    def __init__(self):
        self.users = {}
        self.score_history = []
        self.load_history()
        self.load_users()

    def load_history(self):
        try:
            with open("history.json", "r") as file:
                self.score_history = json.load(file)
        except FileNotFoundError:
            self.score_history = []

    def save_history(self):
        with open("history.json", "w") as file:
            json.dump(self.score_history, file, indent=1)

    def load_users(self):
        try:
            with open("users.json", "r") as file:
                self.users = json.load(file)
        except FileNotFoundError:
            self.users = {}

    def save_users(self):
        with open("users.json", "w") as file:
            json.dump(self.users, file, default=str)

    def login_menu(self):

        print("1. Login")
        print("2. Create account")
        print("3. Exit")

    def main_menu(self):
        # Ideas for more features for app go here
        # Home page to display golf news.

        print("1. Play golf")
        print("2. History")
        print("3. Launch Monitor")
        print("4. Swing Analysis")
        print("5. Fitness")
        print("6. Game Insights")
        print("7. Exit")

    def play_golf(self):
        # track score and shots
        # course info and gps as well as mapping
        date = input("Enter the date (MM-DD-YY): ")
        course = input("Enter the course: ")
        num_holes = int(input("Numbers of holes: "))

        round_scores = {"date": date,
                        "course": course,
                        "holes": {}
                        }
        total_diff = 0
        total_par = 0
        total_score = 0

        for hole in range(1, num_holes + 1):
            par = int(input(f"Enter the par for hole {hole}: "))
            score = int(input(f"Enter score for hole {hole}: "))

            under_or_over = score - par
            total_diff += under_or_over
            total_par += par
            total_score += score

            if total_par > total_score:
                round_scores["holes"][hole] = {
                    "score": score,
                    "par": par,
                    "under_or_over": under_or_over,
                    "status": f"{under_or_over} under par"
                }
                print(f"You are now {total_diff} under par")
            elif total_par < total_score:
                round_scores["holes"][hole] = {
                    "score": score,
                    "par": par,
                    "under_or_over": under_or_over,
                    "status": f"{abs(under_or_over)} over par"
                }
                print(f"You are now {total_diff} over par")
            else:
                round_scores["holes"][hole] = {
                    "score": score,
                    "par": par,
                    "under_or_over": under_or_over,
                    "status": "Even par"
                }
                print("You are even par")

        round_scores["total_diff"] = total_diff
        self.score_history.append(round_scores)
        self.save_history()
        print("Scorecard Saved")
    def display_history(self):
        search_date = input("Enter the date of the round: ")
        found_round = None

        for round in self.score_history:
            if round['date'] == search_date:
                found_round = round
                break
        if found_round:
            print(f"Date: {found_round['date']}, Course: {found_round['course']}")
            print("Hole Scores:")
            for hole, data in found_round['holes'].items():
                par = data['par']
                score = data['score']
                under_or_over = data['under_or_over']

                if under_or_over > 0:
                    par_status = f"{under_or_over} over par"
                elif under_or_over < 0:
                    par_status = f"{abs(under_or_over)} under par"
                else:
                    par_status = "Even par"

                print(f"Hole {hole} Par: {par}, Score: {score}, {par_status}")

            if found_round['total_diff'] > 0:
                print(f"{found_round['total_diff']} over par")
            elif found_round['total_diff'] < 0:
                print(f"{found_round['total_diff']} under par")
            else:
                print("Even par")
        else:
            print(f"No round found for the date: {search_date}")

    def launch_monitor(self):
        pass

    def swing_analysis(self):
        pass

    def fitness(self):
        # workout golf related
        # diet
        pass

    def game_insights(self):
        # tips and tricks
        # personal data on improvements
        pass

    def login(self):
        username = input("Enter username: ")
        password = input("Enter password: ")

        if username in self.users and self.users[username] == password:
            print("Login successful.")
            self.load_history()
            return True
            # code for after login actions goes here
        else:
            print("Invalid username or password.")

    def create(self):
        username = input("Please enter username: ")
        if username in self.users:
            print("Username already exists. Please choose another")
            return

        password = input("Enter a password: ")
        self.users[username] = password
        self.save_users()
        print("Account created successfully.")

    def exit(self):
        print("Have a nice day!")
        exit()

    def go_back(self):
        exit()

    def run(self):
        while True:
            self.login_menu()
            choice = input("Select option: ")

            if choice == '1':
                if self.login():
                    while True:
                        self.main_menu()
                        choice1 = input("Select option: ")

                        if choice1 == '1':
                            self.play_golf()
                        elif choice1 == '2':
                            self.display_history()
                        elif choice1 == '3':
                            self.launch_monitor()
                        elif choice1 == '4':
                            self.swing_analysis()
                        elif choice1 == '5':
                            self.fitness()
                        elif choice1 == '6':
                            self.game_insights()
                        elif choice1 == '7':
                            self.go_back()
                        else:
                            print("Invalid option")

            elif choice == '2':
                self.create()
            elif choice == '3':
                self.exit()
                break
            else:
                print("Invalid choice. Select one of the options displayed.")


golf_app = GolfApp()
golf_app.run()
