from pathlib import Path
import cv2
import numpy as np
import math

# Define paths to sub-folders
root_dir = Path.cwd()
images_path = root_dir / '..' / 'test_images'

def canny(image, sigma=0.33):
    # compute the median of the single channel pixel intensities
    v = np.median(image)
    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)
    # return the edged image
    return edged

def plot_line(img, rho, theta):
    # Plots the line coming out of a Hough Line Transform
    a = math.cos(theta)
    b = math.sin(theta)
    x0 = a * rho
    y0 = b * rho
    pt1 = (int(x0 + 10000*(-b)), int(y0 + 10000*(a)))
    pt2 = (int(x0 - 10000*(-b)), int(y0 - 10000*(a)))
    cv2.line(img, pt1, pt2, (0, 255, 0), 3, cv2.LINE_AA)

def prune_lines(lines):
    # Prunes the list of lines using some tricks
    line_list = [line[0] for line in lines]
    # Remove the thetas that are too vertical
    theta_pruned = [a for a in line_list if np.pi/3 <= a[1] < 2*np.pi/3]
    avg_p = np.mean([line[0] for line in theta_pruned])
    avg_theta = np.mean([line[1] for line in theta_pruned])
    return avg_p, avg_theta


for image_path in list(images_path.glob('*.png')):
    image = cv2.imread(str(image_path))
    # Blur image and convert to grayscale
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(image, (3, 3), 0)
    # Use Canny edge detection to find edges
    edges = canny(image)
    # Use Hough Line Transform to get lines
    threshold = 100
    lines = cv2.HoughLines(edges, 40, np.pi / 45, threshold, None, 0, 0)
    if lines is not None:
        print('Found %s lines' % (len(lines)))
#         # Print all lines
#         for line in lines:
#             for rho,theta in line:
#                 plot_line(edges, rho, theta)
        # Average line
        avg_rho, avg_theta = prune_lines(lines)
        plot_line(image, avg_rho, avg_theta)
    else:
        print('No Horizon Found')

    cv2.imshow("Original", image)
    # cv2.imshow("Edges", edges)
    cv2.waitKey(0)