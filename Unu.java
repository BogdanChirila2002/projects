class C {
  int a; boolean b;
  C(int aa, boolean bb) { a = aa; b = bb; }
  C() { a = 13; }
  void met() {
    System.out.println(a + " " + b);
  }
  boolean met(int b) { return a<b; }
}

class Unu {
  public static void main(String[] qqq) {
    for(int i=0; i<qqq.length; i++) System.out.print(qqq[i] + "\t");
    C Ob = new C(11,false);
    System.out.println(Ob.a + " " + Ob.b );
    Ob.met();
    C Ob1 = new C(); 
    System.out.println( Ob1.met(15)) ;
  }
}
