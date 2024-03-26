from log.log import Log as mylog


class Assert:

    def assert_code(self, actual_code, expect_code=200):
        """
        判断响应状态码是否符合预期
        :param actual_code: 实际的响应状态码
        :param expect_code: 预期的响应状态码, 默认为200
        :return: True或者抛异常
        """

        try:
            assert actual_code == expect_code
            return True
        except:
            mylog.error(f"响应状态码不符合预期, 实际的状态码是{actual_code}, 预期的状态码是{expect_code}\n")
            raise

    def assert_equal(self, actual_value, expect_value):
        """
        判断实际结果是否符合预期
        :param actual_value: 实际结果
        :param expect_value: 预期结果
        :return: True或者抛异常
        """

        try:
            assert actual_value == expect_value
            mylog.info(f"实际结果符合预期\n")
            return True
        except:
            mylog.error(f"实际结果不符合预期, 实际结果是{actual_value}, 预期结果是{expect_value}\n")
            raise
