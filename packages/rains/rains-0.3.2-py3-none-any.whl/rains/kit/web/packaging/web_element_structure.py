#!/usr/bin/env python3
# coding=UTF-8
#
# Copyright 2022. quinn.7@foxmail.com All rights reserved.
# Author :: cat7
# Email  :: quinn.7@foxmail.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, 
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================
"""
[ Web元素结构体 ]

"""


# ----------------------------------
class WebElementStructure(object):
    """
    [ Web元素结构体 ]


    """

    page: str
    """ [ 页面名称 ] """

    name: str
    """ [ 组件名称 ] """

    by_key: str
    """ [ 元素定位策略 ] """

    by_value: str
    """ [ 元素定位策略对应的值 ] """

    anchor_by_key: str
    """ [ 锚点元素定位策略 ] """

    anchor_by_value: str
    """ [ 锚点元素定位策略 ] """

    anchor_location_id: int
    """ [ 锚点元素定位ID ] """

    # ------------------------------
    def __init__(
        self, 
        page: str, 
        name: str, 
        by_key: str, 
        by_value: str, 
        anchor_by_key: str = None, 
        anchor_by_value: str = None, 
        anchor_location_id: int = None
    ):
        """
        [ Web元素结构体 ]

        * 构建组件时, 需要传递组件于页面上的定位方式(by_key)与相应的值(by_value).
        * 当传递了非必须的锚点元素时, 表示将在该锚点节点中定位元素.
        * 如果传递锚点元素(anchor), 则必须同时传递 anchor_by_key、anchor_by_value、anchor_location_id.

        ---
        参数:
            page { str } : 页面名称.
            name { str } : 组件名称.
            by_key { str } : 元素定位策略.
            by_value { str } : 元素定位策略对应的值.
            anchor_by_key { str, optional } : 锚点元素定位策略.
            anchor_by_value { str, optional } : 锚点元素定位策略对应的值.
            anchor_location_id { str, optional } : 锚点元素定位ID.

        """

        # 获取元素参数
        self.page = page
        self.name = name
        self.by_key = by_key
        self.by_value = by_value
        self.anchor_by_key = anchor_by_key
        self.anchor_by_value = anchor_by_value
        self.anchor_location_id = anchor_location_id
