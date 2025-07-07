import requests
from urllib.parse import urljoin
from lxml import html
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "https://app.leg.wa.gov/rcw/"


def extract_inner_url(url):
    """extract url from html"""
    logger.info(f'wait get url: {url}')
    rsp = requests.get(url)
    if rsp.status_code == 200:
        tree = html.fromstring(rsp.content)
        title_url_lst = tree.xpath('//table//tr/td[1]/a[1]/@href')
        top3_url = [url if 'http' in url else urljoin(BASE_URL, url) for url in title_url_lst]
        return top3_url
    raise Exception(f"failed get html, code: {rsp.status_code}")


def extract_inner_text(url):
    """extract text from html"""
    logger.info(f'wait get url: {url}')
    rsp = requests.get(url)
    if rsp.status_code == 200:
        tree = html.fromstring(rsp.content)
        inner_text_lst = tree.xpath("//div[@id='contentWrapper']//text()")
        title = tree.xpath("//h3//text()")[3]
        inner_text = ','.join(inner_text_lst)
        return title, inner_text
    raise Exception(f"failed get html, code: {rsp.status_code}")


def get_html_url():
    """the url we need is in the third page"""
    top3_url_lst = extract_inner_url(BASE_URL)
    top3_url_lst = top3_url_lst[:3]
    logger.info(f'first page url: {top3_url_lst}')
    inner_url_lst = []
    for t3_url in top3_url_lst:
        second_url_lst = extract_inner_url(t3_url)
        logger.info(f'second page url: {second_url_lst}')
        for sec_url in second_url_lst:
            third_url_lst = extract_inner_url(sec_url)
            logger.info(f'third page url: {third_url_lst}')
            inner_url_lst.extend(third_url_lst)
    return inner_url_lst


if __name__ == '__main__':
    logger.info('start spider')
    t = extract_inner_text('http://app.leg.wa.gov/RCW/default.aspx?cite=1.70.900')
    print(t)
