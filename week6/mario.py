def main():
    height = get_height()
    for i in range(height):
         for j in range(height):
           if i + j >= height - 1:
                print("#",end="")
           else:
                print(" ",end="")
         print()


def get_height():
    while True:
       try:
           n = int(input("Height: "))
           if((n <= 8) and (n >= 1)):
                 return n
       except ValueError:
              print("Not an integer")

main()