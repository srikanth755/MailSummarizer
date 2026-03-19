# MailSummarizer

A Python script that connects to the Gmail API to retrieve and read your recent or filtered emails.

## Prerequisites

- **Python 3.x** installed on your system.
- A **Google Cloud Platform** account.
- A basic understanding of your operating system's terminal/command prompt.

## Setup Instructions

### 1. Google Cloud API Setup
You need to authenticate with Google to access your Gmail account.

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project (e.g., "MailSummarizer").
3. Navigate to **APIs & Services > Library** and enable the **Gmail API**.
4. Navigate to **APIs & Services > OAuth consent screen**:
   - Choose **External** (or Internal if you have a Google Workspace).
   - Fill in the required app information.
   - Add your email address as a "Test User".
5. Navigate to **APIs & Services > Credentials**:
   - Click **Create Credentials > OAuth client ID**.
   - Select **Desktop app** as the application type.
   - Click **Create**.
   - Download the JSON file, rename it to **`credentials.json`**, and place it in the root folder of this project (`MailSummarizer/credentials.json`).

### 2. Python Environment Setup

It is recommended to use a virtual environment to manage dependencies.

**Open your terminal and navigate to the project directory:**
```powershell
cd /path/to/MailSummarizer
```

**Create and activate the virtual environment:**
```powershell
# Create a virtual environment named "MS"
python -m venv MS

# Activate it (Windows)
.\MS\Scripts\activate

# Activate it (Mac/Linux)
# source MS/bin/activate
```

### 3. Install Dependencies

With the virtual environment activated, install the required Google API Python libraries:

```powershell
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

## Running the Script

Once the setup is complete, you can run the application.

```powershell
python GetMessages.py
```

### First Run (Authentication)
The first time you run the script:
1. A new browser window will open asking you to log in to your Google Account.
2. It will warn you that the app is unverified (since you just created it). Click **Advanced** and then **Go to [App Name]**.
3. Grant the required permissions (read emails).
4. You can close the browser window. The script will automatically save a `token.json` file in your project directory so you don't have to log in every time.

## Customizing the Target Emails

Open `GetMessages.py` and modify the bottom section under `if __name__ == '__main__':` to change what emails are fetched:
- Un-comment `list_recent_messages()` to print your 10 most recent emails.
- Change the query string in `list_filtered_messages('from:notifications@github.com')` to fetch emails matching standard Gmail search syntax (e.g., `is:unread`, `subject:urgent`).
