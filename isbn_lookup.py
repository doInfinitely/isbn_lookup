try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen
import selenium
from html.parser import HTMLParser
from selenium import webdriver

class MyISBNParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.xpath = []
        self.title = None
    def handle_starttag(self, tag, attrs):
        self.xpath.append(tag)

    def handle_endtag(self, tag):
        self.xpath.pop()

    def handle_data(self, data):
        if self.xpath[-1] == 'h1' and self.title is None:
            self.title = data

def get_title(isbn, use_selenium=True):
    isbn = ''.join(isbn.split('-'))
    if not use_selenium:
        with urlopen('https://isbnsearch.org/isbn/{}'.format(isbn)) as f:
            source = f.read()
    else:
        driver = webdriver.Chrome()
        driver.get('https://isbnsearch.org/isbn/{}'.format(isbn))
        source = driver.page_source
        driver.close()
    parser = MyISBNParser()
    parser.feed(source)
    return parser.title

def get_neighbors(isbn):
    isbn = ''.join(isbn.split('-'))
    output = set()
    for i,x in enumerate(isbn):
        output.update({isbn[:i]+str(y)+isbn[i+1:] for y in range(10) if y != isbn[i]})
    return output

def get_nearest(label, isbn_set, distance_metric):
    distance = float('inf')
    old_distance = distance
    nearest = None
    for isbn in isbn_set:
        title = get_title(isbn)
        distance = min(distance, distance_metric(label,title))
        if old_distance != distance:
            nearest = title
    return nearest, distance

# Distance Metrics
def levenshtein_distance(s, t):
    D = [[0 for i in range(len(t)+1)] for j in range(len(s)+1)]
    for i in range(1,len(s)+1):
        D[i][0] = i
    for j in range(1, len(t)+1):
        D[0][j] = j
    for j in range(1, len(t)+1):
        for i in range(1, len(s)+1):
            try:
                cost = int(not s[i-1] == t[j-1])
            except IndexError:
                cost = 1
            D[i][j] = min([D[i-1][j]+1, D[i][j-1]+1, D[i-1][j-1]+cost])
    return D[len(s)][len(t)]

#TODO: Semantic Distance Metrics

if __name__ == "__main__":
    print(levenshtein_distance("sitting", "kitten"))
    print(get_title('9780061122415'))
    isbn_set = get_neighbors('9780061122415')
    print(isbn_set)
    isbn_set = set()
    isbn_set.add('9780061122415')
    print(get_nearest('the alchemist', isbn_set, levenshtein_distance))
