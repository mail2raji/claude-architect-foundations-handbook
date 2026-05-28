# Contributing

This handbook is primarily a personal learning project, but if you spot a bug, typo, or outdated model name:

1. Open an issue describing what you found.
2. Or open a PR against `main`.

## Local development

```powershell
git clone https://github.com/mail2raji/claude-architect-foundations-handbook.git
cd claude-architect-foundations-handbook
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
# edit .env with your ANTHROPIC_API_KEY
```

## Regenerating the book

After you edit any chapter `README.md` or chapter content, regenerate `BOOK.md`:

```powershell
python tools/build_book.py
```

The script concatenates every chapter in order with chapter dividers and a generated table of contents.

## Style

- Keep code samples small (< 200 lines) and self-contained.
- Real-world examples preferred over toy ones.
- Every new pattern needs a "when to use" + "when NOT to use" note.
- Model names stay current. As of this edition: `claude-haiku-4-5`, `claude-sonnet-4-5`, `claude-opus-4-5`.

## Code of conduct

Be kind. Disagree respectfully. Don't ship malware.
