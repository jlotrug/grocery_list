def get_list_total(items):
    total = 0

    for item in items:
        total += (item.item_id.item_price * item.quantity)

    return total

def get_list_calorie_count(items):
    total = 0

    for item in items:
        total += (int(item.item_id.item_calories) * item.quantity)

    return total
