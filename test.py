from store import Store
from walmart import Walmart
from database import Database
from ProductPopulator import ProductPopulator

def test_search_and_cheapest():
    wal = Walmart()
    
    wal.login('tanner28aw@gmail.com', 't@12103101')
    print("Logged in...")
    wal.search("butter")
    
    print("Results Dict....")
    for name in wal.results.keys():
        print(name + ": " + str(wal.results[name]))
    
    name, link, price = wal.get_cheapest()
    print('\nCheapest: ' + name + " at: " + str(price))
    
    
populator = ProductPopulator()    
# test_search_and_cheapest()

# wal = Walmart()
# wal.login('', '')
# wal.run_job(1)