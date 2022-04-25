//Nested loops
class Imports{
  declare void print(int a);
  void Imports(){return ;}
}

class Main{
  void Main(){return;}

  int main(){
    Imports imp=new Imports();
    int a=10000;
    int b = 0;

    int i = 0;
    int j=10;  

    while(i<10){                    //while loop
        a=a/2;
 		for(; j >0 ; j = j - 1){         //for loop
     		 b=b+1;
      
    	}
        i=i+1;
    }
   imp.print(a);             //print statement for ints
   imp.print(b);

    return 0;
  }
}