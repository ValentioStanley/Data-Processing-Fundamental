import time
import datetime
import requests
from bs4 import BeautifulSoup
import re
 
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    )
}
 
 
def fetching_content(url):
    """Mengambil konten HTML dari URL yang diberikan."""
    session = requests.Session()
    response = session.get(url, headers=HEADERS)
    try:
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Terjadi kesalahan ketika melakukan requests terhadap {url}: {e}")
        return None
 
 
def extract_product_data(product):
    """Mengambil data buku berupa judul, harga, ketersediaan, dan rating dari article (element html)."""
    product_title = product.find('h3', class_='product-title').text # judul produk
    # print(product.prettify())
    detail_element = product.find('div', class_='product-details')
    # harga
    if detail_element.find('div', class_='price-container'):
        price = detail_element.find('span', class_='price').text
    else:
        price = detail_element.find('p', class_='price').text
    
    # rcsg = rating color size gender
    rating, num_color, size, gender = 'null', 'null', 'null', 'null'
    # rating = num_color = size = gender = 'null'
    # detail_rcsg = detail_element.find('p').text.strip()
    detail_rcsg = detail_element.find_all('p')
    # print(detail_rcsg)
    for texts in detail_rcsg:
        text = texts.text.strip()
        if re.search(r"Rating:", text):
            rating = text
        elif re.search(r"\bColors\b", text):
            num_color = text
        elif re.search(r"Size:", text):
            size = text
        elif re.search(r"Gender:", text):
            gender = text
    
    # Menambahkan kolom baru untuk timestamp
    timestamp = datetime.datetime.now()
    
    items = {
        "Title": product_title,
        "Price": price,
        "Rating": rating,
        "Number Color": num_color,
        "Size": size,
        "Gender": gender,
        "Timestamp" : timestamp
    }
    
    return items
 
 
def scrape_product(base_url, start_page=1, delay=2):
    """Fungsi utama untuk mengambil keseluruhan data, mulai dari requests hingga menyimpannya dalam variabel data."""
    data = []
    page_number = start_page
 
    while True:
        # url = base_url+"page{}".format(page_number)
    
        if page_number > 1:
            url = base_url+"page{}".format(page_number)
        else: 
            url = base_url
        #     url = f"{base_url}/page{page_number}" 
        print(f"Scraping halaman: {url}")
 
        content = fetching_content(url)
        if content:
            soup = BeautifulSoup(content, "html.parser")
            collection_elements = soup.find_all('div', class_='collection-card')
            for collection in collection_elements:
                product = extract_product_data(collection)
                data.append(product)
                
            next_button = soup.find('li', class_='page-item next')
            if next_button:
                page_number += 1
                time.sleep(delay) # Delay sebelum halaman berikutnya
            else:
                break # Berhenti jika sudah tidak ada next button
        else:
            break # Berhenti jika ada kesalahan
 
    return data
 
 