# Q : o -> sum(unwrap(R_Q_oper.imglookup('bu', (o,))), (o,), _U_Q) : Top
# Q_oper : o -> {(_v1,) for (o,) in VARS(R__QU_Q_oper) for (o, o_f) in F(f) for (o_f, _v1) in M()} : {(Top, Top)}
# _QU_Q_oper : {(_v5o,) for (_v5o,) in VARS(_U_Q)} : {(Top)}
from incoq.mars.runtime import *
# _M : {(Top, Top)}
_M = Set()
# _F_f : {(Top, Top)}
_F_f = Set()
# _U_Q : {(Top)}
_U_Q = Set()
# R__QU_Q_oper : {(Top)}
R__QU_Q_oper = CSet()
# R_Q_oper : {(Top, Top)}
R_Q_oper = CSet()
# A_Q : {(Top): Number}
A_Q = Map()
# R_Q_oper_bu : {(Top): {(Top)}}
R_Q_oper_bu = Map()
# _F_f_ub : {(Top): {(Top)}}
_F_f_ub = Map()
def _maint_R_Q_oper_bu_for_R_Q_oper_add(_elem):
    (_elem_v1, _elem_v2) = _elem
    _v17_key = (_elem_v1,)
    _v17_value = (_elem_v2,)
    if (_v17_key not in R_Q_oper_bu):
        _v18 = Set()
        R_Q_oper_bu[_v17_key] = _v18
    R_Q_oper_bu[_v17_key].add(_v17_value)

def _maint_R_Q_oper_bu_for_R_Q_oper_remove(_elem):
    (_elem_v1, _elem_v2) = _elem
    _v19_key = (_elem_v1,)
    _v19_value = (_elem_v2,)
    R_Q_oper_bu[_v19_key].remove(_v19_value)
    if (len(R_Q_oper_bu[_v19_key]) == 0):
        del R_Q_oper_bu[_v19_key]

def _maint__F_f_ub_for__F_f_add(_elem):
    (_elem_v1, _elem_v2) = _elem
    _v20_key = (_elem_v2,)
    _v20_value = (_elem_v1,)
    if (_v20_key not in _F_f_ub):
        _v21 = Set()
        _F_f_ub[_v20_key] = _v21
    _F_f_ub[_v20_key].add(_v20_value)

def _maint__F_f_ub_for__F_f_remove(_elem):
    (_elem_v1, _elem_v2) = _elem
    _v22_key = (_elem_v2,)
    _v22_value = (_elem_v1,)
    _F_f_ub[_v22_key].remove(_v22_value)
    if (len(_F_f_ub[_v22_key]) == 0):
        del _F_f_ub[_v22_key]

def _maint_A_Q_for_R_Q_oper_add(_elem):
    (_elem_v1, _elem_v2) = _elem
    _v14_key = (_elem_v1,)
    _v14_value = _elem_v2
    if (_v14_key in _U_Q):
        _v14_state = A_Q[_v14_key]
        _v14_state = ((index(_v14_state, 0) + _v14_value), (index(_v14_state, 1) + 1))
        del A_Q[_v14_key]
        A_Q[_v14_key] = _v14_state

def _maint_A_Q_for_R_Q_oper_remove(_elem):
    (_elem_v1, _elem_v2) = _elem
    _v15_key = (_elem_v1,)
    _v15_value = _elem_v2
    if (_v15_key in _U_Q):
        _v15_state = A_Q[_v15_key]
        _v15_state = ((index(_v15_state, 0) - _v15_value), (index(_v15_state, 1) - 1))
        del A_Q[_v15_key]
        A_Q[_v15_key] = _v15_state

def _maint_A_Q_for__U_Q_add(_key):
    _v16_state = (0, 0)
    (_key_v1,) = _key
    for (_v16_value,) in R_Q_oper_bu.get((_key_v1,), Set()):
        _v16_state = ((index(_v16_state, 0) + _v16_value), (index(_v16_state, 1) + 1))
    A_Q[_key] = _v16_state

def _maint_A_Q_for__U_Q_remove(_key):
    del A_Q[_key]

def _maint_R_Q_oper_for_R__QU_Q_oper_add(_elem):
    (_v8_o,) = _elem
    if hasfield(_v8_o, 'f'):
        _v8_o_f = _v8_o.f
        if isset(_v8_o_f):
            for _v8__v1 in _v8_o_f:
                _v8_result = (_v8_o, _v8__v1)
                if (_v8_result not in R_Q_oper):
                    R_Q_oper.add(_v8_result)
                    _maint_R_Q_oper_bu_for_R_Q_oper_add(_v8_result)
                    _maint_A_Q_for_R_Q_oper_add(_v8_result)
                else:
                    R_Q_oper.inccount(_v8_result)

