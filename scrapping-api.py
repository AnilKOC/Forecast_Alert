from flask import Flask
from flask_restful import Api, Resource
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import re

app = Flask(__name__)
api = Api(app)

class data(Resource):
    def get(self,url):
        global price
        global active
        global title
        baseURL = "https://www.investing.com/"
        newURL = re.sub("@","/",url)
        pasteURL = baseURL + newURL
        data = urlopen(Request(pasteURL, headers={'User-Agent': 'Mozilla'})).read()
        parse = BeautifulSoup(data)

        for last in parse.find_all('h1', class_="float_lang_base_1 relativeAttr"):
            self.title = last.text
        green_icon = re.findall("inlineblock greenClockBigIcon middle isOpen", str(parse))
        try:
            if green_icon[0] != None:
                print("Active!")
                for last in parse.find_all('span', id="last_last"):
                    liste = list(last)
                    print("Last price: " + str(liste[0]))
                    self.price = liste[0]
                    self.active = 1
        except:
            None

        red_icon = re.findall("inlineblock redClockBigIcon middle isOpen", str(parse))
        try:
            if red_icon[0] != None:
                print("Passive!")
                for last in parse.find_all('span', id="last_last"):
                    liste = list(last)
                    print("Close price: " + str(liste[0]))
                    self.price = liste[0]
                    self.active = 0
        except:
            None

        return {"title":self.title,"price": self.price, "active": self.active}

api.add_resource(data, "/data/<string:url>")

if __name__ == "__main__":
    app.run(debug=True)