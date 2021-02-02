from collections import defaultdict
from urllib.parse import urlparse


### useful for question 3

def common_words() -> None:
    frequency = defaultdict(int)
    stopwords = set()
    with open('stopwords.txt', 'r') as stop:
        for word in stop:
            stopwords.add(word.rstrip('\n'))
    with open('textlist.txt', 'r') as f:
        for word in f:
            frequency[word.rstrip('\n')] += 1
    with open('textfrequency.txt', 'w') as write:
        for k, v in sorted(frequency.items(), key=lambda item: (-item[1], item[0])):
            # to also see the frequency of stopwords, just delete this if
            if k not in stopwords:
                write.writelines("{} -> {}\n".format(k, v))

### useful for question 4

def subdomains() -> None:
    subdomain = defaultdict(int)
    # adding only urls with 'ics.uci.edu' included
    with open('urllist.txt', 'r') as f:
        urls = [urlparse(url.rstrip('\n')).netloc.lower() for url in f if 'ics.uci.edu' in urlparse(url.rstrip('\n')).netloc]
    for url in sorted(urls):
            subdomain[url.rstrip('\n')] += 1
    with open('ics_uci_edu.txt', 'w') as write:
        for k, v in subdomain.items():
            write.writelines("{} -> {}\n".format(k, v))
    
if __name__ == '__main__':
    common_words()
    subdomains()