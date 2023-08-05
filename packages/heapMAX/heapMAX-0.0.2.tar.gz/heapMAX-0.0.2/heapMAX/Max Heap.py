# Mriganka's Max Binary Heap and some of it's operation implementation

class MaxHeap:
    def __init__(self):
        self.__heap = [] # here we will use a list data type(array) to implement our heap
        next_insertion = 0
    def __str__(self):
        return "Max Binary Heap By Creator Mriganka"
    def push(self, values):
        len_of_heap = len(self.__heap)
        if len_of_heap == 0:
            c = values.pop(0)
            self.__heap.append(c)
            len_of_heap += 1
        insertion_position = len_of_heap
        if ((insertion_position + 1) % 2) == 0:
           parent_index = ((len_of_heap - 1) // 2)
        elif ((insertion_position + 1) % 2) == 1:
            parent_index = ((len_of_heap - 2) // 2) 
        holder = insertion_position
        c = 0
        for elem in values:
            if elem <= self.__heap[parent_index]:
                self.__heap.append(elem)
                
                
            elif elem > self.__heap[parent_index]:
                
                heap_invariant_not_maintained = True
                self.__heap.append(elem)
                while heap_invariant_not_maintained == True:
                    parent_node_value = self.__heap[parent_index]
                    self.__heap[parent_index], self.__heap[insertion_position] = elem, parent_node_value
                    insertion_position = parent_index
                    if parent_index == 0:
                        break
                        
                    if (insertion_position + 1) % 2 == 0:
                        
                        parent_index = ((insertion_position - 1) // 2)
                        
                        if parent_index < 0:
                            break
                    elif (insertion_position + 1) % 2 == 1:

                        parent_index = ((insertion_position - 2) // 2)
                        if parent_index < 0:
                            break
                    if self.__heap[parent_index] >= self.__heap[insertion_position]:
                        
                        heap_invariant_not_maintained = False
                
            holder = holder + 1
            insertion_position = holder
            if (insertion_position + 1) % 2 == 0:
                parent_index = ((insertion_position - 1) // 2)
            elif (insertion_position + 1) % 2 == 1:
                parent_index = ((insertion_position - 2) // 2)
            
    def get_length(self):
        return len(self.__heap)

    
    def get_heap(self):
        return self.__heap
    
    def __bubble_down(self, parent_index, left_child_index, right_child_index, length_of_heap, root_node = None):
        heap_invariant_not_satisfied = True
        
        while heap_invariant_not_satisfied:
            if self.__heap[parent_index] < self.__heap[left_child_index] and self.__heap[left_child_index] >= self.__heap[right_child_index]:
                #swaping and bubbling down the new root node untill the heap invariant is satisfied
                self.__heap[left_child_index], self.__heap[parent_index] = self.__heap[parent_index],self.__heap[left_child_index]
                parent_index = left_child_index
            elif self.__heap[parent_index] < self.__heap[right_child_index] and self.__heap[left_child_index] < self.__heap[right_child_index]:
                self.__heap[right_child_index] ,self.__heap[parent_index] = self.__heap[parent_index], self.__heap[right_child_index]
                parent_index = right_child_index
            #updating left_child_index and right_child_index with 2i + 1 and 2i + 2 formulae
            ''' note if a binary heap is implemented with an array, if the parent index is at i
              it's left child will always be at 2i + 1 index and right child will alway be at 2i + 2 index'''
            left_child_index = (2 * parent_index) + 1
            right_child_index = (2 * parent_index) + 2
            if left_child_index >= length_of_heap and right_child_index >= length_of_heap:
                return root_node
            if right_child_index >= length_of_heap:
                if self.__heap[parent_index] >= self.__heap[left_child_index]:
                    return root_node
                else:
                    self.__heap[left_child_index], self.__heap[parent_index] = self.__heap[parent_index],self.__heap[left_child_index]
                    return root_node

            if self.__heap[parent_index] >= self.__heap[left_child_index] and self.__heap[parent_index] >= self.__heap[right_child_index]:
                return root_node
            
    
    def __bubble_up(self, present_node, parent_index_up):
            self.__heap[parent_index_up], self.__heap[present_node] = self.__heap[present_node], self.__heap[parent_index_up]
            present_node = parent_index_up
            if (present_node + 1) % 2 == 0:
                parent_index_up = ((present_node - 1) // 2)
            if (present_node + 1) % 2 == 0:
                parent_index_up = ((present_node - 2) // 2)
            if parent_index_up < 0:
                return
            if self.__heap[present_node] <= self.__heap[parent_index_up]:
                return       
    def poll(self):
        
        length_of_heap = len(self.__heap)
        extreme_node = self.__heap[-1]
        root_node = self.__heap[0]
        #swap the root_node with the extreme
        self.__heap[-1], self.__heap[0] = root_node, extreme_node
        if length_of_heap < 3:
            root = self.__heap.pop()
            return root
        if length_of_heap == 3:
            if self.__heap[0] >= self.__heap[1]:
                root = self.__heap.pop()
                return root
            else:
                self.__heap[0], self.__heap[1] = self.__heap[1], self.__heap[0]
                root = self.__heap.pop()
                return root
            
        root_node = self.__heap.pop()
        parent_index = 0
        left_child_index = 1
        right_child_index = 2
        if self.__heap[parent_index] >= self.__heap[left_child_index] and self.__heap[parent_index] >= self.__heap[right_child_index]:
            return root_node
        length_of_heap = len(self.__heap)
        heap_invariant_not_satisfied = True
        if heap_invariant_not_satisfied:
            val = self.__bubble_down(parent_index, left_child_index, right_child_index, length_of_heap, root_node)
            return val

    def remove(self, value):
        if value == self.__heap[0]:
            self.__heap.poll()
            return
        if value not in self.__heap:
             print("Warning: there is no such value as  " + str(value) + "  in the heap")
             return
        removed_index = self.__heap.index(value)
        length_of_heap = len(self.__heap)
        if removed_index == length_of_heap - 1:
            self.__heap.pop()
            return
        if removed_index == self.__heap[0]:
            self.poll()
            return
        #swaping the value which has to be removed with the last index
        self.__heap[removed_index], self.__heap[-1] = self.__heap[-1], self.__heap[removed_index]
        self.__heap.pop() # removing the node with the asked value from the last position
        length_of_heap -= 1
        if length_of_heap <= 3:
            return
        
        left_child_index = ((2 * removed_index) + 1)
        right_child_index = ((2 * removed_index) + 2)
        if (removed_index + 1) % 2 == 0:
            parent_index_up = ((removed_index - 1) // 2)
        if (removed_index + 1) % 2 == 1:
            parent_index_up = ((removed_index - 2) // 2)
        if (left_child_index >= length_of_heap and right_child_index >= length_of_heap):
            if self.__heap[removed_index] <= self.__heap[parent_index_up]: # Condition satisfied
                return
            elif self.__heap[removed_index] > self.__heap[parent_index_up]:
                 self.__bubble_up(removed_index, parent_index_up)
                 return

        if (right_child_index >= length_of_heap): # Special Condition if it has no right child 
            if self.__heap[parent_index_up] >= self.__heap[removed_index] and self.__heap[removed_index] >= self.__heap[left_child_index]:
                return
            elif self.__heap[parent_index_up] < self.__heap[removed_index]:
                self.bubble_up(removed_index, parent_index_up)
            elif self.__heap[removed_index] < self.__heap[left_child_index] and self.__heap[parent_index_up] >= self.__heap[removed_index]:
                self.__heap[removed_index], self.__heap[left_child_index] = self.__heap[left_child_index], self.__heap[removed_index]
                return
        
            
        if self.__heap[removed_index] >= self.__heap[left_child_index] and self.__heap[removed_index] >= self.__heap[right_child_index]:
            if self.__heap[removed_index] <= self.__heap[parent_index_up]:
                return
            else:
                self.__bubble_up(removed_index, parent_index_up)
                return
                '''If the new swaped node at the past position of the removed item
                                    and it is greater or equal to both of it's child but also greater then it's upward
                                     parent node then bubble_up is invoked'''

            
      #If none of the above condition is satisfied it will bubble_down
        parent_index = removed_index
        self.__bubble_down(parent_index, left_child_index, right_child_index, length_of_heap)
        
    def nlargest(self, n):
        sorted_heap_rev = sorted(self.__heap, reverse = True)
        if n > len(self.__heap):
            return "You are entering an argument which is greater then the length of the heap"
        return sorted_heap[:n]
            
    def nsmallest(self, n):
        sorted_heap_rev = sorted(self.__heap)
        if n > len(self.__heap):
            return "You are entering an argument which is greater then the length of the heap"
        return sorted_heap_rev[:n]
            
    def heap_pushpoll(self, value):
        self.push([value])
        val = self.poll()
        return val
    
    def heap_replace(value):
        val = self.poll()
        self.push([value])
        return val
   
    
            
            
        
        
            
        
        
        
        
        
        
            
            
            
            
        
        
        



        
        
        



                        
                    
                 
              
          
          
          
          
          
            
            
        
        
            
        
        
        
        
        
        
            
            
            
                
                
                
                
            
            
            
            
            
            
            
            
            
        
            
        
        


