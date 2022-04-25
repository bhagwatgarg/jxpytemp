// TODO: function parameters should be accessed with rbp+


// ++ +=
// TODO: add in pec: need {} in for, while, if
class Math{
  void Math(){return;}
  declare int max(int a, int b);
  declare int min(int a, int b);
  declare int signum(int a);
  declare int abs(int a);
  declare int is_prime(int a);
  declare int square(int a);
  declare int cube(int a);
}
class Imports{
  // void print(int a){return;}
  declare void print(int a);
  declare int scan_int();
  void Imports(){return ;}
}

class Main{
  // declare int fact2(int b);
  int fact(int b){
    if(b==0){return 1;}
    else{
        int k=b-1;
        int k1=this.fact(k);
        return b*k1;
    }
    return 0;
  }
  int fact(int b, int r, int p){
    if(b==r){return r*p;}
    else{
        int k=b-1;
        int k1=this.fact(k, r, p);
        return b*k1;
    }
    return 0;
  }
  void Main(){return;}
  int main(){
    Imports imp=new Imports();
    int a =5, _b = 6, c_ = 7;
    // a=5;
    // int i;
    // for(int i=0; i <10; i=i+1){
    // while(a<10){
    //   a=a+1;
    //   for(int i = 0; i < 10; i = i + 1)
    //   {
    //     c = c + 1;
    //   }
    // }
    // imp.print(a);
    // imp.print(c);
    // int b= this.fact(5, 3, 10);
    // int b = -5;
    // b += 2;
    // imp.print(b);
    // for(int i=0; i<100; i++){
    //   imp.print(i);
    // }
    // int arr[]=new int[30];
    // b=arr[2];
    // int b=5;
    // imp.print(b);
    // imp.print(b);
    // int p = imp.scan_int();
    // imp.print(p);
    // if((a == 5)||!(a == 5) )
    // {
    //   a = 4;
    // }
    // else
    // {
    //   a = 3;
    // }
    // a = a+ 2;
    int a_ = 5, b=23, c = 3, d = 4, e = 5;
    int a__ = 5-1+6-2+7-3+8+9+10+5-1+6-2+7-3+8+9+10+5-1+6-2+7-3+8+9+10;;
    int b__=23;
    int c__ = 3;
    int d__ = 4; 
    int e__ = 5;
    for(int i = 0; i < 4; ++i)
    {
      int p = imp.scan_int();
      p=this.fact(p);
      imp.print(p);
    }
    // imp.print(b);
    imp.print(_b);
    // imp.print(a);
    int i=0;
    // a=imp.scan_int();
    
    Math math=new Math();
    int v=math.abs(a);
    imp.print(v);
    v=(math.cube(a));
    imp.print(v);
    v=(math.is_prime(a));
    imp.print(v);
    v=(math.max(a, 10000));
    imp.print(v);
    v=(math.min(a, 10000));
    imp.print(v);
    v=(math.signum(a));
    imp.print(v);
    v=(math.square(a));
    imp.print(v);
    return 0;
  }
}