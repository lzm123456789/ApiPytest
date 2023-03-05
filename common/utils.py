import os
import sys
import yaml
import smtplib
import requests
from log.log import MyLog as log
from config.config import MyConfig
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

conf = MyConfig()
email_server = conf.get_conf('email', 'email_server')
username = conf.get_conf('email', 'username')
password = conf.get_conf('email', 'password')
sender = conf.get_conf('email', 'sender')
receiver = conf.get_conf('email', 'receiver')

currpath = os.path.dirname(os.path.realpath(__file__))
rootpath = os.path.dirname(currpath)
reportpath = os.path.join(rootpath, 'report', 'report.html')
yamltestpath = os.path.join(rootpath, 'testcase', 'testcases_template.py')


def get_yaml(yaml_file):
    """
    获取yaml文件上的数据
    :param yaml_file: yaml文件的路径
    :return: 按框架上yaml编写测试用例的规范，结果为列表里嵌套字典
    """

    ld = {}
    try:
        with open(yaml_file, "r", encoding="utf-8") as yo:
            f = yo.read()
            ld = yaml.load(f)
    except Exception as e:
        log.error(f'获取yaml文件数据失败，具体原因：{e}')
    return ld


def update_file(filepath, oldstr, newstr):
    """
    修改文件
    :param filepath: 文件路径
    :param oldstr: 旧字符串
    :param newstr: 新字符串
    :return:
    """

    try:
        file_data = ""
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                if oldstr in line:
                    line = line.replace(oldstr, newstr)
                file_data += line
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(file_data)
    except Exception as e:
        log.error(f'修改文件失败，具体原因：{e}')


def create_yamltest(yamlname):
    """
    :param yamlname: 编写用例的yaml文件名
    :return:
    """

    try:
        file_data = ""
        with open(yamltestpath, "r", encoding="utf-8") as f:
            for line in f:
                if 'TEMPLATE' in line:
                    line = line.replace('TEMPLATE', yamlname)
                file_data += line
        filename = os.path.join(rootpath, 'testcase', f"test_{yamlname.split('.')[0]}.py")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(file_data)
    except Exception as e:
        log.error(f'创建基于yaml执行的测试用例失败，具体原因：{e}')


def email_testreport(reportpath=reportpath,
                     email_server=email_server,
                     username=username,
                     password=password,
                     email_subject="接口层自动化测试报告",
                     sender=sender,
                     receiver=receiver):
    """
    邮件发送测试报告
    :param reportpath:
    :param email_server:
    :param username:
    :param password:
    :param email_subject:
    :param sender:
    :param receiver: 多个收件人需用空格隔开
    :return:
    """

    try:
        # 读取测试报告内容
        with open(reportpath, 'rb') as file_html:
            content = file_html.read()

        # 实例化带附件的MIMEMultipart对象
        mail = MIMEMultipart()
        #  定义邮件主题
        mail['Subject'] = Header(email_subject, 'utf-8')
        #  定义邮件发送人
        mail['From'] = sender
        #  定义邮件接收人
        mail['To'] = ','.join(receiver.split(' '))

        # 构造邮件的正文
        mail_text = MIMEText(content, 'html', 'utf-8')
        # 将邮件的正文添加到MIMEMultipart对象中
        mail.attach(mail_text)

        # 构造邮件的附件
        mail_file = MIMEText(content, 'html', 'utf-8')
        mail_file['Content-Type'] = 'application/octet-stream'
        mail_file["Content-Disposition"] = 'attachment; filename="TestReport.html"'
        # 将邮件的附件添加到MIMEMultipart对象中
        mail.attach(mail_file)

        # 实例化SMTP对象 连接SMTP主机
        smtp = smtplib.SMTP_SSL(email_server, 465)
        # smtp = smtplib.SMTP()
        # smtp.connect(self.email_server)
        # 输出发送邮件详细过程
        # smtp.set_debuglevel(1)
        # 邮件登录
        smtp.login(username, password)
        # 邮件发送
        smtp.sendmail(mail['From'], receiver.split(' '), mail.as_string())
        # 断开SMTP连接
        smtp.quit()
        log.info("邮件发送测试报告成功～")
    except Exception as e:
        log.error(f"邮件发送测试报告失败，具体原因: {e}")


def wechat_send_testreport(key, projectname, total, passrate, success, fail, skip, error, reportpath=reportpath):
    """
    企业微信发送测试报告
    :param key: 企业微信群机器人对应的key
    :param projectname: 测试的项目名称
    :param total: 测试用例总数
    :param passrate: 通过率
    :param success: 成功数
    :param fail: 失败数
    :param skip: 跳过数
    :param error: 错误数
    :param reportpath: 测试报告地址
    :return:
    """

    wechaturl = 'https://qyapi.weixin.qq.com/cgi-bin/webhook'
    uploadurl = f'{wechaturl}/upload_media?key={key}&type=file'
    sendurl = f'{wechaturl}/send?key={key}'
    data1 = {
        "msgtype": "markdown",  # 消息类型，此时固定为markdown
        "markdown": {
            "content": "# **提醒！自动化测试反馈**\n#### **请相关同事注意，及时跟进！**\n"
                       "> 项目名称：<font color=\"info\">%s</font> \n"
                       # "> 项目指定端：<font color=\"info\">%s</font> \n"
                       "> 测试用例总数：<font color=\"info\">%s条</font>；通过率：<font color=\"info\">%s</font>\n"
                       "> **--------------------运行详情--------------------**\n"
                       "> **成功数：**<font color=\"info\">%s</font>\n**失败数：**<font color=\"warning\">%s</font>\n"
                       "> **跳过数：**<font color=\"info\">%s</font>\n**错误数：**<font color=\"comment\">%s</font>\n"
                       "> ##### **测试报告详情，请打开下面附件查看(手机端需用手机浏览器打开)：**" % (
                           projectname, total, passrate, success, fail, skip, error),
            # 加粗：**需要加粗的字**
            # 引用：> 需要引用的文字
            # 字体颜色(只支持3种内置颜色)
            # 标题 （支持1至6级标题，注意#与文字中间要有空格）
            # 绿色：info、灰色：comment、橙红：warning
            # "mentioned_list": ["wangqing", "@all"],
            "mentioned_mobile_list": ["@all"]
        }
    }
    try:
        # 发送测试概况
        resp = requests.post(url=sendurl, json=data1, verify=False)
        if resp.json()['errcode'] != 0:
            log.error(f"发送测试概况失败，具体原因：{resp.json()['errmsg']}")
            sys.exit(0)
        # 上传测试报告附件
        filedata = {'media': open(reportpath, 'rb')}
        resp = requests.post(url=uploadurl, files=filedata, verify=False)
        if resp.json()['errcode'] != 0:
            log.error(f"上传测试报告附件失败，具体原因：{resp.json()['errmsg']}")
            sys.exit(0)
        media_id = resp.json()['media_id']
        data2 = {
            "msgtype": "file",
            "file": {"media_id": media_id}
        }
        # 发送测试报告附件
        resp = requests.post(url=sendurl, json=data2, verify=False)
        if resp.json()['errcode'] != 0:
            log.error(f"发送测试报告附件失败，具体原因：{resp.json()['errmsg']}")
    except Exception as e:
        log.error(f"企业微信发送测试报告失败，具体原因: {e}")


if __name__ == '__main__':
    # email_testreport()
    create_yamltest('contract.yaml')
