from lxml import etree
from datetime import datetime
import asyncio
from pyppeteer import launch
import pandas as pd

root_url = "http://graschool.ahu.edu.cn/"

news_url =  root_url + "9577/list.htm"

current_date = datetime.datetime.now().strftime('%Y-%m-%d')

async def main():
    # headless参数设为False，则变成有头模式
    browser = await launch(headless=True)
    
    page = await browser.newPage()
    await page.evaluateOnNewDocument('function(){Object.defineProperty(navigator, "webdriver", {get: () => undefined})}')

    await page.goto(news_url, options={'timeout': 50000})

    # 等待页面加载完成
    await page.waitForNavigation()

    cookies = await page.cookies()

    # 将结果集的文本转化为树的结构
    tree = etree.HTML(await page.content())
    
    the_list =  tree.xpath("""//*[@id="wp_news_w1205"]/ul/li""")
    news_list = []
    

    df = pd.read_csv('news.csv')

    for the_li in range(1, len(the_list) + 1):
        the_title = tree.xpath(f"""//*[@id="wp_news_w1205"]/ul/li[{the_li}]/div[1]/span[2]/a/text()""")
        the_date = tree.xpath(f"""//*[@id="wp_news_w1205"]/ul/li[{the_li}]/div[2]/span/text()""")
        the_url = tree.xpath(f"""//*[@id="wp_news_w1205"]/ul/li[{the_li}]/div[1]/span[2]/a/@href""")

        result_df = df[df.title == the_title[0]].date == the_date[0]
        if len(result_df) == 0 or result_df.tolist()[0] == False:
            news_dict = {}
            news_dict['url'] = root_url + the_url[0]
            news_dict['title'] = the_title[0]
            news_dict['date'] = the_date[0]
            news_dict['add_date'] = current_date
            news_list.append(news_dict)

    
    df = pd.concat([df,pd.DataFrame(news_list)], ignore_index=True)
    df.to_csv("news.csv",index=0)
            
    
    result_file = open('result.txt','w', encoding='utf-8')
    if len(news_list) != 0:
        for line in news_list:
            write_str = ""
            for k,v in line.items():
                write_str += f"{k}:{v}\n"
            write_str += "\n\n"
            result_file.write(write_str)
    else:
        write_str = "没有最新的新闻"
        result_file.write(write_str)
    result_file.close()
    
    # 关闭浏览器
    await browser.close()

asyncio.get_event_loop().run_until_complete(main())
