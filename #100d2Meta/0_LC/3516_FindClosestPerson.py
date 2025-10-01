class Solution:
    def findClosest(self, x: int, y: int, z: int) -> int: 
        dist_1 = abs(z-x)
        dist_2 = abs(z-y)
        if dist_1<dist_2:
            return 1
        elif dist_1>dist_2:
            return 2
        else:
            return 0
