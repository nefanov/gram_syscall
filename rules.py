import routines

PROC_LIMIT = 2**16

class representor:
    def __init__(self, parent, p, g, s, children):
        self.parent = parent
        self.p = p
        self.g = g
        self.s = s
        self.children = children
        return

    def fork(self, ns_last_pid):
        while pid_checker(self, ns_last_pid):
            ns_last_pid += 1
            ns_last_pid % PROC_LIMIT

        self.children.append(representor(self, ns_last_pid, self.g, self.s, []))

        ns_last_pid += 1
        ns_last_pid % PROC_LIMIT
        return ns_last_pid

    def setsid(self):
        if self.p == self.g:
            return -1
        if pgid_checker(self, self.p):
            return -1

        self.s = self.g = self.p
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

        if process.s != self.s: # ?????????
            return -1

        return 0

    def exit1(self):
        pass

    def exit2(self):
        pass


# returns process with given pid
def pid_checker(r, pid):
    res = None
    routines.dfs(r, routines.worker_check_field, routines.worker_empty, ['p', pid], res)
    return res


# returns list of processes in the given session
def sid_checker(r, sid):
    res = None
    routines.dfs(r, routines.worker_check_field, routines.worker_empty, ['s', sid], res)
    return res


# returns list of processes of the given group
def pgid_checker(r, pgid):
    res = None
    routines.dfs(r, routines.worker_check_field, routines.worker_empty, ['g', pgid], res)
    return res
