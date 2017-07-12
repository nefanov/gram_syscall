import routines

PROC_LIMIT = 2**8#(2**16 - 2)


def init_repr_node(r, parent):
    return routines.Node(r, parent=parent)


def init_text_node(parent, p, g, s):
    return routines.Node("|" + str(p) + " " + str(g) + " " + str(s) + ";", parent=parent)


def fork(node,
         ns_last_pid,
         proc_limit=2**16):
    while pid_checker(node, ns_last_pid)[0] or ns_last_pid == 1 or ns_last_pid == 0:  # 0 - SCHED, 1 - INIT
        ns_last_pid += 1
        ns_last_pid % proc_limit

    routines.Node("|" + str(ns_last_pid) + " " + str(node.g) + " " + str(node.s) + ";", ns_last_pid, node.g, node.s, parent=node)
    #        print ns_last_pid
    ns_last_pid += 1
    ns_last_pid %= proc_limit+1
    return ns_last_pid

def setsid(node):
    if node.p == node.g:
        return -1
    if pgid_checker(node, node.p):
        return -1

    node.s = node.g = node.p
    return 0


def setpgid(node,
            pid=0,
            pgid=0,
            root=None):

    if pid == 0:
        if pgid == 0:
            node.g = node.p
        else:
            node.g = pgid

    if pgid == 0:
        pid = pgid

    proc = pid_checker(node, pid)

    if not proc:
        return -1

    if node.s != proc.s:
        return -1

    if pid == proc.s:
        return -1


    if not root:  # there are no root of process tree
        return -1

    process = pid_checker(root, pid)



    return 0


def exit1(self):
    pass


def exit2(self):
    pass


# returns process with given pid
def pid_checker(r, pid):
    res = [None]
    routines.dfs(r, routines.worker_check_field, routines.worker_empty, ['p', pid], res)
    if not res[-1]:
        return [0]

    return res[-1].value


# returns list of processes in the given session
def sid_checker(r, sid):
    res = [None]
    routines.dfs(r, routines.worker_check_field, routines.worker_empty, ['s', sid], res)
    return res


# returns list of processes of the given group
def pgid_checker(r, pgid):
    res = [None]
    routines.dfs(r, routines.worker_check_field, routines.worker_empty, ['g', pgid], res)
    return res
