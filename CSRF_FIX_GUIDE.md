# 🔐 CSRF Token Error - Fix Guide

## Problem
You're getting: **"CSRF verification failed. Request aborted."**

## Root Causes & Solutions

### ✅ Solution 1: Clear Cookies & Reload (Most Common)

1. **Clear Browser Cookies:**
   - Press `Ctrl+Shift+Delete` (Windows)
   - Select "All time" for time range
   - Check ✅ "Cookies"
   - Click "Clear data"

2. **Reload the page:**
   - Press `Ctrl+F5` (hard refresh)
   - Or `Ctrl+Shift+R`

3. **Try the form again**

---

### ✅ Solution 2: If Clear Cookies Didn't Work

1. **Close all browser tabs to this site**
   - This clears session state

2. **Open new tab and navigate to:**
   ```
   http://127.0.0.1:8000
   ```

3. **Login fresh**
   - Your session will be clean

4. **Try the form again**

---

### ✅ Solution 3: Use Private/Incognito Window

1. **Open Private Window:**
   - Press `Ctrl+Shift+N` (Chrome/Edge)
   - Or `Ctrl+Shift+P` (Firefox)

2. **Go to:**
   ```
   http://127.0.0.1:8000
   ```

3. **Login and test**

---

### ✅ Solution 4: Restart Django Server

1. **Stop the server:**
   - Press `Ctrl+C` in terminal

2. **Wait 2 seconds**

3. **Restart:**
   ```bash
   python manage.py runserver
   ```

4. **Reload browser:** `Ctrl+F5`

5. **Test again**

---

### ✅ Solution 5: Verify Server Settings (Already Done ✅)

Settings have been updated with:
```python
CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1:8000', 'http://localhost:8000']
CSRF_COOKIE_SECURE = False  # OK for development
CSRF_COOKIE_HTTPONLY = False  # Allows JavaScript to access token
```

---

## Which Forms Have CSRF Protection?

✅ **Protected (have POST forms with `{% csrf_token %}`):**
- Dream Company form
- Interview Experience submission
- TPO Approval/Reject buttons

✅ **Also Protected (GET pages, but forms included):**
- Student Dashboard
- Student Profile
- All authenticated pages

---

## Testing Checklist

After applying fixes:

- [ ] **Dream Company:** `/jobs/dream-company/` → Can submit company name
- [ ] **Prep Vault:** `/jobs/prep-vault/` → Can browse experiences
- [ ] **Interview Experience:** `/jobs/interview-experience/submit/` → Can submit form
- [ ] **TPO Approval:** `/jobs/tpo/interview-experiences/` → Can approve/reject

---

## Browser Troubleshooting

### If you see "CSRF cookie not set"
```bash
# This means Django isn't setting cookies properly

# Solution: Restart server
python manage.py runserver

# Then clear browser cookies
Ctrl+Shift+Delete → Select "All time" → Check "Cookies" → Clear
```

### If it says "CSRF token from POST incorrect"
```bash
# This means the token in the form doesn't match

# Solution:
1. Reload the page (not just refresh, clear cache)
   Ctrl+Shift+Delete → Clear cache + cookies
2. Close all tabs to the site
3. Open fresh browser tab
4. Go to http://127.0.0.1:8000
5. Try again
```

### If private window works but regular doesn't
```bash
# Your browser cache/cookies are corrupted

# Solution:
1. Clear all cookies:
   Ctrl+Shift+Delete → "All time" → "Cookies"
2. Clear browsing data:
   Ctrl+Shift+Delete → "All time" → Check all boxes
3. Restart browser completely
4. Try again
```

---

## Developer Debugging

### Check if CSRF token is in HTML

1. **Open page where form is:**
   - Go to `/jobs/dream-company/`

2. **Right-click → "Inspect" or press `F12`**

3. **In DevTools Console, paste:**
   ```javascript
   console.log(document.querySelector('[name="csrfmiddlewaretoken"]'))
   ```

4. **If it shows an input element = ✅ Token is present**
   ```
   <input type="hidden" name="csrfmiddlewaretoken" value="...">
   ```

5. **If it shows `null` = ❌ Token is MISSING**

---

### Check Browser Cookies

1. **Open DevTools:** `F12`
2. **Go to "Application" tab**
3. **Click "Cookies" → select the domain**
4. **Look for `csrftoken` cookie**
   - Should see value like: `abcd1234...`

If missing:
```bash
# Restart server and reload page with Ctrl+F5
python manage.py runserver
```

---

### Check Server Logs

When you get CSRF error, Django logs it. Look for:

```
[WARNING] CSRF token missing or incorrect.
```

This appears in the terminal running `python manage.py runserver`

---

## Permanent Fix (If issues persist)

### Step 1: Verify All Templates Have CSRF Tokens

**Check each template:**

```bash
# Check if CSRF tokens are in forms
grep -r "csrf_token" templates/
```

Should show:
```
templates/jobs/dream_company.html:{% csrf_token %}
templates/jobs/interview_experience_form.html:{% csrf_token %}
templates/jobs/tpo_interview_experiences.html:{% csrf_token %}
```

### Step 2: Add CSRF Exemption (If Needed)

For specific views that need CSRF bypass (rare):

```python
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  # CAREFUL - only for API endpoints
def my_view(request):
    pass
```

---

## Step-by-Step Resolution

1. **Clear cookies:**
   ```
   Ctrl+Shift+Delete → All time → Cookies → Clear
   ```

2. **Hard reload:**
   ```
   Ctrl+F5
   ```

3. **If still fails:**
   ```bash
   # Stop server (Ctrl+C)
   # Restart server
   python manage.py runserver
   ```

4. **Try new browser tab:**
   ```
   Ctrl+N (new window)
   Ctrl+Shift+N (private window)
   ```

5. **If private window works:**
   - Clear all browser data (not just cookies)
   - Restart browser

---

## Quick Command Reference

```bash
# Restart Django server
python manage.py runserver

# Check system
python manage.py check

# Clear session data (if needed)
python manage.py clearsessions

# Check Django version
python manage.py --version

# Verify CSRF is in template
grep -n "csrf_token" templates/jobs/interview_experience_form.html
```

---

## ✨ Expected Behavior

**Correct Flow:**
1. Load page with form → Django creates CSRF cookie
2. JavaScript/HTML reads cookie → Sets in hidden form field
3. Submit form → Django validates token matches
4. ✅ Form processes successfully

**If CSRF fails at any step → Error page appears**

---

## Need More Help?

**Try these exact steps in order:**

```bash
# 1. Stop server
Ctrl+C

# 2. Clear cache
python manage.py clearsessions

# 3. Restart server
python manage.py runserver

# 4. In browser:
# - Ctrl+Shift+Delete (Clear cookies)
# - Ctrl+F5 (Hard reload)
# - Try form again
```

If still failing, check:
- Is JavaScript enabled in browser?
- Are cookies enabled?
- Is DEBUG = True in settings.py?

---

**Status:** ✅ All templates have `{% csrf_token %}`  
**Settings:** ✅ CSRF middleware configured  
**Server:** ✅ Running with CSRF protection enabled
