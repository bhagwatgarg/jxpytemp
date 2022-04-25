// TODO: function parameters should be accessed with rbp+


// ++ +=
// TODO: add in pec: need {} in for, while, if

class Imports{
  // void print_int(int a){return;}
  declare void print_int(int a);
  void Imports(){return ;}
}

class Main{
  // declare int fact2(int b);
  int fact(int b){
    if(b==0){return 1;}
    else{
        int k=b-1;
        int k1=this.fact(k);
        return b*k1;
    }
    return 0;
  }
  int fact(int b, int r, int p){
    if(b==r){return r*p;}
    else{
        int k=b-1;
        int k1=this.fact(k, r, p);
        return b*k1;
    }
    return 0;
  }
  void Main(){return;}
  int main(){
    Imports imp=new Imports();
    int a =5, b_ = 6, c = 7;
    a=5;
    // int i;
    // for(int i=0; i <10; i=i+1){git checkout 
    // while(a<10){
    //   a=a+1;
    //   for(int i = 0; i < 10; i = i + 1)
    //   {
    //     c = c + 1;
    //   }
    // }
    // imp.print_int(a);
    // imp.print_int(c);
    int b=0;
    
    // int b = -5;
    // b += 2;
    // imp.print_int(b);
    // for(int i=0; i<100; i++){
    //   imp.print_int(i);
    // }
    a=98;
    // int arr[]=new int[30];
    // for (int i=0;i<10;i++){
    //   arr[i]=i;
    //   imp.print_int(arr[i]);
    // }

    int arr[][] = new int[5][3];
    arr[2][1]=0;
    return a;
  }
}

/*
mov [rbp+8], qword [rbp+16]
*/