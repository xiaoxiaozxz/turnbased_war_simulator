# from core.unit import CUnit, UnitAttr
# from core.state import CBattleState
# from simulator_env.simulator import CBattleSimulator
# from ai.agents import CRandomAgent,CGreedyAgent

# oEnv = CBattleSimulator(iMaxTurns=30)
# oEnv.Reset()
# print("\n=== 运行一个随机 AI 对局（渲染）===")
# oRandomAgent = CRandomAgent()
# fReward, iTurns = oEnv.RunEpisode(oRandomAgent, bRender=False, bVerbose=False)
# print(f"总奖励: {fReward}, 总回合数: {iTurns}")
    
    
# print("\n=== 运行一个贪心 AI 对局（渲染）===")
# oGreedyAgent = CGreedyAgent()
# fReward, iTurns = oEnv.RunEpisode(oGreedyAgent, bRender=False, bVerbose=False)
# print(f"总奖励: {fReward}, 总回合数: {iTurns}")
import random
print(random.choice([1,2,3,4,5]))
