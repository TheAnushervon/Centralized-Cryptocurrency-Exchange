import heapq
import time

class Order:
    def __init__(self, order_id, symbol, order_type, price, quantity, timestamp=None):
        self.order_id = order_id
        self.symbol = symbol  
        self.order_type = order_type  
        self.price = price
        self.quantity = quantity
        self.timestamp = timestamp or time.time()

    def __lt__(self, other):
        if self.order_type == 'buy':
            return (self.price, self.timestamp) > (other.price, other.timestamp)  
        else:
            return (self.price, self.timestamp) < (other.price, other.timestamp)  

class OrderBook:
    def __init__(self):
        self.order_books = {}

    def add_order(self, order):
        """Add a new order to the order book."""
        if order.symbol not in self.order_books:
            self.order_books[order.symbol] = {'buy_orders': [], 'sell_orders': []}

        if order.order_type == 'buy':
            
            heapq.heappush(self.order_books[order.symbol]['buy_orders'], (-order.price, order.timestamp, order))
        else:
            
            heapq.heappush(self.order_books[order.symbol]['sell_orders'], (order.price, order.timestamp, order))

    def match_orders(self):
        """Match buy and sell orders and return the matched orders."""
        matched_orders = []

        for symbol, books in self.order_books.items():
            buy_orders = books['buy_orders']
            sell_orders = books['sell_orders']

            while buy_orders and sell_orders:
            
                buy_price, buy_timestamp, buy_order = buy_orders[0]
                sell_price, sell_timestamp, sell_order = sell_orders[0]

            
                if -buy_price >= sell_price:
            
                    matched_quantity = min(buy_order.quantity, sell_order.quantity)

            
                    buy_order.quantity -= matched_quantity
                    sell_order.quantity -= matched_quantity

            
                    matched_orders.append({
                        'symbol': symbol,
                        'buy_order_id': buy_order.order_id,
                        'sell_order_id': sell_order.order_id,
                        'price': sell_price,
                        'quantity': matched_quantity,
                    })

            
                    if buy_order.quantity == 0:
                        heapq.heappop(buy_orders)
                    if sell_order.quantity == 0:
                        heapq.heappop(sell_orders)

                else:
                    
                    break

        return matched_orders