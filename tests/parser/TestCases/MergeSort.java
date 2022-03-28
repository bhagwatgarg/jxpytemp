package TestCases;

public class MergeSort{
  int a;
  public static void mergeSort(int arr[]){
    mergeSort(arr, 0, arr.length-1);
  }

  private static void mergeSo(int arr[], int l, int r){
    if(r-l<1)return;
    int mid=l+(r-l)/2;
    mergeSort(arr, l,  mid);
    mergeSort(arr, mid+1, r);
    merge(arr, l, r);
  }

  private static void merge(int arr[], int l, int r){
    if(r-l<1)return;
    int n=r-l+1, mid=l+(r-l)/2;
    int n1=l, n2=mid+1, i=0;
    int[] b=new int[n];
    while(n1<=mid && n2<=r){
      if(arr[n1]<arr[n2]){
        b[i++]=arr[n1++];
      }
      else b[i++]=arr[n2++];
    }
    while(n1<=mid)b[i++]=arr[n1++];
    while(n2<=r)b[i++]=arr[n2++];
    i=0;
    while(i<n){
      arr[l+i]=b[i++];
    }
  }
}