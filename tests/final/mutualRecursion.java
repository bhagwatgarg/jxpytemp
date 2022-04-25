class mutual_recursion {

  void mutual_recursion(){return;}

  declare int f1(int a);
  declare int f2(int a);

  int f2(int a){
    if(a==0){return 0;}
    int b=a-1;
    int c=this.f1(b);
    c+=1;
    return c;
  }
  int f1(int a){
    if(a==0){return 0;}
    int b=a-1;
    int c=this.f2(b);
    c+=1;
    return c;
  }
}

class Imports{
  // void print(int a){return;}
  declare void print(int a);
  declare int scan_int();
  void Imports(){return ;}
}

class Main{
  void Main(){return;}
  int main(){
    mutual_recursion mr=new mutual_recursion();
    int res=mr.f2(10);
    Imports imp=new Imports();
    imp.print(res);
    return 0;
  }
}
