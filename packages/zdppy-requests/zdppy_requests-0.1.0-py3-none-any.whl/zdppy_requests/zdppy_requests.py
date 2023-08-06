#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/2/22 15:17
# @Author  : 张大鹏
# @Site    : 
# @File    : zdppy_requests.py
# @Software: PyCharm
from typing import Dict
import requests
from zdppy_log import Log
from .exceptions import StatusCodeError, ParamError


class Requests:
    def __init__(self,
                 *,
                 host: str = "127.0.0.1",
                 port: int = 8888,
                 root_path: str = "",
                 prefix: str = "http",
                 log_file_path: str = "logs/zdppy/zdppy_requests.log",
                 debug: bool = False):
        self.host = host
        self.port = port
        self.root_path = root_path
        self.prefix = prefix
        self.url = f"{prefix}://{host}:{port}/{root_path}"
        if self.url.endswith("/"):  # 去除尾部空格
            self.url = self.url[:-1]

        # 初始化日志
        self.log_file_path = log_file_path
        self.debug = debug
        self.log = Log(log_file_path=log_file_path, debug=debug)

    def add(self, table: str, data: Dict, status_code: int = 200):
        """
        添加数据
        :return:
        """
        url = f"{self.url}/{table}"
        response = requests.post(url, json=data)

        # 校验状态码
        if response.status_code != status_code:
            raise StatusCodeError(f"期望状态码={status_code} 实际状态码={response.status_code}")

        # 返回数据
        return response.json()

    def find_by_page(self, table: str, offset: int = 0, size: int = 100, status_code: int = 200):
        """
        根据分页查询数据
        :return:
        """
        url = f"{self.url}/{table}"
        response = requests.get(url, data={"offset": offset, "size": size})

        # 校验状态码
        if response.status_code != status_code:
            raise StatusCodeError(f"期望状态码={status_code} 实际状态码={response.status_code}")

        # 返回数据
        return response.json()

    def find_by_id(self, table: str, id: int = 1, status_code: int = 200):
        """
        根据ID查询数据
        :return:
        """
        url = f"{self.url}/{table}/{id}"
        response = requests.get(url)

        # 校验状态码
        if response.status_code != status_code:
            raise StatusCodeError(f"期望状态码={status_code} 实际状态码={response.status_code}")

        # 返回数据
        return response.json()

    def delete_by_id(self, table: str, id: int = 1, status_code: int = 200):
        """
        根据ID查询数据
        :return:
        """
        url = f"{self.url}/{table}/{id}"
        response = requests.delete(url)

        # 校验状态码
        if response.status_code != status_code:
            raise StatusCodeError(f"期望状态码={status_code} 实际状态码={response.status_code}")

        # 返回数据
        return response.json()

    def update_by_id(self, table: str, id: int = 1, data: Dict = None, status_code: int = 200):
        """
        根据ID更新数据
        :return:
        """
        # 校验参数
        if data is None:
            raise ParamError(f"要更新的数据不能为空：data = {data}")

        # 准备url
        url = f"{self.url}/{table}/{id}"
        response = requests.patch(url, json=data)

        # 校验状态码
        if response.status_code != status_code:
            raise StatusCodeError(f"期望状态码={status_code} 实际状态码={response.status_code}")

        # 返回数据
        return response.json()
