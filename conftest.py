import pytest
from py._xmlgen import html
from datetime import datetime
from config import config as myconfig
from common.base_request import BaseRequest

conf = myconfig.Config()


@pytest.fixture(scope='session')
def myrequest():
    """实例化请求对象"""

    return BaseRequest()


@pytest.fixture(scope='session')
def hosts():
    """获取系统的所有host"""

    return conf.get_section_dict('host')


@pytest.fixture(scope='session')
def testdatas():
    """获取固定的测试数据"""

    return conf.get_section_dict('data')


@pytest.fixture(scope='function')
def temp():
    """获取临时变量（文件传参）"""

    # 重新实例化配置对象，保证能读取到最新的值
    conf = myconfig.Config()
    return conf.get_section_dict('temp')


@pytest.fixture(scope='function')
def newconfig():
    """
    重新实例化配置对象，用于修改配置文件
    """

    conf = myconfig.Config()
    return conf


def pytest_collection_modifyitems(items):
    """
    测试用例收集完成时，将收集到的item的name和nodeid的中文显示在控制台上
    :return:
    """
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode_escape")
        item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")


# 修改报告标题
@pytest.mark.optionalhook
def pytest_html_report_title(report):
    report.title = "接口层自动化测试报告"


# 添加接口地址与项目名称
def pytest_configure(config):
    config._metadata["项目名称"] = "xxx"
    config._metadata['接口地址'] = 'https://test.xxx.com'
    config._metadata['开始时间'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # 删除无需展示的信息
    config._metadata.pop("Packages")
    config._metadata.pop("Platform")
    config._metadata.pop("Plugins")
    config._metadata.pop("Python")


# 修改Summary
@pytest.mark.optionalhook
def pytest_html_results_summary(prefix):
    prefix.extend([html.p("所属业务线: xxx")])
    prefix.extend([html.p("测试人员: xxx")])


# 添加用例描述
@pytest.mark.optionalhook
def pytest_html_results_table_header(cells):
    cells.insert(2, html.th('Description'))
    # cells.insert(3, html.th('StartTime', class_='sortable time', col='time'))
    cells.pop()


@pytest.mark.optionalhook
def pytest_html_results_table_row(report, cells):
    cells.insert(2, html.td(report.description))
    # cells.insert(3, html.td(datetime.utcnow(), class_='col-time'))
    cells.pop()


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    report.description = str(item.function.__doc__)
    report.nodeid = report.nodeid.encode("utf-8").decode("unicode_escape")  # 设置编码显示中文


# 自定义命令行参数
def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="test", help="env：表示被测试的环境，默认测试环境")


@pytest.fixture(scope='session')
def env(pytestconfig):
    return pytestconfig.getoption('--env')


# 收集测试结果
def pytest_terminal_summary(terminalreporter):
    conf = myconfig.Config()
    passed = len([i for i in terminalreporter.stats.get('passed', []) if i.when != 'teardown'])
    failed = len([i for i in terminalreporter.stats.get('failed', []) if i.when != 'teardown'])
    error = len([i for i in terminalreporter.stats.get('error', []) if i.when != 'teardown'])
    skipped = len([i for i in terminalreporter.stats.get('skipped', []) if i.when != 'teardown'])
    total = passed + failed + error + skipped
    passrate = passed / (passed + failed + error) * 100
    conf.set_conf('temp', 'total', total)
    conf.set_conf('temp', 'passed', passed)
    conf.set_conf('temp', 'failed', failed)
    conf.set_conf('temp', 'error', error)
    conf.set_conf('temp', 'skipped', skipped)
    conf.set_conf('temp', 'passrate', '%.2f%%' % passrate)
    if failed + error == 0:
        conf.set_conf('temp', 'testresult', 'success')
    else:
        conf.set_conf('temp', 'testresult', 'failed')


# 全局清理数据
@pytest.fixture(scope='session')
def clean_testdata():
    pass
