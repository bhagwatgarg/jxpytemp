class matmul{

  int main(){
      //creating two matrices
      matmul [][][] a= new matmul[3][4][5];
      matmul [][][] b= new matmul[3][4][5];
      matmul [][][] c=new matmul[3][4][5];
      for(int i=0;i<3;i++){
          for(int j=0;j<4;j++){
            for(int k=0;k<5;k*=2){
                a[i][j][k] = new matmul();
                b[i][j][k] = new matmul();
            }
          }
      }

      //multiplying and printing multiplication of 2 matrices
      for(int i=0;i<3;i++){
          for(int j=0;j<3;j++){
              c[i][j]=0;
              int k = 0;
              while(k<3)
              {
                  c[i][j]= c[i][j] + a[i][k]*b[k][j];
                  k++;
              }//end of k loop
          }//end of j loop
      }
      // for(int i=0;i<3;i++)
          // for(int j=0;j<3;j++)
              // println(c[i][j]);
      return 0;
  }
}
