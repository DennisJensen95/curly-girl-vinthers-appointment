import sys

coverage: int = int(sys.argv[1])

if (coverage >= 80):
    print("brightgreen")
elif (coverage < 80 and coverage >= 60):
    print("green")
elif (coverage < 60 and coverage >= 40):
    print("yellow")
elif (coverage < 40 and coverage >= 20):
    print("orange")
else:
    print("red")
