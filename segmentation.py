


from numpy import *
import cv2
import numpy
from scipy.cluster.vq import *
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage as ndi

from skimage import data
from skimage.metrics import (adapted_rand_error,
                             variation_of_information)
from skimage.filters import sobel
from skimage.measure import label
from skimage.util import img_as_float
from skimage.feature import canny
from skimage.morphology import remove_small_objects
from skimage.segmentation import (morphological_geodesic_active_contour,
                                  inverse_gaussian_gradient,
                                  watershed,
                                  mark_boundaries)

from skimage import data, img_as_float
from skimage.segmentation import chan_vese


def chanves(image):


    # image = img_as_float(data.camera())
    # Feel free to play around with the parameters to see how they impact the result
    cv = chan_vese(image, mu=0.25, lambda1=1, lambda2=1, tol=1e-3, max_iter=200,
                   dt=0.5, init_level_set="checkerboard", extended_output=True)






    img_cv = cv[1]


    edges = sobel(img_cv)
    im_test1 = watershed(edges, markers=468, compactness=0.001)

    elevation_map = sobel(img_cv)
    markers = np.zeros_like(img_cv)
    markers[image < 30] = 1
    markers[image > 150] = 2
    im_true = watershed(elevation_map, markers)
    im_true = ndi.label(ndi.binary_fill_holes(im_true - 1))[0]

    edges = canny(img_cv)
    fill_coins = ndi.binary_fill_holes(edges)
    im_test2 = ndi.label(remove_small_objects(fill_coins, 21))[0]

    image = img_as_float(img_cv)
    gradient = inverse_gaussian_gradient(image)
    init_ls = np.zeros(image.shape, dtype=np.int8)
    init_ls[10:-10, 10:-10] = 1
    im_test3 = morphological_geodesic_active_contour(gradient, iterations=500,
                                                     init_level_set=init_ls,
                                                     smoothing=1, balloon=-1,
                                                     threshold=0.69)
    im_test3 = label(im_test3)

    method_names = ['Compact watershed', 'Canny filter',
                    'Morphological Geodesic Active Contours']
    short_method_names = ['Compact WS', 'Canny', 'GAC']

    precision_list = []
    recall_list = []
    split_list = []
    merge_list = []
    for name, im_test in zip(method_names, [im_test1, im_test2, im_test3]):
        error, precision, recall = adapted_rand_error(im_true, im_test)
        splits, merges = variation_of_information(im_true, im_test)
        split_list.append(splits)
        merge_list.append(merges)
        precision_list.append(precision)
        recall_list.append(recall)
        print(f"\n## Method: {name}")
        print(f"Adapted Rand error: {error}")
        print(f"Adapted Rand precision: {precision}")
        print(f"Adapted Rand recall: {recall}")
        print(f"False Splits: {splits}")
        print(f"False Merges: {merges}")
    return (mark_boundaries(image,im_true))

