/**
 * static: constructor
 *
 */

 // TODO: constructor
 // TODO: check array access, offsets, pass by reference
 // TODO: correct array access tac code
 // TODO: clear temp variables
 // TODO: imports
 // TODO: check break and continue
 // TODO: remove function width
 // TODO: declare * datatype size
 // TODO: multidim dims exactly equal
 // TODO: width in array access
package TestCases;

class ListNode {
  int val2, val;
  ListNode next;
  void ListNode(int b){
    this.next=new ListNode();
    this.val=b; // this.val in tac
  }

  void print_val(int c){
    int val1;  // should be present in tac
    int val2=this.val;
  }

  void f1(ListNode n1, int c1){
    int d;
    return;
  }

  // int f1(int n1, int c1){
  //   char d;
  //   return d;
  // }

  ListNode f1(int n1, int c1){
    int n2;
    n2=1;
    n1=c1;
    c1=1;
    char d;
    // TODO: ListNode l1=this.next; working but ListNode l1=this;
    ListNode l1=this.next;
    for(int _=0; _<1; _++){
      int c1;
      l1.next.next.print_val(_);
    }
    // ListNode b=new ListNode();
    return new ListNode();
  }
}

class Main{
  public static int main(){
    ListNode root=new ListNode();  // call not present (temp2)
    // ListNode root2=new ListNode();
    root.next.next.next.val=2;  // .next.next not present
    int b;
    root.next.next.val=root.next.next.next.val;  // .next.next not present
    root.next.next.print_val(2); // push root.next.next
    // root.print_val(3);

    // int n1;
    ListNode l2=new ListNode();
    root=l2;
    int a=1;
    a=b;
    // root.f1(root.f1(root, 4), 2);
    // root.f1(a, 2);
    root.next.next.f1(new ListNode(), 2);

    for(int i=0; i<10; i++){
      a=b;
    }

    while(a == 1)
    {
      a = b;
    }

    do{
      a = b;
    }while(a == 1);
    int[] arr=new int[10];
    arr[10]=1;
    arr[a]=2;
    return 1;
  }
}
