import util
import requests
import xmltodict
import datetime
import logging
import os
import unidecode
import pandas as pd
import os
from bs4 import BeautifulSoup




credentials = util.getCredentials()
sysPath = os.getcwd() + "/"


def get_google_trends():
    def parser_xml(v_xml):
        key_words = []
        content_xml = xmltodict.parse(v_xml)
        for i in content_xml['rss']['channel']['item']:
            rel_news = []
            for j in i['ht:news_item']:
                print(j)
                if not isinstance(j, str):
                    rel_news.append(j['ht:news_item_title'])  
            obj = {
                "title": "{}".format(removingCaracter(i['title'])), 
                "traffic": "{}".format(tratarNumber(i['ht:approx_traffic'])),
                "pubDate": "{}".format(i['pubDate']),
                "picture": "{}".format(i['ht:picture']),
                "pictureSource": "{}".format(i['ht:picture_source']),
                "description": "{}".format(i['description']),
                "related_news": rel_news,
                "dateInsert": datetime.datetime.now()
                }
            key_words.append(obj)
        return key_words

    logging.info("--- Getting GOOGLE TRENDS ---")
    # URL do trending topics do Google
    url = "https://trends.google.com.br/trends/trendingsearches/daily/rss?geo=BR"

    content = requests.get(url)
    return parser_xml(content.text)


def ask_for_a_subject():
    print("Getting google Trends...")
    gsubject = get_google_trends()
    df = pd.DataFrame(gsubject)
    df["traffic"] = pd.to_numeric(df["traffic"])
    df["pubDate"] =  pd.to_datetime(df["pubDate"], format='%a, %d %b %Y %H:%M:%S %z')
    df['date'] = df['pubDate'].dt.strftime('%y/%m/%d')
    df['dateInsert2'] = df['dateInsert'].dt.strftime('%Y%m%d')
    ArchiveDate = df.at[0,'dateInsert2']
    df = df.sort_values(by=['pubDate','traffic'], ascending=[False,False])
    df_grouped = df.groupby(by='date').sum()
    df_grouped['total_traffic'] = df_grouped['traffic']
    df = df.merge(df_grouped[['total_traffic']], on='date', how='left')
    df['percent'] = (df['traffic'] / df['total_traffic']) * 100
    df = df.sort_values(by=['date', 'percent'], ascending=[False, False])

    df.to_csv(sysPath+"output/GoogleTrends/"+ArchiveDate+"_GoogleTrends.csv",header=True,index=False,encoding='UTF-8')#encoding='utf8')




def removingCaracter(t_input):
    outputString = unidecode.unidecode(t_input).upper()
    outputString = outputString.replace('#','')
    return outputString

def tratarNumber(n_input):
    logging.info('Cleaning text...')
    n_input = n_input.replace('+','')
    n_input = n_input.replace(',','')
    if n_input == 'None':
        return -1
    return int(n_input)

