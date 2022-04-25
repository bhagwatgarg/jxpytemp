// While loop
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
    int i = 0, j=0;

    for(; j < 10 ; ++j){         //for loop
      b=b+1;
      a=a/2;
      
    }
    int c=(a+b);

   	imp.print(c);             //print statement for ints


    return 0;
  }
}