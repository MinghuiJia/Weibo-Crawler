import time

from getAnswers import getAnsweredInfo

if __name__ == "__main__":
    keywordsList = ['小日本', '日本鬼子']
    # 问题收集
    for keyword in keywordsList:
        print("search keyword ", keyword)
        print("start get keyword-related answers")

        # 回答获取
        getAnsweredInfo(keyword)

