package TestCases;

public class BinarySearch{

  int p,q,r,s;
  // char po, pl;
  // float x,y,z;
  double hi;
  boolean a = true;
  // int b = NULL;

<<<<<<< HEAD
  public static int search(int[] arr, int num){
=======
  public int search(int[] arr, int num){
>>>>>>> Method Invocation and Overloading working (again)
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

  public static int hello (){
		int arr = 5;
		return arr;
	}	

  // public static int hello(int a, int b)
  // {
  //   return 1;
  // }

  // public static int hello(int a, int b)
  // {
  //   return 1;
  // }

}

class Main{
	public static int hello (){
		BinarySearch a = new BinarySearch();
		int[] arr = {1,2,3,4,5};
		a.search(arr, 3);
    return 1;
	}	
}