import os
import json
import sys
from openai import OpenAI
from dotenv import load_dotenv

# 1. Load Environment Variables
load_dotenv()

# 2. Initialize the Client
client = OpenAI(
    api_key=os.getenv("LLM_API_KEY"),
    base_url=os.getenv("LLM_BASE_URL")
)

MODEL_NAME = os.getenv("LLM_MODEL", "gpt-3.5-turbo")

def validate_user_profile(user_data):
    """
    Validates user profile using an LLM.
    Enforces strict JSON output schema.
    """
    
    # SYSTEM PROMPT
    # Updated to explicitly check phone number LENGTH
    system_prompt = """
   You are a strict Data Validation Assistant.

Your task is to validate a user profile JSON against real-world data standards using reasoning only.
You must NOT use regex, validation libraries, or hardcoded lookup tables.
The LLM itself is the only validator.

---

### CRITICAL INSTRUCTIONS

- Output ONLY valid JSON.
- Do NOT explain why any field is valid.
- Report ONLY rule violations.
- Do NOT infer, guess, or fabricate missing data.
- Apply validation rules ONLY to fields that are present in the input.
- Do NOT invent new fields or rules.
- If multiple rules are violated, report ALL of them.
- All messages must be grounded strictly in the provided input values.

---

### VALIDATION RULES

#### 1. ERRORS (Invalid Data — Must Be Fixed)

Add a message to the "errors" list ONLY if a present field clearly violates a real-world standard.

- **name**  
  Must be a non-empty string.

- **email**  
  Must follow a valid, real-world email address format.

- **age**  
  Must be a valid, non-negative number.

- **country**  
  Must follow the ISO-3166-1 alpha-2 country code standard.

- **phone**  
  Must follow the E.164 international phone number standard, including:
  - Proper use of the '+' prefix
  - A valid country calling code
  - A plausible total length for that country code

If a phone number is too short, too long, malformed, or not plausible under E.164, it is an ERROR.

---

#### 2. WARNINGS (Valid but Risky Data)

Add a message to the "warnings" list ONLY if the data is valid but potentially risky.

- **name**  
  Very short names may be risky.

- **age**  
  Values indicating a minor may be risky.

- **email**  
  Disposable or temporary email domains may be risky.

- **phone**  
  A phone number that is valid E.164 but whose country calling code does not align with the provided country field may be risky.

---

### RESPONSE FORMAT (STRICT)

Return a single JSON object in the following format:

{
  "is_valid": boolean,
  "errors": string[],
  "warnings": string[]
}

Rules:
- "is_valid" must be true ONLY if "errors" is empty.
- Warnings must NOT make "is_valid" false.
- Do NOT include any fields outside this schema.

    """

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": json.dumps(user_data)}
            ],
            response_format={"type": "json_object"},
            temperature=0
        )
        
        content = response.choices[0].message.content
        return json.loads(content)

    except Exception as e:
        return {
            "is_valid": False,
            "errors": [f"Internal System Error: {str(e)}"],
            "warnings": []
        }

# --- MAIN EXECUTION BLOCK (CLI) ---
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_user.py <input_file.json>")
        sys.exit(1)
        
    file_path = sys.argv[1]
    
    try:
        with open(file_path, 'r') as f:
            user_data = json.load(f)
            
        result = validate_user_profile(user_data)
        print(json.dumps(result, indent=2))
        
    except FileNotFoundError:
        print(json.dumps({
            "is_valid": False,
            "errors": [f"File not found: {file_path}"],
            "warnings": []
        }, indent=2))
    except json.JSONDecodeError:
        print(json.dumps({
            "is_valid": False,
            "errors": ["Invalid JSON format in input file"],
            "warnings": []
        }, indent=2))