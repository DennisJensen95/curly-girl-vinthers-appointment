"""Interface for saving curly girl posts and artifacts
"""

# Standard library
from hashlib import sha256
from datetime import datetime
import os

# Third party libraries
import pysondb


DATEFORMAT = "%d/%m/%Y-%H:%M:%S"


def initialize_database(database_path: str = f"{os.getcwd()}/curlygirl.json") -> pysondb.db.JsonDatabase:
    """Initialize pysondb

    Args:
        database_path (str, optional): Path to database. Defaults to "CURRENT_DIR/curlygirl.json".

    Returns:
        pysondb.db: database object.
    """
    return pysondb.db.getDb(database_path)


def save_post(post_text: str, db: pysondb.db.JsonDatabase):
    """Save post to database

    Args:
        post_text (str): Text of the post saved.
        db (pysondb.db): Database being saved to.

    Returns:
        id (str): Id of the post.
    """
    id_sha256 = compute_post_id(post_text)

    if db.getByQuery({"id_post": id_sha256}):
        return id_sha256

    db.add({"post_text": post_text, "time": datetime.now().strftime(
        DATEFORMAT), "id_post": f"{id_sha256}"})
    return id_sha256


def compute_post_id(post_text: str):
    return sha256(post_text.encode()).hexdigest()


def get_post_timestamp(post_id: str, db: pysondb.db.JsonDatabase):
    post = db.getByQuery({"id_post": post_id})
    if len(post) != 1:
        assert "Multiple entries with the same id should not be possible"

    return datetime.strptime(post[0]["time"], DATEFORMAT)
