import java.util.*;

class elem {
  int i; elem st,dr; static elem rad;

  elem() { }
  elem(int ii) { i = ii; }

  void creare() {
    Scanner sc = new Scanner(System.in);
    rad = new elem( sc.nextInt() );
    while ( sc.hasNextInt() ) adaug(rad, sc.nextInt());
  }

  void adaug(elem x, int i) {
     if (i<x.i) 
       if (x.st != null) adaug(x.st,i);
       else x.st = new elem(i);
     else 
       if (x.dr != null) adaug(x.dr,i);
       else x.dr = new elem(i);
  }

  String parcurg(elem x) {
    if (x==null) return("");
    else return( parcurg(x.st) + x.i + " " + parcurg(x.dr));
  }
}

class ArbSort {
  public static void main(String arg[]) { 
    elem Ob = new elem();
    Ob.creare();
    System.out.println(Ob.parcurg(elem.rad));
  }
}
