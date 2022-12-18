import requests
import random
from bs4 import BeautifulSoup as bs

def getEnrollInfo(year : str, code : str) -> dict:
    """Scrape enrollment info from webreg.

    Args:
        year: the year and term of class
        code: code of class
    Returns:
        A list of enrollment max, enrolled, waitlist, and requested.

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
    data_dict = {}
    b_index = lst.index("Bookstore")
    data_dict["max_enroll"] = str(lst[b_index-5])
    data_dict["enroll"] = str(lst[b_index-4])
    data_dict["waitlist"] = str(lst[b_index-3])
    data_dict["requested"] = str(lst[b_index-2])
    return data_dict

def checkSpace(jsondata: dict) -> bool:
    """Check if space is available for enrollment.

    Args:
        lst: list of values from getEnrollmentInfo()
    Returns:
        A boolean with True is space is available and False else.

    """
    max_enroll = int(jsondata["max_enroll"])
    enroll = int(jsondata["enroll"])
    if max_enroll - enroll > 0:
        return True
    return False

def getYear() -> str:
    """Check for the newly updated course term.

    Args:
        None
    Returns:
        Current year and term

    """
    base_url = "https://www.reg.uci.edu/perl/WebSoc"
    headers = {"User-Agent": f"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.{random.randrange(99)} (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36"}
    # params = {}
    # params["YearTerm"] = year
    # params["Breadth"] = "GE-1A"
    
    response = requests.get(base_url, headers=headers)
    soup = bs(response.text, features="html.parser")
    r1 = soup.find('select').findChildren()
    result = ""
    for i in r1:
        text = i.string
        if "(Law)" not in text:
            if "Summer" not in text:
                result = text
                break
    year = result[0:4]
    tag = ""
    if "Winter" in result:
        tag = "-03"
    elif "Fall" in result:
        tag = "-92"
    elif "Spring" in result:
        tag = "-14"
    return f"{year}{tag}"

if __name__ == "__main__":
    y = getYear()
    print(y)
    x = getEnrollInfo(y, "35700")
    print(x) #dict of data
    b = checkSpace(x)
    print(b) #bool