import enum as en


@en.unique
class MarioForms(en.IntEnum):
    """0 is basic, 1 is fireman, 2 is superform"""
    basic: int = 0
    fireman: int = 1
    super_form: int = 2


@en.unique
class ProcStatus(en.IntEnum):
    """0 is ok, 1 is err, 2 is stuck"""
    ok: int = 0
    err: int = 1
    stuck: int = 2


@en.unique
class EntityName(en.IntEnum):
    """0 is player, 1 is monster, 2 is other"""
    player: int = 0
    monster: int = 1
    other: int = 2
