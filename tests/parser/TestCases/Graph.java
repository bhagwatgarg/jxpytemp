package TestCases;
public class Graph{
  int vertices;
  int[][] adj1;
  int[] keys_1;
  private boolean[] visit;
  public void _Graph(int vertices, int[] keys, int[][] adj){
    adj1=new int[vertices][];
    keys_1=new int[vertices];
    visit=new boolean[vertices];
    for(int i=0; i<vertices; i++)keys_1[i]=keys[i][1];
    for (int i=0; i<vertices; i++){
      adj1[i]=new int[1000];
      for(int j=0; j<1000; j++)adj1[i][j]=adj[i][j];
    }
  }
  

  
  
}