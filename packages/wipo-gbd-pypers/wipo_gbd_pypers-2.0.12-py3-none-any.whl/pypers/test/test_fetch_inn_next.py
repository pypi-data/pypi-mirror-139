import unittest
from pypers.steps.fetch.download.inn.next import Next
from pypers.utils.utils import dict_update
import os
import shutil
import copy
from pypers.test import mock_db, mockde_db, mock_logger
from mock import patch, MagicMock


class MockStream:

    @patch("pypers.core.interfaces.db.get_db_logger", MagicMock(side_effect=mock_logger))
    def read(self, *args, **kwargs):
        return ''


class MockPage:

    @patch("pypers.core.interfaces.db.get_db_logger", MagicMock(side_effect=mock_logger))
    def __init__(self, raw=False):
        self.text = ""
        for i in range(0, 10):
            self.text += '<br> <a class="INN_Hub" href="archive%s.zip">' \
                         'archive%i.zip</a>'
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
        'step_class': 'pypers.steps.fetch.download.inn.next.Next',
        'sys_path': None,
        'name': 'Next',
        'meta': {
            'job': {},
            'pipeline': {
                'input': {
                    'done_file': os.path.join(path_test, 'done.done'),
                },
                'run_id': 1,
                'log_dir': path_test
            },
            'step': {},
        },
        'output_dir': path_test
    }

    extended_cfg = {
    }

    @patch("pypers.core.interfaces.db.get_db_logger", MagicMock(side_effect=mock_logger))
    def setUp(self):
        try:
            shutil.rmtree(self.path_test)
        except Exception as e:
            pass
        os.makedirs(self.path_test)
        mock_db().test_updated_done(['0\tproposed-10\ttoto\t\n', '1\trecommended-11\ttoto\t\n'])
        self.cfg = dict_update(self.cfg, self.extended_cfg)

    @patch("pypers.core.interfaces.db.get_db_logger", MagicMock(side_effect=mock_logger))
    def tearDown(self):
        mock_db().test_updated_done([])
        try:
            shutil.rmtree(self.path_test)
            pass
        except Exception as e:
            pass

    @patch("pypers.core.interfaces.db.get_db", MagicMock(side_effect=mock_db))
    @patch("pypers.core.interfaces.db.get_db_logger", MagicMock(side_effect=mock_logger))
    @patch("pypers.core.interfaces.db.get_done_file_manager", MagicMock(side_effect=mock_db))
    def test_process_exception(self):
        tmp = copy.deepcopy(self.cfg)
        mockde_db.update(tmp)
        step = Next.load_step("test", "test", "step")
        try:
            step.process()
            self.fail('Should rise exception because no input is given')
        except Exception as e:
            pass

    @patch("requests.sessions.Session.get",
           MagicMock(side_effect=side_effect_mock_page))
    @patch("pypers.core.interfaces.db.get_db", MagicMock(side_effect=mock_db))
    @patch("pypers.core.interfaces.db.get_db_logger", MagicMock(side_effect=mock_logger))
    @patch("pypers.core.interfaces.db.get_done_file_manager", MagicMock(side_effect=mock_db))
    def test_process_from_web(self):
        tmp = copy.deepcopy(self.cfg)
        mockde_db.update(tmp)
        tmp['meta']['pipeline']['input'] = {
            'done_file': os.path.join(self.path_test, 'done.done'),
            'credentials': {
                'client': 'python',
                'password': 'password'
            },
            'url': 'http://my_url.url.com'
        }

        step = Next.load_step("test", "test", "step")
        step.process()
        self.assertEqual(['Proposed List 11 - 10 names'], step.new_publication)


if __name__ == "__main__":
    unittest.main()
