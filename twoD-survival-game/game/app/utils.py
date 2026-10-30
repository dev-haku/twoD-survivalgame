import pygame
import json

from os.path import supports_unicode_filenames
import random
import math


def gradient(x, y, seed):
    value = hash_value(x, y, seed)

    angle = value * 2 * math.pi

    return (
        math.cos(angle),
        math.sin(angle)
    )

def hash_value(x, y, seed):
    value = x * 374761393
    value += y * 668265263
    value += seed * 1442695041

    value = (value ^ (value >> 13)) * 1274126177
    value = value ^ (value >> 16)

    return (value & 0xffffffff) / 0xffffffff

def fade(t):
    return t * t * t * (t * (t * 6 - 15) + 10)

def lerp(a, b, t):
    return a + (b - a) * t

def noise(x, y, seed):
    # ① 座標が入っている格子を求める
    x0 = math.floor(x)
    y0 = math.floor(y)

    x1 = x0 + 1
    y1 = y0 + 1

    # ② 格子点ごとの勾配ベクトルを取得
    g00 = gradient(x0, y0, seed)
    g10 = gradient(x1, y0, seed)
    g01 = gradient(x0, y1, seed)
    g11 = gradient(x1, y1, seed)

    # ③ 各格子点から(x, y)への距離ベクトル
    dx = x - x0
    dy = y - y0

    # ④ 勾配ベクトルと距離ベクトルの内積
    n00 = g00[0] * dx     + g00[1] * dy
    n10 = g10[0] * (dx-1) + g10[1] * dy
    n01 = g01[0] * dx     + g01[1] * (dy-1)
    n11 = g11[0] * (dx-1) + g11[1] * (dy-1)

    # ⑤ 滑らかにする
    u = fade(dx)
    v = fade(dy)

    # ⑥ x方向に補間
    nx0 = lerp(n00, n10, u)
    nx1 = lerp(n01, n11, u)

    # ⑦ y方向に補間
    value = lerp(nx0, nx1, v)

    return value

def hash2d(x, y, seed):
    h = (x * 374761393 + y * 668265263 + seed * 144665) & 0xFFFFFFFF
    h = ((h ^ (h >> 13)) * 1274126177) & 0xFFFFFFFF
    h = h ^ (h >> 16)
    return h / 0xFFFFFFFF * 2 - 1   # -1〜1