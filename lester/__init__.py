"""
Create setup.py for PyPi listing
"""
from .app import App
from .room import Room
from .item import Item
from .action import Action


def lester_init(download_check=False):
    if download_check:  # Make sure nltk is up to date
        __download_nltk()


# Export all Classes that a user will need to use Lester
__all__ = ['App', 'Room', 'Item', 'Action', 'lester_init']


def __download_nltk():
    import nltk as __nltk

    # TODO: Check if these can be skipped automatically if they already exist
    __nltk.download('wordnet')
    __nltk.download('brown')
