import subprocess
import threading
import time


def run_background():
    try:
        # Popen runs the process without blocking
        process = subprocess.Popen(
            ["uvicorn", "web_server.api_call:app", "--host", "127.0.0.1", "--port", "8000"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print("Backend server started successfully")
        process.wait()  # Keeps the thread alive by waiting for the process to finish
    except Exception as e:
        print(f"An error occurred while running the backend: {e}")

    
def run_frontend():
    try:
        # Popen runs the process without blocking
        process = subprocess.Popen(
            ["streamlit", "run", "Frontend/main.py"],
            stdout=subprocess.PIPE,# Captures normal output
            stderr=subprocess.PIPE # Captures error messages
        )
        print("Frontend server started successfully")
        process.wait()  # Keep the thread alive
    except Exception as e:
        print(f"An error occurred while running the frontend: {e}")

    
if __name__ == "__main__":
    # Start backend in a separate thread
    t1 = threading.Thread(target=run_background, daemon=True)
    t1.start()
    
    # Wait for backend to start
    time.sleep(3)
    
    # Start frontend (runs in main thread)
    run_frontend()


# subprocess.Popen() instead of subprocess.run() - Starts 
# the process without blocking
# daemon=True for the backend thread - Ensures it closes when the main program exits
# Increased sleep time to 3 seconds - Gives the backend more time to initialize
# Added print statements - So you can see when servers start
# Fixed typo - run_backround → run_background


# stdout = Standard Output (normal messages, logs, print statements)
# stderr = Standard Error (error messages, warnings)
# PIPE = Special tunnel that captures this output so you can read it in Python