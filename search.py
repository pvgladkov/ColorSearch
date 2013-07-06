#-*- coding: UTF-8 -*-

from color import *
from SimpleCV import *
import matplotlib.pyplot as plt
import cv
import time
import sqlite3
import getopt

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
    cur.execute('DROP TABLE "image_colors"')
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


def get_image_id(filename):
    image_id = cur.execute("SELECT id FROM images WHERE filename='%s'" % filename).fetchone()
    return image_id[0]


def insert_relation(image_id, color):
    cur.execute("INSERT INTO image_colors (image_id, color) values (?,?)", (image_id, color))
    con.commit()


def index(filename):
    cv_image = SimpleCV.Image(filename)
    hsv = cv_image.toHSV()
    peaks = hsv.huePeaks()
    colors = []
    for vals in peaks:
        colors.append(round(vals[0]/10)*10)

    image_id = get_image_id(filename)
    for color in colors:
        insert_relation(image_id, color)


def search(color):
    result = cur.execute(
        "SELECT images.filename from image_colors\
         join images on (image_colors.image_id=images.id)\
        where image_colors.color=%s" % color
    ).fetchall()
    print [item[0] for item in result]
    return [item[0] for item in result]


def run(argv):

    try:
        opts, args = getopt.getopt(argv, "ts:image")
    except getopt.GetoptError:
        sys.exit(2)

    if len(args) > 0:
        resultCount = int(args[0])
    else:
        resultCount = 3

    if '-t' == opts[0][0]:
        indx = Indexer()
        images = indx.getImList()

        fill_images(images)
        create_relation_table()

        for image in images:
            index(image)

    elif '-s' == opts[0][0]:

        result = search(opts[0][1])

        for i in range(resultCount):
            cv.NamedWindow('result_'+str(i), cv.CV_WINDOW_NORMAL)
            cv.ShowImage('result_'+str(i), cv.LoadImage(result[i]))
        cv.WaitKey(0)

        for i in result:
            print i

if __name__ == '__main__':

    run(sys.argv[1:])

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
