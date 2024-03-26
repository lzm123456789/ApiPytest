import pytest
from common.my_assert import Assert

myassert = Assert()


@pytest.mark.smoketest
@pytest.mark.run(order=1)
def test_add_student_api(myrequest, hosts, clean_testdata):
    """添加学生"""

    url = f"{hosts['pc']}/student/add/"
    data = {
        'sno': 95666,
        'name': '陈圆圆',
        'gender': '女',
        'birthday': '2000-11-01',
        'mobile': '18500000001',
        'email': 'test@qq.com',
        'address': '测试',
        'image': None
    }
    resp = myrequest.post_json(url, data, '')
    myassert.assert_code(resp[0])
    myassert.assert_equal(resp[1]['code'], 1)


@pytest.mark.smoketest
@pytest.mark.run(order=2)
def test_update_student_api(myrequest, hosts):
    """修改学生"""

    url = f"{hosts['pc']}/student/update/"
    data = {
        "sno": 95666,
        "name": "陈圆圆",
        "gender": "女",
        "birthday": "2000-11-01",
        "mobile": "18500000001",
        "email": "test@qq.com",
        "address": "测试修改",
        "image": None
    }
    resp = myrequest.post_json(url, data, '')
    myassert.assert_code(resp[0])
    myassert.assert_equal(resp[1]['code'], 1)


@pytest.mark.smoketest
@pytest.mark.run(order=3)
def test_query_student_api(myrequest, hosts):
    """查询学生"""

    url = f"{hosts['pc']}/student/query/"
    data = {"inputstr": '陈圆圆'}
    resp = myrequest.get(url, data, {})
    myassert.assert_code(resp[0])
    myassert.assert_equal(resp[1]['data'][0]['name'], '陈圆圆')


@pytest.mark.smoketest
@pytest.mark.run(order=4)
def test_delete_student_api(myrequest, hosts):
    """删除学生"""

    url = f"{hosts['pc']}/student/delete/"
    data = {"sno": 95666}
    resp = myrequest.post_json(url, data, '')
    myassert.assert_code(resp[0])
    myassert.assert_equal(resp[1]['code'], 1)
