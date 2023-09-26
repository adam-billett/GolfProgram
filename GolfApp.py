import tkinter as tk
from GUIManager import GUIManager
from DatabaseManager import DatabaseManager

def main():
    golf = tk.Tk()
    db_manager = DatabaseManager("GolfApp", "postgres", "Bearcat", "localhost", "5432")
    app_gui = GUIManager(golf, db_manager)
    golf.mainloop()

if __name__ == "__main__":
    main()