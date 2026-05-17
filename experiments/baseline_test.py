import sys
import os

# Get the directory where the current file is located (experiments)
current_dir = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory (project root directory turn_battle_sim)
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

import random, time, csv
import matplotlib.pyplot as plt
from ai.agents import CRandomAgent,CGreedyAgent, CRandomSearchAgent
from simulator_env.simulator import CBattleSimulator, SimulateBattle
from core.unit import CUnit,UnitAttr,CSkill,PLAYER_CAMP,MONSTER_CAMP


def BaseLineTest(oPlayerAgent, oMonsterAgent,lUnits=[], sTestName="Random vs Random",iMaxTurns=13, N=1000):
    # random.seed(42)
    iWinsPlayer = 0
    iWinsMonster = 0
    iDraws = 0
    lTurns = []
    lTurnInfo = []
    start = time.perf_counter()
    for i in range(N):
        iWinner, iTurn = SimulateBattle(oPlayerAgent, oMonsterAgent, iMaxTurns=iMaxTurns, lUnits=lUnits)
        lTurns.append(iTurn)
        if iWinner == PLAYER_CAMP:
            iWinsPlayer += 1
            lTurnInfo.append(("player", iTurn))
        elif iWinner == MONSTER_CAMP:
            iWinsMonster += 1
            lTurnInfo.append(("monster", iTurn))
        else:
            lTurnInfo.append(("draw", iTurn))
            iDraws += 1
    elapsed = time.perf_counter() - start
    print(f"=========== {sTestName} ========")
    print(f"完成 {N} 场，耗时 {elapsed:.2f} 秒")
    print(f"玩家胜: {iWinsPlayer} ({iWinsPlayer/N*100:.1f}%)")
    print(f"怪物胜: {iWinsMonster} ({iWinsMonster/N*100:.1f}%)")
    print(f"平局: {iDraws} ({iDraws/N*100:.1f}%)")
    print(f"平均回合: {sum(lTurns)/N:.1f}")
    # 保存 CSV
    with open(f'docs/phase1/baseline_{sTestName}.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['game_id', 'winner', 'turns'])
        for i, tTurnInfo in enumerate(lTurnInfo):
            winner_str = tTurnInfo[0]
            writer.writerow([i, winner_str, tTurnInfo[1]])

    import matplotlib.pyplot as plt
    plt.bar(['Player Win','Monster Win','Draw'], [iWinsPlayer, iWinsMonster, iDraws])
    plt.title(f'{sTestName} Baseline (1000 games)')
    plt.savefig(f'docs/phase1/baseline_hist_{sTestName}.png')
    plt.show()

N = 1000
iMaxTurns = 12
oHero = CUnit({
        UnitAttr.NAME: "Hero", UnitAttr.CUR_HP: 30, UnitAttr.MAX_HP: 30,
        UnitAttr.ATK: 8, UnitAttr.CAMP: PLAYER_CAMP,
        UnitAttr.DEF: 2,  # 假设给点防御
        UnitAttr.SKILLS: {0:CSkill(0, "普攻", 1.0), 1:CSkill(1, "重击", 1.5)}
    })
    
oGuard = CUnit({
    UnitAttr.NAME: "Guard",
    UnitAttr.CUR_HP: 15, UnitAttr.MAX_HP: 15,
    UnitAttr.ATK: 4, UnitAttr.CAMP: PLAYER_CAMP,
    UnitAttr.DEF: 2,
    UnitAttr.SKILLS: {0:CSkill(0, "普通攻击", 1.0),}
})
oMonster1 = CUnit({
    UnitAttr.NAME: "Monster1",
    UnitAttr.CUR_HP: 30, UnitAttr.MAX_HP: 30,
    UnitAttr.ATK: 10, UnitAttr.CAMP: MONSTER_CAMP,
    UnitAttr.DEF: 2,
    UnitAttr.SKILLS: {0:CSkill(0, "普通攻击", 1.0),1: CSkill(1, "重击", 1.5)}
})
oMonster2 = CUnit({
    UnitAttr.NAME: "Monster2",
    UnitAttr.CUR_HP: 10, UnitAttr.MAX_HP: 10,
    UnitAttr.ATK: 10, UnitAttr.CAMP: MONSTER_CAMP,
    UnitAttr.DEF: 2,
    UnitAttr.SKILLS: {0:CSkill(0, "普通攻击", 1.0),1: CSkill(1, "重击", 1.5)}
})
lUnits = [oHero, oGuard, oMonster1, oMonster2]


# BaseLineTest(CRandomAgent(), CRandomAgent(),lUnits=lUnits, sTestName="RandomVSRandom",iMaxTurns=iMaxTurns,N=N)
# BaseLineTest(CGreedyAgent(), CGreedyAgent(),lUnits=lUnits, sTestName="GreedyVSGreedy",iMaxTurns=iMaxTurns,N=N)
# BaseLineTest(CGreedyAgent(), CRandomAgent(),lUnits=lUnits, sTestName="GreedyVSRandom",iMaxTurns=iMaxTurns,N=N)
BaseLineTest(CRandomSearchAgent(), CRandomAgent(),lUnits=lUnits, sTestName="RandomSearchAgentVSRandom",iMaxTurns=iMaxTurns,N=3)
