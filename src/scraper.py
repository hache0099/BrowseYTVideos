from dataclasses import dataclass, fields
from SafeRequest.SafeRequest import safe_request

@dataclass
class MySearchResult:
	videoId: str
	title: str
	lengthSeconds: int
	author: str


class YTScraper:
    def __init__(self,yt_link = "https://vid.puffyan.us/api/v1/search"):
        self.yt_link = yt_link
    

    def _get_result(self, request):
        new_req = request.replace(" ", "+")
#        print(new_req)
        params ={
                "q": new_req,
                "type": "video",
                "pretty": 1,
                "fields": "videoId,title,lengthSeconds,author",
                }
        results = safe_request(self.yt_link, Data=params)

        return results
    

    def __call__(self, request):
        results = self._get_result(request)
        return results

def _from_dict(cls, search_result):
#	print(f"{search_result=}")
	cls_vars = {f.name for f in fields(cls)}
	filtered_vars = {k : v for k, v in search_result.items() if k in cls_vars}
	print(f"{filtered_vars=}")
	tmp = filtered_vars["lengthSeconds"]
	filtered_vars["lengthSeconds"] = int(tmp)
	
	return cls(**filtered_vars)
	

# Esta sección es sólo para pruebas del módulo
def main():
	sc = YTScraper()
#	print(sc("doki doki waku waku"))
	result_list = sc("doki doki waku waku")
	print(result_list)
	result_cls_list = [_from_dict(MySearchResult, d) for d in result_list]
	
	print(result_cls_list)

if __name__ == "__main__":
    main()