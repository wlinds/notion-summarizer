# Notion-Summarizer

Python app to fetch a table from Notion, convert it to Excel and email it along with a visualization. Can be used to email notes, expenses, work schedules or any other table or database.

The default behavior of this app emails the previous week's data from a given table/db.

**At least one column with datetime type is mandarory for default settings.**

### Setup

0. Clone this repo.

1. Create a **[Notion integration](https://www.notion.so/profile/integrations)** and generate a token (secret).

2. In you Notion app or browser, click on the `...` More menu in the top-right corner of the page, scroll down to `+` Add Connections. Search for your integration and select it.

3. Get your **database ID**, this can be found in the URL. If your URL looks like below, then <long_hash_1> is the database ID and <long_hash_2> is the view ID. <br>```https://www.notion.so/<long_hash_1>?v=<long_hash_2>```
    

4. In this directory, create a `.env` and add paset the text below, make sure to replace with actual values:
```
NOTION_TOKEN = YOUR_NOTION_TOKEN/SECRET
DB_ID = YOUR-DATABASE-ID
EMAIL_APP_PASSWORD = YOUR-EMAIL-APP-PASSWORD
```

5. Create a `email-details.json` in /src folder. Paste the following and replace details:

```
{
    "sender" : "alice@gmail.com",
    "receiver" : "bob@gmail.com",
    "subject" : "Your Weekly Report -",
    "body" : "Hiya! Here's your report. Best regards, 🐹.",
    "file_name" : "this_is_a_filename_no_extension_needed"
}
```

6. Install dependencies and run `main.py` manually or schedule it with a cronjob.

---


⚠️ If your using a **gmail account** you have to generate a new app password:

1. Go to your Google Account.
2. On the left navigation panel, choose Security.
3. On the 'Signing in to Google' panel, choose App passwords.
4. At the bottom, choose Select app.
5. Choose Select device and choose the device that you're using.
6. Choose Generate.