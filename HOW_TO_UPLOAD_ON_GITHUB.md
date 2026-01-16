# 📤 How to Upload Your Website on GitHub - Complete Steps

## ✅ Prerequisites (Do You Have These?)

- ✅ GitHub account (sign up at github.com if you don't have one)
- ✅ Git installed on your computer
- ✅ Your project folder ready
- ✅ Internet connection

---

## 🚀 EXACT STEPS TO FOLLOW

### **STEP 1: Create a Repository on GitHub**

1. **Open browser and go to:** https://github.com/new

2. **You'll see a form. Fill it like this:**

```
Repository name: placement-portal
Description: Smart Internship & Placement Portal
Choose: Public (so anyone can see it)

Leave these UNCHECKED:
☐ Initialize this repository with a README
☐ Add .gitignore
☐ Choose a license
```

3. **Click:** `Create repository` button

4. **You'll see instructions. COPY this URL:**
```
https://github.com/YOUR_USERNAME/placement-portal.git
```

---

### **STEP 2: Open PowerShell in Your Project Folder**

**Option A: Using VS Code**
1. Open VS Code
2. Open your project folder
3. Press `Ctrl + `` (backtick) to open terminal
4. Terminal will open at the bottom

**Option B: Manual**
1. Right-click on your project folder
2. Select "Open in Terminal" or "Open PowerShell here"

---

### **STEP 3: Configure Git Remote (Run These Commands)**

**Copy and paste each command one by one:**

**Command 1:**
```powershell
git remote remove origin
```
Press Enter ↵

**Command 2:**
```powershell
git remote add origin https://github.com/YOUR_USERNAME/placement-portal.git
```
Replace `YOUR_USERNAME` with your actual GitHub username
Press Enter ↵

**Example:**
```powershell
git remote add origin https://github.com/VaibhavKadam2004/placement-portal.git
```

---

### **STEP 4: Verify Remote Configuration**

**Run this command:**
```powershell
git remote -v
```

**You should see output like:**
```
origin  https://github.com/YOUR_USERNAME/placement-portal.git (fetch)
origin  https://github.com/YOUR_USERNAME/placement-portal.git (push)
```

✅ If you see this, you're good!

---

### **STEP 5: Check Git Status**

**Run this command:**
```powershell
git status
```

**You should see:**
```
On branch main
nothing to commit, working tree clean
```

✅ This means all changes are already committed!

---

### **STEP 6: Push Code to GitHub**

**Run this command:**
```powershell
git push -u origin main
```

Press Enter ↵

---

### **STEP 7: Authenticate with GitHub**

**You'll see one of these:**

**Option A: Browser Opens (Easiest)**
- A browser window opens automatically
- Log in to GitHub
- Click "Authorize"
- Go back to PowerShell
- Done! ✨

**Option B: Terminal Asks for Password**
```
Username for 'https://github.com': YOUR_USERNAME
Password for 'https://YOUR_USERNAME@github.com': 
```

Enter:
- **Username:** Your GitHub username
- **Password:** Your Personal Access Token (NOT your actual password)

**How to get Personal Access Token:**
1. Go to: https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Give it a name: "GitHub CLI"
4. Check these boxes:
   - ☑ repo
   - ☑ workflow
5. Click "Generate token"
6. Copy the token (save it somewhere!)
7. Paste it as password in terminal

---

### **STEP 8: Verify on GitHub**

1. **Go to:** https://github.com/YOUR_USERNAME/placement-portal

2. **You should see:**
   - ✅ All your files listed
   - ✅ README.md displaying
   - ✅ Commit history
   - ✅ "main" branch

---

## 💻 Complete Commands (Copy & Paste)

**Do this in PowerShell:**

```powershell
# Navigate to your project
cd "c:\Users\Vaibhav\OneDrive\Documents\EY_4.0_AVCOE\Project3"

# Check status
git status

# Configure remote (replace YOUR_USERNAME)
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/placement-portal.git

# Verify remote
git remote -v

# Push to GitHub
git push -u origin main
```

Then authenticate when prompted!

---

## 🎯 What Each Command Does

| Command | What It Does |
|---------|------------|
| `git remote remove origin` | Removes old GitHub connection |
| `git remote add origin [URL]` | Adds new GitHub repository link |
| `git remote -v` | Shows your GitHub connection |
| `git status` | Shows what files will be pushed |
| `git push -u origin main` | Uploads all code to GitHub |

---

## ❌ Common Errors & Fixes

### Error 1: "fatal: not a git repository"
**Fix:**
```powershell
cd "c:\Users\Vaibhav\OneDrive\Documents\EY_4.0_AVCOE\Project3"
git status
```

### Error 2: "Repository not found"
**Causes:**
- Wrong username in URL
- Repository not created on GitHub yet
- Typo in URL

**Fix:**
- Check GitHub username spelling
- Verify repository exists at github.com/new
- Re-run: `git remote add origin [CORRECT_URL]`

### Error 3: "Authentication failed"
**Fix:**
- Use Personal Access Token (not password)
- Get token at: https://github.com/settings/tokens
- When asked for password, paste the token

### Error 4: "Permission denied"
**Causes:**
- Wrong GitHub account
- Not owner of repository

**Fix:**
- Verify you're logged into correct GitHub account
- Check you created the repository
- Try Personal Access Token authentication

---

## ✅ Success Checklist

After pushing, verify:

```
✅ Browser shows no errors after authentication
✅ Terminal shows "Everything up-to-date"
✅ GitHub page shows all your files
✅ You can see your commits in history
✅ README.md displays on main page
✅ Branch shows "main"
✅ Last updated timestamp shows "now"
```

---

## 🌐 Your GitHub URL

After successful push, your project is at:

```
https://github.com/YOUR_USERNAME/placement-portal
```

**Example:**
```
https://github.com/VaibhavKadam2004/placement-portal
```

---

## 📱 What Gets Uploaded

### ✅ YES (Uploaded):
- Python files (.py)
- HTML templates
- CSS & JavaScript
- Configuration files
- Documentation
- .gitignore
- requirements.txt

### ❌ NO (Not Uploaded):
- Virtual environment (venv/)
- Database (db.sqlite3)
- User uploads (media/)
- Cache files (__pycache__/)
- Environment variables (.env)

---

## 💡 After Upload - Next Steps

### Optional but Recommended:

1. **Add Description to GitHub:**
   - Go to your repo
   - Click "About" (right side)
   - Add description: "Smart Placement Portal"
   - Add website link (if you deploy it)

2. **Add Topics:**
   - Click "About"
   - Add topics: django, python, placement-portal

3. **Set README:**
   - GitHub auto-shows README.md
   - Your repo already has one

4. **Star Your Repo:**
   - Click star icon
   - Bookmark your own project!

---

## 🎓 Understanding the Process

```
Your Computer                GitHub.com
┌─────────────────┐         ┌──────────────┐
│  Your Project   │ ─push─> │  Repository  │
│  Files          │         │  (Online)    │
└─────────────────┘         └──────────────┘
       git                   (Website updated)
```

---

## 🚀 Final Command Summary

**The ONLY 3 commands you need:**

```powershell
# 1. Go to your project folder
cd "c:\Users\Vaibhav\OneDrive\Documents\EY_4.0_AVCOE\Project3"

# 2. Update remote (replace YOUR_USERNAME)
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/placement-portal.git

# 3. Push to GitHub
git push -u origin main
```

That's it! Your website will be on GitHub! ✨

---

## 📞 Need Help?

**If something goes wrong:**
- Check error message carefully
- Look at "Common Errors & Fixes" section above
- Read GITHUB_PUSH_GUIDE.md in your project
- Check GitHub username spelling
- Verify repository exists at github.com

---

## 🎉 You're Ready!

Your project is set up and ready to go to GitHub. Just follow the 3 steps above!

**Questions?**
- GitHub Docs: https://docs.github.com
- Git Help: https://git-scm.com/doc
- Your Project Guides: QUICK_REFERENCE.md, GITHUB_VISUAL_GUIDE.md

---

**Your website will be live on GitHub in 5 minutes! 🚀**
