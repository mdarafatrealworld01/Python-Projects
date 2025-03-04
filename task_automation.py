# Required modules
import os
import shutil
import smtplib
import schedule
import time
import pyautogui
import getpass  # Securely input email password

# Function to organize files in a specified directory
def organize_files(directory):
    try:
        if not os.path.exists(directory):
            print(f"Directory '{directory}' not found!")
            return

        # Create folders if they don't exist
        for folder in ['Images', 'Documents', 'Videos']:
            os.makedirs(os.path.join(directory, folder), exist_ok=True)

        # Move files to corresponding folders
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)

            if os.path.isfile(filepath):
                if filename.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                    shutil.move(filepath, os.path.join(directory, 'Images', filename))
                elif filename.endswith(('.pdf', '.docx', '.txt')):
                    shutil.move(filepath, os.path.join(directory, 'Documents', filename))
                elif filename.endswith(('.mp4', '.mkv')):
                    shutil.move(filepath, os.path.join(directory, 'Videos', filename))

        print("Files organized successfully.")
    except Exception as e:
        print(f"Error in organizing files: {e}")

# Function to send an automated email
def send_email(subject, body, to_email):
    try:
        from_email = "your_email@example.com"
        password = getpass.getpass("Enter your email password: ")  # Secure input

        message = f'Subject: {subject}\n\n{body}'

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(from_email, password)
            server.sendmail(from_email, to_email, message)

        print("Email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")

# Function to automate GUI task
def automate_gui_task():
    try:
        pyautogui.hotkey('win', 'r')  # Open Run dialog
        time.sleep(1)
        pyautogui.typewrite('notepad\n', interval=0.1)  # Open Notepad
        time.sleep(1)
        pyautogui.typewrite('Hello, this is an automated message!', interval=0.1)  # Type message
        print("GUI task executed successfully.")
    except Exception as e:
        print(f"Error in GUI automation: {e}")

# Schedule tasks
schedule.every().day.at("10:00").do(organize_files, directory='C:/path/to/your/directory')
schedule.every().day.at("10:05").do(send_email, subject='Daily Report', body='Files have been organized.', to_email='recipient@example.com')
schedule.every().day.at("10:10").do(automate_gui_task)

# Run the scheduled tasks in a loop with error handling
try:
    print("Task automation system running... (Press Ctrl+C to stop)")
    while True:
        schedule.run_pending()
        time.sleep(1)
except KeyboardInterrupt:
    print("\n Task automation system stopped by user.")
