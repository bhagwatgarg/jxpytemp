class mutual_recursion {
  declare void f1();
  declare void f2();

  void f2(){this.f1();}
  void f1(){this.f2();}
}
