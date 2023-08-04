import sys
import requests
from bs4 import BeautifulSoup
import re
import json

from collections import OrderedDict
import io
from urllib.request import Request, urlopen

from pypdf import PdfWriter, PdfReader

def has_github_link(text):
    # Sử dụng biểu thức chính quy để kiểm tra liên kết GitHub
    github_repo_pattern = r'^https?://github.com/.*$'
    return re.match(github_repo_pattern, text)
    # return 'github.com' in text

def find_github_link_from_arxiv(article_title):
    # Tìm kiếm bài báo trên arXiv
    search_url = f"https://arxiv.org/search/?query={article_title.replace(' ', '+')}&searchtype=all"
    print(search_url)
    response = requests.get(search_url)
    html_content = response.text

    # Phân tích cú pháp HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Tìm liên kết đầu tiên trong kết quả tìm kiếm
    link_tag = soup.find('li', class_='arxiv-result')

    if link_tag:
        title = link_tag.find('div', class_='is-marginless')
        article_link = title.find('a', string='pdf')['href']

        # Truy cập trang bài báo trên arXiv
        writer = PdfWriter()

        remote_file = urlopen(Request(article_link)).read()
        memory_file = io.BytesIO(remote_file)
        pdf_file = PdfReader(memory_file)

        page_1 = pdf_file.pages[0].extract_text()

        # Tìm liên kết GitHub trong trang 1 bài báo
        lines = page_1.split('\n')
        for line in lines:
            idx = line.find("https://github.com")
            if idx != -1:
                # print(line)
                return line[idx:]
    return None

def find_github_link_from_paperswithcode(article_title):
    # Tìm kiếm bài báo trên paperswithcode
    search_url = f"https://paperswithcode.com/search?q={article_title.replace(' ', '+')}"
    print(search_url)
    response = requests.get(search_url)
    html_content = response.text

    # Phân tích cú pháp HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Tìm liên kết đầu tiên trong kết quả tìm kiếm
    link_tag = soup.find('div', class_='infinite-container')

    if link_tag:
        h1 = link_tag.find('h1')
        if h1:
          title = h1.find('a')
          article_link = "https://paperswithcode.com" + title['href']

          # Truy cập trang bài báo trên paperswithcode
          response = requests.get(article_link)
          html_content = response.text

          # Tìm liên kết GitHub trong trang bài báo
          soup = BeautifulSoup(html_content, 'html.parser')
          code = soup.find('div', class_='code-table')
          list_tag = code.find_all('a')
          return [i['href'] for i in list_tag]
    return None

def find_github_link_from_github(article_title):
    # Tìm kiếm bài báo trên GitHub
    search_url = f"https://github.com/search?q={article_title.replace(' ', '+')}&type=repositories"
    print(search_url)
    response = requests.get(search_url)
    search_content = response.text
    content = json.loads(search_content)
    list_repo = ["https://github.com/" + i["hl_name"] for i in content["payload"]["results"]]

    github_links = []
    for repo_link in list_repo:
      page_content = requests.get(repo_link).text
      if article_title in page_content:
        github_links.append(repo_link)
    return github_links if github_links else None

def find_github_link_from_google(article_title):
    # Tìm kiếm bài báo trên Google
    search_url = f"https://www.google.com/search?q={article_title.replace(' ', '+')}"
    print(search_url)
    response = requests.get(search_url)
    html_content = response.text

    # Phân tích cú pháp HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Tìm các thẻ chứa tiêu đề của bài báo
    link_tags = soup.find_all('a', href=True)
    github_link = None
    # Lặp qua các liên kết để tìm liên kết bài báo
    for link_tag in link_tags:
        href = link_tag['href']
        if "/url?q=" in href:
            # Trích xuất liên kết thực tế của bài báo từ liên kết của Google
            github_link = href.replace("/url?q=", "").split("&")[0]
            if has_github_link(github_link):
                return github_link
    return None

def find_github_link(article_title):
    linkes = OrderedDict()

    # Kiểm tra liên kết GitHub trên arXiv
    github_link_from_arxiv = find_github_link_from_arxiv(article_title)
    linkes['arxiv'] = github_link_from_arxiv if github_link_from_arxiv else "Không tìm thấy liên kết GitHub trong bài báo."

    # Kiểm tra liên kết GitHub trên paperswithcode
    github_link_from_paperswithcode = find_github_link_from_paperswithcode(article_title)
    linkes['paperswithcode'] = github_link_from_paperswithcode if github_link_from_paperswithcode else "Không tìm thấy liên kết GitHub trong bài báo."

    # Kiểm tra liên kết GitHub trên GitHub
    github_link_from_github = find_github_link_from_github(article_title)
    linkes['github'] = github_link_from_github if github_link_from_github else "Không tìm thấy liên kết GitHub trong bài báo."

    # Kiểm tra liên kết GitHub trên Google
    github_link_from_google = find_github_link_from_google(article_title)
    linkes['google'] = github_link_from_google if github_link_from_google else "Không tìm thấy liên kết GitHub trong bài báo."

    return linkes
  
def main():
    if len(sys.argv) != 2:
        print("Sử dụng: python find_github.py <Tên bài báo>")
        return

    article_title = sys.argv[1]
    github_link = find_github_link(article_title)

    if github_link:
        print("Liên kết GitHub của bài báo:")
        print(github_link)
    else:
        print("Không tìm thấy liên kết GitHub trong bài báo.")

if __name__ == "__main__":
    main()
