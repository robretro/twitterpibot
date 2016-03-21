import os
import random

from twitterpibot.logic import googlehelper, fsh

__author__ = 'andrewtatham'
folder = fsh.root + "temp" + os.sep + "images" + os.sep + "imagemanager" + os.sep


def get_image(topics):
    topic = random.choice(topics)
    images = googlehelper.get_search_images(topic, 5)
    image_url = random.choice(images)
    file_path = fsh.download_file(folder, image_url, topic + ".jpg")
    return file_path