import json
import os
import datetime
from PIL import Image
import yfinance as yf
import requests
from PIL import Image
import requests
from io import BytesIO
import yfinance as yf
import requests
from datetime import datetime
import termcolor
import json
import os
import pandas as pd

curentList = []
import os

curDir = os.getcwd()
try:
    os.mkdir('data')
except:
    pass
dataDir = os.path.join(curDir, 'data')


class Stock:
    def __init__(self, symbol, p=None):
        self.path = dataDir
        curentList.append(symbol)
        self.symbol = symbol
        self.ticker = yf.Ticker(symbol)
        self.info = self.ticker.info
        self.sector = self.info['sector']
        try:
            self.sectorDir = os.path.join(dataDir, self.sector)
            os.mkdir(self.sectorDir)
        except:
            pass
        self.filePath = os.path.join(dataDir, self.sector, self.symbol) + '.json'
        self.hist = self.ticker.history(period=p)
        self.news = self.ticker.news
        self.yearReturn = self.info['52WeekChange']
        self.teps = self.info['trailingEps']
        self.feps = self.info['forwardEps']
        self.fpe = self.info['forwardPE']
        self.logo = self.info['logo_url']
        self.response = requests.get(self.logo)
        self.img = Image.open(BytesIO(self.response.content))
        self.ptb = self.info['priceToBook']
        self.roe = self.info['returnOnEquity']
        self.debtEquityRatio = self.info['debtToEquity']
        self.insiders = ['heldPercentInsiders']
        self.method_list = [method for method in dir(self) if method.startswith('__') is False]
        self.mySave()

    def mySave(self):
        x = json.dumps(self.__dict__, indent=4, sort_keys=True, default=str)
        j = json.loads(x)
        print(self.filePath)
        with open(self.filePath, 'w') as f:
            json.dump(j, f)

    def __repr__(self):
        return self.filePath
