#!/usr/bin/python2
# -*- coding: utf-8 -*-
import os

from helpers import BaseHostCase

TEST_ROOT = os.path.dirname(os.path.abspath(__file__))
FIXTURES_ROOT = os.path.join(TEST_ROOT, 'fixtures')
print FIXTURES_ROOT

class TestHostsUpload(BaseHostCase):
    fixtures = [os.path.join(FIXTURES_ROOT,'1.gif'), 'http://habreffect.ru/files/fa8/4a8042f57/1.gif']

    def test_ib_imgby(self):
        """
        TestHostsUpload.test_ib_imgby http://imgby.com
        """
        for f in self.fixtures:
            self._run_host('ib_imgby', f)

    def test_pf_picfront(self):
        """
        TestHostsUpload.test_pf_picfront http://picfront.org
        """
        for f in self.fixtures:
            self._run_host('pf_picfront', f)

    def test_ps_pictureshack(self):
        """
        TestHostsUpload.test_ps_pictureshack http://pictureshack.ru
        """
        for f in self.fixtures:
            self._run_host('ps_pictureshack', f)

    def test_im_itmages(self):
        """
        TestHostsUpload.test_im_itmages http://itmages.ru
        """
        for f in self.fixtures:
            self._run_host('im_itmages', f)

    def test_sp_savepic(self):
        """
        TestHostsUpload.test_sp_savepic http://savepic.ru
        """
        for f in self.fixtures:
            self._run_host('sp_savepic', f)

    def test_j1_jpg1(self):
        """
        TestHostsUpload.test_j1_jpg1 http://jpg1.ru
        """
        for f in self.fixtures:
            self._run_host('j1_jpg1', f)

    def test_al_anime_last(self):
        """
        TestHostsUpload.test_al_anime_last http://sun.anime-last.info
        """
        for f in self.fixtures:
            self._run_host('al_anime_last', f)

    def test_pu_pikucha(self):
        """
        TestHostsUpload.test_pu_pikucha http://pikucha.ru
        """
        for f in self.fixtures:
            self._run_host('pu_pikucha', f)

    def test_10p_10pix(self):
        """
        TestHostsUpload.test_10p_10pix http://10pix.ru
        """
        for f in self.fixtures:
            self._run_host('10p_10pix', f)

    def test_it_itrash(self):
        """
        TestHostsUpload.test_it_itrash http://itrash.ru
        """
        for f in self.fixtures:
            self._run_host('it_itrash', f)

    def test_c2n_clip2net(self):
        """
        TestHostsUpload.test_c2n_clip2net http://clip2net.com
        """
        for f in self.fixtures:
            self._run_host('c2n_clip2net', f)

    def test_s_smages(self):
        """
        TestHostsUpload.test_s_smages http://smages.com
        """
        for f in self.fixtures:
            self._run_host('s_smages', f)

    def test_k_imageshack(self):
        """
        TestHostsUpload.test_k_imageshack http://imageshack.us
        """
        for f in self.fixtures:
            self._run_host('k_imageshack', f)

    def test_r_radikal(self):
        """
        TestHostsUpload.test_r_radikal http://radikal.ru
        """
        for f in self.fixtures:
            self._run_host('r_radikal', f)

    def test_xt_xtupload(self):
        """
        TestHostsUpload.test_xt_xtupload http://xtupload.com
        """
        for f in self.fixtures:
            self._run_host('xt_xtupload', f)

    def test_iu_imageup(self):
        """
        TestHostsUpload.test_iu_imageup http://imageup.ru
        """
        for f in self.fixtures:
            self._run_host('iu_imageup', f)

    def test_px_pixs(self):
        """
        TestHostsUpload.test_px_pixs http://pixs.ru
        """
        for f in self.fixtures:
            self._run_host('px_pixs', f)

    def test_fp_fastpic(self):
        """
        TestHostsUpload.test_fp_fastpic http://fastpic.ru
        """
        for f in self.fixtures:
            self._run_host('fp_fastpic', f)

    def test_ig_imgur(self):
        """
        TestHostsUpload.test_ig_imgur http://imgur.com
        """
        for f in self.fixtures:
            self._run_host('ig_imgur', f)

    def test_pb_picbox(self):
        """
        TestHostsUpload.test_pb_picbox http://picbox.su
        """
        for f in self.fixtures:
            self._run_host('pb_picbox', f)

    def test_u_funkyimg(self):
        """
        TestHostsUpload.test_u_funkyimg http://funkyimg.com
        """
        for f in self.fixtures:
            self._run_host('u_funkyimg', f)

    def test_p_picthost(self):
        """
        TestHostsUpload.test_p_picthost http://picthost.ru
        """
        for f in self.fixtures:
            self._run_host('p_picthost', f)

    def test_ba_bayimg(self):
        """
        TestHostsUpload.test_ba_bayimg http://bayimg.com
        """
        for f in self.fixtures:
            self._run_host('ba_bayimg', f)

    def test_om_omploader(self):
        """
        TestHostsUpload.test_om_omploader http://omploader.org
        """
        for f in self.fixtures:
            self._run_host('om_omploader', f)

    def test_pm_picamatic(self):
        """
        TestHostsUpload.test_pm_picamatic http://picamatic.com
        """
        for f in self.fixtures:
            self._run_host('pm_picamatic', f)

