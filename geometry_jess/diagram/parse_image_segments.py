# coding=utf-8
from scipy import ndimage
import cv2
import numpy as np

from geometry_jess.diagram.states import ImageSegment, ImageSegmentParse
from geometry_jess.ontology.instantiator_definitions import instantiators

__author__ = 'minjoon'


def parse_image_segments(image):
    kernel = np.ones((3,3), np.uint8)
    block_size = 13
    c = 20
    min_area = 20
    min_height = 3
    min_width = 3

    image_segments = _get_image_segments(image, kernel, block_size, c)
    diagram_segment, label_segments = _get_diagram_and_label_segments(image_segments, min_area, min_height, min_width)
    # diagram_segment.display_pixels()
    # print(diagram_segment)
    # print(image)
    image_segment_parse = ImageSegmentParse(image, diagram_segment, label_segments)
    return image_segment_parse



def _get_image_segments(image, kernel, block_size, c):
#이미지를 경계가 확실한 이진 이미지로 바꾸고, label을 통해 선을 찾고,각각의 번호를 주고, 부분으로 slice한뒤,
#  그것을 ImageSegment로 저장한것을 dictionary로 모아서 리턴
    binarized_image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                            cv2.THRESH_BINARY_INV, block_size, c)
    # print "original image: " , image[30]

    # print "thresholid image : ", binarized_image[30]
    labeled, nr_objects = ndimage.label(binarized_image, structure=kernel)
    # print type(labeled)
    # print type(nr_objects)
    slices = ndimage.find_objects(labeled)
    # print(slices)
    # segment별로 분해된 object들
    # print "slice", slices
    image_segments = {}
    # segment 저장용 dictionary
    for idx, slice_ in enumerate(slices):
        offset = instantiators['point'](slice_[1].start, slice_[0].start)
        # print offset
        sliced_image = image[slice_]
        boolean_array = labeled[slice_] == (idx+1)
        # print "slice", sliced_image
        # print "boo", boolean_array

        segmented_image = 255- (255-sliced_image) * boolean_array
        # print "seg" , segmented_image
        pixels = set(instantiators['point'](x, y) for x, y in np.transpose(np.nonzero(np.transpose(boolean_array))))
        binarized_segmented_image = cv2.adaptiveThreshold(segmented_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                                          cv2.THRESH_BINARY_INV, block_size, c)
        # print binarized_segmented_image
        # print "pixels : ", pixels
        # print "offset : ", offset

        image_segment = ImageSegment(segmented_image, sliced_image, binarized_segmented_image, pixels, offset, idx)
        # image_segment.display_segmented_image()
        # image_segment.display_binarized_segmented_image()
        # print "size: " , image.shape
        # image_segment.display_pixels()
        image_segments[idx] = image_segment

    return image_segments


def _get_diagram_and_label_segments(image_segments, min_area, min_height, min_width):
    diagram_segment = max(image_segments.values(), key=lambda s: s.area)

    label_segments = {}
    for key, image_segment in image_segments.iteritems():
        if key == diagram_segment.key:
            continue
        a = image_segment.area >= min_area
        # print image_segment.area
        h = image_segment.shape[1] >= min_height
        w = image_segment.shape[0] >= min_width
        if a and h and w:
            label_segments[key] = image_segment
    # print label_segments
    return diagram_segment, label_segments
