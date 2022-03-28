package TestCases;
public class Graph{
  int vertices;
  int[][] adj;
  int[] keys;
  private boolean[] visited;
  public void _Graph(int vertices, int[] keys, int[][] adj){
    this.vertices=vertices;
    this.adj=new int[vertices][];
    this.keys=new int[vertices];
    this.visited=new boolean[vertices];
    for(int i=0; i<vertices; i++)this.keys[i]=keys[i];
    for (int i=0; i<vertices; i++){
      this.adj[i]=new int[adj[i].length];
      for(int j=0; j<adj[i].length; j++)this.adj[i][j]=adj[i][j];
    }
  }
  
    private boolean dfs(int v, int key){
      if(this.visited[v])return false;
      this.visited[v]=true;
      if(this.keys[v]==key)return true;
      boolean result=false;
      for(int i=0; i<this.adj[v].length; i++){
        result=dfs(this.adj[v][i], key);
        if(result)return result;
      }
      return false;
    }
  
  public boolean _dfs(int key){
    boolean result=false;
    for(int i=0; i<this.vertices; i++)this.visited[i]=false;
    for(int i=0; i<this.vertices; i++){
      if(!this.visited[i]){
        result=dfs(i, key);
        if(result)return true;
      }
    }
    return false;
  }
}