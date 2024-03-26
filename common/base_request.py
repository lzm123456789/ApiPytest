import json
import requests
from log.log import Log as mylog


def get_formatted_json(d):
    """获取格式化的json字符串"""

    return json.dumps(d, indent=4, ensure_ascii=False)


def request_log(func):
    """给请求加日志"""

    def inner(*args, **kwargs):
        url = args[1]
        data = args[2]
        method = 'get' if 'get' in func.__name__ else 'post'
        mylog.info(f'请求地址：{url}')
        mylog.info(f'{method}请求')
        mylog.info(f'请求参数：\n{get_formatted_json(dict(data))}')
        ret = ()
        try:
            ret = func(*args, **kwargs)
            code, data = ret
            resplog = get_formatted_json(data)
            mylog.info(f'返回状态码：{code}')
            mylog.info(f'返回结果：\n{resplog}')
        except Exception as e:
            mylog.error(f'调用接口({url})异常：{e}')
        return ret

    return inner


class BaseRequest:

    @request_log
    def get(self, url, data, cookies):
        """
        需要传cookies的get请求，适用于PC web 前后端不分离的系统架构
        :param url:
        :param data: 请求参数，字典类型
        :param cookies: 接口鉴权相关，字典类型
        :return: (响应状态码,响应的数据)，元组
        """

        resp = requests.get(url=url, cookies=cookies, params=data, verify=False)
        respcode = resp.status_code
        respdata = resp.json()
        return respcode, respdata

    @request_log
    def post(self, url, data, cookies, resp_is_json=1):
        """
        需要传cookies的post请求，适用于PC web 前后端不分离的系统架构，表单提交，这类post请求的请求参数还需csrf
        :param url:
        :param data: 请求参数，字典类型
        :param cookies: 接口鉴权相关，字典类型
        :param resp_is_json: 接口返回数据是否为json格式，默认是 传非1为否
        :return: (响应状态码,响应的数据)，元组
        """

        resp = requests.post(url=url, cookies=cookies, data=data, verify=False)
        respcode = resp.status_code
        respdata = resp.json() if resp_is_json == 1 else '一个html'
        return respcode, respdata

    @request_log
    def app_get(self, url, data, headers):
        """
        需要传headers的get请求，适用于app端
        :param url:
        :param data: 请求参数，字典类型
        :param headers: 接口鉴权相关，字典类型
        :return: (响应状态码,响应的数据)，元组
        """

        resp = requests.get(url=url, headers=headers, params=data, verify=False)
        respcode = resp.status_code
        respdata = resp.json()
        return respcode, respdata

    @request_log
    def app_post(self, url, data, headers):
        """
        需要传headers的post请求，适用于app端，json提交
        :param url: 请求地址
        :param data: 请求参数，字典类型
        :param headers: 接口鉴权相关，字典类型
        :return: (响应状态码,响应的数据)，元组
        """

        resp = requests.post(url=url, headers=headers, json=data, verify=False)
        respcode = resp.status_code
        respdata = resp.json()
        return respcode, respdata

    @request_log
    def get_fbspilit(self, url, data, token):
        """
        需要传access_token的get请求，适用于PC web前后端分离的系统架构
        :param url:
        :param data: 请求参数，字典类型
        :param token: 接口鉴权相关，字典类型
        :return: (响应状态码,响应的数据)，元组
        """

        data.update({'access_token': token})
        resp = requests.get(url=url, headers={'xxx': 'xxx'}, params=data, verify=False)
        respcode = resp.status_code
        respdata = resp.json()
        return respcode, respdata

    @request_log
    def post_json(self, url, data, token):
        """
        需要传access_token的post请求，适用于PC web前后端分离的系统架构，json提交
        :param url:
        :param data: 请求参数，字典类型
        :param token: 接口鉴权相关，字典类型
        :return: (响应状态码,响应的数据)，元组
        """

        resp = requests.post(url=f'{url}?token= {token}', headers={'xxx': 'xxx'}, json=data, verify=False)
        respcode = resp.status_code
        respdata = resp.json()
        return respcode, respdata
