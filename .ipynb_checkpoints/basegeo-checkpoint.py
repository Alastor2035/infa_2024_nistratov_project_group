class Vector3d:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __abs__(self):
        return (self.x**2 + self.y**2 + self.z**2)**0.5
    
    def dot_product(self, v):
        return self.x * v.x + self.y * v.y + self.z * v.z
    
    def __mul__(self, x, y = 0, z = 0):
        if isinstance(x, Vector3d):
            return self.dot_product(x)
        else:
            return Vector3d(self.x * x, self.y * x, self.z*x)
        
    def __rmul__(self, v):
        return Vector3d(self.x * v, self.y * v, self.z*v)
    
    def __add__(self, x):
        if isinstance(x, Vector3d):
            return Vector3d(self.x + x.x, self.y +x.y, self.z + x.z)
        else:
            return Vector3d(self.x + x, self.y + x, self.z + x)
        
    def __sub__(self, x):
        if isinstance(x, Vector3d):
            return Vector3d(self.x - x.x, self.y - x.y, self.z - x.z)
        else:
            return Vector3d(self.x - x, self.y - x, self.z - x)
        
    def __str__(self):
        return f"{self.x} {self.y} {self.z}"
        
    def cross_product(self, v):
        return Vector3d(self.y*v.z-self.z*v.y, -self.x*v.z+self.z*v.x, self.x*v.y -self.y*v.x)
    

vecs = [Vector3d(1, 2, 3), Vector3d(4, 5, 6), Vector3d(7, 8, 9)]

# 1.1
v = Vector3d(0, 0, 0)
for i in vecs:
    v = v + i
v = v * (1 / len(vecs))
print(v)

# 1.2
maxs = 0
points = [Vector3d(1, 6, 5), Vector3d(4, 2, 765), Vector3d(5, 2, 3), Vector3d(6, 2, 3)]
for i in points:
    for j in points:
        for k in points:
            v1 = i - j
            v2 = i - k
            s = 0.5 * abs(v1.cross_product(v2))
            maxs = max(s, maxs)
print(maxs)