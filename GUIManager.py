import customtkinter as ctk
from tkinter import messagebox
class GUIManager:
    def __init__(self, app, db_manager):
        self.app = app
        self.db_manager = db_manager

        self.initialize_gui()

    def initialize_gui(self):
        pass
