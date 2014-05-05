insta_mosaic
============

build mosaic from instagram images

langugages used: Python, bash

python libraries used: numpy, re, os, mechanize, BeautifulSoup, hashlib, Image, optparse, MySQLdb, math

1. instagram.py is a python code which scrapes Instagram for images by iterating through a growing list of usernames found during the scraping process. The images are downloaded locally.

2. image2sql.py is a python code which adds the downloaded images to a mySQL database. Data stored includes filename and 10x10 coarse-grained RGB pixel intensity values.

3. mosaic.py is a python code which takes a target image (e.g. target.jpg -- Van Gogh's starry night) and divides it into small squares. Each square is matched to an image file in the mySQL database by finding similar features in the 10x10 coarse-grained pixels. The matched images are treated as "macro-pixels" and assembled together to form a mosaic representation of the target image.
