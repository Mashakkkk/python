// A* on a 0.75 m grid. Diagonal corner cutting is forbidden.
export class Navigation {
  constructor(obstacles = []) { this.step = .75; this.minX = -23.25; this.minZ = -17.25; this.cols = 63; this.rows = 47; this.obstacles = obstacles; }
  point(x, z) { return { x: this.minX + x * this.step, z: this.minZ + z * this.step }; }
  cell(p) { return { x: Math.round((p.x - this.minX) / this.step), z: Math.round((p.z - this.minZ) / this.step) }; }
  walkable(x, z) {
    if (x < 0 || z < 0 || x >= this.cols || z >= this.rows) return false;
    const p = this.point(x, z);
    return !this.obstacles.some(o => p.x > o.x - o.w/2 - .3 && p.x < o.x + o.w/2 + .3 && p.z > o.z - o.d/2 - .3 && p.z < o.z + o.d/2 + .3);
  }
  nearest(p) {
    const c = this.cell(p);
    if (this.walkable(c.x, c.z)) return c;
    for (let r = 1; r < 65; r++) {
      let best, distance = Infinity;
      for (let dx=-r; dx<=r; dx++) for(let dz=-r; dz<=r; dz++) {
        if (Math.abs(dx)!==r && Math.abs(dz)!==r) continue;
        const x=c.x+dx,z=c.z+dz;
        if (this.walkable(x,z)) { const d=dx*dx+dz*dz; if(d<distance){best={x,z};distance=d;} }
      }
      if (best) return best;
    }
    return null;
  }
  find(start, end) {
    const a=this.nearest(start),b=this.nearest(end); if(!a||!b)return [];
    const key=p=>p.z*this.cols+p.x, h=p=>Math.hypot(p.x-b.x,p.z-b.z);
    const open=[{...a,g:0,f:h(a)}], parents=new Map(), scores=new Map([[key(a),0]]),closed=new Set();
    while(open.length){
      open.sort((a,b)=>b.f-a.f);const n=open.pop(),k=key(n);if(closed.has(k))continue;closed.add(k);
      if(n.x===b.x&&n.z===b.z){const path=[this.point(n.x,n.z)];let t=k;while(parents.has(t)){t=parents.get(t);path.push(this.point(t%this.cols,Math.floor(t/this.cols)));}return path.reverse().slice(1);}
      for(const [dx,dz] of [[1,0],[-1,0],[0,1],[0,-1],[1,1],[1,-1],[-1,1],[-1,-1]]){
        const x=n.x+dx,z=n.z+dz;if(!this.walkable(x,z)||(dx&&dz&&(!this.walkable(n.x+dx,n.z)||!this.walkable(n.x,n.z+dz))))continue;
        const p={x,z},q=key(p),g=n.g+Math.hypot(dx,dz);if(g>=(scores.get(q)??Infinity))continue;
        parents.set(q,k);scores.set(q,g);open.push({...p,g,f:g+h(p)});
      }
    }return [];
  }
  canStand(p) { const c=this.cell(p); return this.walkable(c.x,c.z); }
}
