import re
import requests
import urllib.robotparser
from urllib.parse import urlparse
from bs4 import BeautifulSoup

# testing purposes
url_count = 0
url_set = set()

# Saving the list of text words in a separate file just in case
# the program crashes and the list of words get gone
# opening and closing textlist.txt if it already exists
# this will overwrite and erase the previous content
tmp = open('textlist.txt', 'w')
tmp.close()

# And we'll have a global dictionary as well
# But we have a backup as a file as well
frequency = {}


def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]


def extract_next_links(url, resp):
    # Implementation required.
    output = set()
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    
    # check if soup is high quality
    # find all unique words in the soup that are of length 3+
    soup_text = set([_ for _ in re.sub('[^A-Za-z0-9]+', ' ', soup.get_text().lower()).split() if len(_) > 2])
    # define high quality soup to be 200+  unique words
    if len(soup_text) <= 200:
        return []

    for link in soup.find_all('a', href=True):
        output.add(link.attrs.get('href'))
        
    # debugging
    
    # print(soup_text)
    
    ### Creating a collection of text files
    
    with open('textlist.txt', 'a') as f: # keeps appending
        f.writelines("%s\n" % word for word in soup_text)
        
    ### as well as our global dictionoary for later convinence
    
    for word in soup_text:
        if word not in frequency: frequency[word] = 1
        else: frequency[word] += 1
    
    print(frequency)
    
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


def is_trap(parsed):
    # long urls
    if len(parsed.geturl()) >= 200:
        return True

    # calendars
    if re.match(r".*(/calendar).?$", parsed.path.lower()):
        return True
    
    # very large files ??
    # can't do much with the parsed urls only; need the actual content


def is_valid(url):
    try:
        parsed = urlparse(url)

        if parsed.scheme not in set(["http", "https"]):
            return False

        global url_count, url_set

        # check domain
        
        # not forget to add other urls
        # "ics.uci.edu/"
        # "cs.uci.edu/"
        # "stat.uci.edu/"
        # "today.uci.edu/department/information_computer_sciences/"
        if url.find("informatics.uci.edu/") == -1:
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
        
        url_set.add(url)
        url_count += 1
        print("CURRENT URL_COUNT: {}".format(url_count))
        
        return True

    except TypeError:
        print ("TypeError for ", parsed)
        raise

