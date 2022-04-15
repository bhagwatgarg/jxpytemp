// package TestCases;

public class BinarySearch{

  int p,q,r,s;
  // char po, pl;
  // float x,y,z;
  double hi;
  boolean a = true;
  // int b = NULL;

  public int search(int[] arr, int num){
    int a[] = new int[5];// = {1,2,3,4,5};
    this.search(arr, num);
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

  public int hello (){
    int[] ar = new int[10];
		this.search(ar, 3);
    this.hello();
		int arr = 5;
		return arr;
	}	

  public static int hello(int a, int b)
  {
    return 1;
  }

  public static int hello(int a)
  {
    return 1;
  }

}

class BinaryWrapper{
  BinarySearch a;
  int i;
  void search(int[] arr, int b){}
}

class Main{
	public static int hello (){
		// BinarySearch a = new BinarySearch();
    BinaryWrapper a=new BinaryWrapper();
		int[] arr = new int[10];
		a.search(arr, 3);
    a.a.search(arr, 2);
    // a.i=2;
    return 1;
	}	
}