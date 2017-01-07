import re
import rules
from anytree import Node, RenderTree

# workers


def worker_check_field(r, argv, ret=0):
    if (argv[0] == 'p'):
        if (r.p == argv[1]):
            ret = 1

    if (argv[0] == 'g'):
        if (r.g == argv[1]):
            ret = 1

    if (argv[0] == 's'):
        if (r.s == argv[1]):
            ret = 1

    return


# collects all the nodes to the list
def worker_list_nodes(r, argv, ret):
    ret.append(None)
    ret[-1] = r
    return


def worker_print(r, argv, ret=0):
    print r, ":"
    if not r:
        return
    print r.p,r.g,r.s
    return


def worker_empty(r, argv, ret):
    return


def worker_get_sid_by_pgid(r, argv, ret):
    if r.g == argv[0]:
        ret = r.s


def reconstruct_finalizer(r, argv, ret):
    ret = argv + "]"
    return


def fill_lvl(r, lst):
    r_lvl = r
    for num, line in enumerate(lst):
        print line
        if line == '':
            continue

        tmp_s = re.findall('\d+', line)
        tmp_v = rules.representor(r_lvl, tmp_s[0], tmp_s[1], tmp_s[2], [])
        r_lvl.children.append(tmp_v)

        if (line[-1] == '['):
            r_lvl = r_lvl.children[-1]
        elif (line[-1] == line[-2] == ']'):
            r_lvl = r_lvl.parent

    return r

# extensive string split by cStringIO routines
def split_extensive(ss, r):
    # type: (string, representor) -> representor
    fill_lvl(r, ss.split('|'))
    return r


def construct(ss, r):
    return split_extensive(ss, r)


#
# worker_reconstruct: reconstruct the string from sub-tree representation
def worker_reconstruct(r, argv, ret):
    ret = argv + "|" + str(r.p) + " " + str(r.s) + " " + str(r.g) + ";["


# process_graph_routines


def dfs(r, func, func_finalizer, argv, ret):
    # type: (representor, worker_func, finalizer, args, retvals) -> void
    if not r:
        return

    func(r, argv, ret)
    func_finalizer(r, argv, ret)

    for node in r.children:
        dfs(node, func, func_finalizer, argv, ret)
    return


def construct(r):
    res = ""
    dfs(r, worker_reconstruct, worker_empty, res, res)
    return res





