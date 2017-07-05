#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import cv2

from copy import move_one_file
from copy import get_file_list
from copy import mkdir
from copy import isfile

def read_info(info):
    infos = open(info)
    return infos


# 通过facedetection结果info查询图片是否合格，是否监测到人脸，不合格就放到bad文件夹
def process_images(img_dir, imgs_info):
    bad_dir = os.path.join(img_dir, "bad")
    good_dir = os.path.join(img_dir, "good")
    if not os.path.exists(bad_dir):
        os.mkdir(bad_dir)
    if not os.path.exists(good_dir):
        os.mkdir(good_dir)
    infos = read_info(imgs_info)
    for info in infos:
        info = info.split(" ")
        img_file = os.path.join(img_dir, info[0])
        if info[1][0] == "0":
            dst = os.path.join(bad_dir, info[0])
            if not os.path.exists(img_file):
                continue
            move_one_file(img_file, dst)
            print "moving %s to %s" % (img_file, dst)
            print "bad"
        else:
            dst = os.path.join(good_dir, info[0])
            move_one_file(img_file, dst)
            print "moving %s to %s" % (img_file, dst)

# 把监测到人脸且有人脸信息的图片保留下来，用下面的函数来检测是否是横屏或者竖屏，分别存放到horizontal和vertical文件夹
def depart_hv(img_dir, info):
    horizontal = os.path.join(img_dir,"horizontal")
    vertical = os.path.join(img_dir,"vertical")
    if not os.path.exists(horizontal):
        os.mkdir(horizontal)
    if not os.path.exists(vertical):
        os.mkdir(vertical)
    infos = read_info(info)
    for info in infos:
        info = info.split(" ")
        img_file = os.path.join(img_dir, info[0])
        if not info[1][0] == "0":
            if not os.path.exists(img_file):
                continue
            img = cv2.imread(img_file)
            if img.shape[0] > img.shape[1]:
                dst = os.path.join(vertical, info[0])
                move_one_file(img_file, dst)
                print "moving %s to %s" % (img_file, dst)
            elif img.shape[0] <= img.shape[1]:
                dst = os.path.join(horizontal, info[0])
                move_one_file(img_file, dst)
                print "moving %s to %s" % (img_file, dst)

# 用下面的函数来判断图片是否高:宽>4:3 或者 高:宽>3:4 phase="vertical"来设置是否是横屏图片或者竖屏图片
def higher_or_wider(img_path, phase = "vertical"):
    img = cv2.imread(img_path)
    higher_rate = img.shape[0]*1.0/img.shape[1]   # 高度比宽度
    if phase == "vertical":
        if higher_rate >= 4.0/3.0:
            return 1, img
        else:
            return 0, img
    elif phase == "horizontal":
        if higher_rate >= 3.0/4.0:
            return 1, img
        else:
            return 0, img
    else:
        raise TypeError

# 用下面的函数对图片进行裁剪，并保存裁剪后的图片到图片文件夹里面crop文件夹
def crop_image(img_dir, info):
    # 把图片坐标信息保存到字典
    infos = open(info)
    img_infos = {}
    for info in infos:
        info = info.split(" ")
        if not info[1][0] == "0":
            img_infos[info[0]] = [info[3].split(":")[1], info[4].split(":")[1].split("\r")[0]]

    count = 0
    # 按照文件名遍历
    horizontal = os.path.join(img_dir, "horizontal")
    vertical = os.path.join(img_dir, "vertical")
    horizontal_filelist = get_file_list(horizontal)
    vertical_filelist = get_file_list(vertical)
    horizontal_crop = os.path.join(horizontal, "crop")
    mkdir(horizontal_crop)
    vertical_crop = os.path.join(vertical, "crop")
    mkdir(vertical_crop)
    # 如果图片是横屏的
    for file_name in horizontal_filelist:
        file_path = os.path.join(horizontal, file_name)
        if not isfile(file_path):
            continue
        count += 1
        print file_name
        higher, img = higher_or_wider(file_path, "horizontal")
        img_height = img.shape[0]
        img_width = img.shape[1]

        # 如果比较高
        if higher:
            y = int(img_infos[file_name][1])
            crop_hight = img.shape[1]*3/4
            if y <= crop_hight/2:
                crop_img = img[0:crop_hight, :]
            elif y > crop_hight/2 and y < img_height-crop_hight/2:    # y2 - y1 = h; (y2 + y1)/2 = y
                crop_img = img[(2*y-crop_hight)/2:(2*y+crop_hight)/2, :]  # y1 = (2*y - h)/2; y2 = (2*y + h)/2
            else:
                crop_img = img[(img_height-crop_hight):img_height, :]
        # 如果图片比较宽
        else:
            x = int(img_infos[file_name][0])
            crop_width = img.shape[0]*4/3
            if x <= crop_width/2:
                crop_img = img[:, 0:crop_width]
            elif x > crop_width/2 and x < img_width-crop_width/2:
                crop_img = img[:, (2*x-crop_width)/2:(2*x+crop_width)/2]
            else:
                crop_img = img[:, (img_width-crop_width):img_width]
        print "processing %d horizontal %s:" % (count, file_name), crop_img.shape, crop_img.shape[0]*1.0/crop_img.shape[1]
        horizontal_crop_file_path = os.path.join(horizontal_crop, file_name)
        cv2.imwrite(horizontal_crop_file_path, crop_img)

    # 如果图片是竖屏的
    for file_name in vertical_filelist:
        file_path = os.path.join(vertical, file_name)
        if not isfile(file_path):
            continue
        count += 1
        print file_name
        higher, img = higher_or_wider(file_path, "vertical")
        img_height = img.shape[0]
        img_width = img.shape[1]
        # 如果图片比较高
        if higher:
            y = int(img_infos[file_name][1])
            crop_hight = img.shape[1] * 4 / 3
            if y <= crop_hight / 2:
                crop_img = img[0:crop_hight, :]
            elif y > crop_hight/2 and y < img_height - crop_hight/2:  # y2 - y1 = h; (y2 + y1)/2 = y
                crop_img = img[(2*y - crop_hight)/2:(2*y + crop_hight)/2,:]  # y1 = (2*y - h)/2; y2 = (2*y + h)/2
            else:
                crop_img = img[(img_height - crop_hight):img_height, :]
        # 如果图片比较宽
        else:
            x = int(img_infos[file_name][0])
            crop_width = img.shape[0] * 3 / 4
            if x <= crop_width / 2:
                crop_img = img[:, 0:crop_width]
            elif x > crop_width/2 and x < img_width - crop_width/2:
                crop_img = img[:, (2*x - crop_width)/2:(2*x + crop_width)/2]
            else:
                crop_img = img[:, (img_width - crop_width):img_width]
        print "processing %d vertical %s:" % (count, file_name), crop_img.shape, crop_img.shape[0]*1.0/crop_img.shape[1]
        vertical_crop_file_path = os.path.join(vertical_crop, file_name)
        cv2.imwrite(vertical_crop_file_path, crop_img)


def test():
    img = cv2.imread("my.jpg")
    print img.shape[0]

if __name__ == "__main__":
    info = "baidu_info.txt"
    img_dir = "baidu_images"
    crop_image(img_dir, info)
    #test()