from store import Store
from database import Database
import time
import requests
import json


# Status meanings:
# 0 : running
# 1 : finished
# 2 : error
class Walmart(Store):
    def __init__(self):
        super().__init__()
        self.status = 0

    def login(self, user, password):
        print("Logging in...")
        self.visit("https://grocery.walmart.com/account/login")
        self.browser.fill('email', user)
        self.browser.fill('password', password)
        self.browser.find_by_text('Sign In').click()
        time.sleep(10)

    def get_price(self):
        # Keep trying to find the price until the page is loaded. Try both old and new versions of the product page.
        cont = True
        while (cont):
            try:
                dollarSpan = self.browser.find_by_css('span[data-automation-id="wholeUnitsOG"]')
                centsSup = self.browser.find_by_css('sup[data-automation-id="partialUnitsOG"]')
                priceS = dollarSpan.text + "." + centsSup.text
                price = float(priceS)
                cont = False
            except:
                try:
                    dollarSpan = self.browser.find_by_css('span[data-automation-id="wholeUnits"]')
                    centsSup = self.browser.find_by_css('sup[data-automation-id="partialUnits"]')
                    priceS = dollarSpan.text + "." + centsSup.text
                    price = float(priceS)
                    cont = False
                except:
                    time.sleep(1)

        print(price)

        return price

    def get_name(self):
        cont = True
        while (cont):
            try:
                nameDiv = self.browser.find_by_css('div[data-automation-id="name"]')
                name = nameDiv.text
                cont = False
            except:
                try:
                    nameDiv = self.browser.find_by_css('span[data-automation-id="nameOG"]')
                    name = nameDiv.text
                    cont = False
                except:
                    time.sleep(1)

        print(name)

        return name

    def search(self, query):
        self.results.clear()
        self.visit('https://grocery.walmart.com/search/?query=' + query)
        time.sleep(5)

        # Loop over results and store in map
        items = self.browser.find_by_css('.ProductsPageOld__productListTile___3c6q8')

        for item in list(items)[:3]:
            try:  # Grab Name and Price
                name = item.find_by_css('div[data-automation-id="name"]').text
                dollars = item.find_by_css('span[data-automation-id="wholeUnits"]').text
                cents = item.find_by_css('sup[data-automation-id="partialUnits"]').text
                link = item.find_by_css('a[data-automation-id="link"]')['href']
                price = float(dollars + "." + cents)
                self.results[name] = (link, price)
            except:  # Try other website tags
                try:
                    name = item.find_by_css('div[data-automation-id="nameOG"]').text
                    dollars = item.find_by_css('span[data-automation-id="wholeUnitsOG"]').text
                    cents = item.find_by_css('sup[data-automation-id="partialUnitsOG"]').text
                    link = item.find_by_css('a[data-automation-id="linkOG"]')['href']
                    price = float(dollars + "." + cents)
                    self.results[name] = (link, price)
                except:
                    continue

    def get_cheapest(self):
        prices = []
        for linkPriceTuple in self.results.values():
            prices.append(linkPriceTuple[1])
        if len(prices) == 0:
            price = 0
        else:
            price = min(prices)

        for name in self.results:
            if self.results[name][1] == price:
                link = self.results[name][0]
                return name, link, price

    def add_to_cart(self):
        print("Starting to add to cart...")
        cont = True
        sleep_amount = 0.5
        time_slept = 0
        while (cont):
            try:
                button = self.browser.find_by_css('button[data-automation-id="addToCartBtn"]')[0]
                button.click()
                print("Clicked button...")
                cont = False
            except:
                try:
                    button = self.browser.find_by_css('button[data-automation-id="addToCartBtnOG"]')[0]
                    button.click()
                    print("Clicked old button...")
                    cont = False
                except:
                    time.sleep(sleep_amount)
                    time_slept += sleep_amount
                    print("Sleeping...")
                    if time_slept > 3:
                        print("Skipping item...")
                        return

    # *****************************************************************
    # Main store function. Attempts to add all products in a user's
    # checklist to their Walmart Cart. First attempting to navigate to
    # the saved url, then manually searching by name should that fail.
    # *****************************************************************
    def run_job(self, user_id):
        # Connect to DB, grab checklist products
        self.login('adam.sorensen455@gmail.com', 'capstone2017')
        db = Database()
        ingredients = db.get_checklist_ingredients(user_id)
        print(ingredients)
        products = db.get_products(ingredients)
        print(products)

        # Search for and add all products to cart
        for product in products:
            print("Product starting...")
            print(product)
            print(product[0][3])
            self.visit(product[0][3])
            self.add_to_cart()

        self.status = 1
        # Report whether success or not
        self.job_done(user_id, self.status)
        print("Sent /done ")

    def clear_results(self):
        self.results = {}