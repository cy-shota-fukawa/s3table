#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import json
from s3_table import S3Table

def main():
    """
    メイン
    """
    # ログインテーブルの削除
    settings = json.load(open("settings/format_loginlog.json", "r"))
    fmt_login = S3Table(**settings)
    fmt_login.drop_table()

    # 課金テーブルの削除
    settings = json.load(open("settings/format_payment_log.json", "r"))
    fmt_payment = S3Table(**settings)
    fmt_payment.drop_table()

    return 0

if __name__ == '__main__':
    sys.exit(main())