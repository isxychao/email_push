from lxml import etree
import datetime
import asyncio
from pyppeteer import launch

current_date = datetime.datetime.now().strftime('%Y-%m-%d')
# current_date = "2022-08-12"
root_url = "http://graschool.ahu.edu.cn/"

news_url =  root_url + "9577/list.htm"

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
        data_file = open('result.txt','a', encoding='utf-8')
        for line in the_list:
            write_str = ""
            for k,v in line.items():
                write_str += f"{k}:{v}\n"
            write_str += "\n\n"
            data_file.write(write_str)
        data_file.close()
    
    # 关闭浏览器
    await browser.close()

asyncio.get_event_loop().run_until_complete(main())
