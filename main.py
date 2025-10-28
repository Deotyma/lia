import sys
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv


def main():
    load_dotenv()

    args = sys.argv[1:]

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: There is no GEMINI_API_KEY in the environment variables.")
        print("Please set it before running the script.")
        sys.exit(1)

    client = genai.Client(api_key=api_key)


    if not args:
        print("Lia - A simple AI Agent to help you with learning Italian.\n")
        print("Let's create your prompt step by step.\n")

        level = input("Which level (A1–C2)? ").strip().upper()
        if level not in ["A1", "A2", "B1", "B2", "C1", "C2"]:
            print("⚠️ Invalid level. Defaulting to A1.")
            level = "A1"

        try:
            paragraphs = int(input("How many paragraphs (1–3)? ").strip())
            if paragraphs not in [1, 2, 3]:
                raise ValueError
        except ValueError:
            print("⚠️ Invalid number. Defaulting to 1 paragraph.")
            paragraphs = 1

        topic = input("Which topic? ").strip()
        if not topic:
            print("⚠️ Empty topic. Defaulting to 'dog'.")
            topic = "dog"

        user_prompt = f"Italian {level} text, {paragraphs} paragraph(s), topic: {topic}."
        print(f"\n✅ Your prompt:\n{user_prompt}\n")

    # --- ARGUMENT MODE (manual prompt passed in command line) ---
    else:
        user_prompt = " ".join(args)

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    generate_content(client, messages)


def generate_content(client, messages):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
    )
    print("\nPrompt tokens:", response.usage_metadata.prompt_token_count)
    print("Response tokens:", response.usage_metadata.candidates_token_count)
    print("\nResponse:\n")
    print(response.text)


if __name__ == "__main__":
    main()
