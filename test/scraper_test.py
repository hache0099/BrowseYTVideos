import sys

sys.path.append("../src")

from scraper import YTScraper, _from_dict

def main():
	sc = YTScraper()
#	print(sc("doki doki waku waku"))
	result_list = sc("doki doki waku waku")
	print(result_list)
	result_cls_list = [_from_dict(d) for d in result_list]
	
	print(result_cls_list)


if __name__ == "__main__":
    main()
