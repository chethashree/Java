import java.util.Scanner;
public class armstrong_check {
    public static void main(String[]args){
        Scanner sc = new Scanner(System.in);
        System.out.print("Enter a number: ");
        int num = sc.nextInt();
        int originalNum = num, result = 0, digits = 0;

        while (originalNum != 0) {
            digits++;
            originalNum /= 10;
        }

        originalNum = num;
        while (originalNum != 0) {
            int remainder = originalNum % 10;
            result += Math.pow(remainder, digits);
            originalNum /= 10;
        }

        if (result == num) {
            System.out.println(num + " is an Armstrong number.");
        } else {
            System.out.println(num + " is not an Armstrong number.");
        }
    }
}
