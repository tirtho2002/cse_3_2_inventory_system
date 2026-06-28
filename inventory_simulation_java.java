import java.util.*;

public class inventory_simulation_java {

    public static void main(String[] args) {

        Random random = new Random(42);

        int S = 60;          // Maximum inventory
        int s = 20;          // Reorder point
        int inventory = 52;  // Initial inventory

        HashMap<Integer, Integer> pendingOrders = new HashMap<>();

        System.out.println("Time\tInventory\tEvent");

        for (int time = 0; time <= 10; time++) {
  
            // Order arrives
            if (pendingOrders.containsKey(time)) {`
                int qty = pendingOrders.get(time);
                inventory += qty;
                pendingOrders.remove(time);

                System.out.println(time + "\t" + inventory +
                        "\tOrder Arrived (+" + qty + ")");
            }

            int demand = random.nextInt(10) + 5;
            inventory -= demand;

            System.out.println(time + "\t" + inventory +
                    "\tDemand = " + demand);

            if (time % 2 == 0) {

                int onOrder = 0;
                for (int qty : pendingOrders.values())
                    onOrder += qty;

                int inventoryPosition = inventory + onOrder;

                if (inventoryPosition < s) {

                    int orderQty = S - inventoryPosition;

                    int arrivalTime = time + random.nextInt(2) + 1;

                    pendingOrders.put(arrivalTime, orderQty);

                    System.out.println(
                        "   --> Ordered " + orderQty +
                        " units. Arrival at time " + arrivalTime);
                }
            }

            System.out.println("--------------------------------");
        }

        System.out.println("Final Inventory = " + inventory);
    }
}