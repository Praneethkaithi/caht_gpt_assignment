import asyncio
from pyppeteer import launch

async def upload_image():
    # Set the path to your local Chrome installation
    browser = await launch(executablePath="C:/Program Files/Google/Chrome/Application/chrome.exe", headless=False)

    # Open a new page
    page = await browser.newPage()

    # Go to the URL
    await page.goto('https://claude.ai/new')

    # Wait for the file input element (replace with actual selector)
    #input_element = await page.waitForSelector(')
    element = await page.waitForXPath('//*[@id="email"]')
    await element.click()
    await element.type('kaithipraneeth98@gmail.com')
    await page.keyboard.press('Enter')
    element = await page.waitForXPath('/html/body/div[2]/div/div[1]/main/div[1]/div[1]/div[1]/div/button')
    await element.click()
    element = await page.waitForXPath('//*[@id="identifierId"]')
    await element.type('kaithipraneeth98@gmail.com')
    await page.keyboard.press('Enter')


    # Upload the file
    #await input_element.uploadFile('C:/path/to/image.png')
    # Close the browser after a short delay
    await asyncio.sleep(5000)
   # await browser.close()

# Run the script
asyncio.get_event_loop().run_until_complete(upload_image())
