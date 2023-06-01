"""
File: linkedbst.py
Author: Ken Lambert
"""
from math import logLinkedBST
import time
import random
from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack



class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            s_el = ""
            if node is not None:
                s_el += recurse(node.right, level + 1)
                s_el += "| " * level
                s_el += str(node.data) + "\n"
                s_el += recurse(node.left, level + 1)
            return s_el

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right is not None:
                    stack.push(node.right)
                if node.left is not None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node is not None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) is not None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""
        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left is None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right is None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def lift_max_left_sub(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            cur_node_e = top.left
            while not cur_node_e.right is None:
                parent = cur_node_e
                cur_node_e = cur_node_e.right
            top.data = cur_node_e.data
            if parent == top:
                top.left = cur_node_e.left
            else:
                parent.right = cur_node_e.left

        # Begin main part of the method
        if self.isEmpty():
            return None

        # Attempt to locate the node containing the item
        item_removed = None
        pre_root = BSTNode(None)
        pre_root.left = self._root
        parent = pre_root
        direction = 'L'
        curr_node = self._root
        while not curr_node is None:
            if curr_node.data == item:
                item_removed = curr_node.data
                break
            parent = curr_node
            if curr_node.data > item:
                direction = 'L'
                curr_node = curr_node.left
            else:
                direction = 'R'
                curr_node = curr_node.right

        # Return None if the item is absent
        if item_removed is None:
            return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not curr_node.left is None \
                and not curr_node.right is None:
            lift_max_left_sub(curr_node)
        else:

            # Case 2: The node has no left child
            if curr_node.left is None:
                new_child = curr_node.right

                # Case 3: The node has no right child
            else:
                new_child = curr_node.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = new_child
            else:
                parent.right = new_child

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = pre_root.left
        return item_removed

    def replace(self, item, n_item):
        """
        If item is in self, replaces it with n_item and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe is not None:
            if probe.data == item:
                old_data = probe.data
                probe.data = n_item
                return old_data
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''
        def height1(node):
            '''
            Helper function
            :param top:
            :return:
            '''
            if node is None:
                return 0
            else:
                left_height = height1(node.left)
                right_height = height1(node.right)
                return max(left_height, right_height) + 1

        if self._root is not None:
            return height1(self._root) - 1
        else:
            return 0

    def is_balanced(self):
        '''
        Метод повинен повертати True, якщо висота дерева менша ніж 2 * log2(n + 1) - 1,
        де n це кількість вершин або False в іншому випадку.
        Return True if tree is balanced
        :return:
        '''
        num = self._size
        if self.height() < 2 * log(num + 1) - 1:
            return True
        return False

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        items = []

        def recurse(node):
            if node is None:
                return
            if low <= node.data <= high:
                items.append(node.data)
                recurse(node.left)
                recurse(node.right)
            if node.data < low:
                recurse(node.right)
            if node.data > high:
                recurse(node.left)

        recurse(self._root)
        return sorted(items)

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        def create_balanced_tree(nodes):
            if not nodes:
                return None

            mid = len(nodes) // 2
            root = BSTNode(nodes[mid])
            root.left = create_balanced_tree(nodes[:mid])
            root.right = create_balanced_tree(nodes[mid + 1:])
            return root

        nodes = list(self)
        nodes.sort()
        self._root = create_balanced_tree(nodes)

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        current = self._root
        res = None

        while current:
            if current.data > item:
                res = current.data
                current = current.left
            else:
                current = current.right
        return res

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        current = self._root
        res = None
        while current:
            if current.data < item:
                res = current.data
                current = current.right
            else:
                current = current.left
        return res

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        with open(path, "r", encoding = "utf8") as file:
            words = file.read().splitlines()

        start_time = time.time()
        random_words = random.choices(words, k=10000)
        for word in random_words:
            _ = word in words
        end_time = time.time()
        total = end_time - start_time
        print(f"час пошуку {total}")

        ordered_list = LinkedBST(words[:1000])
        start_time = time.time()
        random_words = random.choices(words, k=10000)
        for word in sorted(random_words):
            ordered_list.find(word)
        end_time = time.time()
        total = end_time - start_time
        print(f"час пошуку {total}")

        ordered_list = LinkedBST()
        start_time = time.time()
        random_words = random.choices(words, k=10000)
        for word in random_words[:1000]:
            ordered_list.add(word)
        end_time = time.time()
        total = end_time - start_time
        print(f"час пошуку {total}")

        ordered_list = LinkedBST(words[:1000])
        ordered_list.rebalance()
        start_time = time.time()
        random_words = random.choices(words, k=10000)
        for word in ordered_list:
            _ = ordered_list.find(word)
        end_time = time.time()
        total = end_time - start_time
        return f"час пошуку {total}"

