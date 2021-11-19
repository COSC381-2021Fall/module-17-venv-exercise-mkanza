import requests
from bs4 import BeautifulSoup as Soup
import pandas as pd
import numpy as np

urls = ['https://www.shakespeare.org.uk/explore-shakespeare/shakespedia/shakespeare-quotes-theme/funny-shakespeare-quotes/',
        'https://www.shakespeare.org.uk/explore-shakespeare/shakespedia/shakespeare-quotes-theme/shakespeare-quotes-anger/',
        'https://www.shakespeare.org.uk/explore-shakespeare/shakespedia/shakespeare-quotes-theme/shakespeare-quotes-life/',
        'https://www.shakespeare.org.uk/explore-shakespeare/shakespedia/shakespeare-quotes-theme/shakespeare-quotes-marriage/',
        'https://www.shakespeare.org.uk/explore-shakespeare/shakespedia/shakespeare-quotes-theme/shakespeare-quotes-friendship/']
data = []
with requests.Session() as client:
    for url in urls:
        resp = client.get(url)
        soup = Soup(resp.text, 'html.parser')
        for block in soup.find_all("blockquote"):
            quote = block.find("p").text
            name, citation = block.find("cite").text.split(",", 1)
            name = name.split(" ", 1)[-1]
            citation = citation.split(",")[0].strip()
            try:
                act, scene = [int(i) for i in citation.split() if i.isnumeric()]
            except ValueError:
                act, scene = np.nan, np.nan
            data.append([quote, name, act, scene])


data = pd.DataFrame(dict(zip(["quote", "title", "act", "scene"], zip(*data))))
data.to_csv("result.csv")