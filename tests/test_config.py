import os
import unittest

from telegram_bot.config import ConfigSingleton, TOKEN, FACE_PP_API_KEY, FACE_PP_API_SECRET, RAPID_API_KEY, json_path


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.config = ConfigSingleton.get_instance()

    def test_config(self):
        self.assertTrue(TOKEN)
        self.assertTrue(FACE_PP_API_KEY)
        self.assertTrue(FACE_PP_API_SECRET)
        self.assertTrue(RAPID_API_KEY)
        self.assertTrue(os.path.exists(json_path))

    def test_config_class(self):
        self.assertTrue(hasattr(self.config, 'total_max_requests'))
        self.assertTrue(hasattr(self.config, 'current_requests'))
        self.assertTrue(hasattr(self.config, 'rapid_url'))
        self.assertTrue(hasattr(self.config, 'face_pp_url'))


if __name__ == '__main__':
    unittest.main()
