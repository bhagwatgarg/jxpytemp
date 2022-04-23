class Imports{
  declare void print_int(int a);
  void Imports(){return ;}
}

class Main{
    void Main(){return;}
   int main(){
      Imports imp=new Imports();
      int a = 5;
      a=a+a+a;
      //float b= 0.2

      imp.print_int(a);
      return a;
  }
}
