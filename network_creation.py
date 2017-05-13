from mesa import Agent

class PolicyNetworkLinks(Agent):

	def __init__(self, unique_id, agent1, agent2, aware, aware_decay, conflict_level):
		# super().__init__(unique_id, model)

		self.agent1 = agent1
		self.agent2 = agent2
		self.aware = aware
		self.aware_decay = aware_decay
		self.conflict_level = conflict_level
		self.unique_id = unique_id

	# def __str__(self):
	# 	return 'LINK - ' + str(self.unique_id) 

	def __str__(self):
		return 'LINK - ' + str(self.unique_id) + ' with agent1: ' + str(self.agent1) + ', and agent2: ' + str(self.agent2)


	# def __str__(self):
	# 	return 'LINK - ' + str(self.unique_id) + ' with agent1: ' + str(self.agent1) + ', and agent2: ' + str(self.agent2) + ', and aware: ' + str(self.aware)
