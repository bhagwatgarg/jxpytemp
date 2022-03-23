// package TestCases;

class BinarySearch{
  int search(int[] arr, int num){
    int lef=0, righ=4, mid;
    while(lef<=righ){
      mid=lef+(righ-lef)/2;
      if(arr[mid]==num)return mid;
      if(arr[mid]<num)lef=mid+1;
      else righ=mid-1;
    }
    return -1;
  }
}
