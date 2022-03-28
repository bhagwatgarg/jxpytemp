// package TestCases;

public class BinarySearch{

  int p,q,r,s;
  // char po, pl;
  // float x,y,z;
  double hi;
  public static int search(int[] arr, int num){
    int a[] = new int[5];// = {1,2,3,4,5};
    int lef=0, righ=5, mid=0;
    while(lef<=righ){
      int a = 5;
      mid=lef+(righ-lef)/2;
      if(arr[mid]==num)return mid;
      if(arr[mid]<num)lef=mid+1;
      else righ=mid-1;
    }
    return -1;
  }

  public static int _hello (){
		int arr = 5;
		return arr;
	}	
}

class Main{
	public static int hello (){
		BinarySearch[] a = new BinarySearch[10];
		// int[] arr = {1,2,3,4,5};
		// return a.search(arr, 3);
    return 1;
	}	
}
