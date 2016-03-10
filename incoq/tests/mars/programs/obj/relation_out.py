# Q : z -> {(z, x) for (z,) in REL(_U_Q) for (z, x) in M() for (x,) in REL(S_wrapped)} : {({Number}, Number)}
from incoq.mars.runtime import *
# S : {Number}
S = Set()
# _M : {(Top, Top)}
_M = Set()
# S_wrapped : {(Number)}
S_wrapped = Set()
# _U_Q : {({Number})}
_U_Q = Set()
# R_Q : {({Number}, Number)}
R_Q = CSet()
# _M_ub : {Top: {Top}}
_M_ub = Map()
# R_Q_bu : {{Number}: {Number}}
R_Q_bu = Map()
def _maint__M_ub_for__M_add(_elem):
    (_elem_v1, _elem_v2) = _elem
    _v11_key = _elem_v2
    _v11_value = _elem_v1
    if (_v11_key not in _M_ub):
        _v12 = Set()
        _M_ub[_v11_key] = _v12
    _M_ub[_v11_key].add(_v11_value)

def _maint__M_ub_for__M_remove(_elem):
    (_elem_v1, _elem_v2) = _elem
    _v13_key = _elem_v2
    _v13_value = _elem_v1
    _M_ub[_v13_key].remove(_v13_value)
    if (len(_M_ub[_v13_key]) == 0):
        del _M_ub[_v13_key]

def _maint_R_Q_bu_for_R_Q_add(_elem):
    (_elem_v1, _elem_v2) = _elem
    _v14_key = _elem_v1
    _v14_value = _elem_v2
    if (_v14_key not in R_Q_bu):
        _v15 = Set()
        R_Q_bu[_v14_key] = _v15
    R_Q_bu[_v14_key].add(_v14_value)

def _maint_R_Q_bu_for_R_Q_remove(_elem):
    (_elem_v1, _elem_v2) = _elem
    _v16_key = _elem_v1
    _v16_value = _elem_v2
    R_Q_bu[_v16_key].remove(_v16_value)
    if (len(R_Q_bu[_v16_key]) == 0):
        del R_Q_bu[_v16_key]

def _maint_R_Q_for__U_Q_add(_elem):
    (_v5_z,) = _elem
    if isset(_v5_z):
        for _v5_x in _v5_z:
            if ((_v5_x,) in S_wrapped):
                _v5_result = (_v5_z, _v5_x)
                if (_v5_result not in R_Q):
                    R_Q.add(_v5_result)
                    _maint_R_Q_bu_for_R_Q_add(_v5_result)
                else:
                    R_Q.inccount(_v5_result)

def _maint_R_Q_for__U_Q_remove(_elem):
    (_v6_z,) = _elem
    if isset(_v6_z):
        for _v6_x in _v6_z:
            if ((_v6_x,) in S_wrapped):
                _v6_result = (_v6_z, _v6_x)
                if (R_Q.getcount(_v6_result) == 1):
                    _maint_R_Q_bu_for_R_Q_remove(_v6_result)
                    R_Q.remove(_v6_result)
                else:
                    R_Q.deccount(_v6_result)

def _maint_R_Q_for__M_add(_elem):
    (_v7_z, _v7_x) = _elem
    if ((_v7_z,) in _U_Q):
        if ((_v7_x,) in S_wrapped):
            _v7_result = (_v7_z, _v7_x)
            if (_v7_result not in R_Q):
                R_Q.add(_v7_result)
                _maint_R_Q_bu_for_R_Q_add(_v7_result)
            else:
                R_Q.inccount(_v7_result)

def _maint_R_Q_for__M_remove(_elem):
    (_v8_z, _v8_x) = _elem
    if ((_v8_z,) in _U_Q):
        if ((_v8_x,) in S_wrapped):
            _v8_result = (_v8_z, _v8_x)
            if (R_Q.getcount(_v8_result) == 1):
                _maint_R_Q_bu_for_R_Q_remove(_v8_result)
                R_Q.remove(_v8_result)
            else:
                R_Q.deccount(_v8_result)

def _maint_R_Q_for_S_wrapped_add(_elem):
    (_v9_x,) = _elem
    for _v9_z in _M_ub.get(_v9_x, Set()):
        if ((_v9_z,) in _U_Q):
            _v9_result = (_v9_z, _v9_x)
            if (_v9_result not in R_Q):
                R_Q.add(_v9_result)
                _maint_R_Q_bu_for_R_Q_add(_v9_result)
            else:
                R_Q.inccount(_v9_result)

def _maint_R_Q_for_S_wrapped_remove(_elem):
    (_v10_x,) = _elem
    for _v10_z in _M_ub.get(_v10_x, Set()):
        if ((_v10_z,) in _U_Q):
            _v10_result = (_v10_z, _v10_x)
            if (R_Q.getcount(_v10_result) == 1):
                _maint_R_Q_bu_for_R_Q_remove(_v10_result)
                R_Q.remove(_v10_result)
            else:
                R_Q.deccount(_v10_result)

def _demand_Q(_elem):
    if (_elem not in _U_Q):
        _U_Q.add(_elem)
        _maint_R_Q_for__U_Q_add(_elem)

def _maint_S_wrapped_for_S_add(_elem):
    _v3_v = (_elem,)
    S_wrapped.add(_v3_v)
    _maint_R_Q_for_S_wrapped_add(_v3_v)

def _maint_S_wrapped_for_S_remove(_elem):
    _v4_v = (_elem,)
    _maint_R_Q_for_S_wrapped_remove(_v4_v)
    S_wrapped.remove(_v4_v)

def main():
    r = Set()
    t = Set()
    for i in [1, 2, 3, 4]:
        if ((i % 2) == 1):
            _v1 = (r, i)
            index(_v1, 0).add(index(_v1, 1))
            _maint__M_ub_for__M_add(_v1)
            _maint_R_Q_for__M_add(_v1)
        else:
            _v2 = (t, i)
            index(_v2, 0).add(index(_v2, 1))
            _maint__M_ub_for__M_add(_v2)
            _maint_R_Q_for__M_add(_v2)
        S.add(i)
        _maint_S_wrapped_for_S_add(i)
    z = r
    print(sorted(((_demand_Q((z,)) or True) and R_Q_bu.get(z, Set()))))
    z = t
    print(sorted(((_demand_Q((z,)) or True) and R_Q_bu.get(z, Set()))))

if (__name__ == '__main__'):
    main()
