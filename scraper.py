from bs4 import BeautifulSoup
from SafeRequest.SafeRequest import safe_request


class YTScraper:
    def __init__(self,yt_link = "https://vid.puffyan.us/api/v1/search"):
        self.yt_link = yt_link
    

    def _get_result(self, request):
        new_req = request.replace(" ", "+")
#        print(new_req)
        params ={
                "q": new_req,
                "pretty": 1,
                "fields": "videoId,title,lengthSeconds,author",
                }
        results = safe_request(self.yt_link, Data=params)

        return results
    

    def __call__(self, request):
        results = self._get_result(request)
#        parsed = BeautifulSoup(results, "html.parser")
        return results


# Esta sección es sólo para pruebas del módulo
def main():
    sc = YTScraper()
    print(sc("doki doki waku waku"))

if __name__ == "__main__":
    main()
