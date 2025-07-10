"""
Entry point for MatcomFunctionLab application.

Run this file to start the application.
"""

if __name__ == "__main__":
    try:
        from Interface.App import main
        main()
    except ImportError as e:
        print(f"Error importing modules: {e}")
        print("Please ensure all dependencies are installed by running:")
        print("pip install -r requirements.txt")
    except Exception as e:
        print(f"Error running application: {e}")
