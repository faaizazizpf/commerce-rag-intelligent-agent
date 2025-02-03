import logging
from datetime import datetime, timedelta
import pytz
import csv
# Set Pakistani timezone
# PAKISTAN_TZ = pytz.timezone('Asia/Karachi')

# Function to get current time in the required format
def get_pakistan_time():
    PAKISTAN_TZ = pytz.timezone('Asia/Karachi')
    now = datetime.now(PAKISTAN_TZ) + timedelta(minutes=20)
    return now.strftime("%d/%m/%Y %I:%M:%S.%f %p")  # Format: 13/10/2024 4:45:02.123456 pm

def get_pakistan_time_for_file():
    PAKISTAN_TZ = pytz.timezone('Asia/Karachi')
    now = datetime.now(PAKISTAN_TZ) + timedelta(minutes=20)
    return now.strftime("%d_%m_%Y_%I_%M")  # Format: 13/10/2024 4:45:02.123456 pm

# Logging configuration
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt="%d/%m/%Y %I:%M:%S.%f %p",
    handlers=[
        logging.FileHandler("server_debug.log"),  # Log to file
        logging.StreamHandler()  # Log to terminal/console
    ]
)

# Log example with custom time format
def log_with_pakistan_time(message):
    current_time = get_pakistan_time()
    logging.info(f"[{current_time}] {message}")

def write_history_csv(messages, query_,full_response):

    with open(f"logs/logs_{get_pakistan_time_for_file()}.csv", "a+", newline='', encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile)
        
        # Check if the file is empty to write headers
        if csvfile.tell() == 0:
            csv_writer.writerow(["Message Index", "Timestamp", "Role", "Content"])
        
        # Log the history being sent to the model
        log_with_pakistan_time("Logging History")
        
        for i, message in enumerate(messages):
            timestamp = get_pakistan_time()
            role = message["role"]
            content = message["content"]
            csv_writer.writerow([i, timestamp, role, content])  # Write each message as a row
        
        # Log the query and response
        csv_writer.writerow(["Q", get_pakistan_time(), "user", query_])
        csv_writer.writerow(["R", get_pakistan_time(), "assistant", full_response])
