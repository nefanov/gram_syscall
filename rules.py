import routines

PROC_LIMIT = 3# (2**16 - 2)


def init_repr_node(r, parent):
    return routines.Node(r, parent=parent)


def init_text_node(parent, p, g, s):
    return routines.Node("|" + str(p) + " " + str(g) + " " + str(s) + ";", parent=parent)


def fork(node, ns_last_pid):
    while pid_checker(node, ns_last_pid)[0] or ns_last_pid == 1 or ns_last_pid == 0:  # 0 - SCHED, 1 - INIT
        ns_last_pid += 1
        ns_last_pid % PROC_LIMIT

    routines.Node("|" + str(ns_last_pid) + " " + str(node.g) + " " + str(node.s) + ";", ns_last_pid, node.g, node.s, parent=node)
    #        print ns_last_pid
    ns_last_pid += 1
    ns_last_pid %= PROC_LIMIT
    return ns_last_pid

def setsid(node):
    if node.p == node.g:
        return -1
    if pgid_checker(node, node.p):
        return -1

    node.s = node.g = node.p
    return 0


def setpgid(self, pid=0, pgid=0, root=None):
    if pid == 0:
        if pgid == 0:
            self.g = self.p
        else:
            self.g = pgid

        return 0

    if not root:  # there are no root of process tree
        return -1

    process = pid_checker(root, pid)
    if not process:
        return -1

    if pgid == 0:
        process.g = self.p
        return 0

    if process.s != self.s:
        return -1

    if process.s != self.s:  # ?????????
        return -1

    return 0


def exit1(self):
    pass


def exit2(self):
    pass


# returns process with given pid
def pid_checker(r, pid):
    res = [None]
    routines.dfs(r, routines.worker_check_field, routines.worker_empty, ['p', pid], res)
    return res


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
