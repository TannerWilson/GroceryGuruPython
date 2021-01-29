from database import Database
from walmart import Walmart
from threading import Timer

#  This calss will run the same function every interval seconds
class ProductPopulator(object):
    def __init__(self):
        self.search_ingredients()
        #  self.interval = 604800 # One week in seconds
        #  self.thread = Timer(self.interval, self.run_function())
        #  self.thread.start()
    
    # def run_function(self):
        # self.search_ingredients()
        # self.thread = Timer(self.interval, self.run_function())
        # self.thread.start()
        
    
    def search_ingredients(self):
        db = Database()
        walmart = Walmart()
        walmart.login('tanner28aw@gmail.com', 't@12103101')
        print("Logged in...")
        
        ingredients = db.get_ingredients()
        
        count = db.get_count("products")[0];
        print(count)
        for ingredient in ingredients:
            count += 1
            print("Adding " + str(ingredient[1]) + " ID: " + str(count))
            walmart.search(ingredient[1])
            name, link, price = walmart.get_cheapest()
            
            db.insert_product(name,link,price)
            db.insert_product_asc(count, ingredient[1])
        
        db.close_connection()