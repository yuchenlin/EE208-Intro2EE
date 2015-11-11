from bs4 import BeautifulSoup
def clean_html(html):
    import re,string
    text = re.sub(r"(?is)<(script|style).*?>.*?(</\1>)", "", html.strip())      
    text = re.sub(r"(?s)<!--(.*?)-->[\n]?", "", text)   
    text = re.sub(r"(?s)<.*?>", "", text)       
    text = re.sub(r"&.*?;", "", text)
    text = re.sub(r"[.*?]", "", text)
    text = re.sub(r"{.*?}", "", text)
    return text

filename = 'html/a767cd30eb22a060d01706b35664ff01.html'
f = open(filename)
bs = BeautifulSoup(f.read())
f.close()
ori_text = clean_html(bs.get_text())
print ori_text