#############################################
#
# Simple Order Book v1
#
#############################################

import pandas as pd
from collections import OrderedDict

buy_orders = {} # key is price, value is size
sell_orders = {}
trades = []

# clear the book and start over
def new_book():
    buy_orders.clear()
    sell_orders.clear()
    
# add order to book
# assumes matcher has already looked for a cross
def add_order_to_book( px, qty, side ):
    if side == 'b':
        if px in buy_orders:
            buy_orders[ px ] += qty
        else:
            buy_orders[ px ] = qty
    else: # side == 's'
        if px in sell_orders:
            sell_orders[ px ] += qty
        else:
            sell_orders[ px ] = qty

        
# add a new order to the book 
def new_order( order_side, order_price, order_qty, display_book = False ):
    # side = s | b, fail on anything else
    if not ( order_side in [ 'b', 's' ] ):
        print( "Side '" + order_side + "' not supported." )
        return
    # price: float
    # qty: integer
    remaining_order_qty = order_qty
    
    # it's a sell order
    if ( order_side == 's' ):
        # make sure the book isn't empty
        if len( buy_orders ) > 0:
            # loop thru buy orders
            for key in sorted( buy_orders, reverse = True ):
                buy_price = key
                buy_qty = buy_orders[ key ]
                # check for price at this level
                if order_price <= buy_price: # we have at least one match
                    trade_qty = min ( buy_qty, remaining_order_qty )
                    trade_price = buy_price
                    # update order book
                    # remove or reduce order 
                    if buy_qty >= remaining_order_qty:
                        # we have exhausted our order quantity, update the resting quantity
                        if ( buy_qty == remaining_order_qty ):
                            # nothing left at this level, remove it
                            del buy_orders[ buy_price ]
                        else:
                            # update residual order book quantity
                            buy_orders[ buy_price ] -= remaining_order_qty
                        trades.append( ( trade_price, trade_qty ) )

                        break # we're done
                    else: # we have more order left, remove this price level in the book and continue
                        # remove buy order 
                        del buy_orders[ key ]
                        # decrement sell qty
                        remaining_order_qty -= trade_qty

                        # record trade
                        trades.append( ( trade_price, trade_qty ) )
                        continue
                else: # prices didn’t match, so add it to the sell side
                    add_order_to_book( order_price, remaining_order_qty, order_side )
                    break 
        else: # buy book is empty
            add_order_to_book( order_price, remaining_order_qty, order_side )

    # it's a buy  
    else:
        # check to make sure sell book isn't empty
        if len( sell_orders ) > 0:
            # loop thru sell orders
            for key in sorted( sell_orders ):
                sell_price = key
                sell_qty = sell_orders[ key ]
                # check for price at this level
                if order_price >= sell_price: # we have at least one match
                    trade_qty = min ( sell_qty, remaining_order_qty )
                    trade_price = sell_price
                    # update order book
                    # remove or reduce order 
                    if sell_qty >= remaining_order_qty:
                        # we have exhausted our order quantity, update the resting quantity
                        if ( sell_qty == remaining_order_qty ):
                            # nothing left at this level, remove it
                            del sell_orders[ sell_price ]
                        else:
                            # update residual order book quantity
                            sell_orders[ sell_price ] -= remaining_order_qty
                        trades.append( ( trade_price, trade_qty ) )
                        break # we're done
                    else: # we have more order left, remove this price level in the book and continue
                        # remove buy order 
                        del sell_orders[ key ]
                        # decrement sell qty
                        remaining_order_qty -= trade_qty

                        # record trade
                        trades.append( ( trade_price, trade_qty ) )
                        continue
                else: # prices didn’t match, so add it to the sell side
                    add_order_to_book( order_price, remaining_order_qty, order_side )
                    break 
        else: # book is empty
            add_order_to_book( order_price, remaining_order_qty, order_side )
    if display_book:
        show_book()


# populate a dummy book for testing
# TODO: change this to use methods
def dummy_book():
    clear_book()
    
    # add some buys and sells
    buy_orders[ 99.50 ] = 1000
    buy_orders[ 99.00 ] = 900
    sell_orders[ 100.02 ] = 2500
    sell_orders[ 100.50 ] = 1900
    sell_orders[ 101.01 ] = 200

def show_book():
    buy_qty = []
    buy_price = []
    sell_price = []
    sell_qty = []
    for key in sorted( buy_orders, reverse = True ):
        buy_price.append( key )
        buy_qty.append( int( buy_orders[key] ) )
    for key in sorted( sell_orders ):
        sell_price.append( key)
        sell_qty.append( sell_orders[key] )
    
    d = OrderedDict( B_QTY = buy_qty, B_PX = buy_price, S_PX = sell_price, S_QTY = sell_qty )
    display_book = pd.DataFrame( OrderedDict( [ ( k, pd.Series( v ) ) for k, v in d.items() ] ) )
    display(display_book)
      
# return best bid and offer
def get_BBO():
    return ( max( buy_orders.items() ), 
            min( sell_orders.items() ) )