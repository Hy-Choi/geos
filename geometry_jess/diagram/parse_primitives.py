import numpy as np
import cv2
import math
from geometry_jess.diagram.states import ImageSegmentParse, PrimitiveParse
from geometry_jess.diagram.computational_geometry import dot_distance_between_points
from geometry_jess.ontology.instantiator_definitions import instantiators
from geometry_jess.parameters import hough_line_parameters as line_params
from geometry_jess.parameters import hough_circle_parameters as circle_params
from geometry_jess.utils.num import dimension_wise_non_maximum_suppression
import cv2.cv as cv

__author__ = 'minjoon'


def parse_primitives(image_segment_parse):
    assert isinstance(image_segment_parse, ImageSegmentParse)
    diagram_segment = image_segment_parse.diagram_image_segment
    lines = _get_lines(diagram_segment, line_params)
    circles = _get_circles(diagram_segment, circle_params)
    line_dict = {idx: line for idx, line in enumerate(lines)}
    # print "line : ", line_dict
    circle_dict = {idx + len(lines): circle for idx, circle in enumerate(circles)}
    primitive_parse = PrimitiveParse(image_segment_parse, line_dict, circle_dict)
    return primitive_parse


def _get_lines(image_segment, params):
    lines = []
    # print image_segment.segmented_image
    # temp = cv2.HoughLines(image_segment.segmented_image, params.rho, params.theta, 30)
    # image_segment.display_segmented_image()
    edges = cv2.Canny(image_segment.segmented_image, 50 , 300)
    # print edges.shape
    temp = cv2.HoughLines(edges, params.rho, params.theta, 45)

    # print temp.shape

    # img_edge = cv2.Canny( image_segment.segmented_image, 50, 150, 2 )
    #
    # temp = cv2.HoughLines(img_edge,1,np.pi/180,100)
    # lines = cv2.HoughLinesP(img_edge,1,np.pi/180,100,minLineLength=100,maxLineGap=10 )

    # for x1,y1,x2,y2 in lines[0]:
    #     cv2.line(image_segment.segmented_image,(x1,y1),(x2,y2),(0,0,255),1)
    # print "temp size :", temp.shape
    #
    # for rho,theta in temp[0]:
    #     x1=int(np.cos(theta)*rho+1000*(-np.sin(theta)))
    #     y1=int(np.sin(theta)*rho+1000*np.cos(theta))
    #     x2=int(np.cos(theta)*rho-1000*(-np.sin(theta)))
    #     y2=int(np.sin(theta)*rho-1000*np.cos(theta))
    #     cv2.line(image_segment.segmented_image, (x1,y1), (x2,y2), (0,0,255), 1)
    #
    # cv2.imshow('result', image_segment.segmented_image)
    # cv2.waitKey(0)
    # if temp is None:
    #     temp = cv2.HoughLines(edges, 1, math.pi / 180.0, 45, np.array([]), 10, 0)
    #     if temp is None:
    #         temp = cv2.HoughLines(edges, 1, math.pi / 180.0, 15, np.array([]), 10, 0)
    #         if temp is None:
    #             temp = cv2.HoughLines(edges, 1, math.pi / 180.0, 60, np.array([]), 10, 0)



    # print(temp)
    # if temp[0] is not None:
    #     a, b, c = temp.shape
    #     for i in range(b):
    #         rho = temp[0][i][0]
    #         theta = temp[0][i][1]
    #         a = math.cos(theta)
    #         b = math.sin(theta)
    #         x0, y0 = a * rho, b * rho
            # pt1 = (int(x0 + 1000 * (-b)), int(y0 + 1000 * (a)))
            # pt2 = (int(x0 - 1000 * (-b)), int(y0 - 1000 * (a)))
            # cv2.line(image_segment.segmented_image, pt1, pt2, (0, 0, 255), 1, cv2.CV_AA)
            # print("pt1,2 " ,pt1, pt2)
    # else:
    #     print("\nno line is detected.")
    # cv2.imshow('original', image_segment.segmented_image)
    # cv2.waitKey(0)


    if temp is None:
        return lines
    # print "***********", temp.size

    rho_theta_pairs = [temp[0][idx] for idx in range(len(temp[0]))]
    # print rho_theta_pairs
    if len(rho_theta_pairs) > params.max_num:
        rho_theta_pairs = rho_theta_pairs[:params.max_num]

    # nms_rho_theta_pairs = dimension_wise_non_maximum_suppression(rho_theta_pairs, (params.nms_rho, params.nms_theta), _dimension_wise_distances_between_rho_theta_pairs)

    for rho_theta_pair in rho_theta_pairs:
        curr_lines = _segment_line(image_segment, rho_theta_pair, params)
        lines.extend(curr_lines)

    return lines


def _get_circles(image_segment, params):
    temp = cv2.HoughCircles(image_segment.segmented_image, cv.CV_HOUGH_GRADIENT, params.dp, params.minDist,
                            param1=params.param1, param2=params.param2,
                            minRadius=params.minRadius, maxRadius=params.maxRadius)
    # print temp
    if temp is None:
        return []

    circle_tuples = temp[0]
    if len(circle_tuples) > params.max_num:
        circle_tuples = circle_tuples[:params.max_num]

    circles = [instantiators['circle'](instantiators['point'](x, y), radius)
               for x, y, radius in circle_tuples]
    return circles


def _segment_line(image_segment, rho_theta_pair, params):
    lines = []
    near_pixels = _get_pixels_near_rho_theta_pair(image_segment.pixels, rho_theta_pair, params.eps)
    if len(near_pixels) == 0:
        return lines

    reference_pixel = near_pixels[0]
    distances = [dot_distance_between_points(_rho_theta_pair_unit_vector(rho_theta_pair), p, reference_pixel)
                 for p in near_pixels]
    order = np.argsort(distances)
    start_idx = None
    end_idx = None

    for order_idx, idx in enumerate(order):
        if start_idx is None:
            start_idx = idx
            end_idx = idx
        else:
            d0 = distances[idx]
            d1 = distances[order[order_idx - 1]]
            if abs(d0 - d1) > params.max_gap or order_idx == len(order) - 1:
                length = abs(distances[start_idx] - distances[end_idx])
                if length > params.min_length:
                    p0 = near_pixels[start_idx]
                    p1 = near_pixels[end_idx]
                    line = instantiators['line'](p0, p1)
                    lines.append(line)
                start_idx = None
            else:
                end_idx = idx

    return lines


def _get_pixels_near_rho_theta_pair(pixels, rho_theta_pair, eps):
    near_pixels = [pixel for pixel in pixels
                   if _distance_between_rho_theta_pair_and_point(rho_theta_pair, pixel) <= eps]
    return near_pixels


def _distance_between_rho_theta_pair_and_point(rho_theta_pair, point):
    rho, theta = rho_theta_pair
    x, y = point
    return abs(rho - x * np.cos(theta) - y * np.sin(theta))


def _rho_theta_pair_unit_vector(rho_theta_pair):
    _, theta = rho_theta_pair
    return tuple([np.sin(theta), -np.cos(theta)])


def _dimension_wise_distances_between_rho_theta_pairs(pair0, pair1):
    rho0, theta0 = pair0
    rho1, theta1 = pair1
    rho_distance = abs(rho0 - rho1)
    theta_distance = min(abs(theta0 - theta1),
                         abs(theta0 - theta1 + 2 * np.pi),
                         abs(theta0 - theta1 - 2 * np.pi))
    return rho_distance, theta_distance
