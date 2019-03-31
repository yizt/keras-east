# -*- coding: utf-8 -*-
"""
Created on 2019/3/31 上午11:24

生成器

@author: mick.yi

"""
import numpy as np
from east.utils import geo_utils


def shrink_poly_edge(poly, rs, edge_index):
    """
    内缩四边形的某一条边
    :param poly: [4,(xi,yi)] i<4,第一个点为左上，顺时针排列
    :param rs: 每个顶点的R距离，R距离为顶点的短边距离
    :param edge_index: 需要内缩的边索引号
    :return:
    """
    # 边对应的两个顶点索引号
    idx1, idx2 = edge_index, (edge_index + 1) % 4
    # 边对应的两个顶点
    p1, p2 = poly[idx1], poly[idx2]
    # 顶点对应的r
    r1, r2 = rs[idx1], rs[idx2]
    # 两边内缩
    poly[idx1] = geo_utils.point_shift_on_line(p1, p2, r1 * 0.3)
    poly[idx2] = geo_utils.point_shift_on_line(p2, p1, r2 * 0.3)


def shrink_polygon(poly):
    """
    内缩四边形
    :param poly: [4,(xi,yi)] i<4,第一个点为左上，顺时针排列
    :return:
    """
    # top,right,bottom,left四边的距离
    dist_edges = [np.linalg.norm(poly[i] - poly[(i + 1) % 4]) for i in range(4)]
    # lt,rt,rb,lb四个顶点的ri值，ri为顶点相邻两边的短边长度
    rs = [min(dist_edges[i], dist_edges[(i + 3) % 4]) for i in range(4)]

    # 先缩长边再缩短边;对边确定长边
    if dist_edges[0] + dist_edges[2] > dist_edges[1] + dist_edges[3]:
        # 长边
        shrink_poly_edge(poly, rs, 0)
        shrink_poly_edge(poly, rs, 2)
        # 短边
        shrink_poly_edge(poly, rs, 1)
        shrink_poly_edge(poly, rs, 3)
    else:
        # 长边
        shrink_poly_edge(poly, rs, 1)
        shrink_poly_edge(poly, rs, 3)
        # 短边
        shrink_poly_edge(poly, rs, 0)
        shrink_poly_edge(poly, rs, 2)


class Generator(object):
    def __init__(self, h, w, annotation_list, **kwargs):
        """

        :param h:
        :param w:
        :param annotation_list:
        :param kwargs:
        """
        self.h = h
        self.w = w
        self.annotation_list = annotation_list
        super(Generator, self).__init__(**kwargs)

    def prepare(self):
        for annotation in self.annotation_list:
            for polygon in annotation['polygons']:
                # 最小外接矩形和矩形角度
                rect, angle = geo_utils.min_area_rect_and_angle(polygon)


    def train_gen(self, h, w):
        pass
