class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.previous = None

class List:

    def __init__(self):
        self.head = Node("head")
        self.tail = Node("tail")
        self.head.next = self.tail
        self.tail.previous = self.head
        self.size = 0

    def __str__(self):
        cur = self.head.next
        out = ""
        while cur.value != "tail":
            out += str(cur.value) + "<->"
            cur = cur.next
        return out[:-3]


    def getSize(self):
        return self.size


    def get_element_by_index(self, index):

        if self.size < index:
            return None

        node = self.head
        while index > 0:
            index -= 1
            node = node.next
        return node.next.value

    def push(self, index, value):
        node = self.head
        while index > 0:
            index -= 1
            if node.next.value == "tail":
                self.push(self.size, None)
            node = node.next

        newNode = Node(value)
        newNode.next = node.next
        newNode.previous = node
        node.next = newNode
        newNode.next.previous = newNode
        self.size += 1



    def pop(self, index):
        if self.size-1 < index:
            raise Exception("Popping out of list")
        node = self.head
        while index > 0:
            index -= 1
            node = node.next
        remove = node.next
        node.next = remove.next
        remove.next.previous = node
        self.size -= 1
        return remove.value


# Driver Code
if __name__ == "__main__":
    list1 = List()
    list1.push(1, 1)
    list1.push(2, 2)
    list1.push(10, 3)
    print(list1)
    print(list1.pop(1))
    print(list1.pop(4))
    print(list1.pop(8))
    print(list1)
    print(list1.getSize())