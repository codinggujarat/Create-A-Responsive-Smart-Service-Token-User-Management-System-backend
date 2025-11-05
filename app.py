# Simple wrapper to make the app accessible at the root level for Render
from backend.app import app

if __name__ == "__main__":
    app.run()