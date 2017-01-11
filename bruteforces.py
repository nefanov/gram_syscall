import routines
import rules
import sys

g_num = 1

def print_log_iteration(iteration=0, power_limit=0, state_notation=""):
    if iteration:
        print "iteration: " + iteration
    if power_limit:
        print "power_limit: " + power_limit
    print state_notation

# in general, transform functions runs dfs, but in is unefficient method


# list transformation for
def fork_lst_transform(argv):
    new_lst=list(argv[1])
    new_lst.insert(argv[0] + 1, argv[1][argv[0]].children[-1])
    return new_lst


# make rule steps for each of node then go further
# lst is temporary list with no strict order
# until MAX_PROC_NUM list len is exceeted, then exit.
# rule is transformation rule with correct argv args (no check!)
# log_tree is n-are tree for string notation logging (see
#  'routines.construct' function) .

def perm(r, lst, rls, argv, func_lst_transform=[None], is_log=0, log_tree=None, max_proc_num=rules.PROC_LIMIT):
    if len(lst) >= max_proc_num:
        return

    global g_num
    g_num += 1
    for num, node in enumerate(lst):
        for rn, rule in enumerate(rls):

            argv_ret = getattr(node, rule)(*argv[rn])
            # log current state into the log_tree
            if is_log:
                log_tree = routines.Node([rule, '('+','.join([str(x) for x in argv[rn]])+')', routines.construct(r)], parent=log_tree)
                print "node #" + str(num+1) + " of " + str(len(lst)) + ":" + routines.construct(r)[0] + " ; "
            new_lst = list(lst)
            try:
                if func_lst_transform[rn]:
                    new_lst = func_lst_transform[rn]([num, lst])
            except IndexError:
                if func_lst_transform[-1]:
                    new_lst = func_lst_transform[-1]([num, lst])

            perm(r, new_lst, rls, [[argv_ret]], func_lst_transform, is_log, log_tree, max_proc_num)
#            print 'branch' + str(g_num) + 'ended'
#            routines.log_output(log_tree, "log_tree"+ str(g_num)+".txt")
#            routines.pkl_write(log_tree, "log_tree"+str(g_num)+".pkl")
#            routines.pkl_write(log_tree, "process_tree"+str(g_num)+".repr")
    return


def brute_fork(r=rules.representor(None, 1, 1, 1, []), ns_last_pid=1, is_log=1, log_tree=routines.Node(["", "", "|1 1 1 ;[]"])):
    lst = []
    routines.dfs(r, routines.worker_list_nodes, routines.worker_empty, [], lst)
    sys.setrecursionlimit(1000000)
    perm(r, lst, ["fork"], [[ns_last_pid]], [fork_lst_transform], is_log, log_tree)

    routines.log_output(log_tree, "log_tree.txt")
    routines.pkl_write(log_tree,"log_tree.pkl")
    routines.pkl_write(log_tree, "process_tree.repr")
    return r


brute_fork()
