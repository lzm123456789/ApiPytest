# coding=utf-8
"""
封装requests
"""
import json
import requests
from log.log import MyLog as log


def json_formatted_output(dic):
    """json字符串格式化输出"""

    j = json.dumps(dic, indent=4, ensure_ascii=False)
    return j


class MyRequest:

    def get(self, url, cookies, data):
        """
        get请求
        :param url: 请求地址
        :param cookies: 接口鉴权
        :param data: 请求参数
        :return: 元组 （响应状态码,响应的数据）
        """

        res = ()
        try:
            log.info(f'请求地址：{url}')
            log.info('GET请求')
            log.info(f'请求参数：\n{json_formatted_output(dict(data))}')
            restem = requests.get(url=url, cookies=cookies, params=data, verify=False)
            rescode = restem.status_code
            resdict = restem.json()
            reslog = json_formatted_output(resdict)
            log.info(f'返回的状态码：{rescode}')
            log.info(f'返回结果：\n{reslog}')
            res = rescode, resdict
        except Exception as e:
            log.error(f'调用GET接口({url})异常：{e}')
        return res

    def post(self, url, cookies, data, resjson=1):
        """
        前后端不分离的post请求
        :param url: 请求地址
        :param cookies: 接口鉴权
        :param data: 请求参数
        :param resjson: 接口返回数据是否为json格式，默认是 传0为否
        :return: 元组 （响应状态码,响应的数据）
        """

        res = ()
        try:
            log.info(f'请求地址：{url}')
            log.info('POST请求')
            log.info(f'请求参数：\n{json_formatted_output(dict(data))}')
            restem = requests.post(url=url, cookies=cookies, data=data, verify=False)
            rescode = restem.status_code
            log.info(f'响应的状态码：{restem.status_code}')
            if resjson:
                resdict = restem.json()
                reslog = json_formatted_output(resdict)
                log.info(f'响应结果：\n{reslog}')
            else:
                resdict = None
                log.info("接口响应为渲染的页面")
            res = rescode, resdict
        except Exception as e:
            log.error(f'调用POST接口({url})异常：{e}')
        return res

    def app_get(self, url, headers, data):
        """
        app端get请求
        :param url: 请求地址
        :param headers: 接口鉴权
        :param data: 请求参数，字典类型
        :return: 元组 （响应状态码,响应的数据）
        """

        res = ()
        try:
            log.info(f'请求地址：{url}')
            log.info('GET请求')
            log.info(f'请求参数：\n{json_formatted_output(dict(data))}')
            restem = requests.get(url=url, headers=headers, params=data, verify=False)
            rescode = restem.status_code
            resdict = restem.json()
            reslog = json_formatted_output(resdict)
            log.info(f'响应的状态码：{rescode}')
            log.info(f'响应结果：\n{reslog}')
            res = rescode, resdict
        except Exception as e:
            log.error(f'调用接口({url})异常：{e}')
        return res

    def app_post(self, url, headers, data):
        """
        app端post请求，json提交
        :param url: 请求地址
        :param headers: 接口鉴权
        :param data: 请求参数，字典类型
        :return: 元组 （响应状态码,响应的数据）
        """

        res = ()
        try:
            log.info(f'请求地址：{url}')
            log.info('POST请求')
            log.info(f'请求参数：\n{json_formatted_output(dict(data))}')
            restem = requests.post(url=url, headers=headers, json=data, verify=False)
            rescode = restem.status_code
            resdict = restem.json()
            reslog = json_formatted_output(resdict)
            log.info(f'响应的状态码：{rescode}')
            log.info(f'响应结果：\n{reslog}')
            res = rescode, resdict
        except Exception as e:
            log.error(f'调用接口({url})异常：{e}')
        return res

    def get_fbspilit(self, url, access_token, data):
        """
        pc前后端分离的get请求
        :param url: 请求地址
        :param access_token: 接口鉴权
        :param data: 请求参数，字典类型
        :return: 元组 （响应状态码,响应的数据）
        """

        res = ()
        try:
            log.info(f'请求地址：{url}')
            log.info('GET请求')
            log.info(f'请求参数：\n{json_formatted_output(dict(data))}')
            data.update({'access_token': access_token})
            restem = requests.get(url=url, headers={'xxx': 'xxx'}, params=data, verify=False)
            rescode = restem.status_code
            resdict = restem.json()
            reslog = json_formatted_output(resdict)
            log.info(f'响应的状态码：{rescode}')
            log.info(f'响应结果：\n{reslog}')
            res = rescode, resdict
        except Exception as e:
            log.error(f'调用接口({url})异常：{e}')
        return res

    def post_json(self, url, access_token, data):
        """
        pc前后端分离的post请求
        :param url: 请求地址
        :param access_token: 接口鉴权
        :param data: 请求参数，字典类型
        :return: 元组 （响应状态码,响应的数据）
        """

        res = ()
        try:
            log.info(f'请求地址：{url}')
            log.info('POST请求')
            log.info(f'请求参数：\n{json_formatted_output(dict(data))}')
            restem = requests.post(url=f'{url}?access_token= {access_token}', headers={'xxx': 'xxx'}, json=data,
                                   verify=False)
            rescode = restem.status_code
            resdict = restem.json()
            reslog = json_formatted_output(resdict)
            log.info(f'响应的状态码：{rescode}')
            log.info(f'响应结果：\n{reslog}')
            res = rescode, resdict
        except Exception as e:
            log.error(f'调用接口({url})异常：{e}')
        return res
