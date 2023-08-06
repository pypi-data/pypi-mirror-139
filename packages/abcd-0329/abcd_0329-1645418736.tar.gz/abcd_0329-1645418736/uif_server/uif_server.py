import time
import threading
import subprocess
import queue
import json
import os

import requests
from aiohttp import web
import caddy_runtime

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
BASE_DIR = BASE_DIR.replace('\\', '/')


def DoCMD(cmd, is_wait=True, cwd=None):
    print('\n\n==', cmd, '\n')
    if is_wait:
        subprocess.Popen(cmd, shell=True, cwd=cwd).wait()
    else:
        subprocess.Popen(cmd, shell=True, cwd=cwd)


# {{{ cloudflare
BASE_URL = 'https://api.cloudflare.com/client/v4/zones'
USER_KEY = '355b5a34004ad824d3b8101326f4b68586a6c'
USER_EMAIL = 'jimmyhuang454@gmail.com'


def Req(url, params, type='get'):
    head = {
        'Content-Type': 'application/json',
        'X-Auth-Email': USER_EMAIL,
        'X-Auth-Key': USER_KEY
    }
    if type == 'get':
        res = requests.get(url, headers=head, params=params)
    elif type == 'post':
        res = requests.post(url, headers=head, json=params)
    elif type == 'put':
        res = requests.put(url, headers=head, json=params)
    else:
        res = requests.delete(url, headers=head, data=params)

    return res


class Domain(object):
    def __init__(self, domain, zone_id):
        self.local_dns = {}
        self.using_path = {}
        self.using_count = 0
        self.ChangeDomain(domain, zone_id)

    def _handle_path(self, path):
        res = "%s.%s" % (path, self.domain)
        return res

    def ChangeDomain(self, domain, zone_id):
        self.domain = domain
        self.zone_id = zone_id
        for item in self.using_path:
            self.using_path[item] = False

    def DispachPath(self):
        for item in self.using_path:
            if self.using_path[item]:
                continue
            self.using_path[item] = True
            return item

        while True:
            self.using_count += 1
            res = "uif_%s" % str(self.using_count)
            if res in self.using_path and self.using_path[res]:
                continue
            break
        self.using_path[res] = True
        return res

    def FreePath(self, path):
        self.using_path[path] = False

    def ReqZone(self, url_path, params={}, type='get'):
        res = Req('%s/%s/%s' % (BASE_URL, self.GetZoneID(), url_path),
                  params,
                  type=type)
        res = json.loads(res.text)
        return res

    def GetZoneID(self):
        return self.zone_id

    def GetDNSRecordList(self):
        return self.ReqZone('dns_records')

    def CreateDNSRecord(self,
                        path,
                        content,
                        type="A",
                        ttl=1,
                        proxied=True,
                        priority=10):
        path = self._handle_path(path)
        self.local_dns[path] = content
        return self.ReqZone('dns_records',
                            params={
                                'name': path,
                                'content': content,
                                'ttl': ttl,
                                'proxied': proxied,
                                'priority': priority,
                                'type': type
                            },
                            type='post')

    def UpdateDNSRecord(self,
                        record_id,
                        path,
                        content,
                        type="A",
                        ttl=1,
                        proxied=True):
        path = self._handle_path(path)
        self.local_dns[path] = content
        return self.ReqZone('dns_records/%s' % record_id,
                            params={
                                'name': path,
                                'content': content,
                                'ttl': ttl,
                                'proxied': proxied,
                                'type': type
                            },
                            type='put')

    def DeleteDNSRecord(self, record_id):
        return self.ReqZone('dns_records/%s' % (record_id), type='delete')

    def GetDNSItem(self, path):
        res = self.GetDNSRecordList()
        name = self._handle_path(path)
        for item in res['result']:
            if item['name'] == name:
                return item
        return {}


# }}}

SERVER_API_KEY = '172574895'
SERVER_PORT = 4040
OCUPATION_TIME = 30 * 60  # 30 minutes
HEART_BEAT_TIME = 100
MAX_ONLINE = 50
USER_HEART_BEAT = 60
DNS_DOMAIN = ''

all_user = {}
all_client = {}
waiting_user = []
all_erro_code = {
    0: 'ok',
    1: 'missing api_key',
    2: 'missing fuc or wrong fuc',
    3: 'wrong user_key',
    4: 'wrong during calling fuc',
}
DNS = Domain('uifv2ray.xyz', 'fa2fbda74a899f4bc5b83d576ed25cff')


