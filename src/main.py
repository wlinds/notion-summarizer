import os
import sys
import json
import time
import datetime

from api import *
from utils import get_current_week, get_email_details
from send_mail import write_email

def main():
    time_now = datetime.datetime.now()
    start_timer = time.time()
    ed = get_email_details()
    ed['week'] = get_current_week()-1
    formatted_start_date = datetime.date.fromisocalendar(datetime.datetime.now().year, ed['week'], 1)
    
    # TODO Add error handling for property "Time" missing 
    payload = {
    f"filter": {
        "property": "Time",
        "date": {
        "on_or_after": str(formatted_start_date)
        }
    }
    }

    data = fetch(DB_ID, payload)
    formated_rows = process_data(data)
    df = format_excel(formated_rows, "Time")

    temp_file = f"{ed['file_name']}_{ed['week']}.xlsx"
    df.to_excel(temp_file, index=False)

    elapsed = time.time() - start_timer

    write_email(ed['sender'], ed['receiver'], f"{ ed['subject']} {ed['week']}", f"<p>{ed['body']}</p><br> <p style='font-family: Courier, sans-serif; font-size: 10px;'>Report fetched {time_now} and sent in {elapsed:.3f} seconds.</p>", temp_file, is_html=True)

    # format_email(ed['sender'], ed['receiver'], f"{ed['subject'], {ed['week']} } {sys.getsizeof(temp_file)}" + f" V.{ed['week']}", f"<p>{ed['body']}</p><br> <p style='font-family: Courier, sans-serif; font-size: 10px;'>Report fetched {time_now} and sent in {elapsed:.3f} seconds.</p>", temp_file, is_html=True)



    try:
        os.remove(temp_file)
    except OSError as e:
        print(f"Error deleting file: {e}")
    
    print(f"Email successfully sent.")

if __name__ == "__main__":
    main()