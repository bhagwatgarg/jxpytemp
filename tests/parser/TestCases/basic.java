// class Main2{
//     int k;
//     void Main2(){
//         this.k=2;
//         return;
//     }
//     int hello(int a){
//       a=2;
//       return a;
//     }
//   }
//   class Main{
//     int main(){
//         int a;
//         Main2 m=new Main2();
//         a = m.hello(3);
//         return 0;
//     }
//   }


class Main{
    void Main(){}
    int main2(int c, int b){
        b=22;
        return b;
    }
    int main(){
        (new Main()).main();
        // m.main();
        // int a=2;
        // a=a*a+a-a;
        // int b=this.main2(a, a);
        return 1;
    }
}