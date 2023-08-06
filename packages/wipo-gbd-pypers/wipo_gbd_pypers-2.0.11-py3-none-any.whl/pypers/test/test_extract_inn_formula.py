import unittest
from pypers.steps.fetch.extract.inn.formula import FORMULA
from pypers.utils.utils import dict_update
from pypers.test import mock_db, mockde_db, mock_logger
from mock import patch, MagicMock
import os
import shutil
import copy


class MockPage:

    @patch("pypers.core.interfaces.db.get_db_logger", MagicMock(side_effect=mock_logger))
    def __init__(self):
        self.text = '''
        <table><tr><td><font>Molecular Formula</font></td><td><img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg==" /></td></tr></table>
        '''

    @patch("pypers.core.interfaces.db.get_db_logger", MagicMock(side_effect=mock_logger))
    def __exit__(self, *args, **kwargs):
        pass

    @patch("pypers.core.interfaces.db.get_db_logger", MagicMock(side_effect=mock_logger))
    def __enter__(self, *args, **kwargs):
        pass


def mock_page(*args, **kwargs):
    return MockPage()


class TestMerge(unittest.TestCase):

    path_test = os.path.join(os.path.dirname(__file__), 'foo')
    cfg = {
        'step_class': ' pypers.steps.fetch.extract.inn.formula.FORMULA',
        'sys_path': None,
        'name': 'FORMULA',
        'meta': {
            'job': {},
            'pipeline': {
                'input': {
                    'from_web': {
                        'credentials': {
                            'user': 'toto',
                            'password': 'password'
                        }
                    }

                },
                'run_id': 1,
                'log_dir': path_test
            },
            'step': {},
        },
        'output_dir': path_test
    }

    extended_cfg = {
        'input_data': [[{
            'img_uri': 'http://my_url.com/img',
            'appnum': 'F001',
            'xml': path_test
        }, {'appnum': 'F002'}]],
        'archive_name': 'toto.zip',
        'input_dir': path_test
    }

    @patch("pypers.core.interfaces.db.get_db_logger", MagicMock(side_effect=mock_logger))
    def setUp(self):
        try:
            shutil.rmtree(self.path_test)
        except Exception as e:
            pass
        os.makedirs(self.path_test)

        self.cfg = dict_update(self.cfg, self.extended_cfg)

    @patch("pypers.core.interfaces.db.get_db_logger", MagicMock(side_effect=mock_logger))
    def tearDown(self):
        try:
            shutil.rmtree(self.path_test)
            pass
        except Exception as e:
            pass

    @patch("requests.sessions.Session.get",
           MagicMock(side_effect=mock_page))
    @patch("pypers.core.interfaces.db.get_db", MagicMock(side_effect=mock_db))
    @patch("pypers.core.interfaces.db.get_db_logger", MagicMock(side_effect=mock_logger))
    def test_process(self):
        mockde_db.update(self.cfg)
        step = FORMULA.load_step("test", "test", "step")
        step.process()

    @patch("requests.sessions.Session.get",
           MagicMock(side_effect=mock_page))
    @patch("pypers.core.interfaces.db.get_db", MagicMock(side_effect=mock_db))
    @patch("pypers.core.interfaces.db.get_db_logger", MagicMock(side_effect=mock_logger))
    def test_process_2(self):
        tmp = copy.deepcopy(self.cfg)
        mockde_db.update(tmp)
        tmp['input_data'] = []
        step = FORMULA.load_step("test", "test", "step")
        step.process()


if __name__ == "__main__":
    unittest.main()
