//integer arithmetic
/**
 * Expected output: 40
 * @return
 */
class Imports{
  declare void print(int a);
  void Imports(){return ;}
}

class Main{
  void Main(){return;}

  int main(){
    Imports imp=new Imports();
    int a=100;
    int b = 0;
    int c=10;
    int d=12;
    int e=2;
    int f;
    f= a+b-c*d/e;
   imp.print(f);            

    return 0;
  }
}