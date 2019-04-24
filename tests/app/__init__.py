import os
import unittest
from pathlib import Path

from app.setup import create_app


class AppContextTestCase(unittest.TestCase):
    test_data_path = Path(__file__).parent.parent.joinpath('test_data')

    def setUp(self):
        os.environ['APP_SETTINGS'] = 'TestingConfig'
        self.app = create_app()
        self.test_client = self.app.test_client()
