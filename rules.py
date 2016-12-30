import routines


class representor:
    def __init__(self, p,g,s, children):
        self.p = p
        self.g = g
        self.s = s
        self.children = children
        return self

    def fork(self, ns_last_pid):
        while pid_checker(self, ns_last_pid):
            ns_last_pid += 1

        self.children.append(representor(ns_last_pid, self.g, self.s, []))

        ns_last_pid += 1
        return ns_last_pid

    def setsid(self,pid,sid):
        pass

    def setpgid(self,pid,pgid):
        pass

    def exit1(self):
        pass

    def exit2(self):
        pass


def pid_checker(r,pid):
    res=0
    routines.dfs(r,routines.worker_check_field,routines.worker_empty,['p',pid],res)
    return res


def sid_checker(r,sid):
    res = 0
    routines.dfs(r,routines.worker_check_field,routines.worker_empty,['s',sid],res)
    return res


def pgid_checker(r,pgid):
    res = 0
    routines.dfs(r,routines.worker_check_field,routines.worker_empty,['g',pgid],res)
    return res
