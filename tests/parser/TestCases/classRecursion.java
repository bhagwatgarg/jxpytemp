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
    this.val=b; // this.val in tac
  }

  void print_val(int c){
    int val1;  // should be present in tac
    int val2=this.val;
  }
}

class Main{
  public static int main(){
    ListNode root=new ListNode();  // call not present (temp2)
    ListNode root2=new ListNode(); 
    root.next.next.next.val=2;  // .next.next not present
    root.next.next.print_val(2); // push root.next.next
    root2.print_val(3);
    return 1;
  }
}
