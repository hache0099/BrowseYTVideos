import sys

sys.path.append("../src")

from scraper import YTScraper, MySearchResult

def main():
	sc = YTScraper()
#	print(sc("doki doki waku waku"))
	result_list = sc("doki doki waku waku")
#	print(result_list)
	
	for result in result_list:
		assert isinstance(result, MySearchResult)
		assert isinstance(result.lenVid, int)
		
		print(result)
	# result_cls_list = [_from_dict(d) for d in result_list]
	
	# print(result_cls_list)


if __name__ == "__main__":
    main()
