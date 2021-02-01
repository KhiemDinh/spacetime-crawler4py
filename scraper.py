import re
import urllib.robotparser
from collections import defaultdict
from urllib.parse import urlparse, urldefrag
from bs4 import BeautifulSoup
from simhash import Simhash, SimhashIndex

# solutions to question 1
url_set = set()

### for answering question 2
### [longest url, number of words] 
longest = ['url', 0]

### question 3
### saving textlist.txt done inside extract_next_links

### question 4
### also saving urllist.txt done inside extract_next_links

### to answer questions, will have a separate file
### utilities.py

### SimhashIndex
num = 0
index = SimhashIndex([], k = 3)

traps = ["/calendar","replytocom=","wp-json","share=","format=xml", "/feed", ".pdf", ".zip", ".sql", "action=login", "?ical=", ".ppt", "version=", "=diff", "difftype=sidebyside"]
disallowed = ["wics.ics.uci.edu/events", "evoke.ics.uci.edu/qs-personal-data-landscapes-poster", "informatics.uci.edu/files/pdf/InformaticsBrochure-March2018"]

ALPHANUM_PATTERN = re.compile(r"[A-Za-z0-9]+")

def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]


def extract_next_links(url, resp):
    # Implementation required.
    try:
        global num
        output = set()

        if 200 == resp.status:
            soup = BeautifulSoup(resp.raw_response.content, 'html.parser')

            # check if soup is high quality
            # find all unique words in the soup that are of length 3+
            soup_text =  soup.get_text()
            soup_list = [i for i in ALPHANUM_PATTERN.findall(soup_text.lower()) if len(i) > 2]
            
            # soup_text = re.sub('[^A-Za-z0-9]+', ' ', soup.get_text().lower())
            # soup_list = [_ for _ in soup_text.split() if len(_) > 2]

            # check if the soup is empty
            if not soup_list: return []
            
            # adds url to the urllist.txt file
            with open('urllist.txt', 'a') as f: # keeps appending
                f.writelines("%s\n" % url)

            ########## SimHash Implementation HERE ##########
            num += 1
            s1 = Simhash(get_features(soup_text))
            if index.get_near_dups(s1): 
                print("duplicate!")
                return []
            else: index.add(str(num), s1)
            #################################################

            # longest content?
            if len(soup_list) > longest[1]:
                longest[0] = url
                longest[1] = len(soup_list)
                with open('longest.txt', 'w') as f:
                    f.writelines("{} : {}".format(longest[0], longest[1]))
            
            # writes to the textlist.txt file
            with open('textlist.txt', 'a') as f: # keeps appending
                f.writelines("%s\n" % word for word in soup_list)

            # find all links
            for link in soup.find_all('a', href=True):
                link = link.attrs.get('href')

                if link: 
                    link = urldefrag(link)[0]

                    if link not in url_set:
                        output.add(link)
            
        return list(output)

    except:
        return []


def crawlable(url, parsed):
    # check robots.txt
    try:
        netloc = parsed.scheme + "://" + parsed.netloc + "/robots.txt"

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

    # trap parts
    for trap in traps:
        if trap in parsed_url:
            return True

    # disallowed websites
    for link in disallowed:
        if link in parsed_url:
            return True

    return False


def is_valid(url):
    try:
        parsed = urlparse(url)

        if parsed.scheme not in set(["http", "https"]):
            return False

        # check domain
        if url.find(".ics.uci.edu/") == -1 and url.find(".cs.uci.edu/") == -1 \
            and url.find(".informatics.uci.edu/") == -1 and url.find(".stat.uci.edu/") == -1 \
            and url.find("today.uci.edu/department/information_computer_sciences/") == -1:
            return False

        # check robots.txt
        if not crawlable(url, parsed):
            return False

        # check trap
        if is_trap(parsed):
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
        
        return True

    except TypeError:
        print ("TypeError for ", parsed)
        raise

### a helper function for simhash

def get_features(s):
    width = 3
    s = s.lower()
    s = re.sub(r'[^\w]+', '', s)
    return [s[i:i + width] for i in range(max(len(s) - width + 1, 1))]
