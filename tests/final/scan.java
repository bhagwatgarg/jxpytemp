class Imports{
  // void print(int a){return;}
  declare void print(int a);
  declare int scan_int();
  void Imports(){return ;}
}

class Main{
  void Main(){return;}
  int main(){
    Imports imp=new Imports();
  	int a=2;
  	a=imp.scan_int();   //takes input from user 
    imp.print(a);

    return 0;
  }
}