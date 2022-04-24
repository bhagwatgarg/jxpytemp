// TODO: function parameters should be accessed with rbp+


// ++ +=
// TODO: add in pec: need {} in for, while, if

class Imports{
  // void print_int(int a){return;}
  declare void print_int(int a);
  void Imports(){return ;}
}

class Main{
  int func(int b){
    b=b*b;
    int c=b+1;
    return c;
  }
  void Main(){return;}
  int main(){
    Imports imp=new Imports();
    int a;
    a=1;
    if(a<10){
      if(a>5){
        if(a==7){
          a=-7;
        }
        else{a=-8;}
      }
      else if(a>3){
        a=-3;
      }
      else if(a==2){a=-2;}
      else{a=-4;}
    }
    else {a=-100;}
    imp.print_int(a);
    return 0;
  }
}