import traceback
import csv
from bs4 import BeautifulSoup
from ebaysdk.finding import Connection
from ebaysdk.shopping import Connection as Shopping

def get_pictures_url(ebay_id):
    api = Shopping(config_file='ebay.yaml')
    request = {'ItemID':ebay_id}

    response = api.execute('GetSingleItem',request)

    url_list = []

    soup = BeautifulSoup(response.content,'lxml')
    #print(soup.prettify())
    pictures_url = soup.find_all('pictureurl')
    for url in pictures_url:
        url = str(url)
        url = url.replace('<pictureurl>','')
        url = url.replace('</pictureurl>','')
        url_list.append(url)
        #print(url)
    return url_list


complete_list = []

#open file with ebay_id and make the queries
with open('k.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        row_list = []

        query = row['query']    
        title = row['title']
        ebay_id = row['ebay_article_id']
        pictures = get_pictures_url(ebay_id)

        row_list.extend((query,title,ebay_id))
        
        for picture in pictures:
            row_list.append(picture)
        complete_list.append(row_list)


fields = ['query', 'title','ebay_id', 'picture_0', 'picture_1','picture_2',
        'picture_3','picture_4','picture_4','picture_5','picture_6',
        'picture_7','picture_8','picture_9','picture_10','picture_11',] 


#write the header
with open('ebay_pictures_raw.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(fields)

#write 
for item in complete_list:
    with open('ebay_pictures_raw.csv', 'a+') as f:
        writer = csv.DictWriter(f, fieldnames=fields)    
        # #writer.writerow({'query': query, 'last_name': 'Beans'})
        # writer.writerows(item)

        csv_writer = csv.writer(f)
        csv_writer.writerow(item)

        # pictures = item[2] # index 2 is a list of pictures        
        # title = item=[1]
        # query = item[0]

        # print(title,query,len(pictures))

        # writer.writerow({'query': query, 'title': title})

        # index = 0

        # for url in pictures:
        #     first_chunk = 'picture_'
        #     pic_number = first_chunk + str(index)

        #     writer.writerow({pic_number: url}) #'last_name': 'Beans'})
        #     index += 1