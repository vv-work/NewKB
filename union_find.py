class Node:
    def __init__(self, data):
        self.data = data
        self.parent = self
        self.rank = 0


class UnionFind:
    def __init__(self, data):
        self.nodes = {item: Node(item) for item in data}

    def union(self, item1, item2):
        node1 = self.nodes[item1]
        node2 = self.nodes[item2]

        root1 = self.find(node1)
        root2 = self.find(node2)

        if root1 != root2:
            if root1.rank < root2.rank:
                root1, root2 = root2, root1

            root2.parent = root1
            if root1.rank == root2.rank:
                root1.rank += 1

    def find(self, node):
        if node != node.parent:
            node.parent = self.find(node.parent)
        return node.parent

    def connected(self, item1, item2):
        return self.find(self.nodes[item1]) == self.find(self.nodes[item2])

