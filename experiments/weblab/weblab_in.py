# Social network example.

from incoq.runtime import *

CONFIG(
    obj_domain = 'true',
)

SYMCONFIG('Q',
#    count_elim_safe_override = 'true',
    well_typed_data = 'true',
)

#def make_user(email, loc):
#    u = Obj()
#    u.followers = Set()
#    u.email = email
#    u.loc = loc
#    return u
#
#def make_group():
#    g = Set()
#    return g
#
#def follow(u, c):
#    assert u not in c.followers
#    c.followers.add(u)
#
#def unfollow(u, c):
#    assert u in c.followers
#    c.followers.remove(u)
#
#def join_group(u, g):
#    assert u not in g
#    g.add(u)
#
#def leave_group(u, g):
#    assert u in g
#    g.remove(u)
#
#def change_loc(u, loc):
#    del u.loc
#    u.loc = loc
#
#def do_query(celeb, group):
#    return QUERY('Q', {user.email for user in celeb.followers if user in group
#                                  if user.loc == 'NYC'})
#
#def do_query_nodemand(celeb, group):
#    return QUERY('Q', {user.email for user in celeb.followers if user in group
#                                  if user.loc == 'NYC'},
#                 {'nodemand': True})



def make_submission(assignment, student):
    s = Obj()
    s.assignment = assignment
    s.student = student
    return s

def change_student(submission, student):
    submission.student = student

def parent(submission1):
    return QUERY('Q',
                 {submission2
                  for assignment1 in submission1.assignment
                  for assignment2 in assignment1.parent
                  for submission2 in assignment2.submissions
                  for student in submission1.student
                  for submission2 in student.submissions
                 },
                 {'nodemand': True}
                )
