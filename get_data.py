from lxml import etree
from datetime import datetime
import asyncio
from pyppeteer import launch

format_pattern = '%Y-%m-%d'

# current_date = datetime.now().strftime('%Y-%m-%d')
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
    
    date_file = open('news_date.txt','r+', encoding='utf-8')
    readlines = date_file.readlines()
    date_file.truncate(0)

    if len(readlines) == 0:
        save_date = '1999-01-01'
    else:
        save_date = readlines[0].split(' ')[1]
    
    save_date = datetime.strptime(save_date, format_pattern)
    latest_date = save_date
    
    for the_li in range(1, len(news_list) + 1):
        news_date = tree.xpath(f"""//*[@id="wp_news_w1205"]/ul/li[{the_li}]/div[2]/span/text()""")
        news_date_st = datetime.strptime(news_date[0], format_pattern)
        if (news_date_st - save_date).days > 0:
            if (news_date_st - latest_date).days > 0:
                latest_date = news_date_st
            news_dict = {}
            the_url = tree.xpath(f"""//*[@id="wp_news_w1205"]/ul/li[{the_li}]/div[1]/span[2]/a/@href""")
            the_title = tree.xpath(f"""//*[@id="wp_news_w1205"]/ul/li[{the_li}]/div[1]/span[2]/a/text()""")
            news_dict['url'] = root_url + the_url[0]
            news_dict['title'] = the_title[0]
            the_list.append(news_dict)
    write_str = f"latest_data {datetime.strftime(latest_date, format_pattern)}"


    date_file.write(write_str)
    date_file.close()
    
    if len(the_list) != 0:
        result_file = open('result.txt','a+', encoding='utf-8')
        for line in the_list:
            write_str = ""
            for k,v in line.items():
                write_str += f"{k}:{v}\n"
            write_str += "\n\n"
            result_file.write(write_str)
        result_file.close()
    
    # 关闭浏览器
    await browser.close()

asyncio.get_event_loop().run_until_complete(main())
