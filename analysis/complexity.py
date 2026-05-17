import sys
import os
import random
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from core import CBattleState, CUnit, CSkill, PLAYER_CAMP, MONSTER_CAMP, UnitAttr
from ai.actions import GetLegalActions
from ai.agents import CRandomAgent
from simulator_env.simulator import CBattleSimulator


# region 实验案例
oHero = CUnit({
    UnitAttr.NAME: "Hero", UnitAttr.CUR_HP: 30, UnitAttr.MAX_HP: 30,
    UnitAttr.ATK: 8, UnitAttr.CAMP: PLAYER_CAMP,
    UnitAttr.DEF: 2,
    UnitAttr.SKILLS: {0: CSkill(0, "普攻", 1.0), 1: CSkill(1, "重击", 1.5)}
})
oGuard = CUnit({
    UnitAttr.NAME: "Guard",
    UnitAttr.CUR_HP: 15, UnitAttr.MAX_HP: 15,
    UnitAttr.ATK: 4, UnitAttr.CAMP: PLAYER_CAMP,
    UnitAttr.DEF: 2,
    UnitAttr.SKILLS: {0: CSkill(0, "普通攻击", 1.0)}
})
oMonster = CUnit({
    UnitAttr.NAME: "Monster",
    UnitAttr.CUR_HP: 40, UnitAttr.MAX_HP: 40,
    UnitAttr.ATK: 10, UnitAttr.CAMP: MONSTER_CAMP,
    UnitAttr.DEF: 2,
    UnitAttr.SKILLS: {0: CSkill(0, "普通攻击", 1.0), 1: CSkill(1, "重击", 1.5)}
})
config_2v1 = [oHero, oGuard, oMonster]



# 玩家方：剑士、弓箭手、牧师（血量适中，攻击有区分度）
p1 = CUnit({
    UnitAttr.NAME: "Swordsman", UnitAttr.CUR_HP: 25, UnitAttr.MAX_HP: 25,
    UnitAttr.ATK: 7, UnitAttr.CAMP: PLAYER_CAMP,
    UnitAttr.DEF: 3,
    UnitAttr.SKILLS: {0: CSkill(0, "斩击", 1.0), 1: CSkill(1, "旋风斩", 1.3)}
})
p2 = CUnit({
    UnitAttr.NAME: "Archer", UnitAttr.CUR_HP: 18, UnitAttr.MAX_HP: 18,
    UnitAttr.ATK: 9, UnitAttr.CAMP: PLAYER_CAMP,
    UnitAttr.DEF: 1,
    UnitAttr.SKILLS: {0: CSkill(0, "射击", 1.0), 1: CSkill(1, "强力射击", 1.6)}
})
p3 = CUnit({
    UnitAttr.NAME: "Priest", UnitAttr.CUR_HP: 20, UnitAttr.MAX_HP: 20,
    UnitAttr.ATK: 4, UnitAttr.CAMP: PLAYER_CAMP,
    UnitAttr.DEF: 2,
    UnitAttr.SKILLS: {0: CSkill(0, "杖击", 1.0)}   # 牧师只有一个技能，增加变化
})

# 怪物方：食人魔 + 哥布林首领
m1 = CUnit({
    UnitAttr.NAME: "Ogre", UnitAttr.CUR_HP: 45, UnitAttr.MAX_HP: 45,
    UnitAttr.ATK: 11, UnitAttr.CAMP: MONSTER_CAMP,
    UnitAttr.DEF: 4,
    UnitAttr.SKILLS: {0: CSkill(0, "锤击", 1.0), 1: CSkill(1, "地震", 1.4)}
})
m2 = CUnit({
    UnitAttr.NAME: "GoblinChief", UnitAttr.CUR_HP: 30, UnitAttr.MAX_HP: 30,
    UnitAttr.ATK: 8, UnitAttr.CAMP: MONSTER_CAMP,
    UnitAttr.DEF: 1,
    UnitAttr.SKILLS: {0: CSkill(0, "爪击", 1.0), 1: CSkill(1, "毒刃", 1.2)}
})

