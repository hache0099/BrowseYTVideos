import sys

sys.path.append("../src")

from scraper import YTScraper, MySearchResult

def main():
	sc = YTScraper()
	result_list = sc("doki doki waku waku")
#	print(result_list)
	
	for result in result_list:
		assert isinstance(result, MySearchResult)
		assert isinstance(result.lenVid, int)
		
		print(result)


if __name__ == "__main__":
    main()
