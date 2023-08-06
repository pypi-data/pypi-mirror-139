import requests
import json
import time

a_uuid = '57d6c59e-9048-11ec-930c-ccf9e4df2448'

res = requests.get('http://127.0.0.1:4040/user',
                   params={
                       'fuc': 'Login',
                       'user_key': a_uuid
                   }).text
res = json.loads(res)
assert not res['success']
assert res['err_code'] == 1

res = requests.get('http://127.0.0.1:4040/user',
                   params={
                       'fuc': 'Login',
                       'api_key': '72574895',
                       'user_key': a_uuid
                   }).text
res = json.loads(res)
assert not res['success']
assert res['err_code'] == 1

res = requests.get('http://127.0.0.1:4040/user',
                   params={
                       'api_key': '172574895',
                       'user_key': a_uuid
                   }).text
res = json.loads(res)
assert not res['success']
assert res['err_code'] == 2

res = requests.get('http://127.0.0.1:4040/user',
                   params={
                       'api_key': '172574895',
                       'fuc': 'Login',
                   }).text
res = json.loads(res)
assert not res['success']
assert res['err_code'] == 3

res = requests.get('http://127.0.0.1:4040/user',
                   params={
                       'api_key': '172574895',
                       'fuc': 'Login',
                       'user_key': a_uuid
                   }).text
res = json.loads(res)
assert res['success']
assert res['err_code'] == 0
assert res['res']['is_waitting']
assert res['res']['total'] == 1
assert res['res']['index'] == 0

#######################################################################
#                               client                                #
#######################################################################
res = requests.get('http://127.0.0.1:4040/client',
                   params={
                       'user_key': a_uuid,
                   }).text
res = json.loads(res)
assert not res['success']
assert res['err_code'] == 1

res = requests.get('http://127.0.0.1:4040/client',
                   params={
                       'api_key': '72574895',
                   }).text
res = json.loads(res)
assert not res['success']
assert res['err_code'] == 1

res = requests.get('http://127.0.0.1:4040/client',
                   params={
                       'api_key': '172574895',
                   }).text
res = json.loads(res)
assert not res['success']
assert res['err_code'] == 2

res = requests.get('http://127.0.0.1:4040/client',
                   params={
                       'api_key': '172574895',
                       'fuc': 'HeartBeat',
                   }).text
res = json.loads(res)
assert not res['success']
assert res['err_code'] == 3

temp = {
    "status": "success",
    "country": "韩国",
    "countryCode": "KR",
    "region": "11",
    "regionName": "首尔特别市",
    "city": "首尔特别市",
    "zip": "04524",
    "lat": 37.5794,
    "lon": 126.9754,
    "timezone": "Asia/Seoul",
    "isp": "The Constant Company, LLC",
    "org": "The Constant Company, LLC",
    "as": "AS20473 The Constant Company, LLC",
    "query": "158.247.208.127"
}
temp['api_key'] = '172574895'
temp['fuc'] = 'HeartBeat'
res = requests.get('http://127.0.0.1:4040/client', params=temp).text
res = json.loads(res)
assert res['success']
assert res['err_code'] == 0


def Login(user_key):
    res = requests.get('http://127.0.0.1:4040/user',
                       params={
                           'api_key': '172574895',
                           'fuc': 'Login',
                           'user_key': user_key
                       }).text
    res = json.loads(res)
    return res


res = Login(a_uuid)
print(res)
assert res['success']
assert res['err_code'] == 0
assert 'online_count' in res['res']
assert 'address' in res['res']

i = 0
for item in range(49):
    res = Login(i)
    assert res['success']
    assert res['err_code'] == 0
    assert 'online_count' in res['res']
    i += 1

res = Login(i)
assert res['success']
assert res['err_code'] == 0
res = res['res']
assert res['total'] == 1
assert res['client_count'] == 1
assert res['index'] == 0
assert 'is_waitting' in res

for item in range(10):
    time.sleep(10)
    res = Login(i)

time.sleep(10)
res = Login(i)
assert res['res']['online_count'] == 1
assert 'is_waitting' not in res['res']
