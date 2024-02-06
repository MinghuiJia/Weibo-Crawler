import os
import re
import time
import urllib.parse

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# import pymysql

def getFirstCommentButton(browser):
    time.sleep(3)
    # 获取页面所有card下的操作栏（点赞、评论等）
    allClickEles = browser.find_elements_by_css_selector('a[action-type="feed_list_comment"]')
    # 获取页面所有的card
    allDivsEles = browser.find_elements_by_css_selector('#pl_feed_main #pl_feedlist_index div[action-type="feed_list_item"]')
    # 从每个操作栏中找到评论按钮，返回评论按钮及其对应的card元素
    for i in range(len(allDivsEles)):
        each = allClickEles[i]
        div = allDivsEles[i]
        commentButton = each
        attribute = commentButton.get_attribute('suda-data')
        if ("key=tblog_search_off_weibo" not in attribute):
            return commentButton, div
    return None, None

def getMoreContent(cardContent):
    time.sleep(3)
    # 获取所有文本中更多的按钮
    moreContent = []
    try:
        moreContent = cardContent.find_elements_by_css_selector('.card-feed>.content>p')
    except Exception as e:
        pass
    finally:
        return moreContent

def getMoreButton(browser):
    time.sleep(3)
    answereds = browser.find_elements_by_css_selector(
        '#pl_feed_main #pl_feedlist_index div[action-type="feed_list_item"]')
    for answered in answereds:
        contents = answered.find_elements_by_css_selector('.card-feed>.content>p')
        # 表明有需要展开的
        if (len(contents) == 2):
            style = contents[0].get_attribute('style')
            clickEle = answered.find_element_by_css_selector('.card-feed>.content>p[node-type="feed_list_content"]>a[action-type="fl_unfold"]')
            if (style == ''):
                return clickEle, answered
    return None, None
# def insertData2Mysql(sql, param):
#     # 存储到数据库
#     # 连接数据库
#     conn = pymysql.connect(host='localhost', port=3306,
#                            user='root', password='JMHjmh1998',
#                            database='crawlerdb')
#
#     # 使用 cursor() 方法创建一个游标对象 cursor
#     cursor = conn.cursor()
#
#     try:
#         cursor.execute(sql, param)
#         conn.commit()
#     except Exception as e:
#         print(e)
#         conn.rollback()
#     finally:
#         conn.close()

