class representor:
	def __init__(self, p,g,s,list children):
		self.p=p
		self.g=g
		self.s=s
		self.children=children
		
	def fork(self):
		#to do: add check
		self.children.append(representor(pid, self.g, self.s, []))
		pid = pid + 1
		return (pid - 1)
		
	
