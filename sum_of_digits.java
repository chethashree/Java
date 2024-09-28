import java.util.Scanner;
public class sum_of_digits {
    public static void main(String[]args){
        Scanner sc = new Scanner(System.in);
        System.out.print("Enter a number  : ");
        int num=sc.nextInt();
        int sum=0;
        while(num!=0){
            sum+=num%10;
            num=num/10;
        }
        System.out.println("Sum of digits of the number is : "+sum);
    }  
}