def extractPageInfo(browser, keyword, func):
    # # 模拟点击评论的过程
    # while True:
    #     try:
    #         time.sleep(2)
    #         # 先获取第一个可以点击的按钮
    #         clickEle, divEle = getFirstCommentButton(browser)
    #         # 点击按钮，页面会更新
    #         if (clickEle):
    #             # 先让评论按钮在范围内，保证不会弹窗
    #             browser.execute_script("arguments[0].scrollIntoView(false)", divEle)
    #             time.sleep(1)
    #             clickEle2, divEle2 = getFirstCommentButton(browser)
    #             browser.execute_script("arguments[0].click();", clickEle2)
    #         # 当页面中没有评论需要点开就结束循环
    #         else:
    #             break
    #
    #         time.sleep(1.5)
    #     except (Exception, BaseException) as e:
    #         print(e)
    #         continue

    # 模拟点击更多的过程
    while True:
        try:
            time.sleep(2)
            # 先获取第一个可以点击的按钮
            clickEle, divEle = getMoreButton(browser)
            # 点击按钮，页面会更新
            if (clickEle):
                # 先让按钮在范围内，保证不会弹窗
                browser.execute_script("arguments[0].scrollIntoView(false)", divEle)
                time.sleep(1)
                clickEle2, divEle2 = getMoreButton(browser)
                browser.execute_script("arguments[0].click();", clickEle2)
            # 当页面中没有评论需要点开就结束循环
            else:
                break

            time.sleep(1.5)
        except (Exception, BaseException) as e:
            print(e)
            continue

    # 获取所有的回答card
    answereds = None
    try:
        # 寻找所有的回答
        answereds = browser.find_elements_by_css_selector('#pl_feed_main #pl_feedlist_index div[action-type="feed_list_item"]')
    except Exception as e:
        print(e)
        time.sleep(300)

        # 如果出现任何意外就重新开始解析这个问题的帖子
        func(browser, keyword)

        return

    # 当前页回答的数量
    print("collected ", len(answereds), " answer list-item")

    # 解析每个回答
    approvalCounts = []
    forwardCounts = []
    commentCounts = []
    contents = []
    profiles = []

    # 记录解析到第几个回答
    processCount = 1
    for answered in answereds:
        try:
            print("processing answer ", processCount, ' start...')

            # 先获取card内容
            cardContent = answered.find_element_by_css_selector('.card-feed>.content')

            # 解析作者信息
            # 作者名称
            name = cardContent.find_element_by_css_selector('.info>div:nth-child(2)>a').get_attribute('nick-name')

            # 解析发表时间及设备
            # 作者个人信息链接
            fromAEles = cardContent.find_elements_by_css_selector('.from a')
            answerTime = fromAEles[0].text

            # 获取当前日期
            current_time = time.localtime()
            year = current_time.tm_year
            month = current_time.tm_mon
            day = current_time.tm_mday
            hour = current_time.tm_hour
            minute = current_time.tm_min
            if ('秒前' in answerTime):
                answerTime = str(year) + "年" + str(month) + "月" + str(
                    day) + "日 " + str(hour) + ":" + str(minute)
            elif ('分钟前' in answerTime):
                pattern1 = r'(\d+)分钟前'
                minute_post = int(re.findall(pattern1, answerTime)[0])
                minute -= minute_post
                if (minute < 0):
                    minute = 60 + minute
                    hour -= 1
                if (hour < 0):
                    hour = 24 + hour

                answerTime = str(year) + "年" + str(month) + "月" + str(
                    day) + "日 " + str(hour) + ":" + str(minute)
            elif ('今天' in answerTime):
                pattern1 = r'今天(\d+:\d+)'
                hour_min = re.findall(pattern1, answerTime)[0]
                answerTime = str(year) + "年" + str(month) + "月" + str(
                    day) + "日 " + hour_min
            elif ('年' not in answerTime):
                answerTime = str(year) + "年" + answerTime

            device = ''
            if (len(fromAEles) == 2):
                device = fromAEles[1].text

            # 获取card对应操作的元素
            operateEles = answered.find_elements_by_css_selector('.card-act li')

            # 帖子相关信息（赞同数量、回答创建时间、评论数量）
            forwardCount = operateEles[0].text
            if (forwardCount == '转发'):
                forwardCount = '0'
            commentCount = operateEles[1].text
            if (commentCount == '评论'):
                commentCount = '0'
            approvalCount = operateEles[2].text
            if (approvalCount == '赞' or approvalCount == ''):
                approvalCount = '0'

            # 获取帖子答案的文本内容
            # 有可能帖子没文字,只有图片,这时也找不到这个p元素和对应的文本,就不收集了(但注意,需要在这之前判断有没有评论,不然可能导致有评论没文字内容,无法收集到评论)
            text = ""
            contentEles = getMoreContent(answered)
            if (len(contentEles) == 2):
                text = contentEles[1].text
            elif (len(contentEles) == 1):
                text = contentEles[0].text
            # else:
            #     text = answered.find_element_by_css_selector('.card-feed>.content>p[node-type="feed_list_content"]').text

            # 所有信息解析完再对数据进行存储操作（防止某个解析崩掉信息不全，如果有信息没解析全，这条信息不会被记录）
            # 获取支持、评论数、作者基本信息
            forwardCounts.append(forwardCount)
            commentCounts.append(commentCount)
            approvalCounts.append(approvalCount)

            profileList = [name, answerTime, device]
            profiles.append(profileList)
            # 回答文本
            contents.append(text)

            # 数据预处理组织成存储到Mysql的形式
            param = (
                name,
                answerTime,
                device,
                forwardCount,
                commentCount,
                approvalCount,
                text,
                keyword
            )

            # # 数据存储到数据库
            # sql = '''
            #         INSERT INTO zhihu_answers(question_name,author_name,author_followers,author_describle,answer_upvotes,answer_create_time,answer_comment_count,answer_content,answer_post_time_ip,keyword) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            #           '''
            # insertData2Mysql(sql, param)

        except (Exception, BaseException) as e:
            print(e)
            continue
        finally:
            print("processing answer ", processCount, ' finished...')
            processCount += 1

    # 清除一下浏览器缓存
    # browser.delete_all_cookies()
    print(approvalCounts)
    print(contents)
    print("upvoteCounts length: ", len(approvalCounts), " contents length: ", len(contents))

# 获取一个问题下的所有回答
def getNormalAnsweredInfo(browser, keyword):
    current_page = 1

    # 不停翻页，直至所有的回答都搜集到
    src = ""
    same_page_count = 0
    # 每页内容不需要滚动动态加载，直接会显示全部的内容
    while True:
        print("start collecting the page ", current_page)
        # 翻到当前页面
        url = 'https://s.weibo.com/weibo?q=' + urllib.parse.quote(keyword) + '&nodup=1&page=' + str(current_page)
        browser.get(url)
        # 获取页面信息
        src_updated = browser.page_source

        # 判断翻页后页面信息没更新,表示没有新的数据了,翻页继续查看是否有更新
        if (src == src_updated):
            same_page_count += 1
            continue
        # 由于可能存在页面更新的bug,所以设置了一个阈值,超过阈值次数后再结束当前关键词搜索
        if (same_page_count > 10):
            break

        src = src_updated
        current_page += 1
        # 由于页面更新了,表明有新的数据,所有要重置统计相同页面信息的次数
        same_page_count = 0

        # 提取页面信息
        extractPageInfo(browser, keyword, getNormalAnsweredInfo)

def getAnsweredInfo(keyword):
    # chromedirver模拟操作浏览器
    chromedriver = "chromedriver"
    os.environ["webdriver.chrome.driver"] = chromedriver
    # 用selenium接管这个浏览器
    chrome_options = Options()
    # 禁止浏览器加载页面图片，防止问题答案过多，加载过程中导致内存不足
    # chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")  # 前面设置的端口号
    browser = webdriver.Chrome(chrome_options=chrome_options)  # executable执行webdriver驱动的文件


    getNormalAnsweredInfo(browser, keyword)

    # browser.quit()

if __name__ == "__main__":
    keywordsList = ['小日本', '日本鬼子']
    # 问题收集
    for keyword in keywordsList:
        # 创建数据库
        getAnsweredInfo(keyword)

