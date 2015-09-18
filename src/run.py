#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import tools
import create_tables
import drop_tables

def main():
    # 引数取得
    options = tools.get_argv()

    if options.create_flg == True:
        # テーブル作成
        create_tables()

    if options.drop_flg == True:
        # テーブル削除
        drop_tables()

    return 0

if __name__ == '__main__':
    sys.exit(main())