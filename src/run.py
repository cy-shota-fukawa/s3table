#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import json
from s3_table import S3Table

def main():
    """
    メイン
    """
    settings = json.load(open("settings.json", "r"))
    instance = S3Table(**settings)
    instance.setup()
    return 0

if __name__ == '__main__':
    sys.exit(main())g