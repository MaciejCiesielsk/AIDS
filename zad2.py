import random
import os
import argparse
import math

parser = argparse.ArgumentParser()
parser.add_argument("-avl", action="store_true", help="Work on AVL tree")
parser.add_argument("-bst", action="store_true", help="Work on BST tree")
args = parser.parse_args()

CURRENT_DIR = os.path.dirname(__file__)

positions = {}



#BST
class TreeNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

class BST:
    def __init__(self):
        self.root = None


    def insert(self, node, key):
        if not node:
            return TreeNode(key)
        if key < node.key:
            node.left = self.insert(node.left, key)
        else:
            node.right = self.insert(node.right, key)
        return node

    def find_max(self, node):
        if not node:
            return None
        while node.right:
            node = node.right
        return node.key

    def find_min(self, node):
        if not node:
            return None
        while node.left:
            node = node.left
        return node
        
    def inorder_traversal(self, node):
        if node:
            self.inorder_traversal(node.left)
            print(node.key, end=" ")
            self.inorder_traversal(node.right)

    def postorder_traversal(self, node):
        if node:
            self.postorder_traversal(node.left)
            self.postorder_traversal(node.right)
            print(node.key, end=" ")

    def preorder_traversal(self, node):
        if node:
            print(node.key, end=" ")
            self.preorder_traversal(node.left)
            self.preorder_traversal(node.right)


        return node
    def insert_key(self, key):
        self.root = self.insert(self.root, key)

    def remove_key(self, key):
        self.root = self.delete(self.root, key)


    def remove(self, node, key):
        if not node:
            return node

        if key < node.key:
            node.left = self.remove(node.left, key)
        elif key > node.key:
            node.right = self.remove(node.right, key)
        else:
            if not node.left:
                temp = node.right
                node = None
                return temp
            elif not node.right:
                temp = node.left
                node = None
                return temp
            temp = self.find_min(node.right)
            node.key = temp.key
            node.right = self.remove(node.right, temp.key)

        return node
    
    def rotate_right(self, root):
        if self.height() < 1:
            return root
        new_root = root.left
        root.left = new_root.right
        new_root.right = root
        root = new_root
        return root



    def vine(self, root):
        tail = root
        rest = tail.right
        while rest:
            if not rest.left:
                tail = rest
                rest = rest.right
            else:
                #jak nie jest po lewej stronie to rotacja
                temp = rest.left
                rest.left = temp.right
                temp.right = rest
                rest = temp
                tail.right = temp
        return root
    
    def height_recursive(self, root):
        if not root:
            return 0
        return 1 + self.height_recursive(root.left) + self.height_recursive(root.right)
    

    def height(self):
        return self.height_recursive(self.root)

    def balance(self):
            n = self.height()
            m = 2 ** (int(math.log2(n + 1))) - 1

            self.rotate_right(m)

            while m > 1:
                m = m // 2
                self.rotate_right(m)
    
    def dsw(self):
        self.vine(self.root)
        self.balance()

    


#AVL

class AVL:
    def __init__(self):
        self.root = None
    
    def height(self, node):
        if not node:
            return 0
        return node.height
    

    def balance(self,node):
        if not node:
            return 0
        return self.height(node.left) - self.height(node.right)
    

    def rotate_left(self, x):
        y = x.right
        temp = y.left

        y.left = x
        x.right = temp

        x.height = 1 + max(self.height(x.left), self.height(x.right))
        y.height = 1 + max(self.height(y.left), self.height(y.right))

        return y

    def rotate_right(self, y):
        x = y.left
        temp = x.right

        x.right = y
        y.left = temp

        y.height = 1 + max(self.height(y.left), self.height(y.right))
        x.height = 1 + max(self.height(x.left), self.height(x.right))

        return x
    
    def insert_sorted(self, keys, start, end):
        if start>end:
            return None
        mid = (start+end)//2
        root = TreeNode(keys[mid])
        root.left = self.insert_sorted(keys,start,mid-1)
        root.right = self.insert_sorted(keys,mid+1,end)
        return root
    
    def insert(self, node, key):
        if not node:
            return TreeNode(key)

        if key < node.key:
            node.left = self.insert(node.left, key)
        else:
            node.right = self.insert(node.right, key)

        node.height = 1 + max(self.height(node.left), self.height(node.right))

        balance = self.balance(node)

        # LL rotation
        if balance > 1 and key < node.left.key:
            return self.rotate_right(node)

        # RR rotation
        if balance < -1 and key > node.right.key:
            return self.rotate_left(node)

        # LR rotation
        if balance > 1 and key > node.left.key:
            node.left = self.rotate_left(node.left)
            return self.rotate_right(node)

        # RL rotation
        if balance < -1 and key < node.right.key:
            node.right = self.rotate_right(node.right)
            return self.rotate_left(node)

        return node





    def remove(self, node, key):
        if not node:
            return node

        if key < node.key:
            node.left = self.remove(node.left, key)
        elif key > node.key:
            node.right = self.remove(node.right, key)
        else:
            if not node.left:
                temp = node.right
                node = None
                return temp
            elif not node.right:
                temp = node.left
                node = None
                return temp
            else:
                temp = self.find_min(node.right)
                node.key = temp.key
                node.right = self.remove(node.right, temp.key)
            if not node:
                return node
        
        node.height = 1 + max(self.height(node.left), self.height(node.right))

        balance = self.balance(node)

        # LL rotation
        if balance > 1 and self.balance(node.left) >= 0:
            return self.rotate_right(node)

        # RR rotation
        if balance < -1 and self.balance(node.right) <= 0:
            return self.rotate_left(node)

        # LR rotation
        if balance > 1 and self.balance(node.left) < 0:
            node.left = self.rotate_left(node.left)
            return self.rotate_right(node)

        # RL rotation
        if balance < -1 and self.balance(node.right) > 0:
            node.right = self.rotate_right(node.right)
            return self.rotate_left(node)

        return node

    def remove_key(self, key):
        self.root = self.remove(self.root, key)
    
    def build_AVL(self,keys):
        keys.sort()
        self.root = self.insert_sorted(keys,0,len(keys)-1)


    
    def find_max(self, node):
        if not node:
            return None
        while node.right:
            node = node.right
        return node.key

    def find_min(self, node):
        if not node:
            return None
        while node.left:
            node = node.left
        return node.key
        
        
    def inorder_traversal(self, node):
        if node:
            self.inorder_traversal(node.left)
            print(node.key, end=" ")
            self.inorder_traversal(node.right)
    def postorder_traversal(self, node):
        if node:
            self.postorder_traversal(node.left)
            self.postorder_traversal(node.right)
            print(node.key, end=" ")


    def preorder_traversal(self, node):
        if node:
            print(node.key, end=" ")
            self.preorder_traversal(node.left)
            self.preorder_traversal(node.right)


