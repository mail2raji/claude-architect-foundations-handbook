# Setup — Windows (PowerShell)

## 1. Python

You need **Python 3.10+**. Check:

```powershell
python --version
```

If missing, install from https://www.python.org/downloads/windows/ (tick *"Add Python to PATH"*).

## 2. Create and activate a virtual environment

From the workspace folder:

```powershell
cd C:\Scripts\Send-escalationEmail\Claude_Learning
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If activation is blocked by execution policy:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

## 3. Install dependencies

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Get an Anthropic API key

1. Sign in at https://console.anthropic.com
2. **Settings → API Keys → Create Key**
3. **Billing → add a small credit** (a few dollars is plenty for this entire course).
4. Copy the key (starts with `sk-ant-...`).

## 5. Configure environment

```powershell
Copy-Item .env.example .env
notepad .env
```

Paste your key:

```env
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxx
```

> **Never commit `.env`.** It's already in `.gitignore`.

## 6. Verify

```powershell
python Phase0_Setup\01_first_call.py
```

You should see a Claude reply. If not, see Troubleshooting below.

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| `ModuleNotFoundError: anthropic` | Activate the venv (`.\.venv\Scripts\Activate.ps1`) then `pip install -r requirements.txt`. |
| `AuthenticationError` | API key wrong or missing. Re-check `.env`. |
| `RateLimitError` | Add credits in console; or `time.sleep(20)` between calls. |
| Proxy/corporate network blocks api.anthropic.com | Configure `HTTPS_PROXY` env var, or run from personal network for learning. |
| `UnicodeDecodeError` on Windows | Add `chcp 65001` before running scripts. |
