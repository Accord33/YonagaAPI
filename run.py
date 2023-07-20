from flask import Flask, render_template, request
import flask
import pandas as pd
from janome.tokenizer import Tokenizer
from bs4 import BeautifulSoup as bs
import pandas as pd
tokenizer = Tokenizer("custom_dict.csv")

app = Flask(__name__)

@app.route("/", methods=["GET"])
def search():
    req = request.args.get("text")
    
    if req == None:
        req = ""
    tokens = list()
    for token in tokenizer.tokenize(req):
        tokens.append(token.surface)
    tokens = [i for i in tokens if i != "*" and i != "\u3000" and i != " "]
    data = pd.read_csv("data.csv")
    for j in tokens:
        print(j)
        data = data.query(f'title.str.contains("{j}")', engine='python')
    num = len(data["Unnamed: 0"])
    
    return render_template("search.html", req=data, num=num)


def reload_csv():
    with open("data.html", "r") as f:
        data = f.read()
    soup = bs(data, "html.parser")
    dismissible = soup.select("#dismissible")
    titles = [i.get_text() for i in soup.find_all(id="video-title")]
    urls = ["https://youtube.com"+str(dismissible[i].a.get("href")) for i in range(len(dismissible))]
    thumbnails = [dismissible[i].find("img").attrs['src'] for i in range(len(dismissible))]
    times = [dismissible[i].find("span",class_="ytd-thumbnail-overlay-time-status-renderer").string.replace("\n", "").replace("  ", "") for i in range(len(dismissible))]
    datas = {
        'title': titles,
        'url': urls,
        'thumbnail': thumbnails,
        "time":times
    }
    df = pd.DataFrame(datas)
    df.to_csv("data.csv")
    print("Reloaded csv")

if __name__ == "__main__":
    reload_csv()
    app.run(port=8889, debug=False, host="0.0.0.0")
