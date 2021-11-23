while True:
    import pandas as pd
    import yfinance as yf
    from splinter import Browser
    from bs4 import BeautifulSoup
    from webdriver_manager.chrome import ChromeDriverManager
    import time
   
    #Use Webdriver for scrape

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    #Scrape stock tickers
    url = 'https://stockanalysis.com/stocks/'
    browser.visit(url)
    element = browser.find_by_name('perpage').first
    element.select('10000')
    html = browser.html   
    soup = BeautifulSoup(html,'html.parser')

    table = soup.find('table', {'class' : 'symbol-table index'})

    symbol = []

    for row in table.find_all('tr')[1:]:
        symbol.append(row.find_all('td')[0].text)

    print("Stock List Created")

    browser.quit()


    #Use yfinance library to pull all  history from Yahoo Finance
    history = pd.DataFrame(columns = ['Symbol','Date','Open','High','Low','Close','Volume','Dividends','Stock Splits'])

    for i in symbol:
        try:
            data = yf.Ticker(i).history(period = 'max')
            df = pd.DataFrame(data)
            df['Date']=df.index
            df['Symbol'] = i
            history = history.append(df)
            print(f"----------{i} complete----------")
        except:
            pass

    history.to_csv('Output/stock_history.csv',index=False)

    time.sleep(60)
