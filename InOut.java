import java.util.*; import java.io.*;

class InOut {
  public static void main(String[] qqqq) throws Exception {
    Scanner sc = new Scanner(new File("a.b"));
    PrintWriter pw = new PrintWriter(new File("b.a"));
    int s = 0;
   
    while(sc.hasNextInt()) s += sc.nextInt();
    pw.print("Suma = " + s); pw.close();
  }
}
