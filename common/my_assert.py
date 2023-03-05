# coding=utf-8
from log.log import MyLog as log


class Assert:

    def assert_code(self, actual_code, expect_code=200):
        """
        断言请求接口返回的状态码是否符合预期
        :param actual_code: 请求接口返回的状态码
        :param expect_code: 预期返回的状态码
        :return: 测试通过或者抛异常测试不通过
        """

        try:
            assert actual_code == expect_code
            return True
        except:
            log.error(f"响应的状态码错误, 实际的状态码是{actual_code}, 预期的状态码是{expect_code}")
            raise

    def assert_equal(self, actual_value, expect_value):
        """
        断言实际得到的值是否符合预期
        :param actual_value:自动化测试最后得到的实际值
        :param expect_value:预期值
        :return:测试通过或者抛异常测试不通过
        """

        try:
            assert actual_value == expect_value
            return True
        except:
            log.error(f"接口返回的数据不符合预期, 实际的数据是{actual_value}, 预期是{expect_value}")
            raise
