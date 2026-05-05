PLAYER_CAMP = 0
MONSTER_CAMP = 1

class UnitAttr:
    NAME = "m_Name"
    MAX_HP = "m_MaxHp"
    CUR_HP = "m_CurHp"
    ATK = "m_Atk"
    CAMP = "m_Camp"
    POS = "m_Pos"
    DEF = "m_Def"
    SKILLS = "m_Skills"

class CSkill:
    def __init__(self, iSkillID: int, sName: str ,iCoeff: float):
        self.m_SkillID = iSkillID
        self.m_Name = sName
        self.m_Coeff = iCoeff

    def GetSkillName(self):
        return self.m_Name
    
    def GetSkillID(self):
        return self.m_SkillID
    
    def GetSkillCoeff(self):
        return self.m_Coeff

    def __repr__(self):
        return f"skill({self.m_SkillID}): {self.m_Name}, coeff={self.m_Coeff}"

class CUnit:
    def __init__(self, dUnit: dict):
        defaults = {
            UnitAttr.NAME: "Unknown",
            UnitAttr.MAX_HP: 10,
            UnitAttr.CUR_HP: 10,
            UnitAttr.ATK: 5,
            UnitAttr.CAMP: 0,
            UnitAttr.DEF: 2,
            UnitAttr.SKILLS: {0: CSkill(0, "普通攻击", 1.0),}
        }
        # 用传入数据覆盖默认值
        defaults.update(dUnit)
        # 批量设置属性
        for key, value in defaults.items():
            setattr(self, key, value)
    
    def refreshUnit(self, dUnit: dict):
        for key, value in dUnit.items():
            setattr(self, key, value)

    def GetAttr(self, attr_name: str, default=None):
        return getattr(self, attr_name, default)
    
    def IsAlive(self):
        return self.GetAttr(UnitAttr.CUR_HP) > 0

    def GetSkills(self):
        return self.GetAttr(UnitAttr.SKILLS).keys()

    def GetSkillBySkillID(self, iSkillID:int):
        return self.GetAttr(UnitAttr.SKILLS).get(iSkillID)

    def GetCamp(self):
        return self.GetAttr(UnitAttr.CAMP)
    
    def GetDef(self):
        return self.GetAttr(UnitAttr.DEF)

    def SetAttr(self, attr_name: str, value):
        setattr(self, attr_name, value)

    def __repr__(self):
        return str(self.__dict__)