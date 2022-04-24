class Imports{
  // void print_int(int a){return;}
  declare void print_int(int a);
  void Imports(){return ;}
}

class Main{
    void Main(){return;}
    // declare void hi(float a);

    int rec(int a)
    {
      // return 10;
      if(a > 5)
      {
        return a;
      }
      int b = a + 1;

      int c=this.rec(b);
      return c;
    }

   int main(){
      Imports imp=new Imports();
      
      int i = 0;
      int a = 0, b = 3, d = 2;
      // int e = 5;
      int c = this.rec(a);
      
      // int p=2,r =3,s=5,t=10; // doesnt work
      // a = 2 * i; // doesnt work
      // a = p*r*s*t;
      // int c = 5;
      // int a = 0;
      // for(; i < 10; i = i + 1)
      // {
      //   a = a + i;
      // }
      // while seems to be working
      // while( i < 10)
      // {
      //   a = a + i;
      //   i = i + 1;
      // }
      //float b= 0.2
      // i = 5;
      // int a = 5;
      // if then else always going inside if block lol
      // if(a > 3)
      // {
      //   a = 69;
      // }
      // else 
      // {
      //   a = 6;
      // }
      // else
      // {
      //   a = 100;
      // }
      imp.print_int(c);
      // imp.print_int(b);
      return i;
  }
}
