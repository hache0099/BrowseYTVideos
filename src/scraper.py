from dataclasses import dataclass, fields
from SafeRequest.SafeRequest import safe_request

@dataclass
class MySearchResult:
	videoId: str
	title: str
	lenVid: int
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
        results_cls = [_from_dict(d) for d in results]
        return results_cls


def change_key(d : dict, old_key: str, new_key: str) -> None:
#	print(d)
	d[new_key] = d.pop(old_key)



def _from_dict(search_result):
#	print(f"{search_result=}")
	change_key(search_result, "lengthSeconds", "lenVid")
	cls_vars = {f.name for f in fields(MySearchResult)}
	filtered_vars = {k : v for k, v in search_result.items() if k in cls_vars}
	
#	print(f"{filtered_vars=}")
#	tmp = filtered_vars["lengthSeconds"]
#	filtered_vars["lengthSeconds"] = int(tmp)
	
	return MySearchResult(**filtered_vars)
	

# Esta sección es sólo para pruebas del módulo
"""
def main():
	sc = YTScraper()
#	print(sc("doki doki waku waku"))
	result_list = sc("doki doki waku waku")
	print(result_list)
	result_cls_list = [_from_dict(MySearchResult, d) for d in result_list]
	
	print(result_cls_list)

if __name__ == "__main__":
    main()
"""
