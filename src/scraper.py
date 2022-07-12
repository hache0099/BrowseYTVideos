import re
from urllib.parse import quote_plus
from dataclasses import dataclass, fields
from custom_exceptions import InvalidQueryError
from easy_request import safe_request

@dataclass
class MySearchResult:
	videoId: str
	title: str
	lenVid: int
	author: str


# ~ class InvalidQueryError(Exception):
    # ~ pass


class YTScraper:
    def __init__(self, yt_link=None):
        # ~ super().__init__(self)
        if yt_link is None:
            self.yt_link = "https://vid.puffyan.us/api/v1/search"
        else:
            self.yt_link = yt_link
    

    def _get_result(self, request):
        print("calling _get_result...")
        # ~ new_req = _replace_chr(request)
        new_req = quote_plus(request)
#        print(new_req)
        params ={
                "q": new_req,
                "type": "video",
                "pretty": 1,
                "fields": "videoId,title,lengthSeconds,author",
                }
        results = safe_request(self.yt_link, Data=params)

        return results
    
    
    def _make_call(self, request):
        if not _check_query(request) or len(request) == 0: 
            raise InvalidQueryError("Búsqueda no válida")
        
        results = self._get_result(request)
        results_cls = tuple(_from_dict(d) for d in results)
        return results_cls
    

    def __call__(self, *args):
        print("YTScraper args:", args)
        results = self._make_call(args[0])
        
        return results


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
    
    for key, val in replace_dict.items():
        new_query = new_query.replace(key,val)
    
    return new_query


def _change_key(d : dict, old_key: str, new_key: str) -> None:
#	print(d)
    d[new_key] = d.pop(old_key)


def _from_dict(search_result):
#	print(f"{search_result=}")
    _change_key(search_result, "lengthSeconds", "lenVid")
    search_result["lenVid"] = _secs_to_min(search_result["lenVid"])
    
    cls_vars = {f.name for f in fields(MySearchResult)}
    filtered_vars = {k : v for k, v in search_result.items() if k in cls_vars}

    #	print(f"{filtered_vars=}")
    #	tmp = filtered_vars["lengthSeconds"]
    #	filtered_vars["lengthSeconds"] = int(tmp)

    return MySearchResult(**filtered_vars)
	

def _secs_to_min(s:int) -> str:
    mins, secs = divmod(s,60)
    
    return "{:02d}:{:02d}".format(mins,secs)
