import unittest
from pypers.steps.fetch.download.catm import CATM
from pypers.utils.utils import dict_update
import os
import shutil
import copy
from pypers.test import mock_db, mockde_db, mock_logger
from mock import patch, MagicMock


def mock_validate(*args, **kwargs):
    return True


class MockStream:

    @patch("pypers.core.interfaces.db.get_db_logger", MagicMock(side_effect=mock_logger))
    def read(self, *args, **kwargs):
        return ''


class MockPage:

    @patch("pypers.core.interfaces.db.get_db_logger", MagicMock(side_effect=mock_logger))
    def __init__(self, raw=False):
        self.text = ""
        for i in range(0, 10):
            self.text += '<tr><td>archive%s.zip</td><td>' \
                         '<a href="foo?wpdmdl=bar&ind=%s.zip">C</a></td></tr>'
            self.text = self.text % (i, i)
        if raw:
            self.raw = MockStream()

    @patch("pypers.core.interfaces.db.get_db_logger", MagicMock(side_effect=mock_logger))
    def __exit__(self, *args, **kwargs):
        pass

    @patch("pypers.core.interfaces.db.get_db_logger", MagicMock(side_effect=mock_logger))
    def __enter__(self, *args, **kwargs):
        pass

    @patch("pypers.core.interfaces.db.get_db_logger", MagicMock(side_effect=mock_logger))
    def iter_content(self, *args, **kwargs):
        return 'toto'


def side_effect_mock_page(*args, **kwargs):
    return MockPage(raw=('stream' in kwargs))


class TestLire(unittest.TestCase):
    path_test = os.path.join(os.path.dirname(__file__), 'foo')
    cfg = {
        'step_class': 'pypers.steps.fetch.download.catm.CATM',
        'sys_path': None,
        'name': 'CATM',
        'meta': {
            'job': {},
            'pipeline': {
                'input': {
                    'done_file': os.path.join(path_test, 'done.done'),
                    'from_dir': os.path.join(path_test, 'from_dir'),
                },
                'run_id': 1,
                'log_dir': path_test
            },
            'step': {},
        },
        'output_dir': path_test
    }

    extended_cfg = {
        'limit': 0,
        'file_regex': ".*.zip",
    }

    @patch("pypers.core.interfaces.db.get_db_logger", MagicMock(side_effect=mock_logger))
    def setUp(self):
        try:
            shutil.rmtree(self.path_test)
        except Exception as e:
            pass
        os.makedirs(self.path_test)
        os.makedirs(os.path.join(self.path_test, 'from_dir'))
        with open(os.path.join(self.path_test, 'done.done'), 'w') as f:
            f.write('0\tarchive1.zip\ttoto\t')
        for i in range(0, 10):
            with open(os.path.join(self.path_test,
                                   'from_dir', 'archive%s.zip' % i), 'w') as f:
                f.write('toto')
        self.cfg = dict_update(self.cfg, self.extended_cfg)

    @patch("pypers.core.interfaces.db.get_db_logger", MagicMock(side_effect=mock_logger))
    def tearDown(self):
        try:
            shutil.rmtree(self.path_test)
            pass
        except Exception as e:
            pass

    @patch("pypers.utils.utils.validate_archive", MagicMock(side_effect=mock_validate))
    @patch("pypers.core.interfaces.db.get_db", MagicMock(side_effect=mock_db))
    @patch("pypers.core.interfaces.db.get_db_logger", MagicMock(side_effect=mock_logger))
    def test_process(self):
        mockde_db.update(self.cfg)
        step = CATM.load_step("test", "test", "step")
        step.process()
        for i in range(0, 10):
            if i == 1:
                continue
            archive = os.path.join(self.path_test, 'from_dir',
                                   'archive%s.zip' % i)
            self.assertTrue(archive in step.output_files)

    @patch("pypers.utils.utils.validate_archive", MagicMock(side_effect=mock_validate))
    @patch("pypers.core.interfaces.db.get_db", MagicMock(side_effect=mock_db))
    @patch("pypers.core.interfaces.db.get_db_logger", MagicMock(side_effect=mock_logger))
    def test_process_exception(self):
        tmp = copy.deepcopy(self.cfg)
        mockde_db.update(tmp)
        tmp['meta']['pipeline']['input'].pop('from_dir')
        step = CATM.load_step("test", "test", "step")
        try:
            step.process()
            self.fail('Should rise exception because no input is given')
        except Exception as e:
            pass

    @patch("pypers.utils.utils.validate_archive", MagicMock(side_effect=mock_validate))
    @patch("requests.sessions.Session.get",
           MagicMock(side_effect=side_effect_mock_page))
    @patch("pypers.core.interfaces.db.get_db", MagicMock(side_effect=mock_db))
    @patch("pypers.core.interfaces.db.get_db_logger", MagicMock(side_effect=mock_logger))
    def test_process_from_web(self):
        tmp = copy.deepcopy(self.cfg)
        mockde_db.update(tmp)
        tmp['meta']['pipeline']['input'].pop('from_dir')
        tmp['meta']['pipeline']['input']['from_web'] = {
            'credentials': {
                'user': 'toto',
                'password': 'password'
            },
            'url': 'http://my_url.url.com'
        }

        step = CATM.load_step("test", "test", "step")
        step.process()
        for i in range(0, 10):
            if i == 1:
                continue
            archive = os.path.join(self.path_test,
                                   'archive%s.zip' % i)
            self.assertTrue(archive in step.output_files)


if __name__ == "__main__":
    unittest.main()
