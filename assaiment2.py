import requests
from bs4 import BeautifulSoup

# Specify the base URL for the search
base_url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_"

# Number of pages to scrape
num_pages = 20

# Function to extract additional product details
def extract_product_details(product_url):
    response = requests.get(product_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    description = soup.find('meta', {'name': 'description'})['content'] if soup.find('meta', {'name': 'description'}) else "N/A"
    asin = soup.find('th', string="ASIN").find_next('td').get_text() if soup.find('th', string="ASIN") else "N/A"
    product_description = soup.find('div', {'id': 'productDescription'}).get_text() if soup.find('div', {'id': 'productDescription'}) else "N/A"
    manufacturer = soup.find('th', string="Manufacturer").find_next('td').get_text() if soup.find('th', string="Manufacturer") else "N/A"

    return {
        'Description': description,
        'ASIN': asin,
        'Product Description': product_description.strip(),
        'Manufacturer': manufacturer
    }

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

        # Extract additional product details
        details = extract_product_details(product_url)

        product_info.append({
            'Title': title,
            'Price': price,
            'Rating': rating,
            'Number of Reviews': review_count,
            'Product URL': product_url,
            **details  # Add the additional details to the product_info dictionary
        })

    # Print the product information from the current page
    print(f"Page {page} Product Information:")
    for item in product_info:
        print(f"Title: {item['Title']}")
        print(f"Price: {item['Price']}")
        print(f"Rating: {item['Rating']}")
        print(f"Number of Reviews: {item['Number of Reviews']}")
        print(f"Product URL: {item['Product URL']}")
        print(f"Description: {item['Description']}")
        print(f"ASIN: {item['ASIN']}")
        print(f"Product Description: {item['Product Description']}")
        print(f"Manufacturer: {item['Manufacturer']}")
        print()

    # Optional: You can add a delay to avoid overloading the server
    # time.sleep(2)  # Import the time module and uncomment this line

    # Note: Amazon may have anti-scraping measures, so use with caution and respect their terms of service.
