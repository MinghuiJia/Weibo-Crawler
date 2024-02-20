# 基于selenium的weibo关键词数据抓取
## 技术实现
  - python selenium 实现微博关键词搜索相关帖子的爬虫程序
  - 由于微博需要进行账号登录，无法直接在selenium自动化测试的脚本情况下进行账号登录
  - 因此，需要使用自己打开的一个浏览器，再用selenium接管这个浏览器这样就可以完成账号登陆
  - chrome映射设置：
    - 增加一个新的映射，以保存原来的chrome不被污染
      - 添加环境变量：将chrome.exe放入系统环境变量中
      - 新建一个存放新环境的文件夹并映射：chrome.exe --remote-debugging-port=9222 --user-data-dir="xxx\selenium_data"
    - selenium代码接管
  - 突破微博关键词查询上线问题（50页内容的限制）
    - 根据关键词搜索返回的内容会限制50页，并且内容也是从最近时刻开始进行获取的
    - 为了获取更多的内容，该项目设置一个endTime，从当前运行项目的时间至endTime期间，按照每间隔一小时的区间进行关键词内容搜索

## 文件夹及文件介绍
  - .\selenium_data文件夹是使用增加新的chrome映射的存放新环境
  - main.py - 主函数执行文件
  - getAnswers.py - 获取关键词对应的微博帖子
