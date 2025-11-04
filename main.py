import sys
import os
from pathlib import Path

from dotenv import load_dotenv
from fpdf import FPDF
from google import genai
from google.genai import types


def generate_content(client, messages):
    """
    Appelle le modèle Gemini et renvoie le texte généré.
    Affiche aussi quelques métadonnées si disponibles.
    """
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
    )

    # tokens used metadata
    try:
        print("\nPrompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)
    except Exception:
        pass
    # extracted text
    text = getattr(response, "text", None)
    if not text:
        try:
            text = response.candidates[0].content.parts[0].text
        except Exception:
            text = ""

    print("\nResponse:\n")
    print(text)
    return text


def save_text_to_pdf(text: str, prompt: str):
    #if user wants to save text as PDF
    choice = input("\nDo you want to save the text as a PDF? (yes/no) ").strip().lower()
    if choice not in ("yes", "y"):
        return

    # filename safe as prompt 
    safe = "".join(c if c.isalnum() or c in (" ", "_", "-") else "_" for c in prompt)
    safe = "_".join(safe.split())[:60] or "italian_text"
    filename = safe + ".pdf"

    # determine save location in downloads or cwd
    downloads_dir = Path.home() / "Downloads"
    target_dir = downloads_dir if downloads_dir.is_dir() else Path.cwd()
    path = target_dir / filename

    # text cleanup for PDF generation for to not have issues with special characters
    replacements = {
        "’": "'", "‘": "'", "“": '"', "”": '"',
        "–": "-", "—": "-", "…": "...", "•": "-",
        "\u00A0": " ",  # non-breaking space
    }
    for bad, good in replacements.items():
        text = text.replace(bad, good)

    # PDF generation
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # content addition
    for block in text.split("\n"):
        pdf.multi_cell(0, 8, block)
        pdf.ln(1)

    try:
        pdf.output(str(path))
        print(f"✅ Saved PDF to: {path}")
    except Exception as e:
        print(f"Could not save PDF: {e}")


def italianText():
    """
    Lia - A simple AI Agent to help you with learning Italian.
    It can operate in two modes:
    1. Interactive mode: No command-line arguments, prompts user for input step-by-step
    2. Argument mode: Command-line arguments are used to form the prompt directly.
    """
    load_dotenv()

    args = sys.argv[1:]

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: There is no GEMINI_API_KEY in the environment variables.")
        print("Please set it before running the script.")
        sys.exit(1)

    client = genai.Client(api_key=api_key)

    # interactive mode if no args
    if not args:
        print("Lia - A simple AI Agent to help you with learning Italian.\n")
        print("Let's create your prompt step by step.\n")

        level = input("Which level (A1–C2)? ").strip().upper()
        if level not in ["A1", "A2", "B1", "B2", "C1", "C2"]:
            print("Invalid level. Defaulting to A1.")
            level = "A1"

        try:
            paragraphs = int(input("How many paragraphs (1–3)? ").strip())
            if paragraphs not in [1, 2, 3]:
                raise ValueError
        except ValueError:
            print("Invalid number. Defaulting to 1 paragraph.")
            paragraphs = 1

        topic = input("Which topic? ").strip()
        if not topic:
            topic = "dog"

        user_prompt = f"Italian {level} text, {paragraphs} paragraph(s), topic: {topic}."
        print(f"\n✅ Your prompt:\n{user_prompt}\n")
    else:
        # Argument mode
        user_prompt = " ".join(args)

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    # text generation option after getting the response to save it as PDF
    text = generate_content(client, messages)
    save_text_to_pdf(text or " ", user_prompt)


if __name__ == "__main__":
    italianText()
