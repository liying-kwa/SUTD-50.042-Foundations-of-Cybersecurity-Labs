#!/usr/bin/env python3

# 50.042 FCS Lab 5 Modular Arithmetics
# Year 2020
# Student: Kwa Li Ying (1003833)

import copy
class Polynomial2:
    def __init__(self,coeffs): 
        self.coeffs = copy.deepcopy(coeffs)

    def add(self,p2):
        new_coeffs = []
        min_order = min(len(self.coeffs), len(p2.coeffs))
        max_order = max(len(self.coeffs), len(p2.coeffs))
        for i in range(min_order):
            new_coeffs.append((self.coeffs[i] + p2.coeffs[i]) % 2)
        for i in range(min_order, max_order):
            if len(self.coeffs) > len(p2.coeffs):
                new_coeffs.append(self.coeffs[i])
            else:
                new_coeffs.append(p2.coeffs[i])
        # Clean off higher order bits if they are 0
        for i in range(len(new_coeffs)-1, -1, -1):
            if new_coeffs[i] == 1:
                break
            new_coeffs.pop()
        return Polynomial2(new_coeffs)

    def sub(self,p2):
        return self.add(p2)

    def mul(self,p2,modp=None):
        # Set fixed power for MSB to check for MSB = 1 later
        if modp != None:
            n = len(modp.coeffs)
        else:
            # GF(2^8) by default
            n = 8
        # Generate partial results
        coeffs1 = copy.deepcopy(self.coeffs)
        coeffs2 = copy.deepcopy(p2.coeffs)
        partials = []
        partials.append(copy.deepcopy(coeffs2))
        partial = copy.deepcopy(coeffs2)
        order = len(coeffs1)
        for i in range(1, order):
            partial.insert(0, 0)
            if len(partial) == n and partial[len(partial)-1] == 1 and modp != None:
                p3 = Polynomial2(partial).add(modp)
                partial = copy.deepcopy(p3.coeffs)
            partials.append(copy.deepcopy(partial))
        # Based on bit 1s in p1, add partial results accordingly
        final = Polynomial2([])
        for i in range(order):
            if coeffs1[i] == 1:
                final = final.add(Polynomial2(partials[i]))
        return final

    def div(self,p2):
        # This is essentially "schoolbook" long division
        q = Polynomial2([])
        r = Polynomial2(copy.deepcopy(self.coeffs))
        d = len(p2.coeffs) - 1
        c = p2.coeffs[len(p2.coeffs)-1]
        while len(r.coeffs)-1 >= d:
            lc_r = r.coeffs[len(r.coeffs)-1]
            s_degree = (len(r.coeffs)-1) - d
            s = Polynomial2([])
            if lc_r/c == 1:
                for i in range(s_degree):
                    s.coeffs.append(0)
                s.coeffs.append(1)
            q = q.add(s)
            r = r.sub(s.mul(p2))
        return q, r

    def __str__(self):
        to_return = ""
        for i in range(len(self.coeffs)-1, -1, -1):
            if self.coeffs[i] == 0:
                continue
            to_return += "x^" + str(i) + "+"
        return to_return[:-1]

    def getInt(self):
        to_return = 0
        for i in range(len(self.coeffs)):
            if self.coeffs[i] == 1:
                to_return += 2 ** i
        return to_return


class GF2N:
    affinemat=[[1,0,0,0,1,1,1,1],
               [1,1,0,0,0,1,1,1],
               [1,1,1,0,0,0,1,1],
               [1,1,1,1,0,0,0,1],
               [1,1,1,1,1,0,0,0],
               [0,1,1,1,1,1,0,0],
               [0,0,1,1,1,1,1,0],
               [0,0,0,1,1,1,1,1]]

    def __init__(self,x,n=8,ip=Polynomial2([1,1,0,1,1,0,0,0,1])):
        self.x = x
        self.n = n
        self.degree = n - 1
        self.ip = ip
        # Create this for convenience, to use Polynomial2 functions easily
        self.coeffs = []
        current = x
        for i in range(n):
            if current == 0:
                break
            elif current == 1:
                self.coeffs.append(1)
                current = 0
            else:
                remainder = current % 2
                self.coeffs.append(remainder)
                current = current // 2
            
    def add(self,g2):
        p3 = Polynomial2(self.coeffs).add(Polynomial2(g2.coeffs))
        x = p3.getInt()
        return GF2N(x, self.n, self.ip)
    
    def sub(self,g2):
        return self.add(g2)
    
    def mul(self,g2):
        p3 = Polynomial2(self.coeffs).mul(Polynomial2(g2.coeffs), self.ip)
        x = p3.getInt()
        return GF2N(x, self.n, self.ip)

    def div(self,g2):
        p3_q, p3_r = Polynomial2(self.coeffs).div(Polynomial2(g2.coeffs))
        gf2n_q = GF2N(p3_q.getInt(), self.n, self.ip)
        gf2n_r = GF2N(p3_r.getInt(), self.n, self.ip)
        return gf2n_q, gf2n_r

    def getPolynomial2(self):
        return Polynomial2(self.coeffs)

    def __str__(self):
        return str(self.getInt())

    def getInt(self):
        return self.x

    def mulInv(self):
        r1 = Polynomial2(self.ip.coeffs)
        r2 = Polynomial2(self.coeffs)
        t1 = Polynomial2([])
        t2 = Polynomial2([1])
        while r2.coeffs != []:
            q, r = r1.div(r2)
            r1 = Polynomial2(copy.deepcopy(r2.coeffs))
            r2 = r
            t = t1.sub( q.mul(t2, self.ip) )
            t1 = Polynomial2(copy.deepcopy(t2.coeffs))
            t2 = t
        if r1.coeffs == [1]:
            return GF2N(t1.getInt(), self.n, self.ip)
        return GF2N(t1.getInt(), self.n, self.ip)

    def affineMap(self):
        # Fill up 0s in p1 for more significant bits for matrix multiplication
        p1_coeffs = copy.deepcopy(self.coeffs)
        for i in range(len(p1_coeffs), 8):
            p1_coeffs.append(0)
        temp_coeffs = []
        for i in range(8):
            sum = 0
            for j in range(8):
                sum += p1_coeffs[j] * self.affinemat[i][j]
            temp_coeffs.append(sum % 2)
        p3 = Polynomial2(temp_coeffs).add(Polynomial2([1,1,0,0,0,1,1,0]))
        return GF2N(p3.getInt(), self.n, self.ip)

