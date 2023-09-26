import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox


class GUIManager:
    def __init__(self, app, db_manager):
        self.app = app
        self.db_manager = db_manager

        self.initialize_gui()

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
            print(self.current_user_role)
            if self.current_user_role == "admin":
                messagebox.showinfo("Welcome admin")
                # Display admin menu
                pass
            elif self.current_user_role == "user":
                messagebox.showinfo("Welcome user")
                pass
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
    def main_menu(self):
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
        self.logout_btn = ctk.CTkButton(self.main_frame, text="Logout", command=self.logout)
        self.logout_btn.pack(pady=8, padx=4)

    # Method to logout from the program
    def logout(self):
        self.main_frame.withdraw()

        self.initialize_gui()