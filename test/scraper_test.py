import sys

sys.path.append("../src")

import pytest
from custom_exceptions import InvalidQueryError, RequestError
from scraper import YTScraper, MySearchResult

sc = YTScraper()


def test_first():
    result_list = sc("doki doki waku waku")
    #	print(result_list)

    assert isinstance(result_list,tuple)
    for result in result_list:
        assert isinstance(result, MySearchResult)
        assert isinstance(result.lenVid, int)

        print(result)


def test_exception():
    with pytest.raises(InvalidQueryError):
        for i in range(10):
            res_list = sc(" " * i)


def test_no_connectivity():
    with pytest.raises(RequestError):
        result_list = sc("doki doki waku waku")