print('\nTest 1')
print('======')
print('p1=x^5+x^2+x')
print('p2=x^3+x^2+1')
p1=Polynomial2([0,1,1,0,0,1])
p2=Polynomial2([1,0,1,1])
p3=p1.add(p2)
print('p3= p1+p2 = ', p3)

print('\nTest 2')
print('======')
print('p4=x^7+x^4+x^3+x^2+x')
print('modp=x^8+x^7+x^5+x^4+1')
p4=Polynomial2([0,1,1,1,1,0,0,1])
#modp=Polynomial2([1,1,0,1,1,0,0,0,1])
modp=Polynomial2([1,0,0,0,1,1,0,1,1])
p5=p1.mul(p4,modp)
print('p5=p1*p4 mod (modp)=', p5)

print('\nTest 3')
print('======')
print('p6=x^12+x^7+x^2')
print('p7=x^8+x^4+x^3+x+1')
p6=Polynomial2([0,0,1,0,0,0,0,1,0,0,0,0,1])    
p7=Polynomial2([1,1,0,1,1,0,0,0,1])
p8q,p8r=p6.div(p7)
print('q for p6/p7=', p8q)
print('r for p6/p7=', p8r)

####
print('\nTest 4')
print('======')
g1=GF2N(100)
g2=GF2N(5)
print('g1 = ', g1.getPolynomial2())
print('g2 = ', g2.getPolynomial2())
g3=g1.add(g2)
print('g1+g2 = ', g3)

print('\nTest 5')
print('======')
ip=Polynomial2([1,1,0,0,1])
print('irreducible polynomial', ip)
g4=GF2N(0b1101,4,ip)
g5=GF2N(0b110,4,ip)
print('g4 = ', g4.getPolynomial2())
print('g5 = ', g5.getPolynomial2())
g6=g4.mul(g5)
print('g4 x g5 = ', g6.getPolynomial2())

print('\nTest 6')
print('======')
g7=GF2N(0b1000010000100,13,None)
g8=GF2N(0b100011011,13,None)
print('g7 = ', g7.getPolynomial2())
print('g8 = ', g8.getPolynomial2())
q,r=g7.div(g8)
print('g7/g8 =')
print('q = ', q.getPolynomial2())
print('r = ', r.getPolynomial2())

print('\nTest 7')
print('======')
ip=Polynomial2([1,1,0,0,1])
print('irreducible polynomial', ip)
g9=GF2N(0b101,4,ip)
print('g9 = ', g9.getPolynomial2())
print('inverse of g9 =', g9.mulInv().getPolynomial2())

print('\nTest 8')
print('======')
ip=Polynomial2([1,1,0,1,1,0,0,0,1])
print('irreducible polynomial', ip)
g10=GF2N(0xc2,8,ip)
print('g10 = 0xc2')
g11=g10.mulInv()
print('inverse of g10 = g11 =', hex(g11.getInt()))
g12=g11.affineMap()
print('affine map of g11 =',hex(g12.getInt()))

# Generate table for addition for GF(2^4)
print("\nAddition Table for GF(2^4)")
for i in range(16):
    for j in range(16):
        print(GF2N(i).add(GF2N(j)), end=" ")
    print("\n")
    
# Generate table for multiplication for GF(2^4)
print("Multiplication Table for GF(2^4)")
ip = Polynomial2([1, 0, 0, 1, 1])
for i in range(16):
    for j in range(16):
        print(GF2N(i, 4, ip).mul(GF2N(j, 4, ip)), end=" ")
    print("\n")

# Generate table for AES S-Box
print("Table for AES S-Box")
for x in range(16):
    for y in range(16):
        inp = (x << 4) + y
        out = GF2N(inp).mulInv().affineMap().getInt()
        print("{0:x}".format(out), end=" ")
    print("\n")