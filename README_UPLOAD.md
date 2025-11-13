This project includes a helper script to initialize a Git repository and upload the project to GitHub.

Files added for upload support:

- `upload_to_github.ps1` — PowerShell script that initializes git, commits files, and creates/pushes the repository using the GitHub CLI (`gh`) if available. If `gh` is not installed, it prompts for a remote URL and pushes to it.
- `.gitignore` — Common Python/Flask ignores (virtualenvs, caches, env files).

How to use (PowerShell):

1. Open PowerShell and change directory to the project root:

```powershell
cd "D:\Setec Insititute\Year III\SEMESTER II\Subject_Python\Exercise\Flask\Lab_3"
```

2. Run the upload script:

```powershell
# If you trust the script and ExecutionPolicy allows it
./upload_to_github.ps1

# Or explicitly call PowerShell if script execution is restricted
powershell -ExecutionPolicy Bypass -File .\upload_to_github.ps1
```

3. Follow the prompts. The script will try to use `gh` (GitHub CLI) if installed. To use `gh` seamlessly:

- Install GitHub CLI: https://cli.github.com/
- Log in: `gh auth login`

Manual alternative (no script):

```powershell
git init
git add .
git commit -m "Initial commit"
git branch -M main
# Create a repository on GitHub and then
git remote add origin https://github.com/<username>/<repo>.git
git push -u origin main
```

If you want, tell me the GitHub repo name and whether you want it public or private and I can supply the exact `gh` command to run, or a one-line command you can paste into PowerShell to create and push the repo automatically.
