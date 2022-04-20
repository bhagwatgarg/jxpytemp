class Test2{
  int v1, v;
  void yomama(){}
}


class Test{
  int v;
  Test2 t2;
  void Test(int i){}
  void Test(){}
  int test_func(int a, int b){
    a=23;
    this.t2.v=23;
    this.test_func(a, b);
    this.t2.v1=1;
    return a+2;
  }
}


public class Main {
  void main(){
    Test t=new Test();
    Test t2=new Test(1);
    t.t2.yomama();
    // t.t2.v=1;
    // t.test_func(1, 2);
    int[][] arr=new int[5][10];
    arr[2][3]=1;
    // int[] arr2=new int[1];
    // arr2[0]=1;
    return;
  }
}