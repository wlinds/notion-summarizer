import os
import requests
import json
import pandas as pd
from dotenv import load_dotenv
import datetime
from pathlib import Path

load_dotenv()

NOTION_API_BASE_URL = "https://api.notion.com/v1/"
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DB_ID = os.getenv("DB_ID")

def get_payload(property_name="Time", week="past_week"):
    """
    Constructs a payload to filter the query.
    - property_name: Column name with datetime object(s). Can include end_time.
    - week: Valid arguments: "past_week" or "next_week"
    """

    payload = {
                "filter": {
                "property": property_name,
                "date" : { week : {} }}
    }

    return payload


def get_headers(NOTION_TOKEN):
    return {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }


def fetch(database_id, payload = {}):
    if not (Path(__file__).parent.parent / ".env").exists():
    
        print(".env file not found! Create an .env and enter values for NOTION_TOKEN, DB_ID, EMAIL_APP_PASSWORD")
        return None

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
    pass