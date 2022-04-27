//factorial

class Imports{
  declare void print(int a);
  void Imports(){return ;}
}

class Main{
  void print_2x(int a){
    a*=2;
    Imports imp=new Imports();
    imp.print(a);
    return;
  }
  void Main(){return;}
  int main(){
    this.print_2x(10);
    return 0;
  }
}