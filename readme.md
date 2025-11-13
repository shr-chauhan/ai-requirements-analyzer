# AI Requirements Analyzer

A small Streamlit web app that converts a business requirement (paste or upload) into:
- Epics & user stories
- Acceptance criteria (Gherkin)
- Test cases
- Functional & Non-functional requirements
- A Mermaid process flow diagram

It uses the OpenAI `gpt-4o-mini` model for generation (most cost-effective option, over 60% cheaper than gpt-3.5-turbo).

## Quick start (local)

### 1. Create a Python 3.10+ virtual environment and activate it

```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### 2. Install requirements

```bash
pip install -r requirements.txt
```

### 3. Set up your OpenAI API Key and App Password

**Option A: Using Streamlit Secrets (Recommended)**

1. Open `.streamlit/secrets.toml` file
2. Replace the placeholder key with your actual OpenAI API key:
   ```toml
   OPENAI_API_KEY = "sk-proj-your-actual-key-here"
   ```
3. Set your app password (change from default):
   ```toml
   APP_PASSWORD = "your-secure-password-here"
   ```
4. Get your API key from: https://platform.openai.com/account/api-keys

**Option B: Using Environment Variable**

On Windows (PowerShell):
```powershell
$env:OPENAI_API_KEY="sk-proj-your-actual-key-here"
```

On Windows (Command Prompt):
```cmd
set OPENAI_API_KEY=sk-proj-your-actual-key-here
```

On Mac/Linux:
```bash
export OPENAI_API_KEY="sk-proj-your-actual-key-here"
```

### 4. Run the app

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Getting Your OpenAI API Key

1. Go to https://platform.openai.com/
2. Sign up or log in to your account
3. Navigate to **API keys** section: https://platform.openai.com/account/api-keys
4. Click **"Create new secret key"**
5. Copy the key (you won't see it again!)
6. Make sure you have billing set up: https://platform.openai.com/account/billing

## Password Protection

The app is protected with a password. The default password is set in `.streamlit/secrets.toml` as `APP_PASSWORD`. 

**To change the password:**
1. Edit `.streamlit/secrets.toml`
2. Change the `APP_PASSWORD` value to your desired password
3. Restart the Streamlit app

**Alternative:** You can also set the password via environment variable:
```bash
# Windows PowerShell
$env:APP_PASSWORD="your-password"

# Windows CMD
set APP_PASSWORD=your-password

# Mac/Linux
export APP_PASSWORD="your-password"
```

## Deployment

This app can be deployed to various platforms. See **[DEPLOYMENT.md](DEPLOYMENT.md)** for detailed deployment instructions.

**Quick Deploy Options:**
- **Streamlit Cloud** (Recommended) - Free, easiest deployment
- **Heroku** - Free tier available
- **AWS/DigitalOcean** - Full control, pay-as-you-go
- **Docker** - Deploy anywhere Docker runs

See the deployment guide for step-by-step instructions for each platform.

## Notes

- The `.streamlit/secrets.toml` file is already in `.gitignore` to prevent committing your API key and password
- Never share or commit your API key or password to version control
- Monitor your API usage to manage costs
- Use the logout button in the top right to end your session