import re 
import os 
import json
import csv
import anthropic
from typing import List
from pathlib import Path 
from tqdm import tqdm
import time


ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    raise ValueError("Please set ANTHROPIC_API_KEY environment variable")


def get_claude_response(prompt: str):
    # Initialize the client with your API key
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    # Create a message request
    response = client.messages.create(
        model="claude-3-5-sonnet-20240620",  # Specify the model version
        max_tokens=1000,  # Set maximum tokens for the response
        temperature=0.5,  # Adjust randomness of responses (0.0 for deterministic)
        system="You are a helpful assistant.",  # System message for context
        messages=[{"role": "user", "content": prompt}],
    )

    # Print the response content
    return response


def parse_translations(text: str) -> List[str]:
    pattern = r"<t>(.*?)</t>"
    translations = re.findall(pattern, text, re.DOTALL)
    translations = [t.strip() for t in translations]
    translations = " ".join(translations)
    return translations.replace("\n", "<br>")


def get_prompt(tibetan_text):
    return f"""
    Translate the following Buddhist Tibetan passage into English: {tibetan_text} English:
    
    ## Core Instructions
    - Enclose final English translation in <t> tags
    """


def get_tibetan_text_list(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)
    target_content = data['target']['books'][0]['content']
    for chapter_num in range(0, len(target_content)):
        for tibetan_text in target_content[chapter_num]:
            yield chapter_num, tibetan_text


RATE_LIMIT = 50  # Maximum number of requests
RATE_LIMIT_PERIOD = 60  # Time period in seconds

# Initialize request counter and start time
request_count = 0
start_time = time.time()



def translate_and_write():
    # json_path = Path("./data/The_Way_of_the_Boddhisattva.json")
    text_list = list(Path(f"./data/chonjuk_drupchen_segments.txt").read_text(encoding='utf-8').splitlines())
    global request_count, start_time  # Access global variables

    with open("Chonjuk_drupchen_segment_translation.csv", "a", newline='', encoding='utf-8') as csv_file:
        fieldnames = ["Tibetan", "English"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        if csv_file.tell() == 0:
            writer.writeheader()

        # for chapter_num, tibetan_text in tqdm(get_tibetan_text_list(json_path), desc="Translating chapters"):
            # Check if rate limit is exceeded
        for tibetan_text in tqdm(text_list[56:], desc="Translating chapters"):    
            if request_count >= RATE_LIMIT:
                elapsed_time = time.time() - start_time
                if elapsed_time < RATE_LIMIT_PERIOD:
                    wait_time = RATE_LIMIT_PERIOD - elapsed_time
                    print(f"Rate limit reached. Waiting for {wait_time:.2f} seconds...")
                    time.sleep(wait_time)
                request_count = 0
                start_time = time.time()

            prompt = get_prompt(tibetan_text)
            response = get_claude_response(prompt)
            English_translate = parse_translations(response.content[0].text)
            writer.writerow({"Tibetan": tibetan_text, "English": English_translate})
            csv_file.flush()
            request_count += 1

if __name__ == "__main__":
    translate_and_write()