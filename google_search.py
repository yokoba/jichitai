import requests
import csv
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import random


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
}


with open("pref_code.csv", mode="r", encoding="utf-8") as f:
    data = list(csv.DictReader(f))

PREF_CODE = {item["pref"]: f"{int(item['code']):02d}" for item in data}


def get_content(target):
    url = target["url"]

    res = requests.get(url, headers=HEADERS)

    region_code = PREF_CODE[target["region"]] if PREF_CODE.get(target["region"], None) is not None else PREF_CODE["北海道"]

    p = Path("./search_log/").joinpath(region_code + "_" + target["region"]).joinpath(target["city"])
    p.mkdir(exist_ok=True, parents=True)

    with open(str(p.joinpath("site.html")), mode="bw") as f:
        f.write(res.content)

    headers = [f"{key:30}: {value}" for key, value in res.headers.items()]

    with open(str(p.joinpath("header.txt")), mode="w") as f:
        for header in headers:
            f.write(header + "\n")

    return True, target


def main():
    with open("site_list.csv", mode="r", encoding="utf_8_sig") as f:
        data = list(csv.DictReader(f))

    random_data = random.sample(data, len(data))
    # get_content(random_data[0])

    results = []

    with ThreadPoolExecutor() as executor:
        for target in random_data:
            results.append(executor.submit(get_content, target))
            time.sleep(0.1)

    for result in as_completed(results):
        print(result.result())


if __name__ == "__main__":
    main()
