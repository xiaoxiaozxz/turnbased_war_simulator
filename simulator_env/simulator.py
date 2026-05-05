import random
from core.unit import *
from core.state import CBattleState
from ai.agents import CRandomAgent,CGreedyAgent
from typing import Optional

class CBattleSimulator:
    def __init__(self, iMaxTurns: int=30, lUnits: list[CUnit]=[]):
        self.m_State: Optional[CBattleState] = None
        self.m_Done: bool = False
        self.m_Units = lUnits
        self.m_MaxTurn = iMaxTurns
        self.Reset()

    def Reset(self) -> CBattleState:
        oHero = CUnit({
            UnitAttr.NAME: "Hero",
            UnitAttr.CUR_HP: 30, UnitAttr.MAX_HP: 30,
            UnitAttr.ATK: 8, UnitAttr.CAMP: PLAYER_CAMP,
            UnitAttr.DEF: 2,
            UnitAttr.SKILLS: {0:CSkill(0, "普通攻击", 1.0),}
        })
        oGuard = CUnit({
            UnitAttr.NAME: "Guard",
            UnitAttr.CUR_HP: 15, UnitAttr.MAX_HP: 15,
            UnitAttr.ATK: 4, UnitAttr.CAMP: PLAYER_CAMP,
            UnitAttr.DEF: 2,
            UnitAttr.SKILLS: {0:CSkill(0, "普通攻击", 1.0),}
        })
        oMonster = CUnit({
            UnitAttr.NAME: "Monster",
            UnitAttr.CUR_HP: 40, UnitAttr.MAX_HP: 40,
            UnitAttr.ATK: 10, UnitAttr.CAMP: MONSTER_CAMP,
            UnitAttr.DEF: 2,
            UnitAttr.SKILLS: {0:CSkill(0, "普通攻击", 1.0),}
        })
        if not self.m_Units:
            self.m_Units = [oHero, oGuard, oMonster]
        self.m_State = CBattleState(self.m_Units, iTurn=0,iMaxTurns=self.m_MaxTurn)
        self.m_Done = False
        return self.m_State
    
    def Step(self, iAttacker:int, iSkill:int, iTarget:int) -> tuple[CBattleState, float, bool, dict]:
        """
        Execute action, return (new status, reward, end, information dictionary).
        The reward is calculated at the end: the player wins+1, the monster wins -1, otherwise 0.
        """
        if self.m_Done:
            return self.m_State, 0.0, True, {"sInfo": "Episode already done"}

        self.m_State = self.m_State.ApplyAction(iAttacker, iSkill, iTarget)
        self.m_Done = self.m_State.IsTerminal()
        fReward = 0.0
        if self.m_Done:
            iWinner = self.m_State.GetWinner()
            if iWinner == PLAYER_CAMP:
                fReward = 1.0
            elif iWinner == MONSTER_CAMP:
                fReward = -1.0

        dInfo = {
            "iCurrentTurn": self.m_State.GetCurrentTurn(),
            "iWinnerCamp": self.m_State.GetWinner()
        }
        return self.m_State, fReward, self.m_Done, dInfo

    def RenderText(self) -> None:
        print(f"=== Turn {self.m_State.GetCurrentTurn()} ===")
        for oUnit in self.m_State.GetAllUnits():
            sStatus = "DEAD" if not oUnit.IsAlive() else f"{oUnit.GetAttr(UnitAttr.CUR_HP)}/{oUnit.GetAttr(UnitAttr.MAX_HP)}"
            sCamp = "PLAYER" if oUnit.GetAttr(UnitAttr.CAMP) == PLAYER_CAMP else "MONSTER"
            print(f"  [{oUnit.GetAttr(UnitAttr.POS)}] {oUnit.GetAttr(UnitAttr.NAME):10} {sCamp:12} {sStatus}")
        if self.m_Done:
            iWinner = self.m_State.GetWinner()
            if iWinner == PLAYER_CAMP:
                print("玩家阵营胜利！")
            elif iWinner == MONSTER_CAMP:
                print("怪物胜利...")
            else:
                print("超过回合上限，平局")
        print("-" * 40)

    def RunEpisode(self, oPlayerAI, bRender: bool = False, bVerbose: bool = False) -> tuple[float, int]:
        """
        Run a complete game, with player factions using given AI decisions and monsters acting randomly.
        Return (total reward, total number of returns).
        """
        self.Reset()
        fTotalReward = 0.0
        lPlayer = [oUnit.GetAttr(UnitAttr.POS) for oUnit in self.m_State.GetAllUnitByCamp(PLAYER_CAMP) if oUnit.IsAlive()]
        lMonster = [oUnit.GetAttr(UnitAttr.POS) for oUnit in self.m_State.GetAllUnitByCamp(MONSTER_CAMP) if oUnit.IsAlive()]
        iSkillID = 0
        while not self.m_Done:
            if self.m_State.GetCurrentTurn() % 2 == 0:
                iAttacker, iSkillID, iTarget = oPlayerAI.select(self.m_State, PLAYER_CAMP)
                if iAttacker not in lPlayer:
                    iAttacker = lPlayer[0] if lPlayer else -1
            else:
                iAttacker, iSkillID, iTarget = CGreedyAgent().select(self.m_State, MONSTER_CAMP)
                if iAttacker not in lMonster:
                    iAttacker = lMonster[0] if lMonster else -1

            if iAttacker == -1 or iTarget == -1:
                break

            _, fReward, _, _ = self.Step(iAttacker, iSkillID, iTarget)
            fTotalReward += fReward
            if bRender:
                self.RenderText()
            if bVerbose and len(self.m_State.m_EventLog) > 0:
                print(self.m_State.m_EventLog[-1])
        return fTotalReward, self.m_State.GetCurrentTurn()


