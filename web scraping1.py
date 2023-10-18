import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

# Specify the base URL for the search
base_url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"

# Number of pages to scrape
num_pages = 20

# Create a list to store all the product information
all_product_info = []

# Loop through the specified number of pages
for page in range(1, num_pages + 1):
    # Create the URL for the current page
    url = f"{base_url}{page}"

    # Send an HTTP request to the URL
    response = requests.get(url)

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find and extract product names, prices, ratings, the number of reviews, and product URLs
    product_info = []

    titles = soup.find_all('span', {'class': 'a-text-normal'})
    prices = soup.find_all('span', {'class': 'a-price-whole'})
    ratings = soup.find_all('span', {'class': 'a-icon-alt'})
    review_counts = soup.find_all('span', {'class': 'a-size-base'})
    product_links = soup.find_all('a', {'class': 'a-link-normal'})

    for i in range(len(titles)):
        title = titles[i].get_text()
        price = prices[i].get_text() if i < len(prices) else "N/A"
        rating = ratings[i].get_text() if i < len(ratings) else "N/A"
        review_count = review_counts[i].get_text() if i < len(review_counts) else "N/A"
        product_url = "https://www.amazon.in" + product_links[i].get('href') if i < len(product_links) else "N/A"

        product_info.append([title, price, rating, review_count, product_url])

    # Add the product information from the current page to the list
    all_product_info.extend(product_info)

# Define the CSV file name
csv_file_name = "amazon_products.csv"

# Write the data to a CSV file
with open(csv_file_name, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    
    # Write the header row
    writer.writerow(['Title', 'Price', 'Rating', 'Number of Reviews', 'Product URL'])
    
    # Write the product information
    writer.writerows(all_product_info)

print(f"Data has been exported to '{csv_file_name}'")
