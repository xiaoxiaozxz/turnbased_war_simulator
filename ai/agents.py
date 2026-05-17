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

class CRandomSearchAgent(CBaseAgent):
    # Random Action Sequence Search Agent
    def __init__(self, K=10, N=20, H=20):
        self.K = K
        self.N = N
        self.H = H

    def select(self, oState, iCamp):
        lAction = GetLegalActions(oState, iCamp)
        if len(lAction) == 0:
            return [-1,-1,-1]
        if len(lAction) == 1:
            return lAction[0]

        tBestAction = lAction[0]
        fBestScore = -1.0

        for tAction in lAction:
            # apply candidate actions to the copy
            iUnitPos, iSkillID, iTargetPos = tAction
            oNextState = oState.ApplyAction(iUnitPos, iSkillID, iTargetPos)
            iTurnCamp = (iCamp + 1)%2
            fTotalRReward = 0.0
            for k in range(self.K):
                for n in range(self.N):
                    fReward = self.RandomRollout(oNextState, self.H - 1, iTurnCamp)
                    fTotalRReward += fReward

            fAvgReward = fTotalRReward / (self.K * self.N)
            if fAvgReward > fBestScore:
                fBestScore = fAvgReward
                tBestAction = tAction
        print("tBestActon", tBestAction)
        return tBestAction
    
    def RandomRollout(self, oState, iLength, iTurnCamp):
        oNewState = oState.clone()
        fReward = 0.5
        for i in range(iLength):
            iCamp = (iTurnCamp + i)%2
            lAction = GetLegalActions(oNewState, iCamp)
            if lAction:
                iUnitPos, iSkillID, iTargetPos = random.choice(lAction)
                oNewState = oNewState.ApplyAction(iUnitPos, iSkillID, iTargetPos)
            if oState.IsTerminal():
                fReward = int(oState.GetWinner() == PLAYER_CAMP) if oState.GetWinner() != -1 else 0.5
                break
        return fReward