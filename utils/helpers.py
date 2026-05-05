from core.unit import *


def CloneComparsion():
    """Clone Performance Test"""
    import time
    import copy
    from core.state import CBattleState
    
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
    oState = CBattleState([oHero, oGuard, oMonster])
    
    N = 10000  # 测试次数
    
    # ---- 测试 deepcopy ----
    print("=== 测试 deepcopy 性能 ===")
    iStart = time.perf_counter()
    for _ in range(N):
        # 模拟原版深拷贝逻辑
        oNewUnits = [copy.deepcopy(u) for u in oState.GetAllUnits()]
        oNewState = CBattleState(oNewUnits, oState.GetCurrentTurn(), oState.GetMaxTurn())
        oNewState.m_EventLog = oState.m_EventLog.copy()
    iElapsedDeep = time.perf_counter() - iStart
    print(f"{N} 次 deepcopy 耗时: {iElapsedDeep:.4f} 秒")
    print(f"平均每次: {iElapsedDeep/N*1000000:.2f} 微秒\n")
    
    # ---- 测试自定义 clone ----
    print("=== 测试自定义 clone 性能 ===")
    iStart = time.perf_counter()
    for _ in range(N):
        _ = oState.clone()
    iElapsedClone = time.perf_counter() - iStart
    print(f"{N} 次 clone 耗时: {iElapsedClone:.4f} 秒")
    print(f"平均每次: {iElapsedClone/N*1000000:.2f} 微秒\n")
    
    # ---- 性能对比 ----
    speedup = iElapsedDeep / iElapsedClone
    print(f"自定义 clone 比 deepcopy 快 {speedup:.2f} 倍")
    print(f"单次节省时间: {(iElapsedDeep - iElapsedClone)/N*1000000:.2f} 微秒")

    print("\n=== 功能一致性验证 ===")
    oObjectA = CUnit({
        UnitAttr.NAME:"A", 
        UnitAttr.CUR_HP:10, 
        UnitAttr.MAX_HP:10, 
        UnitAttr.ATK: 8,
        UnitAttr.CAMP: 0,
        UnitAttr.DEF: 2,
        UnitAttr.SKILLS: {0:CSkill(0, "普通攻击", 1.0),}
        })
    oObjectB = CUnit({
        UnitAttr.NAME:"B", 
        UnitAttr.CUR_HP:10, 
        UnitAttr.MAX_HP:10, 
        UnitAttr.ATK: 4,
        UnitAttr.CAMP: 0,
        UnitAttr.DEF: 2,
        UnitAttr.SKILLS: {0:CSkill(0, "普通攻击", 1.0),}
        })
    oTestState = CBattleState([oObjectA, oObjectB])
    oTestState.m_EventLog = ["start"]
    
    # deepcopy 方式
    lNewUnitsDeep = [copy.deepcopy(u) for u in oTestState.GetAllUnits()]
    oStateDeep = CBattleState(lNewUnitsDeep, oTestState.GetCurrentTurn())
    oStateDeep.m_EventLog = oTestState.m_EventLog.copy()
    oUnitDeep = oStateDeep.GetUnitByPos(0)
    iCurHPDeep = oUnitDeep.GetAttr(UnitAttr.CUR_HP, 0)
    oUnitDeep.SetAttr(UnitAttr.CUR_HP, iCurHPDeep-5)
    
    # clone 方式
    oStateClone = oTestState.clone()
    oUnitClone = oStateClone.GetUnitByPos(0)
    iCurHPClone = oUnitClone.GetAttr(UnitAttr.CUR_HP, 0)
    oUnitClone.SetAttr(UnitAttr.CUR_HP, iCurHPClone-5)
    
    # 检查原状态是否未被修改
    oUnitTest = oTestState.GetUnitByPos(0)
    iCurHPTest = oUnitTest.GetAttr(UnitAttr.CUR_HP)
    assert iCurHPTest == 10, "原状态被意外修改！"
    print("原状态未被修改")
    oUnitDeep = oStateDeep.GetUnitByPos(0)
    iCurHPDeep = oUnitDeep.GetAttr(UnitAttr.CUR_HP)
    oUnitClone = oStateClone.GetUnitByPos(0)
    iCurHPClone = oUnitClone.GetAttr(UnitAttr.CUR_HP)
    print(f"deepcopy 新状态 HP: {iCurHPDeep}")
    print(f"clone 新状态 HP: {iCurHPClone}")