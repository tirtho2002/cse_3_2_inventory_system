import pandas as pd
import random


def run_inventory_simulation(days=100, s=20, S=100, lead_time=3, initial_stock=50, max_demand=15):
    stock = initial_stock
    orders_in_transit = []

    log = []

    for day in range(days):


        delivered_today = 0
        remaining_transit = []

        for arrival_day, qty in orders_in_transit:
            if arrival_day == day:
                stock += qty
                delivered_today += qty
            else:
                remaining_transit.append((arrival_day, qty))

        orders_in_transit = remaining_transit


        demand = random.randint(0, max_demand)


        shortage = max(0, demand - stock)
        stock = max(0, stock - demand)


        if stock <= s:
            order_qty = S - stock
            arrival_day = day + lead_time
            orders_in_transit.append((arrival_day, order_qty))


        in_transit = sum(qty for _, qty in orders_in_transit)


        log.append({
            "Day": day + 1,
            "Demand": demand,
            "Ending_Stock": stock,
            "Shortage": shortage,
            "In_Transit": in_transit
        })

    df = pd.DataFrame(log)
    return df



df = run_inventory_simulation(
    days=100,
    s=20,
    S=100,
    lead_time=3,
    initial_stock=50,
    max_demand=15
)


print(df.to_string(index=False))