This library is made to implement Max Heap data structure.

This Max_Heap module is made on the Object Oriented Principles, It has a class named MaxHeap and inside it has 11 functions.

 .push(list1) function -- This function expect a list as an argument. It heapify that list into a max heap. Even if only one elements is required to add into the max heap, It has to be given as a list of 1 element as argument of the push function.
 For example,
 obj = MaxHeap()
 obj.push([30, 40, 50])
 obj.push([90])

 .poll() function -- This function doesn't required any arguments, This function pop out the largest or the root node of the max heap and mantain the heap invariant. 

This library is made to implement Max Heap data structure.

This Max_Heap module is made on the Object Oriented Principles, It has a class named MaxHeap and inside it has 11 functions. Please note this module only works on Integer, Float  Data Types, I doesn't work on string data type. The Heap data structure is implemented in a list data type.

 .push(list1) function -- This function expect a list as an argument. It heapify that list into a max heap. Even if only one elements is required to add into the max heap, It has to be given as a list of 1 element as argument of the push function.
 For example,
 obj = MaxHeap()
 obj.push([30, 40, 50])
 obj.push([90])
 -------------
 .poll() function -- This function doesn't required any arguments, This function pop out the largest or the root node of the max heap while mantaining the heap invariant inside the heap.
 ---------------
 .remove(arg) -- This function required one argument, give any argument(value) which you want to remove from the heap. It will successfully remove it while maintaining the heap invariant. It's uses two additional private member functions .__bubble_up() and .__bubble_down(), to do numerous swaping operations to maintain the heap invariant while an item is removed from any position.
 -------
 .get_heap() -- This function doesn't required any argument it simply returns the max heap which has been implemented in a list.
 --------
 .get_length() --- This function doesn't required any argument it simply returns the length of the max heap.
 --------
 .nlargest(n) -- This function required one argument which is a number and it returns the list of largest values in the heap upto that number.
 --------
 .nsmallest(n) -- This function required one argument which is a number and it returns the list of smallest values in the heap upto that number.
 ----------
 .heap_pushpoll(value) -- This function required one argument and it does the pushing(inserting) of that value into the max heap and after that polling (popping) out the largest or the root node from the max heao.
 -----------
 .heap_replace(value) -- This function required one argument and it poll(pop) out the largest or the root node and after that pushing or inserting given value in the argument.
 ------------
 .__bubble_up() -- This function is a private function and it is used by the algorithm to bubble up to maintain the heap invariant while a polling or remove operation is being done. This function should not be invoked by mangaling. All the operations are done automatically.
 ----------
 .__bubble_down() --  This function is a private function and it is used by the algorithm to bubble down to maintain the heap invariant while a polling or remove operation is being done. This function should not be invoked by mangaling. All the operations are done automatically.
