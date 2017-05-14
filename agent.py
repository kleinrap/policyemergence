import random
from team_creation import Team
from coalition_creation import Coalition


class Agent:
	
	def __init__(self, unique_id, model):
		self.unique_id = unique_id
		self.model = model

	def step(self):

		pass

	def network_upkeep_as(self, agents, link_list, affiliation_weights, AS_theory):

		"""
		Network update function (agenda setting)
		===========================

		This function is used to perform the maintenance and upkeep actions for the
		networks during the agenda setting. Two strategies are considered for these
		actions.

		Strategy 1 - Largest network strategy:
		For this, the agents focus on maintenaing all links awareness level at a 
		low level while opening new links wherever possible.

		Strategy 2 - Focus network strategy:
		For this, the agents focus on maintenaing the awareness of the links at a
		high level.

		"""

		# print('This is the agent: ' + str(agents))

		if agents.network_strategy == 1:
			# if there are still resources left:
			# First step: Check agents with less than 0.3
			low_link_list = []
			low_link_list_aware = []
			low_link = True
			# Check if there are resources left or if there still low level links
			while agents.resources_network > 0.0001 and low_link == True:
				# print('Agent network resources: ' + str(agents.resources_network))
				for links in link_list:
					# finding all links related to this agent and with aware higher than 0 and lower than 0.3
					if (links.agent1 == agents or links.agent2 == agents) and links.aware > 0 and links.aware < 0.3:
						# print('Links list: ' + str(links) + ' with their aware: ' + str(links.aware))
						low_link_list.append(links)
						low_link_list_aware.append(links.aware)
				# Make sure that the list is not 0
				if len(low_link_list) > 0:
					# print('Trust list: ' + str(low_link_list_aware))
					index_min_aware = low_link_list_aware.index(min(low_link_list_aware))
					# print('Chosen index: ' + str(index_min_aware))
					# print(low_link_list[index_min_aware].aware)
					# print('The link upgrade is link: ' + str(low_link_list[index_min_aware]) + ' with aware: ' + str(low_link_list[index_min_aware].aware))
					# Calculating the change in aware depending on resources and affiliation weight
					# Same affiliation
					if links.agent1.affiliation == links.agent2.affiliation:
						low_link_list[index_min_aware].aware += 0.04*agents.resources[0]
					# Affiliation 1 and 2
					if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
				      (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
						low_link_list[index_min_aware].aware += 0.04*agents.resources[0]*affiliation_weights[0]
					# Affiliation 1 and 3
					if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
					  (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
						low_link_list[index_min_aware].aware += 0.04*agents.resources[0]*affiliation_weights[1]
					# Affiliation 2 and 3
					if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
					  (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
						low_link_list[index_min_aware].aware += 0.04*agents.resources[0]*affiliation_weights[2]
					agents.resources_network -= 0.04*agents.resources[0]
					# print('        ')
					# print('        ')
					low_link_list = []
					low_link_list_aware = []
				# if it is, stop the loop
				else:
					# print('Loop stops now because there is no more low aware.')
					low_link = False
			# 
			# Second step: Make new links:
			new_link_list = []
			new_link = True
			while agents.resources_network > 0.0001 and new_link == True:
				# The list is shuffled such that it is not always the links with the smallest ID that are selected:
				shuffled_list_links = link_list
				random.shuffle(shuffled_list_links)
				for links in shuffled_list_links:
					if (links.agent1 == agents or links.agent2 == agents) and links.aware == 0:
						new_link_list.append(links)
				if len(new_link_list) > 0:
					# Same affiliation
					if links.agent1.affiliation == links.agent2.affiliation:
						random.choice(new_link_list).aware += 0.04*agents.resources[0]
					# Affiliation 1 and 2
					if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
				      (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
						random.choice(new_link_list).aware += 0.04*agents.resources[0]*affiliation_weights[0]
					# Affiliation 1 and 3
					if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
					  (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
						random.choice(new_link_list).aware += 0.04*agents.resources[0]*affiliation_weights[1]
					# Affiliation 2 and 3
					if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
					  (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
						random.choice(new_link_list).aware += 0.04*agents.resources[0]*affiliation_weights[2]
					agents.resources_network -= 0.04*agents.resources[0]
					new_link_list = []
				else:
						# print('Loop stops now because there is no more 0 aware links.')
					new_link = False

			# Third step: Raise aware of remaining links:
			normal_link_list = []
			normal_link = True
			while agents.resources_network > 0.0001 and normal_link == True:
				for links in link_list:
					if (links.agent1 == agents or links.agent2 == agents) and links.aware <= 1 and links.aware != -1:
						normal_link_list.append(links)
				if len(normal_link_list) > 0:
					normal_link_to_change = random.choice(normal_link_list)
					if links.agent1.affiliation == links.agent2.affiliation:
						normal_link_to_change.aware += 0.04*agents.resources[0]
					# Affiliation 1 and 2
					if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
				      (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
						normal_link_to_change.aware += 0.04*agents.resources[0]*affiliation_weights[0]
					# Affiliation 1 and 3
					if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
					  (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
						normal_link_to_change.aware += 0.04*agents.resources[0]*affiliation_weights[1]
					# Affiliation 2 and 3
					if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
					  (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
						normal_link_to_change.aware += 0.04*agents.resources[0]*affiliation_weights[2]
					# Make sure that no link will have a aware level higher than 1
					if normal_link_to_change.aware > 1:
						normal_link_to_change.aware = 1
					agents.resources_network -= 0.04*agents.resources[0]
					normal_link_list = []
				else:
					# print('All loops are their highest level.')
					new_link = False
	
		if agents.network_strategy  == 2:

			# First step: Check agents with more than 0.7 and similar beliefs
			high_link_list = []
			high_link_list_aware = []
			high_link = True
			# Check if there are resources left or if there still high level links
			while agents.resources_network > 0.0001 and high_link == True:
				for links in link_list:
					# finding all links related to this agent and with lower than than 0.7 and with similar belief:
					# similar belief is defined as if one of the two agents has their selected problem with 0.2 of the other.
					if AS_theory != 2:
						if (links.agent1 == agents or links.agent2 == agents) and links.aware > 0.7 and links.aware <= 1 and \
						(abs(links.agent1.belieftree[0][links.agent1.select_as_issue][1] - links.agent1.belieftree[0][links.agent2.select_as_issue][1]) < 0.2 or 
						  abs(links.agent2.belieftree[0][links.agent1.select_as_issue][1] - links.agent2.belieftree[0][links.agent2.select_as_issue][1]) < 0.2):
							high_link_list.append(links)
							high_link_list_aware.append(links.aware)	
					if AS_theory == 2:			
						if (links.agent1 == agents or links.agent2 == agents) and links.aware > 0.7 and links.aware <= 1 and \
						(abs(links.agent1.belieftree[0][links.agent1.select_problem_3S_as][1] - links.agent1.belieftree[0][links.agent2.select_problem_3S_as][1]) < 0.2 or 
						  abs(links.agent2.belieftree[0][links.agent1.select_problem_3S_as][1] - links.agent2.belieftree[0][links.agent2.select_problem_3S_as][1]) < 0.2):
							high_link_list.append(links)
							high_link_list_aware.append(links.aware)
				# Make sure that the list is not 0
				if len(high_link_list) > 0:
					index_min_aware = high_link_list_aware.index(min(high_link_list_aware))
					# Calculating the change in aware depending on resources and affiliation weight
					# Same affiliation
					if links.agent1.affiliation == links.agent2.affiliation:
						# print('Same affiliation')
						high_link_list[index_min_aware].aware += 0.04*agents.resources[0]
					# Affiliation 1 and 2
					if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
					  (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
						# print('Affiliation 1 and 2')
						high_link_list[index_min_aware].aware += 0.04*agents.resources[0]*affiliation_weights[0]
					# Affiliation 1 and 3
					if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
					  (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
					# print(' Affiliation 1 and 3')
						high_link_list[index_min_aware].aware += 0.04*agents.resources[0]*affiliation_weights[1]
						# Affiliation 2 and 3
					if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
					  (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
						# print('Affiliation 2 and 3')
						high_link_list[index_min_aware].aware += 0.04*agents.resources[0]*affiliation_weights[2]
					# Check that it is smaller than 1
					if high_link_list[index_min_aware].aware > 1:
						high_link_list[index_min_aware].aware = 1
					agents.resources_network -= 0.04*agents.resources[0]
					# print(high_link_list[index_min_aware].aware)
					high_link_list = []
					high_link_list_aware = []
				# if it is, stop the loop
				else:
					# print('Loop stops now because there is no more low aware.')
					high_link = False

			# Second step: Check agents with that are 0 and similar beliefs
			new_link_list = []
			new_link = True
			# Check if there are resources left or if there still high level links
			while agents.resources_network > 0.0001 and new_link == True:
				# print('Agent network resources: ' + str(agents.resources_network))
				shuffled_list_links = link_list
				random.shuffle(shuffled_list_links)
				for links in shuffled_list_links:
					# finding all links related to this agent and with aware of 0 and with similar belief:
					# similar belief is defined as if one of the two agents has their selected problem with 0.2 of the other.
					if AS_theory != 2:
						if (links.agent1 == agents or links.agent2 == agents) and links.aware == 0 and \
						(abs(links.agent1.belieftree[0][links.agent1.select_as_issue][1] - links.agent1.belieftree[0][links.agent2.select_as_issue][1]) < 0.2 or 
						  abs(links.agent2.belieftree[0][links.agent1.select_as_issue][1] - links.agent2.belieftree[0][links.agent2.select_as_issue][1]) < 0.2):
							# print(str(links) + ' with their aware: ' + str(links.aware))
							new_link_list.append(links)
					if AS_theory == 2:
						if (links.agent1 == agents or links.agent2 == agents) and links.aware == 0 and \
						(abs(links.agent1.belieftree[0][links.agent1.select_problem_3S_as][1] - links.agent1.belieftree[0][links.agent2.select_problem_3S_as][1]) < 0.2 or 
						  abs(links.agent2.belieftree[0][links.agent1.select_problem_3S_as][1] - links.agent2.belieftree[0][links.agent2.select_problem_3S_as][1]) < 0.2):
							# print(str(links) + ' with their aware: ' + str(links.aware))
							new_link_list.append(links)
						
				# Make sure that the list is not 0
				if len(new_link_list) > 0:
					# Calculating the change in aware depending on resources and affiliation weight
					# Same affiliation
					if links.agent1.affiliation == links.agent2.affiliation:
						# print('Same affiliation')
						random.choice(new_link_list).aware += 0.04*agents.resources[0]
					# Affiliation 1 and 2
					if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
					  (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
						# print('Affiliation 1 and 2')
						random.choice(new_link_list).aware += 0.04*agents.resources[0]*affiliation_weights[0]
					# Affiliation 1 and 3
					if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
					  (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
						# print(' Affiliation 1 and 3')
						random.choice(new_link_list).aware += 0.04*agents.resources[0]*affiliation_weights[1]
					# Affiliation 2 and 3
					if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
					  (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
						# print('Affiliation 2 and 3')
						random.choice(new_link_list).aware += 0.04*agents.resources[0]*affiliation_weights[2]
					agents.resources_network -= 0.04*agents.resources[0]
					new_link_list = []
				# if it is, stop the loop
				else:
					# print('Loop stops now because there is no more low aware.')
					new_link = False
				
			# Third step: Raise agents with low aware
			medium_link_list = []
			medium_link_list_aware = []
			medium_link = True
			# Check if there are resources left or if there still high level links
			while agents.resources_network > 0.0001 and medium_link == True:
				# print('Agent network resources: ' + str(agents.resources_network))
				for links in link_list:
					# finding all links related to this agent and with lower than than 0.7 and with similar belief:
					# similar belief is defined as if one of the two agents has their selected problem with 0.2 of the other.
					if (links.agent1 == agents or links.agent2 == agents) and links.aware < 0.7 and links.aware > 0:
						# print(str(links) + ' with their aware: ' + str(links.aware))
						medium_link_list.append(links)
						medium_link_list_aware.append(links.aware)
				# print(medium_link_list)
						
				# Make sure that the list is not 0
				if len(medium_link_list) > 0:
					index_min_aware = medium_link_list_aware.index(min(medium_link_list_aware))
					# Calculating the change in aware depending on resources and affiliation weight
					# Same affiliation
					if links.agent1.affiliation == links.agent2.affiliation:
						# print('Same affiliation')
						medium_link_list[index_min_aware].aware += 0.04*agents.resources[0]
					# Affiliation 1 and 2
					if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
					  (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
						# print('Affiliation 1 and 2')
						medium_link_list[index_min_aware].aware += 0.04*agents.resources[0]*affiliation_weights[0]
					# Affiliation 1 and 3
					if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
					  (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
						# print(' Affiliation 1 and 3')
						medium_link_list[index_min_aware].aware += 0.04*agents.resources[0]*affiliation_weights[1]
					# Affiliation 2 and 3
					if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
					  (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
						# print('Affiliation 2 and 3')
						medium_link_list[index_min_aware].aware += 0.04*agents.resources[0]*affiliation_weights[2]
					agents.resources_network -= 0.04*agents.resources[0]
					# print('Tadah! ' + str(medium_link_list[index_min_aware].aware))
					medium_link_list = []
					medium_link_list_aware = []
				# if it is, stop the loop
				else:
					# print('Loop stops now because there is no more low aware.')
					medium_link = False

			# Fourth step: Check agents with that are 0 and similar beliefs
			new2_link_list = []
			new2_link = True
			# Check if there are resources left or if there still high level links
			while agents.resources_network > 0.0001 and new2_link == True:
				# print('Agent network resources: ' + str(agents.resources_network))
				shuffled_list_links = link_list
				random.shuffle(shuffled_list_links)
				for links in shuffled_list_links:
					# finding all links related to this agent and with aware of 0:
					# similar belief is defined as if one of the two agents has their selected problem with 0.2 of the other.
					if (links.agent1 == agents or links.agent2 == agents) and links.aware == 0:
						# print(str(links) + ' with their aware: ' + str(links.aware))
						new2_link_list.append(links)
						
				# Make sure that the list is not 0
				if len(new2_link_list) > 0:
					# Calculating the change in aware depending on resources and affiliation weight
					# Same affiliation
					if links.agent1.affiliation == links.agent2.affiliation:
						# print('Same affiliation')
						random.choice(new2_link_list).aware += 0.04*agents.resources[0]
					# Affiliation 1 and 2
					if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
					  (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
						# print('Affiliation 1 and 2')
						random.choice(new2_link_list).aware += 0.04*agents.resources[0]*affiliation_weights[0]
					# Affiliation 1 and 3
					if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
					  (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
						# print(' Affiliation 1 and 3')
						random.choice(new2_link_list).aware += 0.04*agents.resources[0]*affiliation_weights[1]
					# Affiliation 2 and 3
					if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
					  (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
						# print('Affiliation 2 and 3')
						random.choice(new2_link_list).aware += 0.04*agents.resources[0]*affiliation_weights[2]
					agents.resources_network -= 0.04*agents.resources[0]
					new2_link_list = []
				# if it is, stop the loop
				else:
					# print('Loop stops now because there is no more low aware.')
					new2_link = False

	def network_upkeep_pf(self, agents, link_list, affiliation_weights, agenda_as_issue, agenda_prob_3S_as, PF_theory):

		"""
		Network update function (policy formulation)
		===========================

		Note: This is the same function as the one for the agenda setting function
		but with modification for the policy formulation part. This means changes in
		the selection of the selected issues.

		This function is used to perform the maintenance and upkeep actions for the
		networks during the policy formulation. Two strategies are considered for
		these actions.

		Strategy 1 - Largest network strategy:
		For this, the agents focus on maintenaing all links awareness level at a 
		low level while opening new links wherever possible.

		Strategy 2 - Focus network strategy:
		For this, the agents focus on maintenaing the awareness of the links at a
		high level.

		"""

		# print('This is the agent: ' + str(agents))

		if agents.network_strategy  == 1:
			# if there are still resources left:
			# First step: Check agents with less than 0.3
			low_link_list = []
			low_link_list_aware = []
			low_link = True
			# Check if there are resources left or if there still low level links
			while agents.resources_network > 0.0001 and low_link == True:
				# print('Agent network resources: ' + str(agents.resources_network))
				for links in link_list:
					# finding all links related to this agent and with aware higher than 0 and lower than 0.3
					if (links.agent1 == agents or links.agent2 == agents) and links.aware > 0 and links.aware < 0.3:
						# print('Links list: ' + str(links) + ' with their aware: ' + str(links.aware))
						low_link_list.append(links)
						low_link_list_aware.append(links.aware)
				# Make sure that the list is not 0
				if len(low_link_list) > 0:
					# print('Trust list: ' + str(low_link_list_aware))
					index_min_aware = low_link_list_aware.index(min(low_link_list_aware))
					# print('Chosen index: ' + str(index_min_aware))
					# print(low_link_list[index_min_aware].aware)
					# print('The link upgrade is link: ' + str(low_link_list[index_min_aware]) + ' with aware: ' + str(low_link_list[index_min_aware].aware))
					# Calculating the change in aware depending on resources and affiliation weight
					# Same affiliation
					if links.agent1.affiliation == links.agent2.affiliation:
						low_link_list[index_min_aware].aware += 0.04*agents.resources[0]
					# Affiliation 1 and 2
					if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
				      (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
						low_link_list[index_min_aware].aware += 0.04*agents.resources[0]*affiliation_weights[0]
					# Affiliation 1 and 3
					if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
					  (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
						low_link_list[index_min_aware].aware += 0.04*agents.resources[0]*affiliation_weights[1]
					# Affiliation 2 and 3
					if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
					  (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
						low_link_list[index_min_aware].aware += 0.04*agents.resources[0]*affiliation_weights[2]
					agents.resources_network -= 0.04*agents.resources[0]
					# print('        ')
					# print('        ')
					low_link_list = []
					low_link_list_aware = []
				# if it is, stop the loop
				else:
					# print('Loop stops now because there is no more low aware.')
					low_link = False
			# 
			# Second step: Make new links:
			new_link_list = []
			new_link = True
			while agents.resources_network > 0.0001 and new_link == True:
				# The list is shuffled such that it is not always the links with the smallest ID that are selected:
				shuffled_list_links = link_list
				random.shuffle(shuffled_list_links)
				for links in shuffled_list_links:
					if (links.agent1 == agents or links.agent2 == agents) and links.aware == 0:
						new_link_list.append(links)
				if len(new_link_list) > 0:
					# Same affiliation
					if links.agent1.affiliation == links.agent2.affiliation:
						random.choice(new_link_list).aware += 0.04*agents.resources[0]
					# Affiliation 1 and 2
					if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
				      (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
						random.choice(new_link_list).aware += 0.04*agents.resources[0]*affiliation_weights[0]
					# Affiliation 1 and 3
					if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
					  (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
						random.choice(new_link_list).aware += 0.04*agents.resources[0]*affiliation_weights[1]
					# Affiliation 2 and 3
					if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
					  (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
						random.choice(new_link_list).aware += 0.04*agents.resources[0]*affiliation_weights[2]
					agents.resources_network -= 0.04*agents.resources[0]
					new_link_list = []
				else:
						# print('Loop stops now because there is no more 0 aware links.')
					new_link = False

			# Third step: Raise aware of remaining links:
			normal_link_list = []
			normal_link = True
			while agents.resources_network > 0.0001 and normal_link == True:
				for links in link_list:
					if (links.agent1 == agents or links.agent2 == agents) and links.aware <= 1 and links.aware != -1:
						normal_link_list.append(links)
				if len(normal_link_list) > 0:
					normal_link_to_change = random.choice(normal_link_list)
					if links.agent1.affiliation == links.agent2.affiliation:
						normal_link_to_change.aware += 0.04*agents.resources[0]
					# Affiliation 1 and 2
					if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
				      (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
						normal_link_to_change.aware += 0.04*agents.resources[0]*affiliation_weights[0]
					# Affiliation 1 and 3
					if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
					  (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
						normal_link_to_change.aware += 0.04*agents.resources[0]*affiliation_weights[1]
					# Affiliation 2 and 3
					if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
					  (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
						normal_link_to_change.aware += 0.04*agents.resources[0]*affiliation_weights[2]
					# Make sure that no link will have a aware level higher than 1
					if normal_link_to_change.aware > 1:
						normal_link_to_change.aware = 1
					agents.resources_network -= 0.04*agents.resources[0]
					normal_link_list = []
				else:
					# print('All loops are their highest level.')
					new_link = False
	
		if agents.network_strategy  == 2:

			if PF_theory != 2:
				same_belief_issue = agenda_as_issue

			if PF_theory == 2:
				same_belief_issue = agenda_prob_3S_as

			# First step: Check agents with more than 0.7 and similar beliefs
			high_link_list = []
			high_link_list_aware = []
			high_link = True
			# Check if there are resources left or if there still high level links
			while agents.resources_network > 0.0001 and high_link == True:
				for links in link_list:
					# finding all links related to this agent and with lower than than 0.7 and with similar belief:
					# similar belief is defined as if one of the two agents has their selected problem with 0.2 of the other.
					if (links.agent1 == agents or links.agent2 == agents) and links.aware > 0.7 and links.aware <= 1 and \
					(abs(links.agent1.belieftree[0][same_belief_issue][1] - links.agent1.belieftree[0][same_belief_issue][1]) < 0.2 or 
					  abs(links.agent2.belieftree[0][same_belief_issue][1] - links.agent2.belieftree[0][same_belief_issue][1]) < 0.2):
						high_link_list.append(links)
						high_link_list_aware.append(links.aware)					
				# Make sure that the list is not 0
				if len(high_link_list) > 0:
					index_min_aware = high_link_list_aware.index(min(high_link_list_aware))
					# Calculating the change in aware depending on resources and affiliation weight
					# Same affiliation
					if links.agent1.affiliation == links.agent2.affiliation:
						# print('Same affiliation')
						high_link_list[index_min_aware].aware += 0.04*agents.resources[0]
					# Affiliation 1 and 2
					if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
					  (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
						# print('Affiliation 1 and 2')
						high_link_list[index_min_aware].aware += 0.04*agents.resources[0]*affiliation_weights[0]
					# Affiliation 1 and 3
					if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
					  (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
					# print(' Affiliation 1 and 3')
						high_link_list[index_min_aware].aware += 0.04*agents.resources[0]*affiliation_weights[1]
						# Affiliation 2 and 3
					if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
					  (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
						# print('Affiliation 2 and 3')
						high_link_list[index_min_aware].aware += 0.04*agents.resources[0]*affiliation_weights[2]
					# Check that it is smaller than 1
					if high_link_list[index_min_aware].aware > 1:
						high_link_list[index_min_aware].aware = 1
					agents.resources_network -= 0.04*agents.resources[0]
					# print(high_link_list[index_min_aware].aware)
					high_link_list = []
					high_link_list_aware = []
				# if it is, stop the loop
				else:
					# print('Loop stops now because there is no more low aware.')
					high_link = False

			# Second step: Check agents with that are 0 and similar beliefs
			new_link_list = []
			new_link = True
			# Check if there are resources left or if there still high level links
			while agents.resources_network > 0.0001 and new_link == True:
				# print('Agent network resources: ' + str(agents.resources_network))
				shuffled_list_links = link_list
				random.shuffle(shuffled_list_links)
				for links in shuffled_list_links:
					# finding all links related to this agent and with aware of 0 and with similar belief:
					# similar belief is defined as if one of the two agents has their selected problem with 0.2 of the other.
					if (links.agent1 == agents or links.agent2 == agents) and links.aware == 0 and \
					(abs(links.agent1.belieftree[0][same_belief_issue][1] - links.agent1.belieftree[0][same_belief_issue][1]) < 0.2 or 
					  abs(links.agent2.belieftree[0][same_belief_issue][1] - links.agent2.belieftree[0][same_belief_issue][1]) < 0.2):
						# print(str(links) + ' with their aware: ' + str(links.aware))
						new_link_list.append(links)
						
				# Make sure that the list is not 0
				if len(new_link_list) > 0:
					# Calculating the change in aware depending on resources and affiliation weight
					# Same affiliation
					if links.agent1.affiliation == links.agent2.affiliation:
						# print('Same affiliation')
						random.choice(new_link_list).aware += 0.04*agents.resources[0]
					# Affiliation 1 and 2
					if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
					  (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
						# print('Affiliation 1 and 2')
						random.choice(new_link_list).aware += 0.04*agents.resources[0]*affiliation_weights[0]
					# Affiliation 1 and 3
					if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
					  (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
						# print(' Affiliation 1 and 3')
						random.choice(new_link_list).aware += 0.04*agents.resources[0]*affiliation_weights[1]
					# Affiliation 2 and 3
					if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
					  (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
						# print('Affiliation 2 and 3')
						random.choice(new_link_list).aware += 0.04*agents.resources[0]*affiliation_weights[2]
					agents.resources_network -= 0.04*agents.resources[0]
					new_link_list = []
				# if it is, stop the loop
				else:
					# print('Loop stops now because there is no more low aware.')
					new_link = False
				
			# Third step: Raise agents with low aware
			medium_link_list = []
			medium_link_list_aware = []
			medium_link = True
			# Check if there are resources left or if there still high level links
			while agents.resources_network > 0.0001 and medium_link == True:
				# print('Agent network resources: ' + str(agents.resources_network))
				for links in link_list:
					# finding all links related to this agent and with lower than than 0.7 and with similar belief:
					# similar belief is defined as if one of the two agents has their selected problem with 0.2 of the other.
					if (links.agent1 == agents or links.agent2 == agents) and links.aware < 0.7 and links.aware > 0:
						# print(str(links) + ' with their aware: ' + str(links.aware))
						medium_link_list.append(links)
						medium_link_list_aware.append(links.aware)
				# print(medium_link_list)
						
				# Make sure that the list is not 0
				if len(medium_link_list) > 0:
					index_min_aware = medium_link_list_aware.index(min(medium_link_list_aware))
					# Calculating the change in aware depending on resources and affiliation weight
					# Same affiliation
					if links.agent1.affiliation == links.agent2.affiliation:
						# print('Same affiliation')
						medium_link_list[index_min_aware].aware += 0.04*agents.resources[0]
					# Affiliation 1 and 2
					if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
					  (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
						# print('Affiliation 1 and 2')
						medium_link_list[index_min_aware].aware += 0.04*agents.resources[0]*affiliation_weights[0]
					# Affiliation 1 and 3
					if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
					  (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
						# print(' Affiliation 1 and 3')
						medium_link_list[index_min_aware].aware += 0.04*agents.resources[0]*affiliation_weights[1]
					# Affiliation 2 and 3
					if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
					  (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
						# print('Affiliation 2 and 3')
						medium_link_list[index_min_aware].aware += 0.04*agents.resources[0]*affiliation_weights[2]
					agents.resources_network -= 0.04*agents.resources[0]
					# print('Tadah! ' + str(medium_link_list[index_min_aware].aware))
					medium_link_list = []
					medium_link_list_aware = []
				# if it is, stop the loop
				else:
					# print('Loop stops now because there is no more low aware.')
					medium_link = False

			# Fourth step: Check agents with that are 0 and similar beliefs
			new2_link_list = []
			new2_link = True
			# Check if there are resources left or if there still high level links
			while agents.resources_network > 0.0001 and new2_link == True:
				# print('Agent network resources: ' + str(agents.resources_network))
				shuffled_list_links = link_list
				random.shuffle(shuffled_list_links)
				for links in shuffled_list_links:
					# finding all links related to this agent and with aware of 0:
					# similar belief is defined as if one of the two agents has their selected problem with 0.2 of the other.
					if (links.agent1 == agents or links.agent2 == agents) and links.aware == 0:
						# print(str(links) + ' with their aware: ' + str(links.aware))
						new2_link_list.append(links)
						
				# Make sure that the list is not 0
				if len(new2_link_list) > 0:
					# Calculating the change in aware depending on resources and affiliation weight
					# Same affiliation
					if links.agent1.affiliation == links.agent2.affiliation:
						# print('Same affiliation')
						random.choice(new2_link_list).aware += 0.04*agents.resources[0]
					# Affiliation 1 and 2
					if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
					  (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
						# print('Affiliation 1 and 2')
						random.choice(new2_link_list).aware += 0.04*agents.resources[0]*affiliation_weights[0]
					# Affiliation 1 and 3
					if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
					  (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
						# print(' Affiliation 1 and 3')
						random.choice(new2_link_list).aware += 0.04*agents.resources[0]*affiliation_weights[1]
					# Affiliation 2 and 3
					if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
					  (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
						# print('Affiliation 2 and 3')
						random.choice(new2_link_list).aware += 0.04*agents.resources[0]*affiliation_weights[2]
					agents.resources_network -= 0.04*agents.resources[0]
					new2_link_list = []
				# if it is, stop the loop
				else:
					# print('Loop stops now because there is no more low aware.')
					new2_link = False

	def agent_team_threeS_as(self, agents, agent_action_list, team_list_as, team_list_as_total, link_list, team_number_as, tick_number, threeS_link_list_as, deep_core, \
		policy_core, secondary, team_gap_threshold, team_belief_problem_threshold, team_belief_policy_threshold):

		"""
		Agent-team actions - Three streams (agenda setting)
		===========================

		This function is used to perform all the agent-team actions during the
		agent setting. The actions are given in order as follows:
			a. Belonging level update
			b. Leave team check
			c. Disband team check
			d. Join team
			e. Start team

		The team considered within this step are teams that are only present in
		the agenda setting. The agents also only consider the issues they have
		selected for the agenda setting.

		"""

		len_DC = len(deep_core)
		len_PC = len(policy_core)
		len_S = len(secondary)

		# print(' ')
		# print(agents.select_issue_3S_as)
		# agents.select_issue_3S_as = 'policy'
		# print(agents.select_issue_3S_as)

		# Calculation needed for the choice of the causal relation
		prefered_DC = []
		for deep_core_issues in range(len_DC):
			prefered_DC.append(agents.belieftree[0][deep_core_issues][2])
		prefered_DC = prefered_DC.index(max(prefered_DC))

		# a. Belonging level update (completed)
		if agents.team_as[0] != None:
			self.belonging_level_as(agents, len_DC, len_PC)

		# b. Leave team check (completed)
		if agents.team_as[0] != None:
			# If the belonging level is below 30%, we remove the agent from the team
			if agents.team_as[1] < 0.3:
				# If the agent is the lead agent, then the team is disbanded
				team = agents.team_as[0]
				if agents == agents.team_as[0].lead:
					# Disband function
					self.disband_team_as(agents, team, threeS_link_list_as, team_list_as)

				# Else only this agent is removed
				else:
					self.remove_agent_team_as(agents)
					# If the length of the team becomes too small, then the team has to be disbanded:
					if len(team.members) < 3:
						# Disband function
						self.disband_team_as(agents, team, threeS_link_list_as, team_list_as)

		# c. Disband team check (completed)		
		if agents.team_as[0] != None:
			# Several cases for which a team can be disbanded:
			# 1. Lead agent changes selected problem/policy
			# This is checked every five ticks
			if (tick_number - agents.team_as[0].creation) % 1 == 0 and tick_number >= 5:
				# 1. Lead agent has different issue than the team issue (checked every five ticks)
				# Check that the agent is the lead of this team
				if agents == agents.team_as[0].lead:
					# Check that the agent has different issue type (problem/policy) or different issue number
					if agents.select_problem_3S_as != agents.team_as[0].issue or agents.select_issue_3S_as != agents.team_as[0].issue_type:
						team = agents.team_as[0]
						# Disband function
						self.disband_team_as(agents, team, threeS_link_list_as, team_list_as)

				# 2. Checking if each agent meets the requirements and remove if not
				# Check that the agent has same issue type (problem/policy) and same issue number
				elif agents.select_problem_3S_as == agents.team_as[0].issue and agents.select_issue_3S_as == agents.team_as[0].issue_type:

					# If the team is advocating for a problem, perform the following actions:
					if agents.team_as[0].issue_type == 'problem':
						team = agents.team_as[0]
						agent_removed = 0
						for agent_members in team.members:
							# Opposite of the requirements for the creation of a team

							if abs(team.lead.belieftree[0][len_DC + len_PC + len_S + prefered_DC*len_PC + (agents.team_as[0].issue - len_DC)][0] - \
								agent_members.belieftree[0][len_DC + len_PC + len_S + prefered_DC*len_PC + (agents.team_as[0].issue - len_DC)][0]) >= team_belief_problem_threshold or \
								abs(agent_members.belieftree[0][agents.select_problem_3S_as][0] - agent_members.belieftree[0][agents.select_problem_3S_as][1]) < team_gap_threshold:
								# Disband the team if the leader doesnt meet the requirements anymore
								if agent_members == team.lead:
									self.disband_team_as(agents, team, threeS_link_list_as, team_list_as)
									break
								else:
									self.remove_agent_team_as(agent_members)
									agent_removed = 1
									print('AS - Pr - THIS AGENT HAS TO BE REMOVED: ' + str(agent_members) + ' from ' + str(team))
									if agents == agent_members:
										print('I AM THE AGENT, BREAK AFTER ME')
										break


					# If the team is advocating for a policy, perform the following actions:
					elif agents.team_as[0].issue_type == 'policy':
						team = agents.team_as[0]
						agent_removed = 0
						for agent_members in team.members:
							# Opposite of the requirements for the creation of a team
							if abs(team.lead.belieftree_policy[0][agents.team_as[0].issue][team.lead.select_problem_3S_as - len_DC] - \
								agent_members.belieftree_policy[0][agents.team_as[0].issue][team.lead.select_problem_3S_as - len_DC]) >= team_belief_policy_threshold or \
								abs(agent_members.belieftree[0][team.lead.select_problem_3S_as][0] - agent_members.belieftree[0][team.lead.select_problem_3S_as][1]) < team_gap_threshold:
								# Disband the team if the leader doesnt meet the requirements anymore
								if agent_members == team.lead:

									self.disband_team_as(agents, team, threeS_link_list_as, team_list_as)
									break
								else:
									# Remove the agent if it does not satisfy the requirements anymore
									self.remove_agent_team_as(agent_members)
									agent_removed = 1
									print('AS - Po - THIS AGENT HAS TO BE REMOVED: ' + str(agent_members) + ' from ' + str(team))
									if agents == agent_members:
										print('I AM THE AGENT, BREAK AFTER ME')
										break

					# Recalculate the belonging level of the agents left
					if agents.team_as[0] != None:
						if agent_removed == 1:
							for agent_members in team.members:
								self.belonging_level_as(agent_members, len_DC, len_PC)

								# If the belonging level is below 30%, the agents are removed (similar to a previous loop)
								if agent_members.team_as[1] < 0.3:
									# team = agents.team_as[0]
									if agent_members == agent_members.team_as[0].lead:
										self.disband_team_as(agent_members, team, threeS_link_list_as, team_list_as)
									else:
										self.remove_agent_team_as(agent_members)
										if len(team.members) < 3:
											self.disband_team_as(agent_members, team, threeS_link_list_as, team_list_as)

					# Check the length of the team after all agents have been checked - disband if too small
					if agents.team_as[0] != None:
						if len(team.members) < 3:
							self.disband_team_as(agents, team, threeS_link_list_as, team_list_as)

		# d. Join a team (completed)
		if agents.team_as[0] == None:

			while True:

				added_team_check = 0

				for join_team in team_list_as:

					# If the team is advocating for a problem, the following tasks are completed
					if join_team.issue_type == 'problem':

						# Check that the team is still active and has members:
						if len(join_team.members) > 0:

							# None check
							check_none = 0
							if agents.belieftree[1+join_team.lead.unique_id][len_DC + len_PC + len_S + prefered_DC*len_PC + (join_team.issue - len_DC)][0] == None:
								agents.belieftree[1+join_team.lead.unique_id][len_DC + len_PC + len_S + prefered_DC*len_PC + (join_team.issue - len_DC)][0] = 0
								check_none = 1

							# First we check that the agent meets both requirements (based on partial knowledge) (we assume that the agent knows who the leader is)
							if abs(agents.belieftree[0][join_team.lead.select_problem_3S_as][0] - agents.belieftree[0][join_team.lead.select_problem_3S_as][1]) >= team_gap_threshold and \
								abs(agents.belieftree[0][len_DC + len_PC + len_S + prefered_DC*len_PC + (join_team.issue - len_DC)][0] - \
							  	agents.belieftree[1+join_team.lead.unique_id][len_DC + len_PC + len_S + prefered_DC*len_PC + (join_team.issue - len_DC)][0]) < team_belief_problem_threshold:

								# Add the agent to the team
								join_team.members.append(agents)
								join_team.members_id.append(agents.unique_id)

								agents.team_as[0] = join_team
								# Share knowledge within the team
								# Exchange of partial knowledge between the agents in the team
								self.knowledge_exchange_team(join_team, join_team.issue, 0)

								# Change belonging level
								self.belonging_level_as(agents, len_DC, len_PC)

								# Notify that the loop can be stopped as the agent has been added
								added_team_check = 1

							# None reset
							if check_none == 1:
								agents.belieftree[1+join_team.lead.unique_id][len_DC + len_PC + len_S + prefered_DC*len_PC + (join_team.issue - len_DC)][0] = None

							# update of the resources
							agents.resources[1] -= 0.02 * agents.resources[0]

							# Resources sufficiency check
							if agents.resources[1] < 0.5 * agents.resources[0]:
								break

							# If the agent has been added to a team, stop this entire procedure
							if added_team_check == 1:
								break

					# If the team is advocating for a policy, the following tasks are completed
					elif join_team.issue_type == 'policy':

						# Check that the team is still active and has members:
						if len(join_team.members) > 0:

							# None check
							check_none = 0

							# team.lead.belieftree_policy[0][agents.team_as[0].issue][team.lead.select_problem_3S_as - len_DC]

							if agents.belieftree_policy[1+join_team.lead.unique_id][join_team.issue][join_team.lead.select_problem_3S_as - len_DC] == None:
								agents.belieftree_policy[1+join_team.lead.unique_id][join_team.issue][join_team.lead.select_problem_3S_as - len_DC] = 0
								check_none = 1

							# First we check that the agent meets both requirements (based on partial knowledge) (we assume that the agent knows who the leader is)
							if abs(agents.belieftree[0][join_team.issue][0] - agents.belieftree[0][join_team.issue][1]) >= team_gap_threshold and \
								abs(agents.belieftree_policy[0][join_team.issue][join_team.lead.select_problem_3S_as - len_DC] - \
								agents.belieftree_policy[1+join_team.lead.unique_id][join_team.issue][join_team.lead.select_problem_3S_as - len_DC]) < team_belief_policy_threshold:
								print(' ')
								print('Checked - Join 1!')

								# Add the agent to the team
								join_team.members.append(agents)
								join_team.members_id.append(agents.unique_id)
								agents.team_as[0] = join_team
								# Share knowledge within the team
								# Exchange of partial knowledge between the agents in the team
								self.knowledge_exchange_team(join_team, join_team.issue, 0)

								# Change belonging level
								self.belonging_level_as(agents, len_DC, len_PC)

								# Notify that the loop can be stopped as the agent has been added
								added_team_check = 1

							# None reset
							if check_none == 1:
								agents.belieftree_policy[1+join_team.lead.unique_id][join_team.issue][join_team.lead.select_problem_3S_as - len_DC] = None

							# update of the resources
							agents.resources[1] -= 0.02 * agents.resources[0]

							# Resources sufficiency check
							if agents.resources[1] < 0.5 * agents.resources[0]:
								break

							# If the agent has been added to a team, stop this entire procedure
							if added_team_check == 1:
								break

				break

		# e. Start a team (completed)
		if agents.team_as[0] == None:
			# First team creation method:
			# Avoided for now - requires memory

			# print('agents.select_issue_3S_as: ' + str(agents.select_issue_3S_as))
			# print('agents.team_as[2]: ' + str(agents.team_as[2]))

			# Second team creation method:
			# a. Method 0 - All agents that qualify are selected
			if agents.team_as[2] == 0:
				# print(' ')
				# print(' ')
				# print('Strategy 0')

				# If the agent is advocating or a problem, the following tasks are performed
				if agents.select_issue_3S_as == 'problem':

					# Check if the agent indeed has a gap:
					if abs(agents.belieftree[0][agents.select_problem_3S_as][0] - agents.belieftree[0][agents.select_problem_3S_as][1]) >= team_gap_threshold:

						team_list_potential_agent = []
						shuffled_list_links = link_list
						random.shuffle(shuffled_list_links)
						for links in shuffled_list_links:
							# Make sure that there is aware
							if links.aware > 0:
								# print(links)
								
								# Make sure it is not in a team already and enough resources for the searching agent and that it is known that the other agent's state is not None
								if links.agent1 == agents and links.agent2.team_as[0] == None and agents.resources[1] > 0.02 * agents.resources[0] and agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][0] != 'No':

									# Check if no partial knowledge (initial value)
									if agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][0] == None:
										agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][0] = 0
									if agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][1] == None:
										agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][1] = 0
									if agents.belieftree[1+links.agent2.unique_id][len_DC + len_PC + len_S + prefered_DC*len_PC + (agents.select_problem_3S_as - len_DC)][0] == None:
										agents.belieftree[1+links.agent2.unique_id][len_DC + len_PC + len_S + prefered_DC*len_PC + (agents.select_problem_3S_as - len_DC)][0] = 0

									# Check for the gap and the similarity in states based on partial knowledge - if okay, add the agent to the list
									if abs(agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][0] - agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][1]) >= team_gap_threshold and \
										abs(agents.belieftree[0][len_DC + len_PC + len_S + prefered_DC*len_PC + (agents.select_problem_3S_as - len_DC)][0] - \
									  	agents.belieftree[1+links.agent2.unique_id][len_DC + len_PC + len_S + prefered_DC*len_PC + (agents.select_problem_3S_as - len_DC)][0]) < team_belief_problem_threshold:
										# Add the agent to the list of potential candidates
										team_list_potential_agent.append(links.agent2)

									# Actual knowledge exchange with a randomness of 0.5
									# Knowledge gained by the lead agent:
									agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][0] = links.agent2.belieftree[0][agents.select_problem_3S_as][0] + (random.random()/2) - 0.25
									agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][1] = links.agent2.belieftree[0][agents.select_problem_3S_as][1] + (random.random()/2) - 0.25
									agents.belieftree[1+links.agent2.unique_id][len_DC + len_PC + len_S + prefered_DC*len_PC + (agents.select_problem_3S_as - len_DC)][0] = \
										links.agent2.belieftree[0][len_DC + len_PC + len_S + prefered_DC*len_PC + (agents.select_problem_3S_as - len_DC)][0] + (random.random()/2) - 0.25
									# 1-1 check
									agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][0] = \
										self.one_minus_one_check(agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][0])
									agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][1] = \
										self.one_minus_one_check(agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][1])
									agents.belieftree[1+links.agent2.unique_id][len_DC + len_PC + len_S + prefered_DC*len_PC + (agents.select_problem_3S_as - len_DC)][0] = \
										self.one_minus_one_check(agents.belieftree[1+links.agent2.unique_id][len_DC + len_PC + len_S + prefered_DC*len_PC + (agents.select_problem_3S_as - len_DC)][0])

									# Knowledge gained by the secondary link agent:
									links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_as][0] = agents.belieftree[0][agents.select_problem_3S_as][0] + (random.random()/2) - 0.25
									links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_as][1] = agents.belieftree[0][agents.select_problem_3S_as][1] + (random.random()/2) - 0.25
									links.agent2.belieftree[1+agents.unique_id][len_DC + len_PC + len_S + prefered_DC*len_PC + (agents.select_problem_3S_as - len_DC)][0] = \
										agents.belieftree[0][len_DC + len_PC + len_S + prefered_DC*len_PC + (agents.select_problem_3S_as - len_DC)][0] + (random.random()/2) - 0.25
									# 1-1 check
									links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_as][0] = \
										self.one_minus_one_check(links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_as][0])
									links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_as][1] = \
										self.one_minus_one_check(links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_as][1])
									links.agent2.belieftree[1+agents.unique_id][len_DC + len_PC + len_S + prefered_DC*len_PC + (agents.select_problem_3S_as - len_DC)][0] = \
										self.one_minus_one_check(links.agent2.belieftree[1+agents.unique_id][len_DC + len_PC + len_S + prefered_DC*len_PC + (agents.select_problem_3S_as - len_DC)][0])

									# Adjusting resources
									agents.resources[1] -= 0.02 * agents.resources[0]
									links.agent2.resources[1] -= 0.01 * links.agent2.resources[0]

								# Make sure it is not in a team already and enough resources for the searching agent and that it is known that the other agent's state is not Non
								if links.agent2 == agents and links.agent1.team_as[0] == None and agents.resources[1] > 0.02 * agents.resources[0] and agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][0] != 'No':
										
										# Check if no partial knowledge (initial value)
										if agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][0] == None:
											agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][0] = 0
										if agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][1] == None:
											agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][1] = 0
										if agents.belieftree[1+links.agent1.unique_id][len_DC + len_PC + len_S + prefered_DC*len_PC + (agents.select_problem_3S_as - len_DC)][0] == None:
											agents.belieftree[1+links.agent1.unique_id][len_DC + len_PC + len_S + prefered_DC*len_PC + (agents.select_problem_3S_as - len_DC)][0] = 0

										# Check for the gap and the similarity in states based on partial knowledge
										if abs(agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][0] - agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][1]) >= team_gap_threshold and \
											abs(agents.belieftree[0][len_DC + len_PC + len_S + prefered_DC*len_PC + (agents.select_problem_3S_as - len_DC)][0] - \
										  	agents.belieftree[1+links.agent1.unique_id][len_DC + len_PC + len_S + prefered_DC*len_PC + (agents.select_problem_3S_as - len_DC)][0]) < team_belief_problem_threshold:
											
											# Add the agent to the list of potential candidates
											team_list_potential_agent.append(links.agent1)

										# Actual knowledge exchange with a randomness of 0.5
										# Knowledge gained by the lead agent:
										agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][0] = links.agent1.belieftree[0][agents.select_problem_3S_as][0] + (random.random()/2) - 0.25
										agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][1] = links.agent1.belieftree[0][agents.select_problem_3S_as][1] + (random.random()/2) - 0.25
										agents.belieftree[1+links.agent1.unique_id][len_DC + len_PC + len_S + prefered_DC*len_PC + (agents.select_problem_3S_as - len_DC)][0] = \
											links.agent1.belieftree[0][len_DC + len_PC + len_S + prefered_DC*len_PC + (agents.select_problem_3S_as - len_DC)][0] + (random.random()/2) - 0.25
										# 1-1 check
										agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][0] = \
											self.one_minus_one_check(agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][0])
										agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][1] = \
											self.one_minus_one_check(agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][1])
										agents.belieftree[1+links.agent1.unique_id][len_DC + len_PC + len_S + prefered_DC*len_PC + (agents.select_problem_3S_as - len_DC)][0] = \
											self.one_minus_one_check(agents.belieftree[1+links.agent1.unique_id][len_DC + len_PC + len_S + prefered_DC*len_PC + (agents.select_problem_3S_as - len_DC)][0])

										# Knowledge gained by the secondary link agent:
										links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_as][0] = agents.belieftree[0][agents.select_problem_3S_as][0] + (random.random()/2) - 0.25
										links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_as][1] = agents.belieftree[0][agents.select_problem_3S_as][1] + (random.random()/2) - 0.25
										links.agent1.belieftree[1+agents.unique_id][len_DC + len_PC + len_S + prefered_DC*len_PC + (agents.select_problem_3S_as - len_DC)][0] = \
											agents.belieftree[0][len_DC + len_PC + len_S + prefered_DC*len_PC + (agents.select_problem_3S_as - len_DC)][0] + (random.random()/2) - 0.25
										# 1-1 check
										links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_as][0] = \
											self.one_minus_one_check(links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_as][0])
										links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_as][1] = \
											self.one_minus_one_check(links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_as][1])
										links.agent1.belieftree[1+agents.unique_id][len_DC + len_PC + len_S + prefered_DC*len_PC + (agents.select_problem_3S_as - len_DC)][0] = \
											self.one_minus_one_check(links.agent1.belieftree[1+agents.unique_id][len_DC + len_PC + len_S + prefered_DC*len_PC + (agents.select_problem_3S_as - len_DC)][0])

										# Adjusting resources
										agents.resources[1] -= 0.02 * agents.resources[0]
										links.agent1.resources[1] -= 0.01 * links.agent1.resources[0]

						# If the list has more than 2 agents, then we can check to create a team
						if len(team_list_potential_agent) > 1:
							team_list_actual_agent = []
							# Make a new list containing the agent that actually match the requirements
							for potential_agent in team_list_potential_agent:
								if agents.belieftree[0][agents.select_problem_3S_as][0] != 'No':
									if abs(agents.belieftree[0][len_DC + len_PC + len_S + prefered_DC*len_PC + (agents.select_problem_3S_as - len_DC)][0] - \
										potential_agent.belieftree[0][len_DC + len_PC + len_S + prefered_DC*len_PC + (agents.select_problem_3S_as - len_DC)][0]) < team_belief_problem_threshold and \
										abs(potential_agent.belieftree[0][agents.select_problem_3S_as][0] - potential_agent.belieftree[0][agents.select_problem_3S_as][1]) >= team_gap_threshold:
								  		team_list_actual_agent.append(potential_agent)
								else:
									print('1. ALERT - THIS IS AN INTRUDER - A AGENT THAT SHOULDNT BE IN THIS TEAM IS IN THIS TEAM')

							# Check that the list is still more than two agents and if so create the team:
							if len(team_list_potential_agent) > 1:

								# Now we can create the team						
								members = team_list_potential_agent
								members.append(agents)
								team_resources = [0, 0]
								members_id = []
								for members_for_id in members:
									members_id.append(members_for_id.unique_id)
								team = Team(team_number_as[0], agents, members, members_id, agents.select_issue_3S_as, agents.select_problem_3S_as, tick_number, team_resources)
								print('TEAM CREATION 1! ')
								# Iteration of the team ID number for the overall team list
								team_number_as[0] += 1
								team_list_as.append(team)
								team_list_as_total.append(team)
								
								# Exchange of partial knowledge between the agents in the team
								self.knowledge_exchange_team(team, team.issue, 0)

								# Calculation of the average issue belief for belonging calculation (based on partial knowledge) per agent:
								for agent_members1 in team.members:
									# Setting the partial knowledge for himself equal to his own belief:
									agent_members1.belieftree[1+agent_members1.unique_id][team.issue][0] = agent_members1.belieftree[0][team.issue][0]
									# Calculating the average belief according to partial knowledge
									issue_avg_belief = []
									for agent_members2 in team.members:
										if agent_members1.belieftree[1+agent_members2.unique_id][team.issue][0] != 'No':
											issue_avg_belief.append(agent_members2.resources[0]*agent_members1.belieftree[1+agent_members2.unique_id][team.issue][0])
										else:
											print('2. ALERT - THIS IS AN INTRUDER - A AGENT THAT SHOULDNT BE IN THIS TEAM IS IN THIS TEAM')
									issue_avg_belief = sum(issue_avg_belief)/len(issue_avg_belief)
									# Setting the belonging level
									agent_members1.team_as[1] = 1 - abs(agent_members1.belieftree[0][team.issue][0] - issue_avg_belief)
									# Setting of the team object
									agent_members1.team_as[0] = team
								# Setting the team resources
								for agent_members in team.members:
									team.resources[0] += agent_members.team_as[1]
									team.resources[1] = team.resources[0]

				# If the agent is advocating or a policy, the following tasks are performed
				if agents.select_issue_3S_as == 'policy':

					# Check if the agent indeed has a gap:
					if abs(agents.belieftree[0][agents.select_problem_3S_as][0] - agents.belieftree[0][agents.select_problem_3S_as][1]) >= team_gap_threshold:

						team_list_potential_agent = []
						shuffled_list_links = link_list
						random.shuffle(shuffled_list_links)
						for links in shuffled_list_links:
							# Make sure that there is aware
							if links.aware > 0:
								# print(links)
								
								# Make sure it is not in a team already and enough resources for the searching agent and that it is known that the other agent's state is not None
								if links.agent1 == agents and links.agent2.team_as[0] == None and agents.resources[1] > 0.02 * agents.resources[0] and agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][0] != 'No':

									# Check if no partial knowledge (initial value)
									if agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][0] == None:
										agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][0] = 0
									if agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][1] == None:
										agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][1] = 0
									if agents.belieftree_policy[1+links.agent2.unique_id][agents.select_policy_3S_as][agents.select_problem_3S_as - len_DC] == None:
										agents.belieftree_policy[1+links.agent2.unique_id][agents.select_policy_3S_as][agents.select_problem_3S_as - len_DC] = 0

									# Check for the gap and the similarity in states based on partial knowledge - if okay, add the agent to the list
									if abs(agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][0] - agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][1]) >= team_gap_threshold and \
										abs(agents.belieftree_policy[0][agents.select_policy_3S_as][agents.select_problem_3S_as - len_DC] - \
									  	agents.belieftree_policy[1+links.agent2.unique_id][agents.select_policy_3S_as][agents.select_problem_3S_as - len_DC]) < team_belief_policy_threshold:
										# Add the agent to the list of potential candidates
										team_list_potential_agent.append(links.agent2)

									# Actual knowledge exchange with a randomness of 0.5
									# Knowledge gained by the lead agent:
									agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][0] = links.agent2.belieftree[0][agents.select_problem_3S_as][0] + (random.random()/2) - 0.25
									agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][1] = links.agent2.belieftree[0][agents.select_problem_3S_as][1] + (random.random()/2) - 0.25
									agents.belieftree_policy[1+links.agent2.unique_id][agents.select_policy_3S_as][agents.select_problem_3S_as - len_DC] = \
										links.agent2.belieftree_policy[0][agents.select_policy_3S_as][agents.select_problem_3S_as - len_DC] + (random.random()/2) - 0.25
									# 1-1 check
									agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][0] = \
										self.one_minus_one_check(agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][0])
									agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][1] = \
										self.one_minus_one_check(agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][1])
									agents.belieftree_policy[1+links.agent2.unique_id][agents.select_policy_3S_as][agents.select_problem_3S_as - len_DC] = \
										self.one_minus_one_check(agents.belieftree_policy[1+links.agent2.unique_id][agents.select_policy_3S_as][agents.select_problem_3S_as - len_DC])

									# Knowledge gained by the secondary link agent:
									links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_as][0] = agents.belieftree[0][agents.select_problem_3S_as][0] + (random.random()/2) - 0.25
									links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_as][1] = agents.belieftree[0][agents.select_problem_3S_as][1] + (random.random()/2) - 0.25
									links.agent2.belieftree_policy[1+agents.unique_id][agents.select_policy_3S_as][agents.select_problem_3S_as - len_DC] = \
										agents.belieftree_policy[0][agents.select_policy_3S_as][agents.select_problem_3S_as - len_DC] + (random.random()/2) - 0.25
									# 1-1 check
									links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_as][0] = \
										self.one_minus_one_check(links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_as][0])
									links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_as][1] = \
										self.one_minus_one_check(links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_as][1])
									links.agent2.belieftree_policy[1+agents.unique_id][agents.select_policy_3S_as][agents.select_problem_3S_as - len_DC] = \
										self.one_minus_one_check(links.agent2.belieftree_policy[1+agents.unique_id][agents.select_policy_3S_as][agents.select_problem_3S_as - len_DC])

									# Adjusting resources
									agents.resources[1] -= 0.02 * agents.resources[0]
									links.agent2.resources[1] -= 0.01 * links.agent2.resources[0]

								# Make sure it is not in a team already and enough resources for the searching agent and that it is known that the other agent's state is not Non
								if links.agent2 == agents and links.agent1.team_as[0] == None and agents.resources[1] > 0.02 * agents.resources[0] and agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][0] != 'No':

									# Check if no partial knowledge (initial value)
									if agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][0] == None:
										agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][0] = 0
									if agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][1] == None:
										agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][1] = 0
									if agents.belieftree_policy[1+links.agent1.unique_id][agents.select_policy_3S_as][agents.select_problem_3S_as - len_DC] == None:
										agents.belieftree_policy[1+links.agent1.unique_id][agents.select_policy_3S_as][agents.select_problem_3S_as - len_DC] = 0

									# Check for the gap and the similarity in states based on partial knowledge
									if abs(agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][0] - agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][1]) >= team_gap_threshold and \
										abs(agents.belieftree_policy[0][agents.select_policy_3S_as][agents.select_problem_3S_as - len_DC] - \
									  	agents.belieftree_policy[1+links.agent1.unique_id][agents.select_policy_3S_as][agents.select_problem_3S_as - len_DC]) < team_belief_policy_threshold:
										
										# Add the agent to the list of potential candidates
										team_list_potential_agent.append(links.agent1)

									# Actual knowledge exchange with a randomness of 0.5
									# Knowledge gained by the lead agent:
									agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][0] = links.agent1.belieftree[0][agents.select_problem_3S_as][0] + (random.random()/2) - 0.25
									agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][1] = links.agent1.belieftree[0][agents.select_problem_3S_as][1] + (random.random()/2) - 0.25
									agents.belieftree_policy[1+links.agent1.unique_id][agents.select_policy_3S_as][agents.select_problem_3S_as - len_DC] = \
										links.agent1.belieftree_policy[0][agents.select_policy_3S_as][agents.select_problem_3S_as - len_DC] + (random.random()/2) - 0.25
									# 1-1 check
									agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][0] = \
										self.one_minus_one_check(agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][0])
									agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][1] = \
										self.one_minus_one_check(agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][1])
									agents.belieftree_policy[1+links.agent1.unique_id][agents.select_policy_3S_as][agents.select_problem_3S_as - len_DC] = \
										self.one_minus_one_check(agents.belieftree_policy[1+links.agent1.unique_id][agents.select_policy_3S_as][agents.select_problem_3S_as - len_DC])

									# Knowledge gained by the secondary link agent:
									links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_as][0] = agents.belieftree[0][agents.select_problem_3S_as][0] + (random.random()/2) - 0.25
									links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_as][1] = agents.belieftree[0][agents.select_problem_3S_as][1] + (random.random()/2) - 0.25
									links.agent1.belieftree_policy[1+agents.unique_id][agents.select_policy_3S_as][agents.select_problem_3S_as - len_DC] = \
										agents.belieftree_policy[0][agents.select_policy_3S_as][agents.select_problem_3S_as - len_DC] + (random.random()/2) - 0.25
									# 1-1 check
									links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_as][0] = \
										self.one_minus_one_check(links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_as][0])
									links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_as][1] = \
										self.one_minus_one_check(links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_as][1])
									links.agent1.belieftree_policy[1+agents.unique_id][agents.select_policy_3S_as][agents.select_problem_3S_as - len_DC] = \
										self.one_minus_one_check(links.agent1.belieftree_policy[1+agents.unique_id][agents.select_policy_3S_as][agents.select_problem_3S_as - len_DC])

									# Adjusting resources
									agents.resources[1] -= 0.02 * agents.resources[0]
									links.agent1.resources[1] -= 0.01 * links.agent1.resources[0]

						# If the list has more than 2 agents, then we can check to create a team
						if len(team_list_potential_agent) > 1:
							team_list_actual_agent = []
							# Make a new list containing the agent that actually match the requirements
							for potential_agent in team_list_potential_agent:
								if agents.belieftree[0][agents.select_problem_3S_as][0] != 'No':
									if abs(agents.belieftree_policy[0][agents.select_policy_3S_as][agents.select_problem_3S_as - len_DC] - \
										potential_agent.belieftree_policy[0][agents.select_policy_3S_as][agents.select_problem_3S_as - len_DC]) < team_belief_policy_threshold and \
										abs(potential_agent.belieftree[0][agents.select_problem_3S_as][0] - potential_agent.belieftree[0][agents.select_problem_3S_as][1]) >= team_gap_threshold:
								  		team_list_actual_agent.append(potential_agent)
								else:
									print('1. ALERT - THIS IS AN INTRUDER - A AGENT THAT SHOULDNT BE IN THIS TEAM IS IN THIS TEAM')

							# Check that the list is still more than two agents and if so create the team:
							if len(team_list_potential_agent) > 1:

								# Now we can create the team						
								members = team_list_potential_agent
								members.append(agents)
								team_resources = [0, 0]
								members_id = []
								for members_for_id in members:
									members_id.append(members_for_id.unique_id)
								team = Team(team_number_as[0], agents, members, members_id, agents.select_issue_3S_as, agents.select_policy_3S_as, tick_number, team_resources)
								print('TEAM CREATION 2! ')
								# Iteration of the team ID number for the overall team list
								team_number_as[0] += 1
								team_list_as.append(team)
								team_list_as_total.append(team)
								
								# Exchange of partial knowledge between the agents in the team
								self.knowledge_exchange_team(team, team.issue, 0)

								# Calculation of the average issue belief for belonging calculation (based on partial knowledge) per agent:
								for agent_members1 in team.members:
									# Setting the partial knowledge for himself equal to his own belief:
									agent_members1.belieftree[1+agent_members1.unique_id][team.issue][0] = agent_members1.belieftree[0][team.issue][0]
									# Calculating the average belief according to partial knowledge
									issue_avg_belief = []
									for agent_members2 in team.members:
										if agent_members1.belieftree[1+agent_members2.unique_id][team.issue][0] != 'No':
											issue_avg_belief.append(agent_members2.resources[0]*agent_members1.belieftree[1+agent_members2.unique_id][team.issue][0])
										else:
											print('2. ALERT - THIS IS AN INTRUDER - A AGENT THAT SHOULDNT BE IN THIS TEAM IS IN THIS TEAM')
									issue_avg_belief = sum(issue_avg_belief)/len(issue_avg_belief)
									# Setting the belonging level
									agent_members1.team_as[1] = 1 - abs(agent_members1.belieftree[0][team.issue][0] - issue_avg_belief)
									# Setting of the team object
									agent_members1.team_as[0] = team
								# Setting the team resources
								for agent_members in team.members:
									team.resources[0] += agent_members.team_as[1]
									team.resources[1] = team.resources[0]

			# b. Method 1 - Only the first X agents are selected for the team
			if agents.team_as[2] == 1:
				# print(' ')
				# print(' ')
				# print('Strategy 1')

				# If the agent is advocating or a problem, the following tasks are performed
				if agents.select_issue_3S_as == 'problem':

					# Check if the agent indeed has a gap:
					if abs(agents.belieftree[0][agents.select_problem_3S_as][0] - agents.belieftree[0][agents.select_problem_3S_as][1]) >= team_gap_threshold:

						team_list_potential_agent = []
						
						# Go through all possible links for this agent:
						while True:
							shuffled_list_links = link_list
							random.shuffle(shuffled_list_links)
							for links in shuffled_list_links:

								# Make sure that there is aware
								if links.aware > 0:
									
									# Make sure it is not in a team already and enough resources for the searching agent and that it is known that the other agent's state is not Non
									if links.agent1 == agents and links.agent2.team_as[0] == None and agents.resources[1] > 0.02 * agents.resources[0] and agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][0] != 'No':
										
										# Check if no partial knowledge (initial value)
										if agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][0] == None:
											agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][0] = 0
										if agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][1] == None:
											agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][1] = 0
										if agents.belieftree[1+links.agent2.unique_id][len_DC + len_PC + len_S + prefered_DC*len_PC + (agents.select_problem_3S_as - len_DC)][0] == None:
											agents.belieftree[1+links.agent2.unique_id][len_DC + len_PC + len_S + prefered_DC*len_PC + (agents.select_problem_3S_as - len_DC)][0] = 0

										# Check for the gap and the similarity in states based on partial knowledge - if okay, add the agent to the list
										if abs(agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][0] - agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][1]) >= team_gap_threshold and \
											abs(agents.belieftree[0][len_DC + len_PC + len_S + prefered_DC*len_PC + (agents.select_problem_3S_as - len_DC)][0] - \
										  	agents.belieftree[1+links.agent2.unique_id][len_DC + len_PC + len_S + prefered_DC*len_PC + (agents.select_problem_3S_as - len_DC)][0]) < team_belief_problem_threshold:
											# Add the agent to the list of potential candidates
											team_list_potential_agent.append(links.agent2)

										# Actual knowledge exchange with a randomness of 0.5
										# Knowledge gained by the lead agent:
										agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][0] = links.agent2.belieftree[0][agents.select_problem_3S_as][0] + (random.random()/2) - 0.25
										agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][1] = links.agent2.belieftree[0][agents.select_problem_3S_as][1] + (random.random()/2) - 0.25
										agents.belieftree[1+links.agent2.unique_id][len_DC + len_PC + len_S + prefered_DC*len_PC + (agents.select_problem_3S_as - len_DC)][0] = \
											links.agent2.belieftree[0][len_DC + len_PC + len_S + prefered_DC*len_PC + (agents.select_problem_3S_as - len_DC)][0] + (random.random()/2) - 0.25
										# 1-1 check
										agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][0] = \
											self.one_minus_one_check(agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][0])
										agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][1] = \
											self.one_minus_one_check(agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][1])
										agents.belieftree[1+links.agent2.unique_id][len_DC + len_PC + len_S + prefered_DC*len_PC + (agents.select_problem_3S_as - len_DC)][0] = \
											self.one_minus_one_check(agents.belieftree[1+links.agent2.unique_id][len_DC + len_PC + len_S + prefered_DC*len_PC + (agents.select_problem_3S_as - len_DC)][0])

										# Knowledge gained by the secondary link agent:
										links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_as][0] = agents.belieftree[0][agents.select_problem_3S_as][0] + (random.random()/2) - 0.25
										links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_as][1] = agents.belieftree[0][agents.select_problem_3S_as][1] + (random.random()/2) - 0.25
										links.agent2.belieftree[1+agents.unique_id][len_DC + len_PC + len_S + prefered_DC*len_PC + (agents.select_problem_3S_as - len_DC)][0] = \
											agents.belieftree[0][len_DC + len_PC + len_S + prefered_DC*len_PC + (agents.select_problem_3S_as - len_DC)][0] + (random.random()/2) - 0.25
										# 1-1 check
										links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_as][0] = \
											self.one_minus_one_check(links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_as][0])
										links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_as][1] = \
											self.one_minus_one_check(links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_as][1])
										links.agent2.belieftree[1+agents.unique_id][len_DC + len_PC + len_S + prefered_DC*len_PC + (agents.select_problem_3S_as - len_DC)][0] = \
											self.one_minus_one_check(links.agent2.belieftree[1+agents.unique_id][len_DC + len_PC + len_S + prefered_DC*len_PC + (agents.select_problem_3S_as - len_DC)][0])

										# Adjusting resources
										agents.resources[1] -= 0.02 * agents.resources[0]
										links.agent2.resources[1] -= 0.01 * links.agent2.resources[0]

									# Make sure it is not in a team already and enough resources for the searching agent and that it is known that the other agent's state is not Non
									if links.agent2 == agents and links.agent1.team_as[0] == None and agents.resources[1] > 0.02 * agents.resources[0] and agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][0] != 'No':
										
										# Check if no partial knowledge (initial value)
										if agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][0] == None:
											agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][0] = 0
										if agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][1] == None:
											agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][1] = 0
										if agents.belieftree[1+links.agent1.unique_id][len_DC + len_PC + len_S + prefered_DC*len_PC + (agents.select_problem_3S_as - len_DC)][0] == None:
											agents.belieftree[1+links.agent1.unique_id][len_DC + len_PC + len_S + prefered_DC*len_PC + (agents.select_problem_3S_as - len_DC)][0] = 0

										# Check for the gap and the similarity in states based on partial knowledge 
										if abs(agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][0] - agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][1]) >= team_gap_threshold and \
											abs(agents.belieftree[0][len_DC + len_PC + len_S + prefered_DC*len_PC + (agents.select_problem_3S_as - len_DC)][0] - \
										  	agents.belieftree[1+links.agent1.unique_id][len_DC + len_PC + len_S + prefered_DC*len_PC + (agents.select_problem_3S_as - len_DC)][0]) < team_belief_problem_threshold:
											# Add the agent to the list of potential candidates
											team_list_potential_agent.append(links.agent1)

										# Actual knowledge exchange with a randomness of 0.5
										# Knowledge gained by the lead agent:
										agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][0] = links.agent1.belieftree[0][agents.select_problem_3S_as][0] + (random.random()/2) - 0.25
										agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][1] = links.agent1.belieftree[0][agents.select_problem_3S_as][1] + (random.random()/2) - 0.25
										agents.belieftree[1+links.agent1.unique_id][len_DC + len_PC + len_S + prefered_DC*len_PC + (agents.select_problem_3S_as - len_DC)][0] = \
											links.agent1.belieftree[0][len_DC + len_PC + len_S + prefered_DC*len_PC + (agents.select_problem_3S_as - len_DC)][0] + (random.random()/2) - 0.25
										# 1-1 check
										agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][0] = \
											self.one_minus_one_check(agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][0])
										agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][1] = \
											self.one_minus_one_check(agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][1])
										agents.belieftree[1+links.agent1.unique_id][len_DC + len_PC + len_S + prefered_DC*len_PC + (agents.select_problem_3S_as - len_DC)][0] = \
											self.one_minus_one_check(agents.belieftree[1+links.agent1.unique_id][len_DC + len_PC + len_S + prefered_DC*len_PC + (agents.select_problem_3S_as - len_DC)][0])

										# Knowledge gained by the secondary link agent:
										links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_as][0] = agents.belieftree[0][agents.select_problem_3S_as][0] + (random.random()/2) - 0.25
										links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_as][1] = agents.belieftree[0][agents.select_problem_3S_as][1] + (random.random()/2) - 0.25
										links.agent1.belieftree[1+agents.unique_id][len_DC + len_PC + len_S + prefered_DC*len_PC + (agents.select_problem_3S_as - len_DC)][0] = \
											agents.belieftree[0][len_DC + len_PC + len_S + prefered_DC*len_PC + (agents.select_problem_3S_as - len_DC)][0] + (random.random()/2) - 0.25
										# 1-1 check
										links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_as][0] = \
											self.one_minus_one_check(links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_as][0])
										links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_as][1] = \
											self.one_minus_one_check(links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_as][1])
										links.agent1.belieftree[1+agents.unique_id][len_DC + len_PC + len_S + prefered_DC*len_PC + (agents.select_problem_3S_as - len_DC)][0] = \
											self.one_minus_one_check(links.agent1.belieftree[1+agents.unique_id][len_DC + len_PC + len_S + prefered_DC*len_PC + (agents.select_problem_3S_as - len_DC)][0])

										# Adjusting resources
										agents.resources[1] -= 0.02 * agents.resources[0]
										links.agent1.resources[1] -= 0.01 * links.agent1.resources[0]

									# Stop the while loop when there are enough agents to be in the team
									if len(team_list_potential_agent) > 1:
										break
							break

						# If there are enough agents, we create a team with them
						if len(team_list_potential_agent) == 2:

							# We check that the actual beliefs are within 0.2
							if abs(agents.belieftree[0][len_DC + len_PC + len_S + prefered_DC*len_PC + (agents.select_problem_3S_as - len_DC)][0] - \
								team_list_potential_agent[0].belieftree[0][len_DC + len_PC + len_S + prefered_DC*len_PC + (agents.select_problem_3S_as - len_DC)][0]) < team_belief_problem_threshold and \
								abs(agents.belieftree[0][len_DC + len_PC + len_S + prefered_DC*len_PC + (agents.select_problem_3S_as - len_DC)][0] - \
							  	team_list_potential_agent[1].belieftree[0][len_DC + len_PC + len_S + prefered_DC*len_PC + (agents.select_problem_3S_as - len_DC)][0]) < team_belief_problem_threshold and \
								abs(team_list_potential_agent[0].belieftree[0][agents.select_problem_3S_as][0] - team_list_potential_agent[0].belieftree[0][agents.select_problem_3S_as][1]) >= team_gap_threshold and \
								abs(team_list_potential_agent[1].belieftree[0][agents.select_problem_3S_as][0] - team_list_potential_agent[1].belieftree[0][agents.select_problem_3S_as][1]) >= team_gap_threshold:
								# Now we can create the team						
								members = team_list_potential_agent
								members.append(agents)
								team_resources = [0, 0]
								members_id = []
								for members_for_id in members:
									members_id.append(members_for_id.unique_id)
								team = Team(team_number_as[0], agents, members, members_id, agents.select_issue_3S_as, agents.select_problem_3S_as, tick_number, team_resources)
								print('TEAM CREATION 3!')
								# Iteration of the team ID number for the overall team list
								team_number_as[0] += 1
								team_list_as.append(team)
								team_list_as_total.append(team)
								
								# Exchange of partial knowledge between the agents in the team
								self.knowledge_exchange_team(team, team.issue, 0)

								# Calculation of the average issue belief (based on partial knowledge) per agent:
								for agent_members1 in team.members:
									# Setting the partial knowledge for himself equal to his own belief:
									agent_members1.belieftree[1+agent_members1.unique_id][team.issue][0] = agent_members1.belieftree[0][team.issue][0]
									# Calculating the average belief according to partial knowledge
									issue_avg_belief = []
									for agent_members2 in team.members:
										issue_avg_belief.append(agent_members2.resources[0]*agent_members1.belieftree[1+agent_members2.unique_id][team.issue][0])
									issue_avg_belief = sum(issue_avg_belief)/len(issue_avg_belief)
									# Setting the belonging level
									agent_members1.team_as[1] = 1 - abs(agent_members1.belieftree[0][team.issue][0] - issue_avg_belief)
									# Setting of the team object
									agent_members1.team_as[0] = team
								# Setting the team resources
								for agent_members in team.members:
									team.resources[0] += agent_members.team_as[1]
									team.resources[1] = team.resources[0]

				# If the agent is advocating or a policy, the following tasks are performed
				if agents.select_issue_3S_as == 'policy':

					# Check if the agent indeed has a gap:
					if abs(agents.belieftree[0][agents.select_problem_3S_as][0] - agents.belieftree[0][agents.select_problem_3S_as][1]) >= team_gap_threshold:

						team_list_potential_agent = []
						
						# Go through all possible links for this agent:
						while True:
							shuffled_list_links = link_list
							random.shuffle(shuffled_list_links)
							for links in shuffled_list_links:

								# Make sure that there is aware
								if links.aware > 0:
									
									# Make sure it is not in a team already and enough resources for the searching agent and that it is known that the other agent's state is not Non
									if links.agent1 == agents and links.agent2.team_as[0] == None and agents.resources[1] > 0.02 * agents.resources[0] and agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][0] != 'No':
										
										# Check if no partial knowledge (initial value)
										if agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][0] == None:
											agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][0] = 0
										if agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][1] == None:
											agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][1] = 0
										if agents.belieftree_policy[1+links.agent2.unique_id][agents.select_policy_3S_as][agents.select_problem_3S_as - len_DC] == None:
											agents.belieftree_policy[1+links.agent2.unique_id][agents.select_policy_3S_as][agents.select_problem_3S_as - len_DC] = 0

										# Check for the gap and the similarity in states based on partial knowledge - if okay, add the agent to the list
										if abs(agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][0] - agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][1]) >= team_gap_threshold and \
											abs(agents.belieftree_policy[0][agents.select_policy_3S_as][agents.select_problem_3S_as - len_DC] - \
										  	agents.belieftree_policy[1+links.agent2.unique_id][agents.select_policy_3S_as][agents.select_problem_3S_as - len_DC]) < team_belief_policy_threshold:
											# Add the agent to the list of potential candidates
											team_list_potential_agent.append(links.agent2)

										# Actual knowledge exchange with a randomness of 0.5
										# Knowledge gained by the lead agent:
										agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][0] = links.agent2.belieftree[0][agents.select_problem_3S_as][0] + (random.random()/2) - 0.25
										agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][1] = links.agent2.belieftree[0][agents.select_problem_3S_as][1] + (random.random()/2) - 0.25
										agents.belieftree_policy[1+links.agent2.unique_id][agents.select_policy_3S_as][agents.select_problem_3S_as - len_DC] = \
											links.agent2.belieftree_policy[0][agents.select_policy_3S_as][agents.select_problem_3S_as - len_DC] + (random.random()/2) - 0.25
										# 1-1 check
										agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][0] = \
											self.one_minus_one_check(agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][0])
										agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][1] = \
											self.one_minus_one_check(agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][1])
										agents.belieftree_policy[1+links.agent2.unique_id][agents.select_policy_3S_as][agents.select_problem_3S_as - len_DC] = \
											self.one_minus_one_check(agents.belieftree_policy[1+links.agent2.unique_id][agents.select_policy_3S_as][agents.select_problem_3S_as - len_DC])

										# Knowledge gained by the secondary link agent:
										links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_as][0] = agents.belieftree[0][agents.select_problem_3S_as][0] + (random.random()/2) - 0.25
										links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_as][1] = agents.belieftree[0][agents.select_problem_3S_as][1] + (random.random()/2) - 0.25
										links.agent2.belieftree_policy[1+agents.unique_id][agents.select_policy_3S_as][agents.select_problem_3S_as - len_DC] = \
											agents.belieftree_policy[0][agents.select_policy_3S_as][agents.select_problem_3S_as - len_DC] + (random.random()/2) - 0.25
										# 1-1 check
										links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_as][0] = \
											self.one_minus_one_check(links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_as][0])
										links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_as][1] = \
											self.one_minus_one_check(links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_as][1])
										links.agent2.belieftree_policy[1+agents.unique_id][agents.select_policy_3S_as][agents.select_problem_3S_as - len_DC] = \
											self.one_minus_one_check(links.agent2.belieftree_policy[1+agents.unique_id][agents.select_policy_3S_as][agents.select_problem_3S_as - len_DC])

										# Adjusting resources
										agents.resources[1] -= 0.02 * agents.resources[0]
										links.agent2.resources[1] -= 0.01 * links.agent2.resources[0]

									# Make sure it is not in a team already and enough resources for the searching agent and that it is known that the other agent's state is not Non
									if links.agent2 == agents and links.agent1.team_as[0] == None and agents.resources[1] > 0.02 * agents.resources[0] and agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][0] != 'No':
										
										# Check if no partial knowledge (initial value)
										if agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][0] == None:
											agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][0] = 0
										if agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][1] == None:
											agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][1] = 0
										if agents.belieftree_policy[1+links.agent1.unique_id][agents.select_policy_3S_as][agents.select_problem_3S_as - len_DC] == None:
											agents.belieftree_policy[1+links.agent1.unique_id][agents.select_policy_3S_as][agents.select_problem_3S_as - len_DC] = 0

										# Check for the gap and the similarity in states based on partial knowledge 
										if abs(agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][0] - agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][1]) >= team_gap_threshold and \
											abs(agents.belieftree_policy[0][agents.select_policy_3S_as][agents.select_problem_3S_as - len_DC] - \
										  	agents.belieftree_policy[1+links.agent1.unique_id][agents.select_policy_3S_as][agents.select_problem_3S_as - len_DC]) < team_belief_policy_threshold:
											# Add the agent to the list of potential candidates
											team_list_potential_agent.append(links.agent1)

										# Actual knowledge exchange with a randomness of 0.5
										# Knowledge gained by the lead agent:
										agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][0] = links.agent1.belieftree[0][agents.select_problem_3S_as][0] + (random.random()/2) - 0.25
										agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][1] = links.agent1.belieftree[0][agents.select_problem_3S_as][1] + (random.random()/2) - 0.25
										agents.belieftree_policy[1+links.agent1.unique_id][agents.select_policy_3S_as][agents.select_problem_3S_as - len_DC] = \
											links.agent1.belieftree_policy[0][agents.select_policy_3S_as][agents.select_problem_3S_as - len_DC] + (random.random()/2) - 0.25
										# 1-1 check
										agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][0] = \
											self.one_minus_one_check(agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][0])
										agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][1] = \
											self.one_minus_one_check(agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][1])
										agents.belieftree_policy[1+links.agent1.unique_id][agents.select_policy_3S_as][agents.select_problem_3S_as - len_DC] = \
											self.one_minus_one_check(agents.belieftree_policy[1+links.agent1.unique_id][agents.select_policy_3S_as][agents.select_problem_3S_as - len_DC])

										# Knowledge gained by the secondary link agent:
										links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_as][0] = agents.belieftree[0][agents.select_problem_3S_as][0] + (random.random()/2) - 0.25
										links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_as][1] = agents.belieftree[0][agents.select_problem_3S_as][1] + (random.random()/2) - 0.25
										links.agent1.belieftree_policy[1+agents.unique_id][agents.select_policy_3S_as][agents.select_problem_3S_as - len_DC] = \
											agents.belieftree_policy[0][agents.select_policy_3S_as][agents.select_problem_3S_as - len_DC] + (random.random()/2) - 0.25
										# 1-1 check
										links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_as][0] = \
											self.one_minus_one_check(links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_as][0])
										links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_as][1] = \
											self.one_minus_one_check(links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_as][1])
										links.agent1.belieftree_policy[1+agents.unique_id][agents.select_policy_3S_as][agents.select_problem_3S_as - len_DC] = \
											self.one_minus_one_check(links.agent1.belieftree_policy[1+agents.unique_id][agents.select_policy_3S_as][agents.select_problem_3S_as - len_DC])

										# Adjusting resources
										agents.resources[1] -= 0.02 * agents.resources[0]
										links.agent1.resources[1] -= 0.01 * links.agent1.resources[0]

									# Stop the while loop when there are enough agents to be in the team
									if len(team_list_potential_agent) > 1:
										break
							break

						# If there are enough agents, we create a team with them
						if len(team_list_potential_agent) == 2:

							# We check that the actual beliefs are within 0.2
							if abs(agents.belieftree_policy[0][agents.select_policy_3S_as][agents.select_problem_3S_as - len_DC] - \
								team_list_potential_agent[0].belieftree_policy[0][agents.select_policy_3S_as][agents.select_problem_3S_as - len_DC]) < team_belief_policy_threshold and \
								abs(agents.belieftree_policy[0][agents.select_policy_3S_as][agents.select_problem_3S_as - len_DC] - \
							  	team_list_potential_agent[1].belieftree_policy[0][agents.select_policy_3S_as][agents.select_problem_3S_as - len_DC]) < team_belief_policy_threshold and \
								abs(team_list_potential_agent[0].belieftree[0][agents.select_problem_3S_as][0] - team_list_potential_agent[0].belieftree[0][agents.select_problem_3S_as][1]) >= team_gap_threshold and \
								abs(team_list_potential_agent[1].belieftree[0][agents.select_problem_3S_as][0] - team_list_potential_agent[1].belieftree[0][agents.select_problem_3S_as][1]) >= team_gap_threshold:
								# Now we can create the team						
								members = team_list_potential_agent
								members.append(agents)
								team_resources = [0, 0]
								members_id = []
								for members_for_id in members:
									members_id.append(members_for_id.unique_id)
								team = Team(team_number_as[0], agents, members, members_id, agents.select_issue_3S_as, agents.select_policy_3S_as, tick_number, team_resources)
								print('TEAM CREATION 4!')
								# Iteration of the team ID number for the overall team list
								team_number_as[0] += 1
								team_list_as.append(team)
								team_list_as_total.append(team)
								
								# Exchange of partial knowledge between the agents in the team
								self.knowledge_exchange_team(team, team.issue, 0)

								# Calculation of the average issue belief (based on partial knowledge) per agent:
								for agent_members1 in team.members:
									# Setting the partial knowledge for himself equal to his own belief:
									agent_members1.belieftree[1+agent_members1.unique_id][team.issue][0] = agent_members1.belieftree[0][team.issue][0]
									# Calculating the average belief according to partial knowledge
									issue_avg_belief = []
									for agent_members2 in team.members:
										issue_avg_belief.append(agent_members2.resources[0]*agent_members1.belieftree[1+agent_members2.unique_id][team.issue][0])
									issue_avg_belief = sum(issue_avg_belief)/len(issue_avg_belief)
									# Setting the belonging level
									agent_members1.team_as[1] = 1 - abs(agent_members1.belieftree[0][team.issue][0] - issue_avg_belief)
									# Setting of the team object
									agent_members1.team_as[0] = team
								# Setting the team resources
								for agent_members in team.members:
									team.resources[0] += agent_members.team_as[1]
									team.resources[1] = team.resources[0]

	def agent_team_threeS_pf(self, agents, agent_action_list, team_list_pf, team_list_pf_total, link_list, team_number_pf, tick_number, threeS_link_list_pf, deep_core, \
		policy_core, secondary, agenda_prob_3S_as, team_gap_threshold, team_belief_problem_threshold, team_belief_policy_threshold):

		"""
		Agent-team actions - Three streams (policy formulation)
		===========================

		Note: This is the same function as the one for the agenda setting function
		but with modification for the policy formulation part. This means changes in
		the agents' selected issues.

		This function is used to perform all the agent-team actions during the
		policy formulation. The actions are given in order as follows:
			a. Belonging level update
			b. Leave team check
			c. Disband team check
			d. Join team
			e. Start team

		The team considered within this step are teams that are only present in
		the policy formulation. The agents also only consider the issues they have
		selected for the policy formulation.
		
		"""

		len_DC = len(deep_core)
		len_PC = len(policy_core)
		len_S = len(secondary)

		# print(' ')
		# print('Test')
		# print('This would be the CR of interest')
		# # For the PF
		# print(len_DC + len_PC + len_S + len_DC*len_PC + agenda_prob_3S_as*len_PC + (agents.team_as[0].issue - len_DC - len_PC))

		# a. Belonging level update (completed)
		if agents.team_pf[0] != None:
			self.knowledge_exchange_team(agents.team_pf[0], agents.team_pf[0].issue, 0)
			self.belonging_level_pf(agents, len_DC, len_PC)

		# b. Leave team check (completed)
		if agents.team_pf[0] != None:
			# If the belonging level is below 30%, we remove the agent from the team
			if agents.team_pf[1] < 0.3:
				# If the agent is the lead agent, then the team is disbanded
				team = agents.team_pf[0]
				if agents == agents.team_pf[0].lead:
					# Disband function
					# print('Disband 1 triggered!')
					self.disband_team_pf(agents, team, threeS_link_list_pf, team_list_pf)

				# Else only this agent is removed
				else:
					self.remove_agent_team_pf(agents)
					# If the length of the team becomes too small, then the team has to be disbanded:
					if len(team.members) < 3:
						# Disband function
						# print('Disband 2 triggered!')
						self.disband_team_pf(agents, team, threeS_link_list_pf, team_list_pf)

		# c. Disband team check (completed)
		if agents.team_pf[0] != None:

			# Several cases for which a team can be disbanded:
			# 1. Lead agent changes selected policy
			# This is checked every five ticks
			if (tick_number - agents.team_pf[0].creation) % 5 == 0 and tick_number >= 5:
				# 1. Lead agent has different issue than the team issue (checked every five ticks)
				# Check that the agent is the lead of this team
				if agents == agents.team_pf[0].lead:
					# Check that the agent has different issue type (problem/policy) or different issue number
					if agents.select_problem_3S_pf != agents.team_pf[0].issue or agents.select_issue_3S_pf != agents.team_pf[0].issue_type:
						team = agents.team_pf[0]
						# Disband function
						# print('Disband 3 triggered!')
						self.disband_team_pf(agents, team, threeS_link_list_pf, team_list_pf)

				# 2. Checking if each agent meets the requirements and remove if not
				# Check that the agent has same issue type (problem/policy) and same issue number
				elif agents.select_problem_3S_pf == agents.team_pf[0].issue and agents.select_issue_3S_pf == agents.team_pf[0].issue_type:

					# If the team is advocating for a problem, perform the following actions:
					if agents.team_pf[0].issue_type == 'problem':
						team = agents.team_pf[0]
						agent_removed = 0

						for agent_members in team.members:
							# Opposite of the requirements for the creation of a team
							if abs(team.lead.belieftree[0][len_DC + len_PC + len_S + len_DC*len_PC + (agenda_prob_3S_as-len_DC)*len_PC + (team.issue - len_DC - len_PC)][0] - \
								agent_members.belieftree[0][len_DC + len_PC + len_S + len_DC*len_PC + (agenda_prob_3S_as-len_DC)*len_PC + (team.issue - len_DC - len_PC)][0]) >= team_belief_problem_threshold or \
								abs(agent_members.belieftree[0][agents.select_problem_3S_pf][0] - agent_members.belieftree[0][agents.select_problem_3S_pf][1]) < team_gap_threshold:
								# Disband the team if the leader doesnt meet the requirements anymore
								if agent_members == team.lead:
									self.disband_team_pf(agents, team, threeS_link_list_pf, team_list_pf)
									break
								else:
									self.remove_agent_team_pf(agent_members)
									agent_removed = 1
									if agents == agent_members:
										print('I AM THE AGENT, BREAK AFTER ME')
										break

					# If the team is advocating for a policy, perform the following actions:
					elif agents.team_pf[0].issue_type == 'policy':
						team = agents.team_pf[0]
						agent_removed = 0
						for agent_members in team.members:
							# Opposite of the requirements for the creation of a team
							if abs(team.lead.belieftree_instrument[0][agents.team_pf[0].issue][team.lead.select_problem_3S_pf - len_DC - len_PC] - \
								agent_members.belieftree_instrument[0][agents.team_pf[0].issue][team.lead.select_problem_3S_pf - len_DC - len_PC]) >= team_belief_policy_threshold or \
								abs(agent_members.belieftree[0][team.lead.select_problem_3S_pf][0] - agent_members.belieftree[0][team.lead.select_problem_3S_pf][1]) < team_gap_threshold:
								# Disband the team if the leader doesnt meet the requirements anymore
								if agent_members == team.lead:
									self.disband_team_pf(agents, team, threeS_link_list_pf, team_list_pf)
									break
								else:
									self.remove_agent_team_pf(agent_members)
									agent_removed = 1
									if agents == agent_members:
										print('I AM THE AGENT, BREAK AFTER ME')
										break


					# Recalculate the belonging level of the agents left
					if agents.team_pf[0] != None:
						if agent_removed == 1:
							for agent_members in team.members:
								self.belonging_level_pf(agent_members, len_DC, len_PC)

								# If the belonging level is below 30%, the agents are removed (similar to a previous loop)
								if agent_members.team_pf[1] < 0.3:
									# team = agents.team_pf[0]
									if agent_members == agent_members.team_pf[0].lead:
										# print('Disband 4 triggered!')
										self.disband_team_pf(agent_members, team, threeS_link_list_pf, team_list_pf)
									else:
										self.remove_agent_team_pf(agent_members)
										if len(team.members) < 3:
											# print('Disband 5 triggered!')
											self.disband_team_pf(agent_members, team, threeS_link_list_pf, team_list_pf)

					# Check the length of the team after all agents have been checked - disband if too small
					if agents.team_pf[0] != None:
						if len(agents.team_pf[0].members) < 3:
							# print('Disband 6 triggered!')
							self.disband_team_pf(agents, team, threeS_link_list_pf, team_list_pf)

		# d. Join a team (completed)
		if agents.team_pf[0] == None:

			while True:

				added_team_check = 0

				for join_team in team_list_pf:

					# If the team is advocating for a problem, the following tasks are completed
					if join_team.issue_type == 'problem':

						# Check that the team is still active and has members:
						if len(join_team.members) > 0:

							# None check
							check_none = 0
							if agents.belieftree[1+join_team.lead.unique_id][len_DC + len_PC + len_S + len_DC*len_PC + (agenda_prob_3S_as-len_DC)*len_PC + (join_team.issue - len_DC - len_PC)][0] == None:
								agents.belieftree[1+join_team.lead.unique_id][len_DC + len_PC + len_S + len_DC*len_PC + (agenda_prob_3S_as-len_DC)*len_PC + (join_team.issue - len_DC - len_PC)][0] = 0
								check_none = 1

							# First we check that the agent meets both requirements (based on partial knowledge) (we assume that the agent knows who the leader is)
							if abs(agents.belieftree[0][join_team.issue][0] - agents.belieftree[0][join_team.issue][1]) >= team_gap_threshold and \
								abs(agents.belieftree[0][len_DC + len_PC + len_S + len_DC*len_PC + (agenda_prob_3S_as-len_DC)*len_PC + (join_team.issue - len_DC - len_PC)][0] - \
									agents.belieftree[1+join_team.lead.unique_id][len_DC + len_PC + len_S + len_DC*len_PC + (agenda_prob_3S_as-len_DC)*len_PC + (join_team.issue - len_DC - len_PC)][0]) < team_belief_problem_threshold:

								# Add the agent to the team
								join_team.members.append(agents)
								join_team.members_id.append(agents.unique_id)
								agents.team_pf[0] = join_team
								# Share knowledge within the team
								# Exchange of partial knowledge between the agents in the team
								self.knowledge_exchange_team(join_team, join_team.issue, 0)

								# Change belonging level
								self.belonging_level_pf(agents, len_DC, len_PC)

								# Notify that the loop can be stopped as the agent has been added
								added_team_check = 1

								# None reset
								if check_none == 1:
									agents.belieftree[1+join_team.lead.unique_id][len_DC + len_PC + len_S + len_DC*len_PC + (agenda_prob_3S_as-len_DC)*len_PC + (join_team.issue - len_DC - len_PC)][0] = None

							# update of the resources
							agents.resources[1] -= 0.02 * agents.resources[0]

							# Resources sufficiency check
							if agents.resources[1] < 0.5 * agents.resources[0]:
								break

							# If the agent has been added to a team, stop this entire procedure
							if added_team_check == 1:
								break

					# If the team is advocating for a policy, the following tasks are completed
					if join_team.issue_type == 'policy':

						# Check that the team is still active and has members:
						if len(join_team.members) > 0:

							# None check
							check_none = 0
							if agents.belieftree_instrument[1+join_team.lead.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_DC - len_PC] == None:
								agents.belieftree_instrument[1+join_team.lead.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_DC - len_PC] = 0
								check_none = 1

							# First we check that the agent meets both requirements (based on partial knowledge) (we assume that the agent knows who the leader is)
							if abs(agents.belieftree[0][join_team.lead.select_problem_3S_pf][0] - agents.belieftree[0][join_team.lead.select_problem_3S_pf][1]) >= team_gap_threshold and \
								abs(agents.belieftree_instrument[0][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_DC - len_PC] - \
									agents.belieftree_instrument[1+join_team.lead.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_DC - len_PC]) < team_belief_policy_threshold:

								# Add the agent to the team
								join_team.members.append(agents)
								join_team.members_id.append(agents.unique_id)
								agents.team_pf[0] = join_team
								# Share knowledge within the team
								# Exchange of partial knowledge between the agents in the team
								self.knowledge_exchange_team(join_team, join_team.issue, 0)

								# Change belonging level
								self.belonging_level_pf(agents, len_DC, len_PC)

								# Notify that the loop can be stopped as the agent has been added
								added_team_check = 1

							# None reset
							if check_none == 1:
								agents.belieftree_instrument[1+join_team.lead.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_DC - len_PC] = None

							# update of the resources
							agents.resources[1] -= 0.02 * agents.resources[0]

							# Resources sufficiency check
							if agents.resources[1] < 0.5 * agents.resources[0]:
								break

							# If the agent has been added to a team, stop this entire procedure
							if added_team_check == 1:
								break
				break

		# e. Start a team (completed)
		if agents.team_pf[0] == None:
			# First team creation method:
			# Avoided for now - requires memory

			# Second team creation method:
			# a. Method 0 - All agents that qualify are selected
			if agents.team_pf[2] == 0:
				# print(' ')
				# print(' ')
				# print('Strategy 0')

				# If the agent is advocating or a problem, the following tasks are performed
				if agents.select_issue_3S_pf == 'problem':

					# Check if the agent indeed has a gap:
					if abs(agents.belieftree[0][agents.select_problem_3S_pf][0] - agents.belieftree[0][agents.select_problem_3S_pf][1]) >= team_gap_threshold:

						team_list_potential_agent = []

						shuffled_list_links = link_list
						random.shuffle(shuffled_list_links)
						for links in shuffled_list_links:
							# Make sure that there is aware
							if links.aware > 0:
								# print(links)
								
								# Make sure it is not in a team already and enough resources for the searching agent and that it is known that the other agent's state is not None
								if links.agent1 == agents and links.agent2.team_pf[0] == None and agents.resources[1] > 0.02 * agents.resources[0] and agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][0] != 'No':

									# Check if no partial knowledge (initial value)
									if agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][0] == None:
										agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][0] = 0
									if agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][1] == None:
										agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][1] = 0
									if agents.belieftree[1+links.agent2.unique_id][len_DC + len_PC + len_S + len_DC*len_PC + (agenda_prob_3S_as-len_DC)*len_PC + (agents.select_problem_3S_pf - len_DC - len_PC)][0] == None:
										agents.belieftree[1+links.agent2.unique_id][len_DC + len_PC + len_S + len_DC*len_PC + (agenda_prob_3S_as-len_DC)*len_PC + (agents.select_problem_3S_pf - len_DC - len_PC)][0] = 0

									# Check for the gap and the similarity in states based on partial knowledge - if okay, add the agent to the list
									if abs(agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][0] - agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][1]) >= team_gap_threshold and \
										abs(agents.belieftree[0][len_DC + len_PC + len_S + len_DC*len_PC + (agenda_prob_3S_as-len_DC)*len_PC + (agents.select_problem_3S_pf - len_DC - len_PC)][0] - \
									  	agents.belieftree[1+links.agent2.unique_id][len_DC + len_PC + len_S + len_DC*len_PC + (agenda_prob_3S_as-len_DC)*len_PC + (agents.select_problem_3S_pf - len_DC - len_PC)][0]) < team_belief_problem_threshold:
										# Add the agent to the list of potential candidates
										team_list_potential_agent.append(links.agent2)

									# Actual knowledge exchange with a randomness of 0.5
									# Knowledge gained by the lead agent:
									agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][0] = links.agent2.belieftree[0][agents.select_problem_3S_pf][0] + (random.random()/2) - 0.25
									agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][1] = links.agent2.belieftree[0][agents.select_problem_3S_pf][1] + (random.random()/2) - 0.25
									agents.belieftree[1+links.agent2.unique_id][len_DC + len_PC + len_S + len_DC*len_PC + (agenda_prob_3S_as-len_DC)*len_PC + (agents.select_problem_3S_pf - len_DC - len_PC)][0] = \
										links.agent2.belieftree[0][len_DC + len_PC + len_S + len_DC*len_PC + (agenda_prob_3S_as-len_DC)*len_PC + (agents.select_problem_3S_pf - len_DC - len_PC)][0] + (random.random()/2) - 0.25
									# 1-1 check
									agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][0] = \
										self.one_minus_one_check(agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][0])
									agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][1] = \
										self.one_minus_one_check(agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][1])
									agents.belieftree[1+links.agent2.unique_id][len_DC + len_PC + len_S + len_DC*len_PC + (agenda_prob_3S_as-len_DC)*len_PC + (agents.select_problem_3S_pf - len_DC - len_PC)][0] = \
										self.one_minus_one_check(agents.belieftree[1+links.agent2.unique_id][len_DC + len_PC + len_S + len_DC*len_PC + (agenda_prob_3S_as-len_DC)*len_PC + (agents.select_problem_3S_pf - len_DC - len_PC)][0])

									# Knowledge gained by the secondary link agent:
									links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][0] = agents.belieftree[0][agents.select_problem_3S_pf][0] + (random.random()/2) - 0.25
									links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][1] = agents.belieftree[0][agents.select_problem_3S_pf][1] + (random.random()/2) - 0.25
									links.agent2.belieftree[1+agents.unique_id][len_DC + len_PC + len_S + len_DC*len_PC + (agenda_prob_3S_as-len_DC)*len_PC + (agents.select_problem_3S_pf - len_DC - len_PC)][0] = \
										agents.belieftree[0][len_DC + len_PC + len_S + len_DC*len_PC + (agenda_prob_3S_as-len_DC)*len_PC + (agents.select_problem_3S_pf - len_DC - len_PC)][0] + (random.random()/2) - 0.25
									# 1-1 check
									links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][0] = \
										self.one_minus_one_check(links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][0])
									links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][1] = \
										self.one_minus_one_check(links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][1])
									links.agent2.belieftree[1+agents.unique_id][len_DC + len_PC + len_S + len_DC*len_PC + (agenda_prob_3S_as-len_DC)*len_PC + (agents.select_problem_3S_pf - len_DC - len_PC)][0] = \
										self.one_minus_one_check(links.agent2.belieftree[1+agents.unique_id][len_DC + len_PC + len_S + len_DC*len_PC + (agenda_prob_3S_as-len_DC)*len_PC + (agents.select_problem_3S_pf - len_DC - len_PC)][0])

									# Adjusting resources
									agents.resources[1] -= 0.02 * agents.resources[0]
									links.agent2.resources[1] -= 0.01 * links.agent2.resources[0]

								# Make sure it is not in a team already and enough resources for the searching agent and that it is known that the other agent's state is not Non
								if links.agent2 == agents and links.agent1.team_pf[0] == None and agents.resources[1] > 0.02 * agents.resources[0] and agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][0] != 'No':
										
										# Check if no partial knowledge (initial value)
										if agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][0] == None:
											agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][0] = 0
										if agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][1] == None:
											agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][1] = 0
										if agents.belieftree[1+links.agent1.unique_id][len_DC + len_PC + len_S + len_DC*len_PC + (agenda_prob_3S_as-len_DC)*len_PC + (agents.select_problem_3S_pf - len_DC - len_PC)][0] == None:
											agents.belieftree[1+links.agent1.unique_id][len_DC + len_PC + len_S + len_DC*len_PC + (agenda_prob_3S_as-len_DC)*len_PC + (agents.select_problem_3S_pf - len_DC - len_PC)][0] = 0

										# Check for the gap and the similarity in states based on partial knowledge
										if abs(agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][0] - agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][1]) >= team_gap_threshold and \
											abs(agents.belieftree[0][len_DC + len_PC + len_S + len_DC*len_PC + (agenda_prob_3S_as-len_DC)*len_PC + (agents.select_problem_3S_pf - len_DC - len_PC)][0] - \
										  	agents.belieftree[1+links.agent1.unique_id][len_DC + len_PC + len_S + len_DC*len_PC + (agenda_prob_3S_as-len_DC)*len_PC + (agents.select_problem_3S_pf - len_DC - len_PC)][0]) < team_belief_problem_threshold:
											
											# Add the agent to the list of potential candidates
											team_list_potential_agent.append(links.agent1)

										# Actual knowledge exchange with a randomness of 0.5
										# Knowledge gained by the lead agent:
										agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][0] = links.agent1.belieftree[0][agents.select_problem_3S_pf][0] + (random.random()/2) - 0.25
										agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][1] = links.agent1.belieftree[0][agents.select_problem_3S_pf][1] + (random.random()/2) - 0.25
										agents.belieftree[1+links.agent1.unique_id][len_DC + len_PC + len_S + len_DC*len_PC + (agenda_prob_3S_as-len_DC)*len_PC + (agents.select_problem_3S_pf - len_DC - len_PC)][0] = \
											links.agent1.belieftree[0][len_DC + len_PC + len_S + len_DC*len_PC + (agenda_prob_3S_as-len_DC)*len_PC + (agents.select_problem_3S_pf - len_DC - len_PC)][0] + (random.random()/2) - 0.25
										# 1-1 check
										agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][0] = \
											self.one_minus_one_check(agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][0])
										agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][1] = \
											self.one_minus_one_check(agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][1])
										agents.belieftree[1+links.agent1.unique_id][len_DC + len_PC + len_S + len_DC*len_PC + (agenda_prob_3S_as-len_DC)*len_PC + (agents.select_problem_3S_pf - len_DC - len_PC)][0] = \
											self.one_minus_one_check(agents.belieftree[1+links.agent1.unique_id][len_DC + len_PC + len_S + len_DC*len_PC + (agenda_prob_3S_as-len_DC)*len_PC + (agents.select_problem_3S_pf - len_DC - len_PC)][0])

										# Knowledge gained by the secondary link agent:
										links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][0] = agents.belieftree[0][agents.select_problem_3S_pf][0] + (random.random()/2) - 0.25
										links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][1] = agents.belieftree[0][agents.select_problem_3S_pf][1] + (random.random()/2) - 0.25
										links.agent1.belieftree[1+agents.unique_id][len_DC + len_PC + len_S + len_DC*len_PC + (agenda_prob_3S_as-len_DC)*len_PC + (agents.select_problem_3S_pf - len_DC - len_PC)][0] = \
											agents.belieftree[0][len_DC + len_PC + len_S + len_DC*len_PC + (agenda_prob_3S_as-len_DC)*len_PC + (agents.select_problem_3S_pf - len_DC - len_PC)][0] + (random.random()/2) - 0.25
										# 1-1 check
										links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][0] = \
											self.one_minus_one_check(links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][0])
										links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][1] = \
											self.one_minus_one_check(links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][1])
										links.agent1.belieftree[1+agents.unique_id][len_DC + len_PC + len_S + len_DC*len_PC + (agenda_prob_3S_as-len_DC)*len_PC + (agents.select_problem_3S_pf - len_DC - len_PC)][0] = \
											self.one_minus_one_check(links.agent1.belieftree[1+agents.unique_id][len_DC + len_PC + len_S + len_DC*len_PC + (agenda_prob_3S_as-len_DC)*len_PC + (agents.select_problem_3S_pf - len_DC - len_PC)][0])

										# Adjusting resources
										agents.resources[1] -= 0.02 * agents.resources[0]
										links.agent1.resources[1] -= 0.01 * links.agent1.resources[0]

						# If the list has more than 2 agents, then we can check to create a team
						if len(team_list_potential_agent) > 1:
							team_list_actual_agent = []
							# Make a new list containing the agent that actually match the requirements
							for potential_agent in team_list_potential_agent:
								if agents.belieftree[0][agents.select_problem_3S_pf][0] != 'No':
									if abs(agents.belieftree[0][len_DC + len_PC + len_S + len_DC*len_PC + (agenda_prob_3S_as-len_DC)*len_PC + (agents.select_problem_3S_pf - len_DC - len_PC)][0] - \
										potential_agent.belieftree[0][len_DC + len_PC + len_S + len_DC*len_PC + (agenda_prob_3S_as-len_DC)*len_PC + (agents.select_problem_3S_pf - len_DC - len_PC)][0]) < team_belief_problem_threshold and \
								  		abs(potential_agent.belieftree[0][agents.select_problem_3S_pf][0] - potential_agent.belieftree[0][agents.select_problem_3S_pf][1]) >= team_gap_threshold:
								  		team_list_actual_agent.append(potential_agent)
								else:
									print('1. ALERT - THIS IS AN INTRUDER - A AGENT THAT SHOULDNT BE IN THIS TEAM IS IN THIS TEAM')

							# Check that the list is still more than two agents and if so create the team:
							if len(team_list_potential_agent) > 1:

								# Now we can create the team						
								members = team_list_potential_agent
								members.append(agents)
								team_resources = [0, 0]
								members_id = []
								for members_for_id in members:
									members_id.append(members_for_id.unique_id)
								team = Team(team_number_pf[0], agents, members, members_id, agents.select_issue_3S_pf, agents.select_problem_3S_pf, tick_number, team_resources)
								print('TEAM CREATION 5! ')
								# Iteration of the team ID number for the overall team list
								team_number_pf[0] += 1
								team_list_pf.append(team)
								team_list_pf_total.append(team)
								
								# Exchange of partial knowledge between the agents in the team
								self.knowledge_exchange_team(team, team.issue, 0)

								# Calculation of the average issue belief for belonging calculation (based on partial knowledge) per agent:
								for agent_members1 in team.members:
									# Setting the partial knowledge for himself equal to his own belief:
									agent_members1.belieftree[1+agent_members1.unique_id][team.issue][0] = agent_members1.belieftree[0][team.issue][0]
									# Calculating the average belief according to partial knowledge
									issue_avg_belief = []
									for agent_members2 in team.members:
										if agent_members1.belieftree[1+agent_members2.unique_id][team.issue][0] != 'No':
											issue_avg_belief.append(agent_members2.resources[0]*agent_members1.belieftree[1+agent_members2.unique_id][team.issue][0])
										else:
											print('2. ALERT - THIS IS AN INTRUDER - A AGENT THAT SHOULDNT BE IN THIS TEAM IS IN THIS TEAM')
									issue_avg_belief = sum(issue_avg_belief)/len(issue_avg_belief)
									# Setting the belonging level
									agent_members1.team_pf[1] = 1 - abs(agent_members1.belieftree[0][team.issue][0] - issue_avg_belief)
									# Setting of the team object
									agent_members1.team_pf[0] = team
								# Setting the team resources
								for agent_members in team.members:
									team.resources[0] += agent_members.team_pf[1]
									team.resources[1] = team.resources[0]

				# If the agent is advocating or a policy, the following tasks are performed
				if agents.select_issue_3S_pf == 'policy':

					# Check if the agent indeed has a gap:
					if abs(agents.belieftree[0][agents.select_problem_3S_pf][0] - agents.belieftree[0][agents.select_problem_3S_pf][1]) >= team_gap_threshold:

						team_list_potential_agent = []

						shuffled_list_links = link_list
						random.shuffle(shuffled_list_links)
						for links in shuffled_list_links:
							# Make sure that there is aware
							if links.aware > 0:
								# print(links)
								
								# Make sure it is not in a team already and enough resources for the searching agent and that it is known that the other agent's state is not None
								if links.agent1 == agents and links.agent2.team_pf[0] == None and agents.resources[1] > 0.02 * agents.resources[0] and agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][0] != 'No':

									# Check if no partial knowledge (initial value)
									if agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][0] == None:
										agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][0] = 0
									if agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][1] == None:
										agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][1] = 0
									if agents.belieftree_instrument[1+links.agent2.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_DC - len_PC] == None:
										agents.belieftree_instrument[1+links.agent2.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_DC - len_PC] = 0

									# Check for the gap and the similarity in states based on partial knowledge - if okay, add the agent to the list
									if abs(agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][0] - agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][1]) >= team_gap_threshold and \
										abs(agents.belieftree_instrument[0][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_DC - len_PC] - \
									  	agents.belieftree_instrument[1+links.agent2.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_DC - len_PC]) < team_belief_policy_threshold:
										# Add the agent to the list of potential candidates
										team_list_potential_agent.append(links.agent2)

									# Actual knowledge exchange with a randomness of 0.5
									# Knowledge gained by the lead agent:
									agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][0] = links.agent2.belieftree[0][agents.select_problem_3S_pf][0] + (random.random()/2) - 0.25
									agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][1] = links.agent2.belieftree[0][agents.select_problem_3S_pf][1] + (random.random()/2) - 0.25
									agents.belieftree_instrument[1+links.agent2.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_DC - len_PC] = \
										links.agent2.belieftree_instrument[0][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_DC - len_PC] + (random.random()/2) - 0.25
									# 1-1 check
									agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][0] = \
										self.one_minus_one_check(agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][0])
									agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][1] = \
										self.one_minus_one_check(agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][1])
									agents.belieftree_instrument[1+links.agent2.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_DC - len_PC] = \
										self.one_minus_one_check(agents.belieftree_instrument[1+links.agent2.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_DC - len_PC])

									# Knowledge gained by the secondary link agent:
									links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][0] = agents.belieftree[0][agents.select_problem_3S_pf][0] + (random.random()/2) - 0.25
									links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][1] = agents.belieftree[0][agents.select_problem_3S_pf][1] + (random.random()/2) - 0.25
									links.agent2.belieftree_instrument[1+agents.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_DC - len_PC] = \
										agents.belieftree_instrument[0][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_DC - len_PC] + (random.random()/2) - 0.25
									# 1-1 check
									links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][0] = \
										self.one_minus_one_check(links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][0])
									links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][1] = \
										self.one_minus_one_check(links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][1])
									links.agent2.belieftree_instrument[1+agents.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_DC - len_PC] = \
										self.one_minus_one_check(links.agent2.belieftree_instrument[1+agents.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_DC - len_PC])

									# Adjusting resources
									agents.resources[1] -= 0.02 * agents.resources[0]
									links.agent2.resources[1] -= 0.01 * links.agent2.resources[0]

								# Make sure it is not in a team already and enough resources for the searching agent and that it is known that the other agent's state is not Non
								if links.agent2 == agents and links.agent1.team_pf[0] == None and agents.resources[1] > 0.02 * agents.resources[0] and agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][0] != 'No':
										
										# Check if no partial knowledge (initial value)
										if agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][0] == None:
											agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][0] = 0
										if agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][1] == None:
											agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][1] = 0
										if agents.belieftree_instrument[1+links.agent1.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_DC - len_PC] == None:
											agents.belieftree_instrument[1+links.agent1.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_DC - len_PC] = 0

										# Check for the gap and the similarity in states based on partial knowledge
										if abs(agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][0] - agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][1]) >= team_gap_threshold and \
											abs(agents.belieftree_instrument[0][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_DC - len_PC] - \
										  	agents.belieftree_instrument[1+links.agent1.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_DC - len_PC]) < team_belief_policy_threshold:
											
											# Add the agent to the list of potential candidates
											team_list_potential_agent.append(links.agent1)

										# Actual knowledge exchange with a randomness of 0.5
										# Knowledge gained by the lead agent:
										agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][0] = links.agent1.belieftree[0][agents.select_problem_3S_pf][0] + (random.random()/2) - 0.25
										agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][1] = links.agent1.belieftree[0][agents.select_problem_3S_pf][1] + (random.random()/2) - 0.25
										agents.belieftree_instrument[1+links.agent1.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_DC - len_PC] = \
											links.agent1.belieftree_instrument[0][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_DC - len_PC] + (random.random()/2) - 0.25
										# 1-1 check
										agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][0] = \
											self.one_minus_one_check(agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][0])
										agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][1] = \
											self.one_minus_one_check(agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][1])
										agents.belieftree_instrument[1+links.agent1.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_DC - len_PC] = \
											self.one_minus_one_check(agents.belieftree_instrument[1+links.agent1.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_DC - len_PC])

										# Knowledge gained by the secondary link agent:
										links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][0] = agents.belieftree[0][agents.select_problem_3S_pf][0] + (random.random()/2) - 0.25
										links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][1] = agents.belieftree[0][agents.select_problem_3S_pf][1] + (random.random()/2) - 0.25
										links.agent1.belieftree_instrument[1+agents.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_DC - len_PC] = \
											agents.belieftree_instrument[0][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_DC - len_PC] + (random.random()/2) - 0.25
										# 1-1 check
										links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][0] = \
											self.one_minus_one_check(links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][0])
										links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][1] = \
											self.one_minus_one_check(links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][1])
										links.agent1.belieftree_instrument[1+agents.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_DC - len_PC] = \
											self.one_minus_one_check(links.agent1.belieftree_instrument[1+agents.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_DC - len_PC])

										# Adjusting resources
										agents.resources[1] -= 0.02 * agents.resources[0]
										links.agent1.resources[1] -= 0.01 * links.agent1.resources[0]

						# If the list has more than 2 agents, then we can check to create a team
						if len(team_list_potential_agent) > 1:
							team_list_actual_agent = []
							# Make a new list containing the agent that actually match the requirements
							for potential_agent in team_list_potential_agent:
								if agents.belieftree[0][agents.select_problem_3S_pf][0] != 'No':
									if abs(agents.belieftree_instrument[0][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_DC - len_PC] - \
										potential_agent.belieftree_instrument[0][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_DC - len_PC]) < team_belief_policy_threshold and \
								  		abs(potential_agent.belieftree[0][agents.select_problem_3S_pf][0] - potential_agent.belieftree[0][agents.select_problem_3S_pf][1]) >= team_gap_threshold:
								  		team_list_actual_agent.append(potential_agent)
								else:
									print('1. ALERT - THIS IS AN INTRUDER - A AGENT THAT SHOULDNT BE IN THIS TEAM IS IN THIS TEAM')

							# Check that the list is still more than two agents and if so create the team:
							if len(team_list_potential_agent) > 1:

								# Now we can create the team						
								members = team_list_potential_agent
								members.append(agents)
								team_resources = [0, 0]
								members_id = []
								for members_for_id in members:
									members_id.append(members_for_id.unique_id)
								team = Team(team_number_pf[0], agents, members, members_id, agents.select_issue_3S_pf, agents.select_policy_3S_pf, tick_number, team_resources)
								print('TEAM CREATION 6! ')
								# Iteration of the team ID number for the overall team list
								team_number_pf[0] += 1
								team_list_pf.append(team)
								team_list_pf_total.append(team)
								
								# Exchange of partial knowledge between the agents in the team
								self.knowledge_exchange_team(team, team.issue, 0)

								# Calculation of the average issue belief for belonging calculation (based on partial knowledge) per agent:
								for agent_members1 in team.members:
									# Setting the partial knowledge for himself equal to his own belief:
									agent_members1.belieftree[1+agent_members1.unique_id][team.issue][0] = agent_members1.belieftree[0][team.issue][0]
									# Calculating the average belief according to partial knowledge
									issue_avg_belief = []
									for agent_members2 in team.members:
										if agent_members1.belieftree[1+agent_members2.unique_id][team.issue][0] != 'No':
											issue_avg_belief.append(agent_members2.resources[0]*agent_members1.belieftree[1+agent_members2.unique_id][team.issue][0])
										else:
											print('2. ALERT - THIS IS AN INTRUDER - A AGENT THAT SHOULDNT BE IN THIS TEAM IS IN THIS TEAM')
									issue_avg_belief = sum(issue_avg_belief)/len(issue_avg_belief)
									# Setting the belonging level
									agent_members1.team_pf[1] = 1 - abs(agent_members1.belieftree[0][team.issue][0] - issue_avg_belief)
									# Setting of the team object
									agent_members1.team_pf[0] = team
								# Setting the team resources
								for agent_members in team.members:
									team.resources[0] += agent_members.team_pf[1]
									team.resources[1] = team.resources[0]


			# b. Method 1 - Only the first X agents are selected for the team
			if agents.team_pf[2] == 1:
				# print(' ')
				# print(' ')
				# print('Strategy 1')

				# If the agent is advocating or a problem, the following tasks are performed
				if agents.select_issue_3S_pf == 'problem':

					# Check if the agent indeed has a gap:
					if abs(agents.belieftree[0][agents.select_problem_3S_pf][0] - agents.belieftree[0][agents.select_problem_3S_pf][1]) >= team_gap_threshold:

						team_list_potential_agent = []
						
						# Go through all possible links for this agent:
						while True:
							shuffled_list_links = link_list
							random.shuffle(shuffled_list_links)
							for links in shuffled_list_links:

								# Make sure that there is aware
								if links.aware > 0:
									
									# Make sure it is not in a team already and enough resources for the searching agent and that it is known that the other agent's state is not Non
									if links.agent1 == agents and links.agent2.team_pf[0] == None and agents.resources[1] > 0.02 * agents.resources[0] and agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][0] != 'No':
										
										# Check if no partial knowledge (initial value)
										if agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][0] == None:
											agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][0] = 0
										if agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][1] == None:
											agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][1] = 0
										if agents.belieftree[1+links.agent2.unique_id][len_DC + len_PC + len_S + len_DC*len_PC + (agenda_prob_3S_as-len_DC)*len_PC + (agents.select_problem_3S_pf - len_DC - len_PC)][0] == None:
											agents.belieftree[1+links.agent2.unique_id][len_DC + len_PC + len_S + len_DC*len_PC + (agenda_prob_3S_as-len_DC)*len_PC + (agents.select_problem_3S_pf - len_DC - len_PC)][0] = 0

										# Check for the gap and the similarity in states based on partial knowledge - if okay, add the agent to the list
										if abs(agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][0] - agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][1]) >= team_gap_threshold and \
											abs(agents.belieftree[0][len_DC + len_PC + len_S + len_DC*len_PC + (agenda_prob_3S_as-len_DC)*len_PC + (agents.select_problem_3S_pf - len_DC - len_PC)][0] - \
											agents.belieftree[1+links.agent2.unique_id][len_DC + len_PC + len_S + len_DC*len_PC + (agenda_prob_3S_as-len_DC)*len_PC + (agents.select_problem_3S_pf - len_DC - len_PC)][0]) < team_belief_problem_threshold:
											# Add the agent to the list of potential candidates
											team_list_potential_agent.append(links.agent2)

										# Actual knowledge exchange with a randomness of 0.5
										# Knowledge gained by the lead agent:
										agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][0] = links.agent2.belieftree[0][agents.select_problem_3S_pf][0] + (random.random()/2) - 0.25
										agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][1] = links.agent2.belieftree[0][agents.select_problem_3S_pf][1] + (random.random()/2) - 0.25
										agents.belieftree[1+links.agent2.unique_id][len_DC + len_PC + len_S + len_DC*len_PC + (agenda_prob_3S_as-len_DC)*len_PC + (agents.select_problem_3S_pf - len_DC - len_PC)][0] = \
											links.agent2.belieftree[0][len_DC + len_PC + len_S + len_DC*len_PC + (agenda_prob_3S_as-len_DC)*len_PC + (agents.select_problem_3S_pf - len_DC - len_PC)][0] + (random.random()/2) - 0.25
										# 1-1 check
										agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][0] = \
											self.one_minus_one_check(agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][0])
										agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][1] = \
											self.one_minus_one_check(agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][1])
										agents.belieftree[1+links.agent2.unique_id][len_DC + len_PC + len_S + len_DC*len_PC + (agenda_prob_3S_as-len_DC)*len_PC + (agents.select_problem_3S_pf - len_DC - len_PC)][0] = \
											self.one_minus_one_check(agents.belieftree[1+links.agent2.unique_id][len_DC + len_PC + len_S + len_DC*len_PC + (agenda_prob_3S_as-len_DC)*len_PC + (agents.select_problem_3S_pf - len_DC - len_PC)][0])

										# Knowledge gained by the secondary link agent:
										links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][0] = agents.belieftree[0][agents.select_problem_3S_pf][0] + (random.random()/2) - 0.25
										links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][1] = agents.belieftree[0][agents.select_problem_3S_pf][1] + (random.random()/2) - 0.25
										links.agent2.belieftree[1+agents.unique_id][len_DC + len_PC + len_S + len_DC*len_PC + (agenda_prob_3S_as-len_DC)*len_PC + (agents.select_problem_3S_pf - len_DC - len_PC)][0] = \
											agents.belieftree[0][len_DC + len_PC + len_S + len_DC*len_PC + (agenda_prob_3S_as-len_DC)*len_PC + (agents.select_problem_3S_pf - len_DC - len_PC)][0] + (random.random()/2) - 0.25
										# 1-1 check
										links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][0] = \
											self.one_minus_one_check(links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][0])
										links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][1] = \
											self.one_minus_one_check(links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][1])
										links.agent2.belieftree[1+agents.unique_id][len_DC + len_PC + len_S + len_DC*len_PC + (agenda_prob_3S_as-len_DC)*len_PC + (agents.select_problem_3S_pf - len_DC - len_PC)][0] = \
											self.one_minus_one_check(links.agent2.belieftree[1+agents.unique_id][len_DC + len_PC + len_S + len_DC*len_PC + (agenda_prob_3S_as-len_DC)*len_PC + (agents.select_problem_3S_pf - len_DC - len_PC)][0])

										# Adjusting resources
										agents.resources[1] -= 0.02 * agents.resources[0]
										links.agent2.resources[1] -= 0.01 * links.agent2.resources[0]

									# Make sure it is not in a team already and enough resources for the searching agent and that it is known that the other agent's state is not Non
									if links.agent2 == agents and links.agent1.team_pf[0] == None and agents.resources[1] > 0.02 * agents.resources[0] and agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][0] != 'No':
										
										# Check if no partial knowledge (initial value)
										if agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][0] == None:
											agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][0] = 0
										if agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][1] == None:
											agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][1] = 0
										if agents.belieftree[1+links.agent1.unique_id][len_DC + len_PC + len_S + len_DC*len_PC + ((agenda_prob_3S_as-len_DC)-len_DC)*len_PC + (agents.select_problem_3S_pf - len_DC - len_PC)][0] == None:
											agents.belieftree[1+links.agent1.unique_id][len_DC + len_PC + len_S + len_DC*len_PC + (agenda_prob_3S_as-len_DC)*len_PC + (agents.select_problem_3S_pf - len_DC - len_PC)][0] = 0

										# Check for the gap and the similarity in states based on partial knowledge 
										if abs(agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][0] - agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][1]) >= team_gap_threshold and \
											abs(agents.belieftree[0][len_DC + len_PC + len_S + len_DC*len_PC + (agenda_prob_3S_as-len_DC)*len_PC + (agents.select_problem_3S_pf - len_DC - len_PC)][0] - \
											agents.belieftree[1+links.agent1.unique_id][len_DC + len_PC + len_S + len_DC*len_PC + (agenda_prob_3S_as-len_DC)*len_PC + (agents.select_problem_3S_pf - len_DC - len_PC)][0]) < team_belief_problem_threshold:
											# Add the agent to the list of potential candidates
											team_list_potential_agent.append(links.agent1)

										# Actual knowledge exchange with a randomness of 0.5
										# Knowledge gained by the lead agent:
										agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][0] = links.agent1.belieftree[0][agents.select_problem_3S_pf][0] + (random.random()/2) - 0.25
										agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][1] = links.agent1.belieftree[0][agents.select_problem_3S_pf][1] + (random.random()/2) - 0.25
										agents.belieftree[1+links.agent1.unique_id][len_DC + len_PC + len_S + len_DC*len_PC + (agenda_prob_3S_as-len_DC)*len_PC + (agents.select_problem_3S_pf - len_DC - len_PC)][0] = \
											links.agent1.belieftree[0][len_DC + len_PC + len_S + len_DC*len_PC + (agenda_prob_3S_as-len_DC)*len_PC + (agents.select_problem_3S_pf - len_DC - len_PC)][0] + (random.random()/2) - 0.25
										# 1-1 check
										agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][0] = \
											self.one_minus_one_check(agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][0])
										agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][1] = \
											self.one_minus_one_check(agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][1])
										agents.belieftree[1+links.agent1.unique_id][len_DC + len_PC + len_S + len_DC*len_PC + (agenda_prob_3S_as-len_DC)*len_PC + (agents.select_problem_3S_pf - len_DC - len_PC)][0] = \
											self.one_minus_one_check(agents.belieftree[1+links.agent1.unique_id][len_DC + len_PC + len_S + len_DC*len_PC + (agenda_prob_3S_as-len_DC)*len_PC + (agents.select_problem_3S_pf - len_DC - len_PC)][0])

										# Knowledge gained by the secondary link agent:
										links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][0] = agents.belieftree[0][agents.select_problem_3S_pf][0] + (random.random()/2) - 0.25
										links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][1] = agents.belieftree[0][agents.select_problem_3S_pf][1] + (random.random()/2) - 0.25
										links.agent1.belieftree[1+agents.unique_id][len_DC + len_PC + len_S + len_DC*len_PC + (agenda_prob_3S_as-len_DC)*len_PC + (agents.select_problem_3S_pf - len_DC - len_PC)][0] = \
											agents.belieftree[0][len_DC + len_PC + len_S + len_DC*len_PC + (agenda_prob_3S_as-len_DC)*len_PC + (agents.select_problem_3S_pf - len_DC - len_PC)][0] + (random.random()/2) - 0.25
										# 1-1 check
										links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][0] = \
											self.one_minus_one_check(links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][0])
										links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][1] = \
											self.one_minus_one_check(links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][1])
										links.agent1.belieftree[1+agents.unique_id][len_DC + len_PC + len_S + len_DC*len_PC + (agenda_prob_3S_as-len_DC)*len_PC + (agents.select_problem_3S_pf - len_DC - len_PC)][0] = \
											self.one_minus_one_check(links.agent1.belieftree[1+agents.unique_id][len_DC + len_PC + len_S + len_DC*len_PC + (agenda_prob_3S_as-len_DC)*len_PC + (agents.select_problem_3S_pf - len_DC - len_PC)][0])

										# Adjusting resources
										agents.resources[1] -= 0.02 * agents.resources[0]
										links.agent1.resources[1] -= 0.01 * links.agent1.resources[0]

									# Stop the while loop when there are enough agents to be in the team
									if len(team_list_potential_agent) > 1:
										break
							break

						# If there are enough agents, we create a team with them
						if len(team_list_potential_agent) == 2:

							# We check that the actual beliefs are within 0.2
							if abs(agents.belieftree[0][len_DC + len_PC + len_S + len_DC*len_PC + (agenda_prob_3S_as-len_DC)*len_PC + (agents.select_problem_3S_pf - len_DC - len_PC)][0] - \
								team_list_potential_agent[0].belieftree[0][len_DC + len_PC + len_S + len_DC*len_PC + (agenda_prob_3S_as-len_DC)*len_PC + (agents.select_problem_3S_pf - len_DC - len_PC)][0]) < team_belief_problem_threshold and \
								abs(agents.belieftree[0][len_DC + len_PC + len_S + len_DC*len_PC + (agenda_prob_3S_as-len_DC)*len_PC + (agents.select_problem_3S_pf - len_DC - len_PC)][0] - \
								team_list_potential_agent[1].belieftree[0][len_DC + len_PC + len_S + len_DC*len_PC + (agenda_prob_3S_as-len_DC)*len_PC + (agents.select_problem_3S_pf - len_DC - len_PC)][0]) < team_belief_problem_threshold and \
								abs(team_list_potential_agent[0].belieftree[0][agents.select_problem_3S_pf][0] - team_list_potential_agent[0].belieftree[0][agents.select_problem_3S_pf][1]) >= team_gap_threshold and \
								abs(team_list_potential_agent[1].belieftree[0][agents.select_problem_3S_pf][0] - team_list_potential_agent[1].belieftree[0][agents.select_problem_3S_pf][1]) >= team_gap_threshold:
								# Now we can create the team						
								members = team_list_potential_agent
								members.append(agents)
								team_resources = [0, 0]
								members_id = []
								for members_for_id in members:
									members_id.append(members_for_id.unique_id)
								team = Team(team_number_pf[0], agents, members, members_id, agents.select_issue_3S_pf, agents.select_problem_3S_pf, tick_number, team_resources)
								print('TEAM CREATION 7! ')
								# Iteration of the team ID number for the overall team list
								team_number_pf[0] += 1
								team_list_pf.append(team)
								team_list_pf_total.append(team)
								
								# Exchange of partial knowledge between the agents in the team
								self.knowledge_exchange_team(team, team.issue, 0)

								# Calculation of the average issue belief (based on partial knowledge) per agent:
								for agent_members1 in team.members:
									# Setting the partial knowledge for himself equal to his own belief:
									agent_members1.belieftree[1+agent_members1.unique_id][team.issue][0] = agent_members1.belieftree[0][team.issue][0]
									# Calculating the average belief according to partial knowledge
									issue_avg_belief = []
									for agent_members2 in team.members:
										issue_avg_belief.append(agent_members2.resources[0]*agent_members1.belieftree[1+agent_members2.unique_id][team.issue][0])
									issue_avg_belief = sum(issue_avg_belief)/len(issue_avg_belief)
									# Setting the belonging level
									agent_members1.team_pf[1] = 1 - abs(agent_members1.belieftree[0][team.issue][0] - issue_avg_belief)
									# Setting of the team object
									agent_members1.team_pf[0] = team

								# Setting the team resources
								for agent_members in team.members:
									team.resources[0] += agent_members.team_pf[1]
									team.resources[1] = team.resources[0]

				# If the agent is advocating or a policy, the following tasks are performed
				if agents.select_issue_3S_pf == 'policy':

					# Check if the agent indeed has a gap:
					if abs(agents.belieftree[0][agents.select_problem_3S_pf][0] - agents.belieftree[0][agents.select_problem_3S_pf][1]) >= team_gap_threshold:

						team_list_potential_agent = []
						
						# Go through all possible links for this agent:
						while True:
							shuffled_list_links = link_list
							random.shuffle(shuffled_list_links)
							for links in shuffled_list_links:

								# Make sure that there is aware
								if links.aware > 0:
									
									# Make sure it is not in a team already and enough resources for the searching agent and that it is known that the other agent's state is not Non
									if links.agent1 == agents and links.agent2.team_pf[0] == None and agents.resources[1] > 0.02 * agents.resources[0] and agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][0] != 'No':
										
										# Check if no partial knowledge (initial value)
										if agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][0] == None:
											agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][0] = 0
										if agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][1] == None:
											agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][1] = 0
										if agents.belieftree_instrument[1+links.agent2.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_DC - len_PC] == None:
											agents.belieftree_instrument[1+links.agent2.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_DC - len_PC] = 0

										# Check for the gap and the similarity in states based on partial knowledge - if okay, add the agent to the list
										if abs(agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][0] - agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][1]) >= team_gap_threshold and \
											abs(agents.belieftree_instrument[0][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_DC - len_PC] - \
											agents.belieftree_instrument[1+links.agent2.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_DC - len_PC]) < team_belief_policy_threshold:
											# Add the agent to the list of potential candidates
											team_list_potential_agent.append(links.agent2)

										# Actual knowledge exchange with a randomness of 0.5
										# Knowledge gained by the lead agent:
										agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][0] = links.agent2.belieftree[0][agents.select_problem_3S_pf][0] + (random.random()/2) - 0.25
										agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][1] = links.agent2.belieftree[0][agents.select_problem_3S_pf][1] + (random.random()/2) - 0.25
										agents.belieftree_instrument[1+links.agent2.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_DC - len_PC] = \
											links.agent2.belieftree_instrument[0][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_DC - len_PC] + (random.random()/2) - 0.25
										# 1-1 check
										agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][0] = \
											self.one_minus_one_check(agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][0])
										agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][1] = \
											self.one_minus_one_check(agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][1])
										agents.belieftree_instrument[1+links.agent2.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_DC - len_PC] = \
											self.one_minus_one_check(agents.belieftree_instrument[1+links.agent2.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_DC - len_PC])

										# Knowledge gained by the secondary link agent:
										links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][0] = agents.belieftree[0][agents.select_problem_3S_pf][0] + (random.random()/2) - 0.25
										links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][1] = agents.belieftree[0][agents.select_problem_3S_pf][1] + (random.random()/2) - 0.25
										links.agent2.belieftree_instrument[1+agents.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_DC - len_PC] = \
											agents.belieftree_instrument[0][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_DC - len_PC] + (random.random()/2) - 0.25
										# 1-1 check
										links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][0] = \
											self.one_minus_one_check(links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][0])
										links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][1] = \
											self.one_minus_one_check(links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][1])
										links.agent2.belieftree_instrument[1+agents.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_DC - len_PC] = \
											self.one_minus_one_check(links.agent2.belieftree_instrument[1+agents.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_DC - len_PC])

										# Adjusting resources
										agents.resources[1] -= 0.02 * agents.resources[0]
										links.agent2.resources[1] -= 0.01 * links.agent2.resources[0]

									# Make sure it is not in a team already and enough resources for the searching agent and that it is known that the other agent's state is not Non
									if links.agent2 == agents and links.agent1.team_pf[0] == None and agents.resources[1] > 0.02 * agents.resources[0] and agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][0] != 'No':
										
										# Check if no partial knowledge (initial value)
										if agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][0] == None:
											agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][0] = 0
										if agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][1] == None:
											agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][1] = 0
										if agents.belieftree_instrument[1+links.agent1.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_DC - len_PC] == None:
											agents.belieftree_instrument[1+links.agent1.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_DC - len_PC] = 0

										# Check for the gap and the similarity in states based on partial knowledge 
										if abs(agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][0] - agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][1]) >= team_gap_threshold and \
											abs(agents.belieftree_instrument[0][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_DC - len_PC] - \
											agents.belieftree_instrument[1+links.agent1.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_DC - len_PC]) < team_belief_policy_threshold:
											# Add the agent to the list of potential candidates
											team_list_potential_agent.append(links.agent1)

										# Actual knowledge exchange with a randomness of 0.5
										# Knowledge gained by the lead agent:
										agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][0] = links.agent1.belieftree[0][agents.select_problem_3S_pf][0] + (random.random()/2) - 0.25
										agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][1] = links.agent1.belieftree[0][agents.select_problem_3S_pf][1] + (random.random()/2) - 0.25
										agents.belieftree_instrument[1+links.agent1.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_DC - len_PC] = \
											links.agent1.belieftree_instrument[0][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_DC - len_PC] + (random.random()/2) - 0.25
										# 1-1 check
										agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][0] = \
											self.one_minus_one_check(agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][0])
										agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][1] = \
											self.one_minus_one_check(agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][1])
										agents.belieftree_instrument[1+links.agent1.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_DC - len_PC] = \
											self.one_minus_one_check(agents.belieftree_instrument[1+links.agent1.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_DC - len_PC])

										# Knowledge gained by the secondary link agent:
										links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][0] = agents.belieftree[0][agents.select_problem_3S_pf][0] + (random.random()/2) - 0.25
										links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][1] = agents.belieftree[0][agents.select_problem_3S_pf][1] + (random.random()/2) - 0.25
										links.agent1.belieftree_instrument[1+agents.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_DC - len_PC] = \
											agents.belieftree_instrument[0][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_DC - len_PC] + (random.random()/2) - 0.25
										# 1-1 check
										links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][0] = \
											self.one_minus_one_check(links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][0])
										links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][1] = \
											self.one_minus_one_check(links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][1])
										links.agent1.belieftree_instrument[1+agents.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_DC - len_PC] = \
											self.one_minus_one_check(links.agent1.belieftree_instrument[1+agents.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_DC - len_PC])

										# Adjusting resources
										agents.resources[1] -= 0.02 * agents.resources[0]
										links.agent1.resources[1] -= 0.01 * links.agent1.resources[0]

									# Stop the while loop when there are enough agents to be in the team
									if len(team_list_potential_agent) > 1:
										break
							break

						# If there are enough agents, we create a team with them
						if len(team_list_potential_agent) == 2:

							# We check that the actual beliefs are within 0.2
							if abs(agents.belieftree_instrument[0][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_DC - len_PC] - \
								team_list_potential_agent[0].belieftree_instrument[0][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_DC - len_PC]) < team_belief_policy_threshold and \
								abs(agents.belieftree_instrument[0][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_DC - len_PC] - \
								team_list_potential_agent[1].belieftree_instrument[0][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_DC - len_PC]) < team_belief_policy_threshold and \
								abs(team_list_potential_agent[0].belieftree[0][agents.select_problem_3S_pf][0] - team_list_potential_agent[0].belieftree[0][agents.select_problem_3S_pf][1]) >= team_gap_threshold and \
								abs(team_list_potential_agent[1].belieftree[0][agents.select_problem_3S_pf][0] - team_list_potential_agent[1].belieftree[0][agents.select_problem_3S_pf][1]) >= team_gap_threshold:
								# Now we can create the team						
								members = team_list_potential_agent
								members.append(agents)
								team_resources = [0, 0]
								members_id = []
								for members_for_id in members:
									members_id.append(members_for_id.unique_id)
								team = Team(team_number_pf[0], agents, members, members_id, agents.select_issue_3S_pf, agents.select_problem_3S_pf, tick_number, team_resources)
								print('TEAM CREATION 8! ')
								# Iteration of the team ID number for the overall team list
								team_number_pf[0] += 1
								team_list_pf.append(team)
								team_list_pf_total.append(team)
								
								# Exchange of partial knowledge between the agents in the team
								self.knowledge_exchange_team(team, team.issue, 0)

								# Calculation of the average issue belief (based on partial knowledge) per agent:
								for agent_members1 in team.members:
									# Setting the partial knowledge for himself equal to his own belief:
									agent_members1.belieftree[1+agent_members1.unique_id][team.issue][0] = agent_members1.belieftree[0][team.issue][0]
									# Calculating the average belief according to partial knowledge
									issue_avg_belief = []
									for agent_members2 in team.members:
										issue_avg_belief.append(agent_members2.resources[0]*agent_members1.belieftree[1+agent_members2.unique_id][team.issue][0])
									issue_avg_belief = sum(issue_avg_belief)/len(issue_avg_belief)
									# Setting the belonging level
									agent_members1.team_pf[1] = 1 - abs(agent_members1.belieftree[0][team.issue][0] - issue_avg_belief)
									# Setting of the team object
									agent_members1.team_pf[0] = team
								# Setting the team resources
								for agent_members in team.members:
									team.resources[0] += agent_members.team_pf[1]
									team.resources[1] = team.resources[0]

	def disband_team_as(self, agents, team, threeS_link_list_as, team_list_as):

		"""
		Disband team function (agenda setting)
		===========================

		This is the disband team function. It removes agents from a team, 
		remove the team from the list of active teams in the agenda setting,
		and makes sure that the agents that were in the team have their
		attributes updated to say that they are not in a team anymore.
		
		"""

		# Deleting the associated shadow network
		to_be_deleted_links = []
		# print(' ')
		# Select the link in question
		for links in threeS_link_list_as:
			if links.agent1 == team:
				to_be_deleted_links.append(links)

		for link in to_be_deleted_links:
			threeS_link_list_as.remove(link)

		# Checking all agents in the team
		for removed_agent in team.members:
			# Remove agent object from the agent
			removed_agent.team_as[0] = None
			# Remove the belonging value of the agent
			removed_agent.team_as[1] = None
		# Removing the members from the team list and the leader of the team
		# For purposes of testing, the issue is kept along with the other attributes
		team.members = []
		team.lead = None
		# Remove the team from the list of active teams
		team_list_as.remove(team)

	def disband_team_pf(self, agents, team, threeS_link_list_pf, team_list_pf):

		"""
		Disband team function (policy formulation)
		===========================

		This is the disband team function. It removes agents from a team, 
		remove the team from the list of active teams in the policy formulation,
		and makes sure that the agents that were in the team have their
		attributes updated to say that they are not in a team anymore.
		
		"""

		# Deleting the associated shadow network
		to_be_deleted_links = []
		# print(' ')
		# Select the link in question
		for links in threeS_link_list_pf:
			if links.agent1 == team:
				to_be_deleted_links.append(links)

		for link in to_be_deleted_links:
			threeS_link_list_pf.remove(link)

		# Checking all agents in the team
		for removed_agent in team.members:
			# Remove agent object from the agent
			removed_agent.team_pf[0] = None
			# Remove the belonging value of the agent
			removed_agent.team_pf[1] = None
		# Removing the members from the team list and the leader of the team
		# For purposes of testing, the issue is kept along with the other attributes
		team.members = []
		team.lead = None
		# Remove the team from the list of active teams
		team_list_pf.remove(team)

	def remove_agent_team_as(self, agents_removal):

		"""
		Remove agent from team function (agenda setting)
		===========================

		This function removes agent from a specified team while updating its
		attributes to reflect that the agent is not part of the team anymore.
		This is the agenda setting version of the function
		
		"""

		agents_removal.team_as[0].members_id.remove(agents_removal.unique_id)
		agents_removal.team_as[0].members.remove(agents_removal)
		# Remove object and belonging values
		agents_removal.team_as[0] = None
		agents_removal.team_as[1] = None

	def remove_agent_team_pf(self, agents_removal):

		"""
		Remove agent from team function (policy formulation)
		===========================

		This function removes agent from a specified team while updating its
		attributes to reflect that the agent is not part of the team anymore.
		This is the policy formulation version of the function
		
		"""

		agents_removal.team_pf[0].members_id.remove(agents_removal.unique_id)
		agents_removal.team_pf[0].members.remove(agents_removal)

		# Remove object and belonging values
		agents_removal.team_pf[0] = None
		agents_removal.team_pf[1] = None

	def belonging_level_as(self, agents, len_DC, len_PC):

		"""
		Belonging level calculation function (agenda setting)
		===========================

		This function is used to update the belonging level of the agents within
		a team. For this first the average of the beliefs is calculated. Then each 
		agent's belonging level is calculated based on the difference between
		their beliefs and the average. This is the agenda setting version.

		Note: This function seems to be incorrectly used in so far as it is used
		for both policy and problem teams while it should only be used for problems
		teams.
		
		"""

		issue_avg_belief = []
		# Setting the partial knowledge for himself equal to his own belief:
		agents.belieftree[1+agents.unique_id][agents.team_as[0].issue][0] = agents.belieftree[0][agents.team_as[0].issue][0]
		# Calculation of the average issue belief for belonging calculation (based on partial knowledge) per agent:
		for agent_members in agents.team_as[0].members:
			issue_avg_belief.append(agent_members.resources[0]*agents.belieftree[1+agent_members.unique_id][agents.team_as[0].issue][0])
		# if len(issue_avg_belief) != 0:
		issue_avg_belief = sum(issue_avg_belief)/len(issue_avg_belief)
		# else:
		# 	issue_avg_belief = 0
		agents.team_as[1] = 1 - abs(agents.belieftree[0][agents.team_as[0].issue][0] - issue_avg_belief)

	def belonging_level_pf(self, agents, len_DC, len_PC):

		"""
		Belonging level calculation function (policy formulation)
		===========================

		This function is used to update the belonging level of the agents within
		a team. For this first the average of the beliefs is calculated. Then each 
		agent's belonging level is calculated based on the difference between
		their beliefs and the average. This is the policy formulation version.

		Note: This function seems to be incorrectly used in so far as it is used
		for both policy and problem teams while it should only be used for problems
		teams.
		
		"""

		issue_avg_belief = []
		# Setting the partial knowledge for himself equal to his own belief:
		agents.belieftree[1+agents.unique_id][agents.team_pf[0].issue][0] = agents.belieftree[0][agents.team_pf[0].issue][0]
		# Calculation of the average issue belief for belonging calculation (based on partial knowledge) per agent:
		for agent_members in agents.team_pf[0].members:
			issue_avg_belief.append(agent_members.resources[0]*agents.belieftree[1+agent_members.unique_id][agents.team_pf[0].issue][0])
		issue_avg_belief = sum(issue_avg_belief)/len(issue_avg_belief)
		agents.team_pf[1] = 1 - abs(agents.belieftree[0][agents.team_pf[0].issue][0] - issue_avg_belief)

	def knowledge_exchange_team(self, team, issue, parameter):

		"""
		Knowledge exchange function - teams
		===========================

		This function is used for the exchange of partial knowledge between agents
		within the same team. This only regards the issue that is selected by the team
		and is kept with a certain amount of randomness.

		Note: This function seems to be incorrectly used in so far as it is used
		for both policy and problem teams while it should only be used for problems
		teams.
		
		"""

		# Exchange of partial knowledge between the agents in the team
		for agent_exchange1 in team.members:
			for agent_exchange2 in team.members:
				# Actual knowledge exchange with a randomness of 0.2
				# print('Before: ' + str(agent_exchange1.belieftree[1 + agent_exchange2.unique_id][team.issue][0]))
				if agent_exchange2.belieftree[0][issue][0] != 'No':
					agent_exchange1.belieftree[1 + agent_exchange2.unique_id][issue][parameter] = \
					  agent_exchange2.belieftree[0][issue][0] + (random.random()/5) - 0.1
					# 1-1 check
					agent_exchange1.belieftree[1 + agent_exchange2.unique_id][issue][parameter] = \
						self.one_minus_one_check(agent_exchange1.belieftree[1 + agent_exchange2.unique_id][issue][parameter])

	def one_minus_one_check(self, to_be_checked_parameter):

		"""
		One minus one check function
		===========================

		This function checks that a certain values does not got over one
		and does not go below one due to the randomisation.
		
		"""

		checked_parameter = 0
		if to_be_checked_parameter > 1:
			checked_parameter = 1
		elif to_be_checked_parameter < -1:
			checked_parameter = -1
		else:
			checked_parameter = to_be_checked_parameter
		return checked_parameter

	##############################################################################
	######################## TO BE MODIFIED AND INTEGRATED #######################
	##############################################################################

	def knowledge_exchange_coalition_policy(self, team, cw_knowledge, parameter):

		# Exchange of partial knowledge between the agents in the team
		for agent_exchange1 in team.members:
			for agent_exchange2 in team.members:
				# Actual knowledge exchange with a randomness of 0.2
				# print('Before: ' + str(agent_exchange1.belieftree[1 + agent_exchange2.unique_id][team.issue][0]))
				agent_exchange1.belieftree_policy[1 + agent_exchange2.unique_id][cw_knowledge][parameter] = \
				  agent_exchange2.belieftree_policy[0][cw_knowledge][0] + (random.random()/5) - 0.1
				# print('After: ' + str(agent_exchange1.belieftree[1 + agent_exchange2.unique_id][team.issue][0]))
				# 1-1 check
				if agent_exchange1.belieftree_policy[1 + agent_exchange2.unique_id][cw_knowledge][parameter] > 1:
					agent_exchange1.belieftree_policy[1 + agent_exchange2.unique_id][cw_knowledge][parameter] = 1
				if agent_exchange1.belieftree_policy[1 + agent_exchange2.unique_id][cw_knowledge][parameter] < -1:
					agent_exchange1.belieftree_policy[1 + agent_exchange2.unique_id][cw_knowledge][parameter]  = -1

	def knowledge_exchange_coalition_instrument(self, team, cw_knowledge, parameter):

		# Exchange of partial knowledge between the agents in the team
		for agent_exchange1 in team.members:
			for agent_exchange2 in team.members:
				# Actual knowledge exchange with a randomness of 0.2
				# print('Before: ' + str(agent_exchange1.belieftree[1 + agent_exchange2.unique_id][team.issue][0]))
				agent_exchange1.belieftree_instrument[1 + agent_exchange2.unique_id][cw_knowledge][parameter] = \
				  agent_exchange2.belieftree_instrument[0][cw_knowledge][0] + (random.random()/5) - 0.1
				# print('After: ' + str(agent_exchange1.belieftree[1 + agent_exchange2.unique_id][team.issue][0]))
				# 1-1 check
				if agent_exchange1.belieftree_instrument[1 + agent_exchange2.unique_id][cw_knowledge][parameter] > 1:
					agent_exchange1.belieftree_instrument[1 + agent_exchange2.unique_id][cw_knowledge][parameter] = 1
				if agent_exchange1.belieftree_instrument[1 + agent_exchange2.unique_id][cw_knowledge][parameter] < -1:
					agent_exchange1.belieftree_instrument[1 + agent_exchange2.unique_id][cw_knowledge][parameter]  = -1
