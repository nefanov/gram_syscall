#include <iostream>
#include <vector>
#include <sstream>
#include <cstdlib>
#include <string>
#include <cstdio>
#include <queue>
#include <climits>

using namespace std;
/* representation structure */
typedef struct repr {
    struct repr *parent; //now is redundant
    unsigned int p;
    unsigned int s;
    unsigned int g;
    vector<struct repr> children;

} representor;

unsigned int ns_last_pid; //last pid representation (as in /sys/kernel/ns_last_pid file from Linux 3.3.*)

representor init_process; // "init" process with first pid

/* init the new process without children */
void init(representor *r,unsigned int p,unsigned int s,unsigned int g) {
    r->p=p;
    r->s=s;
    r->g=g;

    return;
}

/* LIST ROUTINES */
/* list_child_add routine adds given child to the tail of children list */
/* 0 - OK, -1 - ERR */

int list_child_add(representor* parent,representor child) {
    parent->children.push_back(child);
    parent->children[parent->children.size()-1].parent = parent;
    return 0;
}

/* /LIST_ROUTINES */

/* STRINGERS: conversions from strings to smth */

/* stringer_graph_construct: string -> graph representor* 
 * returns:  0 - OK
 *          -1 - parsing error */
//int construct(stringstream* ss, representor* r);

int construct(stringstream* ss, vector<struct repr> vr) {
    char c;
    int res;
    representor r;
    while(!(*ss).eof()) {
        *ss >> c;
        if (c!='|') {
            if (c==']') {
            /*
            (*ss).putback(c);
             */
                return 0;
            }
            return -1;
        }
    
        *ss >> r.p >> r.g >> r.s;
        *ss >> c >> c;
    
        vr.push_back(r); //added to current vector instance
        if (c!='[') {
            vr.erase(vr.end()); //rewert the previous changes
            return -1;
        }
    
        *ss >> c;
        if (c == ']')
            continue;
            
        (*ss).putback(c);
        representor child;
        res = construct(ss,vr[0].children);
    }
    return 0;
}


/* /STRINGERS */

/* WORKERS */

/* worker: reconstruct the string from representor's node*/
void worker_reconstruct(representor* r,void *par) {
    string *s=(string*)par;
    s->append("|");
    s->append(std::to_string(r->p));
    s->append(" ");
    s->append(std::to_string(r->s));
    s->append(" ");
    s->append(std::to_string(r->g));
//  s->append(" ");
    s->append(";[");
}

void worker_reconstruct_finalizer(representor* r, void *par) {
    string *s=(string*)par;
    s->append("]");
}

/* worker: search for process with a given pgid and return pid in *par if there are no one,
 * else return -1 */
void worker_pgid_lookup(representor* r, void *par) {
    if (*(int*)par==r->g)
        *(int*)par=-1;
    
    return;
}
/* work: lookup process with given group (arg0) and return its sid(arg1) */
void worker_lookup_sid_by_pgid(representor *r, void *par) {
    int* args=(int*)par;
    if (r->g==args[0])
        args[1]=r->s;

    return;
}

/* worker: search for process with a given pid and return pid in *par if there are no one,
 * else return -1 */
void worker_lookup_pid(representor *r, void *par) {
    if (*(int*)par==r->p)
        *(int*)par=-1;
    
    return;
}

/* stub worker: nothing to do there:) */
void worker_stub(representor* r, void *par) {
    return;
}
/* worker: count the nodes
int worker_count() {
    static int nodes;
    nodes++;
    return nodes;
}
*/
/* /WORKERS */

/* GRAPH ROUTINES */

/* We need DFS at least for string-from-tree-nodes recursive generation */
int dfs(representor* r, void (*work)(representor*, void*), void (*work_finalizer)(representor*, void*),void *ret) {
    (*work)(r,ret);
    for(vector<struct repr>::iterator it = r->children.begin() ; it != r->children.end(); ++it) {
        dfs(&(*it),work,work_finalizer,ret);

    }
    (*work_finalizer)(r,ret);

    return 0;
}

int bfd(representor* r) {
    static int nodes;
    nodes++;
    
    queue <representor*> q;
    q.push(r);
    
    return nodes;
}

int lookup_pid(representor *r, unsigned int pid) {
    int exists = pid;
    dfs(r, worker_lookup_pid, worker_stub, &exists);
    if (exists==-1)
        return 0;
    return -1;
}

/* RULES */
int rule_fork(representor* parent, unsigned int pid) {
    representor child;
    int pid_cnt = 0;
    init(&child,pid,parent->s,parent->g);
    while (lookup_pid(&init_process, pid)) {
        ns_last_pid++;
        pid_cnt++;
        if (pid_cnt == UINT_MAX)
            return -2; //no new process can be added!
    }
    
    if(list_child_add(parent, child))
        return -1;
    
    return 0;
}

int rule_setsid(representor *parent) {
    if (parent->p == parent->g) {
        return -1;
    }
    /*else if there are any process with group == parent->pid -> return -1*/
    int pgid=parent->p;
    dfs(parent,&worker_pgid_lookup,&worker_stub,&pgid);
    if (pgid==-1) {
        return -1;
    }
    else {
        parent->s = parent->g = parent->p;
    }
    return 0;
}
int rule_setpgid(representor *parent,unsigned int pgid,representor *process) {
    if (!pgid) {
        process->g = parent->p;
        return 0;
    }

    if (process->s!=parent->s) //sessions doesn't match
        return -1;
    if (process->p==process->s) //process is a session leader
        return -1;

    if (process->p==0)
        parent->g=pgid;
    
/*Доп. проверка: найти процесс с pgid Этой группы. Сессии не совпадают - ошибка*/
    int* lookup=(int*)malloc(2*sizeof(int));
    lookup[0] = pgid;
    lookup[1] = -1;
    dfs(parent, &worker_lookup_sid_by_pgid,&worker_stub,lookup);
    if (lookup[1]!=parent->s)
        return -1;

    return 0;
}

void exit(representor* r) {
    return;
}

int abstract_rule(representor *parent,int argc,char** argv) {
    return 0;
}

vector <void*> ftable;




/* /RULES */

/* SET ROUTINES */
representor* bruteforce_fork(representor* r)
{
    representor copy = *r; //get the safe copy
    for (int i=1;i<UINT_MAX;i++) {
        if(!rule_fork(&copy, ns_last_pid)) {
            ns_last_pid++;
            
        }
    }
    
    return r;
}

representor* optimizer(representor*);

/* /SET ROUTINES */

int main()
{

    return 0;
}
