import sys
query = None
while True:
    if not query: 
        query = input("Denis: ")
    if query in ['quit', 'q']:
        sys.exit()
    print("Alfred: " + query)
    query = None