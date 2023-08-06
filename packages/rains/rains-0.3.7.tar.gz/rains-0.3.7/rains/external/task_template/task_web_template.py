#!/usr/bin/env python3
# coding=UTF-8

from rains.kit.web.web_task import WebTask
from rains.kit.web.web_plant import BY


class Task(WebTask):
    """
    [ Task ]

    """

    # ------------------------------
    def set_task_init(self):
        """
        [ 设置任务初始化 ]

        * 该接口将在 [ 任务 ] 开始时执行, 全程只会执行一次.

        """

        # 在这里实例化元素对象

        # 百度搜索框元素定位
        self.search_input = self.plant.element(
            page='百度',
            name='搜索框',
            by_key=BY.ID,
            by_value='kw'
        )

        # 百度百度一下元素定位
        self.ok_button = self.plant.element(
            page='百度',
            name='百度一下',
            by_key=BY.ID,
            by_value='su'
        )

    # ------------------------------
    def set_task_quit(self):
        """
        [ 设置任务注销 ]

        * 该接口将在 [ 任务 ] 结束后执行, 全程只会执行一次.

        """
        ...

    # ------------------------------
    def set_case_init(self):
        """
        [ 设置用例初始化 ]

        * 该接口将在每次 [ 用例 ] 开始时执行.

        """
        ...

    # ------------------------------
    def set_case_quit(self):
        """
        [ 设置用例注销 ]

        * 该接口将在每次 [ 用例 ] 结束后执行.

        """
        ...

    # ------------------------------
    def case_1(self):
        """
        [ 用例1 ]

        """

        # 页面访问URL
        self.plant.view.page.goto('http://www.baidu.com/')

        # 百度搜索框输入内容
        self.search_input.input.send('rains')

        # 点击百度一下
        self.ok_button.mouse.tap()
