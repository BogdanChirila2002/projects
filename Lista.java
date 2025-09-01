import java.util.*;

class Lista {
  public static void main(String[] qqq) {
    L Ob = new L();
    System.out.print("\nDirect : "); Ob.direct(Ob.p); 
    System.out.print("\nInvers : "); Ob.invers(Ob.p);
  }
}

class Elem {
  int val; Elem leg;
  Elem(int v) { val = v; } 
}

class L {
  Elem p,u,x;
  L() {
    Scanner sc = new Scanner(System.in);
    p = new Elem(sc.nextInt()); u = p;
    while (sc.hasNextInt()) {
      x = new Elem(sc.nextInt()); u.leg = x; u =x;
    }
  }

  void direct(Elem x) {
    if (x == null) {}
    else { System.out.print(x.val + "\t"); direct(x.leg); }
  }

  void invers(Elem x) {
    if (x != null) {
      invers(x.leg); System.out.print(x.val + "\t"); 
    }
  }

}