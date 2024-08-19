import os, sys, json, time
from datetime import datetime as dt

from api import *
from utils import get_email_details, get_df, cleanup_files
from send_mail import compose_and_send
from model import get_basic_summary

USE_LOCAL_LLM = False

def generate_report(data, datetime_col, plot_type, file_name):
    df, plot = get_df(data, datetime_col, plot_type)

    if plot:
        plot.savefig(file_name + ".png")

    df.to_excel(file_name + ".xlsx", index=False)

    return [file_name + ".xlsx", file_name + ".png"] if plot else [file_name + ".xlsx"]


def main():
    start_timer = time.time()
    datetime_col = "Time"
    email_details = get_email_details()
    email_details["week"] = dt.now().isocalendar()[1]

    file_name = f"{email_details['file_name']}_{email_details['week']}"
    data = fetch(DB_ID, get_payload(property_name=datetime_col, week="past_week"))

    if not data: return
    
    clean_data = process_data(data)
    attachments = generate_report(clean_data, datetime_col, "schedule", file_name)

    if USE_LOCAL_LLM:
        email_details['body'] += get_basic_summary(clean_data, "Note")

    email_details['elapsed'] = time.time() - start_timer

    if compose_and_send(email_details, attachments):
        cleanup_files(attachments)


if __name__ == "__main__":
    load_dotenv()
    main()