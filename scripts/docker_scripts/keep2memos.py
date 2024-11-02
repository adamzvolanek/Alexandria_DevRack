import argparse
from datetime import datetime
import requests
import os
import json

DEFAULT_TAKEOUT_FOLDER = "Takeout/keep"
INSTANCE = ""
TOKEN = ""

def timestamp_to_date(microseconds):
    return datetime.fromtimestamp(microseconds / 1e6).strftime('%Y-%m-%dT%H:%M:%SZ')

def array_to_markdown_checklist(items):
    checklist = []
    for item in items:
        checkbox = "[x]" if item["isChecked"] else "[ ]"
        checklist.append(f"- {checkbox} {item['text']}")
    return "\n".join(checklist)

def post_memo(content):
    url = INSTANCE + "/api/v1/memos"
    
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "content": content,
        "visibility": "VISIBILITY_PRIVATE"
    }

    try:
        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            try:
                responseData = response.json()
            except ValueError:
                print("Error : No valid return from API, check url and token")
                return
            memoId = responseData.get("name", "").split('/')[1]
            print("Memo posted successfully:", memoId)
            return memoId
        else:
            print(f"Failed to post memo. Status code: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def patch_memo(id, date, archived):
    url = f"{INSTANCE}/api/v1/memos/{id}"
    
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }
    status = "ACTIVE"
    if(archived):
        status = 'ARCHIVED'
    
    data = {
        "rowStatus": status,
        "createTime": date
    }

    try:
        response = requests.patch(url, json=data, headers=headers)

        if response.status_code == 200:
            print("Memo patched successfully")
        else:
            print(f"Failed to patch memo. Status code: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def process_json_files_in_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)

            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                
                title = data.get("title", "No Title")
                text_content = data.get("textContent", "")
                if(text_content == ""):
                    text_content = array_to_markdown_checklist(data.get("listContent", ""))
                created_timestamp_usec = data.get("createdTimestampUsec", 0)
                archived = data.get("isArchived",False)

                date = timestamp_to_date(created_timestamp_usec)
                memo_content = "";

                if(title):
                    memo_content = f"## {title}\n"
                memo_content += f"{text_content}"
                memoId = post_memo(memo_content)
                if(memoId):
                    patch_memo(memoId,date,archived)
# Define the argument parser
def get_args():
    parser = argparse.ArgumentParser(description="Process JSON files with Memos API.")
    parser.add_argument('--instance', required=True, help="Your Memos instance URL")
    parser.add_argument('--token', required=True, help="Your API token")
    parser.add_argument('--folder', default=DEFAULT_TAKEOUT_FOLDER, help="Folder containing JSON files")
    return parser.parse_args()


def main():
    args = get_args()

    # Use the instance and token from command line arguments
    globals()["INSTANCE"] = args.instance
    globals()["TOKEN"] = args.token
    globals()["DEFAULT_TAKEOUT_FOLDER"] = args.folder

    print(f"Processing instance: {INSTANCE}")
    print(f"Using token: {TOKEN}")
    
    # Process the folder
    process_json_files_in_folder(DEFAULT_TAKEOUT_FOLDER)
    print('Import successful !')

if __name__ == "__main__":
    main()
