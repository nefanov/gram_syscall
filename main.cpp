#include <iostream>
#include <vector>

using namespace std;
/* representation structure */
typedef struct repr {
    unsigned int p;
    unsigned int s;
    unsigned int g;
    vector<struct repr> children;

} representor;

/* init the new process without children */
void init(representor *r,unsigned int p,unsigned int s,unsigned int g) {
    r->p=p;
    r->s=s;
    r->g=g;
    r->children = NULL;
    return;
}

/* LIST ROUTINES */
/* list_child_add routine adds given child to the tail of children list */
/* 0 - OK, -1 - ERR */

int list_child_add(representor* parent,representor child) {
    parent->children.push_back(child);

    return 0;
}

/* GRAPH ROUTINES */
int dfs(representor* r) {
    static int nodes;
    nodes++;
    for(vector<struct repr>::iterator it = r->children.begin() ; it != r->children.end(); ++it) {
        dfs((representor*)*it);

    }

    return nodes;
}

int bfd(representor* r) {
    static int nodes;
    nodes++;

    return nodes;
}

/* RULES */
int rule_fork(representor* parent, unsigned int pid) {
    representor child;
    child.p = pid;
    child.s = parent->s;
    child.g = parent->g;
    child.children = NULL;
    if(list_child_add(parent, child))
        return -1;
    return 0;
}

void rule_setsid(representor *parent,unsigned int sid) {
    return;
}
void rule_setpgid(representor *parent,unsigned int pgid) {
    return;
}

void exit() {
    return;
}

int abstract_rule(representor *parent,int argc,char** argv) {
    return 0;
}

int main()
{

    return 0;
}