async def Home(req):
    text = {'ip': req.remote}
    return web.Response(text=json.dumps(text))


def GetValue(dicts, key, default_value=""):
    if key in dicts:
        return dicts[key]
    return default_value


class Client(object):
    """
    """
    def __init__(self, client_info):
        self.client_info = client_info
        self.is_off = False
        self.last_online_time = int(time.time())
        self.using_user = {}
        self.api_url = 'http://%s' % self.GetIP()
        self.req_queue = queue.Queue()
        self.client_path = DNS.DispachPath()
        DNS.CreateDNSRecord(self.client_path, self.GetIP())
        temp = DNS.GetDNSItem(self.client_path)
        DNS.UpdateDNSRecord(temp['id'], self.client_path, self.GetIP())
        threading.Thread(target=self._do_request, daemon=True).start()

    def HeartBeat(self):
        self.last_online_time = int(time.time())
        self._off_client()

    def Off(self):
        self.is_off = True
        self.using_user = {}
        DNS.FreePath(self.client_path)

    def _off_client(self):
        for item in all_client:
            if not all_client[item].IsDead() or all_client[item].is_off:
                continue
            self.Off()

    def GetClientInfo(self):
        return {
            'address': self.GetAddress(),
            'location': self.GetRegion(),
            'online_count': self.GetUserCount()
        }

    def IsDead(self):
        if self.last_online_time - int(time.time()) > 300:
            return True
        return False

    def GetIP(self):
        return self.client_info['query']

    def GetAddress(self):
        return "%s.%s" % (self.client_path, DNS.domain)

    def _do_request(self):
        while True:
            try:
                res = self.req_queue.get()
                requests.get(res['url'], params=res['params'], timeout=10)
            except:
                pass

    def _request(self, path, params, is_queue=True):
        params['api_key'] = SERVER_API_KEY
        url = self.api_url + path
        if is_queue:
            self.req_queue.put({'url': url, 'params': params})
        else:
            return requests.get(url, params=params)

    def LogoutUser(self, user_key, tag='uif_inbound_free'):
        self._request('/removeUser', params={'user_key': user_key, 'tag': tag})
        if user_key in self.using_user:
            del self.using_user[user_key]

    def LoginUser(self, user_key, tag='uif_inbound_free'):
        self._request('/addUser', params={'user_key': user_key, 'tag': tag})
        if user_key in all_user:
            self.using_user[user_key] = all_user[user_key]

    def GetUserTraffic(self, user_key, is_reset=False):
        if is_reset is True:
            is_reset = '1'
        else:
            is_reset = '0'
        res = self._request('/getTraffic',
                            params={
                                'user_key': user_key,
                                'is_reset': is_reset
                            })
        res = json.loads(res.text)
        return res['msg']

    def GetUserCount(self):
        return len(self.using_user)

    def GetRegion(self):
        res = []
        if 'country' in self.client_info:
            res.append(self.client_info['country'])
        if 'regionName' in self.client_info:
            res.append(self.client_info['regionName'])
        if 'city' in self.client_info:
            res.append(self.client_info['city'])
        return res


class FreeUser(object):
    def __init__(self, user_key):
        self.user_key = user_key
        self.is_online = False
        self.is_waitting = False
        self.last_online_time = int(time.time())
        self.last_login_time = 0
        self.using_client = None
        self.is_frequen = False

    def Login(self, params):
        now = int(time.time())
        if (now - self.last_online_time) < USER_HEART_BEAT:
            self.is_frequen = True
        else:
            self.is_frequen = False
        self.last_online_time = now

        if not self.is_online:
            self.using_client = self._get_available_client()
            if self.using_client is None:
                self.AddToWaitList()
                return self.GetWaitingInfo()
            self.PopWaitList()
            self.using_client.LoginUser(self.user_key)
            self.is_online = True
            self.last_login_time = now
        return self.using_client.GetClientInfo()

    def Logout(self):
        if self.using_client is not None:
            self.using_client.LogoutUser(self.user_key)
        self.is_online = False
        self.using_client = None
        self.PopWaitList()

    def AddToWaitList(self):
        if self.is_waitting:
            return
        waiting_user.append(self.user_key)
        self.is_waitting = True

    def PopWaitList(self):
        if self.is_waitting:
            try:
                index = waiting_user.index(self.user_key)
                waiting_user.pop(index)
            except:
                pass
        self.is_waitting = False

    def GetWaitingInfo(self):
        index = -1
        if self.is_waitting:
            index = waiting_user.index(self.user_key)
        return {
            'is_waitting': self.is_waitting,
            'total': len(waiting_user),
            'client_count': len(all_client),
            'index': index
        }

    def _offline_user(self):
        now = int(time.time())
        for item in all_user:
            if not all_user[item].is_online:
                continue
            if (now - all_user[item].last_login_time) > OCUPATION_TIME or (
                    now - all_user[item].last_online_time) > HEART_BEAT_TIME:
                all_user[item].Logout()

    def _get_available_client(self):
        self._offline_user()
        for item in all_client:
            if all_client[item].IsDead():
                continue
            if all_client[item].GetUserCount() >= MAX_ONLINE:
                continue
            return all_client[item]


