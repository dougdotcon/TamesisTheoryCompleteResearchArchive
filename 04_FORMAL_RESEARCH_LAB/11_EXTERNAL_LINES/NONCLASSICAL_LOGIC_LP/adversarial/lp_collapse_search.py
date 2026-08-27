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

def is_cvalid(f, atoms, bvals):
    return all(beval(b, f) for b in bvals)

def is_lpvalid(f, atoms, lvvals):
    return all(leval(v, f) in D for v in lvvals)

atoms = ['p','q']
bvals = list(all_valuations(atoms, [False, True]))
lvvals = list(all_valuations(atoms, [F,B,T]))

# Build formulas by size class (number of connective nodes)
by_size = {0: [('atom', a) for a in atoms]}
MAX_SIZE = 4
for s in range(1, MAX_SIZE+1):
    layer = []
    all_smaller = [f for k in range(0,s) for f in by_size[k]]
    # neg: size s formulas from size s-1
    for f in by_size[s-1]:
        layer.append(('neg', f))
    # binary connectives: split s-1 = i + j across the two children (i from 0..s-1)
    for i in range(0, s):
        j = s-1-i
        if j < 0: continue
        for f in by_size.get(i, []):
            for g in by_size.get(j, []):
                layer.append(('and', f, g))
                layer.append(('or', f, g))
                layer.append(('imp', f, g))
    by_size[s] = layer
    print(f"size {s}: {len(layer)} formulas", file=sys.stderr)

all_forms = [f for k in by_size for f in by_size[k]]
print("TOTAL formulas up to size", MAX_SIZE, ":", len(all_forms))

counterexamples = []
for f in all_forms:
    if is_cvalid(f, atoms, bvals) and not is_lpvalid(f, atoms, lvvals):
        counterexamples.append(f)

print("Counterexamples to (CValid -> Valid):", len(counterexamples))
for c in counterexamples[:20]:
    print(c)

# Also sanity check the reverse direction holds (Valid -> CValid), matching the proven theorem
rev_counterexamples = []
for f in all_forms:
    if is_lpvalid(f, atoms, lvvals) and not is_cvalid(f, atoms, bvals):
        rev_counterexamples.append(f)
print("Counterexamples to (Valid -> CValid) [should be 0, proven theorem]:", len(rev_counterexamples))
