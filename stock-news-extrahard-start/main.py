import requests
from twilio.rest import Client

STOCK = "VOLTAS.BSE"
COMPANY_NAME = "Voltas"
STOCK_API_KEY="QA6DEI5NW25NKNIZ"

## STEP 1: Use https://www.alphavantage.co
stock_parameter={
    "function":"TIME_SERIES_DAILY",
    "symbol":STOCK,
    "apikey":STOCK_API_KEY
}

def getNews(symbol:str,date:str):
    news_parameter={
        "qInTitle" :symbol,
        "from":date,
        "searchIn":"title",
        "language":"en",
        "apiKey":"e20aea3c52f84686b059b59bd6a6f368"
    }
    newsResponse=r=requests.get(url="https://newsapi.org/v2/everything",params=news_parameter)
    newsResponse.raise_for_status()
    print(newsResponse.json())
    article_list=newsResponse.json()["articles"][:3]
    Headlines=""
    for a in article_list:
        Headlines+=a["title"]+"\n"+a["description"]+"\n\n"
    #print(Headlines)
    return Headlines


def sendMSG(msg:str):
    acc_sid = "AC04f213f196d0db2b5b709b9c5b6cd061"
    acc_auth = "227f932f1095261a7fc5040b76752512"
    twilo_no = "+18573746635"
    own_no = "+91 98343 43800"  #put real no for it to work
    client=Client(acc_sid,acc_auth)
    message=client.messages.create(
            body=msg,
            from_=twilo_no,
            to=own_no)
    print(message.status)
    print(msg)


response=requests.get(url="https://www.alphavantage.co/query",params=stock_parameter)
response.raise_for_status()
stock_data=response.json()
print(stock_data)

dail_stock_data=stock_data["Time Series (Daily)"]
print(dail_stock_data)
days=list(dail_stock_data.keys())
print(days)
day_befor_yesterday_close=float(dail_stock_data[days[2]]['4. close'])
yesterday_close=float(dail_stock_data[days[1]]['4. close'])
change_percent=round((yesterday_close-day_befor_yesterday_close)/day_befor_yesterday_close*100,2)
print("change%",change_percent,day_befor_yesterday_close,yesterday_close)


if abs(change_percent)<5:
    phonetxt = ""
    if change_percent>0:
        phonetxt=f"VOLTAS: 🔺{abs(change_percent)}\n"
    else:
        phonetxt = f"VOLTAS: 🔻{abs(change_percent)}\n"

    stockHeadlines= getNews("Voltas",days[2])
    phonetxt +=stockHeadlines

    sendMSG(phonetxt)

# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.



## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 


#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

