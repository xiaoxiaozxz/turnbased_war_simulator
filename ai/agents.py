import random
from core.unit import *
from core.state import CBattleState
from ai.actions import GetLegalActions


class CBaseAgent:
    def select(self, state, camp) -> tuple[int,int,int] | None:
        raise NotImplementedError

class CRandomAgent(CBaseAgent):
    def select(self, oState, iCamp):
        lAction = GetLegalActions(oState, iCamp)
        return random.choice(lAction) if lAction else None

class CGreedyAgent(CBaseAgent):
    def select(self, oState, iCamp):
        lAction = oState.GetLegalActions(iCamp=iCamp)
        # Sort in descending order of attack power
        if not lAction:
            return [-1,-1,-1]
        fBestDamage = -1
        tBestAction = lAction[0]
        for tAction in lAction:
            iUnitPos, iSkill, iTargetPos = tAction
            iAttack = oState.GetUnitByPos(iUnitPos).GetAttr(UnitAttr.ATK)
            iCoeff = oState.GetUnitByPos(iUnitPos).GetSkillBySkillID(iSkill).GetSkillCoeff()
            iDef = oState.GetUnitByPos(iTargetPos).GetAttr(UnitAttr.DEF)
            if iAttack*iCoeff - iDef > fBestDamage:
                fBestDamage = max(iAttack*iCoeff - iDef, 1)
                tBestAction = tAction
        return tBestAction