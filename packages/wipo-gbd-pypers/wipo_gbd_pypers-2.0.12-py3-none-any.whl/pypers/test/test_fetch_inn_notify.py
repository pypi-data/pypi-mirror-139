import unittest
from pypers.steps.fetch.download.inn.notify import Notify
from pypers.utils.utils import dict_update
import os
import shutil
import copy
from pypers.utils import utils
from pypers.test import captured_output
from pypers.test import mock_db, mockde_db, mock_logger
from mock import patch, MagicMock


def sendmail(f, t, s, text=None, html=None,
             files=None, server="127.0.0.1"):
    print("%s %s %s" % (f, t, s))


class TestLire(unittest.TestCase):
    path_test = os.path.join(os.path.dirname(__file__), 'foo')
    cfg = {
        'step_class': 'pypers.steps.fetch.download.inn.notify.Notify',
        'sys_path': None,
        'name': 'Notify',
        'meta': {
            'job': {},
            'pipeline': {
                'input': {
                },
                'run_id': 1,
                'log_dir': path_test
            },
            'step': {},
        },
        'output_dir': path_test
    }

    extended_cfg = {
        'new_publication': ['Proposed List 11 - 10 names'],
        'recipients': ['unit_test@wipo.int'],
    }

    @patch("pypers.core.interfaces.db.get_db_logger", MagicMock(side_effect=mock_logger))
    def setUp(self):
        self.old_send = utils.send_mail
        utils.send_mail = sendmail
        try:
            shutil.rmtree(self.path_test)
        except Exception as e:
            pass
        os.makedirs(self.path_test)
        self.cfg = dict_update(self.cfg, self.extended_cfg)

    @patch("pypers.core.interfaces.db.get_db_logger", MagicMock(side_effect=mock_logger))
    def tearDown(self):
        utils.send_mail = self.old_send
        try:
            shutil.rmtree(self.path_test)
            pass
        except Exception as e:
            pass

    @patch("pypers.core.interfaces.db.get_db", MagicMock(side_effect=mock_db))
    @patch("pypers.core.interfaces.db.get_db_logger", MagicMock(side_effect=mock_logger))
    def test_process_no_recipents(self):
        tmp = copy.deepcopy(self.cfg)
        mockde_db.update(tmp)
        tmp['recipients'] = []
        step = Notify.load_step("test", "test", "step")
        self.assertEqual(step.process(), None)

    @patch("pypers.core.interfaces.db.get_db", MagicMock(side_effect=mock_db))
    @patch("pypers.core.interfaces.db.get_db_logger", MagicMock(side_effect=mock_logger))
    def test_process_no_pubications(self):
        tmp = copy.deepcopy(self.cfg)
        mockde_db.update(tmp)
        tmp['new_publication'] = []
        step = Notify.load_step("test", "test", "step")
        self.assertEqual(step.process(), None)

    @patch("pypers.core.interfaces.db.get_db", MagicMock(side_effect=mock_db))
    @patch("pypers.core.interfaces.db.get_db_logger", MagicMock(side_effect=mock_logger))
    def test_process_from_web(self):
        mockde_db.update(self.cfg)
        step = Notify.load_step("test", "test", "step")
        with captured_output() as (out, err):
            step.process()
            output = out.getvalue().strip()
        output = output.split('\n')[0]


if __name__ == "__main__":
    unittest.main()
