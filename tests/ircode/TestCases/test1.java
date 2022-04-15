/**
 * static: constructor
 * 
 */

package TestCases;

class ListNode {
  int val;
  ListNode next;
  void ListNode(int b){
    this.next=new ListNode();
    this.val=b; 
  }

  void print_val(int c){
    int val1;
    int val2=this.val;
  }
}

class Main{
  public static int main(){
    ListNode root2=new ListNode(); 
    root2.print_val(3);
    return 1;
  }
}
