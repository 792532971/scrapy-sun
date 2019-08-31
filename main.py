# -*- coding: utf-8 -*-

from scrapy.cmdline import execute

import sys
import os

# print(os.path.abspath(__file__))
sys.path.append(os.path.abspath(__file__))
execute(["scrapy", "crawl", "sun0769"])