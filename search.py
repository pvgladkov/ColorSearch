#-*- coding: UTF-8 -*-

from color import *
from SimpleCV import *
import matplotlib.pyplot as plt
import cv
import time
import sqlite3

con = sqlite3.connect('searcher.db')
with con:
    cur = con.cursor()


def create_images_table():
    cur.execute('DROP TABLE "images"')
    cur.execute('CREATE TABLE "images" (\
        "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,\
        "name" TEXT,\
        "filename" TEXT\
    )')
    con.commit()


def create_relation_table():
    cur.execute('CREATE TABLE "image_colors" (\
        "image_id" INTEGER NOT NULL,\
        "color" INTEGER NOT NULL\
    )')
    con.commit()


def fill_images(images):
    create_images_table()
    for image in images:
        cur.execute("INSERT INTO images (name, filename) values(?, ?)",  (image, image))
    con.commit()


def index(filename):
    cv_image = SimpleCV.Image(filename)
    hsv = cv_image.toHSV()
    peak = hsv.huePeaks()


if __name__ == '__main__':

    indx = Indexer()
    images = indx.getImList()

    fill_images(images)

    #print image

    #cv_image = SimpleCV.Image(image)
    #hsv = cv_image.toHSV()

    # гистограмма иненсивности
    #hist = hsv.histogram(255)

    #
    #hist = hsv.hueHistogram()
    #peak = hsv.huePeaks()
    #print peak
    #peak_one = peak[1][0]
    #print peak_one
    #hue = cv_image.hueDistance(peak_one)
    #hue.show()
    #time.sleep(10000)
    #cv.NamedWindow('image', cv.CV_WINDOW_NORMAL)
    #cv.ShowImage('image', cv.LoadImage(image))
    #cv.WaitKey(0)
    #plt.plot(hist)
    #plt.show()
    #SimpleCV.plot(hist)
