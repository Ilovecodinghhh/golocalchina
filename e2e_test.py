"""
E2E Test: Simulate a Guide and a Tourist using GoLocalChina.
Takes screenshots at every step, logs all issues found.
"""
import time
import json
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PwTimeout

BASE = "https://golocalchina.vercel.app"
API = "https://golocalchina-production.up.railway.app"
SHOTS = Path("test-screenshots")
SHOTS.mkdir(exist_ok=True)

issues = []
step_num = 0

def shot(page, name):
    global step_num
    step_num += 1
    path = SHOTS / f"{step_num:02d}_{name}.png"
    page.screenshot(path=str(path), full_page=True)
    print(f"  📸 {path.name}")
    return path

def log_issue(severity, description, screenshot=None):
    issue = {"severity": severity, "description": description, "screenshot": screenshot}
    issues.append(issue)
    icon = {"critical": "🔴", "major": "🟡", "minor": "⚪"}.get(severity, "⚪")
    print(f"  {icon} ISSUE: {description}")

def check_page_errors(page, context):
    """Check for console errors and broken images."""
    # Check broken images
    broken = page.evaluate("""() => {
        return Array.from(document.querySelectorAll('img')).filter(img => !img.complete || img.naturalWidth === 0).map(img => img.src);
    }""")
    if broken:
        log_issue("major", f"[{context}] Broken images: {broken[:3]}")
    
    # Check if page loaded
    title = page.title()
    if not title or "404" in title or "error" in title.lower():
        log_issue("critical", f"[{context}] Page title indicates error: '{title}'")

def wait_and_check(page, context, timeout=5000):
    """Wait for network idle and check for issues."""
    try:
        page.wait_for_load_state("networkidle", timeout=timeout)
    except PwTimeout:
        pass
    check_page_errors(page, context)


