import sys
f = open("/tmp/out.txt", "w")
for x in sys.argv[1:]:
	print(3*int(x), end=' ', file=f)
f.close()