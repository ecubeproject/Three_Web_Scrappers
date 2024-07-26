import streamlit as st
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import scrapy
from scrapy.crawler import CrawlerProcess
import os


def scrape_images_with_beautiful_soup(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    images = []
    for img in soup.find_all('img'):
        img_url = img.get('src')
        if img_url and img_url.startswith('http'):
            images.append(img_url)
    return images


def scrape_images_with_selenium(url):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)
    images = []
    for img in driver.find_elements(By.TAG_NAME, 'img'):
        img_url = img.get_attribute('src')
        if img_url and img_url.startswith('http'):
            images.append(img_url)
    driver.quit()
    return images


def scrape_images_with_scrapy(url):
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

    url = st.text_input("Enter the URL to scrape images from:")
    output_dir = st.text_input("Enter the output directory for images:")
    if st.button("Scrape Images"):
        if library == "Beautiful Soup":
            images = scrape_images_with_beautiful_soup(url)
            st.write(f"Found {len(images)} images:")
            st.write(images)
            download_images(images, output_dir)
            st.write(f"Images downloaded to {output_dir}")
        elif library == "Selenium":
            images = scrape_images_with_selenium(url)
            st.write(f"Found {len(images)} images:")
            st.write(images)
            download_images(images, output_dir)
            st.write(f"Images downloaded to {output_dir}")
        elif library == "Scrapy":
            scrape_images_with_scrapy(url)
            st.write("Scrapy yields data to a file, not to the app. Check your local directory for the scraped images.")


if __name__ == "__main__":
    main()