def run_guide_flow(browser):
    """Simulate a local guide who wants to promote their trip."""
    print("\n" + "="*60)
    print("🧭 GUIDE FLOW: Li Wei, Beijing history guide")
    print("="*60)
    
    context = browser.new_context(viewport={"width": 1280, "height": 800})
    page = context.new_page()
    
    # Collect console errors
    console_errors = []
    page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
    
    # 1. Visit homepage
    print("\n[Step 1] Visit homepage")
    page.goto(BASE, wait_until="networkidle", timeout=15000)
    wait_and_check(page, "Homepage")
    shot(page, "guide_01_homepage")
    
    # Check hero images loaded
    hero_visible = page.evaluate("() => document.querySelector('div[style*=\"background-image\"]') !== null")
    if not hero_visible:
        log_issue("major", "Hero background images not rendering")
    
    # Check if CTA button exists
    cta = page.query_selector("text=Find a Guide")
    if not cta:
        log_issue("major", "Homepage missing 'Find a Guide' CTA button")
    
    # 2. Navigate to Register
    print("\n[Step 2] Click Sign Up")
    page.click("text=Sign Up")
    page.wait_for_url("**/register", timeout=5000)
    wait_and_check(page, "Register page")
    shot(page, "guide_02_register")
    
    # 3. Fill registration — Step 1: Email + Captcha
    print("\n[Step 3] Register as guide — email + captcha")
    ts = int(time.time())
    guide_email = f"guide_test_{ts}@test.com"
    
    email_input = page.query_selector('input[type="email"]')
    if not email_input:
        log_issue("critical", "Register page: no email input found")
        context.close()
        return None
    
    page.fill('input[type="email"]', guide_email)
    
    # Solve captcha
    captcha_text = page.text_content("text=/What is/")
    if captcha_text:
        import re
        nums = re.findall(r'\d+', captcha_text)
        if len(nums) >= 2:
            answer = int(nums[0]) + int(nums[1])
            page.fill('input[type="number"]', str(answer))
    else:
        log_issue("major", "Captcha question not found on register page")
    
    shot(page, "guide_03_captcha_filled")
    
    # Click send code
    page.click("text=Send Verification Code")
    time.sleep(3)
    shot(page, "guide_04_code_sent")
    
    # Check if code was displayed (MVP demo mode)
    demo_code = page.text_content("text=/Your code is/")
    if demo_code:
        import re
        code_match = re.search(r'\d{6}', demo_code)
        if code_match:
            code = code_match.group()
            print(f"  Got demo code: {code}")
            page.fill('input[placeholder="123456"]', code)
            page.click("text=Verify Code")
            time.sleep(2)
            shot(page, "guide_05_code_verified")
        else:
            log_issue("critical", "Could not extract verification code from demo message")
            context.close()
            return None
    else:
        log_issue("critical", "No demo code displayed after sending verification code")
        # Check for error
        error_el = page.query_selector('[role="alert"]')
        if error_el:
            log_issue("critical", f"Error on send code: {error_el.text_content()}")
        context.close()
        return None
    
    # Step 3: Fill password + profile
    print("\n[Step 4] Fill password + select Guide role")
    time.sleep(1)
    name_input = page.query_selector('input[type="text"]')  # Display name
    if name_input:
        name_input.fill("Li Wei")
    
    pw_input = page.query_selector('input[type="password"]')
    if pw_input:
        pw_input.fill("TestGuide#123")
    
    shot(page, "guide_06_password")
    
    # Select Guide role
    guide_btn = page.query_selector("text=🧭 Local Guide")
    if guide_btn:
        guide_btn.click()
    else:
        log_issue("major", "Guide role button not found")
    
    time.sleep(1)
    shot(page, "guide_07_role_selected")
    
    # Click Create Account
    create_btn = page.query_selector("text=Create Account")
    if create_btn:
        if create_btn.is_disabled():
            log_issue("major", "Create Account button is disabled — password might not meet requirements")
            shot(page, "guide_07b_button_disabled")
        else:
            create_btn.click()
            time.sleep(3)
            shot(page, "guide_08_registered")
    else:
        log_issue("critical", "Create Account button not found")
    
    # 4. Check if we landed on dashboard
    print("\n[Step 5] Check dashboard")
    current_url = page.url
    if "/dashboard" not in current_url:
        log_issue("major", f"After registration, not on dashboard. URL: {current_url}")
        # Try navigating manually
        page.goto(f"{BASE}/dashboard", timeout=10000)
        time.sleep(2)
    
    wait_and_check(page, "Guide dashboard")
    shot(page, "guide_09_dashboard")
    
    # 5. Try creating a listing
    print("\n[Step 6] Create a new listing")
    create_listing_btn = page.query_selector("text=Create New Listing")
    if create_listing_btn:
        create_listing_btn.click()
        time.sleep(1)
        shot(page, "guide_10_new_listing_dialog")
        
        # Fill listing form
        title_input = page.query_selector('input[name="title"], label:has-text("Title") + div input, input[placeholder*="Beijing"]')
        if not title_input:
            # Try finding by label text
            inputs = page.query_selector_all('input[type="text"]')
            if inputs:
                inputs[0].fill("Hidden Hutongs & Imperial Secrets — Half Day")
        else:
            title_input.fill("Hidden Hutongs & Imperial Secrets — Half Day")
        
        # Fill textareas
        textareas = page.query_selector_all('textarea')
        if len(textareas) >= 1:
            textareas[0].fill("Explore the hidden alleys of old Beijing that tourists never find. Drink tea in a 400-year-old courtyard.")
        if len(textareas) >= 2:
            textareas[1].fill("We start at 8am at Nanluoguxiang. I'll take you through alleys that haven't changed in 600 years. We'll visit my favorite jianbing vendor, drink tea in a courtyard home, explore the Drum and Bell towers from a local perspective, and end with the best roast duck in Beijing — not the tourist one.")
        
        shot(page, "guide_11_listing_filled")
        
        # Click publish
        publish_btn = page.query_selector("text=Publish Listing")
        if publish_btn:
            publish_btn.click()
            time.sleep(3)
            shot(page, "guide_12_listing_published")
        else:
            log_issue("major", "Publish Listing button not found")
    else:
        log_issue("critical", "Create New Listing button not found on guide dashboard")
    
    # 6. Check if listing appears
    print("\n[Step 7] Verify listing appears in dashboard")
    time.sleep(2)
    shot(page, "guide_13_dashboard_with_listing")
    listing_visible = page.query_selector("text=Hidden Hutongs")
    if not listing_visible:
        log_issue("major", "Created listing does not appear in guide dashboard")
    
    # 7. Check Requests tab
    print("\n[Step 8] Check requests tab")
    requests_tab = page.query_selector("text=Requests")
    if requests_tab:
        requests_tab.click()
        time.sleep(1)
        shot(page, "guide_14_requests_tab")
    else:
        log_issue("minor", "No Requests tab found for guide")
    
    # Log any console errors
    if console_errors:
        log_issue("minor", f"Console errors during guide flow: {console_errors[:5]}")
    
    context.close()
    return guide_email


