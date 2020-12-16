"""
level: mid 

亚历克斯和李用几堆石子在做游戏。偶数堆石子排成一行，每堆都有正整数颗石子 piles[i] 。
游戏以谁手中的石子最多来决出胜负。石子的总数是奇数，所以没有平局。
亚历克斯和李轮流进行，亚历克斯先开始。 每回合，玩家从行的开始或结束处取走整堆石头。 这种情况一直持续到没有更多的石子堆为止，此时手中石子最多的玩家获胜。
假设亚历克斯和李都发挥出最佳水平，当亚历克斯赢得比赛时返回 true ，当李赢得比赛时返回 false 。

 

示例：

输入：[5,3,4,5]
输出：true
解释：
亚历克斯先开始，只能拿前 5 颗或后 5 颗石子 。
假设他取了前 5 颗，这一行就变成了 [3,4,5] 。
如果李拿走前 3 颗，那么剩下的是 [4,5]，亚历克斯拿走后 5 颗赢得 10 分。
如果李拿走后 5 颗，那么剩下的是 [3,4]，亚历克斯拿走后 4 颗赢得 9 分。
这表明，取前 5 颗石子对亚历克斯来说是一个胜利的举动，所以我们返回 true 。
 

提示：

2 <= piles.length <= 500
piles.length 是偶数。
1 <= piles[i] <= 500
sum(piles) 是奇数。
"""

from typing import List


class Solution:
    def stoneGame(self, piles: List[int]) -> bool:
        """dp[i][j] 含义为 piles[i:j] 时 (先手所持有的石子个数，后手所持有的石子个数), dp[0][n-1].[0] - dp[0][n-1].[1] 最后的结果差
        """
        n = len(piles)
        dp = [[(0, 0)]*n for _ in range(n)]
        # base case
        # 当 i==j 是说明至于一堆石子，肯定是先拿的人赢，(piles[i], 0) 这样的形式
        for i in range(n):
            dp[i][i] = (piles[i], 0)
        # 状态转移方程, i 正向遍历，j 逆向遍历
        for i in reversed(range(0, n)):
            for j in range(i+1, n):
                first_side = 'left'
                
                # 选左边，则下一次选择变为后手
                left = piles[i] + dp[i+1][j][1]
                # 选右边，则下一次选择变为后手
                right = piles[j] + dp[i][j-1][1]
                if left > right:
                    first_side = 'left'
                    first = left
                else:
                    first_side = 'right'
                    first = right

                # 不管先手选择了左边还是右边，后手在下一次选择中都会变为先手
                second = dp[i+1][j][0] if first_side == 'left' else dp[i][j-1][0]   
                dp[i][j] = (first, second)
        
        return True if dp[0][n-1][0] > dp[0][n-1][1] else False