import nltk
from nltk.tokenize import sent_tokenize
import sys

# Ensure the path to nltk_data is added
nltk.data.path.append('/home/jimmychestnut/nltk_data')
nltk.download('punkt')

# Print the system path
print(sys.path)

text = "This is a test. It should tokenize sentences correctly."
print(sent_tokenize(text))
