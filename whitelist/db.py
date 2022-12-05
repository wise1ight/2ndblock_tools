import os
import pymysql


DB_HOST = os.environ.get('DB_HOST')
DB_USER = os.environ.get('DB_USER')
DB_DATABASE = os.environ.get('DB_DATABASE')
DB_PASSWORD = os.environ.get('DB_PASSWORD')


class WhitelistDB:
    def count_nickname(self, nickname):
        db = pymysql.connect(host=DB_HOST, user=DB_USER, database=DB_DATABASE, password=DB_PASSWORD)
        curs = db.cursor()

        sql = '''SELECT COUNT(*) FROM `snapshot` WHERE `nickname` = %s'''
        curs.execute(sql, nickname)
        nickname_count = curs.fetchone()
        db.close()
        return nickname_count[0]

    def insert_address(self, nickname, address):
        db = pymysql.connect(host=DB_HOST, user=DB_USER, database=DB_DATABASE, password=DB_PASSWORD)
        curs = db.cursor()

        sql = '''INSERT INTO address (nickname, address) VALUES(%s, %s)'''
        curs.execute(sql, (nickname, address))
        db.commit()
        db.close()
