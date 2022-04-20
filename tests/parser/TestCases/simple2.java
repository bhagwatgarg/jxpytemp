class linked_list_search{
  int a;
  declare int append(int a, int b);
  declare int printInt(int n);
  declare int next(int l);
  declare int val(int l);
   void main() {
      int l[] = new int[5];
      int i,j,y;
      for (i=0;i<5;i++){
        y = this.append(0,1);
        l[i]=y;
        for(j=0;j<6;j++){
          y = this.append(y,i*j);
        }
      }

      y = l[3];
      for(i=0;i<5;i++){
        int h = this.val(y);
        this.printInt(h);
        y=this.next(y);
      }
  }
  int append(int a, int b){
    return 1;
  }
}