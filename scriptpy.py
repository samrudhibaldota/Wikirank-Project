# -*- coding: utf-8 -*-
"""scriptpy.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/13D6Q_jBrxbGvEQ84Brhw1qwVjA2hHVT9
"""

import bz2
from lxml import etree

with bz2.open("simplewiki-latest-pages-articles.xml.bz2", 'rt', encoding='utf-8') as f:
    for event, elem in etree.iterparse(f, events=('start',)):
        print("Root tag:", elem.tag)
        break