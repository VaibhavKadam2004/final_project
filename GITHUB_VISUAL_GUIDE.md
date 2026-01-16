# 📸 GitHub Push - Visual Step-by-Step Guide

## Step-by-Step Commands to Push Your Project

```
YOUR COMPUTER                    GITHUB
┌──────────────────┐           ┌──────────────┐
│ Project Files    │    git    │   Your Repo  │
│ ├─ accounts/     ├─ push ──→ │ (Online)     │
│ ├─ jobs/         │           └──────────────┘
│ ├─ templates/    │
│ ├─ manage.py     │
│ └─ .gitignore    │
└──────────────────┘
```

---

## 🚀 QUICK START - Do This Now!

### Step 1️⃣ : Create Repository on GitHub

📍 **Open in Browser:** https://github.com/new

```
┌─────────────────────────────────────┐
│ Create a new repository             │
├─────────────────────────────────────┤
│ Repository name *                   │
│ ┌─────────────────────────────────┐ │
│ │ placement-portal                 │ │ ← Type this
│ └─────────────────────────────────┘ │
│                                      │
│ Description (optional)              │
│ ┌─────────────────────────────────┐ │
│ │ Smart Placement & Internship     │ │
│ │ Portal with advanced features    │ │
│ └─────────────────────────────────┘ │
│                                      │
│ ○ Public  ●                         │ ← Select Public
│                                      │
│ □ Initialize with README            │ ← Leave UNCHECKED
│ □ Add .gitignore                    │ ← Leave UNCHECKED
│ □ Choose a license                  │ ← Leave UNCHECKED
│                                      │
│              [ Create repository ]   │
└─────────────────────────────────────┘
```

✅ After clicking "Create repository", you'll see a page like:
```
Quick setup — if you've done this kind of thing before

https://github.com/YOUR_USERNAME/placement-portal.git

We recommend every repository include a README, LICENSE, and .gitignore.

…or push an existing repository from the command line

git remote add origin https://github.com/YOUR_USERNAME/placement-portal.git
git branch -M main
git push -u origin main
```

---

### Step 2️⃣ : Open PowerShell in VS Code

1. Press `Ctrl + ``` (backtick) to open terminal
2. Or go to **Terminal → New Terminal**

```
Terminal Output:
PS C:\Users\Vaibhav\OneDrive\Documents\EY_4.0_AVCOE\Project3>
```

---

### Step 3️⃣ : Update Git Remote

**Copy this command and paste into PowerShell:**

```powershell
git remote remove origin
```

Press Enter ↵

Then:

```powershell
git remote add origin https://github.com/YOUR_USERNAME/placement-portal.git
```

Replace `YOUR_USERNAME` with your actual GitHub username!

Example:
```powershell
git remote add origin https://github.com/VaibhavKadam2004/placement-portal.git
```

Press Enter ↵

---

### Step 4️⃣ : Verify Remote

```powershell
git remote -v
```

You should see:
```
origin  https://github.com/YOUR_USERNAME/placement-portal.git (fetch)
origin  https://github.com/YOUR_USERNAME/placement-portal.git (push)
```

✅ If this shows, you're good!

---

### Step 5️⃣ : Push to GitHub

```powershell
git push -u origin main
```

Press Enter ↵

---

### Step 6️⃣ : Enter Authentication

**You'll see:**
```
info: please complete authentication in your browser...
```

✅ A browser window will open automatically
- Log in to GitHub if needed
- Click "Authorize"
- Come back to VS Code

Or if browser doesn't open:

**Enter your GitHub credentials:**
```
Username for 'https://github.com': YOUR_USERNAME
Password for 'https://YOUR_USERNAME@github.com': [USE PERSONAL ACCESS TOKEN]
```

💡 **Don't have a token?** See section below.

---

### Step 7️⃣ : Verify on GitHub

