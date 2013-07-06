#-*- coding: UTF-8 -*-

import os
from config import cfg


class Indexer(object):

    def __init__(self):
        pass

    def getColors(self):
        pass

    def getImList(self):
        """
        получить список файлов
        """
        imageList = [
            os.path.join(cfg.Config.getImageDir(), image) for image in os.listdir(cfg.Config.getImageDir())
            if '.jpg' in image
        ]
        return imageList