def run_tourist_flow(browser, guide_email=None):
    """Simulate a tourist looking for a local experience."""
    print("\n" + "="*60)
    print("🌍 TOURIST FLOW: Sarah, American tourist visiting Beijing")
    print("="*60)
    
    context = browser.new_context(viewport={"width": 1280, "height": 800})
    page = context.new_page()
    
    console_errors = []
    page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
    
    # 1. Visit homepage
    print("\n[Step 1] Visit homepage")
    page.goto(BASE, wait_until="networkidle", timeout=15000)
    wait_and_check(page, "Tourist - Homepage")
    shot(page, "tourist_01_homepage")
    
    # Check hero image rotation
    time.sleep(6)  # Wait for one rotation
    shot(page, "tourist_02_homepage_rotated")
    
    # 2. Click "Find a Guide"
    print("\n[Step 2] Click Find a Guide")
    page.click("text=Find a Guide")
    page.wait_for_url("**/guides", timeout=5000)
    wait_and_check(page, "Tourist - Guides page")
    shot(page, "tourist_03_guides_page")
    
    # Check guide cards loaded
    cards = page.query_selector_all('[class*="MuiCard"]')
    print(f"  Found {len(cards)} guide cards")
    if len(cards) == 0:
        log_issue("critical", "No guide cards visible on /guides page")
    
    # 3. Filter by Beijing
    print("\n[Step 3] Filter by Beijing")
    city_select = page.query_selector('[id*="city"], [aria-label*="City"]')
    if city_select:
        city_select.click()
        time.sleep(0.5)
        beijing_opt = page.query_selector("text=Beijing")
        if beijing_opt:
            beijing_opt.click()
            time.sleep(0.5)
    
    search_btn = page.query_selector("text=Search Guides")
    if search_btn:
        search_btn.click()
        time.sleep(1)
    
    shot(page, "tourist_04_filtered_beijing")
    
    # 4. Click on first guide
    print("\n[Step 4] View guide detail")
    view_btn = page.query_selector("text=View Details")
    if view_btn:
        view_btn.click()
        time.sleep(2)
        wait_and_check(page, "Tourist - Guide detail")
        shot(page, "tourist_05_guide_detail")
        
        # Check sections exist
        payment_section = page.query_selector("text=Payment Methods")
        if not payment_section:
            log_issue("minor", "Payment Methods section not visible on guide detail")
        
        listings = page.query_selector_all("text=Request to Connect")
        print(f"  Found {len(listings)} 'Request to Connect' buttons")
        if len(listings) == 0:
            log_issue("major", "No 'Request to Connect' buttons on guide detail page")
    else:
        log_issue("critical", "No 'View Details' button found on guide cards")
        context.close()
        return
    
    # 5. Register as tourist
    print("\n[Step 5] Register as tourist")
    page.goto(f"{BASE}/register", timeout=10000)
    time.sleep(2)
    shot(page, "tourist_06_register")
    
    ts = int(time.time())
    tourist_email = f"tourist_test_{ts}@test.com"
    
    # Step 1: Email + captcha
    page.fill('input[type="email"]', tourist_email)
    captcha_text = page.text_content("text=/What is/")
    if captcha_text:
        import re
        nums = re.findall(r'\d+', captcha_text)
        if len(nums) >= 2:
            page.fill('input[type="number"]', str(int(nums[0]) + int(nums[1])))
    
    page.click("text=Send Verification Code")
    time.sleep(3)
    
    demo_code = page.text_content("text=/Your code is/")
    if demo_code:
        import re
        code_match = re.search(r'\d{6}', demo_code)
        if code_match:
            page.fill('input[placeholder="123456"]', code_match.group())
            page.click("text=Verify Code")
            time.sleep(2)
    else:
        log_issue("critical", "Tourist registration: no demo code displayed")
        context.close()
        return
    
    # Step 3: Password + profile
    time.sleep(1)
    inputs = page.query_selector_all('input[type="text"]')
    if inputs:
        inputs[0].fill("Sarah Johnson")
    page.fill('input[type="password"]', "Tourist#2024!")
    
    # Select Tourist role (should be default)
    tourist_btn = page.query_selector("text=🌍 Tourist")
    if tourist_btn:
        tourist_btn.click()
    
    # Select country (if visible)
    time.sleep(0.5)
    country_select = page.query_selector('[aria-label*="Country"], label:has-text("Country")')
    if country_select:
        pass  # Country dropdown might need special handling
    
    shot(page, "tourist_07_filled_registration")
    
    create_btn = page.query_selector("text=Create Account")
    if create_btn and not create_btn.is_disabled():
        create_btn.click()
        time.sleep(3)
        shot(page, "tourist_08_registered")
    else:
        log_issue("major", "Tourist Create Account button disabled or not found")
        shot(page, "tourist_08_button_issue")
    
    # 6. Go to guides page and request a connection
    print("\n[Step 6] Browse and send connection request")
    page.goto(f"{BASE}/guides", timeout=10000)
    time.sleep(2)
    shot(page, "tourist_09_guides_logged_in")
    
    # Click first guide
    view_btn = page.query_selector("text=View Details")
    if view_btn:
        view_btn.click()
        time.sleep(2)
        shot(page, "tourist_10_guide_detail_logged_in")
        
        # Click Request to Connect
        connect_btn = page.query_selector("text=Request to Connect")
        if connect_btn:
            connect_btn.click()
            time.sleep(1)
            shot(page, "tourist_11_connect_dialog")
            
            # Fill date
            date_input = page.query_selector('input[type="date"]')
            if date_input:
                date_input.fill("2026-07-15")
            
            # Fill notes
            notes = page.query_selector('textarea')
            if notes:
                notes.fill("Hi! I'm visiting Beijing for 3 days. I love history and street food. Would love to explore hutongs and find the best local restaurants!")
            
            shot(page, "tourist_12_request_filled")
            
            # Send
            send_btn = page.query_selector("button:has-text('Send Request')")
            if send_btn:
                send_btn.click()
                time.sleep(3)
                shot(page, "tourist_13_request_sent")
        else:
            log_issue("major", "Request to Connect button not found on guide detail")
    
    # 7. Check dashboard for request
    print("\n[Step 7] Check dashboard for sent request")
    page.goto(f"{BASE}/dashboard", timeout=10000)
    time.sleep(2)
    wait_and_check(page, "Tourist dashboard")
    shot(page, "tourist_14_dashboard")
    
    # Check if request shows
    request_visible = page.query_selector("text=pending")
    if request_visible:
        print("  ✅ Request shows as pending in dashboard!")
    else:
        log_issue("major", "Sent request not visible in tourist dashboard")
    
    # 8. Check How It Works page
    print("\n[Step 8] Check How It Works page")
    page.goto(f"{BASE}/how-it-works", timeout=10000)
    time.sleep(2)
    wait_and_check(page, "How It Works")
    shot(page, "tourist_15_how_it_works")
    
    # Log console errors
    if console_errors:
        log_issue("minor", f"Console errors during tourist flow: {console_errors[:5]}")
    
    context.close()


