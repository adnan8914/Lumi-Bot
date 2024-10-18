import sys
import os

# Add the project directory to the Python path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

from chatbot.main import run_chatbot

if __name__ == "__main__":
    run_chatbot()
