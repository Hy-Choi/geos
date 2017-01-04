import os


from computational_geometry import normalize_angle, horizontal_angle, area_of_polygon
from get_instances import get_all_instances
from geometry_jess.diagram.parse_confident_formulas import parse_confident_formulas
from geometry_jess.diagram.parse_core import parse_core
from geometry_jess.diagram.parse_graph import parse_graph
from geometry_jess.diagram.parse_image_segments import parse_image_segments
from geometry_jess.diagram.parse_primitives import parse_primitives
from geometry_jess.diagram.select_primitives import select_primitives
from geometry_jess.utils.prep import open_image
import cv2

import numpy as np

__author__ = 'minjoon'



def run_graph(filepath):
    image_segment_parse = parse_image_segments(open_image(filepath))
    primitive_parse = parse_primitives(image_segment_parse)
    selected_primitive_parse = select_primitives(primitive_parse)
    core_parse = parse_core(selected_primitive_parse)
    graph_parse = parse_graph(core_parse)
    # core_parse.save_points_image(str(filename))
    return graph_parse



def test_computational_geometry():
    ans = area_of_polygon([(0,0), (1,0), (1,1), (0,1)])
    print ans

def test_labelparsing():
    image_segment_parse = parse_image_segments(open_image("../../input/math22.png"))

    image_segment_parse.display_diagram()

    for idx,seg in image_segment_parse.label_image_segments.items():
        if seg.area >= 100:
            print "idx . area : ", seg .area
            print seg.binarized_segmented_image
            resize_label_segment(seg.binarized_segmented_image)
            seg.display_segmented_image()
        # if seg.area >= 100:
            # print seg.area
            # seg.display_segmented_image()

    # image_segment_parse.display_labels()
    # primitive_parse = parse_primitives(image_segment_parse)
    #
    # primitive_parse.image_segment_parse()
    # selected = select_primitives(primitive_parse)
    # core_parse = parse_core(selected)
    # image = core_parse.get_image_points()
    # cv2.imwrite("../../", image)

def resize_label_segment(image):
    size = 36,36
    load_newimg = np.zeros((size))
    i_offset = (36 - image.shape[0]) / 2
    j_offset = (36 - image.shape[1]) / 2
    for i in range(0, image.shape[0]):
        for j in range(0, image.shape[1]):
            load_newimg[i + i_offset,j + j_offset] = image[i,j]

    for i in range(36):
        print load_newimg[i]

if __name__ == "__main__":
    # test_parse_image_segments()
    # save_parse_image_segments()
    # test_parse_primitives()
    # save_parse_primitives()
    # test_select_primitives()
    # save_select_primitives()
    # test_parse_core()
    # save_parse_core()
    # test_computational_geometry()
    # a = [1020]
    # for num in a:
    #     test_result(num)
    # filename = ""
    # run_graph(filename)
    test_labelparsing()


