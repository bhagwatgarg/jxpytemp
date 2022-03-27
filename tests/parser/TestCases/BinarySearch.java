// package TestCases;

public class BinarySearch{
  public static int search(int[] arr, int num){
    int a[] = new int[5];// = {1,2,3,4,5};
    int lef=0, righ=5, mid=0;
    int a = 3;
    while(lef<=righ){
      int a = 5;
      mid=lef+(righ-lef)/2;
      if(arr[mid]==num)return mid;
      if(arr[mid]<num)lef=mid+1;
      else righ=mid-1;
    }
    return -1;
  }
}

class Main{
	public static int hello (){
		BinarySearch a = new BinarySearch();
		int[] arr = {1,2,3,4,5};
		return a.search(arr, 3);
	}	
}
