import re
from simhash import Simhash, SimhashIndex
from bs4 import BeautifulSoup
def get_features(s):
    width = 3
    s = s.lower()
    s = re.sub(r'[^\w]+', '', s)
    return [s[i:i + width] for i in range(max(len(s) - width + 1, 1))]

print('%x' % Simhash(get_features('How are you? I am fine. Thanks.')).value)
print('%x' % Simhash(get_features('How are u? I am fine.     Thanks.')).value)
print('%x' % Simhash(get_features('How r you?I    am fine. Thanks.')).value)


print(Simhash('aa').distance(Simhash('bb')))
print(Simhash('aaa').distance(Simhash('aa')))

ALPHANUM_PATTERN = re.compile(r"[A-Za-z0-9]+")

a = 'https://wics.ics.uci.edu/wics-spring-quarter-week-5-yoga-and-study-sessionice-cream/?afg78_page_id=2'
b = 'https://wics.ics.uci.edu/wics-spring-quarter-week-5-yoga-and-study-sessionice-cream/?afg78_page_id=1'

soup = BeautifulSoup(a, 'html.parser')
soup_list = [i for i in ALPHANUM_PATTERN.findall(soup.get_text().lower()) if len(i) > 2]
print(soup_list)
soup2 = BeautifulSoup(b, 'html.parser')
soup_list2 = [i for i in ALPHANUM_PATTERN.findall(soup.get_text().lower()) if len(i) > 2]

soup_list2.append("this")
print(soup_list2)

print(Simhash(soup_list).distance(Simhash(soup_list2)))

data = {
    1: u'How are you? I Am fine. blar blar blar blar blar Thanks.',
    2: u'How are you i am fine. blar blar blar blar blar than',
    3: u'This is simhash test.',
}
objs = [(str(k), Simhash(get_features(v))) for k, v in data.items()]
index = SimhashIndex(objs, k=3)

print(index.bucket_size())

s1 = Simhash(get_features(u'How are you i am fine. blar blar blar blar blar thank'))
print(index.get_near_dups(s1))

index.add('4', s1)
print(index.get_near_dups(s1))
