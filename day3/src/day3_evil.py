"""An evil one-liner"""
print([(f:=open("day3/input")),(d:=lambda x:list(map(chr,(0,*range(97,123),*range(65,91)))).index(x)),sum(d(({*x}&{*y}).pop())for x,y in((z[:len(z)//2],z[len(z)//2:])for z in open("day3/input"))),sum(d(({*x}&{*y}&{*z}-{"\n"}).pop())for x,y,z in([l,next(f),next(f)] for l in f))][-2:])
