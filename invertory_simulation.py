import matplotlib.pyplot as plt
import numpy as np

# --- Simulation Parameters ---
np.random.seed(42)  # For reproducible random demands and lags
SIM_TIME = 4.0  # Total time steps to simulate
DT = 0.01  # Small time step for high-resolution plotting
S_max = 60  # Upper inventory limit (S)
s_min = 20  # Reorder point (s)

# Review times (e.g., at integer times 1, 2, 3...)
review_times = [1.0, 2.0, 3.0]

# --- Generate Random Events ---
demand_times = sorted(np.random.uniform(0.1, SIM_TIME, size=12))
demand_sizes = np.random.randint(5, 15, size=12)

# Tracks active orders: dictionary mapping arrival_time -> order_quantity
pending_orders = {}
delivery_lag_mean = 0.4

# --- Simulation Loop Setup ---
time_steps = np.arange(0, SIM_TIME + DT, DT)
I_history = []
I_plus_history = []
I_minus_history = []

# Initial state
current_inventory = 100

print("=" * 60)
print(f"{'TIME':<8} | {'NET INV':<10} | {'ON-HAND':<10} | {'SHORTAGE':<10} | {'PENDING'}")
print("=" * 60)

# Processing the simulation time-step by time-step
for t in time_steps:
    # 1. Check if an order arrives
    arrived_orders = [
        eta for eta in pending_orders if abs(t - eta) < DT / 2 or (t >= eta and t - DT < eta)
    ]
    for eta in arrived_orders:
        qty = pending_orders.pop(eta)
        print(f"[{t:4.2f}]   *** ORDER ARRIVED: +{qty} units ***")

    # 2. Check if a demand occurs
    for d_time, d_size in zip(demand_times, demand_sizes):
        if t - DT < d_time <= t:
            current_inventory -= d_size

    # Calculate current split statuses
    on_hand = max(0, current_inventory)
    shortage = max(0, -current_inventory)
    on_order = sum(pending_orders.values())

    # 3. Review period check & Status Output
    for r_time in review_times:
        if t - DT < r_time <= t:
            inventory_position = current_inventory + on_order
            status_msg = ""

            if inventory_position < s_min:
                order_qty = S_max - inventory_position
                lag = np.random.exponential(delivery_lag_mean)
                pending_orders[t + lag] = order_qty
                status_msg = f"-> PLACED ORDER: {order_qty} units"
                on_order += order_qty  # update for immediate print readout

            print(
                f"t = {t:<4.1f} | {current_inventory:<10} | {on_hand:<10} | {shortage:<10} | {on_order:<7} {status_msg}"
            )

    # 4. Record Metrics for graphing
    I_history.append(current_inventory)
    I_plus_history.append(on_hand)
    I_minus_history.append(shortage)

print("=" * 60)
print("\n### FINAL PRODUCT STATUS SUMMARY ###")
print(f"Current Net Inventory I(t):       {current_inventory}")
print(f"Current On-Hand Stock I+(t):      {max(0, current_inventory)}")
print(f"Current Stock Shortage I-(t):    {max(0, -current_inventory)}")
print(f"Total Stock Securely On-Order:    {sum(pending_orders.values())}")
print("-" * 60)

# --- Plotting the Simulation Result ---
plt.figure(figsize=(12, 7))

plt.step(time_steps, I_history, where="post", color="black", linewidth=2, label="$I(t)$ (Net Inventory)")
plt.step(
    time_steps,
    I_plus_history,
    where="post",
    color="black",
    linestyle=":",
    linewidth=2,
    label="$I^+(t)$ (On-hand)",
)
plt.step(
    time_steps,
    I_minus_history,
    where="post",
    color="black",
    linestyle="-.",
    linewidth=2,
    label="$I^-(t)$ (Shortages)",
)

plt.axhline(y=S_max, color="gray", linestyle="--", alpha=0.5)
plt.axhline(y=s_min, color="gray", linestyle="--", alpha=0.5)
plt.yticks([0, s_min, S_max], ["0", "$s$", "$S$"])
plt.xticks(review_times, [str(int(r)) for r in review_times])

plt.title("SIMULATION OF AN INVENTORY SYSTEM", fontsize=16, fontweight="bold", pad=20)
plt.xlabel("Time ($t$)", fontsize=12)
plt.ylabel("Inventory Level", fontsize=12)
plt.legend(title="Key", loc="upper right", frameon=True)

plt.gca().spines["top"].set_visible(False)
plt.gca().spines["right"].set_visible(False)
plt.axhline(0, color="black", linewidth=1)
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.show()