1. Open GitHub in browser
2. Go to: `https://github.com/YOUR_USERNAME/placement-portal`
3. Refresh page (F5)
4. You should see all your files! 🎉

```
GitHub Repository
┌──────────────────────────────────────┐
│ YOUR_USERNAME / placement-portal     │
├──────────────────────────────────────┤
│ 📁 accounts/                         │
│ 📁 jobs/                             │
│ 📁 templates/                        │
│ 📁 static/                           │
│ 📄 manage.py                         │
│ 📄 requirements.txt                  │
│ 📄 README.md                         │
│ 📄 .gitignore                        │
│ ... and more                         │
│                                      │
│ Latest commit: "Add documentation"   │
│ by YOUR_USERNAME just now            │
└──────────────────────────────────────┘
```

---

## 🔐 If You Need a Personal Access Token

### Get Your Token:

1. **Open:** https://github.com/settings/tokens
2. **Click:** "Generate new token" → "Generate new token (classic)"
3. **Name it:** "Git CLI Token"
4. **Select scopes:**
   - ☑️ repo
   - ☑️ workflow
5. **Scroll down → Click:** "Generate token"
6. **COPY the token** (you won't see it again!)

### Use Token:

When prompted for password in Git, paste this token instead.

```
Username for 'https://github.com': YOUR_USERNAME
Password: ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx ← Paste token here
```

---

## ✅ Success Checklist

After pushing, verify:

```
✅ GitHub repository created with your name
✅ All files visible on GitHub
✅ README.md showing correctly
✅ Commit history shows your commits
✅ .gitignore preventing sensitive files
✅ Can see recent commit timestamp
```

---

## 🎯 TL;DR (Too Long, Didn't Read)

```bash
# 1. Create repo on GitHub at github.com/new
#    - Name: "placement-portal"
#    - Choose Public
#    - Leave Initialize options unchecked

# 2. Open PowerShell in your project

# 3. Run these 2 commands (replace USERNAME):
git remote remove origin
git remote add origin https://github.com/USERNAME/placement-portal.git

# 4. Push to GitHub:
git push -u origin main

# 5. Authenticate when prompted (use GitHub password or Personal Access Token)

# 6. Done! Check GitHub ✨
```

---

## 🆘 Troubleshooting

### "Authentication failed"
→ Use Personal Access Token, not password
→ See "Get Your Token" section above

### "remote: repository not found"
→ Check spelling in URL
→ Make sure you replaced USERNAME
→ Repository exists on GitHub

### "fatal: could not read Username"
→ Configure Git:
```bash
git config --global user.name "Your Name"
git config --global user.email "your-email@github.com"
```

### "rejected (fetch first)"
→ Try:
```bash
git pull origin main --allow-unrelated-histories
git push -u origin main
```

---

## 💡 What's Being Pushed?

```
All files EXCEPT:
├── .gitignore excludes:
│   ├── venv/                  (Virtual environment)
│   ├── __pycache__/           (Python cache)
│   ├── *.pyc                  (Compiled Python)
│   ├── .vscode/               (VS Code settings)
│   ├── .env                   (Secret keys)
│   ├── db.sqlite3             (Database)
│   └── media/                 (User uploads)
│
And INCLUDES:
├── Source code (.py files)
├── Templates (.html files)
├── CSS/JS files
├── requirements.txt (dependencies)
├── manage.py
└── Configuration files
```

---

## 🎉 After Successful Push

Your GitHub repository is now live!

### Next Steps:
1. ⭐ Add a Star to your repo (so you remember it!)
2. 👥 Add collaborators if working with others
3. 🔧 Enable Discussions (Settings → Features)
4. 📝 Update Repository Description & Tags
5. 🚀 Deploy (see Deployment section for Heroku/Railway)

### Share Your Project:
```
https://github.com/YOUR_USERNAME/placement-portal
```

---

**🎊 Congratulations! Your code is now on GitHub! 🎊**

