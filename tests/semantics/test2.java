class Debug {
  int add(int doge, int bhaggu) {
      return doge + bhaggu;
  }
  int main() {
      int doge = 19;
      int [][] bhaggu = new int[doge][20];
      bhaggu[2][3] = 10;
      bhaggu[1][2] = 20;
      int pattu = add(bhaggu[2][3],bhaggu[1][2]);
  }
}