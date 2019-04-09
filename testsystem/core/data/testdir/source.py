import sys
while 1:
    pass

f = open("/tmp/out.txt", "w")
for x in sys.argv[1:]:
	print(2*int(x), end=' ', file=f)
f.close()