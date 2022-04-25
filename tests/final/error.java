// Error, function not declared
//should output: not declared in current scope

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
   imp.print1(a);             //ERROR!!!!!
   imp.print(b);

    return 0;
  }
}