Here is the rewritten guide specifically for **Windows** users using **IntelliJ IDEA**. I have adapted the commands for the Windows Command Prompt and PowerShell environments.

---

# Setup Guide: Claude API on Windows (IntelliJ IDEA)

This guide follows the [Making a request](https://anthropic.skilljar.com/claude-with-the-anthropic-api/287725) lesson but is optimized for a Windows environment.

## 1. Project Initialization

1. Open **IntelliJ IDEA**.
2. Select **New Project** -> **Python**.
3. **Project SDK**: Ensure "New Virtualenv environment" is selected.
* *Location:* `C:\Users\<YourName>\PycharmProjects\ClaudeProject\venv`


4. Click **Create**.

---

## 2. Environment Activation & Installation

Open the **Terminal** tab at the bottom of IntelliJ (usually `Alt + F12`).

### If using Command Prompt (cmd):

You should see `(venv)` at the start of the line. If not, run:

```cmd
venv\Scripts\activate

```

### If using PowerShell:

If you see an error about "scripts execution," run this first:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

```

Then activate:

```powershell
.\venv\Scripts\Activate.ps1

```

### Install Dependencies:

Once `(venv)` is visible, run:

```powershell
pip install anthropic python-dotenv

```

---

## 3. Configuration (.env)

1. Right-click the project folder -> **New** -> **File**.
2. Name it exactly `.env`.
3. Add your key (no spaces around the `=`):
```text
ANTHROPIC_API_KEY="your-api-key-here"

```



---

## 4. Python Script (`main.py`)

Create a new Python file and paste the following. Note the model update to a current version:

```python
import os
from dotenv import load_dotenv
from anthropic import Anthropic

# Load variables from .env
load_dotenv()

# Initialize Client
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Create Request
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1000,
    messages=[
        {
            "role": "user", 
            "content": "What is quantum computing? Answer in one sentence."
        }
    ]
)

# Output result
print(message.content[0].text)

```

---

## 5. Execution

* **Right-click** anywhere inside `main.py`.
* Select **Run 'main'**.
* The output will appear in the **Run** window at the bottom.

> [!IMPORTANT]
> On Windows, ensure your `.env` file is in the **root** folder of the project (the same level as `main.py`), otherwise `load_dotenv()` will not find it automatically.