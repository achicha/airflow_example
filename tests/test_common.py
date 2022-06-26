import os
import pytest
from pathlib import Path
from dags.utils.common import read_file


@pytest.fixture()
def common_read_file():
    file_ = os.path.join(Path(__file__).parent.parent.resolve(), 'data', 'twitter_urls.txt')
    return read_file(file_)


def test_read_file(common_read_file):
    assert isinstance(common_read_file, list)
    assert common_read_file[0] == 'https://twitter.com/elonmusk'
