import unittest
import tempfile
import configparser

from ...utils import config


class Test(unittest.TestCase):

    def setUp(self):
        # Use a temporary file to test the config
        file_ = tempfile.NamedTemporaryFile()
        config.configPath = file_.name

    def test_getConfig(self):
        self.assertIsInstance(config.getConfig(), configparser.SectionProxy)

    def test_setDefaultConfigFile(self):
        self.assertIsNone(config.setDefaultConfigFile())

    def test_update(self):
        config.update('some_name', 'some_value')
        retrieved = config.getConfig()
        self.assertEqual(retrieved['some_name'], 'some_value')

    def test_saveConfig(self):
        config.getConfig()
        self.assertIsNone(config.saveConfig())
