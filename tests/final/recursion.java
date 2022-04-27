//factorial

class Imports{
  declare void print(int a);
  void Imports(){return ;}
}

class Main{
  void Main(){return;}
  int factorial(int x){
  	if(x<1){
  		return 1;
  	}
  	else{
  		int k=x-1;
  		int b = this.factorial(k);
  		int c = x*b;
  		return c;
  	}
  }

  int main(){
    Imports imp=new Imports();
    int a= this.factorial(5);
    imp.print(a);
    return 0;
  }
}