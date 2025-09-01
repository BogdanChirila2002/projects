class Comutativ {
  public static void main(String[] ppp) {
    C Ob = new C();
    // System.out.println(Ob.a + Ob.met());  
    System.out.println(Ob.met() + Ob.a);
  }
}

class  C {
  int a=1;
  int met() { return a++; }
}