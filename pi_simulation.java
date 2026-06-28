import java.util.Random;

public class MonteCarloPi {
    public static void main(String[] args) {
        int totalPoints = 1000000;
        int insideCircle = 0;

        Random rand = new Random();

        for (int i = 0; i < totalPoints; i++) {
            double x = rand.nextDouble();
            double y = rand.nextDouble();

            if (x * x + y * y <= 1) {
                insideCircle++;
            }
        }

        double pi = 4.0 * insideCircle / totalPoints;
        System.out.println("Estimated Pi = " + pi);
    }
}