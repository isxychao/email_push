from lxml import etree
import datetime
import requests

current_date = datetime.datetime.now().strftime('%Y-%m-%d')
# current_date = "2022-08-12"
root_url = "http://graschool.ahu.edu.cn/"



headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
}

news_url =  root_url + "9577/list.htm"



# resp = requests.get(news_url,headers=headers)
# request_cookies = requests.utils.dict_from_cookiejar(resp.request._cookies)

# 设置cookies
cookies = {}

# for k,v in request_cookies.items():
# # cookies['JSESSIONID'] = 'F9FCB587DCACFAD0A8D4BE520E0FFF54'
#     cookies[k] = v
cookies['v48D3cqudNzB264'] = 'Kt70UWqdBlgdRdB0A3bNTIudBqX8V7i3IA6v4HkEjv88yqJZZQEdu8EwX_ChLzO7O5Gyk0BxreagDqTdl.z_XgEUwwlgvtgnxKPV9ja1PStY4'

# get请求，传入参数，返回结果集
resp = requests.get(news_url,headers=headers, cookies=cookies)
resp.encoding = resp.apparent_encoding
# 将结果集的文本转化为树的结构
tree = etree.HTML(resp.text)

news_list =  tree.xpath("""//*[@id="wp_news_w1205"]/ul/li""")
the_list = []

for the_li in range(1, len(news_list) + 1):
    the_date = tree.xpath(f"""//*[@id="wp_news_w1205"]/ul/li[{the_li}]/div[2]/span/text()""")
    if current_date == the_date[0]:
        news_dict = {}
        the_url = tree.xpath(f"""//*[@id="wp_news_w1205"]/ul/li[{the_li}]/div[1]/span[2]/a/@href""")
        the_title = tree.xpath(f"""//*[@id="wp_news_w1205"]/ul/li[{the_li}]/div[1]/span[2]/a/text()""")
        news_dict['url'] = root_url + the_url[0]
        news_dict['title'] = the_title[0]
        the_list.append(news_dict)

if len(the_list) != 0:
    data_file = open('result.txt','a')
    for line in the_list:
        write_str = ""
        for k,v in line.items():
            write_str += f"{k}:{v}\n"
        write_str += "\n\n"
        data_file.write(write_str)
    data_file.close()

