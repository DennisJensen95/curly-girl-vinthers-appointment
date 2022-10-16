# Standard library
import unittest
import os

# Module to test
import curly_db
from main import is_post_too_old


class TestCurlyDb(unittest.TestCase):
    database_path = "/tmp/curly_girl_test_db.json"

    def setUp(self) -> None:
        print("Setup of test")
        self.db = curly_db.initialize_database(self.database_path)

    def tearDown(self) -> None:
        print("Teardown of test")
        self.db.deleteAll()
        os.system(f"rm -rf {self.db.filename}*")

    def test_inserting_post(self):
        # 1
        # Insert random post text and check if it is there afterwards
        post_text = "Afbud! Der er kommet en tid på mandag bla bla bla."
        post_id = curly_db.save_post(post_text=post_text, db=self.db)
        self.assertEqual(post_text, self.db.getByQuery(
            {"id_post": post_id})[0]["post_text"])

        # 2
        # Inserting identical post and only one entry should be there.
        post_id = curly_db.save_post(post_text=post_text, db=self.db)
        self.assertTrue(len(self.db.getByQuery({"id_post": post_id})) == 1)

    def test_getting_timestamp(self):
        # 1
        # Timestamp here and now
        post_text = "Afbud! Der er kommet en tid på mandag bla bla bla."
        post_id = curly_db.save_post(post_text=post_text, db=self.db)
        time_stamp = curly_db.get_post_timestamp(post_id, self.db)
        self.assertTrue(not is_post_too_old(10, time_stamp))

        # 2
        # Make sure it is the current time which is timestamped.
        self.assertTrue(is_post_too_old(0, time_stamp))
