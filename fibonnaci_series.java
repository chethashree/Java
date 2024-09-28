import java.util.Scanner;
public class fibonnaci_series {
    public static void main(String[]args){
Scanner sc=new Scanner(System.in);
System.out.print("Enter number of terms : ");
int n=sc.nextInt();
int first=0,second=1,next;
System.out.println("Fibonnaci series upto "+n+" terms is : ");
System.out.print(first);
System.out.print(" "+second);
for(int i=3;i<=n;i++){
 
    next=first+second;
    System.out.print(" "+next);
    first=second;
    second=next;

}
    }
}
