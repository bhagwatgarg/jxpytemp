// TODO: function parameters should be accessed with rbp+


// ++ +=
// TODO: add in pec: need {} in for, while, if

class Imports{
  // void print_int(int a){return;}
  declare void print_int(int a);
  void Imports(){return ;}
}

class Main{
  int func(int b){
    b=b*b;
    int c=b+1;
    return c;
  }
  void Main(){return;}
  int main(){
    Imports imp=new Imports();
    int a, b = 0;
    a=1;
    int i = 0;
    for(; i < 10 ; i = i + 1){
      a=a+1;
      if(a > 5)
      {
      continue;
      }
      b = b + 1;
      // i =i + 1;
    }
    imp.print_int(a);
    // imp.print_int(b);
    return 0;
  }
}