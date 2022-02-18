package TestCases;
public class Operators{
  public static void literals_and_operators() {
    int i_a = 10, i_b = 0, i_c = -113256, i_d;

    long l_a = 9578192, l_b = 4753075l, l_c = 3245L, l_d = -2131L, l_e;

    float f_a = 111f, f_b = -1, f_c = 112e1f, f_d = 3e2F, f_e = 1.222f, f_f;

    double d_a = 12.65E12d, d_b = 0.3E-12D, d_c = .337, d_d;

    boolean b_a = true, b_b = false, b_c;

    char c_a = 'a', c_b = '\n', c_c = '\u00fa', c_d;

    String s_a = "", s_b = "a", s_c = "qwer", s_d = "\n", s_e;

    long o_a = (i_a++) + (++i_b) + (i_c) - (l_a--) + (--l_b) * (~l_c) % l_d + (2 << 2) + (3 >> 1) - (-1 >>> 2);


    if(i_a<i_b)
      i_b<<=1;
    else if(i_b>i_c){
      i_c>>=2;
      if(i_b>=i_c){
        i_c<<=1;
      }
      else if(i_b<=1)i_b++;
      else i_a++;
    }
    else if(i_c==i_b || i_c==i_a){
      if(i_b!=i_c)i_c++;
    }
    else{
      l_a=l_b&l_c;
      l_b=l_c|l_d;
      l_b=l_c^l_d;
    }
    
    switch(i_a){
      case 1:
        i_a=2;
        break;
      case 2:
        i_a=3;
        break;
      default:
        i_a=10;
    }

    i_d=i_c==i_b?10:20;

    l_a=l_b;
    l_a+=12;
    l_a-=l_c;
    f_a*=f_b;
    f_c/=f_d;
    l_a%=l_b;
    i_a&=i_a;
    i_a|=i_b;
    i_c^=i_a;
    System.out.println("[SUCCESS] Literals and Operators");
  }

  public static void loops(){
    int i1, i2, i3, i4, i5, i6, n=10;
    for(i1=0; i1<n; ++i1){
      if(i1==4)break;
      if(i1==0)continue;
      i2=2;
      while(i2>0){
        i3=1;
        while(i3>0)i3--;
        i4=2;
        do{
          i4--;
          for(i5=0; i5<2; i5++)i5++;
          for(i5=0; i5<2; i5++){
            i6=2;
            do
              i6--;
            while(i6>0);
          }
        }while(i4>0);
        i2--;
      }
    }
    System.out.println("[SUCCESS] Loops");
  }

}