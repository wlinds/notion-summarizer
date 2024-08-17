import os
import json
import pandas as pd
import datetime

from plots import get_plot

# TODO Add error handling for property "Time" missing 
def get_payload(property_name="Time", week="past_week"):
    payload = {
    "filter": {
        "property": property_name,
        "date" : { week : {} }}}

    return payload

def get_current_week():
    return datetime.datetime.now().isocalendar()[1]

def get_email_details(json_file_path=None):
    default_path = os.path.join(os.path.dirname(__file__), "email-details.json")
    file_path = json_file_path if json_file_path else default_path

    try:
        with open(file_path, 'r') as f:
            email_details = json.load(f)
        if not all(key in email_details for key in ['sender', 'receiver', 'subject', 'body', 'file_name']):
            raise KeyError(f"The JSON {file_path} must contain 'sender', 'receiver', 'subject', 'body' and 'file_name' keys.")
    
    except FileNotFoundError:
        print(f"Error: {file_path} was not found.")
        return {}
    except json.JSONDecodeError:
        print("Error: The file is not a valid JSON file.")
        return {}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {}

    return email_details

def get_df(csv, column_name):
    # df = pd.read_csv(csv)
    df = pd.DataFrame(csv)
    
    start_end_times = df[column_name].str.split(' -> ', expand=True)
    
    start_times = pd.to_datetime(start_end_times[0])
    end_times = pd.to_datetime(start_end_times[1])


    df['StartDate'] = start_times.dt.day
    df['StartMonth'] = start_times.dt.month
    df['StartYear'] = start_times.dt.year
    df['StartTime'] = start_times.dt.strftime('%H:%M')
    df['EndDate'] = end_times.dt.day
    df['EndMonth'] = end_times.dt.month
    df['EndYear'] = end_times.dt.year
    df['EndTime'] = end_times.dt.strftime('%H:%M')
    
    plot = get_plot(df, start_times, end_times)
    df.drop(columns=["StartDateTime", "EndDateTime", "Duration", "Day", "y" ])

    df = df.drop(columns=[column_name])

    column_order = ['Customer', 'Tags', 'StartDate', 'StartMonth', 'StartYear', 'StartTime', 'EndDate', 'EndMonth', 'EndYear', 'EndTime', 'Note', 'Tim']
    df = df[column_order + [col for col in df.columns if col not in column_order]]

    df = df.sort_values(by=['StartYear', 'StartMonth', 'StartDate', 'StartTime'])
    
    return df, plot


if __name__ == "__main__":
    email_dict = get_email_details()
    email_dict['week'] = get_current_week()-1
    print(email_dict)
    print(email_dict['sender'][-9::])