#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
from os import listdir
from datetime import date
from optparse import OptionParser

# =========================
# 引数関連
# =========================
def get_argv():
    """
    引数を変数に
    :param work_space: ワークスペース
    :param dir_name: ディレクトリ名
    """
    parser = OptionParser()
    parser.add_option("--contents_codes", dest="contents_codes", default=None)
    parser.add_option("--target_date", dest="target_date", default=None)
    parser.add_option("--dir_name", dest="dir_name", default="cynapse")
    parser.add_option("--start_date", dest="start_date", default=None)
    parser.add_option("--end_date", dest="end_date", default=None)
    parser.add_option("--create", action="store_true", dest="create_flg", default=False)
    parser.add_option("--drop", action="store_true", dest="drop_flg", default=False)

    (options, args) = parser.parse_args()

    return options

def change_date_format(str_date):
    """
    文字列(YYYY-MM-DD)を日付型にして返す
    :param str_date: 文字列
    :return: 日付型に変換したもの
    """
    d = str_date.split("-")
    return date(int(d[0]), int(d[1]), int(d[2]))

def replace_tags(text, contents_code="", platform="", target_date="", log_type=""):
    """
    タグを置換
    :param text: 置換元文字列
    :param contents_code: 置換に使用するコンテンツコード
    :param platform: 置換に使用するプラットフォーム名
    :param target_date: 置換に使用する日付
    :return: 置換後の文字列
    """
    return text.replace("<CONTENTS_CODE>", contents_code)\
               .replace("<PLATFORM>",      platform)\
               .replace("<YEAR>",          target_date.strftime("%Y"))\
               .replace("<MONTH>",         target_date.strftime("%m"))\
               .replace("<DAY>",           target_date.strftime("%d"))\
               .replace("<LOG_TYPE>",      log_type)