from bs4 import BeautifulSoup
import requests
import pymysql.cursors

def get_url(urls):

    source = requests.get(urls[0]).text
    soup = BeautifulSoup(source, "lxml")
    news_links = soup.find_all("div", {"class": "views-field views-field-title"})
    company_name = urls[1]

    for i in news_links:
        headline = i.find("a").get_text()
        url = i.find("a").attrs["href"]
        get_data(company_name,headline,url)


def get_data(company_name,headline,url):
    article = ""
    new_url = "https://www.theedgemarkets.com" + url
    print(new_url)
    try:
         source = requests.get(new_url).text
         soup = BeautifulSoup(source, "lxml")
         news = soup.find("div",{"property": "content:encoded"}).find_all("p")
         for i in news:
             article += i.getText()
         news_date = soup.find("span", {"class": "post-created"}).getText()
         store(news_date,company_name, headline,article,new_url)
    except:
        print("Wrong! Check Again!")


def store(datenews,list_of_company, title, content, news_links):


    conn = pymysql.connect(host="localhost", user="root", passwd="password", db="mysql")
    cur = conn.cursor()
    try:
        cur.execute("USE News")
        sql_query = "INSERT INTO companynews (datenews,list_of_company, title, content, news_links)" \
                    " VALUES (%s,%s,%s,%s,%s)"
        try:
            cur.execute(sql_query,(datenews,list_of_company, title, content, news_links))

        except ValueError:
                print("Finish")
        cur.connection.commit()

    finally:
        cur.close()
        conn.close()


company_news_urls = []
company_names = ["DIGI","MAYBANK","GENTING", "MAXIS", "RHB"]


for item in company_names:
    for i in range (0,5):
        company_news_urls.append(["https://www.theedgemarkets.com/search-results?page={0}&keywords={1}".format(i,item), item])
for item in company_news_urls:
    get_url(item)