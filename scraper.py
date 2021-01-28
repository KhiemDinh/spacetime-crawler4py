import re
import requests
import urllib.robotparser
from urllib.parse import urlparse
from bs4 import BeautifulSoup

def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]


def extract_next_links(url, resp):
    # Implementation required.
    output = set()
    soup = BeautifulSoup(requests.get(url).content, 'html.parser')
    for link in soup.find_all('a'):
        output.add(link.attrs.get('href'))
    return list(output)


def crawlable(url, parsed):
    # check robots.txt
    try:
        netloc = "https://" + parsed.netloc + "/robots.txt"
        site = requests.get(netloc)
        
        if site.status_code != 200:
            return False
        
        permission = urllib.robotparser.RobotFileParser()
        permission.set_url(netloc)
        permission.read()

        return permission.can_fetch("*", url)
    
    # no robots.txt
    except:
        return False


def is_valid(url):
    try:
        parsed = urlparse(url)

        if parsed.scheme not in set(["http", "https"]):
            return False

        # check domain
        if url.find('informatics.uci.edu/') == -1 and \
                 url.find("today.uci.edu/department/information_computer_sciences/") == -1:
            return False

        # check robots.txt
        if not crawlable(url, parsed):
            return False

        # check trap

        # check quality

        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise

