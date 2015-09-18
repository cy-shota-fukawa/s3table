#!/usr/bin/python
# -*- coding: utf-8 -*-
import MySQLdb

class DB:
    def __init__(self, host, dbname, user, passwd):
        """
        コンストラクタ
        :param host: ホスト
        :param dbname: DB名
        :param user: ユーザ名
        :param passwd: パスワード
        """
        self.host       = host
        self.dbname     = dbname
        self.user       = user
        self.passwd     = passwd
        self.connector  = None

    def __del__(self):
        """
        デストラクタ
        """
        if self.connector is not None:
            self.connector.close()
            self.connector = None

    def disconnect(self):
        """
        接続を切る
        """
        if self.connector is not None:
            self.connector.close()
            self.connector = None

    def connect(self):
        """
        DBに接続
        """
        self.connector = MySQLdb.connect(
            host    = self.host,
            db      = self.dbname,
            user    = self.user,
            passwd  = self.passwd
        )

    def query(self, sql):
        """
        クエリの実行
        :param sql: 流すクエリ
        :return:
        """
        # DBとの接続確認
        if self.connector is None:
            self.connect()

        print sql
        # データ取得
        cursor  = self.connector.cursor()
        cursor.execute(sql)
        self.connector.commit()
        results = cursor.fetchall()
        return results