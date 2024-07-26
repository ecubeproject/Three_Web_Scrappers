import os
import time

import requests
import scrapy
import streamlit as st
from bs4 import BeautifulSoup
from scrapy.crawler import CrawlerProcess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def scrape_images_with_beautiful_soup(search_word):
    url = f"https://unsplash.com/s/photos/{search_word}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    images = []
    for img in soup.find_all('img'):
        img_url = img.get('src')
        if img_url and img_url.startswith('http'):
            images.append(img_url)
    return images


def scrape_images_with_selenium(search_word, num_images):
    url = f"https://unsplash.com/s/photos/{search_word}"
    options = Options()
    options.binary_location = "/usr/bin/google-chrome-stable"
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)

    images = []
    while len(images) < num_images:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        img_elements = soup.find_all('img', class_='oCCRx')
        for img_element in img_elements:
            img_url = img_element.get('src')
            if img_url and img_url.startswith('https'):
                images.append(img_url)

        # Scroll down to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Wait for new images to load

    driver.quit()
    return images


def scrape_images_with_scrapy(search_word):
    url = f"https://unsplash.com/s/photos/{search_word}"

    class ImageScraper(scrapy.Spider):
        name = "image_scraper"
        start_urls = [url]

        def parse(self, response, **kwargs):
            for img in response.css('img'):
                img_url = img.get()
                if img_url and img_url.startswith('http'):
                    yield {
                        'image_url': img_url
                    }

    process = CrawlerProcess()
    process.crawl(ImageScraper)
    process.start()
    return None  # Return None as Scrapy yields data to a file, not to the function


def download_images(images, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for i, img_url in enumerate(images):
        response = requests.get(img_url)
        with open(os.path.join(output_dir, f'image_{i + 1}.jpg'), 'wb') as f:
            f.write(response.content)


def main():
    st.title("Image Scraper App")
    st.write("Select the library you want to use for image scraping:")
    library = st.selectbox("Library", ["Beautiful Soup", "Selenium", "Scrapy"])

    search_word = st.text_input("Enter a search word (e.g. 'Nature' or 'Travel'):")
    num_images_input = st.text_input("Enter the number of images to download:")
    output_dir = st.text_input("Enter the output directory for images:")
    if st.button("Scrape Images"):
        try:
            num_images = int(num_images_input)
            if num_images <= 0:
                st.error("Please enter a positive integer.")
            else:
                if library == "Beautiful Soup":
                    images = scrape_images_with_beautiful_soup(search_word)
                    st.write(f"Found {len(images)} images:")
                    st.write(images)
                    download_images(images, output_dir)
                    st.write(f"Images downloaded to {output_dir}")
                elif library == "Selenium":
                    images = scrape_images_with_selenium(search_word, num_images)
                    st.write(f"Found {len(images)} images:")
                    st.write(images)
                    download_images(images, output_dir)
                    st.write(f"Images downloaded to {output_dir}")
                elif library == "Scrapy":
                    scrape_images_with_scrapy(search_word)
                    st.write(
                        "Scrapy yields data to a file, not to the app. Check your local directory for the scraped "
                        "images.")
        except ValueError:
            st.error("Please enter a valid integer.")


if __name__ == "__main__":
    main()
