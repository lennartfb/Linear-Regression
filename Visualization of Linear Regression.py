import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd
from datetime import datetime


ticker_symbol_stock1 = "AMZN"
ticker_symbol_stock2 =  "AAPL"
starting_year = 2010


#Name des Unternehmens abfragen anhand des Ticker-Symbols
#Die Funktioniert liefert einen String mit dem entsprechenden Namen des Unternehmens
def stock_name_abfragen(symbol):
    stock = yf.Ticker(symbol)
    # Name des Unternehmens abrufen
    company_name = stock.info['longName']
    return company_name

#Called die Yaho Api und fragt die Daten für das entsprechende Ticker Symbol ab 
#Die daten werden dann zu einem bestimmten Zeitraum zugeschnitten (Von beginning year -bis- heute)
def preiseabfragen(ticker_symbol, beginningyear):
    #Das derzeitige Jahr abfragen:
    current_year = datetime.now().year
    #daten aus finance api abfragen 
    stock_data = yf.Ticker(ticker_symbol)
    current_data = stock_data.history(period='max')
    #Daten zuschneiden auf die entsprechenden Jahre
    data = current_data.loc[f'{beginningyear}-01-01':f'{current_year}-12-31']
    return data
    


stock1_data = preiseabfragen(ticker_symbol_stock1,starting_year)
stock2_data = preiseabfragen(ticker_symbol_stock2,starting_year)   

#Erstellen des matplotlib plots
def aktienplot(data_stock1, data_stock2):
    #Erstellen der Gerade für die lineare Regression
    lr = linear_regression(data_stock1['Open'],data_stock2['Open'])
    x_values = [data_stock1['Open'].min(),data_stock1['Open'].max()]
    y_values = lr
    plt.plot(x_values,y_values, color = "red",lw = 3)

    #Erstellen der einzelnen Punkte für die Kombination aus Openin Price von Stock 1 und Opening Price von Stock 2
    plt.scatter(data_stock1['Open'],data_stock2['Open'],s=10,alpha=0.5)

    #Erstellen der geraden (Abstände u) zwischen den Punkten und der Regressionsgerade 
    i = 0
    while  i < len(data_stock1['Open']):
        print
        gesuchter_stock_x_wert = data_stock1['Open'][i]
        gesuchter_stock_y_wert = data_stock2['Open'][i]
        ux_values = [gesuchter_stock_x_wert,gesuchter_stock_x_wert]
        uy_values = [gesuchter_stock_y_wert,werte_linear_regression(data_stock1['Open'],data_stock2['Open'],gesuchter_stock_x_wert)]
        plt.plot(ux_values, uy_values, color = 'green',ls = "dashdot")
        i = i+50

    #Name der Aktie mit dem entsprechenden Ticker-Symbol abfragen:
    name_stock1 = stock_name_abfragen(ticker_symbol_stock1)
    name_stock2 = stock_name_abfragen(ticker_symbol_stock2)
    plt.xlabel(f'Opening price of {name_stock1}')
    plt.ylabel(f'Opening price of {name_stock2}')
    plt.title(f'Linear Regression of {name_stock1} and {name_stock2} opening prices')

    #Plot erstellen
    plt.show()


    #Berechnung der Linearen regressionsgerade
    #berechnet den Ersten und letzen punkt der gerade (y1,y2) und gibt dies in array wieder
def linear_regression(x,y):
    #Daten aus x und y werden zu einem Dataframe kombiniert und deren Spalten benannt
    merged_data = pd.concat([x,y], axis = 1)
    merged_data.columns = ['X','Y']
    #Berechnung des Y-Achesnabschnitt a und der Steigung b 
    #b = cov(x,y)/var(x)
    #a = mean(y)-b*mean(x)
    b = merged_data.cov().loc['X','Y']/x.var()
    a = y.mean() - b*x.mean()

    
    #Berechnen des start und end punkts:
    y1 = a+b*x.min()
    y2 = a+b*x.max()
    
    
    return [y1,y2]
    
#berechnet zu einem gegebenen x wert den dazugehörigen wert der regressionsgerae 
def werte_linear_regression(x,y,x_wert_gesucht):
    merged_data = pd.concat([x,y], axis = 1)
    merged_data.columns = ['X','Y']
    
    b = merged_data.cov().loc['X','Y']/x.var()
    a = y.mean() - b*x.mean()

    y1 = a+b*x_wert_gesucht
    
    return y1




aktienplot(stock1_data,stock2_data)




