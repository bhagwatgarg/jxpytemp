// class _Node{
//   int n, p ,q;
//   // _Node next;
// }


class _Graph{
  // private _Node no;
  int vis;
   int _edge;
  public int calc(){
    // _edge=2;
    this._edge>>=5 + 2*3 - 3;
    this.calc();
    return 1;
  }
}

class _GraphWrapper{
    public _Graph gg;
    void assign_gg(){
      // this.gg=new _Graph();
      this.gg._edge=1;
      _Graph lol = this.gg;
      lol.calc();

      // int a=this.gg.calc();
    }
}

class Main{
  public static int hello (){
		_Graph g = new _Graph();
    // g.no=1;
    g.vis=1;
    // g.calc();
    _GraphWrapper gw=new _GraphWrapper();
    // gw.gg=g;
    gw.gg.calc();
    return 0;
	}
}