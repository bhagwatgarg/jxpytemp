// package TestCases;

public class BinarySearch{
  public statc int search(int[] arr, int num){
    int lef=0, righ=arr.length - 1, mid=0;
    while(lef<=righ){
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
		BinarySearch a = BinarySearch();
		int[] arr = {1,2,3,4,5};
		return a.search(arr, 3);
	}	
}
