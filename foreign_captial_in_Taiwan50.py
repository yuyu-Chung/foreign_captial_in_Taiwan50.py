# 本程式檔目標為找出台灣50股票中，每日外資買超前三名之股票，列入選股參考。
# 本程式檔使用方式 : 已預設跑出台灣50中外資買超前3名的股票，可重新設定希望呈現之前幾名股票，如 foreign_investor = foreign_investor[:5]
# 本程式檔如何驗證 : 可對照輸出之台灣50與每日外資買超前100名股票代號取交集的list，是否與台灣50股票及每日外資買超排名前100名單交叉比對一致。
#                   以及最後輸出之折線圖，其公司是否包含於 交集list、網路台灣50名單、網路每日外資買超排名名單內。(參考爬蟲網頁。)

# 先載入將使用之第三方套件包，requests、BeautifulSoup、pandas、yfinance、matplotlib，若無下載皆須先行下載(pip install (requests、BeautifulSoup、pandas、yfinance、matplotlib))

import requests
from bs4 import BeautifulSoup
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

# 應用網路爬蟲，比對台灣50成分股 與 外資買超排名前100股票，取交集製作新list

def foreign_investor_list():

    # 網路爬蟲，取得台灣50成分股代號，做成list
    url_1 = "https://histock.tw/twclass/A901"
    html_1 = requests.get(url_1)
    html_1_text = BeautifulSoup(html_1.text, "html5lib")
    html_1_data = html_1_text.find_all("span",{"class":{"w60 lft-p stockno"}})
    taiwan_50 = []
    for elem in html_1_data:
        list_1 = elem.text
        list_2 = list_1+".TW"
        taiwan_50.append(list_2)
    del taiwan_50[0]

    # 網路爬蟲，取得外資買超排名前100股票代號，做成list
    url_2 = "https://tw.stock.yahoo.com/rank/foreign-investor-buy/"
    html_2 = requests.get(url_2)
    html_2_text = BeautifulSoup(html_2.text, "html5lib")
    html_2_data = html_2_text.find_all("div",{"class":{"D(f) Ai(c)"}})
    foreign_100 = []
    for symble in html_2_data:
        stock = symble.text
        foreign_100.append(stock)
    for not_stock in foreign_100:
        if len(not_stock)!= 7:
            foreign_100.remove(not_stock)

    # 將 台灣50代號list 與 外資100代號list，取交集，做成供查詢 的 目標list
    # list 取交集:intersection；取聯集:union；取差集:difference
    foreign_investor = list(set(foreign_100).intersection(set(taiwan_50)))
    
    return foreign_investor

# 將預備好的 foreign_investor list 整理出股票資料DataFrame 以及最後折線圖呈現。

def stock_info(foreign_investor):
    stock = yf.Ticker(foreign_investor)
    stock_data = stock.history(period="1y", interval="1d")
    stock_name = stock.info
    stock_pd = pd.DataFrame(stock_data)
    
    sma = stock_pd["Close"].rolling(5).mean()
    lma = stock_pd["Close"].rolling(20).mean()

    stock_pd["SMA"] = sma
    stock_pd["LMA"] = lma

    plt.plot(stock_pd.Close, color = "navy", label="Close Price")
    plt.plot(stock_pd.SMA, color="red", label="SMA")
    plt.plot(stock_pd.LMA, color ="orange", label="LMA")
    plt.title(stock_name["shortName"]+" Curve")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend(loc="best")
    plt.grid()
    plt.show() 

# 依本程式目標，呼叫台灣50股票中，外資買超前3高者，股票折線圖呈現。

if __name__ == "__main__":
    foreign_investor = foreign_investor_list()
    foreign_investor = foreign_investor[:3]
    for elem in foreign_investor:
        stock_info(elem)
      
