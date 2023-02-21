import util
import os
import requests
import pandas as pd
import ChatGPT

credentials = util.getCredentials()
sysPath = os.getcwd() + "/"

def News(subject, date):
    api = credentials['NEWS_API']
    url = ('https://newsapi.org/v2/everything?'
        'q=' + subject + '&'
        'from=' + date + '&'
        'language=' +'pt'+'&'
        'sortBy=popularity&'
        'apiKey=' + api)

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        articles = data['articles']
        df = pd.DataFrame(articles)
        df = df.head(1)
        if  not df.empty:
            df['description_ChatGPT'] = df['description'].apply(lambda x: ChatGPT.Rewrite(x))
            df['Curiosity_ChatGPT'] = subject.apply(lambda x: ChatGPT.Ask(f'Uma Curiosidade sobre {x}'))#try this code after get back
            
            df.to_csv(sysPath+"output/"+'News/'+subject+"_News.csv",header=True,index=False,encoding='UTF-8')#encoding='utf8')
            return df
    else:
        ResposeCode(response.status_code)
        return None
    

# https://newsapi.org/docs/errors
def ResposeCode(codeNumber):
    if codeNumber == 200:
        print('The request was executed successfully')
    if codeNumber == 400:
        print('The request was unacceptable, often due to a missing or misconfigured')
    if codeNumber == 401:
        print('Your API key was missing from the request, or wasnt correct')        
    if codeNumber == 429:
        print('You made too many requests within a window of time and have been rate limited. Back off for a while.')
    if codeNumber == 500:
        print('Something went wrong on our side.')
