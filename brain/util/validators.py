import urllib
import re


def format_domain(url):
    # valid conditions for urls in string
    if not url:
        return ''

    if not re.match('https?://(?:www)?(?:[\w-]{2,255}(?:\.\w{2,6}){1,2})(?:/[\w&%?#-]{1,300})?', url):
        p = urllib.parse.urlparse(url, 'http')
        netloc = p.netloc or p.path
        path = p.path if p.netloc else ''
        if not netloc.startswith('www.'):
            netloc = 'www.' + netloc

        p = urllib.parse.ParseResult('http', netloc, path, *p[3:])
        p = p.geturl()

        if not p.endswith(".br"):
            if not p.endswith(".com"):
                p = p + ".com"

        return p
    return url
