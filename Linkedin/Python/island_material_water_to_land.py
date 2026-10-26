"""
An artificial island is one that is constructed by humans rather than formed through natural processes. People can fill the ocean with materials.
Now we have an 1D array to represent the land (1) and ocean (0) locations, along with a limited amount of material to convert ocean cells to land, find the size of the largest island possible.
Examples
Example 1:

islands = [0, 1, 0, 1, 1, 1]
material = 1

result largest island: 5
explanation: [0, 1, 1 (filled), 1, 1, 1]
Example 2:

islands = [0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1]
material = 2

result largest island: 10
explanation: [0, 1, 0, 1, 0, 1, 1 (filled), 1, 1, 1 (filled), 1, 1, 1, 1, 1]


Example 3:
islands = [1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1]
material = 3

result largest island: 8
explanation: [1, 1, 1 (filled), 1, 1 (filled), 1, 1, 1 (filled), 0, 0, 0, 0, 0, 1, 1, 1]
Example 4:
islands = [1, 1, 1, 1, 1]
material = 3

result largest island: 5
explanation: [1, 1, 1, 1, 1]


"""


"""
keep a queue of (0, index of 0) and use two pointer method to move,
 i will be at the start and end pointer will move adding to the count, 
 when we see "0" we add to the queue and 
 add it's count and have zeroCount incremented. 
 when we no longer any material to convert to land zeroCount==material ,
  we will move the start pointer to the first zero element. 
  Popleft from the queue to get the first zero in the path and 
  have start=zeroIndex+1 until start< end and zeroIndex+1 !=0 , 
  keep moving right to find non-zero index right of the first zero.
   update zeroCount and path length accordingly


"""

def island_material_water_to_land(islands:List[int], material: int)-> int:
    max_path_len=0
    start,end=0,0
    zero_count=0
    curr_len=0

    while start <= end and end < len(islands):
        # we have zero left to convert
        if islands[end] == 0:
            zero_count += 1
            while zero_count > material and start <= end:
                if islands[start] == 0:
                    zero_count -= 1
                start += 1
        curr_len = end - start + 1
        max_path_len = max(max_path_len, curr_len)
        end+=1
    return max_path_len

ans=island_material_water_to_land([0, 1, 0, 1, 1, 1], 1)
print(f"Testcase 1: {ans}")
assert ans == 5

ans=island_material_water_to_land([0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1], 2)
assert ans == 10
print(f"Testcase 2: {ans}")


ans=island_material_water_to_land([1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1], 3)
print(f"Testcase 3: {ans}")
assert ans==8


ans=island_material_water_to_land([1, 1, 1, 1, 1],3)
print(f"Testcase 4: {ans}")
assert ans==5

