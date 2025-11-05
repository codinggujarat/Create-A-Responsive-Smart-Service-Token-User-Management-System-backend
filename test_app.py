import os
import sys

# Add the current directory to the Python path
sys.path.insert(0, os.path.abspath('.'))

try:
    from backend.app import create_app
    print("Import successful!")
    
    # Create the app
    app = create_app()
    print("App created successfully!")
    
    # Test the app context
    with app.app_context():
        print("App context created successfully!")
        
    print("All tests passed!")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()