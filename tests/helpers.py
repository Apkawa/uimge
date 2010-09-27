#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from copy import copy
#http://somethingaboutorange.com/mrl/projects/nose/0.11.3/testing_tools.html



TEST_DIR = os.path.abspath(os.path.dirname(__file__))
PROGRAM_DIR = os.path.dirname(TEST_DIR)
os.sys.path.insert(0, PROGRAM_DIR)

FIXTURES = [os.path.join(TEST_DIR, 'fixtures/qr.png'), "http://s41.radikal.ru/i092/0902/93/40b756930f38.png"]


from uimge import uimge

class BaseHostCase(object):
    def _run_host(self, host, obj):
        _hosts = copy(uimge.Hosts.hosts_dict)
        _hosts.update(uimge.Hosts.dev_hosts_dict)
        host = _hosts.get(host)

        assert host
        host = host()

        host.upload(obj)
        host.preload()
        host.send_post()
        host.postload()

        result = host.img_url, host.img_thumb_url
        assert result
        for r in result:
            assert r
            assert r.startswith('http://')
        return result

''
################################
# Генератор тестов. использует exec
################################
class_template = \
'''
class Test{0}(BaseHostCase):
    fixtures = {1}'''
methods_template = \
'''
    def test_{0}(self):
        """
        Test{2}.test_{0} http://{1}
        """
        for f in self.fixtures:
            self._run_host('{0}', f)'''

for classname, fixtures in (
            ('HostsUpload', FIXTURES),
            ):
    for_eval = []
    for_eval.append(class_template.format(classname, fixtures))
    for host, host_obj in uimge.Hosts.hosts_dict.iteritems():
        for_eval.append(methods_template.format(host, host_obj.host, classname))
    s = ''.join(for_eval)
    #print s
    exec(s)

for classname, fixtures in (
            ('DevHostsUpload', FIXTURES),
            ):
    for_eval = []
    for_eval.append(class_template.format(classname, fixtures))
    for host, host_obj in uimge.Hosts.dev_hosts_dict.iteritems():
        if host != 'ex_example':
            for_eval.append(methods_template.format(host, host_obj.host, classname))
    s = ''.join(for_eval)
    #print s
    exec(s)


if __name__ == "__main__":

    pass
