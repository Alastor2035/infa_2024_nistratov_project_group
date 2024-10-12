a = { 'a': 1, 'b': 2, 'c': 3} 
b = { 'c': 3, 'd': 4,'e': 5}
ab = {}
for key in a.keys():
    ab[key] = [a[key], None]
for key in b.keys():
    if key in ab.keys():
        ab[key] = [a[key], b[key]]
    else:
        ab[key] = [None, b[key]]
print(ab)