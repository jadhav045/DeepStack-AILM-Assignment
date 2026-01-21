
# LLM-Based User Input Validator

A strict, LLM-powered validation script that enforces data integrity without using traditional regex or validation libraries. Built with Python, this tool relies entirely on Large Language Models to interpret and validate user profiles against complex international standards (ISO-3166, E.164).

It is designed to be **provider-agnostic**, supporting OpenAI, Groq, and other OpenAI-compatible APIs.

## 🚀 Features

* **Pure LLM Validation:** Logic is driven by Few-Shot Prompting to enforce rules like "valid ISO-2 country code" and "E.164 phone format" without hardcoded string manipulation.
* **Strict JSON Output:** Utilizes `response_format={"type": "json_object"}` to guarantee deterministic, machine-readable validation results.
* **Automated Evaluations:** Includes a comprehensive `promptfoo` test suite to verify schema compliance, error detection, and warning logic across edge cases.
* **Interactive Web Dashboard:** Includes a **Streamlit** UI for real-time, visual testing of the validator.
* **Provider-Agnostic:** Seamlessly switch between paid models (OpenAI GPT-4o) and free/open-source models (Groq Llama-3) via environment variables.

## 🛠️ Setup Instructions

### Prerequisites

* **Python 3.10+** (Required for type hinting and library support)
* **Node.js** (Required to run the `promptfoo` evaluation suite)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/yourusername/llm-validator.git](https://github.com/yourusername/llm-validator.git)
    cd llm-validator
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # Create venv
    python -m venv venv

    # Activate (Windows)
    venv\Scripts\activate

    # Activate (Mac/Linux)
    source venv/bin/activate
    ```

3.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## ⚙️ Configuration

The project uses a `.env` file to manage API keys and model selection.

1.  **Initialize Environment Variables:**
    ```bash
    cp .env.example .env
    # Or manually create a .env file
    ```

2.  **Configure your preferred LLM provider:**

    ### Option A: OpenAI (Paid)
    ```ini
    LLM_API_KEY=sk-proj-your-openai-key
    LLM_BASE_URL=[https://api.openai.com/v1](https://api.openai.com/v1)
    LLM_MODEL=gpt-4o-mini
    ```

    ### Option B: Groq (Free Tier / High Speed)
    ```ini
    LLM_API_KEY=gsk_your-groq-key
    LLM_BASE_URL=[https://api.groq.com/openai/v1](https://api.groq.com/openai/v1)
    LLM_MODEL=llama3-70b-8192
    ```

## 🏃 How to Run

### 1. Command Line Interface (CLI)
The script accepts a single JSON file as an argument and outputs the validation result in strict JSON format.

**Command:**
```bash
python validate_user.py <path_to_input_file.json>

```

**Example Usage:**

```bash
# Run with included test data
python validate_user.py data/valid_user.json

```

### 2. Interactive Web Dashboard 🌟

Launch the Streamlit dashboard to test the validator via a graphical interface. This allows you to fill out a form and see the AI validation logic in real-time.

**Command:**

```bash
streamlit run app.py

```

*This will automatically open a new tab in your default web browser.*

## 🧪 How to Run Evaluations

This project uses **Promptfoo** to ensure the LLM behaves correctly across edge cases and correctly distinguishes between "Errors" (invalid data) and "Warnings" (risky data).

1. **Initialize Promptfoo** (One-time setup if not installed globally):
```bash
npx promptfoo@latest init

```


2. **Run the Test Suite:**
Execute the evaluation using the provided configuration file (located in the `tests/` folder):
```bash
npx promptfoo eval -c tests/promptfoo.yaml

```



### What is Tested?

The test suite covers the following scenarios:

* ✅ **Happy Path:** Valid inputs with correct formatting.
* ❌ **Critical Errors:**
* Phone number not in E.164 format.
* Country code not complying with ISO-3166-1 alpha-2.
* Missing required fields (Name, Email).


* ⚠️ **Warnings:**
* Phone country code does not match the `country` field.
* Use of disposable email domains (e.g., tempmail).
* User age under 18.



## 📂 Project Structure

```text
.
├── data/               # 📂 JSON test files (input.json, valid_user.json, etc.)
├── tests/              # 🧪 Automated evaluation suite
│   ├── promptfoo.yaml  #    - Eval configuration
│   └── test_wrapper.py #    - Python bridge for Promptfoo
├── validate_user.py    # 🚀 Main CLI application logic
├── app.py              # 🌐 Streamlit Web Dashboard
├── requirements.txt    # 📦 Python dependencies
├── .env                # 🔒 API credentials (excluded from Git)
└── README.md           # 📖 Project documentation

```

## 🧠 Design Philosophy

1. **No Hardcoded Logic:** The script contains zero regex or `if/else` checks for data format. All validation logic is inferred by the LLM based on high-level instructions (e.g., "Validate against ISO-2").
2. **Schema Enforcement:** We use `response_format={"type": "json_object"}` to prevent the LLM from generating conversational filler, ensuring the output is always parseable by downstream systems.
3. **Separation of Concerns:**
* **Errors** are reserved for syntactically invalid or missing data.
* **Warnings** are reserved for valid but semantically risky data (e.g., disposable emails).



## 📄 License

This project is licensed under the MIT License.

```
