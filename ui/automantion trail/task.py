from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Set up the Chrome WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Navigate to YouTube
driver.get('https://claude.ai/new')

# Optional: You can add more actions here

# Close the browser after 10 seconds
'''import time
time.sleep(10)
driver.quit()
'''