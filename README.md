# PR Quality Bot 🤖

A lightweight bot to ensure high-quality Pull Requests using pre-commit hooks and CI checks.

## 🧠 Checks
- PR title format validation  
- PR description (includes Jira ID)  
- File change analysis  
- Detect forbidden files  
- Commit message validation  

## ⚙️ Run modes
- **Pre-commit hook:** Local validation before commit
- **GitHub Action / ADO pipeline:** Auto-runs on every PR

## 🧩 Setup
1. Add `.github/workflows/pr-quality-bot.yml` or `ado/azure-pipelines-pr-quality.yml`.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
