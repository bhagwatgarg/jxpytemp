//Math Functions
//insert class math

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
  declare void print(int a);
  declare int scan_int();
  void Imports(){return ;}
}

class Main{
  void Main(){return;}

  int main(){
    Imports imp=new Imports();
    Math math=new Math();
  	int a, b, c, d;
    a=100;
    a=imp.scan_int();   //takes input from user 

    int v=math.abs(a);		//absolute value
    imp.print(v);
    v=(math.cube(a));		//cube
    imp.print(v);
    v=(math.is_prime(a));	//is_prime
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