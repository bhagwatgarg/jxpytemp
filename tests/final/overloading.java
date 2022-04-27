//factorial

class Imports{
  declare void print(int a);
  void Imports(){return ;}
}

class Main{
  int area(int a){
    int b=a*a;
    return b;
  }
  int area(int a, int b){
    int c=a*b;
    return c;
  }
  void Main(){return;}
  int main(){
    int ar1=this.area(10);
    int ar2=this.area(10, 20);
    Imports imp=new Imports();
    imp.print(ar1);
    imp.print(ar2);
    return 0;
  }
}