def SimulateBattle(oPlayerAgent, oMonsterAgent, iMaxTurns=30, lUnits: list[CUnit]=[], seed=None, bVerbose: bool = False):
    if seed:
        random.seed(seed)
    oHero = CUnit({
        UnitAttr.NAME: "Hero", UnitAttr.CUR_HP: 30, UnitAttr.MAX_HP: 30,
        UnitAttr.ATK: 8, UnitAttr.CAMP: PLAYER_CAMP,
        UnitAttr.DEF: 2,
        UnitAttr.SKILLS: {0:CSkill(0, "普攻", 1.0), 1:CSkill(1, "重击", 1.5)}
    })
    
    oGuard = CUnit({
        UnitAttr.NAME: "Guard",
        UnitAttr.CUR_HP: 15, UnitAttr.MAX_HP: 15,
        UnitAttr.ATK: 4, UnitAttr.CAMP: PLAYER_CAMP,
        UnitAttr.DEF: 2,
        UnitAttr.SKILLS: {0:CSkill(0, "普通攻击", 1.0),}
    })
    oMonster = CUnit({
        UnitAttr.NAME: "Monster",
        UnitAttr.CUR_HP: 40, UnitAttr.MAX_HP: 40,
        UnitAttr.ATK: 10, UnitAttr.CAMP: MONSTER_CAMP,
        UnitAttr.DEF: 2,
        UnitAttr.SKILLS: {0:CSkill(0, "普通攻击", 1.0),1: CSkill(1, "重击", 1.5)}
    })
    if not lUnits:
            lUnits = [oHero, oGuard, oMonster]
    oState = CBattleState(lUnits, iMaxTurns=iMaxTurns)

    while not oState.IsTerminal():
        if oState.GetCurrentTurn() % 2 == 0:
            tAction = oPlayerAgent.select(oState, PLAYER_CAMP)
        else:
            tAction = oMonsterAgent.select(oState, MONSTER_CAMP)
        if tAction is None:
            break
        iUnit, iSkill, iTarget = tAction
        oState = oState.ApplyAction(iUnit, iSkill, iTarget)
        if bVerbose and len(oState.m_EventLog) > 0:
            print(oState.m_EventLog[-1])
    return oState.GetWinner(), oState.GetCurrentTurn()