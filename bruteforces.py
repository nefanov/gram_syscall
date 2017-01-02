import routines
import rules

global ns_last_pid


# make fork steps for each of node then go further
# lst is temporary list with no strict order
# until MAX_PROC_NUM list len is exceeted, then exit.
# log_tree is n-are tree for string notation logging (see
#  'routines.construct' function) .

def perm(r, lst, is_log=0, log_tree=None, max_proc_num=2 ** 16):
    if len(lst) >= max_proc_num:
        return

    for num, node in enumerate(lst):
        ns_last_pid = node.fork(ns_last_pid)
        if is_log:
            log_tree.append(routines.construct(r))

        new_lst = list(lst)
        new_lst.insert(num + 1, node.children[-1])
        perm(r, new_lst)

    return


def brute_fork(r):
    lst = []
    routines.dfs(r, routines.worker_list_nodes(), routines.worker_empty, [], lst)
    return r
