import numpy as np

import cv2 as cv

from matplotlib import pyplot as plt

from hdr import gamma as gc

from utility import imageutil as im
from utility import constants as ct


plt.rc('font', size=ct.SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=ct.SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=ct.MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=ct.SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=ct.SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=ct.SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=ct.BIGGER_SIZE)  # fontsize of the figure title


def generate_hdr_stack_histogram(file_name, file_name_exp, gamma_params, display=ct.DONT_DISPLAY_PLOT):
    # Loads the three images from the exposure folder and generates the plots

    image1 = im.read(ct.EXPOSURE_READ_PATH + "/Correctly_Exposed.JPG")
    image2 = im.read(ct.EXPOSURE_READ_PATH + "/Partly_Saturated.JPG")
    image3 = im.read(ct.EXPOSURE_READ_PATH + "/Really_Saturated.JPG")

    images = [image1, image2, image3]

    exp1 = 1/350
    exp2 = 1/90
    exp3 = 1/30

    exp_times = [exp1, exp2/exp1, exp3/exp1]

    __generate_histogram__(file_name, images, gamma_params, display)
    __generate_exp_histogram__(file_name_exp, images, gamma_params, exp_times, display)

    return images


def __generate_histogram__(file_name, images, gamma_params, display=ct.DONT_DISPLAY_PLOT):
    graph_num = 0
    plt.figure(4)
    for i, image in enumerate(images):
        # Histogram needs Float32 values, which is a callback function
        img = gc.invert_gamma_of_image(image, gamma_params, np.float32)
        for j in range(0, 3):
            graph_num = graph_num + 1
            plt.subplot(int("33" + str(graph_num)))
            hist = im.histogram(img, j, gamma_params)
            plt.plot(hist, color=ct.CHANNEL_COLOUR[j])
            plt.title(ct.CHANNEL[j] + " Channel  \nPicture " + str(i + 1))

    plt.suptitle("HDR Stack Histogram")
    plt.tight_layout()
    plt.subplots_adjust(top=0.8)
    plt.savefig(ct.EXPOSURE_WRITE_PATH + "/" + file_name)

    if display is True:
        plt.show()


def __generate_exp_histogram__(file_name, images, gamma_params, exp_times, display=ct.DONT_DISPLAY_PLOT):
    # Histogram needs Float32 values, which is a callback function
    img1 = (gc.invert_gamma_of_image(images[1], gamma_params, np.float32))/exp_times[1]
    img2 = (gc.invert_gamma_of_image(images[2], gamma_params, np.float32))/exp_times[2]

    img = [img1, img2]
    graph_num = 0
    plt.figure(5)
    for i, image in enumerate(img):
        for j in range(0,3):
            graph_num = graph_num + 1
            plt.subplot(int("23" + str(graph_num)))
            hist = im.histogram(img[i], j, gamma_params)
            plt.plot(hist, color=ct.CHANNEL_COLOUR[j])
            plt.title(ct.CHANNEL[j] + " Channel \nPicture " + str(i + 1))

    plt.suptitle("Histograms for B'(a1*T)/a1 and B'(a2*T)/a2")
    plt.tight_layout()
    plt.subplots_adjust(top=0.8)
    plt.savefig(ct.EXPOSURE_WRITE_PATH + "/" + file_name)

    if display is True:
        plt.show()


def __generate_composite_histogram__(images, display=ct.DONT_DISPLAY_PLOT):
    graph_num = 0
    plt.figure(6)
    for i, image in enumerate(images):
        image = np.float32(image)
        for j in range(0,3):
            graph_num = graph_num + 1
            plt.subplot(int("23" + str(graph_num)))
            hist = cv.calcHist([image], [j], None, [256], [0, 255])
            plt.plot(hist, color=ct.CHANNEL_COLOUR[j])
            plt.title(ct.CHANNEL[j] + "Composite Channel")

    plt.suptitle("Histograms for Composite Image")
    plt.tight_layout()
    plt.subplots_adjust(top=0.8)
    plt.savefig(ct.HDR_WRITE_PATH + "/CompositeHistogram.png")

    if display is True:
        plt.show()
