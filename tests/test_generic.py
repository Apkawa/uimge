#!/usr/bin/python
import os
#http://somethingaboutorange.com/mrl/projects/nose/0.11.3/testing_tools.html


TEST_DIR = os.path.abspath(os.path.dirname(__file__))
PROGRAM_DIR = os.path.dirname(TEST_DIR)
os.sys.path.insert(0, PROGRAM_DIR)

from uimge import uimge

class BaseHostCase(object):
    def _run_host(self, host, obj):
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


    def test_ib_imgby(self):
        """
        test_ib_imgby http://imgby.com
        """
        for f in self.fixtures:
            self._run_host(uimge.Hosts.hosts_dict.get('ib_imgby'), f)

    def test_pf_picfront(self):
        """
        test_pf_picfront http://picfront.org
        """
        for f in self.fixtures:
            self._run_host(uimge.Hosts.hosts_dict.get('pf_picfront'), f)

    def test_ps_pictureshack(self):
        """
        test_ps_pictureshack http://pictureshack.ru
        """
        for f in self.fixtures:
            self._run_host(uimge.Hosts.hosts_dict.get('ps_pictureshack'), f)

    def test_im_itmages(self):
        """
        test_im_itmages http://itmages.ru
        """
        for f in self.fixtures:
            self._run_host(uimge.Hosts.hosts_dict.get('im_itmages'), f)

    def test_sp_savepic(self):
        """
        test_sp_savepic http://savepic.ru
        """
        for f in self.fixtures:
            self._run_host(uimge.Hosts.hosts_dict.get('sp_savepic'), f)

    def test_p_picthost(self):
        """
        test_p_picthost http://picthost.ru
        """
        for f in self.fixtures:
            self._run_host(uimge.Hosts.hosts_dict.get('p_picthost'), f)

    def test_o_opicture(self):
        """
        test_o_opicture http://opicture.ru
        """
        for f in self.fixtures:
            self._run_host(uimge.Hosts.hosts_dict.get('o_opicture'), f)

    def test_al_anime_last(self):
        """
        test_al_anime_last http://sun.anime-last.info
        """
        for f in self.fixtures:
            self._run_host(uimge.Hosts.hosts_dict.get('al_anime_last'), f)

    def test_pu_pikucha(self):
        """
        test_pu_pikucha http://pikucha.ru
        """
        for f in self.fixtures:
            self._run_host(uimge.Hosts.hosts_dict.get('pu_pikucha'), f)

    def test_10p_10pix(self):
        """
        test_10p_10pix http://10pix.ru
        """
        for f in self.fixtures:
            self._run_host(uimge.Hosts.hosts_dict.get('10p_10pix'), f)

    def test_it_itrash(self):
        """
        test_it_itrash http://itrash.ru
        """
        for f in self.fixtures:
            self._run_host(uimge.Hosts.hosts_dict.get('it_itrash'), f)

    def test_c2n_clip2net(self):
        """
        test_c2n_clip2net http://clip2net.com
        """
        for f in self.fixtures:
            self._run_host(uimge.Hosts.hosts_dict.get('c2n_clip2net'), f)

    def test_s_smages(self):
        """
        test_s_smages http://smages.com
        """
        for f in self.fixtures:
            self._run_host(uimge.Hosts.hosts_dict.get('s_smages'), f)

    def test_k_imageshack(self):
        """
        test_k_imageshack http://imageshack.us
        """
        for f in self.fixtures:
            self._run_host(uimge.Hosts.hosts_dict.get('k_imageshack'), f)

    def test_r_radikal(self):
        """
        test_r_radikal http://radikal.ru
        """
        for f in self.fixtures:
            self._run_host(uimge.Hosts.hosts_dict.get('r_radikal'), f)

    def test_xt_xtupload(self):
        """
        test_xt_xtupload http://xtupload.com
        """
        for f in self.fixtures:
            self._run_host(uimge.Hosts.hosts_dict.get('xt_xtupload'), f)

    def test_iu_imageup(self):
        """
        test_iu_imageup http://imageup.ru
        """
        for f in self.fixtures:
            self._run_host(uimge.Hosts.hosts_dict.get('iu_imageup'), f)

    def test_px_pixs(self):
        """
        test_px_pixs http://pixs.ru
        """
        for f in self.fixtures:
            self._run_host(uimge.Hosts.hosts_dict.get('px_pixs'), f)

    def test_fp_fastpic(self):
        """
        test_fp_fastpic http://fastpic.ru
        """
        for f in self.fixtures:
            self._run_host(uimge.Hosts.hosts_dict.get('fp_fastpic'), f)

    def test_ig_imgur(self):
        """
        test_ig_imgur http://imgur.com
        """
        for f in self.fixtures:
            self._run_host(uimge.Hosts.hosts_dict.get('ig_imgur'), f)

    def test_hm_hostmyjpg(self):
        """
        test_hm_hostmyjpg http://hostmyjpg.com
        """
        for f in self.fixtures:
            self._run_host(uimge.Hosts.hosts_dict.get('hm_hostmyjpg'), f)

    def test_pb_picbox(self):
        """
        test_pb_picbox http://picbox.su
        """
        for f in self.fixtures:
            self._run_host(uimge.Hosts.hosts_dict.get('pb_picbox'), f)

    def test_u_funkyimg(self):
        """
        test_u_funkyimg http://funkyimg.com
        """
        for f in self.fixtures:
            self._run_host(uimge.Hosts.hosts_dict.get('u_funkyimg'), f)

    def test_j1_jpg1(self):
        """
        test_j1_jpg1 http://jpg1.ru
        """
        for f in self.fixtures:
            self._run_host(uimge.Hosts.hosts_dict.get('j1_jpg1'), f)

    def test_ba_bayimg(self):
        """
        test_ba_bayimg http://bayimg.com
        """
        for f in self.fixtures:
            self._run_host(uimge.Hosts.hosts_dict.get('ba_bayimg'), f)

    def test_om_omploader(self):
        """
        test_om_omploader http://omploader.org
        """
        for f in self.fixtures:
            self._run_host(uimge.Hosts.hosts_dict.get('om_omploader'), f)

    def test_pm_picamatic(self):
        """
        test_pm_picamatic http://picamatic.com
        """
        for f in self.fixtures:
            self._run_host(uimge.Hosts.hosts_dict.get('pm_picamatic'), f)


class TestHostsUploadFile(BaseHostCase):
    fixtures = [
            os.path.join(TEST_DIR, 'fixtures/qr.png'),
            ]

class TestHostsUploadUrl(BaseHostCase):
    fixtures = ["http://s41.radikal.ru/i092/0902/93/40b756930f38.png",]



def make():
    for host, host_obj in uimge.Hosts.hosts_dict.iteritems():
        print \
'''
    def test_{0}(self):
        """
        test_{0} http://{1}
        """
        for f in self.fixtures:
            self._run_host(uimge.Hosts.hosts_dict.get('{0}'), f)'''.format(host, host_obj.host)

if __name__ == "__main__":
    make()

