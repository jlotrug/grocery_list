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

def get_error_list(item):
    error_list = []
    print(item.item_protein)

    if not item.item_carbs.isnumeric():
        error_list.append("Carbs must be a numeric value")
    if not item.item_fat.isnumeric():
        error_list.append("Fat must be a numeric value")
    if not item.item_protein.isnumeric():
        error_list.append("Protein must be a numeric value")
    if not item.item_calories.isnumeric():
        error_list.append("Calories must be a numeric value")

    return error_list
