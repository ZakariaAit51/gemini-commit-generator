# Gemini Commit Message Generator

This project integrates the Gemini API to automatically generate concise and meaningful Git commit messages based on **staged** changes.

## Features

- Extracts **only staged** changes (`git diff --staged`).
- Uses **Gemini AI** to generate a commit message.
- Displays the suggested commit message before committing.
- Provides an optional `--use` flag to display API token usage and general info.

---

## Installation & Setup

### **1. Clone the Repository**

```sh
git clone [https://github.com/yourusername/gemini-commit.git]
cd gemini-commit
```

### **2. Create a Virtual Environment (Recommended)**

```sh
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### **3. Install Dependencies**

```sh
pip install -r requirements.txt
```

### **4. Set Up API Key**

Create a `.env` file in the project root and add your Gemini API key:

```ini
GEMINI_API_KEY=your-secret-api-key
```

Alternatively, use a **global** `.env` file:

```sh
echo "GEMINI_API_KEY=your-secret-api-key" > ~/.gemini_commit.env
```

---

## Usage

### **Generate a Commit Message**

```sh
python gemini_commit.py
```

This will:

- Get the **staged changes**.
- Generate a commit message.
- Display the message before committing.

### **Check API Token Usage**

```sh
python gemini_commit.py --use
```

This will **not** generate a commit message but instead display:

- Used tokens
- Total available tokens
- Other general API info

### **Make It a Global Command** (Optional)

For convenience, you can move the script to `/usr/local/bin`:

```sh
chmod +x gemini_commit.py
mv gemini_commit.py /usr/local/bin/gemini-commit
```

Now, you can run:

```sh
gemini-commit
```

from anywhere!

---

## **Convert to Standalone Executable (Optional)**

To avoid needing Python and dependencies, you can create a standalone executable:

```sh
pip install pyinstaller
pyinstaller --onefile gemini_commit.py
```

The output file will be in `dist/gemini_commit`.
Move it to `/usr/local/bin` for global access:

```sh
mv dist/gemini_commit /usr/local/bin/gemini-commit
chmod +x /usr/local/bin/gemini-commit
```

---

## **Troubleshooting**

- If the API key is not recognized, ensure the `.env` file exists and is formatted correctly.
- If the script does not detect changes, make sure you have **staged** files (`git add .`).
- If using the standalone version, ensure you have the `.env` file in the correct location (`~/.gemini_commit.env` or project root).

---

## **License**

MIT License. Feel free to modify and use it as needed!

---

### **Author**

[Zakariyae](https://github.com/ZakariaAit51)

---
