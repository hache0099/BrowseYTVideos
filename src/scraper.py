import re
from dataclasses import dataclass, fields
from SafeRequest.SafeRequest import safe_request

@dataclass
class MySearchResult:
	videoId: str
	title: str
	lenVid: int
	author: str


class InvalidQueryError(Exception):
    pass


class YTScraper:
    def __init__(self,yt_link = "https://vid.puffyan.us/api/v1/search"):
        self.yt_link = yt_link
    

    def _get_result(self, request):
        new_req = _replace_chr(request)
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
        if not check_query(request):
            raise InvalidQueryError()
        
        results = self._get_result(request)
        results_cls = [_from_dict(d) for d in results]
        return results_cls


def _check_query(query: str) -> bool:
    # Quizás deba añadir más en el futuro
    regex_checks = (
    r"^(?!\s+$)",
    )
    for r in regex_checks:
        if re.match(r, query):
            return True
    
    return False


def _replace_chr(query: str) -> str:
    new_query = query
    replace_dict = {
        "+": "%2B",
        "%": "%25",
        "/": "%2F",
    }
    
    for key, val in replace_dict.items():s
        new_query = new_query.replace(key,val)
    
    return new_query


def _change_key(d : dict, old_key: str, new_key: str) -> None:
#	print(d)
    d[new_key] = d.pop(old_key)



def _from_dict(search_result):
#	print(f"{search_result=}")
    _change_key(search_result, "lengthSeconds", "lenVid")
    cls_vars = {f.name for f in fields(MySearchResult)}
    filtered_vars = {k : v for k, v in search_result.items() if k in cls_vars}

    #	print(f"{filtered_vars=}")
    #	tmp = filtered_vars["lengthSeconds"]
    #	filtered_vars["lengthSeconds"] = int(tmp)

    return MySearchResult(**filtered_vars)
	
