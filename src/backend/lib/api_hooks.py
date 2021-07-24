#!/usr/bin/python
import requests
import json
# sys.path.insert(1, 'lib/')


class DuckDuckGo:
    """duckduckgo related searching"""

    def __init__(self):
        self.url = "https://api.duckduckgo.com/?q="

    def image_result(self, query):
        """
        Returns json containing url to image
        :param _key: &t=h_&iar=images&iax=images&ia=images&format=json&pretty=1
        """
        _key = "&t=h_&iar=images&iax=images&ia=images&format=json&pretty=1"
        breakpoint()
        try:
            query = query.string
        except AttributeError:
            query = query
        search_result = requests.get(self.url + query + _key)
        try:
            image_result = search_result.json()["Image"]
        except ValueError:
            image_result = ""
        if search_result.status_code == 200 and image_result != "":
            image = requests.get(search_result.json()["Image"], stream=True)
            image.raw.decode_content = True
            return image.raw
        else:
            return False

    def description_result(self, query):
        _key = "&format=json"
        try:
            query = query.string
        except AttributeError:
            pass
        try:
            _r = json.loads(requests.get(self.url + query + _key).text)
        except Exception as e:
            return None
        if len(_r["Results"]) == 0:
            return None
        else:
            try:
                return _r["Abstract"]
            except AttributeError:
                return None
            return _r.Results[0]
