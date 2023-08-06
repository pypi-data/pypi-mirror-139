"""A module called nester.py made to print out nested lists. It contains one function designed
for that purpose. """


def printList(myList):
    """The function which does the work."""
    for item in myList:
        if(isinstance(item,list)):
            printList(item)
        else:
            print(item)
