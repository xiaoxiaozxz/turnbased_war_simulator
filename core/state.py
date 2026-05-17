import random
from .unit import UnitAttr,CSkill,CUnit,PLAYER_CAMP,MONSTER_CAMP
import logging

class CBattleState:
    """
    Battle status snapshot.
    Design principle: Do not modify in place, all actions return to the new state (in preparation for MCTS).
    """
    def __init__(self, lUnits: list[CUnit], iTurn: int = 0, iMaxTurns: int= 30):
        self.m_Units = lUnits
        self.m_Curturn = iTurn
        self.m_MaxTurns = iMaxTurns
        self.m_EventLog = []  
        self.RefreshUnitPos()
    
    def RefreshUnitPos(self):
        for iPos, oUnit in enumerate(self.m_Units):
            oUnit.SetAttr(UnitAttr.POS, iPos)

    def IsTerminal(self) -> bool:
        """Check if battle has ended (one side eliminated or max turns reached)"""
        if self.m_Curturn >= self.m_MaxTurns:
            return True
        iPlayerAlive = sum(1 for oUnit in self.m_Units if oUnit.IsAlive() and oUnit.GetCamp() == PLAYER_CAMP)
        iMonsterAlive = sum(1 for oUnit in self.m_Units if oUnit.IsAlive() and oUnit.GetCamp() == MONSTER_CAMP)
        return iPlayerAlive <= 0 or iMonsterAlive <= 0

    def GetWinner(self) -> int | None:
        if self.m_Curturn >= self.m_MaxTurns:
            return -1
        for oUnit in self.m_Units:
            if oUnit.IsAlive():
                return oUnit.GetCamp()
        return -1
    
    def GetAllUnitByCamp(self, iCamp:int) -> list[CUnit]:
        """Retrieve all surviving objects based on the camp"""
        lUnit = []
        for oUnit in self.m_Units:
            if oUnit.IsAlive() and oUnit.GetCamp() == iCamp:
                lUnit.append(oUnit)
        return lUnit

    def GetAllUnitIndexByCamp(self, iCamp:int) -> list[int]:
        """Retrieve the index of all surviving objects based on the camp"""
        lUnitIndex = []
        for iIndex, oUnit in enumerate(self.m_Units):
            if oUnit.IsAlive() and oUnit.GetCamp() == iCamp:
                lUnitIndex.append(iIndex)
        return lUnitIndex

    def GetCurrentTurn(self) -> int:
        return self.m_Curturn
    
    def GetMaxTurn(self) -> int:
        return self.m_MaxTurns

    def GetAllUnits(self) -> list[CUnit]:
        return self.m_Units
    
    def GetUnitByPos(self, iPos:int) -> CUnit:
        if iPos < 0 or iPos >= len(self.m_Units):
            return None
        return self.m_Units[iPos]

    def GetLegalActions(self, iCamp: int) -> list[tuple[int, int, int]]:
        """Retrieve all valid actions of the iCamp faction in the current state"""
        lAction = []
        lActionUnit = self.GetAllUnitByCamp(iCamp)
        iTargetCamp = 0 if iCamp == 1 else 1
        lTargetUnit = self.GetAllUnitByCamp(iTargetCamp)
        for oUnit in lActionUnit:
            if oUnit.IsAlive() :
                iAction = oUnit.GetAttr(UnitAttr.POS)
                for iSkill in oUnit.GetSkills():
                    for oTarget in lTargetUnit:
                        if oTarget.IsAlive():
                            iTarget = oTarget.GetAttr(UnitAttr.POS)
                            lAction.append((iAction, iSkill, iTarget))
        return lAction



    def clone(self) -> 'CBattleState':
        """Manual shallow copy+object reconstruction, better performance than deepcopy"""
        lNewUnits = []
        for oUnit in self.m_Units:
            oNewUnit = CUnit.__new__(CUnit)
            oNewUnit.__dict__.update(oUnit.__dict__)
            lNewUnits.append(oNewUnit)
        
        oNewState = CBattleState(lNewUnits, self.m_Curturn, self.m_MaxTurns)
        oNewState.m_EventLog = self.m_EventLog.copy()
        return oNewState

    def ApplyAction(self, iUnitPos: int, iSkillID: int, iTargetPos: int) -> 'CBattleState':
        """Execute a single action: attacker uses skill on target, returns new game state."""
        # 深拷贝当前状态
        oNewState = self.clone()
        lNewUnits = oNewState.GetAllUnits()
        oAttacker = lNewUnits[iUnitPos]
        # 寻找所有存活的敌方单位
        if iTargetPos >= len(lNewUnits):
            # 没有敌人可打，状态不变（实际不会发生）
            oNewState.m_Curturn += 1
            print(" 没有敌人可打，状态不变（实际不会发生） ")
            return oNewState

        oUseSkill = oAttacker.GetSkillBySkillID(iSkillID)

        # 选择一个敌人攻击
        oTarget = lNewUnits[iTargetPos]
        # 计算伤害
        fDamage = round((oAttacker.GetAttr(UnitAttr.ATK, 0)*oUseSkill.GetSkillCoeff() - oTarget.GetDef()) * random.uniform(0.95,1.05), 2)
        fDamage = max(fDamage, 1.0) # 最低为1
        iTargetCurHp = round(max(0, oTarget.GetAttr(UnitAttr.CUR_HP) - fDamage), 2)
        oTarget.SetAttr(UnitAttr.CUR_HP, iTargetCurHp)

        # 生成日志
        sLogEntry = f"Turn {self.m_Curturn}: {oAttacker.GetAttr(UnitAttr.NAME)} 使用{oUseSkill.GetSkillName()}对 {oTarget.GetAttr(UnitAttr.NAME)} 造成 {fDamage} 点伤害。 {oTarget.GetAttr(UnitAttr.NAME)}剩余血量：{oTarget.GetAttr(UnitAttr.CUR_HP)} "
        if not oTarget.IsAlive():
            sLogEntry += f"\n {oTarget.GetAttr(UnitAttr.NAME)}: 阵亡"
        # 构建新状态
        oNewState.m_Curturn += 1
        oNewState.m_EventLog.append(sLogEntry)
        oNewState.RefreshUnitPos()
        return oNewState