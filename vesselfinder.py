import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


class VesselfinderSpider(scrapy.Spider):
    name = "countries"
    allowed_domains = ["vesselfinder.com"]
    start_urls = ["http://toscrape.com/"]  # URL doesn't really matter

    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
    }

    def parse(self, response):
        driver = webdriver.Chrome()
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--window-size=1920x1080")
        options.add_argument(
            "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36"
        )
        desired_capabilities = options.to_capabilities()

        driver = webdriver.Chrome(
            desired_capabilities=desired_capabilities, chrome_options=options
        )

        driver.get(
            "https://www.vesselfinder.com/vessels/COUGA-IMO-9414905-MMSI-477748900"
        )

        driver.implicitly_wait(10)

        wait = WebDriverWait(driver, 5)
        wait.until(EC.presence_of_element_located((By.ID, "port-calls")))

        ports = driver.find_elements_by_css_selector("tbody.pctable > tr > td > a")

        if not ports:
            print("====empty>>>>>>>>>>>")
        else:
            urls = [port.get_attribute("href") for port in ports]
            for url in urls:
                yield scrapy.Request(url=url, callback=self.parse_details)

        driver.quit()

    def parse_details(self, response):
        text = response.css("div.port-section > p::text").extract_first()
        yield {"text": text}
