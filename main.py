import os
import google.generativeai as genai
import subprocess
import argparse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key and token limit
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TOKEN_LIMIT = int(os.getenv("GEMINI_TOKEN_LIMIT", 0))

if not GEMINI_API_KEY:
    print("Error: GEMINI_API_KEY is not set. Add it to the .env file.")
    exit(1)

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

def get_api_usage():
    """Retrieve API usage details."""
    try:
        model = genai.GenerativeModel("gemini-pro")
        # Use a more realistic prompt for token estimation.  "test" is too short.
        response = model.count_tokens("This is a more realistic example prompt for token counting.")
        tokens_used = response['totalTokens']

        print("\n🔍 Gemini API Usage Info:")
        print(f"📌 Tokens used in this request: {tokens_used}")

        if TOKEN_LIMIT > 0:
            tokens_remaining = TOKEN_LIMIT - tokens_used
            usage_percentage = (tokens_used / TOKEN_LIMIT) * 100
            print(f"💳 Total token quota: {TOKEN_LIMIT}")
            print(f"⏳ Tokens used: {tokens_used}/{TOKEN_LIMIT} ({usage_percentage:.2f}%)")
            print(f"✅ Tokens remaining: {tokens_remaining}\n")
        else:
            print("⚠️ No total limit set. Add 'GEMINI_TOKEN_LIMIT' to .env for tracking.\n")

    except Exception as e:
        print("⚠️ Error fetching API usage info:", str(e))


def get_staged_diff():
    """Get the diff of only staged changes."""
    try:
        # Add --no-ext-diff to avoid potentially very long diffs from binary files
        diff = subprocess.check_output(["git", "diff", "--staged", "--no-ext-diff"], universal_newlines=True)
        return diff.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error getting staged diff: {e}") # Print the specific error
        return ""  # Return empty string instead of None


def generate_commit_message(diff):
    """Use Gemini API to generate a commit message based on the diff."""
    if not diff:
        print("No staged changes found.")
        return None

    # More specific prompt for better commit messages
    prompt = f"""Generate a concise and informative Git commit message (under 72 characters if possible) for the following staged changes:\n\n```diff
{diff}
```\n\nFollow conventional commits format.  Consider the type of change (feat, fix, chore, etc.) and use a descriptive summary."""

    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        commit_message = response.text.strip() if response.text else "Auto-generated commit message."

        # Validate and improve the generated message (optional but recommended)
        if not commit_message.startswith(("feat", "fix", "chore", "docs", "style", "refactor", "test", "build", "ci")):
            print("Warning: Commit message does not follow conventional commits format. Consider adding a type prefix (feat, fix, chore, etc.).")

        if len(commit_message) > 72:
            print(f"Warning: Commit message exceeds 72 characters: {len(commit_message)}.  Consider shortening it.")
            # You could add some logic here to attempt to automatically shorten it.

        return commit_message

    except Exception as e:
        print(f"Error generating commit message: {e}")
        return None


def main():
    """Main function with CLI argument handling."""
    parser = argparse.ArgumentParser(description="Generate AI-powered commit messages or check API usage.")
    parser.add_argument("--use", action="store_true", help="Show API usage info and exit.")
    parser.add_argument("--amend", action="store_true", help="Amend the last commit with the generated message.") # New option
    args = parser.parse_args()

    if args.use:
        get_api_usage()
        return

    diff = get_staged_diff()

    if not diff:
        print("No staged changes to commit.")
        return

    commit_message = generate_commit_message(diff)

    if commit_message:
        print("\nSuggested Commit Message:\n")
        print(commit_message)
        print("\nTo use it, run:\n")
        if args.amend:  # Handle the --amend option
            subprocess.run(["git", "commit", "--amend", "-m", f"{commit_message}"])
            print("Commit amended successfully.")
        else:
            print(f'git commit -m "{commit_message}"')


if __name__ == "__main__":
    main()