def _maint_R_Q_oper_for_R__QU_Q_oper_remove(_elem):
    (_v9_o,) = _elem
    if hasfield(_v9_o, 'f'):
        _v9_o_f = _v9_o.f
        if isset(_v9_o_f):
            for _v9__v1 in _v9_o_f:
                _v9_result = (_v9_o, _v9__v1)
                if (R_Q_oper.getcount(_v9_result) == 1):
                    _maint_A_Q_for_R_Q_oper_remove(_v9_result)
                    _maint_R_Q_oper_bu_for_R_Q_oper_remove(_v9_result)
                    R_Q_oper.remove(_v9_result)
                else:
                    R_Q_oper.deccount(_v9_result)

def _maint_R_Q_oper_for__F_f_add(_elem):
    (_v10_o, _v10_o_f) = _elem
    if ((_v10_o,) in R__QU_Q_oper):
        if isset(_v10_o_f):
            for _v10__v1 in _v10_o_f:
                _v10_result = (_v10_o, _v10__v1)
                if (_v10_result not in R_Q_oper):
                    R_Q_oper.add(_v10_result)
                    _maint_R_Q_oper_bu_for_R_Q_oper_add(_v10_result)
                    _maint_A_Q_for_R_Q_oper_add(_v10_result)
                else:
                    R_Q_oper.inccount(_v10_result)

def _maint_R_Q_oper_for__F_f_remove(_elem):
    (_v11_o, _v11_o_f) = _elem
    if ((_v11_o,) in R__QU_Q_oper):
        if isset(_v11_o_f):
            for _v11__v1 in _v11_o_f:
                _v11_result = (_v11_o, _v11__v1)
                if (R_Q_oper.getcount(_v11_result) == 1):
                    _maint_A_Q_for_R_Q_oper_remove(_v11_result)
                    _maint_R_Q_oper_bu_for_R_Q_oper_remove(_v11_result)
                    R_Q_oper.remove(_v11_result)
                else:
                    R_Q_oper.deccount(_v11_result)

def _maint_R_Q_oper_for__M_add(_elem):
    (_v12_o_f, _v12__v1) = _elem
    for (_v12_o,) in _F_f_ub.get((_v12_o_f,), Set()):
        if ((_v12_o,) in R__QU_Q_oper):
            _v12_result = (_v12_o, _v12__v1)
            if (_v12_result not in R_Q_oper):
                R_Q_oper.add(_v12_result)
                _maint_R_Q_oper_bu_for_R_Q_oper_add(_v12_result)
                _maint_A_Q_for_R_Q_oper_add(_v12_result)
            else:
                R_Q_oper.inccount(_v12_result)

def _maint_R_Q_oper_for__M_remove(_elem):
    (_v13_o_f, _v13__v1) = _elem
    for (_v13_o,) in _F_f_ub.get((_v13_o_f,), Set()):
        if ((_v13_o,) in R__QU_Q_oper):
            _v13_result = (_v13_o, _v13__v1)
            if (R_Q_oper.getcount(_v13_result) == 1):
                _maint_A_Q_for_R_Q_oper_remove(_v13_result)
                _maint_R_Q_oper_bu_for_R_Q_oper_remove(_v13_result)
                R_Q_oper.remove(_v13_result)
            else:
                R_Q_oper.deccount(_v13_result)

def _maint_R__QU_Q_oper_for__U_Q_add(_elem):
    (_v6__v5o,) = _elem
    _v6_result = (_v6__v5o,)
    if (_v6_result not in R__QU_Q_oper):
        R__QU_Q_oper.add(_v6_result)
        _maint_R_Q_oper_for_R__QU_Q_oper_add(_v6_result)
    else:
        R__QU_Q_oper.inccount(_v6_result)

def _maint_R__QU_Q_oper_for__U_Q_remove(_elem):
    (_v7__v5o,) = _elem
    _v7_result = (_v7__v5o,)
    if (R__QU_Q_oper.getcount(_v7_result) == 1):
        _maint_R_Q_oper_for_R__QU_Q_oper_remove(_v7_result)
        R__QU_Q_oper.remove(_v7_result)
    else:
        R__QU_Q_oper.deccount(_v7_result)

def _demand_Q(_elem):
    if (_elem not in _U_Q):
        _U_Q.add(_elem)
        _maint_A_Q_for__U_Q_add(_elem)
        _maint_R__QU_Q_oper_for__U_Q_add(_elem)

def main():
    p = Obj()
    q = Obj()
    _v2 = (p, Set())
    index(_v2, 0).f = index(_v2, 1)
    _maint__F_f_ub_for__F_f_add(_v2)
    _maint_R_Q_oper_for__F_f_add(_v2)
    _v3 = (q, Set())
    index(_v3, 0).f = index(_v3, 1)
    _maint__F_f_ub_for__F_f_add(_v3)
    _maint_R_Q_oper_for__F_f_add(_v3)
    for i in [1, 2, 3, 4]:
        r = (p if (i % 2) else q)
        _v4 = (r.f, i)
        index(_v4, 0).add(index(_v4, 1))
        _maint_R_Q_oper_for__M_add(_v4)
    o = p
    print(((_demand_Q((o,)) or True) and index(A_Q[(o,)], 0)))
    o = r
    print(((_demand_Q((o,)) or True) and index(A_Q[(o,)], 0)))

if (__name__ == '__main__'):
    main()
