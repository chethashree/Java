// import java.util.Scanner;
// public class ReplaceZeroWithFive {
//         public static void main(String[] args) {
//         Scanner scanner = new Scanner(System.in);
//         System.out.print("Enter a number: ");
//         int num = scanner.nextInt();

//         String newNumStr = String.valueOf(num).replace('0', '5');
//         int newNum = Integer.parseInt(newNumStr);
//         System.out.println("New number: " + newNum);
//     }
// }


import java.util.Scanner;

public class ReplaceZeroWithFive {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter a number: ");
        String numStr = scanner.nextLine(); 

        
        if (numStr.replace("0", "").isEmpty()) {
            
            System.out.println("New number: " + "5".repeat(numStr.length()));
        } else {
            
            String newNumStr = numStr.replace('0', '5');
            System.out.println("New number: " + newNumStr);
        }
    }
}