def main():
    print("🚀 GoLocalChina E2E Test — Guide + Tourist Simulation")
    print(f"Target: {BASE}")
    print(f"Screenshots: {SHOTS}/")
    print()
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        
        # Run both flows
        guide_email = run_guide_flow(browser)
        run_tourist_flow(browser, guide_email)
        
        browser.close()
    
    # Report
    print("\n" + "="*60)
    print(f"📋 ISSUE REPORT — {len(issues)} issues found")
    print("="*60)
    
    for sev in ["critical", "major", "minor"]:
        sev_issues = [i for i in issues if i["severity"] == sev]
        if sev_issues:
            icon = {"critical": "🔴", "major": "🟡", "minor": "⚪"}[sev]
            print(f"\n{icon} {sev.upper()} ({len(sev_issues)}):")
            for i, issue in enumerate(sev_issues, 1):
                print(f"  {i}. {issue['description']}")
    
    if not issues:
        print("\n✅ NO ISSUES FOUND — Both guide and tourist flows completed successfully!")
    
    # Save report
    with open(SHOTS / "report.json", "w") as f:
        json.dump({"issues": issues, "total": len(issues), "screenshots": step_num}, f, indent=2)
    
    print(f"\n📸 {step_num} screenshots saved to {SHOTS}/")
    print(f"📄 Report saved to {SHOTS}/report.json")
    
    return issues


if __name__ == "__main__":
    main()
