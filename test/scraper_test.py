import sys

sys.path.append("../src")

import pytest
from scraper import YTScraper, MySearchResult, InvalidQueryError

sc = YTScraper()


def test_first():
    result_list = sc("doki doki waku waku")
    #	print(result_list)

    for result in result_list:
        assert isinstance(result, MySearchResult)
        assert isinstance(result.lenVid, int)

        print(result)


def test_exception():
    with pytest.raises(InvalidQueryError):
        for i in range(10):
            res_list = sc(" " * i)


