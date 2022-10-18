import urllib.request
from urllib.parse import urlparse
from urllib.parse import parse_qs
import requests
import os
import concurrent.futures
import time
import concurrent.futures

failed = []
fails = []
failedfile = open('failed_urls.csv', 'a')


def download_image(url, index):
    try:
        if int(index) >= 0:
            # print(index, '\n')
            opener = urllib.request.URLopener()
            opener.addheader('User-Agent',
                             'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36')
            parsed_url = urlparse(url)
            file_name = 'empty'
            # if int(index)==18000:
            #     print(parsed_url)
            if 'name=' in url:
                file_name = file_name = parsed_url.path + parse_qs(parsed_url.query)['name'][0]
            elif 'file=' in url:
                file_name = file_name = parsed_url.path + parse_qs(parsed_url.query)['file'][0]
            else:
                file_name = parsed_url.path
            # else:file_name=url.split('/')[-2]+url.split('/')[-1]

            file_name = 'comment_attachments' + file_name
            query = "/" + file_name.split('/')[-1]
            # print(1,query)
            path = file_name.replace(query, '')
            # print(2,path)
            # print(path,query,'path')
            if 'file=' in url:
                file_name = path + query
                file_name = file_name.replace('/download.php', '')
                path = path.replace('/download.php', '')
            try:
                os.makedirs(path)
            except OSError:
                print('',end=" ")
                # print("Creation of the directory %s failed", file_name, " 'path may already exist '")
            # filename,headers=opener.retrieve(url,'./assets/'+file_name)
            # dl_image(url,'assets/',file_name)
            if (file_name != 'empty'):
                with open(file_name, 'wb') as f:
                    im = requests.get(url)
                    f.write(im.content)
                    print(index,' success ',end=" ")
                    return 1

    except:
        with open('failed_urls.csv', 'a', encoding='UTF8') as fail:
            writer = csv.writer(fail)
            print(index, ' failed ',end=" ")
            # write the header
            writer.writerow([index, url])
        return 0


# for i in ['https://teradek.zendesk.com/attachments/token/woMkj1rQWJEHPkWRciJfZR0Bn/?name=inline1054491252.png',
# 'https://creativesolutionsinc.lightning.force.com/lightning/r/Knowledge__kav/ka04W000001Ityn/view',
# 'https://creativesolutionsinc.lightning.force.com/lightning/r/Knowledge__kav/ka08a000000aOXG/view']:
#   download_image(i)

import csv

# to extract url
# opening the CSV file
extensions = ['end']
urls = {'1': '1'}
with concurrent.futures.ThreadPoolExecutor() as executor:
    with open('zendesk_comment_attachment_content_urls_and_plain_body_urls_oct_17.csv', encoding="utf8",
              errors='ignore') as file:
        # reading the CSV file
        csvFile = csv.reader(file)

        # displaying the contents of the CSV file
        for line in csvFile:
            link = line[1]
            l = len(link)
            # if '.' in link[l - 7:l]:
            #     d = link[l - 7:l]
            #     d = d.split('.')
            # if d[1] in ["jpeg","JPEG","zip","ZIP","bin","BIN","png","PNG","jpg","JPG","deb","DEB","mp4","MP4","tar","TAR","pdf","PDF","WEBP", "webp", "GIF", "gif"] or line[0] in fails or 'file=' in link:
            # download_image(link, line[0])
            args = ({"url": link, "index": line[0]})
            if  line[0] !='index' and int(line[0]) % 2 != 0:
                download_image(link, line[0])

failedfile.close()
print('failed_list', failed)
