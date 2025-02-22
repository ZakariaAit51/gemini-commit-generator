import google.generativeai as genai
import subprocess
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from .env
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

def get_staged_diff():
    """Get the diff of only staged changes."""
    try:
        diff = subprocess.check_output(["git", "diff", "--staged"], universal_newlines=True)
        return diff.strip()
    except subprocess.CalledProcessError:
        return ""

def generate_commit_message(diff):
    """Use Gemini API to generate a commit message based on the diff."""
    if not diff:
        print("No staged changes found.")
        return None

    prompt = f"Generate a concise and meaningful Git commit message for the following staged changes:\n\n{diff}"

    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    
    return response.text.strip() if response.text else "Auto-generated commit message."

def main():
    """Main function to generate and display the commit message."""
    diff = get_staged_diff()
    
    if not diff:
        print("No staged changes to commit.")
        return
    
    commit_message = generate_commit_message(diff)
    
    if commit_message:
        print("\nSuggested Commit Message:\n")
        print(commit_message)
        print("\nTo use it, run:\n")
        print(f'git commit -m "{commit_message}"')

if __name__ == "__main__":
    main()
