import java.util.*;

class ArbNiv1 {
  public static void main(String[] s) {
    new nivel();
  }
}

class nivel {      
  int[][] mat; int n;

  nivel() {
    int[] temp; int ntemp;
    Scanner sc = new Scanner(System.in);
    System.out.print("n= "); n = sc.nextInt();
    mat = new int[n][]; temp = new int[n];
    for (int i=0; i<n; i++) {
      System.out.print("Fiii lui " + i + " : "); 
      ntemp = 0; 
      while( sc.hasNextInt() ) temp[ntemp++] = sc.nextInt();
      sc.next();
      mat[i] = new int[ntemp];
      for (int j=0; j<ntemp; j++) mat[i][j] = temp[j];
    }
    System.out.println("**************");
    parcurgere();
  }

  void parcurgere() {
    int i,j,k;
    ArrayList<Integer> coada = new ArrayList();
    // radacina este varful 0 !!!
    coada.add(0);
    while ( ! coada.isEmpty() ) {
      i = coada.get(0); coada.remove(0);
      System.out.print(i+"  ");
      for (k=0; k<mat[i].length; k++) {
        j = mat[i][k]; coada.add(j);
      }
    }
  }
}
