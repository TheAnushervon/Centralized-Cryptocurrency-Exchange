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
        if order.symbol not in self.order_books:
            self.order_books[order.symbol] = {'buy_orders': [], 'sell_orders': []}

        if order.order_type == 'buy':
            heapq.heappush(self.order_books[order.symbol]['buy_orders'], (-order.price, order.timestamp, order))
        else:
            heapq.heappush(self.order_books[order.symbol]['sell_orders'], (order.price, order.timestamp, order))

    def match_orders(self):
        matched_orders = []
        for symbol, books in self.order_books.items():
            while books['buy_orders'] and books['sell_orders']:
                buy_price, buy_timestamp, buy_order = books['buy_orders'][0]
                sell_price, sell_timestamp, sell_order = books['sell_orders'][0]

                if -buy_price >= sell_price:
                    matched_quantity = min(buy_order.quantity, sell_order.quantity)
                    buy_order.quantity -= matched_quantity
                    sell_order.quantity -= matched_quantity

                    matched_orders.append({
                        'symbol': symbol,
                        'buy_order_id': buy_order.order_id,
                        'sell_order_id': sell_order.order_id,
                        'price': sell_price,
                        'quantity': matched_quantity
                    })

                    if buy_order.quantity == 0:
                        heapq.heappop(books['buy_orders'])
                    if sell_order.quantity == 0:
                        heapq.heappop(books['sell_orders'])
                else:
                    break

        return matched_orders