config_3v2 = [p1, p2, p3, m1, m2]

# 玩家阵营：骑士、法师、盗贼
knight = CUnit({
    UnitAttr.NAME: "Knight", UnitAttr.CUR_HP: 28, UnitAttr.MAX_HP: 28,
    UnitAttr.ATK: 6, UnitAttr.CAMP: PLAYER_CAMP,
    UnitAttr.DEF: 5,
    UnitAttr.SKILLS: {0: CSkill(0, "突刺", 1.0), 1: CSkill(1, "盾击", 0.8)}
})
mage = CUnit({
    UnitAttr.NAME: "Mage", UnitAttr.CUR_HP: 16, UnitAttr.MAX_HP: 16,
    UnitAttr.ATK: 12, UnitAttr.CAMP: PLAYER_CAMP,
    UnitAttr.DEF: 0,
    UnitAttr.SKILLS: {0: CSkill(0, "火球", 1.0), 1: CSkill(1, "暴风雪", 1.8)}
})
rogue = CUnit({
    UnitAttr.NAME: "Rogue", UnitAttr.CUR_HP: 20, UnitAttr.MAX_HP: 20,
    UnitAttr.ATK: 8, UnitAttr.CAMP: PLAYER_CAMP,
    UnitAttr.DEF: 2,
    UnitAttr.SKILLS: {0: CSkill(0, "背刺", 1.0), 1: CSkill(1, "致命毒药", 1.4)}
})

# 怪物阵营：恶魔、石像鬼、暗影法师
demon = CUnit({
    UnitAttr.NAME: "Demon", UnitAttr.CUR_HP: 40, UnitAttr.MAX_HP: 40,
    UnitAttr.ATK: 10, UnitAttr.CAMP: MONSTER_CAMP,
    UnitAttr.DEF: 3,
    UnitAttr.SKILLS: {0: CSkill(0, "地狱火", 1.0), 1: CSkill(1, "吸血光环", 1.2)}
})
gargoyle = CUnit({
    UnitAttr.NAME: "Gargoyle", UnitAttr.CUR_HP: 22, UnitAttr.MAX_HP: 22,
    UnitAttr.ATK: 7, UnitAttr.CAMP: MONSTER_CAMP,
    UnitAttr.DEF: 4,
    UnitAttr.SKILLS: {0: CSkill(0, "石化", 1.0)}
})
shadow_mage = CUnit({
    UnitAttr.NAME: "ShadowMage", UnitAttr.CUR_HP: 18, UnitAttr.MAX_HP: 18,
    UnitAttr.ATK: 9, UnitAttr.CAMP: MONSTER_CAMP,
    UnitAttr.DEF: 1,
    UnitAttr.SKILLS: {0: CSkill(0, "暗影箭", 1.0), 1: CSkill(1, "诅咒", 0.9)}
})

config_3v3 = [knight, mage, rogue, demon, gargoyle, shadow_mage]

# 玩家方两位
player_a = CUnit({
    UnitAttr.NAME: "Warrior", UnitAttr.CUR_HP: 22, UnitAttr.MAX_HP: 22,
    UnitAttr.ATK: 8, UnitAttr.CAMP: PLAYER_CAMP,
    UnitAttr.DEF: 2,
    UnitAttr.SKILLS: {0: CSkill(0, "劈砍", 1.0), 1: CSkill(1, "猛击", 1.3)}
})
player_b = CUnit({
    UnitAttr.NAME: "Healer", UnitAttr.CUR_HP: 16, UnitAttr.MAX_HP: 16,
    UnitAttr.ATK: 3, UnitAttr.CAMP: PLAYER_CAMP,
    UnitAttr.DEF: 1,
    UnitAttr.SKILLS: {0: CSkill(0, "治愈", 0.0)}   # 治疗暂不实现，这里仅占位
})

