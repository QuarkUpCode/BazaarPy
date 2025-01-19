import requests
import json
import time
from math import floor


DEFAULT_ENDPOINT = "https://api.hypixel.net/v2/skyblock/bazaar"


class BazaarItem():

	def __init__(self, quantity:int, price:float):
		
		self.quantity:int = quantity
		self.price:float = price
	
	def __str__(self):
		return f"< {self.quantity}\t@\t{self.price}/u >"

class BazaarItemPair():

	def __init__(self, buy_order:BazaarItem, sell_offer:BazaarItem):
		
		self.buy_order:BazaarItem = buy_order
		self.sell_offer:BazaarItem = sell_offer
	
	def __str__(self):
		return f"Buy order :\t{str(self.buy_order)}\nSell offer :\t{str(self.sell_offer)}"




class BazaarAPI():
	
	def __init__(self):
		
		self.endpoint:str = DEFAULT_ENDPOINT
		self.content:dict[str, dict] = None
		self.last_update:float = 0
		self.min_delay:float = 1

		self.watchlist = []
	

	def update_watchlist(self, watchlist:list[str]):
		self.watchlist = watchlist.copy()

	def loadf(self, filename:str):
		with open(filename, 'r') as f:
			self.content = json.loads(f.read())

	def update(self):
		
		if(self.min_delay - (time.time() - self.last_update)) > 0 : time.sleep(self.min_delay - (time.time() - self.last_update))

		r = requests.get(self.endpoint).content
		self.content = json.loads(r)

		self.last_update = time.time()

	def search_id(self, query:str) -> list[str]:
		
		f = []
		for key in self.content["products"].keys():
			
			if query.lower() in str(key).lower():
				f.append(key)

		return f
		#could add deeper search with SequenceMatcher

	def get_item(self, item_name:str) -> dict[str, list]:

		if not (item_name in self.content["products"].keys()):
			print(f"ERROR : key {item_name} not found.")
			return {"product_id":None, "sell_summary":[], "buy_summary":[]}
		
		return self.content["products"][item_name]

	def get_top_orders(self, item_name:str):

		bo = self.get_item(item_name)["sell_summary"][0]
		so = self.get_item(item_name)["buy_summary"][0]

		return BazaarItemPair(BazaarItem(bo["amount"], bo["pricePerUnit"]), BazaarItem(so["amount"], so["pricePerUnit"]))
	
	def get_summary(self):

		print(f"\n\n\n=== {floor(time.time())} ===\n")
		
		for product in self.watchlist:
			print(f"\n>>> {' '.join([x.capitalize() for x in product.lower().split('_')])} <<<\n")
			print(self.get_top_orders(product))