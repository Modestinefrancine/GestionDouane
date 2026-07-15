# main.py
from database import initialiser_db
from gui import lancer_interface

if __name__ == "__main__":
    initialiser_db()        
    lancer_interface()