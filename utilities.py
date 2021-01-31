from collections import defaultdict
from urllib.parse import urlparse


### useful for question 3

def common_words() -> None:
    frequency = defaultdict(int)
    with open('textlist.txt', 'r') as f:
        for word in f:
            frequency[word.rstrip('\n')] += 1
    with open('textfrequency.txt', 'w') as write:
        for k, v in sorted(frequency.items(), key=lambda item: (-item[1], item[0])):
            write.writelines("{} -> {}\n".format(k, v))

### useful for question 4

def subdomains() -> None:
    with open('urllist.txt', 'r') as f:
        urls = [url.rstrip('\n') for url in f]
    #### need to work
    pass

if __name__ == '__main__':
    common_words()
    subdomains()