
import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

public class MultiplyTwoNumbers {
	public static void main(String[] args) throws FileNotFoundException {
		File fd = new File(args[0]);
		Scanner scan = new Scanner(fd);
		int total = scan.nextInt() * scan.nextInt();
		
		scan.close();
		
		System.out.println(total);
	}
}