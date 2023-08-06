import unittest
from pypers.steps.fetch.extract.it.update_status import UpdateStatus
from pypers.utils.utils import dict_update
from pypers.test import mock_db, mockde_db, mock_logger
from mock import patch, MagicMock
import os
import shutil
import copy
import gzip


class MockPage:

    @patch("pypers.core.interfaces.db.get_db_logger", MagicMock(side_effect=mock_logger))
    def __init__(self, include_error=False, include_media=False):
        self.media = '<MarkImageURI>Toto</MarkImageURI>'
        if not include_media:
            self.media = ''
        self.content = '''<?xml version="1.0" encoding="UTF-8"?>
        <Transaction xmlns="http://www.wipo.int/standards/XMLSchema/trademarks">
          <TradeMarkTransactionBody>
            <ApplicantKey>
              <Applicant>toto</Applicant>
            </ApplicantKey>
            <RepresentativeKey>
              <Representative>foo</Representative>
            </RepresentativeKey>
          </TradeMarkTransactionBody>
          <DesignRepresentationSheetDetails>
          </DesignRepresentationSheetDetails>
          %s
        </Transaction>''' % self.media
        if include_error:
            self.content = '''<?xml version="1.0" encoding="UTF-8"?>
<Transaction xmlns="http://www.wipo.int/standards/XMLSchema/trademarks">
 <exceptionVO>
   <TransactionContentDetails>
   </TransactionContentDetails>
 </exceptionVO>
</Transaction>'''

    @patch("pypers.core.interfaces.db.get_db_logger", MagicMock(side_effect=mock_logger))
    def __exit__(self, *args, **kwargs):
        pass

    @patch("pypers.core.interfaces.db.get_db_logger", MagicMock(side_effect=mock_logger))
    def __enter__(self, *args, **kwargs):
        pass


nb_calls = 0


def mock_page(*args, **kwargs):
    global nb_calls
    nb_calls += 1
    return MockPage(include_error=(nb_calls == 1),
                    include_media=(nb_calls == 2))


def mock_get_nodevalue(*args, **kwargs):
    global nb_calls
    if nb_calls == 12:
        raise Exception()
    return 'fooo'


class TestMerge(unittest.TestCase):

    path_test = os.path.join(os.path.dirname(__file__), 'foo')
    cfg = {
        'step_class': ' pypers.steps.fetch.extract.it.update_status.UpdateStatus',
        'sys_path': None,
        'name': 'UpdateStatus',
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
        'output_dir': path_test,
    }

    extended_cfg = {
        'input_files': [os.path.join(path_test, 'foobar.txt')],
        'xml_store': path_test
    }

    @patch("pypers.core.interfaces.db.get_db_logger", MagicMock(side_effect=mock_logger))
    def setUp(self):
        try:
            shutil.rmtree(self.path_test)
        except Exception as e:
            pass
        os.makedirs(self.path_test)
        with open(os.path.join(self.path_test, 'foobar.txt'), 'w') as f:
            f.write("""
20 skip line
30F0103,20
30F0102,20
""")
        path = os.path.join(self.path_test, '01', '02')
        os.makedirs(path)
        with gzip.open(os.path.join(path, "F0102.xml.gz"), 'wb') as f:
            f.write(b'''<?xml version="1.0" encoding="UTF-8"?>
        <Transaction xmlns="http://www.wipo.int/standards/XMLSchema/trademarks">
            <MarkCurrentStatusCode>
                totototo
            </MarkCurrentStatusCode>
        </Transaction>
            ''')
        with open(os.path.join(path, "F0102.high.png"), 'w') as f:
            f.write('''<?xml version="1.0" encoding="UTF-8"?>
        <Transaction xmlns="http://www.wipo.int/standards/XMLSchema/trademarks">
            <MarkCurrentStatusCode>
                totototo
            </MarkCurrentStatusCode>
        </Transaction>
            ''')

        self.cfg = dict_update(self.cfg, self.extended_cfg)

    @patch("pypers.core.interfaces.db.get_db_logger", MagicMock(side_effect=mock_logger))
    def tearDown(self):
        try:
            shutil.rmtree(self.path_test)
            pass
        except Exception as e:
            pass

    @patch('pypers.utils.xmldom.get_nodevalue',
           MagicMock(side_effect=mock_get_nodevalue))
    @patch("requests.sessions.Session.get",
           MagicMock(side_effect=mock_page))
    @patch("pypers.core.interfaces.db.get_db", MagicMock(side_effect=mock_db))
    @patch("pypers.core.interfaces.db.get_db_logger", MagicMock(side_effect=mock_logger))
    def test_process(self):
        mockde_db.update(self.cfg)
        step = UpdateStatus.load_step("test", "test", "step")
        step.process()

    @patch("pypers.core.interfaces.db.get_db", MagicMock(side_effect=mock_db))
    @patch("pypers.core.interfaces.db.get_db_logger", MagicMock(side_effect=mock_logger))
    def test_process_no_input(self):
        tmp = copy.deepcopy(self.cfg)
        mockde_db.update(tmp)
        tmp['input_files'] = []
        step = UpdateStatus.load_step("test", "test", "step")
        step.process()


if __name__ == "__main__":
    unittest.main()
