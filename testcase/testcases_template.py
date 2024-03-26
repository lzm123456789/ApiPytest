import re
import json
import pytest
import jsonpath
from config.config import Config
from common.utils import get_yaml
from common.my_assert import Assert
from common.common_xx import CommomForXX

conf = Config()
myassert = Assert()
xx = CommomForXX()

yamlname = 'TEMPLATE'

yamlpath = 'data/' + yamlname
yamldatas = get_yaml(yamlpath)
currhost = yamldatas[0]['basedatas']['host']
tokenname = yamldatas[0]['basedatas']['token']
tempvars = yamldatas[0]['basedatas']['tempvars']
testcases = yamldatas[1:]
casemarks = [i['path'] for i in testcases]


@pytest.fixture(scope='module')
def usera():
    """PC端 用户usera的token"""

    token = xx.get_pc_token()
    return token


# 按yaml上设置的业务流程执行测试（套用pytest的测试用例参数化执行）
@pytest.mark.yamltest
@pytest.mark.parametrize('testcase', testcases, ids=casemarks)
def test_yaml_xx_api(testcase, myrequest, hosts, usera):
    # 修改测试用例描述
    test_yaml_xx_api.__doc__ = testcase['testcasename']

    # 根据yaml上标记hostname匹配配置文件里的host
    host = dict(locals()['hosts']).get(currhost)

    path = jsonpath.jsonpath(testcase, '$..path')[0]
    url = host + path

    # 执行测试用例前置的sql
    setupsql = jsonpath.jsonpath(testcase, '$..setupsql')
    if setupsql:
        setupsql = setupsql[0]
        r = setupsql.get('r', None)
        cud = setupsql.get('cud', None)
        if r:
            dbname = r['db']
            currdb = locals().get(dbname)
            temp = currdb.mysql_r(sql=r['sql'], is_dict=1)
            key = list(temp.keys())[0]
            value = list(temp.values())[0]
            ## 将查询的值赋给临时变量
            tempvars[key] = value
            # with open(yamlpath, 'w', encoding='utf-8') as f:
            #     yaml.dump(yamldatas, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
        if cud:
            dbname = cud['db']
            currdb = locals().get(dbname)
            currdb.mysql_cud(sql=cud['sql'])

    method = jsonpath.jsonpath(testcase, '$..method')[0]
    data = jsonpath.jsonpath(testcase, '$..data')[0]
    datajson = json.dumps(data)

    # 根据&&标识符找到yaml上定义的全局变量，然后用变量名到配置文件里面取值，然后替换全局变量标识符
    gvars = re.findall(r'"&&(.*?)"', datajson)
    if gvars:
        globvars = conf.get_section_dict('data')
        for i in gvars:
            gvalue = globvars[i]
            datajson = datajson.replace('&&' + i, gvalue)

    # 根据@@标识符找到yaml上定义的临时变量，匹配上方定义的临时变量名，然后替换临时变量标识符
    tvars = re.findall(r'"@@(.*?)"', datajson)
    if tvars:
        for i in tvars:
            tvalue = tempvars[i]
            datajson = datajson.replace('@@' + i, tvalue)

    data = json.loads(datajson)
    token = locals().get(tokenname)
    if method == 'post_json':
        resp = myrequest.post_json(url, token, data)
    if method == 'get':
        resp = myrequest.get(url, {}, data)
    checkkey = jsonpath.jsonpath(testcase, '$..key')[0]
    checkvalue = jsonpath.jsonpath(testcase, '$..value')[0]
    myassert.assert_code(resp[0])
    myassert.assert_equal(jsonpath.jsonpath(resp[1], f'$..{checkkey}')[0], checkvalue)

    # 保存接口返回的数据，给其他接口用
    savevar = jsonpath.jsonpath(testcase, '$..savevar')
    if savevar:
        savevar = savevar[0]
        key = list(savevar.keys())[0]
        keytemp = list(savevar.values())[0]
        value = jsonpath.jsonpath(resp[1], f'$..{keytemp}')[0]
        tempvars[key] = value
        # with open(yamlpath, 'w', encoding='utf-8') as f:
        #     yaml.dump(yamldatas, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

    # 执行测试用例后置的sql
    teardownsql = jsonpath.jsonpath(testcase, '$..teardownsql')
    if teardownsql:
        teardownsql = teardownsql[0]
        dbname = teardownsql.get('db', None)
        sql = teardownsql.get('sql', None)
        currdb = locals().get(dbname)
        currdb.mysql_cud(sql)


"""
执行命令：
python3 testsuite/test_by_single_yaml.py TEMPLATE

#TODO
如果yaml编写的测试用例需要按标记和顺序执行的话，
可以通过在yaml--basedatas增加参数mark和order、testcases_template读取、create_yamltest替换"order(run=xx)"和"mark.xx"实现
"""
