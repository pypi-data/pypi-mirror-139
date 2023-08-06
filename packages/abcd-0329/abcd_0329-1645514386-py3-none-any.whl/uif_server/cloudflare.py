import requests
import json

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
        self.domain = domain
        self.zone_id = zone_id
        self.local_dns = {}

    def _handle_path(self, path):
        return "%s.%s" % (path, self.domain)

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


def Test():
    test_domain = 'uifv2ray.xyz'
    test_zone_id = 'fa2fbda74a899f4bc5b83d576ed25cff'
    test_path = 'test3'
    value = '45.32.140.15'

    test_dns = Domain(test_domain, test_zone_id)

    res = test_dns.CreateDNSRecord(test_path, value)
    assert res['success']

    added_record = test_dns.GetDNSItem(test_path)
    assert added_record is not None
    assert added_record['proxied']
    assert added_record['ttl'] == 1
    assert added_record['name'] == '%s.%s' % (test_path, test_domain)
    assert added_record['content'] == value

    res = test_dns.UpdateDNSRecord(added_record['id'], test_path, value)
    assert res['success']
    assert res['result']['proxied']

    res = test_dns.DeleteDNSRecord(added_record['id'])
    assert res['success']
