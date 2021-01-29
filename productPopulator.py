from database import Database
from walmart import Walmart
from threading import Timer

#  This calss will run the same function every interval seconds
class ProductPopulator(object):
    def __init__(self):
        self.interval = 604800 # One week in seconds
        self.thread = Timer(self.interval, self.run_function())
        self.thread.start()
    
    def run_function(self):
        self.search_ingredients()
        self.thread = Timer(self.interval, self.run_function())
        self.thread.start()
        
    
    def search_ingredients(self):
        db = Database()
        walmart = Walmart()
        
        ingredients = db.get_ingredients()
        
        for ingredient in ingredients:
            walmart.search(ingredient[0][1])
            name, url, price = walmart.get_cheapest()
            
        db.close_connection
            
            