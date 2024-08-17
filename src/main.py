import os, sys, json, time, datetime

from api import *
from utils import get_current_week, get_email_details, get_df
from send_mail import write_email

load_dotenv()

def main():
    start_timer = time.time()
    ed = get_email_details()
    ed['week'] = get_current_week()-1

    temp_file = f"{ed['file_name']}_{ed['week']}"

    payload = get_payload(week="past_week")
    data = fetch(DB_ID, payload)
    formated_rows = process_data(data)
    df, plot = get_df(formated_rows, "Time", "schedule")

    if plot:
        plot.savefig(temp_file+".png")

    df.to_excel(temp_file+".xlsx", index=False)

    elapsed = time.time() - start_timer

    attachments = [temp_file+".xlsx", temp_file+".png"] if plot else temp_file+".xlsx"

    if write_email(ed['sender'],
                ed['receiver'],
                f"{ ed['subject']} {ed['week']}",
                f"""<p>{ed['body']}</p><br>
                <p style='font-family: Courier, sans-serif; font-size: 10px;'>
                Report fetched {datetime.datetime.now()} and sent in {elapsed:.3f} seconds.<br>
                Source Code: <a href='https://github.com/wlinds/notion-summarizer'>wlinds/notion-summarizer</a></p>""", 
                attachments, is_html=True) == True:
        print(f"""• Notion-Summarizer | {datetime.datetime.now()} | Email "{ed['subject']} {ed['week']}" successfully sent to {ed['receiver']}.""")

        try:
            os.remove(temp_file+".xlsx")
            if plot:
                os.remove(temp_file+".png")
        except OSError as e:
            print(f"Error deleting file: {e}")
    else:
        print("Could not send email. Files have been saved locally instead.")


if __name__ == "__main__":
    main()