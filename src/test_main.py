# Standard library
import unittest
from datetime import datetime, timedelta

# Module being tested
from main import identify_cancellation, is_post_too_old


class TestMain(unittest.TestCase):
    def test_identifying_positiv_cancellation(self):
        post_text = "Afbud! Der er kommet en tid på mandag bla bla bla."
        is_canellation_post = identify_cancellation(post_text)
        self.assertTrue(is_canellation_post)

        post_text = "afbudstid i min dag"
        is_canellation_post = identify_cancellation(post_text)
        self.assertTrue(is_canellation_post)

    def test_identifying_negative_cancellation(self):
        post_text = """Så er der nyhed fra innersense Du kan nu købe en
                    Collection og spare 25% af normal prisen! Du får shampoo,
                    Balsam, leave in og detox maske - alt du skal bruge for at
                    komme i gang 😍"""
        is_canellation_post = identify_cancellation(post_text)
        self.assertFalse(is_canellation_post)

    def test_is_post_too_old(self):
        now = datetime.now()
        post_time = now - timedelta(minutes=5)
        self.assertFalse(is_post_too_old(10, post_time))
        self.assertTrue(is_post_too_old(3, post_time))


if __name__ == '__main__':
    unittest.main()
