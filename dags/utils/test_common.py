from common import read_file


file_ = '/Users/andreyev/Documents/Github/airlfow_example/data/twitter_urls.txt'

assert isinstance(read_file(file_), list)
assert read_file(file_)[0] == 'https://twitter.com/elonmusk'
