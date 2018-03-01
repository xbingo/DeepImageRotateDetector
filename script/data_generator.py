#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from PIL import Image
from PIL import ImageFile
import shutil


ImageFile.LOAD_TRUNCATED_IMAGES = True

SRC_PATH = '/Users/rubinxie/data/qzone_tag_data/20180110'
DST_PATH = '/Users/rubinxie/data/TestRotate'
IMG_SUFFIX = ['.jpg', '.png', '.bmp']
SIZE_THRESHOLD = 3 * 1024
DIR_NAME = ['up', 'left', 'down', 'right']
DIRECT = [0, 90, 180, 270]
TAGET_SIZE = 224


def save_file(img, direct, file_name):
    save_path = os.path.join(DST_PATH, DIR_NAME[direct], file_name + '.jpg')
    img.save(save_path)


def process(path):
    for root, dirs, files in os.walk(path):
        for d in dirs:
            process(os.path.join(root, d))
        for f in files:
            split = os.path.splitext(f)
            if split[1].lower() not in IMG_SUFFIX:
                continue
            photo_path = os.path.join(root, f)
            if os.path.getsize(photo_path) < SIZE_THRESHOLD:
                continue
            img = Image.open(photo_path).convert('RGB')
            small_img = img.resize((TAGET_SIZE, TAGET_SIZE), Image.BICUBIC)
            save_file(small_img, 0, split[0])

            for i in range(1, 4):
                dst_img = small_img.rotate(DIRECT[i])
                save_file(dst_img, i, split[0])


for dir_name in DIR_NAME:
    d = os.path.join(DST_PATH, dir_name)
    if os.path.exists(d):
        shutil.rmtree(d)
    os.makedirs(d)

process(SRC_PATH)
