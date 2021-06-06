import requests
import json
import time
import platform    # For getting the operating system name
import subprocess  # For executing a shell command



S = requests.Session()
URL = "https://en.wikipedia.org/w/api.php"

class Utils():

    def __init__(self):
        self.category2id = {}
        self.id2article = {}

    '''
    Function to check if the server is active
    '''
    def ping(self, host):
        """
        Returns True if host (str) responds to a ping request.
        Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
        """

        # Option for the number of packets as a function of
        param = '-n' if platform.system().lower()=='windows' else '-c'

        # Building the command. Ex: "ping -c 1 google.com"
        command = ['ping', param, '1', host]

        return subprocess.call(command) == 0


    '''
    Function that returns the title of given ID
    '''
    def get_title_from_id(self, id):

        PARAMS = {
            "action" : "query",
            "prop" : "info", 
            "format":"json",
            "pageids" : id,
        }
        
        try:
            R = S.get(url=URL, params=PARAMS)
            data = R.json()
        except:
            time.sleep(600)
            R = S.get(url=URL, params=PARAMS)
            data = R.json()
        
        try:
            return list(data["query"]["pages"].values())[0]["title"]
        except:
            print("Title not found for:", id)
            return "None"

    '''
    Function that returns the ID of a given title
    '''
    def get_id_from_title(self, title):

        PARAMS = {
            "action" : "query",
            "prop" : "info", 
            "format":"json",
            "titles" : title,
        }
        try:
            R = S.get(url=URL, params=PARAMS)
            data = R.json()
        except:
            time.sleep(600)
            R = S.get(url=URL, params=PARAMS)
            data = R.json()

        return (list(data["query"]["pages"].keys())[0])