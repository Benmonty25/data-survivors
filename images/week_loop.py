import pandas as pd
import yfinance as yf
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

#Use Webdriver for scrape

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=True)

#Infinite loop for local data updates

while True:
    #Scrape stock tickers
    url = 'https://stockanalysis.com/stocks/'
    browser.visit(url)
    element = browser.find_by_name('perpage').first
    element.select('10000')
    html = browser.html   
    soup = BeautifulSoup(html,'html.parser')

    table = soup.find('table', {'class' : 'symbol-table index'})

    symbol = []
    company_name = []
    industry = []
    market_cap= []
    for row in table.find_all('tr')[1:]:
        symbol.append(row.find_all('td')[0].text)
        company_name.append(row.find_all('td')[1].text)
        industry.append(row.find_all('td')[2].text)
        market_cap.append(row.find_all('td')[3].text)

    stocks_df = pd.DataFrame(list(zip(symbol, company_name,industry,market_cap)),
            columns =['Symbol', 'Company','Industry','Market Cap'])

    stocks_df.to_csv('Output/stock_list.csv',index=False)

    print("Stock List Created")

    #Scrape S&P stock tickers

    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    browser.visit(url)

    html = browser.html   
    soup = BeautifulSoup(html,'html.parser')

    table = soup.find('table')

    spsymbol = []

    for row in table.find_all('tr')[1:]:
        spsymbol.append(row.find_all('td')[0].text)
    browser.quit()

    cleaned = []
    for i in spsymbol:
        cleaned.append(i.strip('\n'))

    sp_df = pd.DataFrame(cleaned, columns =['Symbol'])
    sp_df.to_csv('Output/sp500_list.csv',index=False)

    print("S&P Stocks Created")

    #Use yfinance library to pull 1 week history from Yahoo Finance
    history = pd.DataFrame(columns = ['Symbol','Date','Open','High','Low','Close','Volume','Dividends','Stock Splits'])

    for i in symbol:
        try:
            data = yf.Ticker(i).history(period = '1wk')
            df = pd.DataFrame(data)
            df['Date']=df.index
            df['Symbol'] = i
            history = history.append(df)
            print(f"----------{i} complete----------")
        except:
            pass

    history.to_csv('Output/1wk_stock_history.csv',index=False)