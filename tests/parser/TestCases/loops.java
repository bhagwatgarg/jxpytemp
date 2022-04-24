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
    int c;
    int d=0;

    int i = 0;
    int j=0;
    int t=3;  

    while(i<10){                    //while loop
        a=a/2;
        if(a<10){
            break;                  //break statement
        }
        i=i+1;
    }

    for(; j < 10 ; j = j + 1){         //for loop
      b=b+1;
      if(b > 5)
      {
      continue;                     //continue 
      }
      
    }
    c=(a+b);
    c=c/d;                        //integer division
    c=c%5
   imp.print(c);             //print statement for ints


    return 0;
  }
}