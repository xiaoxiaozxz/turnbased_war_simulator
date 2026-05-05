from core.unit import *
from core.state import CBattleState

def GetLegalActions(oState: CBattleState, iCamp: int) -> list[tuple[int, int, int]]:
        """Retrieve all valid actions of the iCamp faction in the current state"""
        lAction = []
        lActionUnit = oState.GetAllUnitByCamp(iCamp)
        iTargetCamp = MONSTER_CAMP if iCamp == PLAYER_CAMP else PLAYER_CAMP
        lTargetUnit = oState.GetAllUnitByCamp(iTargetCamp)
        for oUnit in lActionUnit:
            if oUnit.IsAlive() :
                iAction = oUnit.GetAttr(UnitAttr.POS)
                for iSkill in oUnit.GetSkills():
                    for oTarget in lTargetUnit:
                        if oTarget.IsAlive():
                            iTarget = oTarget.GetAttr(UnitAttr.POS)
                            lAction.append((iAction, iSkill, iTarget))
        return lAction