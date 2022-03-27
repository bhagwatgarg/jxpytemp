import java.lang.String;

import TestCases.*;

// Single line comment
/* Another Single line comment */
/**
  * Multi line comment
  *
*/

/**
  * Non Trivial Programs:
  * Merge Sort
  * Graph and DFS
  * Binary Search
*/
class Main {
  int a = 4;
  void main(String[] args, int lol) {
    // System.out.println("Hello world!");
    // ;
    
    // Operators.literals_and_operators();
    // Operators.loops();


    // int[] arr={12, 22, 1, 0, -11, 3, 4};
    // MergeSort.mergeSort(arr);
    // printArray(arr);
    // System.out.println("[SUCCESS] MergeSort");

    // System.out.println(BinarySearch.search(arr, 4));
    // System.out.println(BinarySearch.search(arr, 2));
    // System.out.println("[SUCCESS] BinarySearch");

    if(a == 4)
    {
      int q = 3;
    }
    else
    {
      int j = 9;
    }

    for(int i = 0; i < 10; ++i)
    {
      int k = 5;
    }
    
    int b = 5;
    int[][] keys = new int[5][6];//={112, 3, 5, 183, 7};
    // int vertices=keys.length;
    int[][] adj={{1, 4, 2}, {}, {2}, {0, 3}, {0, 1, 2, 3}};
    Graph g=new Graph(vertices, keys, adj);
    // System.out.println(g.dfs(4));
    // System.out.println(g.dfs(7));
    // System.out.println("[SUCCESS] Graph");
  }

  // private static void printArray(int[] arr){
  //   for(int i=0; i<arr.length; i++){
  //     System.out.printf("%d ", arr[i]);
  //   }
  //   System.out.println();

  // }

}