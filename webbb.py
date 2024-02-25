import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import colorama
class colors:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'



def get_internal_links(url):
    internal_links = set()
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            parsed_url = urlparse(url)

            for link in soup.find_all('a'):
                href = link.get('href')
                if href and not href.startswith(('http://', 'https://', 'mailto:', 'tel:')):
                    # If the link is relative, make it absolute
                    href = urljoin(url, href)
                    # Check if the link belongs to the same domain
                    if parsed_url.netloc == urlparse(href).netloc:
                        internal_links.add(href)

    except Exception as e:
        print(f"Error getting links from {url}: {e}")

    return internal_links

def crawl_website(starting_url):
    visited_urls = set()
    urls_to_visit = set([starting_url])

    while urls_to_visit:
        current_url = urls_to_visit.pop()
        if current_url in visited_urls:
            continue

        visited_urls.add(current_url)
        print(colors.GREEN +f"Crawling: {current_url}"+ colors.END)

        internal_links = get_internal_links(current_url)
        urls_to_visit.update(internal_links - visited_urls)

    return visited_urls

def save_to_html(urls, file_name='crawled_urls.html'):
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write('<html>\n<head><title>Crawled URLs</title></head>\n<body>\n')
        file.write('<h1>Crawled URLs</h1>\n<ul>\n')
        for url in urls:
            file.write(f'<li><a href="{url}">{url}</a></li>\n')
        file.write('</ul>\n</body>\n</html>')
      

# Example usage:
starting_url = input(colors.CYAN +"enter url: "+ colors.END)
crawled_urls = crawl_website(starting_url)
for url in crawled_urls:
    print(url)

# Save crawled URLs to an HTML file
save_to_html(crawled_urls)




