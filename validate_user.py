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
    Your task is to validate a user profile JSON against specific constraints.

    ### CRITICAL INSTRUCTIONS
    - Output ONLY valid JSON.
    - Do NOT explain why a field is valid.
    - Only include messages for rules that are VIOLATED.

    ### VALIDATION RULES

    **1. ERRORS (Invalid Data - Fix Immediately)**
    Add to "errors" list if:
    - 'name': Is empty, null, or missing.
    - 'email': Is not a valid email address format.
    - 'age': Is not a number, or smaller that 18, or is a negative number .
    - 'country': Is NOT a valid 2-letter ISO-3166-1 alpha-2 code (e.g. "India" is ERROR, "IN" is OK).
    - 'phone': Is NOT in valid E.164 format. It MUST start with '+', contain a country code, AND have the **correct number of digits** for that country.
      (e.g., '+91' for India requires exactly 10 digits after the code. 9 digits is an ERROR).
    
    **IMPORTANT PHONE RULE:** If the phone number is a valid, plausible E.164 number (correct length), it is NOT an Error, even if it doesn't match the country.
    However, if the length is wrong (e.g. too short), it IS an Error.

    **2. WARNINGS (Valid but Risky Data)**
    Add to "warnings" list if:
    - 'age': Number is less than 18 (but positive).
    - 'name': Length is less than 3 characters (but not empty).
    - 'email': Domain is disposable/temporary (e.g. tempmail, mailinator).
    - 'phone': The phone is valid E.164 (correct length), BUT the country code does not match the 'country' field.

    ### RESPONSE FORMAT
    {
      "is_valid": boolean, // true if "errors" list is EMPTY. Warnings do not make it false.
      "errors": string[],
      "warnings": string[]
    }

    ### EXAMPLES

    Case 1: Valid Phone, Wrong Country
    Input: {"name": "John", "email": "j@test.com", "age": 25, "country": "US", "phone": "+919876543210"}
    Output:
    {
      "is_valid": true,
      "errors": [],
      "warnings": ["phone country code does not match the country field"]
    }

    Case 2: Invalid Phone Format (Garbage)
    Input: {"name": "John", "email": "j@test.com", "age": 25, "country": "US", "phone": "9876543210"}
    Output:
    {
      "is_valid": false,
      "errors": ["phone number must be in E.164 format"],
      "warnings": []
    }

    Case 3: Phone Too Short (Invalid Length)
    Input: {"name": "John", "email": "j@test.com", "age": 25, "country": "IN", "phone": "+91987654321"}
    Output:
    {
      "is_valid": false,
      "errors": ["phone number length is invalid for country code"],
      "warnings": []
    }
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