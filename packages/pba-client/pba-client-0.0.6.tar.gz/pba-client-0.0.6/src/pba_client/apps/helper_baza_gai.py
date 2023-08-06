import urllib.parse as url_parse


def fix_baza_gai_image_url(image_url: str):
    url_base = "https://baza-gai.com.ua"
    parsed_url = url_parse.urlsplit(image_url)
    url_path = url_parse.quote(parsed_url.path)
    return url_parse.urljoin(url_base, url_path)