# 敌方镜像（角色名不同，但属性完全一样，保证对称）
enemy_a = CUnit({
    UnitAttr.NAME: "OrcWarrior", UnitAttr.CUR_HP: 22, UnitAttr.MAX_HP: 22,
    UnitAttr.ATK: 8, UnitAttr.CAMP: MONSTER_CAMP,
    UnitAttr.DEF: 2,
    UnitAttr.SKILLS: {0: CSkill(0, "劈砍", 1.0), 1: CSkill(1, "猛击", 1.3)}
})
enemy_b = CUnit({
    UnitAttr.NAME: "Shaman", UnitAttr.CUR_HP: 16, UnitAttr.MAX_HP: 16,
    UnitAttr.ATK: 3, UnitAttr.CAMP: MONSTER_CAMP,
    UnitAttr.DEF: 1,
    UnitAttr.SKILLS: {0: CSkill(0, "治愈", 0.0)}
})

config_2v2 = [player_a, player_b, enemy_a, enemy_b]
# endregion


def EstimateStateSpaceSize(lUnits):
    # 给定每个单位最大HP，计算离散血量的笛卡尔积上限
    # 例如 Hero(30), Guard(15), Monster(40) → 31 * 16 * 41 ≈ 20336
    iLimitSpace = 1
    for oUnit in lUnits:
        iLimitSpace *= oUnit.GetAttr(UnitAttr.MAX_HP)
    return iLimitSpace

def CalculateBranchingFactor(state, camp):
    actions = GetLegalActions(state, camp)
    return len(actions)

def ComputeBranchingStatistics(states: list[CBattleState], camp: int = PLAYER_CAMP):
    if not states:
        return {"min": 0, "max": 0, "avg": 0.0, "count": 0}
    
    lFactors = [CalculateBranchingFactor(s, camp) for s in states]
    return {
        "min": min(lFactors),
        "max": max(lFactors),
        "avg": round(sum(lFactors) / len(lFactors),2),
        "count": len(lFactors)
    }

# --------------------
if __name__ == "__main__":
    random.seed(42)
    for sType,lConfig in [("2V1", config_2v1), ("3V2", config_3v2), ("3V3", config_3v3), ("2V2", config_2v2)]:
        oState = CBattleState(lConfig)
        print(sType, "单位总HP乘积上限", EstimateStateSpaceSize(lConfig))
        oEnv = CBattleSimulator(iMaxTurns=30, lUnits=oState.GetAllUnits())
        oEnv.Reset()
        oRandomAgent = CRandomAgent()
        lState = []
        while not oState.IsTerminal():
            if oState.GetCurrentTurn() % 2 == 0:
                tAction = oRandomAgent.select(oState, PLAYER_CAMP)
            else:
                tAction = oRandomAgent.select(oState, MONSTER_CAMP)
            if tAction is None:
                break
            iUnit, iSkill, iTarget = tAction
            oState = oState.ApplyAction(iUnit, iSkill, iTarget)
            oTempState = oState.clone()
            lState.append(oTempState)
        fReward, oState = oEnv.RunEpisode(oRandomAgent, bRender=False, bVerbose=False)
        print(sType, "分支因子数据", ComputeBranchingStatistics(lState))

"""
运行结果：
2V1 单位总HP乘积上限 18000
2V1 分支因子数据 {'min': 0, 'max': 3, 'avg': 2.5, 'count': 10}
3V2 单位总HP乘积上限 12150000
3V2 分支因子数据 {'min': 0, 'max': 10, 'avg': 6.88, 'count': 16}
3V3 单位总HP乘积上限 141926400
3V3 分支因子数据 {'min': 0, 'max': 18, 'avg': 10.31, 'count': 26}
2V2 单位总HP乘积上限 123904
2V2 分支因子数据 {'min': 0, 'max': 6, 'avg': 4.27, 'count': 11}
"""