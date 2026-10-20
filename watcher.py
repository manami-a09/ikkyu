import os
import re
import requests

URL = "https://restaurant.ikyu.com/106791"
DATES = ["2027-01-09", "2027-01-16"]
PARTY = 4


def check(date):
    url = f"{URL}?visitDate={date}&visitorsCount={PARTY}"
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=20)
    r.raise_for_status()
    text = re.sub(r"\s+", " ", r.text)
    date_tokens = [date, date.replace("-", "/"), f"{int(date[5:7])}月{int(date[8:10])}日"]
    has_date = any(x in text for x in date_tokens)
    positive = any(x in text for x in ["予約する", "予約入力", "空席", "ランチ"])
    negative = any(x in text for x in ["現在、予約可能日はございません", "満席"])
    return has_date and positive and not negative, url


def main():
    found = []
    for date in DATES:
        ok, url = check(date)
        if ok:
            found.append(f"{date} {url}")
    if found:
        print("AVAILABILITY_FOUND")
        print("\n".join(found))
        with open("availability.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(found))
    else:
        print("No target availability detected")


if __name__ == "__main__":
    main()
