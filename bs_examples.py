from bs4 import BeautifulSoup
hi_path = 'data/hi.html'
with open(hi_path, 'r') as f:
    hi = f.read()
    hi = BeautifulSoup(hi, 'html.parser')
    print(hi.title) # find the title tag
    print(hi.title.string)  # find the value of tag