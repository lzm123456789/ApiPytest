import os
import sys

sys.path.append(os.path.split(os.path.abspath(os.path.dirname(__file__)))[0])
from log.log import MyLog
from datetime import datetime
from config.config import MyConfig
from common.utils import email_testreport, wechat_send_testreport

mylog = MyLog
myconfig1 = MyConfig()

mylog.info("""
xx业务的核心接口：
添加学生
修改学生
查询学生
删除学生
""")
if myconfig1.is_option_exist('temp', 'testresult'):
    myconfig1.remove_option('temp', 'testresult')

# 每周五上午执行，报告上需输出日志，其他时间执行不需要
dayOfWeek = datetime.now().weekday()
nowHour = datetime.now().strftime('%H')
if dayOfWeek == 4 and nowHour == '08':
    os.system('pytest -m smoketest --reruns=3 --capture=sys')
else:
    os.system('pytest -m "alltest or yamltest" --reruns=3')

# 重新实例化配置对象，获取最新的测试结果；否则上面的配置对象已经删除了测试结果，获取为空
myconfig2 = MyConfig()
testresult = myconfig2.get_conf('temp', 'testresult')
receiver = myconfig2.get_conf('email', 'receiver')
# 测试不通过，才发邮件
if testresult == 'failed':
    mylog.warning("测试不通过，详情查看测试报告")
    email_testreport(receiver=receiver, email_subject="xx业务流程回归测试")

# 获取测试结果详情
total = myconfig2.get_conf('temp', 'total')
passed = myconfig2.get_conf('temp', 'passed')
failed = myconfig2.get_conf('temp', 'failed')
error = myconfig2.get_conf('temp', 'error')
skipped = myconfig2.get_conf('temp', 'skipped')
successful = myconfig2.get_conf('temp', 'successful')

# 每周五上午执行，通过企业微信发送测试报告
if dayOfWeek == 4 and nowHour == '08':
    wechat_send_testreport(key='xxx',  # 企业微信群机器人的key
                           projectname="每周五xxx业务流程接口层回归测试",
                           total=total,
                           passrate=successful,
                           success=passed,
                           fail=failed,
                           skip=skipped,
                           error=error)