class __TestDevHostsUpload(BaseHostCase):
    fixtures = ['/home/apkawa/Code/uimge/uimge/tests/fixtures/qr.png', 'http://s41.radikal.ru/i092/0902/93/40b756930f38.png']

    def test_xe_xegami(self):
        """
        TestDevHostsUpload.test_xe_xegami http://xegami.com
        """
        for f in self.fixtures:
            self._run_host('xe_xegami', f)

    def test_k4_keep4u(self):
        """
        TestDevHostsUpload.test_k4_keep4u http://keep4u.ru
        """
        for f in self.fixtures:
            self._run_host('k4_keep4u', f)

    def test_i_ipicture(self):
        """
        TestDevHostsUpload.test_i_ipicture http://ipicture.ru
        """
        for f in self.fixtures:
            self._run_host('i_ipicture', f)

    def test_zi_zikuka(self):
        """
        TestDevHostsUpload.test_zi_zikuka http://zikuka.ru
        """
        for f in self.fixtures:
            self._run_host('zi_zikuka', f)

    def test_pc_piccy(self):
        """
        TestDevHostsUpload.test_pc_piccy http://piccy.info
        """
        for f in self.fixtures:
            self._run_host('pc_piccy', f)

    def test_ir_imagebits(self):
        """
        TestDevHostsUpload.test_ir_imagebits http://image-bits.ro
        """
        for f in self.fixtures:
            self._run_host('ir_imagebits', f)

    def test_o_opicture(self):
        """
        TestDevHostsUpload.test_o_opicture http://opicture.ru
        """
        for f in self.fixtures:
            self._run_host('o_opicture', f)

    def test_tp_tinypic(self):
        """
        TestDevHostsUpload.test_tp_tinypic http://tinypic.com
        """
        for f in self.fixtures:
            self._run_host('tp_tinypic', f)

    def test_up_upimg(self):
        """
        TestDevHostsUpload.test_up_upimg http://upimg.ru
        """
        for f in self.fixtures:
            self._run_host('up_upimg', f)

    def test_hm_hostmyjpg(self):
        """
        TestDevHostsUpload.test_hm_hostmyjpg http://hostmyjpg.com
        """
        for f in self.fixtures:
            self._run_host('hm_hostmyjpg', f)

    def test_xp_xpichost(self):
        """
        TestDevHostsUpload.test_xp_xpichost http://xpichost.net
        """
        for f in self.fixtures:
            self._run_host('xp_xpichost', f)
