
/**
 * static: constructor
 * 
 */

class Imports{
  declare void print(int a);
  void Imports(){return ;}
}

class ListNode {
  void ListNode(){return;}
  int val;
  ListNode next;
  void ListNode(int b){
    this.val=b; 
    return;
  }

  void print_val(int c){
    int val2=this.val+c;
    Imports imp=new Imports();
    imp.print(val2);
    return;
  }
}

class Main{
  void Main(){return;}
   int main(){
    ListNode root2=new ListNode(69);
    ListNode r3=new ListNode(420);
    root2.next=r3;
    ListNode r2_next=root2.next;
    r2_next.print_val(3);
    return 1;
  }
}
