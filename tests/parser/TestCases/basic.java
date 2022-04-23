class Main2{
    int k;
    void Main2(){
        this.k=2;
    }
    int hello(int a){
      a=2;
      return a;
    }
  }
  class Main{
    int main(){
        Main2 m=new Main2();
        int a;
        a = m.hello(3);
        return 0;
    }
  }