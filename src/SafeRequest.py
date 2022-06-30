import requests


class RequestException(Exception):
    pass


def safe_request(
    url, req_type="GET", Data=None, return_resp=False, time_out=10, **kwargs
):
    try:
        resp = requests.request(req_type.upper(), url, params=Data, timeout=time_out)

        resp.raise_for_status()

    except (
        requests.exceptions.Timeout,
        requests.exceptions.HTTPError,
        requests.exceptions.ConnectionError,
    ) as e:
        raise RequestException(*e.args)
    # ~ except :
    # ~ code = resp.status_code
    # ~ print(f"Bad Request ({code=})")
    # ~ return
    # ~ except requests.exceptions.ConnectionError as e:
    # ~ print("No se ha podido establecer la conexión")
    else:
        if return_resp:
            return resp

        try:
            return resp.json()
        except:
            return resp.text
