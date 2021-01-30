import re
import requests
import urllib.robotparser
from collections import defaultdict
from urllib.parse import urlparse, urldefrag
from bs4 import BeautifulSoup

# testing purposes + solutions to question 1
url_set = set()

### Saving the list of text words in a separate file just in case
### the program crashes and the list of words get gone
### opening and closing textlist.txt if it already exists
### this will overwrite and erase the previous content
tmp = open('textlist.txt', 'w')
tmp.close()

### And we'll have a global dictionary as well
### But we have a backup as a file as well
frequency = defaultdict(int)


def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]


def extract_next_links(url, resp):
    # Implementation required.
    output = set()
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    
    # check if soup is high quality
    # find all unique words in the soup that are of length 3+
    soup_text = [_ for _ in re.sub('[^A-Za-z0-9]+', ' ', soup.get_text().lower()).split() if len(_) > 2]
    
    # define high quality soup to be 200+ unique words
    # account for if the response status is 200 but has no text
    if len(set(soup_text)) <= 200 or (resp.status == 200 and set(soup_text) == set()):
        return []

    ########## SimHash Implementation HERE ##########

    #################################################

    for link in soup.find_all('a', href=True):
        output.add(urldefrag(link.attrs.get('href'))[0])
        
    # debugging
    # print(soup_text)
    # print(frequency)
    
    return list(output)


def crawlable(url, parsed):
    # check robots.txt
    try:
        netloc = "https://" + parsed.netloc + "/robots.txt"
        site = requests.get(netloc)
        
        permission = urllib.robotparser.RobotFileParser()
        permission.set_url(netloc)
        permission.read()

        return permission.can_fetch("*", url)
    
    # no robots.txt
    except:
        return False


def is_trap(parsed):
    parsed_url = parsed.geturl()
    # long urls
    if len(parsed_url) >= 200:
        return True

    # calendars
    if re.match(r".*(calendar).?$", parsed_url):
        return True

    # disallowed websites
    if re.match(r".*(wics.ics.uci.edu/events|evoke.ics.uci.edu).?$", parsed_url):
        return True
    
    # very large files ??
    # can't do much with the parsed urls only; need the actual content


def is_valid(url):
    try:
        parsed = urlparse(url)

        if parsed.scheme not in set(["http", "https"]):
            return False

        # check domain
        if url.find("ics.uci.edu/") == -1 and url.find("cs.uci.edu/") == -1 \
            and url.find("informatics.uci.edu/") == -1 and url.find("stat.uci.edu/") == -1 \
            and url.find("today.uci.edu/department/information_computer_sciences/") == -1:
            return False

        # check robots.txt
        if not crawlable(url, parsed):
            return False

        # check trap
        if is_trap(parsed):
            return False

        # check duplicates
        if url in url_set:
            return False

        if re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv|thesis"
            + r"|z|aspx|mpg|mat|pps|bam|ppsx"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz|war|apk)$", parsed.path.lower()):
            return False
        
        record_information(url)
        
        return True

    except TypeError:
        print ("TypeError for ", parsed)
        raise

# record information here because we know that the url is a valid url to be downloaded from.
# unfortunately takes a lot of time so a better implementation on how to record the information
# would be very much appreciated
def record_information(url):
    global url_set, frequency    

    url_set.add(url)
    print("CURRENT URL_COUNT: {}".format(len(url_set)))

    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    soup_text = [_ for _ in re.sub('[^A-Za-z0-9]+', ' ', soup.get_text().lower()).split() if len(_) > 2]

    for word in soup_text:
        frequency[word] += 1

    with open('textlist.txt', 'w') as f:
        for k, v in sorted(frequency.items(), key=lambda item: (-item[1], item[0])):
            f.writelines("{} -> {}\n".format(k, v))
