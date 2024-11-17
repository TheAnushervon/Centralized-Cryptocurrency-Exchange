from celery import shared_task
from .models import Orders
from django.db import transaction
import heapq

@shared_task
def match_orders():
    from .utils import OrderBook  # Ensure the OrderBook logic is accessible
    order_book = OrderBook()

    # Fetch all active buy and sell orders
    buy_orders = Orders.objects.filter(order_type='buy').order_by('-price', 'timestamp')
    sell_orders = Orders.objects.filter(order_type='sell').order_by('price', 'timestamp')

    # Add orders to the FIFO order book
    for order in buy_orders:
        order_book.add_order(order)

    for order in sell_orders:
        order_book.add_order(order)

    # Match orders
    matched_orders = order_book.match_orders()

    # Update the database within a transaction
    with transaction.atomic():
        for match in matched_orders:
            # Update buyer and seller balances
            buy_order = Orders.objects.get(id=match['buy_order_id'])
            sell_order = Orders.objects.get(id=match['sell_order_id'])

            # Deduct/credit balances (example logic)
            buyer = buy_order.user
            seller = sell_order.user

            # Assume buyer/seller balances are stored in User's profile
            buyer.profile.usdt_balance -= match['price'] * match['quantity']
            buyer.profile.coin_balance += match['quantity']
            seller.profile.coin_balance -= match['quantity']
            seller.profile.usdt_balance += match['price'] * match['quantity']

            buyer.profile.save()
            seller.profile.save()

            # Remove or update orders
            if buy_order.quantity == match['quantity']:
                buy_order.delete()
            else:
                buy_order.quantity -= match['quantity']
                buy_order.save()

            if sell_order.quantity == match['quantity']:
                sell_order.delete()
            else:
                sell_order.quantity -= match['quantity']
                sell_order.save()
