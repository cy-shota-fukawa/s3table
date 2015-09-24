#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import commands
from db import DB

class S3Table:
    def __init__(self, table_name, columns, load_files, db_settings, separator, init_sqls):
        self.table_name = table_name
        self.columns = columns
        self.load_files = load_files
        self.db_settings = db_settings
        self.separator = separator
        self.init_sqls = init_sqls
        self.db = None

    def __del__(self):
        """
        デストラクタ
        :return:
        """
        # テーブルの削除(DROP文)
        pass

    def connect_db(self):
        """
        DB接続
        """
        # DB接続
        if self.db is None:
            self.db = DB(**self.db_settings)
            self.db.connect()
            for sql in self.init_sqls:
                self.db.query(sql)

    def disconnect_db(self):
        """
        # 接続を切る
        """
        self.db.disconnect()

    def setup(self):
        """
        テーブルの作成、データの用意まで
        :return:
        """
        # DBへ接続
        self.connect_db()

        # テーブルの作成
        self.create_table()

        # INDEXをはる
        self.add_index()

        # ファイルのダウンロード
        cp_files = self.get_s3_files()

        # データをDBに入れる
        self.load_data(cp_files)

        # DBへの接続を切る
        self.disconnect_db()

    def get_s3_files(self):
        """
        S3からファイルをダウンロード
        :return: ダウンロードしたファイルのリスト
        """
        cp_files = []
        self.load_files = self.wild_process(self.load_files)
        for path in self.load_files:
            print "path : ", path
            # ファイルダウンロード
            os.system("aws s3 cp %s ./" % path)

            # 後でローカルファイルを削除するために保存しておく
            cp_files.append(path.split("/")[-1])

        return cp_files

    def wild_process(self, load_files):
        """
        ワイルドカード用の処理
        :param load_files:
        :return:
        """
        results = []
        for load_file in load_files:
            if load_file.endswith("/"):
                # ワイルドカード対応
                """
                ファイルリストを出す必要がある
                """
                # ファイルリストを取得
                cmd = "aws s3 ls %s" % load_file
                res = commands.getoutput(cmd)

                # 日付、容量、ファイル名の形になっているのでファイル名だけを取得
                for row in res.split("\n"):
                    file_name = row.split(" ")[-1]
                    results.append(file_name)
            else:
                results.append(load_file)
        return results

    def load_data(self, cp_files):
        """
        DBにデータを入れる
        :return:
        """
        for cp_file in cp_files:
            # データロード用のSQLを取得
            sql = """
            LOAD DATA LOCAL INFILE '%s' REPLACE INTO TABLE %s FIELDS TERMINATED BY '%s' ENCLOSED BY '"'
            """ % (cp_file, self.table_name, self.separator)
            self.db.query(sql)

            # ローカルに保存したファイルを削除
            os.system("rm %s" % cp_file)
        return 0

    def create_table(self):
        """
        テーブル作成用のSQL作成
        """
        # SQLの作成
        columns = ["%s %s" % (d[0], d[1]) for d in self.columns]
        sql = "CREATE TABLE %s (%s);" % (self.table_name, ",".join(columns))
        self.db.query(sql)

    def add_index(self):
        """
        インデックス用のSQL作成
        """
        index_columns = [d[0] for d in self.columns if d[2] == True]
        sql = "ALTER TABLE %s ADD INDEX %s_index (%s);" % (self.table_name, self.table_name, ",".join(index_columns))
        self.db.query(sql)

    def drop_table(self):
        """
        テーブル削除用のクエリ作成
        :return:
        """
        # DBへ接続をする
        self.connect_db()

        sql = "DROP TABLE %s.%s;" % (self.db_settings["dbname"], self.table_name)
        self.db.query(sql)

        # DBへの接続を切る
        self.disconnect_db()