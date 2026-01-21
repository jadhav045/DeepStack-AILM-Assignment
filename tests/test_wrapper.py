import json
import sys
import os

# Add the parent directory (root) to sys.path so we can import validate_user
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now we can import the main logic
from validate_user import validate_user_profile

def call_validation(prompt, options, context):
    """
    Bridge function for Promptfoo.
    'prompt' will contain the JSON string from our test cases.
    """
    try:
        user_data = json.loads(prompt)
        result = validate_user_profile(user_data)
        return {
            "output": json.dumps(result)
        }
    except Exception as e:
        return {
            "error": f"Test Error: {str(e)}"
        }