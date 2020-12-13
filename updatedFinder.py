import re
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
    def __init__ (self, url=""):
        self.url= "%s" % url
        
    def fetch_url(self):
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
            self.url
        )

        driver.implicitly_wait(10)

        wait = WebDriverWait(driver, 5)
        #wait.until(EC.presence_of_element_located((By.ID, "port-calls")))
        ports = driver.find_elements_by_css_selector("tbody > tr > td> div > a")
        #ports = driver.find_elements_by_css_selector("tbody.pctable > tr > td > a")
        if not ports:
            print("====empty>>>>>>>>>>>")
            port_urls = []
        else:
            port_urls = [port.get_attribute("href") for port in ports]

        driver.quit()

        return port_urls

    def parse(self, response):
        urls = self.fetch_url()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_details)

    def parse_details(self, response):
        port = response.css("div.page-header > h1::text").extract_first()
        context = response.css("div.port-section > p::text").extract_first()
        points = re.findall("[0-9.]+[NSEW]+", context)

        yield {"port": port, "points": points}
