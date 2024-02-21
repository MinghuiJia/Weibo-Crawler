
import pymysql
def queryDataFromMysql(sql, param=None):
    # 存储到数据库
    # 连接数据库
    conn = pymysql.connect(host='localhost', port=3306,
                           user='root', password='JMHjmh1998',
                           database='crawlerdb')

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = conn.cursor()

    try:
        cursor.execute(sql, param)
        tables = cursor.fetchall()
        return tables
    except Exception as e:
        print(e)
        return None
    finally:
        conn.close()

def insertData2Mysql(sql, param):
    # 存储到数据库
    # 连接数据库
    conn = pymysql.connect(host='localhost', port=3306,
                           user='root', password='JMHjmh1998',
                           database='crawlerdb')

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = conn.cursor()

    try:
        cursor.execute(sql, param)
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()
    finally:
        conn.close()

def get_tables(sql):

    tables = queryDataFromMysql(sql)
    return tables

if __name__ == "__main__":
    sql = '''
                select *
                from weibo_answers_copy;
            '''

    tables = get_tables(sql)

    for i in range(len(tables)):
        param = (
            tables[i][0],
            tables[i][1],
            tables[i][2],
            tables[i][3],
            tables[i][4],
            tables[i][5],
            tables[i][6],
            tables[i][7],
        )
        # 数据存储到数据库
        sql = '''
                INSERT INTO weibo_answers_copy_copy(author_name,answer_post_time,device,forward_count,comment_count,approval_count,post_content,keyword) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                '''
        insertData2Mysql(sql, param)
        print("finished ", i+1, " ...")

    print(len(tables))