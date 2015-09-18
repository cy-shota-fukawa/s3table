#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

from s3table.src import run


def main():
    run.main()
    return 0

if __name__ == '__main__':
    sys.exit(main())