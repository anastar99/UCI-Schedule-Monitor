import requests
import random
from bs4 import BeautifulSoup as bs

def getEnrollInfo(year : str, code : str) -> list[int]:
    """Scrape enrollment info from webreg.

    Args:
        year: the year and term of class
        code: code of class
    Returns:
        A list of enrollment max, enrollend, waitlist, and requested.

    """
    base_url = "https://www.reg.uci.edu/perl/WebSoc"
    headers = {"User-Agent": f"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.{random.randrange(99)} (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36"}
    params = {}
    params["YearTerm"] = year
    params["CourseCodes"] = code
    
    response = requests.get(base_url, params=params, headers=headers)
    soup = bs(response.text, features="html.parser")
    r1 = soup.find(valign='top', bgcolor='#FFFFCC').findChildren()

    lst = []
    for i in r1:
        lst.append(i.string)

    b_index = lst.index("Bookstore")
    max_enroll = lst[b_index-6]
    enroll = lst[b_index-5]
    waitlist = lst[b_index-4]
    requested = lst[b_index-3]
    return [max_enroll, enroll, waitlist, requested]

if __name__ == "__main__":
    x = getEnrollInfo("2023-03", "35700")
    print(x)