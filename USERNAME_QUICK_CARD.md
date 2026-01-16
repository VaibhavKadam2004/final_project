# 🎯 YOUR_USERNAME - Quick Reference Card

## What is YOUR_USERNAME?

**YOUR_USERNAME = A placeholder that you must replace with your actual GitHub username**

It's like:
- Template: "Hello [YOUR_NAME]"
- Real usage: "Hello Vaibhav"

---

## How to Find Your GitHub Username

### Option 1: Direct Check
1. Go to: https://github.com
2. Look at top right corner
3. Click your profile picture
4. Look at the page URL or profile name

### Option 2: Settings
1. Go to: https://github.com/settings/profile
2. Look at "Name" field
3. Or look at URL: https://github.com/YOUR_ACTUAL_USERNAME

---

## The Command Template

```
git remote add origin https://github.com/YOUR_USERNAME/placement-portal.git
```

---

## Real Examples

### Example 1:
```
If your GitHub username is: myusername

Then use:
git remote add origin https://github.com/myusername/placement-portal.git
```

### Example 2:
```
If your GitHub username is: john_developer

Then use:
git remote add origin https://github.com/john_developer/placement-portal.git
```

### Example 3:
```
If your GitHub username is: VaibhavKadam2004

Then use:
git remote add origin https://github.com/VaibhavKadam2004/placement-portal.git
```

---

## Step-by-Step

### Step 1: Find Your Username
- Go to GitHub profile
- Look for: `@your_username`
- Note this username

### Step 2: Copy the Template
```
git remote add origin https://github.com/YOUR_USERNAME/placement-portal.git
```

### Step 3: Replace YOUR_USERNAME
Delete `YOUR_USERNAME` and type your actual username

**Before:**
```
https://github.com/YOUR_USERNAME/placement-portal.git
```

**After (if username is myname):**
```
https://github.com/myname/placement-portal.git
```

### Step 4: Run in PowerShell
Paste the command (with your username) into PowerShell and press Enter

---

## ✅ How to Verify

After running the command, verify it worked:

```powershell
git remote -v
```

**Good (you see your username):**
```
origin  https://github.com/myusername/placement-portal.git (fetch)
origin  https://github.com/myusername/placement-portal.git (push)
```

**Bad (still shows YOUR_USERNAME):**
```
origin  https://github.com/YOUR_USERNAME/placement-portal.git (fetch)
origin  https://github.com/YOUR_USERNAME/placement-portal.git (push)
```

If bad, run the command again with your actual username.

---

## ⚠️ Important Notes

1. **Case matters:** `MyName` ≠ `myname`
2. **No brackets:** Remove any `[]` or `{}`
3. **No spaces:** Usernames have no spaces
4. **Exact spelling:** Match exactly what GitHub shows
5. **Keep the rest:** Only replace `YOUR_USERNAME`, keep `/placement-portal.git`

---

## 📝 Your Personal Command

**Your GitHub username: ________________**

Replace `YOUR_USERNAME` above, then your command becomes:

```
git remote add origin https://github.com/YOUR_USERNAME/placement-portal.git
```

---

## 🚀 All Three Commands Together

```powershell
# Remove old connection
git remote remove origin

# Add new connection (REPLACE YOUR_USERNAME!)
git remote add origin https://github.com/YOUR_USERNAME/placement-portal.git

# Push to GitHub
git push -u origin main
```

---

## 💡 Remember

**YOUR_USERNAME is NOT your email!**

| What It's NOT | What It IS |
|--------------|-----------|
| ❌ vaibhav@gmail.com | ✅ VaibhavKadam2004 |
| ❌ john@company.com | ✅ john_developer |
| ❌ Your real name | ✅ Your GitHub handle |

---

**That's it! Just replace and you're good to go! 🎉**
