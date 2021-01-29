#!/python-mysqldb_1.2.3-2ubuntu1_amd64.deb
import pymysql.cursors

class Database(object):
    def __init__(self):
        self.db = pymysql.connect(host="us-cdbr-iron-east-05.cleardb.net",
                                  user="b1257ec0f3455d",
                                  passwd="f483f285",
                                  db="heroku_5d2941f1ecc4e61")
       
        
    def get_checklist_ingredients(self, user_id):
        print("Getting ingredients")
        sql = "SELECT * FROM checkout_lists WHERE user_id="+str(user_id)+";"
        
        cursor = self.db.cursor()
        
        try:
           # Execute the SQL command
           cursor.execute(sql)
           # Fetch all the rows, return a list
           checklist = cursor.fetchall()
        except:
           print ("Error: Could not fetch checklist")
           
        ingredients = []   
        for ingredient in checklist:
            sql = "SELECT * FROM ingredients WHERE id="+str(ingredient[2])+";"
            
            try:
               cursor.execute(sql)
               ingred = cursor.fetchall()
               ingredients.append(ingred)
            except:
                print ("Error: Could not fetch ingredient")
                
        return ingredients
           
           
    
    def get_products(self, ingredients):
        print("Getting products")
        products = []
        for ingredient in ingredients:
            print(ingredient[0])
            sql = "SELECT * FROM products WHERE id="+str(ingredient[0][4])+";"
            cursor = self.db.cursor()
            
            try:
               cursor.execute(sql)
               prod = cursor.fetchall()
               products.append(prod)
            except:
                print ("Error: Could not fetch product")
                
        return products
        
        
    def close_connection(self):
        # Disconnect from server
        self.db.close()
        
        
    def get_ingredients(self):
        sql = "SELECT * FROM ingredients WHERE id > 1;"
        cursor = self.db.cursor()
        
        try:
           cursor.execute(sql)
           ingredients = cursor.fetchall()
        except:
            print ("Error: Could not fetch ingredients")
        return ingredients
        
       
    def insert_product_asc(self, fid, name):
        cursor = self.db.cursor()
        try:
            sql = "Update ingredients SET product_id="+fid+" WHERE name='"+name+"'"
            self.db.commit()
            
        except Exception as e:
            print("Could not insert asc")
            print(format(e))
        
    def insert_product(self, name, url, price):
        cursor = self.db.cursor()
        try:
            # Create a new record
            sql = "INSERT INTO products (name, price, walmart_url) VALUES (%s, %s, %s)"
            cursor.execute(sql, (name, price, url))
            self.db.commit()
 
        except Exception as e:
            print("Could not insert " + name)
            print(format(e))
            
    def get_count(self, tab_name):
        cursor = self.db.cursor()
        try:
            # Create a new record
            sql = "SELECT COUNT(*) FROM "+ tab_name + ";"
            cursor.execute(sql)
            return cursor.fetchall()[0]
                
        except:
            print("Error in getting count")
            
            
# db = Database()
# check = db.get_checklist_ingredients(1)
# print(check)
# db.close_connection()