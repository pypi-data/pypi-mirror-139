#!/usr/bin/env python3
# coding=UTF-8

from rains.kit.api.api_task import ApiTask


class Task(ApiTask):
    """
    [ Task ]

    """

    # ------------------------------
    def set_task_init(self):
        """
        [ 设置任务初始化 ]

        * 该接口将在 [ 任务 ] 开始时执行, 全程只会执行一次.

        """
        ...

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
        ...
        