def ResolvErrorCode(err_code):
    if err_code not in all_erro_code:
        return 'unknow'
    return all_erro_code[err_code]


async def UserOP(req):
    params = req.rel_url.query
    text = {'ip': req.remote, 'success': False, 'msg': '', 'err_code': 0}
    api_key = GetValue(params, 'api_key')
    user_key = GetValue(params, 'user_key')
    fuc = GetValue(params, 'fuc')
    if api_key != SERVER_API_KEY:
        text['err_code'] = 1
    elif fuc == "" or not getattr(FreeUser, fuc):
        text['err_code'] = 2
    elif user_key == "":
        text['err_code'] = 3
    else:
        if user_key not in all_user:
            all_user[user_key] = FreeUser(user_key)
        obj = all_user[user_key]
        fuc = getattr(obj, fuc)
        try:
            text['res'] = fuc(params)
        except Exception as e:
            text['res'] = str(e)
            text['err_code'] = 4
            raise e
    text['msg'] = ResolvErrorCode(text['err_code'])
    if text['err_code'] == 0:
        text['success'] = True
    return web.Response(text=json.dumps(text))


async def GetOP(req):
    params = req.rel_url.query
    api_key = GetValue(params, 'api_key')
    kind = GetValue(params, 'kind')
    if api_key != SERVER_API_KEY or kind == "":
        return web.Response(text="1")
    if kind == 'user':
        kind = all_user
    else:
        kind = all_client
    return web.Response(text=json.dumps(kind))


async def ChangeDomain(req):
    params = req.rel_url.query
    api_key = GetValue(params, 'api_key')
    name = GetValue(params, 'name')
    zone_id = GetValue(params, 'zone_id')
    if api_key != SERVER_API_KEY or name == "" or zone_id == "":
        return web.Response(text="1")
    DNS.ChangeDomain(name, zone_id)
    return web.Response(text="ok")


async def ClientOP(req):
    params = req.rel_url.query
    text = {'success': False, 'msg': '', 'err_code': 0}
    api_key = GetValue(params, 'api_key')
    query = GetValue(params, 'query')
    fuc = GetValue(params, 'fuc')
    if api_key != SERVER_API_KEY:
        text['err_code'] = 1
    elif fuc == "" or not getattr(Client, fuc):
        text['err_code'] = 2
    elif query == "":
        text['err_code'] = 3
    else:
        if query not in all_client:
            all_client[query] = Client(params)
        obj = all_client[query]
        fuc = getattr(obj, fuc)
        text['res'] = fuc()
    text['msg'] = ResolvErrorCode(text['err_code'])
    if text['err_code'] == 0:
        text['success'] = True
    return web.Response(text=json.dumps(text))


def Run():
    caddy_config_file_path = BASE_DIR + '/caddy_server.txt'
    DoCMD("sudo chmod -R 750 " + caddy_runtime.CADDY_RUNTIME_DIR)
    DoCMD("sudo ufw allow 80")
    DoCMD("sudo ufw allow 443")
    DoCMD('nohup %s run -config "%s" -adapter caddyfile' %
          (caddy_runtime.CADDY_RUNTIME_PATH, caddy_config_file_path),
          cwd=caddy_runtime.CADDY_RUNTIME_DIR,
          is_wait=False)

    app = web.Application()
    app.add_routes([
        web.get('/', Home),
        web.get('/user', UserOP),
        web.get('/client', ClientOP),
        web.get('/change_domain', ChangeDomain),
        web.get('/get', GetOP),
    ])
    web.run_app(
        app,
        host='127.0.0.1',
        port=int(SERVER_PORT),
    )  # block here


if __name__ == '__main__':
    Run()
