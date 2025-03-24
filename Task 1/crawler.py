import time
import re
import tkinter as tk
from tkinter import scrolledtext, messagebox
import webbrowser
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
from bs4 import BeautifulSoup, NavigableString

# Setup Selenium WebDriver
options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)





#Crawling through webpage and Extracting Publicaction Data  
def read_html(soup):
    # Find the <ul> element with class "list-results"
    ul_element = soup.find("ul", class_="list-results")
    # print (ul_element)
    
    if ul_element:
        # Find all <li> elements within this <ul>
        li_elements = ul_element.find_all("li", class_=re.compile(r"list-result-item list-result-item-\d+"))
        # li_elements = ul_element.find_all("li", class_="list-result-item list-result-item-0")
        # print(li_elements)
        # Iterate over each <li> element and print its class attribute
        for li in li_elements:
            # print(li)
            h3_element = li.find("h3", class_="title")
            #print(h3_element)
            a_element = h3_element.find("a", class_="link")
            # Extract the href attribute from the <a> element
            link = a_element.get("href")
            # Extract the text inside the <span> element
            title = a_element.find("span").get_text(strip=True)
            auther_name = ""
            author_text = None
            next_node = h3_element.next_sibling

            # Loop through the siblings until we find a non-empty text node
            while next_node is not None:
                # Ensure that the node is a NavigableString (text)
                if isinstance(next_node, NavigableString):
                    text = next_node.strip()
                    if text:  # if non-empty after stripping whitespace
                        author_text = text
                        auther_name += author_text
                        break
                # Move to the next sibling node
                next_node = next_node.next_sibling
            a_element_name = li.find("a", class_="link person")
            # print(a_element_name)
            if a_element_name:
                author_link = a_element_name.get("href")
                span_text_name = a_element_name.find("span").get_text(strip=True)
                next_node_1 = a_element_name.next_sibling
                # Loop through the siblings until we find a non-empty text node
                while next_node_1 is not None:
                    # Ensure that the node is a NavigableString (text)
                    if isinstance(next_node_1, NavigableString):
                        text = next_node_1.strip()
                        if text:  # if non-empty after stripping whitespace
                            author_text_1 = text
                            auther_name = auther_name + span_text_name + author_text_1
                            break
                    # Move to the next sibling node
                    next_node_1 = next_node_1.next_sibling
            else:
                author_link=""
            date_element = li.find("span", class_="date")
            if date_element: 
                date = date_element.get_text("span")
            df.loc[len(df)] =[title,link,auther_name,author_link,date] 
            # print("iteration done")       
    else:
        print("No <ul> found with class 'list-results'")


# Retrives HTML Content and Navigate to multiple pages further it parses to read function 
def read(url):
    # The website you want to read
    driver.get(url)
    # Extract the page content (HTML source)
    page_source = driver.page_source
    # Use BeautifulSoup to prettify the HTML
    soup = BeautifulSoup(page_source, "html.parser")
    pretty_html = soup.prettify()
    # print(pretty_html)
    read_html(soup)
    next_element = soup.find("li", class_="next")
    # print(next_element)
    if next_element:
        # print("dgfhg123")
        next_link = next_element.find("a", class_="nextLink")
        # print(next_link)
        new_url = next_link.get("href")
        new_url = "https://pureportal.coventry.ac.uk" + new_url
        print(new_url)
    else:
        new_url = ""
    return new_url



#Publication URL in search button 
df = pd.DataFrame(columns=["title", "link", "author", "author_link", "date"])
url_1 = "https://pureportal.coventry.ac.uk/en/organisations/fbl-school-of-economics-finance-and-accounting"
#print(url_1)

driver.get(url_1)
page_source = driver.page_source
soup = BeautifulSoup(page_source, "html.parser")
section = soup.find("div", class_="page-section content-relation-section organisation-publications")
# print(section)
publication_url_soup = section.find("a", class_="portal_link btn-primary btn-large")
publication_url = publication_url_soup.get("href")
publication_url = "https://pureportal.coventry.ac.uk" + publication_url
print(publication_url)
while publication_url != "":
    publication_url = read(publication_url)
# link = read(publication_url)
# print(url)
# url = read(url)


print(df)
df.to_csv("output.csv", index=False)

time.sleep(10)
