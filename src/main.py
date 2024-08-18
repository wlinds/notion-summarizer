import os, sys, json, time, datetime

from api import *
from utils import get_email_details, get_df
from send_mail import write_email

load_dotenv()

def main():
    start_timer = time.time()
    
    datetime_col = "Time"
    ed = get_email_details()
    ed['week'] = datetime.datetime.now().isocalendar()[1] - 1
    file_name = f"{ed['file_name']}_{ed['week']}" # Adjusted filename to past week

    data = fetch(DB_ID, get_payload(property_name=datetime_col, week="past_week"))

    if data:
        formatted_rows = process_data(data)
    else: return

    df, plot = get_df(formatted_rows, datetime_col, "schedule")

    if plot:
        plot.savefig(file_name+".png")

    df.to_excel(file_name+".xlsx", index=False)

    attachments = [file_name+".xlsx", file_name+".png"] if plot else file_name+".xlsx"

    ed['elapsed'] = time.time() - start_timer
    if write_email(ed, attachments, is_html=True) == True:
        print(f"""• Notion-Summarizer | {datetime.datetime.now()} | Email "{ed['subject']} {ed['week']}" successfully sent to {ed['receiver']}.""")

        try:
            os.remove(file_name+".xlsx")
            if plot:
                os.remove(file_name+".png")
        except OSError as e:
            print(f"Error deleting file: {e}")
    else:
        print("Could not send email. Files have been saved locally instead.")


if __name__ == "__main__":
    main()