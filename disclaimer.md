#syscall rules list:
[pgs;[c]]

syscall		rule

fork		|***;* --> |\1\2\3;\4 n | n\2\3

setsid		|***;* --> |\1\1\1;\4

setpgid(0)      |***;* --> |\1\1\3;\4

setpgid(g)	|gg*;*, |***;* --> |gg\1;\2,|\3g\5;\6

exit()		|1**;*, |***;* --> |1\1\2;\3\7
		|1**;*, |***;* --> |1\1\2;\3\7,|X\5\6
		
#status: exit is coming soon ...
