"""
Create setup.py for PyPi listing
"""

import nltk

# TODO: Check if these can be skipped automatically if they already exist
nltk.download('wordnet')
nltk.download('brown')
