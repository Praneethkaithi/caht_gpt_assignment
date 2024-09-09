from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # Launch a new browser instance
    browser = p.chromium.launch()
    page = browser.new_page()

    # Navigate to the website
    page.goto('https://claude.ai/new')

    # Click on the file input to open the file dialog
    page.set_input_files('input[type="file"]', 'path/to/image.jpg')

    # Optionally submit the form if needed
    element = page.query_selector('/html/body/div[2]/div/main/div[2]/div/fieldset/div[2]/div/div/div/div/div[1]/div/button[1]')

    element = frame.query_selector('input[type="file"]')
    page.click('button[type="submit"]')

    # Close the browser
    browser.close()
