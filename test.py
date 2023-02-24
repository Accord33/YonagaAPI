from bs4 import BeautifulSoup as bs
import pandas as pd
with open("data.html", "r") as f:
    data = f.read()
soup = bs(data, "html.parser")
dismissible = soup.select("#dismissible")
titles = [dismissible[i].find("yt-formatted-string").string for i in range(len(dismissible))]
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