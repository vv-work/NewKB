class Solution:
    def reorderedPowerOf2(self, n: int) -> bool:
        def signature(x:int)->str:
            return "".join(sorted(str(x)))
        target = signature(n)

        for i in range(32):
            if signature(1<<i) == target:
                return True
        return False
