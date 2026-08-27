import itertools, sys
sys.setrecursionlimit(10000)
F,B,T = 0,1,2
D = {T,B}
def neg(x): return {F:T,B:B,T:F}[x]
def land(x,y): return min(x,y)
def lor(x,y): return max(x,y)
def limp(x,y): return lor(neg(x), y)
def leval(v, f):
    tag = f[0]
    if tag == 'atom': return v[f[1]]
    if tag == 'neg': return neg(leval(v, f[1]))
    if tag == 'and': return land(leval(v, f[1]), leval(v, f[2]))
    if tag == 'or': return lor(leval(v, f[1]), leval(v, f[2]))
    if tag == 'imp': return limp(leval(v, f[1]), leval(v, f[2]))
def beval(b, f):
    tag = f[0]
    if tag == 'atom': return b[f[1]]
    if tag == 'neg': return not beval(b, f[1])
    if tag == 'and': return beval(b, f[1]) and beval(b, f[2])
    if tag == 'or': return beval(b, f[1]) or beval(b, f[2])
    if tag == 'imp': return (not beval(b, f[1])) or beval(b, f[2])
def all_valuations(atoms, vals):
    keys = list(atoms)
    for combo in itertools.product(vals, repeat=len(keys)):
        yield dict(zip(keys, combo))

def run(atoms, max_size, label):
    bvals = list(all_valuations(atoms, [False, True]))
    lvvals = list(all_valuations(atoms, [F,B,T]))
    by_size = {0: [('atom', a) for a in atoms]}
    for s in range(1, max_size+1):
        layer = []
        for f in by_size[s-1]:
            layer.append(('neg', f))
        for i in range(0, s):
            j = s-1-i
            if j < 0: continue
            for f in by_size.get(i, []):
                for g in by_size.get(j, []):
                    layer.append(('and', f, g))
                    layer.append(('or', f, g))
                    layer.append(('imp', f, g))
        by_size[s] = layer
    all_forms = [f for k in by_size for f in by_size[k]]
    cex = [f for f in all_forms if all(beval(b,f) for b in bvals) and not all(leval(v,f) in D for v in lvvals)]
    print(f"[{label}] atoms={atoms} max_size={max_size} total_formulas={len(all_forms)} counterexamples={len(cex)}")
    for c in cex[:10]:
        print("  ", c)

run(['p'], 6, "1-atom deep")
run(['p','q','r'], 2, "3-atom")
