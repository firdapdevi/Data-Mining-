import time
import csv
import requests
from lxml import html
from selenium import webdriver


class AppCrawler:
    def __init__(self, starting_url, depth):
        self.starting_url = starting_url
        self.depth = depth
        self.apps = []

    def get_app_from_link(self, link):
		start_page = requests.get(link)
		tree = html.fromstring(start_page.text)

		Name = tree.xpath('//h1[@class="stock-profile f16"]/text()')[0]
		Board = tree.xpath('//li[@class="f14"]/text()')[0]
		StockCode = tree.xpath('//li[@class="f14"]/text()')[1]
		
		Price = tree.xpath('//td[@id="slcontent_0_ileft_0_lastdonetext"]/text()')[0]
		
		Volume = tree.xpath('//td[@id="slcontent_0_ileft_0_voltext"]/text()')[0]

		Date = tree.xpath('//span[@id="slcontent_0_ileft_0_datetxt"]/text()')[0]
		Time = tree.xpath('//span[@id="slcontent_0_ileft_0_timetxt"]/text()')[0]

		Board = Board[3:]
		StockCode = StockCode[3:]
		Date = Date[10:].replace(" |", "")	

		data = Name+","+Board+","+StockCode+","+\
				Price+","+Volume+","+Date+","+Time+"\n"

		with open("/Users/stephen/Desktop/stock_data.csv", "a") as wf:
		    wf.write(data)

		return

    def crawl(self):
        self.get_app_from_link(self.starting_url)
        return

    
class GetData:
	def __init__(self, alphabet):
		self.alphabet = alphabet

	def writeData(self):
	    for alpha in self.alphabet:
	        driver = webdriver.Chrome(executable_path=r'/Users/stephen/Desktop/chromedriver')
	        driver.get("https://www.thestar.com.my/business/marketwatch/stock-list/?alphabet="+alpha)
	        company_links = driver.find_elements_by_xpath('//tr[@class="linedlist"]//a')
	        for link in company_links:
	            value = link.get_attribute('href')
	            crawler = AppCrawler(value, 0)
	            crawler.crawl()
	        driver.quit()
            
start = time.time()

alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M",\
	    			"N","O","P","Q","R","S","T","U","V","W","X","Y","Z", "0-9"]
data = GetData(alphabet)
data.writeData()

end = time.time()
hours, rem = divmod(end-start, 3600)
minutes, seconds = divmod(rem, 60)
print("{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds))

