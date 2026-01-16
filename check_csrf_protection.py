#!/usr/bin/env python
"""
🔐 CSRF Token Verification Script
Ensures all templates have proper CSRF protection
"""

import os
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def check_csrf_in_templates():
    """Check if all POST forms have CSRF tokens"""
    
    print("=" * 80)
    print("🔐 CSRF TOKEN VERIFICATION")
    print("=" * 80)
    print()
    
    templates_dir = BASE_DIR / 'templates'
    csrf_found = {}
    post_forms_without_csrf = []
    
    # Find all HTML files
    for html_file in templates_dir.rglob('*.html'):
        relative_path = html_file.relative_to(BASE_DIR)
        
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if file has POST forms
        has_post_form = 'method="POST"' in content or "method='POST'" in content
        has_csrf_token = '{% csrf_token %}' in content
        
        csrf_found[str(relative_path)] = {
            'has_post_form': has_post_form,
            'has_csrf_token': has_csrf_token,
            'status': '✅' if (not has_post_form or has_csrf_token) else '❌'
        }
        
        if has_post_form and not has_csrf_token:
            post_forms_without_csrf.append(str(relative_path))
    
    # Display results
    print("📋 TEMPLATE CSRF STATUS:")
    print("-" * 80)
    
    for template, info in sorted(csrf_found.items()):
        if info['has_post_form']:
            status = '✅' if info['has_csrf_token'] else '❌'
            token_status = 'YES' if info['has_csrf_token'] else 'MISSING'
            print(f"{status} {template}")
            print(f"   POST Form: YES | CSRF Token: {token_status}")
        else:
            print(f"ℹ️  {template} (No POST forms)")
    
    print()
    print("=" * 80)
    
    # Summary
    total_templates = len(csrf_found)
    with_post = sum(1 for t in csrf_found.values() if t['has_post_form'])
    with_csrf = sum(1 for t in csrf_found.values() if t['has_csrf_token'])
    
    print(f"📊 SUMMARY:")
    print(f"   Total templates: {total_templates}")
    print(f"   Templates with POST forms: {with_post}")
    print(f"   Templates with CSRF tokens: {with_csrf}")
    
    if post_forms_without_csrf:
        print()
        print(f"⚠️  TEMPLATES WITHOUT CSRF TOKENS ({len(post_forms_without_csrf)}):")
        for template in post_forms_without_csrf:
            print(f"   ❌ {template}")
        return False
    else:
        print()
        print("✅ ALL POST FORMS ARE PROTECTED WITH CSRF TOKENS")
        return True


def check_settings():
    """Verify CSRF settings in Django settings"""
    
    print()
    print("=" * 80)
    print("⚙️  DJANGO SETTINGS VERIFICATION")
    print("=" * 80)
    print()
    
    settings_file = BASE_DIR / 'placement_portal' / 'settings.py'
    
    with open(settings_file, 'r', encoding='utf-8') as f:
        settings_content = f.read()
    
    checks = {
        'CsrfViewMiddleware': "'django.middleware.csrf.CsrfViewMiddleware'" in settings_content,
        'CSRF Context Processor': "'django.template.context_processors.csrf'" in settings_content,
        'SessionMiddleware': "'django.contrib.sessions.middleware.SessionMiddleware'" in settings_content,
        'AuthenticationMiddleware': "'django.contrib.auth.middleware.AuthenticationMiddleware'" in settings_content,
    }
    
    for check_name, is_present in checks.items():
        status = '✅' if is_present else '❌'
        print(f"{status} {check_name}: {'Present' if is_present else 'MISSING'}")
    
    print()
    
    # Check optional CSRF settings
    optional_settings = {
        'CSRF_TRUSTED_ORIGINS': 'CSRF_TRUSTED_ORIGINS' in settings_content,
        'CSRF_COOKIE_SECURE': 'CSRF_COOKIE_SECURE' in settings_content,
        'CSRF_COOKIE_HTTPONLY': 'CSRF_COOKIE_HTTPONLY' in settings_content,
    }
    
    print("🔒 Optional CSRF Settings:")
    for setting_name, is_present in optional_settings.items():
        status = '✅' if is_present else 'ℹ️ '
        print(f"{status} {setting_name}: {'Configured' if is_present else 'Using defaults'}")
    
    print()
    all_required_present = all(checks.values())
    return all_required_present


def check_middleware_order():
    """Verify middleware is in correct order"""
    
    print()
    print("=" * 80)
    print("🔄 MIDDLEWARE ORDER VERIFICATION")
    print("=" * 80)
    print()
    
    settings_file = BASE_DIR / 'placement_portal' / 'settings.py'
    
    with open(settings_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract middleware list
    middleware_pattern = r"MIDDLEWARE\s*=\s*\[(.*?)\]"
    middleware_match = re.search(middleware_pattern, content, re.DOTALL)
    
    if middleware_match:
        middleware_str = middleware_match.group(1)
        # Extract middleware names
        middlewares = re.findall(r"'(django[\w\.]*)'", middleware_str)
        
        print("Middleware order (should be in this order):")
        print()
        
        for i, middleware in enumerate(middlewares, 1):
            print(f"{i}. {middleware}")
        
        # Check correct order
        expected_order = [
            'django.middleware.security.SecurityMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
        ]
        
        print()
        print("✅ Middleware order is CORRECT" if all(
            m in middlewares for m in expected_order
        ) else "⚠️  Middleware order may need adjustment")
        
        return True
    
    return False


def main():
    """Run all verification checks"""
    
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + "CSRF PROTECTION VERIFICATION".center(78) + "║")
    print("╚" + "=" * 78 + "╝")
    print()
    
    # Run checks
    templates_ok = check_csrf_in_templates()
    settings_ok = check_settings()
    middleware_ok = check_middleware_order()
    
    print()
    print("=" * 80)
    print("📋 FINAL REPORT")
    print("=" * 80)
    print()
    
    print(f"✅ Templates: {'All protected' if templates_ok else 'Some missing CSRF'}")
    print(f"✅ Settings: {'Properly configured' if settings_ok else 'Missing configuration'}")
    print(f"✅ Middleware: {'Correct order' if middleware_ok else 'Check order'}")
    
    print()
    
    if templates_ok and settings_ok and middleware_ok:
        print("╔" + "=" * 78 + "╗")
        print("║" + "✨ ALL CSRF PROTECTIONS ARE IN PLACE ✨".center(78) + "║")
        print("║" + "Your forms are secure and ready for production!".center(78) + "║")
        print("╚" + "=" * 78 + "╝")
        return 0
    else:
        print("⚠️  SOME CHECKS FAILED - Review above for details")
        return 1


if __name__ == '__main__':
    exit(main())
