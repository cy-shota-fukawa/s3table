#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import json

from s3table.src import tools
from s3_table import S3Table


def main():
    # 引数取得
    options = tools.get_argv()
    options.setting_files = options.setting_files.split(",")

    for setting_file in options.setting_files:
        settings = json.load(open(setting_file, "r"))
        instance = S3Table(**settings)

        if options.create_flg == True:
            # テーブル作成
            instance.setup()

        if options.drop_flg == True:
            # テーブル削除
            instance.drop_table()

    return 0

if __name__ == '__main__':
    sys.exit(main())