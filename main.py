# Web scrapping
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
from openpyxl.workbook import Workbook

chrome_driver_path = "C:/dev/chromedriver.exe"
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

url = "https://www.nba.com/stats/players/traditional?PerMode=Totals&sort=PTS&dir=-1&SeasonType=Regular+Season&Season=2022-23"

driver.get(url)
select = Select(driver.find_element(By.XPATH,
                                    '//*[@id="__next"]/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[2]/div[1]/div[3]/div/label/div/select'))
select.select_by_index(0)
src = driver.page_source
soup = BeautifulSoup(src, "lxml")
table = soup.find("div", attrs={"class": "Crom_container__C45Ti"})
cols = table.find_all('th')[1:]
col_list = []
stats = []

for header in cols:
    if not 'RANK' in header.getText():
        col_list.append(header.getText())

rows = table.find_all("tr")[1:]
for i in range(len(rows)):
    row_data = []
    for td in rows[i].find_all('td')[1:]:
        text = td.getText().strip()
        row_data.append(text)
    stats.append(row_data)

NBA_stats = pd.DataFrame(stats, columns=col_list)

pd.DataFrame.to_csv(NBA_stats, "NBA_stats.csv")
pd.DataFrame.to_excel(NBA_stats, "NBA_stats.xlsx")
