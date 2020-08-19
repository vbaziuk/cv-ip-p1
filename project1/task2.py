"""
Template Matching
(Due date: Sep. 25, 3 P.M., 2019)

The goal of this task is to experiment with template matching techniques, i.e., normalized cross correlation (NCC).

Please complete all the functions that are labelled with '# TODO'. When implementing those functions, comment the lines 'raise NotImplementedError' instead of deleting them. The functions defined in 'utils.py'
and the functions you implement in 'task1.py' are of great help.

Do NOT modify the code provided to you.
Do NOT use ANY API provided by opencv (cv2) and numpy (np) in your code.
Do NOT import ANY library (function, module, etc.).
"""


import argparse
import json
import os

import utils
from task1 import *


def parse_args():
    parser = argparse.ArgumentParser(description="cse 473/573 project 1.")
    parser.add_argument(
        "--img-path",
        type=str,
        default="./data/proj1-task2.jpg",
        help="path to the image")
    parser.add_argument(
        "--template-path",
        type=str,
        default="./data/proj1-task2-template.jpg",
        help="path to the template"
    )
    parser.add_argument(
        "--result-saving-path",
        dest="rs_path",
        type=str,
        default="./results/task2.json",
        help="path to file which results are saved (do not change this arg)"
    )
    args = parser.parse_args()
    return args

def norm_xcorr2d(patch, template):
    """Computes the NCC value between a image patch and a template.

    The image patch and the template are of the same size. The formula used to compute the NCC value is:
    sum_{i,j}(x_{i,j} - x^{m}_{i,j})(y_{i,j} - y^{m}_{i,j}) / (sum_{i,j}(x_{i,j} - x^{m}_{i,j}) ** 2 * sum_{i,j}(y_{i,j} - y^{m}_{i,j})) ** 0.5
    This equation is the one shown in Prof. Yuan's ppt.

    Args:
        patch: nested list (int), image patch.
        template: nested list (int), template.

    Returns:
        value (float): the NCC value between a image patch and a template.
    """

    # computing template mean
    template_sum = 0
    n_template_items = 0
    for i in range(len(template)):
        for j in range(len(template[0])):
            template_sum += template[i][j]
            n_template_items += 1

    mean_template = template_sum / n_template_items

    # computing image patch mean
    patch_sum = 0
    n_patch_items = 0
    for i in range(len(patch)):
        for j in range(len(patch[0])):
            patch_sum += patch[i][j]
            n_patch_items += 1

    mean_patch = patch_sum / n_patch_items

    # computing numerator for NCC formula
    numerator = 0
    for k in range(len(template)):
        for l in range(len(template[0])):
            numerator += (template[k][l] - mean_template) * (patch[k][l] - mean_patch)

    # computing denominator for NCC formula
    left_sum = 0
    for k in range(len(template)):
        for l in range(len(template[0])):
            left_sum += (template[k][l] - mean_template) ** 2

    right_sum = 0
    for k in range(len(template)):
        for l in range(len(template[0])):
            right_sum += (patch[k][l] - mean_patch) ** 2

    denominator = (left_sum * right_sum) ** 0.5

    ncc_result = numerator / denominator

    return ncc_result

    raise NotImplementedError

def match(img, template):
    """Locates the template, i.e., a image patch, in a large image using template matching techniques, i.e., NCC.

    Args:
        img: nested list (int), image that contains character to be detected.
        template: nested list (int), template image.

    Returns:
        x (int): row that the character appears (starts from 0).
        y (int): column that the character appears (starts from 0).
        max_value (float): maximum NCC value.
    """

    # Run crop() function, returns patch. This gets passed into the norm_xcorr2d() function.
    # run compares to find highest NCC value.

    x_val = 0
    y_val = 0
    max_ncc = 0
    highest_ncc = 0

    # iterating through the image to find the highest NCC value.
    for x in range(len(img) - len(template)):
        for y in range(len(img[0]) - len(template[0])):

            # obtaining the patch
            patch = utils.crop(img, x, x+len(template), y, y+len(template[0]))

            # print(x, x+len(template), y, y+len(template[0]))

            # determining NCC value
            ncc_val = norm_xcorr2d(patch, template)

            # finding highest NCC value
            if ncc_val > highest_ncc:
                x_val = x
                y_val = y
                max_ncc = ncc_val
                highest_ncc = ncc_val

    return x_val, y_val, max_ncc

    # TODO: implement this function.
    # raise NotImplementedError
    raise NotImplementedError

def save_results(coordinates, template, template_name, rs_directory):
    results = {}
    results["coordinates"] = sorted(coordinates, key=lambda x: x[0])
    results["templat_size"] = (len(template), len(template[0]))
    with open(os.path.join(rs_directory, template_name), "w") as file:
        json.dump(results, file)


def main():
    args = parse_args()

    img = read_image(args.img_path)
    # template = utils.crop(img, xmin=10, xmax=30, ymin=10, ymax=30)
    # template = np.asarray(template, dtype=np.uint8)
    # cv2.imwrite("./data/proj1-task2-template.jpg", template)
    template = read_image(args.template_path)

    x, y, max_value = match(img, template)
    # The correct results are: x: 17, y: 129, max_value: 0.994
    with open(args.rs_path, "w") as file:
        json.dump({"x": x, "y": y, "value": max_value}, file)


if __name__ == "__main__":
    main()
