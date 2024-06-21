def calculating_total_cost(cart_items):
    total_cost = sum(item.item.price * item.quantity for item in cart_items)
    return total_cost if total_cost else 0
