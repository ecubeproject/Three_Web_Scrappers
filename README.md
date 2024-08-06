This repository contains three image scrappers.

(1) basic_image_scrapper app is generic and can work on any website. However as various websites are structured differently and their scrraping allowing policies are different it may not work for all websites. It worked on https://unsplash.com and https://www.pexels.com but did not work on many other. TRY SELENIUM, BEAUTIFUL SOUP AND SCRAPY ALL ONE BY ONE

(2) unsplash_image_scrapper is designed specifically for https://unsplash.com. It allows user to choose a topic , no of images to be scrapped and destination directory where images will be saved.

(3) shtterstock_image_scrapper is designed specifically for https://shutterstcok.com. It allows user to choose a topic , type of image (photo, 3-d image etc) , no of images to be scrapped and destination directory where images will be saved.

NOTE: ALL THREE MUST BE TREATED AS SEPARATE PROJECTS AND MUST BE USED AS FOLLOWS:

(a) DOWNLOAD THE RESPOSITORY
(b) Unzip and three folders basic_image_scrappe, unsplash_image_scrapper, shtterstock_image_scrapper will be created. Open any one using pycharm or Vscode
(c) Use pip install --r requirements.txt in terminal
(d) Type streamlit run <your_script_name>.py in terminal
(e) Streamlit app will run in browser
