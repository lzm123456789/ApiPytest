import os
import sys

sys.path.append(os.path.split(os.path.abspath(os.path.dirname(__file__)))[0])
from config.config import Config
from common.utils import email_testreport, create_yamltest

myconfig = Config()
receiver = myconfig.get_conf('email', 'receiver')

# 根据yaml测试用例文件名生成可执行的py文件
yamls = []
currpath = os.path.dirname(os.path.realpath(__file__))
yamlpath = os.path.join(os.path.dirname(currpath), 'data')
files = os.listdir(yamlpath)
for file in files:
    if os.path.splitext(file)[1] == '.yaml' and file not in ['template.yaml']:
        yamls.append(file)
for yaml in yamls:
    create_yamltest(yaml)

os.system("pytest")
email_testreport(receiver=receiver, email_subject="全量接口层自动化测试")  # 调试的时候，注释这一行，避免发邮件
# 执行完之后，删除按yaml生成的py文件
for yaml in yamls:
    filename = 'test_' + os.path.splitext(yaml)[0] + '.py'
    filepath = os.path.join(os.path.dirname(currpath), 'testcase', filename)
    os.remove(filepath)
