import java.util.*;

class Scan {
  public static void main(String[] qqq)  {
      Scanner sc = new Scanner(System.in);
      System.out.println("Nume : " + sc.next());
      int i,suma=0;
      while(sc.hasNextInt()) suma += sc.nextInt();
      System.out.println(suma);
    }
}