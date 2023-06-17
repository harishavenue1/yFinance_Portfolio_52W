import urllib3
import pandas as pd
import requests

urllib3.disable_warnings()

url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v4/get-statistics"
headers = {
    "X-RapidAPI-Key": "4a13244469mshf2fccb7d18450b5p106fa3jsn52398743b756",
    "X-RapidAPI-Host": "apidojo-yahoo-finance-v1.p.rapidapi.com"
}

listOfStocks = [
    "ACE         ",
    "ADANIPOWER  ",
    "AGARIND     ",
    "ALUFLUOR    ",
    "AMRUTANJAN  ",
    "APCOTEXIND  ",
    "APLAPOLLO   ",
    "APOLLOPIPE  ",
    "ARMANFIN    ",
    "ASTEC       ",
    "BAJFINANCE  ",
    "BALKRISIND  ",
    "CANBK       ",
    "CARYSIL     ",
    "COSMOFIRST  ",
    "DEEPAKNTR   ",
    "DBOL        ",
    "DIVISLAB    ",
    "DMCC        ",
    "GABRIEL     ",
    "GLOBUSSPR   ",
    "GRANULES    ",
    "GRAVITA     ",
    "FLUOROCHEM  ",
    "HCG         ",
    "IRCTC       ",
    "ICICIBANK   ",
    "IDFCFIRSTB  ",
    "IIFL        ",
    "ITC         ",
    "JYOTIRES    ",
    "KABRAEXTRU  ",
    "KEI         ",
    "KMCSHIL     ",
    "KPIGREEN    ",
    "LAURUSLABS  ",
    "MASTEK      ",
    "MCX         ",
    "NH          ",
    "NAVINFLUOR  ",
    "POLICYBZR   ",
    "PHANTOMFX-SM",
    "PPLPHARMA   ",
    "PIXTRANS    ",
    "PRICOLLTD   ",
    "RADICO      ",
    "RAINBOW     ",
    "RHIM        ",
    "ROLEXRINGS  ",
    "SAREGAMA    ",
    "SBCL        ",
    "SONACOMS    ",
    "SUDARSCHEM  ",
    "SUMICHEM    ",
    "SUNTECK     ",
    "SYNGENE     ",
    "TEJASNET    ",
    "UFLEX       ",
    "VENUSPIPES  ",
    "VIDHIING    ",
    "YASHPAKKA   "
]

stock_52w_high = {}
y_high = 0
response = {}
stockName = None


def fetchResponse():
    global response
    querystring = {"symbol": stockName}
    response = requests.get(url, headers=headers, params=querystring, verify=False)
    response.raise_for_status()


def fetch_52W_high():
    global y_high
    try:
        y_high = round(response.json()['quoteSummary']['result'][0]['defaultKeyStatistics']['52WeekChange']['raw'] * 100, 2)
        print(f"For stock {stockName} 52w Change", y_high)
    except ValueError:
        print("Failed to fetch 52w value for stock", stock)


for stock in listOfStocks:
    stockName = stock.strip() + ".NS"
    try:
        fetchResponse()
        fetch_52W_high()
    except Exception:
        print('failed to fetch value for stock', stockName)
        stockName = stock.strip() + ".BO"
        print('attempting for BSE Code', stockName)
        try:
            fetchResponse()
            fetch_52W_high()
        except Exception:
            print('failed to fetch value for stock', stockName)
    else:
        stock_52w_high[stock] = y_high

print(stock_52w_high)

# convert to dataFrame
df = pd.DataFrame(stock_52w_high.items(), columns=['stock', '52w_high'])
df.sort_values(by=['52w_high'], ascending=[False], inplace=True)
df.to_csv('myStock_52wHigh.csv', index=False)
