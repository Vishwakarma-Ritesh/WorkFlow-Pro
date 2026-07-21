# Professional Repository Structure

This project now follows a standard Python QA automation layout similar to what client teams use for maintainable frameworks.

```text
WorkFlow-Pro/
├── .github/
│   └── workflows/
│       └── qa.yml
├── config/
│   ├── browserstack.yaml
│   ├── config.yaml
│   └── environments/
│       ├── dev.yaml
│       └── staging.yaml
├── docs/
├── logs/
├── reports/
├── src/
│   └── workflowpro_qa/
│       ├── api/
│       │   ├── clients/
│       │   ├── endpoints/
│       │   ├── helpers/
│       │   └── models/
│       ├── browserstack/
│       ├── config/
│       ├── fixtures/
│       ├── pages/
│       │   └── components/
│       └── utils/
├── test_data/
├── tests/
│   ├── api/
│   ├── integration/
│   ├── mobile/
│   └── ui/
├── .env.example
├── .gitignore
├── .pre-commit-config.yaml
├── Makefile
├── pyproject.toml
├── pytest.ini
├── README.md
└── requirements.txt
```

## Why This Is Better

- `src/workflowpro_qa` makes framework code installable and reusable.
- `tests` stays focused on business scenarios, not framework internals.
- `config` contains non-secret runtime configuration.
- `test_data` contains templates only, while credentials stay in `.env` or CI secrets.
- `reports`, `logs`, `.ruff_cache`, `.pytest_cache`, and `__pycache__` are generated artifacts, not source code.

## What `.ruff_cache` Is

`.ruff_cache` is created by Ruff when it checks or formats Python code. It stores analysis results so future lint runs are faster. It is safe to delete and should not be committed.

Clean generated local files with:

```bash
make clean
```