def tikz_guide(node, level=0, pos=0):
    global positions
    if positions is None:
        positions = {}
    if node is None:
        return "", pos
    while(pos,-level) in positions:
        pos += 1
    positions[(pos,-level)]=node.key
    result="\\node at ({},{}) {{{}}};\n".format(pos,-level,node.key)
    if node.left is not None:
        left_result, left_pos = tikz_guide(node.left,level+1,pos-1)
        result+=left_result
        result+="\\draw ({},{}) -- ({},{});\n".format(pos,-level,pos-1,-level-1)
    if node.right is not None:
        right_result, right_pos = tikz_guide(node.right,level+1,pos+1)
        result+=right_result
        result+="\\draw ({},{}) -- ({},{});\n".format(pos,-level,pos+1,-level-1)
    return result, pos  


def tikz_file(filename, text):
    with open(filename, 'w') as file:
        file.write("\\documentclass{standalone}\n")
        file.write("\\usepackage{tikz}\n")
        file.write("\\begin{document}\n")
        file.write("\\begin{tikzpicture}[\n")
        file.write("level distance=1cm,\n")
        file.write("level 1/.style={sibling distance=3cm},\n")
        file.write("level 2/.style={sibling distance=1.5cm},\n")
        file.write("level 3/.style={sibling distance=1cm}\n")
        file.write("]\n")
    file.close()
    with open(filename, 'a') as file:
        file.write(text)
    file.close()
    with open(filename, 'a') as file:
        file.write("\\end{tikzpicture}\n")
        file.write("\\end{document}\n")
    file.close()


def build_tree(node):
    result, _ = tikz_guide(node)
    return result


def chosenTree(treeName, tree, root):
    treeName = treeName.upper()
    print(f"--- {treeName} Tree ---")
    print("Type Help for commands")
    while True:
        command = input('action> ').lower()
        print(command)
        if command == 'help':
            print("Help".center(50, "-"))
            print("Commands:")
            print("Help - display this message")
            print("Exit - exit the program")
            print("Print - print the trees using Pre-Order, In-Order and Post-Order traversals")
            print("Insert - insert a node into the trees")
            print("Delete - delete all nodes from the trees")
            print("Export - save the tree to a txt file")
            print("Rebalance - rebalance the AVL tree")
            print("Remove - remove a node from the trees")
            print("MinMax - find the minimum and maximum values in the trees")
            print("-".center(50, "-"))
            continue


        if command == 'exit':
            break


        if command == "print":
            print(treeName, " tree:")
            print("\nPre-order:", end=" ")
            tree.preorder_traversal(root)
            print("\nIn-order:", end=" ")
            tree.inorder_traversal(root)
            print("\nPost-order:", end=" ")
            tree.postorder_traversal(root)
            print("")


        elif command == "export":
            print(f"{treeName} tree has been saved to a txt file:")
            tikz_file(os.path.join(CURRENT_DIR, f"tikzpicture{treeName}.txt"), build_tree(root))


        elif command == 'insert':
            num_nodes = int(input('nodes> '))
            keys = list(map(int, input('insert> ').split()))
            for key in keys:
                root = tree.insert(root, key)


        elif command == 'delete':
            root = None
            print(f"All nodes have been deleted from the {treeName} tree.")


        elif command == 'rebalance':
            print(f"{treeName} tree has been rebalanced.")
            root = tree.dsw()
        elif command == 'remove':
            keys = list(map(int, input('remove> ').split()))
            for key in keys:
                root = tree.remove(root, key)


        elif command == 'minmax':
            minTree = tree.find_min(root)
            maxTree = tree.find_max(root)
            print(f"{treeName} tree: Min = {minTree}, Max = {maxTree}")


        else:
            print("Unknown command. Type help for more information.")




def main():
    avl_tree = AVL()
    bst_tree = BST()
    avl_root = None
    bst_root = None

    if args.avl:
        chosenTree("AVL", avl_tree, avl_root)
    if args.bst:
        chosenTree("BST", bst_tree, bst_root)


if __name__ == "__main__":
    main()