class Imports{
  declare void print_int(int a);
  void Imports(){return ;}
}

class Main{
    void Main(){return;}
   int main(){
      Imports imp=new Imports();
      int a = 1+2;
      a=a+a;
      imp.print_int(55);
      return a;
  }
}
