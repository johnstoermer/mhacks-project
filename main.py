from flask import Flask
app = Flask(__name__)
import requests
from lxml import html
from flask.json import jsonify

URL = 'http://www.ratemyprofessors.com/'

def getProf(q):
    try:
        urlSearch = URL + 'search.jsp?query=' + q
        page = requests.get(urlSearch)
        tree = html.fromstring(page.content)
        href = tree.xpath('//*[@id="searchResultsBox"]/div[2]/ul/li/a')[0].attrib['href']
        urlProf = URL + href
        page = requests.get(urlProf)
        tree = html.fromstring(page.content)
        #main
        name = tree.xpath('//*[@id="mainContent"]/div[1]/div[1]/div[2]/div[1]/div[2]/h1/span[1]/text()')[0].strip() + ' ' + tree.xpath('//*[@id="mainContent"]/div[1]/div[1]/div[2]/div[1]/div[2]/h1/span[2]/text()')[0].strip() + ' ' + tree.xpath('//*[@id="mainContent"]/div[1]/div[1]/div[2]/div[1]/div[2]/h1/span[3]/text()')[0].strip()
        rating = tree.xpath('//*[@id="mainContent"]/div[1]/div[3]/div[1]/div/div[1]/div/div/div/text()')[0].strip()
        takeagain = tree.xpath('//*[@id="mainContent"]/div[1]/div[3]/div[1]/div/div[2]/div[1]/div/text()')[0].strip()
        difficulty = tree.xpath('//*[@id="mainContent"]/div[1]/div[3]/div[1]/div/div[2]/div[2]/div/text()')[0].strip()
        #reviews
        dates = tree.xpath('//*[starts-with(@id, "")]/td[1]/div[1]/text()')
        classes = tree.xpath('//*[starts-with(@id, "")]/td[2]/span[1]/span/text()')
        qualities = tree.xpath('//*[starts-with(@id, "")]/td[1]/div[2]/div[2]/div[1]/div/span[1]/text()')
        difficulties = tree.xpath('//*[starts-with(@id, "")]/td[1]/div[2]/div[2]/div[2]/div/span[1]/text()')
        comments = tree.xpath('//*[starts-with(@id, "")]/td[3]/p/text()')
        profDict = {'name': name, 'rating': rating, 'takeagain': takeagain, 'difficulty': difficulty, 'url': urlProf, 'reviews': []}
        for i in range(len(comments)):
            dict = {'date': dates[i][1:], 'class': classes[i], 'quality': qualities[i], 'difficulty': difficulties[i], 'comment': comments[i][22:-18]}
            profDict['reviews'].append(dict)
        return profDict
    except:
        return None

@app.route("/<string:q>", methods=['GET'])
def return_prof(q):
    return jsonify(getProf(q))

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
