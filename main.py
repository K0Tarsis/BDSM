import requests
import pandas as pd
import argparse

from bs4 import BeautifulSoup


class Parser:
    def __init__(self, url, headers):
        self.url = url
        self.headers = headers

    def pars_movie_paige(self):
        req = requests.get(self.url, headers=self.headers)
        src = req.text
        soup = BeautifulSoup(src, 'lxml')
        contant_main = soup.find(class_="b-content__main")
        title = contant_main.find(class_="b-post__title").text.rstrip().lstrip()
        original_title = contant_main.find(class_="b-post__origtitle").text.rstrip().lstrip()
        imdb = contant_main.find(class_="b-post__info_rates imdb").find('span').text.rstrip().lstrip()
        tr_list = contant_main.find_all("tr")

        for tr in tr_list:
            if "Страна" in tr.text:
                country = tr.find('a').text
                break
            else:
                country = "None"

        for tr in tr_list:
            if "Время" in tr.text:
                duration = tr.find_all('td')[-1].text.rstrip().lstrip()
                break
            else:
                duration = "None"

        description = contant_main.find(class_="b-post__description_text").text.rstrip().lstrip()

        content = {"Title": [title],
                   "Original_title": [original_title],
                   "IMDB": [imdb],
                   "Country": [country],
                   "Duration": [duration],
                   "Description": [description]}

        self.content = content
        return content

    def write_to_csv(self, name):
        if not name:
            name = "_".join(self.url.split('-')[1:])[:-5]
        pd_data = pd.DataFrame.from_dict(self.content)
        pd_data.to_csv(f'{name}.csv', index=True)

        return pd_data


def main(url, name):
    headers = {
        'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/'
            'avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
            ' Chrome/97.0.4692.71 Safari/537.36'
    }

    silicon_valley = Parser(url, headers)
    silicon_valley.pars_movie_paige()
    silicon_valley.write_to_csv(name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', type=str, default='https://rezka.ag/series/comedy/2040-kremnievaya-dolina-2014.html',
                        help='Url for movie page')
    parser.add_argument('--name', default='', help='Name for csv file')
    opt = parser.parse_args()
    main(opt.url, opt.name)
