# Q : a -> {(a, x) for (a,) in REL(_U_Q) for (x,) in REL(S) if (x > a)} : {(Number, Number)}
from incoq.runtime import *
# S : {(Number)}
S = Set()
# _U_Q : {(Number)}
_U_Q = LRUSet()
# R_Q_bu : {Number: {(Number)}}
R_Q_bu = Map()
def _maint_R_Q_bu_for_R_Q_add(_elem):
    (_elem_v1, _elem_v2) = _elem
    _v7_key = _elem_v1
    _v7_value = (_elem_v2,)
    if (_v7_key not in R_Q_bu):
        _v8 = Set()
        R_Q_bu[_v7_key] = _v8
    R_Q_bu[_v7_key].add(_v7_value)

def _maint_R_Q_bu_for_R_Q_remove(_elem):
    (_elem_v1, _elem_v2) = _elem
    _v9_key = _elem_v1
    _v9_value = (_elem_v2,)
    R_Q_bu[_v9_key].remove(_v9_value)
    if (len(R_Q_bu[_v9_key]) == 0):
        del R_Q_bu[_v9_key]

def _maint_R_Q_for__U_Q_add(_elem):
    (_v3_a,) = _elem
    for (_v3_x,) in S:
        if (_v3_x > _v3_a):
            _v3_result = (_v3_a, _v3_x)
            _maint_R_Q_bu_for_R_Q_add(_v3_result)

def _maint_R_Q_for__U_Q_remove(_elem):
    (_v4_a,) = _elem
    for (_v4_x,) in S:
        if (_v4_x > _v4_a):
            _v4_result = (_v4_a, _v4_x)
            _maint_R_Q_bu_for_R_Q_remove(_v4_result)

def _maint_R_Q_for_S_add(_elem):
    (_v5_x,) = _elem
    for (_v5_a,) in _U_Q:
        if (_v5_x > _v5_a):
            _v5_result = (_v5_a, _v5_x)
            _maint_R_Q_bu_for_R_Q_add(_v5_result)

def _demand_Q(_elem):
    if (_elem not in _U_Q):
        while (len(_U_Q) >= 3):
            _stale = _U_Q.peek()
            _maint_R_Q_for__U_Q_remove(_stale)
            _U_Q.remove(_stale)
        _U_Q.add(_elem)
        _maint_R_Q_for__U_Q_add(_elem)

def main():
    for v in [1, 3]:
        _v1 = (v,)
        S.add(_v1)
        _maint_R_Q_for_S_add(_v1)
    a = 2
    print(sorted(((_demand_Q((a,)) or True) and (R_Q_bu[a] if (a in R_Q_bu) else Set()))))
    for v in [2, 4]:
        _v2 = (v,)
        S.add(_v2)
        _maint_R_Q_for_S_add(_v2)
    print(sorted(((_demand_Q((a,)) or True) and (R_Q_bu[a] if (a in R_Q_bu) else Set()))))
    print(sorted((R_Q_bu[a] if (a in R_Q_bu) else Set())))
    R_Q_bu.dictclear()
    _U_Q.clear()
    R_Q_bu.dictclear()
    _U_Q.clear()

if (__name__ == '__main__'):
    main()
