from sys import stderr as perr
import requests
import simplejson
import copy
from time import sleep
import deeper.api.simapi
import deeper.api.simthread


class PublApi(deeper.api.simapi.SimpleApi):
    def __init__(self, delay, search_term, **kwargs):
        deeper.api.simapi.SimpleApi.__init__(self)
        self.setDelay(delay)
        self.setSearchTerm(search_term)
        self.setKwargs(kwargs)
        self.setSession(requests.session())
        self.setURL('http://dblp.org/search/publ/api')

    def callAPI(self, params):
        while True:
            try:
                resp = self.__session.get(self.__searchURL, params=params)
                re = resp.json()
                if 'hit' in re['result']['hits']:
                    return re['result']['hits']['hit']
                else:
                    return []
            except simplejson.scanner.JSONDecodeError:
                print >> perr, 'JSONDecodeError error!!!'
                sleep(self.__delay)
                continue
            except requests.ConnectionError:
                print >> perr, 'ConnectionError error!!!'
                sleep(self.__delay)
                continue

    def callMulAPI(self, queries):
        threads = []
        for query in queries:
            params = self.getKwargs()
            params[self.__searchTerm] = '+'.join(query)
            t = deeper.api.simthread.SimpleThread(self.callAPI, (params,), self.callAPI.__name__)
            threads.append(t)
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        mresult = []
        for t in threads:
            mresult.extend(t.getResult())
        return mresult

    def setDelay(self, delay):
        self.__delay = delay

    def getDelay(self):
        return self.__delay

    def setSearchTerm(self, search_term):
        self.__searchTerm = search_term

    def getSearchTerm(self):
        return self.__searchTerm

    def setKwargs(self, kwargs):
        self.__kwargs = kwargs
        self.__kwargs['format'] = 'json'

    def getKwargs(self):
        return copy.deepcopy(self.__kwargs)

    def setURL(self, url):
        self.__searchURL = url

    def getURL(self):
        return self.__searchURL

    def setID(self, client_id, client_secret):
        pass

    def getID(self):
        pass

    def getToken(self):
        pass

    def setToken(self):
        pass

    def setSession(self, session):
        self.__session = session

    def getSession(self):
        return self.__session
