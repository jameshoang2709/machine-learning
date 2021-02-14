#!/usr/bin/env python
# coding: utf-8

from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import pandas as pd
import numpy as np

# Get the number of restaurant to scrape (with input check)
wrong_input = True
while(wrong_input):
    try:
        num_restaurant = int(input('Enter a number of restaurants to scrape:'))
    except:
        print('Invalid input')
    else:
        wrong_input = False

root_url = 'https://www.yelp.ca'
url = '/biz/pai-northern-thai-kitchen-toronto-5?osq=Restaurants'

# Scrape info from the restaurant and then go to the next restaurant in the recommendation list
# Do this for num_restaurant of restaurants

name_list = []
num_reviews_list = []
reviewer_list = []
review_rating_list = []
review_text_list = []
counter = 1

for i in range (num_restaurant):
    print(f'Scraping info from Restaurant #{counter}')
    url_path = root_url + url
    html = urlopen(url_path).read()
    soup = bs(html, 'html.parser')
    # Get restaurant name
    name = soup.find('h1', {'class': 'heading--h1__373c0__dvYgw undefined heading--inline__373c0__10ozy'})
    print(name.get_text().strip())
    
    # Get number of reviews
    num_reviews = soup.find('span', {'class': 'text__373c0__2Kxyz text-color--white__373c0__22aE8 text-align--left__373c0__2XGa- text-weight--semibold__373c0__2l0fe text-size--large__373c0__3t60B'})
    
    # Loop through every found Review Entries of the restaurant and get its info
    for review_entry in soup.find_all('div', {'class': 'review__373c0__13kpL border-color--default__373c0__3-ifU'}):
        name_list.append(name.get_text().strip())
        num_reviews_list.append(num_reviews.get_text().strip())
        
        reviewer = review_entry.find('a', {'class': 'link__373c0__1G70M link-color--inherit__373c0__3dzpk link-size--inherit__373c0__1VFlE'})
        reviewer_list.append(reviewer.get_text().strip())

        review_rating_element = review_entry.find('div', {'class': 'i-stars__373c0__1BRrc'})
        review_rating = review_rating_element['aria-label']
        review_rating_list.append(review_rating[0])

        review_text = review_entry.find('span', {'class': 'raw__373c0__3rcx7'})
        review_text_list.append(review_text.get_text().strip())
        
#     Get a random recommendation from the suggestion list
    all_url_element = soup.find_all('a', {'class': 'link__373c0__1G70M photo-link__373c0__1sZ41 link-color--blue-dark__373c0__85-Nu link-size--default__373c0__7tls6'})
    rand_element = np.random.randint(0, len(all_url_element))
    next_url_element = all_url_element[rand_element]
    url = next_url_element['href']
    counter += 1

# Put everything in a dataframe and export to csv file

name_col = pd.Series(name_list)
num_reviews_col = pd.Series(num_reviews_list)
reviewer_col = pd.Series(reviewer_list)
review_rating_col = pd.Series(review_rating_list)
review_text_col = pd.Series(review_text_list)

data = pd.DataFrame()

data['Restaurant'] = name_col
data['Num_Reviews'] = num_reviews_col
data['Reviewer'] = reviewer_col
data['Review_Rating'] = review_rating_col
data['Review_Text'] = review_text_col

data.to_csv('scrapped_data.csv')

