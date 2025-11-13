<#
PowerShell helper to initialize and push this project to GitHub.
Behavior:
 - If git isn't installed, exits with an error.
 - If GitHub CLI (`gh`) is installed and you're logged in, it will create the remote repo and push.
 - Otherwise, it asks for a remote URL (https) and pushes to it.
Usage:
  Right-click the file in Explorer and Run with PowerShell, or from PowerShell:
    cd "path\to\project"; .\upload_to_github.ps1
#>

param(
    [string]$RepoName = "",
    [ValidateSet("public","private")][string]$Visibility = "public"
)

function Prompt-IfEmpty([string]$val, [string]$prompt) {
    if ([string]::IsNullOrWhiteSpace($val)) {
        return Read-Host $prompt
    }
    return $val
}

# Ensure git available
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Error "git is not installed or not available in PATH. Install Git and try again: https://git-scm.com/downloads"
    exit 1
}

# Determine defaults
$cwd = Get-Location
if ([string]::IsNullOrWhiteSpace($RepoName)) {
    $RepoName = Prompt-IfEmpty $RepoName "Enter GitHub repository name (default: current folder name):"
    if ([string]::IsNullOrWhiteSpace($RepoName)) { $RepoName = Split-Path -Leaf $cwd }
}

if ([string]::IsNullOrWhiteSpace($Visibility)) {
    $Visibility = Prompt-IfEmpty $Visibility "Visibility (public/private) [public]:"
    if ($Visibility -ne 'private') { $Visibility = 'public' }
}

# Create .gitignore if missing (light safeguard)
$gitignorePath = Join-Path $cwd '.gitignore'
if (-not (Test-Path $gitignorePath)) {
    @"# Byte-compiled files
__pycache__/
*.py[cod]
# virtualenv
venv/
.env
"@ | Out-File -Encoding utf8 -FilePath $gitignorePath
    Write-Host "Created basic .gitignore"
}

# Initialize if necessary
if (-not (Test-Path (Join-Path $cwd '.git'))) {
    git init
    Write-Host "Initialized empty Git repository"
}

# Stage and commit
try {
    git add .
    git commit -m "Initial commit" -q
    Write-Host "Committed files"
}
catch {
    # If commit failed because nothing changed, allow empty commit
    Write-Host "No changes to commit or commit failed. Creating an initial empty commit."
    git commit --allow-empty -m "Initial commit" -q
}

# Use gh if available
if (Get-Command gh -ErrorAction SilentlyContinue) {
    Write-Host "Found GitHub CLI (gh). Creating remote repo and pushing..."
    try {
        # Use gh to create and push the repo. --source and --push attach and push current folder
        gh repo create $RepoName --$Visibility --source=. --remote=origin --push
        Write-Host "Repository created and pushed using gh. URL: https://github.com/$(gh api user --jq .login)/$RepoName"
    }
    catch {
        Write-Warning "gh command failed: $_"
        Write-Host "If the repo already exists remote creation may have failed. You can add a remote manually."
    }
}
else {
    Write-Host "GitHub CLI (gh) not found. I'll ask for a remote URL to push to (e.g. https://github.com/username/$RepoName.git)."
    $remoteUrl = Read-Host "Enter remote URL (leave empty to skip pushing):"
    if (-not [string]::IsNullOrWhiteSpace($remoteUrl)) {
        try {
            git branch -M main
            git remote add origin $remoteUrl
            git push -u origin main
            Write-Host "Pushed to remote: $remoteUrl"
        }
        catch {
            Write-Error "Push failed: $_"
            Write-Host "If the remote already exists, run: git push -u origin main"
        }
    }
    else {
        Write-Host "No remote provided. Repository exists locally. To push later:"
        Write-Host "  git branch -M main"
        Write-Host "  git remote add origin https://github.com/<username>/$RepoName.git"
        Write-Host "  git push -u origin main"
    }
}

Write-Host "Done."
