from bs4 import BeautifulSoup
import re
from selenium import webdriver
import csv

url_start = "https://www.thestar.com.my/business/marketwatch/stocks/?qcounter="
driver = webdriver.Firefox()

def name_cat(url):

    urls = []
    driver.get(url)
    src = driver.execute_script("return document.documentElement.outerHTML")
    soup = BeautifulSoup(src,"lxml")
    companies_urls_list = soup.find("div", {"class": "btn-group btn-group-sm"}).find_all("a", {"class": "btn btn-default"})
    for link in companies_urls_list[20:]:
        urls.append(companies_urls(link.get("href")))


    print(urls)

    return urls

def companies_urls(url):

    url_list = []
    driver.get(url)
    src = driver.execute_script("return document.documentElement.outerHTML")
    soup = BeautifulSoup(src, "lxml")
    company_url_list = soup.find("table", {"class": "market-trans"}).find_all("a", href=re.compile("(.)*$"))
    for link in company_url_list:
        href = "https://www.thestar.com.my" + link.get("href")
        print(href)
        url_list.append(href)
    return url_list


def data_list(urls):
    data_li = []
    for url in urls:
        for _ in url:
            company_name,stock_code,raw_data = company_data(_)
            data_li.append((company_name,stock_code,raw_data))
    print(data_li)

    return data_li

def company_data(urls):
    raw_data = []
    driver.get(urls)
    src = driver.execute_script("return document.documentElement.outerHTML")
    soup = BeautifulSoup(src, "lxml")

    try:
        data_list = soup.find("table", {"class": "market-trans bot-15"}).find("tbody").findAll("td")
        for _ in data_list:
            raw_data.append(_.get_text())
        company_name = soup.find("h1", {"class": "stock-profile f16"}).get_text()
        com_stock_code = soup.find("ul", {"class": "stock-code"}).find_all("li", {"class": "f14"})
        stock_code = com_stock_code[1].contents[1].strip(" :")
        print(company_name, stock_code, raw_data)
    except ValueError:
        company_name = soup.find("h1", {"class": "stock-profile f16"}).get_text()
        com_stock_code = soup.find("ul", {"class": "stock-code"}).find_all("li", {"class": "f14"})
        stock_code = com_stock_code[1].contents[1].strip(" :")
        print(company_name, stock_code, raw_data)
    return company_name,stock_code, raw_data

if __name__ == "__main__":

    company_url_list = name_cat(url_start)
    actual_data = data_list(company_url_list)
    with open("Dataset.csv",mode="a") as csv_file:
        for _ in actual_data:
            writer = csv.writer(csv_file)
            writer.writerow(_)