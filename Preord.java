import java.util.*;

class Preord {
  public static void main(String[] arfs) {
    ArbBin Ob = new ArbBin();
    Ob.creare();
    System.out.print("Preordine :\t");  Ob.pre(Ob.rad);
   }
}

class ArbBin {
  int rad; int nv;
  int[] st,dr;

  void creare() {
    Scanner sc = new Scanner(System.in);
    System.out.print("Nr. varfuri : "); nv =  sc.nextInt();
    st = new int[nv]; dr = new int[nv];
    System.out.print("Radacina : "); rad = sc.nextInt();
    for (int i=0; i<nv; i++) {
      System.out.print(" st si dr al varfului " + i + ": ");
      st[i] = sc.nextInt(); dr[i] = sc.nextInt();
    }
  }

  void pre(int x) {
    if( x<0 );
    else { 
      System.out.print(x + "  "); pre(st[x]); pre(dr[x]); 
    }
  }

} 
