import os
import requests
import json
import pandas as pd
from dotenv import load_dotenv
import datetime

from utils import get_current_week, format_excel

load_dotenv()

NOTION_API_BASE_URL = "https://api.notion.com/v1/"
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DB_ID = os.getenv("DB_ID")


def get_headers(NOTION_TOKEN):
    return {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }


def fetch(database_id, payload = {}):
    url = f"{NOTION_API_BASE_URL}databases/{database_id}/query"

    try:
        response = requests.post(url, headers=get_headers(NOTION_TOKEN), json=payload)
        response.raise_for_status()
        data = response.json()
        return data

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err} - {response.text}")
    except Exception as err:
        print(f"Other error occurred: {err}")
    return None


def process_data(data):
    all_rows = []
    if data and "results" in data:
        for row in data["results"]:
            properties = row["properties"]
            row_data = {}
            for column, value in properties.items():
                row_data[column] = value_processor(value)
            all_rows.append(row_data)

    return all_rows


def value_processor(value):
    if value["type"] == "title":
        return " ".join([t["plain_text"] for t in value["title"]])

    elif value["type"] == "rich_text":
        return " ".join([t["plain_text"] for t in value["rich_text"]])

    elif value["type"] == "multi_select":
        return ", ".join([opt["name"] for opt in value["multi_select"]])

    elif value["type"] == "date":
        start_date = value["date"]["start"]
        end_date = value["date"].get("end", "")
        return f"{start_date} -> {end_date}" if end_date else start_date

    elif value["type"] == "formula":
        return value["formula"][value["formula"]["type"]]

    else:
        return value[value["type"]]


if __name__ == "__main__":
    previous_week_start = datetime.date.fromisocalendar(datetime.datetime.now().year, get_current_week()-1, 1)
    
    payload = {
    f"filter": {
        "property": "Time",
        "date": {
        "on_or_after": str(previous_week_start)
        }
    }
    }
    

    all_data = fetch(DB_ID, payload)
    all_rows = process_data(all_data)
    df = pd.DataFrame(all_rows)
    # df.to_csv(os.path.join(os.getcwd(), "notion.csv"), index=False)

    df2 = format_excel(all_rows, "Time")
