import asyncio, requests, json, time, os
from pyvirtualdisplay import Display
from fake_useragent import UserAgent
from pyppeteer import launch

print("Loading config")
with open('config.json') as handle: config = json.loads(handle.read())

class aeza():

    async def browse(self):
        if config['headless']:
            print("Starting virtual display")
            display = Display(visible=0, size=(1920, 1080))
            display.start()

        browser = await launch(
            headless=config['headless'], 
            autoClose=False, 
            executablePath=config['executablePath'],
            args=[
                '--start-maximized', 

                '--disable-infobars'
            ]
        )

        page = await browser.newPage()

        # Set viewport to full window size
        await page.setViewport({
            'width': 1280, 
            'height': 720,
            'deviceScaleFactor': 1
        })

        ua = UserAgent()
        userAgent = ua.chrome
        print(f"Using {userAgent}")
        await page.setUserAgent(userAgent)
        await page.goto(f"https://discord.com/channels/1332521485302104084/1332521485763608618")
        await asyncio.sleep(3)

        await page.focus('input[name="email"]')
        await page.keyboard.type(config['username'], delay=100)
        await page.focus('input[name="password"]')
        await page.keyboard.type(config['password'], delay=100)

        await page.click('button[type="submit"]')
        await asyncio.sleep(10)

        messageSelector = '[aria-label="Message #general"]'
        await page.waitForSelector(messageSelector)
        await page.type(messageSelector, 'Hello from Puppeteer!')
        await page.keyboard.press('Enter')

        # Return the browser and page objects for continued use
        return {
            'browser': browser,
            'page': page,
            'display': display if config['headless'] else None
        }

    async def run_continuous(self):
        # Open initial browser session
        session = await self.browse()
        
        try:
            while True:
                # Example of performing repeated actions
                # You can modify this loop with your specific requirements
                await asyncio.sleep(60)  # Wait for 60 seconds between actions
                
                # Example of taking a new action
                await session['page'].reload()
                print("Page reloaded")
                
                # Add any specific commands or checks you want to perform
                # For instance, you might want to check for something on the page
                # or perform periodic actions
                
        except Exception as e:
            print(f"An error occurred: {e}")
        
        finally:
            # Cleanup when done
            await session['page'].close()
            await session['browser'].close()
            if session['display']:
                session['display'].stop()

# Async main function to run the continuous browsing
async def main():
    Aeza = aeza()
    await Aeza.run_continuous()

# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())