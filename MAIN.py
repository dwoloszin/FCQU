import GoogleTrends
import ImportDF
import NewsApi


#Get trends from Google
#GoogleTrends.ask_for_a_subject()


#get news from News API
Fields = ['title','traffic','date','percent']
pathImport = '/output/GoogleTrends'
dataFrame = ImportDF.processArchive(Fields,pathImport)



'''
for index, row in dataFrame.iterrows():
    NewsApi.News(row['title'],"2023-02-21")
'''

NewsApi.News('GUERRA','2023-02-21')
