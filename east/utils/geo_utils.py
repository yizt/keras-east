# -*- coding: utf-8 -*-
"""
Created on 2019/3/30 下午9:07

几何图形工具类

@author: mick.yi

"""

import numpy as np
import cv2


def dist_point_to_line(p1, p2, p3):
    """
    点p3到直线(p1,p2)的距离
    :param p1: [x,y]
    :param p2: [x,y]
    :param p3: [x,y]
    :return:
    """
    # 以(p1,p3),(p2,p3)为边的平行四边形面积
    area = np.cross(p1 - p3, p2 - p3)
    # 点p3到直线(p1,p2)的距离=area除以边(p1,p2)的距离
    dist_p1_p2 = np.linalg.norm(p1 - p2)
    return area / dist_p1_p2


def elem_cycle_shift(elements, shift):
    """
    将元素位移指定长度;
    如：elements=[1,2,3,4] shift=1 则返回[2,3,4,1]
                       shift=2 则返回[3,4,1,2]
                       shift=-1 则返回[4,1,2,3]
                       shift > 0 左移，反之，右移
    :param elements: 元素列表list of elem
    :param shift: 位移长度
    :return:
    """
    length = len(elements)
    return [elements[(i + shift) % length] for i in range(length)]


def min_area_rect_and_angle(polygon):
    """
    包围多边形的最小矩形框
    :param polygon:
    :return:
    """
    rect = cv2.minAreaRect(polygon)  # ((ctx,cty),(w,h),angle) angle为负
    box = cv2.boxPoints(rect)  # 边框四个坐标[4,2];顺时针排列,第一个坐标是y值最大的那个
    # 角度
    angle = abs(rect[2])
    if angle == 0:
        if box[0][0] == np.max(box[:, 0]):  # box[0]是右下角
            box = elem_cycle_shift(list(box), 2)
        else:  # box[0]是左下角
            box = elem_cycle_shift(list(box), 1)
    elif angle <= 45:  # box[0]是左下角
        box = elem_cycle_shift(list(box), 1)
    else:  # box[0]是右下角
        box = elem_cycle_shift(list(box), 2)

    # angle转为pi表示
    return box, angle * np.pi / 180


def dist_point_to_rect(point, box):
    """
    点到矩形框4条边的距离
    :param point: numpy数组[(x,y)]
    :param box: 矩形框的顶点，numpy数组[4,(xi,yi)];  (x0,y0)代表左上顶点，顺时针方向排列
    :return: 返回点到矩形框上边，右边，下边，左边的距离
    """
    dist_top, dist_right, dist_bottom, dist_left = [dist_point_to_line(
        box[i], box[(i + 1) % 4], point) for i in range(4)]
    return dist_top, dist_right, dist_bottom, dist_left


def main():
    print(elem_cycle_shift([1, 2, 3, 4], 1))
    print(elem_cycle_shift([1, 2, 3, 4], 2))
    print(elem_cycle_shift([1, 2, 3, 4], -1))


if __name__ == '__main__':
    main()
