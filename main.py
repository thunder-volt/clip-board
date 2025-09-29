import pyperclip
import time
from datetime import datetime
from git import Repo
import os

# --- Config ---
REPO_PATH = r'C:\Users\ishu1\OneDrive\Documents\Cheating_tool'  # Local clone of your GitHub repo
FILE_NAME = 'log.md'                   # Markdown file to append clipboard
GIT_COMMIT_MSG = 'Update clipboard log'
BATCH_INTERVAL = 10                    # Seconds to batch clipboard entries

# Initialize repo
if not os.path.exists(REPO_PATH):
    raise Exception(f"Repo path does not exist: {REPO_PATH}")

repo = Repo(REPO_PATH)
file_path = os.path.join(REPO_PATH, FILE_NAME)

# Track last text to avoid duplicates
last_text = ''
batch = []

print("Monitoring clipboard... Press Ctrl+C to stop.")

while True:
    try:
        text = pyperclip.paste().strip()
        if text and text != last_text:
            last_text = text
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            batch.append(f"- [{timestamp}] {text}")
            print(f"[{timestamp}] Queued: {text}")

        # If batch interval passed, write and push
        if batch and (time.time() % BATCH_INTERVAL < 1):
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write('\n'.join(batch) + '\n')

            # Commit and push
            repo.git.add(FILE_NAME)
            repo.index.commit(GIT_COMMIT_MSG)
            repo.git.push()
            print(f"Pushed {len(batch)} entries to GitHub.")

            batch = []

        time.sleep(1)

    except KeyboardInterrupt:
        # Push remaining entries before exit
        if batch:
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write('\n'.join(batch) + '\n')
            repo.git.add(FILE_NAME)
            repo.index.commit(GIT_COMMIT_MSG)
            repo.git.push()
            print(f"Pushed remaining {len(batch)} entries to GitHub.")
        print("Stopped monitoring.")
        break
    except Exception as e:
        print("Error:", e)
        time.sleep(5)
