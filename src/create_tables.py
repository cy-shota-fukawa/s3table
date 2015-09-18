#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import json
from s3_table import S3Table

def main():
    """
    メイン
    """

    # ログインテーブルの作成
    settings = json.load(open("settings/format_loginlog.json", "r"))
    fmt_login = S3Table(**settings)
    fmt_login.setup()

    # 課金テーブルの作成
    settings = json.load(open("settings/format_payment_log.json", "r"))
    fmt_payment = S3Table(**settings)
    fmt_payment.setup()

    return 0

if __name__ == '__main__':
    sys.exit(main())