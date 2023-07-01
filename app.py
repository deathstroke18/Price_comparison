from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def scrape_product_prices(product):
    amazon_url = "https://www.amazon.in/s?k=" + product
    flipkart_url = "https://www.flipkart.com/search?q=" + product

    amazon_page = requests.get(amazon_url)
    flipkart_page = requests.get(flipkart_url)

    amazon_soup = BeautifulSoup(amazon_page.content, "html.parser")
    flipkart_soup = BeautifulSoup(flipkart_page.content, 'html.parser')

    amazon_products = []
    flipkart_products = []

    amazon_product_containers = amazon_soup.find_all("div", class_="sg-col-inner")
    for container in amazon_product_containers:
        name_element = container.find("span", class_=["a-size-base-plus a-color-base a-text-normal"]) or container.find("span", class_=["a-size-medium a-color-base a-text-normal"])
        price_element = container.find("span", class_="a-offscreen")

        if name_element and price_element:
            name = name_element.text.strip()
            price = price_element.text.strip()
            amazon_products.append({
                'name': name,
                'price': price
            })

    flipkart_product_containers = flipkart_soup.find_all('div', class_="_1AtVbE")
    for container in flipkart_product_containers:
        name_element = container.find('div', class_="_4rR01T")
        price_element = container.find('div', class_="_30jeq3 _1_WHN1")

        if name_element and price_element:
            name = name_element.text.strip()
            price = price_element.text.strip()
            flipkart_products.append({
                'name': name,
                'price': price
            })

    return amazon_products, flipkart_products


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Get the product name from the user input
        product_name = request.form.get('product_name')

        # Call the web scraping function to retrieve the scraped data
        amazon_products, flipkart_products = scrape_product_prices(product_name)

        # Return the scraped data to display on the result page
        return render_template('result.html', amazon_products=amazon_products, flipkart_products=flipkart_products)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
