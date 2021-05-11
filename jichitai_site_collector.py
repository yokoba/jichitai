import requests
from bs4 import BeautifulSoup
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
}


BASE_URL = "https://www.j-lis.go.jp"


def get_city(url, pref, region):
    time.sleep(1)
    res = requests.get(url, headers=HEADERS)

    soup = BeautifulSoup(res.content, "html.parser")
    table = soup.select("table[class='listtbl']")[1]
    link_list = table.select("a")

    site_list = []

    for link in link_list:
        href = link["href"]
        name = link.text

        site = (href, pref, region, name)

        site_list.append(site)

    return site_list


def get_region(url, pref):
    time.sleep(1)
    res = requests.get(url, headers=HEADERS)

    soup = BeautifulSoup(res.content, "html.parser")
    h3 = soup.select("h3")

    site_list = []

    for h in h3:
        href = BASE_URL + h.select_one("a")["href"]
        region = h.select_one("a").text

        site = get_city(href, pref, region)

        site_list.extend(site)

    return site_list


def get_pref(html):
    soup = BeautifulSoup(html, "html.parser")
    pref_li = soup.select("li[class='genrelist_genre2']")

    site_list = []

    for li in pref_li:
        href = BASE_URL + li.select_one("a")["href"]
        name = li.select_one("a").text

        site = get_region(href, name)

        site_list.extend(site)

    return site_list


def main():
    TOP = "https://www.j-lis.go.jp/spd/map-search/cms_1069.html"
    res = requests.get(TOP, headers=HEADERS)

    with open("top.html", mode="bw") as f:
        f.write(res.content)

    site_list = get_pref(res.content)

    header = "url,pref,region,city"
    with open("site_list.csv", mode="w", encoding="utf-8") as f:
        f.write(header + "\n")
        for line in site_list:
            site = ",".join(line) + "\n"
            f.write(site)


if __name__ == "__main__":
    main()
