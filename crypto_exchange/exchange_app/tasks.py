from celery import shared_task
from .models import Orders
from django.db import transaction
import logging

# Configure logging
logger = logging.getLogger(__name__)

@shared_task
def match_orders():
    from .utils import OrderBook  
    order_book = OrderBook()

    try:
        
        buy_orders = Orders.objects.filter(order_type='buy').order_by('-price', 'timestamp')
        sell_orders = Orders.objects.filter(order_type='sell').order_by('price', 'timestamp')

        
        for order in buy_orders:
            order_book.add_order(order)

        for order in sell_orders:
            order_book.add_order(order)

        
        matched_orders = order_book.match_orders()

        
        with transaction.atomic():
            for match in matched_orders:
        
                buy_order = Orders.objects.select_for_update().get(id=match['buy_order_id'])
                sell_order = Orders.objects.select_for_update().get(id=match['sell_order_id'])

                buyer = buy_order.user
                seller = sell_order.user

                buyer.profile.usdt_balance -= match['price'] * match['quantity']
                buyer.profile.coin_balance += match['quantity']
                seller.profile.coin_balance -= match['quantity']
                seller.profile.usdt_balance += match['price'] * match['quantity']

                buyer.profile.save()
                seller.profile.save()

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

        logger.info("Orders matched successfully.")

    except Exception as e:
        logger.error(f"Error matching orders: {e}")
        raise
