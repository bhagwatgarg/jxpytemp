//while loop
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
    int c=12;
    int i = 0;


    while(i<10){                    //while loop
        a=a/2;
        b=b+1;
        if(a<10){
            break;                  //break statement
        }
        i=i+1;
    }

   imp.print(a);             //print statement for ints
   imp.print(b);
   imp.print(c);
    return 0;
  }
}