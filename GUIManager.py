import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

import DatabaseManager as db


class GUIManager:
    def __init__(self, app, db_manager):
        self.app = app
        self.db_manager = db_manager

        self.main_frame = None
        self.admin_frame = None

        self.initialize_gui()

    def on_option(self, event, select_option):  # Drop down event
        select_option = self.selected_option

    def on_close(self):  # Method for all .protocols on new windows
        self.app.quit()

    def back_to_login(self):  # Back to the login screen after the user creates a new user
        if self.create_frame:
            self.create_frame.withdraw()
        self.initialize_gui()

    # Login menu (The first window to show)
    def initialize_gui(self):

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

    # Login verification
    def login(self):
        username = self.username.get()
        password = self.password.get()

        if not username or not password:
            messagebox.showerror("Missing Info", "Username or password is missing")
            return

        user_info = self.db_manager.login(username, password)
        if user_info is not None:
            # Login Successful
            self.current_user_role = user_info
            if self.current_user_role == "admin":
                # Display admin menu
                self.logged_in = True
                self.admin_menu()
            elif self.current_user_role == "user":
                self.logged_in = True
                self.user_menu()
                # Display users menu
            else:
                messagebox.showerror("Error", "You have no role")
        else:
            # Login Fail
            self.password.delete(0, tk.END)
            messagebox.showerror("Login Failed", "Invalid username or password")

    # Create a new user frame
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

    def create(self):
        username = self.username_create.get()
        password = self.password_create.get()
        confirm = self.password_confirm.get()
        name = self.full_name.get()

        if password != confirm:
            # Passwords do not match
            messagebox.showerror("Passwords", "Passwords do not match")
            self.password_confirm.delete(0, tk.END)
            return

        if self.db_manager.create(username, password, confirm, name):
            # Creation successful
            messagebox.showinfo("Success", "Account Creation successful")
            self.back_to_login()

        else:
            # Creation Failed
            messagebox.showerror("Error", "Username already exists")

    # MAIN MENU
    def user_menu(self):
        # IF ROLE IS A USER THIS IS THE MAIN MENU
        self.login_window.withdraw()  # withdrawing the login menu

        # Making a new frame for the users menu
        self.main_frame = ctk.CTkToplevel(self.app)
        self.main_frame.title("Golf Now")
        self.main_frame.geometry("500x500")
        self.main_frame.protocol("WM_DELETE_WINDOW", self.on_close)

        # Displaying the current user in the top
        self.curr_user = ctk.CTkLabel(self.main_frame, text=self.username.get())
        self.curr_user.pack(pady=8, padx=4)

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
        self.logout_btn = ctk.CTkButton(self.main_frame, text="Logout", command=self.logout)
        self.logout_btn.pack(pady=8, padx=4)

    def admin_menu(self):
        # IF ROLE IS ADMIN THIS IS THE MAIN MENU

        self.login_window.withdraw()  # Withdrawing the login menu

        #  Making a new frame for the admins menu
        self.admin_frame = ctk.CTkToplevel(self.app)
        self.admin_frame.title("Admin")
        self.admin_frame.geometry("500x500")
        self.admin_frame.protocol("WM_DELETE_WINDOW", self.on_close)

        # Displaying the current user in the top
        self.curr_user = ctk.CTkLabel(self.admin_frame, text=self.username.get())
        self.curr_user.pack(pady=8, padx=4)

        # Adjust roles button
        self.adjust_roles = ctk.CTkButton(self.admin_frame, text="User Roles", command=self.user_roles)
        self.adjust_roles.pack(pady=8, padx=4)

        # Add courses button
        self.add_course = ctk.CTkButton(self.admin_frame, text="Add Course")
        self.add_course.pack(pady=8, padx=4)

        # Logout button
        self.logout_adm = ctk.CTkButton(self.admin_frame, text="Logout", command=self.logout)
        self.logout_adm.pack(pady=8, padx=4)

    # ADMIN METHODS
    def user_roles(self):  # Admin Method to adjust users roles
        # Get a list of all the users
        users = self.db_manager.get_all_users()
        # List of the roles to give a user
        roles = ["Select a role", "user", "admin"]
        # Drop down menu for them to select a user
        users.insert(0, "Select a user")

        # Setting the box to default display "Select a user"
        self.selected_option = tk.StringVar(self.admin_frame)
        self.selected_option.set("Select a user")

        # Style for the drop-down menu
        option_menu_style = ttk.Style()
        option_menu_style.configure("Custom.TMenubutton", background="grey", padding=5)
        option_menu_style.configure("Custom.TMenubutton.TButton", relief="flat")

        # Setting the style for the drop-down menu
        option_menu = ttk.OptionMenu(self.admin_frame, self.selected_option, *users, style="Custom.TMenubutton")
        option_menu.pack(pady=8, padx=4)

        # Event when they click the option it updates the drop-down
        option_menu.bind("<ButtonRelease-1>", lambda event, arg=self.selected_option: self.on_option(event, arg))

        self.role_type = tk.StringVar(self.admin_frame)
        self.role_type.set("Select a role")

        # Styling for the drop-down menu
        option_menu_style = ttk.Style()
        option_menu_style.configure("Custom.TMenubutton", background="grey", padding=5)
        option_menu_style.configure("Custom.TMenubutton.TButton", relief="flat")

        # Setting the style for the drop-down menu
        option_menu = ttk.OptionMenu(self.admin_frame, self.role_type, *roles, style="Custom.TMenubutton")
        option_menu.pack(pady=8, padx=4)

        # Event when they click the option it updates the drop-down
        option_menu.bind("<ButtonRelease-1>",
                         lambda event, arg=self.role_type: self.on_option(event, arg))

        # Button to submit the updated role to the user they selected
        self.update_btn = ctk.CTkButton(self.admin_frame, text="Update", command=self.update_role)
        self.update_btn.pack(pady=8, padx=4)

    def update_role(self):  # Method to update the users role
        username = self.selected_option.get()
        role = self.role_type.get()

        updated = self.db_manager.user_roles(role, username)
        if updated:
            messagebox.showinfo("Success", "users role has been updated")
        else:
            messagebox.showerror("Error", "idk something happened")

    def add_course(self):  # Admin Method to add a course
        pass

    # USER METHODS

    def play_golf(self):  # User method to play a round of golf
        pass

    def golf_rounds(self):  # User method to check out past rounds of golf
        pass

    def golf_sim(self):  # User method to go into the golf simulator
        pass

    def swing_analysis(self):  # User method to get into the swing analysis
        pass

    def fitness_golf(self):  # User method to get into the fitness portion
        pass

    def golf_insights(self):  # User method to get into tips/ insight of their golf game
        pass

    # Method to logout from the program
    def logout(self):
        if self.admin_frame:
            self.admin_frame.withdraw()
            self.admin_frame = None
        elif self.main_frame:
            self.main_frame.withdraw()
            self.main_frame = None

        self.initialize_gui()

