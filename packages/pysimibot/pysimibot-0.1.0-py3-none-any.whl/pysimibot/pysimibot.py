

class Simsimi():
    def __init__(self):
        self._lang = None

        
    def _set_lang(self, language):
        self._lang = language

    def Talk(self, text):
        import requests
        import json

        data = text
        url = f'https://api-sv2.simsimi.net/v2/?text={data}&lc={self._lang}&cf=false'
        req = requests.get(url)
        data = req.json()
        return data['success']
    lang = property(fset=_set_lang) 

