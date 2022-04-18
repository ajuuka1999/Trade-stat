#!/usr/bin/python3
from datetime import datetime, date,timedelta
import yfinance as yf

today = date.today()
targetstart = today - timedelta(days=3)
def search(code):

    Code = yf.Ticker(code)
    values = Code.history(start=targetstart, end=today)
    if "Empty DataFrame" in str(values):
        return False

    datals = (str(values).split("\n")[-1]).split(" ")
    datals.insert(0, code)
    newls = []
    for x in datals:
        if x:
            newls.append(x)
    return newls[:7]


if __name__ == "__main__":
    values = search("AAPL")
    if values == False:
        print("FAIL")
    else:
        print(values)
