import os
import sys

sys.path.append(os.path.split(os.path.abspath(os.path.dirname(__file__)))[0])
from log.log import Log
from config.config import Config
from common.utils import update_file, email_testreport

mylog = Log
myconfig1 = Config()

yamlname = sys.argv[1]

if myconfig1.is_option_exist('temp', 'testresult'):
    myconfig1.remove_option('temp', 'testresult')
update_file('testcase/testcases_template.py', 'TEMPLATE', yamlname)
os.system('pytest testcase/testcases_template.py')
update_file('testcase/testcases_template.py', yamlname, 'TEMPLATE')

# 重新实例化配置对象，获取最新的测试结果；否则上面的配置对象已经删除了测试结果，获取为空
myconfig2 = Config()
testresult = myconfig2.get_conf('temp', 'testresult')
receiver = myconfig2.get_conf('email', 'receiver')
# 测试不通过，才发邮件
if testresult == 'failed':
    mylog.warning("测试不通过，详情查看测试报告")
    # email_testreport(receiver=receiver, email_subject="接口层自动化测试报告")

"""
执行命令：
python3 testsuite/test_by_single_yaml.py student.yaml
"""
