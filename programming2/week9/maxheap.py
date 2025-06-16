''' 
author: wazeen hoq 
kuid: 3137691 
date created: 4/27
lab: lab#1005C
last modified: 4/28
purpose: MaxHeap class
'''

class MaxHeap:
    def __init__(self):
        self.data = []

    def push(self, patient):
        self.data.append(patient)
        self._heapify_up(len(self.data) - 1)

    def pop(self):
        if self.is_empty():
            return None
        self._swap(0, len(self.data) - 1)
        patient = self.data.pop()
        self._heapify_down(0)
        return patient

    def peek(self):
        if self.is_empty():
            return None
        return self.data[0]

    def is_empty(self):
        return len(self.data) == 0

    def size(self):
        return len(self.data)

    def _parent(self, index):
        return (index - 1) // 2

    def _left(self, index):
        return 2 * index + 1

    def _right(self, index):
        return 2 * index + 2

    def _heapify_up(self, index):
        parent = self._parent(index)
        if index > 0 and self.data[parent] < self.data[index]:
            self._swap(index, parent)
            self._heapify_up(parent)

    def _heapify_down(self, index):
        largest = index
        left = self._left(index)
        right = self._right(index)

        if left < len(self.data) and self.data[largest] < self.data[left]:
            largest = left
        if right < len(self.data) and self.data[largest] < self.data[right]:
            largest = right

        if largest != index:
            self._swap(index, largest)
            self._heapify_down(largest)

    def _swap(self, i, j):
        self.data[i], self.data[j] = self.data[j], self.data[i]
