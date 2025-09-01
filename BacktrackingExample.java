import java.util.ArrayList;
import java.util.List;

public class BacktrackingExample {

    public static void main(String[] args) {
        int n = 4;
        int k = 2;
        generateCombinations(n, k);
    }

    private static void generateCombinations(int n, int k) {
        List<Integer> currentCombination = new ArrayList<>();
        backtrack(1, n, k, currentCombination);
    }

    private static void backtrack(int start, int n, int k, List<Integer> currentCombination) {
        if (currentCombination.size() == k) {
            System.out.println(currentCombination);
            return;
        }

        for (int i = start; i <= n; i++) {
            currentCombination.add(i);
            backtrack(i + 1, n, k, currentCombination);
            currentCombination.remove(currentCombination.size() - 1);
        }
    }
}
