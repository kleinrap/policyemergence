from agent import Agent
import random
import copy


# Creation of the truth agents
class Truth(Agent):

	def __init__(self, pos, belieftree_truth):
		# super().__init__(unique_id, model)
		self.pos = pos
		# self.model = model
		self.belieftree_truth = belieftree_truth

	def __str__(self):
		return 'Position: [' + str(self.pos[0]) + ',' + str(self.pos[1]) + '], Belief tree: ' + str(self.belieftree_truth)

# Creation of the electorate agents
class Electorate(Agent):

	def __init__(self, run_number, pos, affiliation, belieftree_electorate, representation):
		# super().__init__(unique_id, model)
		self.run_number = run_number
		self.pos = pos
		# self.model = model
		self.affiliation = affiliation
		self.belieftree_electorate = belieftree_electorate
		self.representation = representation

	def electorate_influence(self, agent, master_list, affiliation_number, electorate_influence_coefficient):
		self.master_list = master_list

		policymaker_list = []
		for agents in self.master_list:
			if type(agents) == Policymakers:
				policymaker_list.append(agents)

		policymaker_number = len(policymaker_list)
		# policymaker_list = self.master_list[Policymakers]
		# Looking through all affiliations
		for i in range(affiliation_number):
			# Selecting one affiliation
			if self.affiliation == i:
				# Selection of the policy maker:
				for j in range(policymaker_number):
					# checking of the affiliation match of the policy maker
					if policymaker_list[j].affiliation == i:
						# Now we can change the tree of the policy makers
						for k in range(len(self.belieftree_electorate)):
							# print('Before change: ' + str(policymaker_list[j].belieftree[0][k][1]))
							policymaker_list[j].belieftree[0][k][1] = policymaker_list[j].belieftree[0][k][1] + \
							  (self.belieftree_electorate[k][1] - policymaker_list[j].belieftree[0][k][1]) * electorate_influence_coefficient
							# Again the oneminusone check does not work here
							policymaker_list[j].belieftree[0][k][1] = \
								self.one_minus_one_check2(policymaker_list[j].belieftree[0][k][1])
							# print('Afters change: ' + str(policymaker_list[j].belieftree[0][k][1]))
						# print(policymaker_list[j].pos)
				# print(self.belieftree_electorate)
				# print(self.affiliation)
				# print(self.pos)

	def one_minus_one_check2(self, to_be_checked_parameter):

		checked_parameter = 0
		if to_be_checked_parameter > 1:
			checked_parameter = 1
		elif to_be_checked_parameter < -1:
			checked_parameter = -1
		else:
			checked_parameter = to_be_checked_parameter
		return checked_parameter

	def electorate_states_update(self, agent, master_list, affiliation_weights):

		"""
		The electorate states update function
		===========================

		This function uses the agent, the master list and the affiliation weight
		to update the states of the electorate belief tree. This is done using the
		states of the external parties depending on their affiliation and is therefore
		impacted by the affiliation weights.

		It is also assumed that the initial belief of the electorate is equal
		to their aim in the first tick.

		"""

		#' Addition of more than 3 affiliation will lead to unreported errors!')
		if len(affiliation_weights) != 3:
			print('WARNING - THIS CODE DOESNT WORK FOR MORE OR LESS THAN 3 AFFILIATIONS')

		# Defining the external party list along with the truth agent relation
		externalparties_list = []
		for agents in master_list:
			if type(agents) == Truth:
				truthagent = agents
			if type(agents) == Externalparties:
				externalparties_list.append(agents)

		# Going through the different external parties:
		belief_sum_ep = [0 for k in range(len(truthagent.belieftree_truth))]
		for i in range(len(truthagent.belieftree_truth)):
			# This is used because in some cases, the external parties will have no impact on the agent (None values in the states of the EP)
			actual_length_ep = 0
			for j in range(len(externalparties_list)):
				# This line is added in case the EP has None states
				if externalparties_list[j].belieftree[i][0] != 'No':
					actual_length_ep += 1
					# Currently, the state of the policy makers is initialised as being equal to their initial aim:
					if agent.belieftree_electorate[i][0] == None:
						# print('Triggered - changed to: ' + str(agent.belieftree[0][i][1]))
						agent.belieftree_electorate[i][0] = agent.belieftree_electorate[i][1]
					# If they have the same affiliation, add without weight
					if externalparties_list[j].affiliation == agent.affiliation:
						# print('AFFILIATIONS ARE EQUAL')
						# print('issue ' + str(i+1) + ': ' + str(externalparties_list[j].belieftree[0][i][0]) +  /
						# ' and affiliation: ' + str(externalparties_list[j].affiliation) + '  ' + str(externalparties_list[j].unique_id))
						# print('This is the sum: ' + str(belief_sum_ep[i]))
						belief_sum_ep[i] = belief_sum_ep[i] + (externalparties_list[j].belieftree[0][i][0] - agent.belieftree_electorate[i][0])
						# print('The sum is equal to: ' + str(belief_sum_ep))
						# print('The change in state belief is equal to: ' + str(belief_sum_ep[i] / len(externalparties_list)))
					if (externalparties_list[j].affiliation == 0 and agent.affiliation == 1) or \
					   (externalparties_list[j].affiliation == 1 and agent.affiliation == 0):
						# print('AFFILIATION 1 AND 2')
						belief_sum_ep[i] = belief_sum_ep[i] + \
						   (externalparties_list[j].belieftree[0][i][0] - agent.belieftree_electorate[i][0]) * affiliation_weights[0]
					if (externalparties_list[j].affiliation == 0 and agent.affiliation == 2) or \
					   (externalparties_list[j].affiliation == 2 and agent.affiliation == 0):
						# print('AFFILIATION 1 AND 3')
						belief_sum_ep[i] = belief_sum_ep[i] + \
						   (externalparties_list[j].belieftree[0][i][0] - agent.belieftree_electorate[i][0]) * affiliation_weights[1]
					if (externalparties_list[j].affiliation == 1 and agent.affiliation == 2) or \
					   (externalparties_list[j].affiliation == 2 and agent.affiliation == 1):
						# print('AFFILIATION 2 AND 3')
						belief_sum_ep[i] = belief_sum_ep[i] + \
						   (externalparties_list[j].belieftree[0][i][0] - agent.belieftree_electorate[i][0]) * affiliation_weights[2]
			agent.belieftree_electorate[i][0] = agent.belieftree_electorate[i][0] + belief_sum_ep[i] / actual_length_ep

	# def __str__(self):
	# 	return 'Affiliation: ' + str(self.affiliation) + ', Position: [' + str(self.pos[0]) + \
	# 	',' + str(self.pos[1]) + '], Electorate belief tree: ' + str(self.belieftree_electorate)

# Creation of the external party agents
class Externalparties(Agent):

	def __init__(self, run_number, agent_id, unique_id, pos, network_strategy, affiliation, resources, belieftree, instrument_preferences, belieftree_policy, belieftree_instrument, select_as_issue, select_pinstrument, select_issue_3S_as, \
		select_problem_3S_as, select_policy_3S_as, select_issue_3S_pf, select_problem_3S_pf, select_policy_3S_pf, team_as, team_pf, coalition_as, coalition_pf):
		# super().__init__(unique_id, model)
		self.run_number = run_number
		self.agent_id = agent_id
		self.unique_id = unique_id
		self.pos = pos
		self.network_strategy = network_strategy
		self.affiliation = affiliation
		self.resources = resources
		self.belieftree = belieftree
		self.instrument_preferences = instrument_preferences
		self.belieftree_policy = belieftree_policy
		self.belieftree_instrument = belieftree_instrument
		self.select_as_issue = select_as_issue
		self.select_pinstrument = select_pinstrument
		self.select_issue_3S_as = select_issue_3S_as
		self.select_problem_3S_as = select_problem_3S_as
		self.select_policy_3S_as = select_policy_3S_as
		self.select_issue_3S_pf = select_issue_3S_pf
		self.select_problem_3S_pf = select_problem_3S_pf
		self.select_policy_3S_pf = select_policy_3S_pf
		self.team_as = team_as
		self.team_pf = team_pf
		self.coalition_as = coalition_as
		self.coalition_pf = coalition_pf

	def external_parties_states_update(self, agent, master_list, no_interest_states):

		for agents in master_list:
			if type(agents) == Truth:
				truthagent = agents

		# print('Before: '  + str(agent.belieftree[0]))
		for i in range(len(truthagent.belieftree_truth)):
			# print(no_interest_states[agent.agent_id][i])
			if no_interest_states[agent.agent_id][i] == 1:
				# print('Value i: ' + str(i) + ' is being changed')
				agent.belieftree[0][i][0] = truthagent.belieftree_truth[i]
			# print('HERE!')
			else:
				agent.belieftree[0][i][0] = 'No'

		# print('After: '  + str(agent.belieftree[0]))
		# print('State updated!')

	def external_parties_preference_udapte(self, agent, master_list, len_DC, len_PC, len_S):
		# This has been placed in the main Policyemergence part
		pass	
	
	# def __str__(self):
	# 	return 'EXTERNAL PARTIES - ' + 'Affiliation: ' + str(self.affiliation) + ', Resources: ' + str(self.resources) + \
	# 	', Position: [' + str(self.pos[0]) + \
	# 	',' + str(self.pos[1]) + '], ID: ' + str(self.unique_id) + ', Problem selected + 1: ' + str(self.select_problem) + \
	# 	', Policy selected + 1: ' + str(self.select_policy) + ', Belief tree: ' + str(self.belieftree)

	# Simple print with ID
	def __str__(self):
		return 'External party: ' + str(self.unique_id)

	def external_parties_actions_as(self, agents, agent_action_list, causalrelation_number, \
		affiliation_weights, deep_core, policy_core, secondary, electorate_number, action_agent_number, master_list):

		len_DC = len(deep_core)
		len_PC = len(policy_core)
		len_S = len(secondary)

		agents.resources_actions_BFraming = agents.resources_actions * 0.5
		agents.resources_actions_EInfluence = agents.resources_actions * 0.5
		# 1. Blanket framing, grading of actions and implementation of the best actions until resources run out 
		# 50% of the resources (from actions)

		cw_of_interest = []
		# We only consider the causal relations related to the problem on the agenda
		for cw_choice in range(len(deep_core)):
				cw_of_interest.append(len_DC + len_PC + len_S + (agents.select_as_issue - len_DC) + cw_choice * len(policy_core))

		if len(cw_of_interest) > 0:
			while agents.resources_actions_BFraming > 0.001:
				# FIRST - Calculation of the best option
				# Estimating the grades of the changes in the causal relations - Based on partial knowledge:
				actions_EP_grades_BFraming = []
				for cw in range(len(cw_of_interest)):
					# Go through each of the agents
					actions_EP_grades_BFraming_ind = []

					for agents_BFraming in range(len(agent_action_list)):
						# Making sure that the agent does not count itself
						if agents != agent_action_list[agents_BFraming]:

							# Calculate the impact of the framing depending on affiliations:
							# WATCH OUT - The agent action list is not ordered, it is therefore paramount to select based on unique_id and not on item number in the list!!
							# This warning only applies when looking for the partial knowledge beliefs in the belief tree of the original agent.
							# Same affiliation

							# Check if no partial knowledge (initial value)
							check_none = 0
							if agents.belieftree[1 + agent_action_list[agents_BFraming].unique_id][cw_of_interest[cw]][0] == None:
								check_none = 1
								agents.belieftree[1 + agent_action_list[agents_BFraming].unique_id][cw_of_interest[cw]][0] = 0
							
							if agents.affiliation == agent_action_list[agents_BFraming].affiliation:
								cw_grade = abs((agents.belieftree[0][cw_of_interest[cw]][0] - \
								agents.belieftree[1 + agent_action_list[agents_BFraming].unique_id][cw_of_interest[cw]][0]) * \
								agents.resources[0] * 0.1 / (action_agent_number - 1))

							# Affiliation 1 and 2
							if (agents.affiliation == 0 and agent_action_list[agents_BFraming].affiliation == 1) or \
			    			  (agents.affiliation == 1 and agent_action_list[agents_BFraming].affiliation == 0):
								cw_grade = abs((agents.belieftree[0][cw_of_interest[cw]][0] - \
								agents.belieftree[1 + agent_action_list[agents_BFraming].unique_id][cw_of_interest[cw]][0]) * \
								agents.resources[0] * 0.1 * affiliation_weights[0] / (action_agent_number - 1))

							# Affiliation 1 and 3
							if (agents.affiliation == 0 and agent_action_list[agents_BFraming].affiliation == 2) or \
							  (agents.affiliation == 2 and agent_action_list[agents_BFraming].affiliation == 0):
								cw_grade = abs((agents.belieftree[0][cw_of_interest[cw]][0] - \
								agents.belieftree[1 + agent_action_list[agents_BFraming].unique_id][cw_of_interest[cw]][0]) * \
								agents.resources[0] * 0.1 * affiliation_weights[1] / (action_agent_number - 1))

							# Affiliation 2 and 3
							if (agents.affiliation == 1 and agent_action_list[agents_BFraming].affiliation == 2) or \
							 (agents.affiliation == 2 and agent_action_list[agents_BFraming].affiliation == 1):
								cw_grade = abs((agents.belieftree[0][len(deep_core) + len(policy_core) + len(secondary) + cw][0] - \
								agents.belieftree[1 + agent_action_list[agents_BFraming].unique_id][cw_of_interest[cw]][0]) * \
								agents.resources[0] * 0.1 * affiliation_weights[2] / (action_agent_number - 1))

							# Reset the value after finding the grade
							if check_none == 1:
								agents.belieftree[1 + agent_action_list[agents_BFraming].unique_id][cw_of_interest[cw]][0] = None
							
							actions_EP_grades_BFraming_ind.append(cw_grade)
						# If it is the same agent, then rate the action as 0 (important for appropriate indexing)
						else:
							cw_grade = 0
							actions_EP_grades_BFraming_ind.append(cw_grade)

					actions_EP_grades_BFraming.append(sum(actions_EP_grades_BFraming_ind))

				# Finding the index of the causal relation most affected based on the partial knowledge
				best_BFraming = actions_EP_grades_BFraming.index(max(actions_EP_grades_BFraming))

				# SECOND - Changing the causal relations of all the agents - Based on actual beliefs:
				for agents_BFraming in range(len(agent_action_list)):
					# Making sure that the agent does not count itself
					if agents != agent_action_list[agents_BFraming]:

						# Same affiliation
						if agents.affiliation == agent_action_list[agents_BFraming].affiliation:
							agent_action_list[agents_BFraming].belieftree[0][cw_of_interest[best_BFraming]][0] += \
							(agents.belieftree[0][cw_of_interest[best_BFraming]][0] - \
							agent_action_list[agents_BFraming].belieftree[0][cw_of_interest[best_BFraming]][0]) * \
							agents.resources[0] * 0.1 / (action_agent_number - 1)
						
						# Affiliation 1 and 2
						if (agents.affiliation == 0 and agent_action_list[agents_BFraming].affiliation == 1) or \
		    			  (agents.affiliation == 1 and agent_action_list[agents_BFraming].affiliation == 0):
							agent_action_list[agents_BFraming].belieftree[0][cw_of_interest[best_BFraming]][0] += \
							(agents.belieftree[0][cw_of_interest[best_BFraming]][0] - \
							agent_action_list[agents_BFraming].belieftree[0][cw_of_interest[best_BFraming]][0]) * \
							agents.resources[0] * 0.1 * affiliation_weights[0] / (action_agent_number - 1)
						
						# Affiliation 1 and 3
						if (agents.affiliation == 0 and agent_action_list[agents_BFraming].affiliation == 2) or \
						  (agents.affiliation == 2 and agent_action_list[agents_BFraming].affiliation == 0):
							agent_action_list[agents_BFraming].belieftree[0][cw_of_interest[best_BFraming]][0] += \
							(agents.belieftree[0][cw_of_interest[best_BFraming]][0] - \
							agent_action_list[agents_BFraming].belieftree[0][cw_of_interest[best_BFraming]][0]) * \
							agents.resources[0] * 0.1 * affiliation_weights[1] / (action_agent_number - 1)
						
						# Affiliation 2 and 3
						if (agents.affiliation == 1 and agent_action_list[agents_BFraming].affiliation == 2) or \
						 (agents.affiliation == 2 and agent_action_list[agents_BFraming].affiliation == 1):
							agent_action_list[agents_BFraming].belieftree[0][cw_of_interest[best_BFraming]][0] += \
							(agents.belieftree[0][cw_of_interest[best_BFraming]][0] - \
							agent_action_list[agents_BFraming].belieftree[0][cw_of_interest[best_BFraming]][0]) * \
							agents.resources[0] * 0.1 * affiliation_weights[2] / (action_agent_number - 1)

						# Check that it is not higher than 1 or lower than -1
						if agent_action_list[agents_BFraming].belieftree[0][cw_of_interest[best_BFraming]][0] > 1:
							agent_action_list[agents_BFraming].belieftree[0][cw_of_interest[best_BFraming]][0] = 1
						if agent_action_list[agents_BFraming].belieftree[0][cw_of_interest[best_BFraming]][0] < -1:
							agent_action_list[agents_BFraming].belieftree[0][cw_of_interest[best_BFraming]][0] = -1

						# Providing partial knowledge - Blanket framing - 0.5 range from real value: (Acting agent)
						agents.belieftree[1 + agent_action_list[agents_BFraming].unique_id][cw_of_interest[best_BFraming]][0] = \
							agent_action_list[agents_BFraming].belieftree[0][cw_of_interest[best_BFraming]][0] + (random.random()/2) - 0.25
						# 1-1 check
						if agents.belieftree[1 + agent_action_list[agents_BFraming].unique_id][cw_of_interest[best_BFraming]][0] > 1:
							agents.belieftree[1 + agent_action_list[agents_BFraming].unique_id][cw_of_interest[best_BFraming]][0] = 1
						if agents.belieftree[1 + agent_action_list[agents_BFraming].unique_id][cw_of_interest[best_BFraming]][0] < -1:
							agents.belieftree[1 + agent_action_list[agents_BFraming].unique_id][cw_of_interest[best_BFraming]][0] = -1
						# Providing partial knowledge - Blanket framing - 0.5 range from real value: (Acted upon agent)
						agent_action_list[agents_BFraming].belieftree[1 + agents.unique_id][cw_of_interest[best_BFraming]][0] = \
							agents.belieftree[0][cw_of_interest[best_BFraming]][0] + (random.random()/2) - 0.25
						# 1-1 check
						if agent_action_list[agents_BFraming].belieftree[1 + agents.unique_id][cw_of_interest[best_BFraming]][0] > 1:
							agent_action_list[agents_BFraming].belieftree[1 + agents.unique_id][cw_of_interest[best_BFraming]][0] = 1
						if agent_action_list[agents_BFraming].belieftree[1 + agents.unique_id][cw_of_interest[best_BFraming]][0] < -1:
							agent_action_list[agents_BFraming].belieftree[1 + agents.unique_id][cw_of_interest[best_BFraming]][0] = -1

				agents.resources_actions_BFraming -= agents.resources[0] * 0.1
				agents.resources_actions -= agents.resources[0] * 0.1

		# 2. Electorate influence, grading of actions and implementation of the best actions until resources run out 
		# 50% of the resources (from actions)
		while agents.resources_actions_EInfluence > 0.001:

			actions_EP_grades_EInfluence = []
			# FIRST - Calculation of the best option
			for issue_num in range(len_DC + len_PC):
				actions_EP_grades_EInfluence_ind = []
				# Going through all agents that are electorate from the master_list
				agents_electorate = []
				for agents_run in master_list:
					if type(agents_run) == Electorate:
						agents_electorate.append(agents_run)

				for agents_el in agents_electorate:

					# Setting grade to 0 if the external party has no interest in the issue:
					if agents.belieftree[0][issue_num][0] == 'No':
						issue_num_grade	 = 0 

					# Calculate a grade if the external party has an interest in the issue
					else:
						# Memorising the original belief values
						original_belief = [0,0,0]
						original_belief[0] = copy.copy(agents_el.belieftree_electorate[issue_num][0])
						original_belief[1] = copy.copy(agents_el.belieftree_electorate[issue_num][1])
						original_belief[2] = copy.copy(agents_el.belieftree_electorate[issue_num][2])

						if agents.affiliation == agents_el.affiliation:
							# Perfoming the action
							agents_el.belieftree_electorate[issue_num][1] += (agents.belieftree[0][issue_num][1] - agents_el.belieftree_electorate[issue_num][1]) \
								* agents.resources[0] * 0.1 / electorate_number
							# Update of the preference
							self.preference_udapte_electorate(agents_el, len_DC, len_PC, len_S)
							# Calculation of the new gradec
							issue_num_grade = abs(agents.belieftree[0][issue_num][2] - agents_el.belieftree_electorate[issue_num][2])

						# Affiliation 1 and 2
						if (agents.affiliation == 0 and agents_el.affiliation == 1) or (agents.affiliation == 1 and agents_el.affiliation == 0):
							# Perfoming the action
							agents_el.belieftree_electorate[issue_num][1] += (agents.belieftree[0][issue_num][1] - agents_el.belieftree_electorate[issue_num][1]) \
								* agents.resources[0] * 0.1 * affiliation_weights[0] / electorate_number
							# Update of the preference
							self.preference_udapte_electorate(agents_el, len_DC, len_PC, len_S)
							# Calculation of the new gradec
							issue_num_grade = abs(agents.belieftree[0][issue_num][2] - agents_el.belieftree_electorate[issue_num][2])

						# Affiliation 1 and 3
						if (agents.affiliation == 0 and agents_el.affiliation == 2) or (agents.affiliation == 2 and agents_el.affiliation == 0):
							# Perfoming the action
							agents_el.belieftree_electorate[issue_num][1] += (agents.belieftree[0][issue_num][1] - agents_el.belieftree_electorate[issue_num][1]) \
								* agents.resources[0] * 0.1 * affiliation_weights[1] / electorate_number
							# Update of the preference
							self.preference_udapte_electorate(agents_el, len_DC, len_PC, len_S)
							# Calculation of the new gradec
							issue_num_grade = abs(agents.belieftree[0][issue_num][2] - agents_el.belieftree_electorate[issue_num][2])

						# Affiliation 2 and 3
						if (agents.affiliation == 1 and agents_el.affiliation == 2) or (agents.affiliation == 2 and agents_el.affiliation == 1):
							# Perfoming the action
							agents_el.belieftree_electorate[issue_num][1] += (agents.belieftree[0][issue_num][1] - agents_el.belieftree_electorate[issue_num][1]) \
								* agents.resources[0] * 0.1 * affiliation_weights[2] / electorate_number
							# Update of the preference
							self.preference_udapte_electorate(agents_el, len_DC, len_PC, len_S)
							# Calculation of the new grade
							issue_num_grade = abs(agents.belieftree[0][issue_num][2] - agents_el.belieftree_electorate[issue_num][2])

						# Restoring the initial values
						agents_el.belieftree_electorate[issue_num][0] = original_belief[0]
						agents_el.belieftree_electorate[issue_num][1] = original_belief[1]
						agents_el.belieftree_electorate[issue_num][2] = original_belief[2]


						# Re-updating the preference levels
						self.preference_udapte_electorate(agents_el, len_DC, len_PC, len_S)

					actions_EP_grades_EInfluence_ind.append(issue_num_grade)

				actions_EP_grades_EInfluence.append(sum(actions_EP_grades_EInfluence_ind))

			# Choose the action that leads to the minimum amount of difference between the EP and the electorates
			best_EInfluence = actions_EP_grades_EInfluence.index(min(actions_EP_grades_EInfluence))
			
			# SECOND - Changing the aims of all the agents for the best choice
			for agents_el in agents_electorate:


				if agents.affiliation == agents_el.affiliation:
					agents_el.belieftree_electorate[best_EInfluence][1] += (agents.belieftree[0][best_EInfluence][1] - agents_el.belieftree_electorate[best_EInfluence][1]) \
					* agents.resources[0] * 0.1 / electorate_number

				# Affiliation 1 and 2
				if (agents.affiliation == 0 and agents_el.affiliation == 1) or (agents.affiliation == 1 and agents_el.affiliation == 0):
					agents_el.belieftree_electorate[best_EInfluence][1] += (agents.belieftree[0][best_EInfluence][1] - agents_el.belieftree_electorate[best_EInfluence][1]) \
					* agents.resources[0] * 0.1 * affiliation_weights[0] / electorate_number

					# Affiliation 1 and 3
				if (agents.affiliation == 0 and agents_el.affiliation == 2) or (agents.affiliation == 2 and agents_el.affiliation == 0):
					agents_el.belieftree_electorate[best_EInfluence][1] += (agents.belieftree[0][best_EInfluence][1] - agents_el.belieftree_electorate[best_EInfluence][1]) \
					* agents.resources[0] * 0.1 * affiliation_weights[1] / electorate_number

				# Affiliation 2 and 3
				if (agents.affiliation == 1 and agents_el.affiliation == 2) or (agents.affiliation == 2 and agents_el.affiliation == 1):
					agents_el.belieftree_electorate[best_EInfluence][1] += (agents.belieftree[0][best_EInfluence][1] - agents_el.belieftree_electorate[best_EInfluence][1]) \
					* agents.resources[0] * 0.1 * affiliation_weights[2] / electorate_number

				# 1-1 check
				agents_el.belieftree_electorate[best_EInfluence][1] = \
					self.one_minus_one_check2(agents_el.belieftree_electorate[best_EInfluence][1])

				# Re-updating the preference levels
				self.preference_udapte_electorate(agents_el, len_DC, len_PC, len_S)

			agents.resources_actions_EInfluence -= agents.resources[0] * 0.1
			agents.resources_actions -= agents.resources[0] * 0.1

	def external_parties_actions_pf(self, agents, agent_action_list, causalrelation_number, \
		affiliation_weights, deep_core, policy_core, secondary, electorate_number, action_agent_number, agenda_as_issue, instruments, master_list):

		"""
		External party actions function for the policy formulation
		===========================

		The description here is currently missing.

		"""

		len_DC = len(deep_core)
		len_PC = len(policy_core)
		len_S = len(secondary)

		# Here are the modifications related to the policy formulation
		# Looking for the relevant causal relations for the policy formulation
		cw_of_interest = []
		# We only consider the causal relations related to the issue on the agenda
		print(agents.select_pinstrument)
		for cw_choice in range(len(secondary)):
			# Index explanation - pass all issues, then all causal relations related to the PC-DC links, then reach the links related to the issue on the agenda
			if agents.belieftree[0][len_DC + len_PC + len_S + (len_DC * len_PC) + (agenda_as_issue - len_DC)*len_S + cw_choice][0] \
				* instruments[agents.select_pinstrument][cw_choice] != 0:
				cw_of_interest.append(len_DC + len_PC + len_S + (len_DC * len_PC) + (agenda_as_issue - len_DC)*len_S + cw_choice)

		
		# Looking for the relevant issues for the policy formulation
		# That is we choose the secondary issues that are impacted by the policy instrument
		# that the agent has selected.
		issue_of_interest = []
		for issue_choice in range(len(secondary)):
			if instruments[agents.select_pinstrument][issue_choice] != 0:
				issue_of_interest.append(len_DC + len_PC + issue_choice)

		# Original agenda setting action loop with slight modifications
		agents.resources_actions_BFraming = agents.resources_actions * 0.5
		agents.resources_actions_EInfluence = agents.resources_actions * 0.5
		# 1. Blanket framing, grading of actions and implementation of the best actions until resources run out 
		# 50% of the resources (from actions)
		if len(cw_of_interest) > 0:
			while agents.resources_actions_BFraming > 0.001:
				# FIRST - Calculation of the best option
				# Estimating the grades of the changes in the causal relations - Based on partial knowledge:
				actions_EP_grades_BFraming = []
				# print('Length: ' + str(len(cw_of_interest)))
				for cw in range(len(cw_of_interest)):
					# Go through each of the agents
					actions_EP_grades_BFraming_ind = []

					for agents_BFraming in range(len(agent_action_list)):
						# Making sure that the agent does not count itself
						if agents != agent_action_list[agents_BFraming]:
							# Calculate the impact of the framing depending on affiliations:
							# WATCH OUT - The agent action list is not ordered, it is therefore paramount to select based on unique_id and not on item number in the list!!
							# This warning only applies when looking for the partial knowledge beliefs in the belief tree of the original agent.
							# Same affiliation

							# Check if no partial knowledge (initial value)
							check_none = 0
							if agents.belieftree[1 + agent_action_list[agents_BFraming].unique_id][cw_of_interest[cw]][0] == None:
								check_none = 1
								agents.belieftree[1 + agent_action_list[agents_BFraming].unique_id][cw_of_interest[cw]][0] = 0

							# Same affiliation
							if agents.affiliation == agent_action_list[agents_BFraming].affiliation:
								cw_grade = abs((agents.belieftree[0][cw_of_interest[cw]][0] - \
								agents.belieftree[1 + agent_action_list[agents_BFraming].unique_id][cw_of_interest[cw]][0]) * \
								agents.resources[0] * 0.1 / (action_agent_number - 1))


							# Affiliation 1 and 2
							if (agents.affiliation == 0 and agent_action_list[agents_BFraming].affiliation == 1) or \
								(agents.affiliation == 1 and agent_action_list[agents_BFraming].affiliation == 0):
								cw_grade = abs((agents.belieftree[0][cw_of_interest[cw]][0] - \
								agents.belieftree[1 + agent_action_list[agents_BFraming].unique_id][cw_of_interest[cw]][0]) * \
								agents.resources[0] * 0.1 * affiliation_weights[0] / (action_agent_number - 1))

							# Affiliation 1 and 3
							if (agents.affiliation == 0 and agent_action_list[agents_BFraming].affiliation == 2) or \
								(agents.affiliation == 2 and agent_action_list[agents_BFraming].affiliation == 0):
								cw_grade = abs((agents.belieftree[0][cw_of_interest[cw]][0] - \
								agents.belieftree[1 + agent_action_list[agents_BFraming].unique_id][cw_of_interest[cw]][0]) * \
								agents.resources[0] * 0.1 * affiliation_weights[1] / (action_agent_number - 1) )

							# Affiliation 2 and 3
							if (agents.affiliation == 1 and agent_action_list[agents_BFraming].affiliation == 2) or \
								(agents.affiliation == 2 and agent_action_list[agents_BFraming].affiliation == 1):
								cw_grade = abs((agents.belieftree[0][cw_of_interest[cw]][0] - \
								agents.belieftree[1 + agent_action_list[agents_BFraming].unique_id][cw_of_interest[cw]][0]) * \
								agents.resources[0] * 0.1 * affiliation_weights[2] / (action_agent_number - 1))

							if check_none == 1:
								agents.belieftree[1 + agent_action_list[agents_BFraming].unique_id][cw_of_interest[cw]][0] = None

							actions_EP_grades_BFraming_ind.append(cw_grade)
						# If it is the same agent, then rate the action as 0 (important for appropriate indexing)
						else:
							cw_grade = 0
							actions_EP_grades_BFraming_ind.append(cw_grade)

					actions_EP_grades_BFraming.append(sum(actions_EP_grades_BFraming_ind))

				# Finding the index of the causal relation most affected based on the partial knowledge
				best_BFraming = actions_EP_grades_BFraming.index(max(actions_EP_grades_BFraming)) 

				# SECOND - Changing the causal relations of all the agents - Based on actual beliefs:
				for agents_BFraming in range(len(agent_action_list)):
					# Making sure that the agent does not count itself
					if agents != agent_action_list[agents_BFraming]:

						# Same affiliation
						if agents.affiliation == agent_action_list[agents_BFraming].affiliation:
							agent_action_list[agents_BFraming].belieftree[0][cw_of_interest[best_BFraming]][0] += \
							(agents.belieftree[0][cw_of_interest[best_BFraming]][0] - \
							agent_action_list[agents_BFraming].belieftree[0][cw_of_interest[best_BFraming]][0]) * \
							agents.resources[0] * 0.1 / (action_agent_number - 1)
						
						# Affiliation 1 and 2
						if (agents.affiliation == 0 and agent_action_list[agents_BFraming].affiliation == 1) or \
		    			  (agents.affiliation == 1 and agent_action_list[agents_BFraming].affiliation == 0):
							agent_action_list[agents_BFraming].belieftree[0][cw_of_interest[best_BFraming]][0] += \
							(agents.belieftree[0][cw_of_interest[best_BFraming]][0] - \
							agent_action_list[agents_BFraming].belieftree[0][cw_of_interest[best_BFraming]][0]) * \
							agents.resources[0] * 0.1 * affiliation_weights[0] / (action_agent_number - 1)
						
						# Affiliation 1 and 3
						if (agents.affiliation == 0 and agent_action_list[agents_BFraming].affiliation == 2) or \
						  (agents.affiliation == 2 and agent_action_list[agents_BFraming].affiliation == 0):
							agent_action_list[agents_BFraming].belieftree[0][cw_of_interest[best_BFraming]][0] += \
							(agents.belieftree[0][cw_of_interest[best_BFraming]][0] - \
							agent_action_list[agents_BFraming].belieftree[0][cw_of_interest[best_BFraming]][0]) * \
							agents.resources[0] * 0.1 * affiliation_weights[1] / (action_agent_number - 1)
						
						# Affiliation 2 and 3
						if (agents.affiliation == 1 and agent_action_list[agents_BFraming].affiliation == 2) or \
						 (agents.affiliation == 2 and agent_action_list[agents_BFraming].affiliation == 1):
							agent_action_list[agents_BFraming].belieftree[0][cw_of_interest[best_BFraming]][0] += \
							(agents.belieftree[0][cw_of_interest[best_BFraming]][0] - \
							agent_action_list[agents_BFraming].belieftree[0][cw_of_interest[best_BFraming]][0]) * \
							agents.resources[0] * 0.1 * affiliation_weights[2] / (action_agent_number - 1)

						# Check that it is not higher than 1 or lower than -1
						agent_action_list[agents_BFraming].belieftree[0][cw_of_interest[best_BFraming]][0] = \
							self.one_minus_one_check2(agent_action_list[agents_BFraming].belieftree[0][cw_of_interest[best_BFraming]][0])

						# Providing partial knowledge - Blanket framing - 0.5 range from real value: (Acting agent)
						agents.belieftree[1 + agent_action_list[agents_BFraming].unique_id][cw_of_interest[best_BFraming]][0] = \
							agent_action_list[agents_BFraming].belieftree[0][cw_of_interest[best_BFraming]][0] + (random.random()/2) - 0.25
						# 1-1 check
						agents.belieftree[1 + agent_action_list[agents_BFraming].unique_id][cw_of_interest[best_BFraming]][0] = \
							self.one_minus_one_check2(agents.belieftree[1 + agent_action_list[agents_BFraming].unique_id][cw_of_interest[best_BFraming]][0])
						# Providing partial knowledge - Blanket framing - 0.5 range from real value: (Acted upon agent)
						agent_action_list[agents_BFraming].belieftree[1 + agents.unique_id][cw_of_interest[best_BFraming]][0] = \
							agents.belieftree[0][cw_of_interest[best_BFraming]][0] + (random.random()/2) - 0.25
						# 1-1 check
						agent_action_list[agents_BFraming].belieftree[1 + agents.unique_id][cw_of_interest[best_BFraming]][0] = \
							self.one_minus_one_check2(agent_action_list[agents_BFraming].belieftree[1 + agents.unique_id][cw_of_interest[best_BFraming]][0])

				agents.resources_actions_BFraming -= agents.resources[0] * 0.1
				agents.resources_actions -= agents.resources[0] * 0.1


		# 2. Electorate influence, grading of actions and implementation of the best actions until resources run out 
		# 50% of the resources (from actions)
		while agents.resources_actions_EInfluence > 0.001:
			actions_EP_grades_EInfluence = []
			# FIRST - Calculation of the best option
			for issue_num in range(len(issue_of_interest)):
				actions_EP_grades_EInfluence_ind = []
				# Going through all agents that are electorate from the master_list
				agents_electorate = []
				for agents_run in master_list:
					if type(agents_run) == Electorate:
						agents_electorate.append(agents_run)

				for agents_el in agents_electorate:

					# Setting grade to 0 if the external party has no interest in the issue:
					if agents.belieftree[0][issue_of_interest[issue_num]][0] == 'No':
						issue_num_grade	 = 0 

					# Calculate a grade if the external party has an interest in the issue
					else:
						if agents.affiliation == agents_el.affiliation:
							issue_num_grade = abs((agents.belieftree[0][issue_of_interest[issue_num]][1] - agents_el.belieftree_electorate[issue_of_interest[issue_num]][1]) * \
								agents.resources[0] * 0.1 / electorate_number)

						# Affiliation 1 and 2
						if (agents.affiliation == 0 and agents_el.affiliation == 1) or (agents.affiliation == 1 and agents_el.affiliation == 0):
							issue_num_grade = abs((agents.belieftree[0][issue_of_interest[issue_num]][1] - agents_el.belieftree_electorate[issue_of_interest[issue_num]][1]) * \
								agents.resources[0] * 0.1 * affiliation_weights[0] / electorate_number * affiliation_weights[0])

						# Affiliation 1 and 3
						if (agents.affiliation == 0 and agents_el.affiliation == 2) or (agents.affiliation == 2 and agents_el.affiliation == 0):
							issue_num_grade = abs((agents.belieftree[0][issue_of_interest[issue_num]][1] - agents_el.belieftree_electorate[issue_of_interest[issue_num]][1]) * \
								agents.resources[0] * 0.1 * affiliation_weights[1] / electorate_number * affiliation_weights[1])

						# Affiliation 2 and 3
						if (agents.affiliation == 1 and agents_el.affiliation == 2) or (agents.affiliation == 2 and agents_el.affiliation == 1):
							issue_num_grade = abs((agents.belieftree[0][issue_of_interest[issue_num]][1] - agents_el.belieftree_electorate[issue_of_interest[issue_num]][1]) * \
								agents.resources[0] * 0.1 * affiliation_weights[2] / electorate_number )

						# Restoring the initial values

					actions_EP_grades_EInfluence_ind.append(issue_num_grade)

				actions_EP_grades_EInfluence.append(sum(actions_EP_grades_EInfluence_ind))

			best_EInfluence = actions_EP_grades_EInfluence.index(max(actions_EP_grades_EInfluence))
			
			# SECOND - Changing the aims of all the agents for the best choice
			for agents_el in agents_electorate:

				if agents.affiliation == agents_el.affiliation:
					agents_el.belieftree_electorate[issue_of_interest[best_EInfluence]][1] += (agents.belieftree[0][issue_of_interest[best_EInfluence]][1] - agents_el.belieftree_electorate[issue_of_interest[best_EInfluence]][1]) \
					* agents.resources[0] * 0.1 / electorate_number

				# Affiliation 1 and 2
				if (agents.affiliation == 0 and agents_el.affiliation == 1) or (agents.affiliation == 1 and agents_el.affiliation == 0):
					agents_el.belieftree_electorate[issue_of_interest[best_EInfluence]][1] += (agents.belieftree[0][issue_of_interest[best_EInfluence]][1] - agents_el.belieftree_electorate[issue_of_interest[best_EInfluence]][1]) \
					* agents.resources[0] * 0.1 * affiliation_weights[0] / electorate_number

					# Affiliation 1 and 3
				if (agents.affiliation == 0 and agents_el.affiliation == 2) or (agents.affiliation == 2 and agents_el.affiliation == 0):
					agents_el.belieftree_electorate[issue_of_interest[best_EInfluence]][1] += (agents.belieftree[0][issue_of_interest[best_EInfluence]][1] - agents_el.belieftree_electorate[issue_of_interest[best_EInfluence]][1]) \
					* agents.resources[0] * 0.1 * affiliation_weights[1] / electorate_number

				# Affiliation 2 and 3
				if (agents.affiliation == 1 and agents_el.affiliation == 2) or (agents.affiliation == 2 and agents_el.affiliation == 1):
					agents_el.belieftree_electorate[issue_of_interest[best_EInfluence]][1] += (agents.belieftree[0][issue_of_interest[best_EInfluence]][1] - agents_el.belieftree_electorate[issue_of_interest[best_EInfluence]][1]) \
					* agents.resources[0] * 0.1 * affiliation_weights[2] / electorate_number

				# Check for max and min:
				agents_el.belieftree_electorate[issue_of_interest[best_EInfluence]][1] = \
					self.one_minus_one_check2(agents_el.belieftree_electorate[issue_of_interest[best_EInfluence]][1])

			agents.resources_actions_EInfluence -= agents.resources[0] * 0.1
			agents.resources_actions -= agents.resources[0] * 0.1

	def external_parties_actions_as_3S(self, agents, agent_action_list, causalrelation_number, \
		affiliation_weights, deep_core, policy_core, secondary, electorate_number, action_agent_number, master_list):

		len_DC = len(deep_core)
		len_PC = len(policy_core)
		len_S = len(secondary)

		cw_of_interest = []
		# We only consider the causal relations related to the problem on the agenda
		for cw_choice in range(len(deep_core)):
				cw_of_interest.append(len_DC + len_PC + len_S + (agents.select_problem_3S_as - len_DC) + cw_choice * len(policy_core))

		agents.resources_actions_BFraming = agents.resources_actions * 0.5
		agents.resources_actions_EInfluence = agents.resources_actions * 0.5
		# 1. Blanket framing, grading of actions and implementation of the best actions until resources run out 

		# If the team is advocating for a problem, the following tasks are completed
		if agents.select_issue_3S_as == 'problem':

			# 50% of the resources (from actions)
			while agents.resources_actions_BFraming > 0.001:
				# FIRST - Calculation of the best option
				# Estimating the grades of the changes in the causal relations - Based on partial knowledge:
				actions_EP_grades_BFraming = []
				for cw in range(len(cw_of_interest)):
					# Go through each of the agents
					actions_EP_grades_BFraming_ind = []

					for agents_BFraming in range(len(agent_action_list)):
						# Making sure that the agent does not count itself
						if agents != agent_action_list[agents_BFraming]:

							# Calculate the impact of the framing depending on affiliations:
							# WATCH OUT - The agent action list is not ordered, it is therefore paramount to select based on unique_id and not on item number in the list!!
							# This warning only applies when looking for the partial knowledge beliefs in the belief tree of the original agent.
							# Same affiliation

							# Check if no partial knowledge (initial value)
							check_none = 0
							if agents.belieftree[1 + agent_action_list[agents_BFraming].unique_id][cw_of_interest[cw]][0] == None:
								check_none = 1
								agents.belieftree[1 + agent_action_list[agents_BFraming].unique_id][cw_of_interest[cw]][0] = 0
							
							if agents.affiliation == agent_action_list[agents_BFraming].affiliation:
								cw_grade = abs((agents.belieftree[0][cw_of_interest[cw]][0] - \
								agents.belieftree[1 + agent_action_list[agents_BFraming].unique_id][cw_of_interest[cw]][0]) * \
								agents.resources[0] * 0.1 / (action_agent_number - 1))

							# Affiliation 1 and 2
							if (agents.affiliation == 0 and agent_action_list[agents_BFraming].affiliation == 1) or \
			    			  (agents.affiliation == 1 and agent_action_list[agents_BFraming].affiliation == 0):
								cw_grade = abs((agents.belieftree[0][cw_of_interest[cw]][0] - \
								agents.belieftree[1 + agent_action_list[agents_BFraming].unique_id][cw_of_interest[cw]][0]) * \
								agents.resources[0] * 0.1 * affiliation_weights[0] / (action_agent_number - 1))

							# Affiliation 1 and 3
							if (agents.affiliation == 0 and agent_action_list[agents_BFraming].affiliation == 2) or \
							  (agents.affiliation == 2 and agent_action_list[agents_BFraming].affiliation == 0):
								cw_grade = abs((agents.belieftree[0][cw_of_interest[cw]][0] - \
								agents.belieftree[1 + agent_action_list[agents_BFraming].unique_id][cw_of_interest[cw]][0]) * \
								agents.resources[0] * 0.1 * affiliation_weights[1] / (action_agent_number - 1))

							# Affiliation 2 and 3
							if (agents.affiliation == 1 and agent_action_list[agents_BFraming].affiliation == 2) or \
							 (agents.affiliation == 2 and agent_action_list[agents_BFraming].affiliation == 1):
								cw_grade = abs((agents.belieftree[0][cw_of_interest[cw]][0] - \
								agents.belieftree[1 + agent_action_list[agents_BFraming].unique_id][cw_of_interest[cw]][0]) * \
								agents.resources[0] * 0.1 * affiliation_weights[2] / (action_agent_number - 1))

							# Reset the value after finding the grade
							if check_none == 1:
								agents.belieftree[1 + agent_action_list[agents_BFraming].unique_id][cw_of_interest[cw]][0] = None
							
							actions_EP_grades_BFraming_ind.append(cw_grade)
						# If it is the same agent, then rate the action as 0 (important for appropriate indexing)
						else:
							cw_grade = 0
							actions_EP_grades_BFraming_ind.append(cw_grade)

					actions_EP_grades_BFraming.append(sum(actions_EP_grades_BFraming_ind))

				# Finding the index of the causal relation most affected based on the partial knowledge
				best_BFraming = actions_EP_grades_BFraming.index(max(actions_EP_grades_BFraming))

				# SECOND - Changing the causal relations of all the agents - Based on actual beliefs:
				for agents_BFraming in range(len(agent_action_list)):
					# Making sure that the agent does not count itself
					if agents != agent_action_list[agents_BFraming]:

						# Same affiliation
						if agents.affiliation == agent_action_list[agents_BFraming].affiliation:
							agent_action_list[agents_BFraming].belieftree[0][cw_of_interest[best_BFraming]][0] += \
							(agents.belieftree[0][cw_of_interest[best_BFraming]][0] - \
							agent_action_list[agents_BFraming].belieftree[0][cw_of_interest[best_BFraming]][0]) * \
							agents.resources[0] * 0.1 / (action_agent_number - 1)
						
						# Affiliation 1 and 2
						if (agents.affiliation == 0 and agent_action_list[agents_BFraming].affiliation == 1) or \
		    			  (agents.affiliation == 1 and agent_action_list[agents_BFraming].affiliation == 0):
							agent_action_list[agents_BFraming].belieftree[0][cw_of_interest[best_BFraming]][0] += \
							(agents.belieftree[0][cw_of_interest[best_BFraming]][0] - \
							agent_action_list[agents_BFraming].belieftree[0][cw_of_interest[best_BFraming]][0]) * \
							agents.resources[0] * 0.1 * affiliation_weights[0] / (action_agent_number - 1)
						
						# Affiliation 1 and 3
						if (agents.affiliation == 0 and agent_action_list[agents_BFraming].affiliation == 2) or \
						  (agents.affiliation == 2 and agent_action_list[agents_BFraming].affiliation == 0):
							agent_action_list[agents_BFraming].belieftree[0][cw_of_interest[best_BFraming]][0] += \
							(agents.belieftree[0][cw_of_interest[best_BFraming]][0] - \
							agent_action_list[agents_BFraming].belieftree[0][cw_of_interest[best_BFraming]][0]) * \
							agents.resources[0] * 0.1 * affiliation_weights[1] / (action_agent_number - 1)
						
						# Affiliation 2 and 3
						if (agents.affiliation == 1 and agent_action_list[agents_BFraming].affiliation == 2) or \
						 (agents.affiliation == 2 and agent_action_list[agents_BFraming].affiliation == 1):
							agent_action_list[agents_BFraming].belieftree[0][cw_of_interest[best_BFraming]][0] += \
							(agents.belieftree[0][cw_of_interest[best_BFraming]][0] - \
							agent_action_list[agents_BFraming].belieftree[0][cw_of_interest[best_BFraming]][0]) * \
							agents.resources[0] * 0.1 * affiliation_weights[2] / (action_agent_number - 1)

						# Check that it is not higher than 1 or lower than -1
						if agent_action_list[agents_BFraming].belieftree[0][cw_of_interest[best_BFraming]][0] > 1:
							agent_action_list[agents_BFraming].belieftree[0][cw_of_interest[best_BFraming]][0] = 1
						if agent_action_list[agents_BFraming].belieftree[0][cw_of_interest[best_BFraming]][0] < -1:
							agent_action_list[agents_BFraming].belieftree[0][cw_of_interest[best_BFraming]][0] = -1

						# Providing partial knowledge - Blanket framing - 0.5 range from real value: (Acting agent)
						agents.belieftree[1 + agent_action_list[agents_BFraming].unique_id][cw_of_interest[best_BFraming]][0] = \
							agent_action_list[agents_BFraming].belieftree[0][cw_of_interest[best_BFraming]][0] + (random.random()/2) - 0.25
						# 1-1 check
						if agents.belieftree[1 + agent_action_list[agents_BFraming].unique_id][cw_of_interest[best_BFraming]][0] > 1:
							agents.belieftree[1 + agent_action_list[agents_BFraming].unique_id][cw_of_interest[best_BFraming]][0] = 1
						if agents.belieftree[1 + agent_action_list[agents_BFraming].unique_id][cw_of_interest[best_BFraming]][0] < -1:
							agents.belieftree[1 + agent_action_list[agents_BFraming].unique_id][cw_of_interest[best_BFraming]][0] = -1
						# Providing partial knowledge - Blanket framing - 0.5 range from real value: (Acted upon agent)
						agent_action_list[agents_BFraming].belieftree[1 + agents.unique_id][cw_of_interest[best_BFraming]][0] = \
							agents.belieftree[0][cw_of_interest[best_BFraming]][0] + (random.random()/2) - 0.25
						# 1-1 check
						if agent_action_list[agents_BFraming].belieftree[1 + agents.unique_id][cw_of_interest[best_BFraming]][0] > 1:
							agent_action_list[agents_BFraming].belieftree[1 + agents.unique_id][cw_of_interest[best_BFraming]][0] = 1
						if agent_action_list[agents_BFraming].belieftree[1 + agents.unique_id][cw_of_interest[best_BFraming]][0] < -1:
							agent_action_list[agents_BFraming].belieftree[1 + agents.unique_id][cw_of_interest[best_BFraming]][0] = -1

				agents.resources_actions_BFraming -= agents.resources[0] * 0.1
				agents.resources_actions -= agents.resources[0] * 0.1

		# If the team is advocating for a policy, the following tasks are completed
		if agents.select_issue_3S_as == 'policy':

			# 2. Electorate influence, grading of actions and implementation of the best actions until resources run out 
			# 50% of the resources (from actions)
			while agents.resources_actions_EInfluence > 0.001:
				actions_EP_grades_EInfluence = []
				# FIRST - Calculation of the best option
				for issue_num in range(len_DC + len_PC):
					actions_EP_grades_EInfluence_ind = []
					# Going through all agents that are electorate from the master_list
					agents_electorate = []
					for agents_run in master_list:
						if type(agents) == Electorate:
							agents_electorate.append(agents_run)

					for agents_el in agents_electorate:

						# Setting grade to 0 if the external party has no interest in the issue:
						if agents.belieftree[0][issue_num][0] == 'No':
							issue_num_grade	 = 0 

						# Calculate a grade if the external party has an interest in the issue
						else:

							# Memorising the original belief values
							original_belief = [0,0,0]
							original_belief[0] = copy.copy(agents_el.belieftree_electorate[issue_num][0])
							original_belief[1] = copy.copy(agents_el.belieftree_electorate[issue_num][1])
							original_belief[2] = copy.copy(agents_el.belieftree_electorate[issue_num][2])

							if agents.affiliation == agents_el.affiliation:
								# Perfoming the action
								agents_el.belieftree_electorate[issue_num][1] += (agents.belieftree[0][issue_num][1] - agents_el.belieftree_electorate[issue_num][1]) \
									* agents.resources[0] * 0.1 / electorate_number
								# Update of the preference
								self.preference_udapte_electorate(agents_el, len_DC, len_PC, len_S)
								# Calculation of the new gradec
								issue_num_grade = abs(agents.belieftree[0][issue_num][2] - agents_el.belieftree_electorate[issue_num][2])

							# Affiliation 1 and 2
							if (agents.affiliation == 0 and agents_el.affiliation == 1) or (agents.affiliation == 1 and agents_el.affiliation == 0):
								# Perfoming the action
								agents_el.belieftree_electorate[issue_num][1] += (agents.belieftree[0][issue_num][1] - agents_el.belieftree_electorate[issue_num][1]) \
									* agents.resources[0] * 0.1 * affiliation_weights[0] / electorate_number
								# Update of the preference
								self.preference_udapte_electorate(agents_el, len_DC, len_PC, len_S)
								# Calculation of the new gradec
								issue_num_grade = abs(agents.belieftree[0][issue_num][2] - agents_el.belieftree_electorate[issue_num][2])

							# Affiliation 1 and 3
							if (agents.affiliation == 0 and agents_el.affiliation == 2) or (agents.affiliation == 2 and agents_el.affiliation == 0):
								# Perfoming the action
								agents_el.belieftree_electorate[issue_num][1] += (agents.belieftree[0][issue_num][1] - agents_el.belieftree_electorate[issue_num][1]) \
									* agents.resources[0] * 0.1 * affiliation_weights[1] / electorate_number
								# Update of the preference
								self.preference_udapte_electorate(agents_el, len_DC, len_PC, len_S)
								# Calculation of the new gradec
								issue_num_grade = abs(agents.belieftree[0][issue_num][2] - agents_el.belieftree_electorate[issue_num][2])

							# Affiliation 2 and 3
							if (agents.affiliation == 1 and agents_el.affiliation == 2) or (agents.affiliation == 2 and agents_el.affiliation == 1):
								# Perfoming the action
								agents_el.belieftree_electorate[issue_num][1] += (agents.belieftree[0][issue_num][1] - agents_el.belieftree_electorate[issue_num][1]) \
									* agents.resources[0] * 0.1 * affiliation_weights[2] / electorate_number
								# Update of the preference
								self.preference_udapte_electorate(agents_el, len_DC, len_PC, len_S)
								# Calculation of the new grade
								issue_num_grade = abs(agents.belieftree[0][issue_num][2] - agents_el.belieftree_electorate[issue_num][2])

							# Restoring the initial values
							agents_el.belieftree_electorate[issue_num][0] = original_belief[0]
							agents_el.belieftree_electorate[issue_num][1] = original_belief[1]
							agents_el.belieftree_electorate[issue_num][2] = original_belief[2]


							# Re-updating the preference levels
							self.preference_udapte_electorate(agents_el, len_DC, len_PC, len_S)

						actions_EP_grades_EInfluence_ind.append(issue_num_grade)

					actions_EP_grades_EInfluence.append(sum(actions_EP_grades_EInfluence_ind))

				# Choose the action that leads to the minimum amount of difference between the EP and the electorates
				best_EInfluence = actions_EP_grades_EInfluence.index(min(actions_EP_grades_EInfluence))
				
				# SECOND - Changing the aims of all the agents for the best choice
				for agents_el in agents_electorate:

					if agents.affiliation == agents_el.affiliation:
						agents_el.belieftree_electorate[best_EInfluence][1] += (agents.belieftree[0][best_EInfluence][1] - agents_el.belieftree_electorate[best_EInfluence][1]) \
						* agents.resources[0] * 0.1 / electorate_number

					# Affiliation 1 and 2
					if (agents.affiliation == 0 and agents_el.affiliation == 1) or (agents.affiliation == 1 and agents_el.affiliation == 0):
						agents_el.belieftree_electorate[best_EInfluence][1] += (agents.belieftree[0][best_EInfluence][1] - agents_el.belieftree_electorate[best_EInfluence][1]) \
						* agents.resources[0] * 0.1 * affiliation_weights[0] / electorate_number

						# Affiliation 1 and 3
					if (agents.affiliation == 0 and agents_el.affiliation == 2) or (agents.affiliation == 2 and agents_el.affiliation == 0):
						agents_el.belieftree_electorate[best_EInfluence][1] += (agents.belieftree[0][best_EInfluence][1] - agents_el.belieftree_electorate[best_EInfluence][1]) \
						* agents.resources[0] * 0.1 * affiliation_weights[1] / electorate_number

					# Affiliation 2 and 3
					if (agents.affiliation == 1 and agents_el.affiliation == 2) or (agents.affiliation == 2 and agents_el.affiliation == 1):
						agents_el.belieftree_electorate[best_EInfluence][1] += (agents.belieftree[0][best_EInfluence][1] - agents_el.belieftree_electorate[best_EInfluence][1]) \
						* agents.resources[0] * 0.1 * affiliation_weights[2] / electorate_number

					# 1-1 check
					agents_el.belieftree_electorate[best_EInfluence][1] = \
						self.one_minus_one_check2(agents_el.belieftree_electorate[best_EInfluence][1])

					# Re-updating the preference levels
					self.preference_udapte_electorate(agents_el, len_DC, len_PC, len_S)

				agents.resources_actions_EInfluence -= agents.resources[0] * 0.1
				agents.resources_actions -= agents.resources[0] * 0.1

	def external_parties_actions_pf_3S(self, agents, agent_action_list, causalrelation_number, \
		affiliation_weights, deep_core, policy_core, secondary, electorate_number, action_agent_number, master_list, agenda_prob_3S_as):

		len_DC = len(deep_core)
		len_PC = len(policy_core)
		len_S = len(secondary)

		agents.resources_actions_BFraming = agents.resources_actions * 0.5
		agents.resources_actions_EInfluence = agents.resources_actions * 0.5
		# 1. Blanket framing, grading of actions and implementation of the best actions until resources run out 

		# Selection of the cw of interest
		cw_of_interest = []
		# Select one by one the DC
		j = agenda_prob_3S_as
		# for j in range(len_PC):
		# Selecting the causal relations starting from DC
		for k in range(len_S):
			# Contingency for partial knowledge issues
			# print(len_DC + len_PC + len_S + len_PC*len_DC + (j-len_DC) + k*len_PC)
			if (agents.belieftree[0][len_DC + len_PC + len_S + len_PC*len_DC + (j-len_DC) + k*len_PC][0] < 0 and (agents.belieftree[0][j][1] - agents.belieftree[0][j][0]) < 0) \
			  or (agents.belieftree[0][len_DC + len_PC + len_S + len_PC*len_DC + (j-len_DC) + k*len_PC][0] > 0 and (agents.belieftree[0][j][1] - agents.belieftree[0][j][0]) > 0):
				cw_of_interest.append(len_DC + len_PC + len_S + len_PC*len_DC + (j-len_DC) + k*len_PC)

		# If the team is advocating for a problem, the following tasks are completed
		if agents.select_issue_3S_pf == 'problem':

			# 50% of the resources (from actions)
			while agents.resources_actions_BFraming > 0.001:
				# FIRST - Calculation of the best option
				# Estimating the grades of the changes in the causal relations - Based on partial knowledge:
				actions_EP_grades_BFraming = []
				for cw in range(len(cw_of_interest)):
					# Go through each of the agents
					actions_EP_grades_BFraming_ind = []

					for agents_BFraming in range(len(agent_action_list)):
						# Making sure that the agent does not count itself
						if agents != agent_action_list[agents_BFraming]:

							# Calculate the impact of the framing depending on affiliations:
							# WATCH OUT - The agent action list is not ordered, it is therefore paramount to select based on unique_id and not on item number in the list!!
							# This warning only applies when looking for the partial knowledge beliefs in the belief tree of the original agent.
							# Same affiliation

							# Check if no partial knowledge (initial value)
							check_none = 0
							if agents.belieftree[1 + agent_action_list[agents_BFraming].unique_id][cw_of_interest[cw]][0] == None:
								check_none = 1
								agents.belieftree[1 + agent_action_list[agents_BFraming].unique_id][cw_of_interest[cw]][0] = 0
							
							if agents.affiliation == agent_action_list[agents_BFraming].affiliation:
								cw_grade = abs((agents.belieftree[0][cw_of_interest[cw]][0] - \
								agents.belieftree[1 + agent_action_list[agents_BFraming].unique_id][cw_of_interest[cw]][0]) * \
								agents.resources[0] * 0.1 / (action_agent_number - 1))

							# Affiliation 1 and 2
							if (agents.affiliation == 0 and agent_action_list[agents_BFraming].affiliation == 1) or \
			    			  (agents.affiliation == 1 and agent_action_list[agents_BFraming].affiliation == 0):
								cw_grade = abs((agents.belieftree[0][cw_of_interest[cw]][0] - \
								agents.belieftree[1 + agent_action_list[agents_BFraming].unique_id][cw_of_interest[cw]][0]) * \
								agents.resources[0] * 0.1 * affiliation_weights[0] / (action_agent_number - 1))

							# Affiliation 1 and 3
							if (agents.affiliation == 0 and agent_action_list[agents_BFraming].affiliation == 2) or \
							  (agents.affiliation == 2 and agent_action_list[agents_BFraming].affiliation == 0):
								cw_grade = abs((agents.belieftree[0][cw_of_interest[cw]][0] - \
								agents.belieftree[1 + agent_action_list[agents_BFraming].unique_id][cw_of_interest[cw]][0]) * \
								agents.resources[0] * 0.1 * affiliation_weights[1] / (action_agent_number - 1))

							# Affiliation 2 and 3
							if (agents.affiliation == 1 and agent_action_list[agents_BFraming].affiliation == 2) or \
							 (agents.affiliation == 2 and agent_action_list[agents_BFraming].affiliation == 1):
								cw_grade = abs((agents.belieftree[0][cw_of_interest[cw]][0] - \
								agents.belieftree[1 + agent_action_list[agents_BFraming].unique_id][cw_of_interest[cw]][0]) * \
								agents.resources[0] * 0.1 * affiliation_weights[2] / (action_agent_number - 1))

							# Reset the value after finding the grade
							if check_none == 1:
								agents.belieftree[1 + agent_action_list[agents_BFraming].unique_id][cw_of_interest[cw]][0] = None
							
							actions_EP_grades_BFraming_ind.append(cw_grade)
						# If it is the same agent, then rate the action as 0 (important for appropriate indexing)
						else:
							cw_grade = 0
							actions_EP_grades_BFraming_ind.append(cw_grade)

					actions_EP_grades_BFraming.append(sum(actions_EP_grades_BFraming_ind))

				# Check that there are indeed grades otherwise break from this loop
				if len(actions_EP_grades_BFraming) > 0:
					# Finding the index of the causal relation most affected based on the partial knowledge
					best_BFraming = actions_EP_grades_BFraming.index(max(actions_EP_grades_BFraming))
				else:
					break

				# SECOND - Changing the causal relations of all the agents - Based on actual beliefs:
				for agents_BFraming in range(len(agent_action_list)):
					# Making sure that the agent does not count itself
					if agents != agent_action_list[agents_BFraming]:

						# Same affiliation
						if agents.affiliation == agent_action_list[agents_BFraming].affiliation:
							agent_action_list[agents_BFraming].belieftree[0][cw_of_interest[best_BFraming]][0] += \
							(agents.belieftree[0][cw_of_interest[best_BFraming]][0] - \
							agent_action_list[agents_BFraming].belieftree[0][cw_of_interest[best_BFraming]][0]) * \
							agents.resources[0] * 0.1 / (action_agent_number - 1)
						
						# Affiliation 1 and 2
						if (agents.affiliation == 0 and agent_action_list[agents_BFraming].affiliation == 1) or \
		    			  (agents.affiliation == 1 and agent_action_list[agents_BFraming].affiliation == 0):
							agent_action_list[agents_BFraming].belieftree[0][cw_of_interest[best_BFraming]][0] += \
							(agents.belieftree[0][cw_of_interest[best_BFraming]][0] - \
							agent_action_list[agents_BFraming].belieftree[0][cw_of_interest[best_BFraming]][0]) * \
							agents.resources[0] * 0.1 * affiliation_weights[0] / (action_agent_number - 1)
						
						# Affiliation 1 and 3
						if (agents.affiliation == 0 and agent_action_list[agents_BFraming].affiliation == 2) or \
						  (agents.affiliation == 2 and agent_action_list[agents_BFraming].affiliation == 0):
							agent_action_list[agents_BFraming].belieftree[0][cw_of_interest[best_BFraming]][0] += \
							(agents.belieftree[0][cw_of_interest[best_BFraming]][0] - \
							agent_action_list[agents_BFraming].belieftree[0][cw_of_interest[best_BFraming]][0]) * \
							agents.resources[0] * 0.1 * affiliation_weights[1] / (action_agent_number - 1)
						
						# Affiliation 2 and 3
						if (agents.affiliation == 1 and agent_action_list[agents_BFraming].affiliation == 2) or \
						 (agents.affiliation == 2 and agent_action_list[agents_BFraming].affiliation == 1):
							agent_action_list[agents_BFraming].belieftree[0][cw_of_interest[best_BFraming]][0] += \
							(agents.belieftree[0][cw_of_interest[best_BFraming]][0] - \
							agent_action_list[agents_BFraming].belieftree[0][cw_of_interest[best_BFraming]][0]) * \
							agents.resources[0] * 0.1 * affiliation_weights[2] / (action_agent_number - 1)

						# Check that it is not higher than 1 or lower than -1
						if agent_action_list[agents_BFraming].belieftree[0][cw_of_interest[best_BFraming]][0] > 1:
							agent_action_list[agents_BFraming].belieftree[0][cw_of_interest[best_BFraming]][0] = 1
						if agent_action_list[agents_BFraming].belieftree[0][cw_of_interest[best_BFraming]][0] < -1:
							agent_action_list[agents_BFraming].belieftree[0][cw_of_interest[best_BFraming]][0] = -1

						# Providing partial knowledge - Blanket framing - 0.5 range from real value: (Acting agent)
						agents.belieftree[1 + agent_action_list[agents_BFraming].unique_id][cw_of_interest[best_BFraming]][0] = \
							agent_action_list[agents_BFraming].belieftree[0][cw_of_interest[best_BFraming]][0] + (random.random()/2) - 0.25
						# 1-1 check
						if agents.belieftree[1 + agent_action_list[agents_BFraming].unique_id][cw_of_interest[best_BFraming]][0] > 1:
							agents.belieftree[1 + agent_action_list[agents_BFraming].unique_id][cw_of_interest[best_BFraming]][0] = 1
						if agents.belieftree[1 + agent_action_list[agents_BFraming].unique_id][cw_of_interest[best_BFraming]][0] < -1:
							agents.belieftree[1 + agent_action_list[agents_BFraming].unique_id][cw_of_interest[best_BFraming]][0] = -1
						# Providing partial knowledge - Blanket framing - 0.5 range from real value: (Acted upon agent)
						agent_action_list[agents_BFraming].belieftree[1 + agents.unique_id][cw_of_interest[best_BFraming]][0] = \
							agents.belieftree[0][cw_of_interest[best_BFraming]][0] + (random.random()/2) - 0.25
						# 1-1 check
						if agent_action_list[agents_BFraming].belieftree[1 + agents.unique_id][cw_of_interest[best_BFraming]][0] > 1:
							agent_action_list[agents_BFraming].belieftree[1 + agents.unique_id][cw_of_interest[best_BFraming]][0] = 1
						if agent_action_list[agents_BFraming].belieftree[1 + agents.unique_id][cw_of_interest[best_BFraming]][0] < -1:
							agent_action_list[agents_BFraming].belieftree[1 + agents.unique_id][cw_of_interest[best_BFraming]][0] = -1

				agents.resources_actions_BFraming -= agents.resources[0] * 0.1
				agents.resources_actions -= agents.resources[0] * 0.1

		# If the team is advocating for a policy, the following tasks are completed
		if agents.select_issue_3S_pf == 'policy':

			# 2. Electorate influence, grading of actions and implementation of the best actions until resources run out 
			# 50% of the resources (from actions)
			while agents.resources_actions_EInfluence > 0.001:
				actions_EP_grades_EInfluence = []
				# FIRST - Calculation of the best option
				for issue_num in range(len_DC + len_PC):
					actions_EP_grades_EInfluence_ind = []
					# Going through all agents that are electorate from the master_list
					agents_electorate = []
					for agents_run in master_list:
						if type(agents) == Electorate:
							agents_electorate.append(agents_run)

					for agents_el in agents_electorate:

						# Setting grade to 0 if the external party has no interest in the issue:
						if agents.belieftree[0][issue_num][0] == 'No':
							issue_num_grade	 = 0 

						# Calculate a grade if the external party has an interest in the issue
						else:

							# Memorising the original belief values
							original_belief = [0,0,0]
							original_belief[0] = copy.copy(agents_el.belieftree_electorate[issue_num][0])
							original_belief[1] = copy.copy(agents_el.belieftree_electorate[issue_num][1])
							original_belief[2] = copy.copy(agents_el.belieftree_electorate[issue_num][2])

							if agents.affiliation == agents_el.affiliation:
								# Perfoming the action
								agents_el.belieftree_electorate[issue_num][1] += (agents.belieftree[0][issue_num][1] - agents_el.belieftree_electorate[issue_num][1]) \
									* agents.resources[0] * 0.1 / electorate_number
								# Update of the preference
								self.preference_udapte_electorate(agents_el, len_DC, len_PC, len_S)
								# Calculation of the new gradec
								issue_num_grade = abs(agents.belieftree[0][issue_num][2] - agents_el.belieftree_electorate[issue_num][2])

							# Affiliation 1 and 2
							if (agents.affiliation == 0 and agents_el.affiliation == 1) or (agents.affiliation == 1 and agents_el.affiliation == 0):
								# Perfoming the action
								agents_el.belieftree_electorate[issue_num][1] += (agents.belieftree[0][issue_num][1] - agents_el.belieftree_electorate[issue_num][1]) \
									* agents.resources[0] * 0.1 * affiliation_weights[0] / electorate_number
								# Update of the preference
								self.preference_udapte_electorate(agents_el, len_DC, len_PC, len_S)
								# Calculation of the new gradec
								issue_num_grade = abs(agents.belieftree[0][issue_num][2] - agents_el.belieftree_electorate[issue_num][2])

							# Affiliation 1 and 3
							if (agents.affiliation == 0 and agents_el.affiliation == 2) or (agents.affiliation == 2 and agents_el.affiliation == 0):
								# Perfoming the action
								agents_el.belieftree_electorate[issue_num][1] += (agents.belieftree[0][issue_num][1] - agents_el.belieftree_electorate[issue_num][1]) \
									* agents.resources[0] * 0.1 * affiliation_weights[1] / electorate_number
								# Update of the preference
								self.preference_udapte_electorate(agents_el, len_DC, len_PC, len_S)
								# Calculation of the new gradec
								issue_num_grade = abs(agents.belieftree[0][issue_num][2] - agents_el.belieftree_electorate[issue_num][2])

							# Affiliation 2 and 3
							if (agents.affiliation == 1 and agents_el.affiliation == 2) or (agents.affiliation == 2 and agents_el.affiliation == 1):
								# Perfoming the action
								agents_el.belieftree_electorate[issue_num][1] += (agents.belieftree[0][issue_num][1] - agents_el.belieftree_electorate[issue_num][1]) \
									* agents.resources[0] * 0.1 * affiliation_weights[2] / electorate_number
								# Update of the preference
								self.preference_udapte_electorate(agents_el, len_DC, len_PC, len_S)
								# Calculation of the new grade
								issue_num_grade = abs(agents.belieftree[0][issue_num][2] - agents_el.belieftree_electorate[issue_num][2])

							# Restoring the initial values
							agents_el.belieftree_electorate[issue_num][0] = original_belief[0]
							agents_el.belieftree_electorate[issue_num][1] = original_belief[1]
							agents_el.belieftree_electorate[issue_num][2] = original_belief[2]


							# Re-updating the preference levels
							self.preference_udapte_electorate(agents_el, len_DC, len_PC, len_S)

						actions_EP_grades_EInfluence_ind.append(issue_num_grade)

					actions_EP_grades_EInfluence.append(sum(actions_EP_grades_EInfluence_ind))

				# Choose the action that leads to the minimum amount of difference between the EP and the electorates
				best_EInfluence = actions_EP_grades_EInfluence.index(min(actions_EP_grades_EInfluence))
				
				# SECOND - Changing the aims of all the agents for the best choice
				for agents_el in agents_electorate:

					if agents.affiliation == agents_el.affiliation:
						agents_el.belieftree_electorate[best_EInfluence][1] += (agents.belieftree[0][best_EInfluence][1] - agents_el.belieftree_electorate[best_EInfluence][1]) \
						* agents.resources[0] * 0.1 / electorate_number

					# Affiliation 1 and 2
					if (agents.affiliation == 0 and agents_el.affiliation == 1) or (agents.affiliation == 1 and agents_el.affiliation == 0):
						agents_el.belieftree_electorate[best_EInfluence][1] += (agents.belieftree[0][best_EInfluence][1] - agents_el.belieftree_electorate[best_EInfluence][1]) \
						* agents.resources[0] * 0.1 * affiliation_weights[0] / electorate_number

						# Affiliation 1 and 3
					if (agents.affiliation == 0 and agents_el.affiliation == 2) or (agents.affiliation == 2 and agents_el.affiliation == 0):
						agents_el.belieftree_electorate[best_EInfluence][1] += (agents.belieftree[0][best_EInfluence][1] - agents_el.belieftree_electorate[best_EInfluence][1]) \
						* agents.resources[0] * 0.1 * affiliation_weights[1] / electorate_number

					# Affiliation 2 and 3
					if (agents.affiliation == 1 and agents_el.affiliation == 2) or (agents.affiliation == 2 and agents_el.affiliation == 1):
						agents_el.belieftree_electorate[best_EInfluence][1] += (agents.belieftree[0][best_EInfluence][1] - agents_el.belieftree_electorate[best_EInfluence][1]) \
						* agents.resources[0] * 0.1 * affiliation_weights[2] / electorate_number

					# 1-1 check
					agents_el.belieftree_electorate[best_EInfluence][1] = \
						self.one_minus_one_check2(agents_el.belieftree_electorate[best_EInfluence][1])

					# Re-updating the preference levels
					self.preference_udapte_electorate(agents_el, len_DC, len_PC, len_S)

				agents.resources_actions_EInfluence -= agents.resources[0] * 0.1
				agents.resources_actions -= agents.resources[0] * 0.1

	def preference_udapte_electorate(self, agent, len_DC, len_PC, len_S):

		"""
		Electorate preference update function
		===========================

		This function is used to calculate the preferences of the electorate
		agents. It is the similar to the function used to calculate the preferences
		of the other agents. The main difference is the non inclusion of the 
		causal relations (the electorate tree does not have any). Each preference
		is therefore calculated based on the state and aim for each level
		in the tree.

		The calculation of the deep core, policy core and secondary issues 
		preferences is performed.c

		"""

		#####
		# Preference calculation for the deep core issues
		DC_denominator = 0
		for h in range(len_DC):
			DC_denominator = DC_denominator + abs(agent.belieftree_electorate[h][1] - agent.belieftree_electorate[h][0])
		for i in range(len_DC):
			# There are rare occasions where the denominator could be 0
			if DC_denominator != 0:
				agent.belieftree_electorate[i][2] = abs(agent.belieftree_electorate[i][1] - agent.belieftree_electorate[i][0]) / DC_denominator
			else:
				agent.belieftree_electorate[i][2] = 0

		#####
		# Preference calculation for the policy core issues
		PC_denominator = 0
		for h in range(len_PC):
			PC_denominator = PC_denominator + abs(agent.belieftree_electorate[len_DC + h][1] - agent.belieftree_electorate[len_DC + h][0])
		for i in range(len_PC):
			# There are rare occasions where the denominator could be 0
			if PC_denominator != 0:
				agent.belieftree_electorate[len_DC + i][2] = abs(agent.belieftree_electorate[len_DC + i][1] - agent.belieftree_electorate[len_DC + i][0]) / PC_denominator
			else:
				agent.belieftree_electorate[len_DC + i][2] = 0

		#####
		# Preference calculation for the secondary issues
		S_denominator = 0
		for h in range(len_S):
			S_denominator = S_denominator + abs(agent.belieftree_electorate[len_DC + len_PC + h][1] - agent.belieftree_electorate[len_DC + len_PC + h][0])
		for i in range(len_S):
			# There are rare occasions where the denominator could be 0
			if S_denominator != 0:
				agent.belieftree_electorate[len_DC + len_PC + i][2] = abs(agent.belieftree_electorate[len_DC + len_PC + i][1] - agent.belieftree_electorate[len_DC + len_PC + i][0]) / S_denominator
			else:
				agent.belieftree_electorate[len_DC + len_PC + i][2] = 0

	def one_minus_one_check2(self, to_be_checked_parameter):

		checked_parameter = 0
		if to_be_checked_parameter > 1:
			checked_parameter = 1
		elif to_be_checked_parameter < -1:
			checked_parameter = -1
		else:
			checked_parameter = to_be_checked_parameter
		return checked_parameter

# Creation of the policy maker agents
class Policymakers(Agent):

	def __init__(self, run_number, agent_id, unique_id, pos, network_strategy, affiliation, resources, belieftree, instrument_preferences, belieftree_policy, belieftree_instrument, select_as_issue, select_pinstrument, select_issue_3S_as, \
		select_problem_3S_as, select_policy_3S_as, select_issue_3S_pf, select_problem_3S_pf, select_policy_3S_pf, team_as, team_pf, coalition_as, coalition_pf):
		# super().__init__(unique_id, model)
		self.run_number = run_number
		self.agent_id = agent_id
		self.pos = pos
		self.network_strategy = network_strategy
		self.unique_id = unique_id
		# self.model = model
		self.affiliation = affiliation
		self.resources = resources
		self.belieftree = belieftree
		self.belieftree_policy = belieftree_policy
		self.belieftree_instrument = belieftree_instrument
		self.instrument_preferences = instrument_preferences
		self.select_as_issue = select_as_issue
		self.select_pinstrument = select_pinstrument
		self.select_issue_3S_as = select_issue_3S_as
		self.select_problem_3S_as = select_problem_3S_as
		self.select_policy_3S_as = select_policy_3S_as
		self.select_issue_3S_pf = select_issue_3S_pf
		self.select_problem_3S_pf = select_problem_3S_pf
		self.select_policy_3S_pf = select_policy_3S_pf
		self.team_as = team_as
		self.team_pf = team_pf
		self.coalition_as = coalition_as
		self.coalition_pf = coalition_pf

	# def __str__(self):
	# 	return 'POLICYMAKER - Affiliation: ' + str(self.affiliation) + ', Resources: ' + str(self.resources) + \
	# 	', Position: [' + str(self.pos[0]) + ',' + str(self.pos[1]) + '], ID: ' + str(self.unique_id) + \
	# 	', Problem selected: ' + str(self.select_problem) + ', Policy selected: ' + str(self.select_policy) + \
	# 	', Belief tree: ' + str(self.belieftree)

	def policymakers_states_update(self, agent, master_list, affiliation_weights):
		#' Addition of more than 3 affiliation will lead to unreported errors!')
		if len(affiliation_weights) != 3:
			print('WARNING - THIS CODE DOESNT WORK FOR MORE OR LESS THAN 3 AFFILIATIONS')

		# Defining the external party list along with the truth agent relation
		externalparties_list = []
		for agents in master_list:
			if type(agents) == Truth:
				truthagent = agents
			if type(agents) == Externalparties:
				externalparties_list.append(agents)

		# going through the different external parties:
		belief_sum_ep = [0 for k in range(len(truthagent.belieftree_truth))]
		# print(belief_sum_ep)
		for i in range(len(truthagent.belieftree_truth)):
			# print('NEW ISSUE! NEW ISSUES!')
			# This is used because in some cases, the external parties will have no impact on the agent (None values in the states of the EP)
			actual_length_ep = 0
			for j in range(len(externalparties_list)):
				# This line is added in case the EP has None states
				if externalparties_list[j].belieftree[0][i][0] != 'No':
					actual_length_ep += 1
					# Currently, the state of the policy makers is initialised as being equal to their initial aim:
					if agent.belieftree[0][i][0] == None:
						# print('Triggered - changed to: ' + str(agent.belieftree[0][i][1]))
						agent.belieftree[0][i][0] = agent.belieftree[0][i][1]
					# If they have the same affiliation, add without weight
					if externalparties_list[j].affiliation == agent.affiliation:
						# print('AFFILIATIONS ARE EQUAL')
						# print('issue ' + str(i+1) + ': ' + str(externalparties_list[j].belieftree[0][i][0]) +  /
						# ' and affiliation: ' + str(externalparties_list[j].affiliation) + '  ' + str(externalparties_list[j].unique_id))
						# print('This is the sum: ' + str(belief_sum_ep[i]))
						belief_sum_ep[i] = belief_sum_ep[i] + (externalparties_list[j].belieftree[0][i][0] - agent.belieftree[0][i][0])
						# print('The sum is equal to: ' + str(belief_sum_ep))
						# print('The change in state belief is equal to: ' + str(belief_sum_ep[i] / len(externalparties_list)))
					if (externalparties_list[j].affiliation == 0 and agent.affiliation == 1) or \
					   (externalparties_list[j].affiliation == 1 and agent.affiliation == 0):
						# print('AFFILIATION 1 AND 2')
						belief_sum_ep[i] = belief_sum_ep[i] + \
						   (externalparties_list[j].belieftree[0][i][0] - agent.belieftree[0][i][0]) * affiliation_weights[0]
					if (externalparties_list[j].affiliation == 0 and agent.affiliation == 2) or \
					   (externalparties_list[j].affiliation == 2 and agent.affiliation == 0):
						# print('AFFILIATION 1 AND 3')
						belief_sum_ep[i] = belief_sum_ep[i] + \
						   (externalparties_list[j].belieftree[0][i][0] - agent.belieftree[0][i][0]) * affiliation_weights[1]
					if (externalparties_list[j].affiliation == 1 and agent.affiliation == 2) or \
					   (externalparties_list[j].affiliation == 2 and agent.affiliation == 1):
						# print('AFFILIATION 2 AND 3')
						belief_sum_ep[i] = belief_sum_ep[i] + \
						   (externalparties_list[j].belieftree[0][i][0] - agent.belieftree[0][i][0]) * affiliation_weights[2]
			agent.belieftree[0][i][0] = agent.belieftree[0][i][0] + belief_sum_ep[i] / actual_length_ep
			# print('This is issue: ' + str(i+1) + ' and its new value is: ' + str(agent.belieftree[0][i][0]))
		# print(agent)

	# Simple print with ID
	def __str__(self):
		return 'Policy maker: ' + str(self.unique_id)

	def pm_pe_actions_as(self, agents, link_list, deep_core, policy_core, secondary, resources_weight_action, resources_potency):

		len_DC = len(deep_core)
		len_PC = len(policy_core)
		len_S = len(secondary)

		# Selection of the cw of interest
		cw_of_interest = []
		# We only consider the causal relations related to the problem on the agenda
		for cw_choice in range(len(deep_core)):
				cw_of_interest.append(len_DC + len_PC + len_S + (agents.select_as_issue - len_DC) + cw_choice * len(policy_core))

		# print(' ')
		# print('Causal relations of interest: ' + str(cw_of_interest))

		# Making sure there are enough resources
		while agents.resources_actions > 0.001:

			# Going through all the links in the model
			# print(agents)
			total_grade_list = []
			total_grade_list_links = []
			for links in link_list:

				# Making sure that the link is attached to the agent and has a aware higher than 0
				if (links.agent1 == agents or links.agent2 == agents) and links.aware > 0:
					total_grade_list_links.append(links)

					# Definition the action weight parameter
					if type(links.agent1) == Policymakers or type(links.agent2) == Policymakers:
						actionWeight = 1
					else:
						actionWeight = 0.95
					
					# 1. Grading all framing actions:
					# Checking through all possible framing - This is all based on partial knowledge!
					for cw in range(len(cw_of_interest)):

						# Checking which agent in the link is the original agent
						if links.agent1 == agents:

							# NEW LIKELIHOOD CALCULATION











							# Check if no partial knowledge (initial value)
							check_none = 0
							if agents.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0] == None:
								agents.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0] = 0
								check_none = 1
							# Memorising the original belief values
							original_belief = [0]
							original_belief[0] = copy.copy(agents.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0])
							# Performing the action
							agents.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0] += \
								(agents.belieftree[0][cw_of_interest[cw]][0] - agents.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0]) * \
								agents.resources[0] * resources_weight_action * links.aware * resources_potency
							# 1-1 check
							agents.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0] = \
								self.one_minus_one_check2(agents.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0])
							# Update of the preferences for that partial knowledge agent
							self.preference_udapte_as_PC(agents, 1 + links.agent2.unique_id, len_DC, len_PC, len_S)
							# Calculation of the new grade - we check selected issue using partial knowledge updates
							cw_grade = abs(agents.belieftree[0][agents.select_as_issue][2] - agents.belieftree[1 + links.agent2.unique_id][agents.select_as_issue][2])
							# print('cw_grade: ' + str(cw_grade))
							# Restoring the initial values
							agents.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0] = original_belief[0]
							# Re-updating the preference levels
							self.preference_udapte_as_PC(agents, 1 + links.agent2.unique_id, len_DC, len_PC, len_S)
							# Adding the grade to the grade list
							total_grade_list.append(cw_grade)
							#  Reset to None after finding the grade
							if check_none == 1:
								agents.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0] = None

						# Checking which agent in the link is the original agent
						if links.agent2 == agents:
							#  Check if no partial knowledge (initial value)
							check_none = 0
							if agents.belieftree[1 + links.agent1.unique_id][cw_of_interest[cw]][0] == None:
								agents.belieftree[1 + links.agent1.unique_id][cw_of_interest[cw]][0] = 0
								check_none = 1
							# Memorising the original belief values
							original_belief = [0]
							original_belief[0] = copy.copy(agents.belieftree[1 + links.agent1.unique_id][cw_of_interest[cw]][0])
							# Performing the action
							agents.belieftree[1 + links.agent1.unique_id][cw_of_interest[cw]][0] += \
								(agents.belieftree[0][cw_of_interest[cw]][0] - agents.belieftree[1 + links.agent1.unique_id][cw_of_interest[cw]][0]) * \
								agents.resources[0] * resources_weight_action * links.aware * resources_potency
							# 1-1 check
							agents.belieftree[1 + links.agent1.unique_id][cw_of_interest[cw]][0] = \
								self.one_minus_one_check2(agents.belieftree[1 + links.agent1.unique_id][cw_of_interest[cw]][0])
							# Update of the preferences for that partial knowledge agent
							self.preference_udapte_as_PC(agents, 1 + links.agent1.unique_id, len_DC, len_PC, len_S)
							# Calculation of the new grade - we check selected issue using partial knowledge updates
							cw_grade = abs(agents.belieftree[0][agents.select_as_issue][2] - agents.belieftree[1 + links.agent1.unique_id][agents.select_as_issue][2])
							# print('cw_grade: ' + str(cw_grade))
							# Restoring the initial values
							agents.belieftree[1 + links.agent1.unique_id][cw_of_interest[cw]][0] = original_belief[0]
							# Re-updating the preference levels
							self.preference_udapte_as_PC(agents, 1 + links.agent1.unique_id, len_DC, len_PC, len_S)
							# Adding the grade to the grade list
							total_grade_list.append(cw_grade)
							# Reset to None after finding the grade
							if check_none == 1:
								agents.belieftree[1 + links.agent1.unique_id][cw_of_interest[cw]][0] = None

					# 2. Grading all individual actions - Aim change
					if links.agent1 == agents:
						# Check if no partial knowledge (initial value)
						check_none = 0
						if agents.belieftree[1 + links.agent2.unique_id][agents.select_as_issue][1] == None:
							agents.belieftree[1 + links.agent2.unique_id][agents.select_as_issue][1] = 0
							check_none = 1
						# Memorising is no partial knoweldge
						original_belief = [0]
						original_belief[0] = copy.copy(agents.belieftree[1 + links.agent2.unique_id][agents.select_as_issue][1])
						# Performing the action
						agents.belieftree[1 + links.agent2.unique_id][agents.select_as_issue][1] += \
							(agents.belieftree[0][agents.select_as_issue][1] - agents.belieftree[1 + links.agent2.unique_id][agents.select_as_issue][1]) * \
							agents.resources[0] * resources_weight_action * links.aware * links.conflict_level[0][agents.select_as_issue][1] * actionWeight * resources_potency
						# 1-1 check
						agents.belieftree[1 + links.agent2.unique_id][agents.select_as_issue][1] = \
							self.one_minus_one_check2(agents.belieftree[1 + links.agent2.unique_id][agents.select_as_issue][1])
						# Update of the preferences for that partial knowledge agent
						self.preference_udapte_as_PC(agents, 1 + links.agent2.unique_id, len_DC, len_PC, len_S)
						# Calculation of the new grade - we check selected issue using partial knowledge updates
						aim_grade_issue = abs(agents.belieftree[0][agents.select_as_issue][2] - agents.belieftree[1 + links.agent2.unique_id][agents.select_as_issue][2])
						# print('aim_grade_issue: ' + str(aim_grade_issue))
						# Restoring the initial values
						agents.belieftree[1 + links.agent2.unique_id][agents.select_as_issue][1] = original_belief[0]
						# Re-updating the preference levels
						self.preference_udapte_as_PC(agents, 1 + links.agent2.unique_id, len_DC, len_PC, len_S)
						#  Reset to None after finding the grade
						if check_none == 1:
							agents.belieftree[1 + links.agent2.unique_id][agents.select_as_issue][1] = None
						# Adding the grade to the grade list
						total_grade_list.append(aim_grade_issue)

					if links.agent2 == agents:
						# Check if no partial knowledge (initial value)
						check_none = 0
						if agents.belieftree[1 + links.agent1.unique_id][agents.select_as_issue][1] == None:
							agents.belieftree[1 + links.agent1.unique_id][agents.select_as_issue][1] = 0
							check_none = 1
						# Memorising is no partial knoweldge
						original_belief = [0]
						original_belief[0] = copy.copy(agents.belieftree[1 + links.agent1.unique_id][agents.select_as_issue][1])
						# Performing the action
						agents.belieftree[1 + links.agent1.unique_id][agents.select_as_issue][1] += \
							(agents.belieftree[0][agents.select_as_issue][1] - agents.belieftree[1 + links.agent1.unique_id][agents.select_as_issue][1]) * \
							agents.resources[0] * resources_weight_action * links.aware * links.conflict_level[1][agents.select_as_issue][1] * actionWeight * resources_potency
						# 1-1 check
						agents.belieftree[1 + links.agent1.unique_id][agents.select_as_issue][1] = \
							self.one_minus_one_check2(agents.belieftree[1 + links.agent1.unique_id][agents.select_as_issue][1])
						# Update of the preferences for that partial knowledge agent
						self.preference_udapte_as_PC(agents, 1 + links.agent1.unique_id, len_DC, len_PC, len_S)
						# Calculation of the new grade - we check selected issue using partial knowledge updates
						aim_grade_issue = abs(agents.belieftree[0][agents.select_as_issue][2] - agents.belieftree[1 + links.agent1.unique_id][agents.select_as_issue][2])
						# print('aim_grade_issue: ' + str(aim_grade_issue))
						# Restoring the initial values
						agents.belieftree[1 + links.agent1.unique_id][agents.select_as_issue][1] = original_belief[0]
						# Re-updating the preference levels
						self.preference_udapte_as_PC(agents, 1 + links.agent1.unique_id, len_DC, len_PC, len_S)
						#  Reset to None after finding the grade
						if check_none == 1:
							agents.belieftree[1 + links.agent1.unique_id][agents.select_as_issue][1] = None
						# Adding the grade to the grade list
						total_grade_list.append(aim_grade_issue)

					# 3. Grading all individual actions - State change
					if links.agent1 == agents:
						# Check if no partial knowledge (initial value)
						check_none = 0
						if agents.belieftree[1 + links.agent2.unique_id][agents.select_as_issue][0] == None:
							agents.belieftree[1 + links.agent2.unique_id][agents.select_as_issue][0] = 0
							check_none = 1
						# Memorising is no partial knoweldge
						original_belief = [0]
						original_belief[0] = copy.copy(agents.belieftree[1 + links.agent2.unique_id][agents.select_as_issue][0])
						# Performing the action
						agents.belieftree[1 + links.agent2.unique_id][agents.select_as_issue][0] += \
							(agents.belieftree[0][agents.select_as_issue][0] - agents.belieftree[1 + links.agent2.unique_id][agents.select_as_issue][0]) * \
							agents.resources[0] * resources_weight_action * links.aware * links.conflict_level[0][agents.select_as_issue][0] * actionWeight * resources_potency
						# 1-1 check
						agents.belieftree[1 + links.agent2.unique_id][agents.select_as_issue][0] = \
							self.one_minus_one_check2(agents.belieftree[1 + links.agent2.unique_id][agents.select_as_issue][0])
						# Update of the preferences for that partial knowledge agent
						self.preference_udapte_as_PC(agents, 1 + links.agent2.unique_id, len_DC, len_PC, len_S)
						# Calculation of the new grade - we check selected issue using partial knowledge updates
						state_grade_issue = abs(agents.belieftree[0][agents.select_as_issue][2] - agents.belieftree[1 + links.agent2.unique_id][agents.select_as_issue][2])
						# print('state_grade_issue: ' + str(state_grade_issue))
						# Restoring the initial values
						agents.belieftree[1 + links.agent2.unique_id][agents.select_as_issue][0] = original_belief[0]
						# Re-updating the preference levels
						self.preference_udapte_as_PC(agents, 1 + links.agent2.unique_id, len_DC, len_PC, len_S)
						#  Reset to None after finding the grade
						if check_none == 1:
							agents.belieftree[1 + links.agent2.unique_id][agents.select_as_issue][0] = None
						# Adding the grade to the grade list
						total_grade_list.append(state_grade_issue)

					if links.agent2 == agents:
						# Check if no partial knowledge (initial value)
						check_none = 0
						if agents.belieftree[1 + links.agent1.unique_id][agents.select_as_issue][0] == None:
							agents.belieftree[1 + links.agent1.unique_id][agents.select_as_issue][0] = 0
							check_none = 1
						# Memorising is no partial knoweldge
						original_belief = [0]
						original_belief[0] = copy.copy(agents.belieftree[1 + links.agent1.unique_id][agents.select_as_issue][0])
						# Performing the action
						agents.belieftree[1 + links.agent1.unique_id][agents.select_as_issue][0] += \
							(agents.belieftree[0][agents.select_as_issue][0] - agents.belieftree[1 + links.agent1.unique_id][agents.select_as_issue][0]) * \
							agents.resources[0] * resources_weight_action * links.aware * links.conflict_level[1][agents.select_as_issue][0] * actionWeight * resources_potency
						# 1-1 check
						agents.belieftree[1 + links.agent1.unique_id][agents.select_as_issue][0] = \
							self.one_minus_one_check2(agents.belieftree[1 + links.agent1.unique_id][agents.select_as_issue][0])
						# Update of the preferences for that partial knowledge agent
						self.preference_udapte_as_PC(agents, 1 + links.agent1.unique_id, len_DC, len_PC, len_S)
						# Calculation of the new grade - we check selected issue using partial knowledge updates
						state_grade_issue = abs(agents.belieftree[0][agents.select_as_issue][2] - agents.belieftree[1 + links.agent1.unique_id][agents.select_as_issue][2])
						# print('state_grade_issue: ' + str(state_grade_issue))
						# Restoring the initial values
						agents.belieftree[1 + links.agent1.unique_id][agents.select_as_issue][0] = original_belief[0]
						# Re-updating the preference levels
						self.preference_udapte_as_PC(agents, 1 + links.agent1.unique_id, len_DC, len_PC, len_S)
						#  Reset to None after finding the grade
						if check_none == 1:
							agents.belieftree[1 + links.agent1.unique_id][agents.select_as_issue][0] = None
						# Adding the grade to the grade list
						total_grade_list.append(state_grade_issue)
					# print(' ')

			# print(' ')
			# print('Number of actions: ' + str(len(total_grade_list)))
			# print(total_grade_list)

			# 4. Choosing an action
			# Check if several actions have the same grade
			min_best_action = min(total_grade_list)
			count_min_list = []
			count = 0
			for item in total_grade_list:
				if item == min_best_action:
					count_min_list.append(count)
				count += 1
			# print('List of indexes: ' + str(count_min_list))
			# print(' ')

			# If there are several grades at the same level, then choose a random action from these grades:
			if len(count_min_list) > 1:
				best_action_index = random.choice(count_min_list)
				# print('Randomly chosen best action: ' + str(best_action_index))
			else:
				best_action_index = total_grade_list.index(min(total_grade_list))
				# print('Not randomly chosen: ' + str(best_action_index))
			
			# print(' ')
			# print('----- New check for best action ------')
			# print('Action value: ' + str(min(total_grade_list)))
			# print('Index of the best action: ' + str(best_action_index))
			# print('This is the grade of the action: ' + str(total_grade_list[best_action_index]))
			# Make sure that we do not take into account the 0 from the list to perform the following calculations
			# best_action_index += 1
			# print('The total amount of links considered: ' + str(len(total_grade_list_links)))
			# print('The number of actions per link considered: ' + str(len(cw_of_interest) + 2))
			# print('The total amount of actions considered: ' + str(len(total_grade_list)))
			# print('The link for the action is: ' + str(int(best_action_index/(len(cw_of_interest) + 2))))
			best_action = best_action_index - (len(cw_of_interest) + 2) * int(best_action_index/(len(cw_of_interest) + 2))
			# print('The impacted index is: ' + str(best_action))
			# print('The would be index without the +1: ' + str((best_action_index - (len(cw_of_interest) + 2) * int(best_action_index/(len(cw_of_interest) + 2))) - 1))
			# print('   ')

			# 5. Performing the actual action
			# Selecting the link:
			for links in link_list:

				if links == total_grade_list_links[int(best_action_index/(len(cw_of_interest) + 2))]:
					# print(links)

					# If the index is in the first part of the list, then the framing action is the best
					if best_action <= len(cw_of_interest) -1:					
						# print(' ')
						# print('Framing action - causal relation')
						# print('best_action: ' + str(best_action))
						# print('cw_of_interest: ' + str(cw_of_interest))
						# print('cw_of_interest[best_action]: ' + str(cw_of_interest[best_action]))

						# To simplify the notations
						best_action = cw_of_interest[best_action]

						# Update of the aware decay parameter
						links.aware_decay = 5

						# print('Causal affected: ' + str(best_action))
						# best_action = len(self.deep_core) + len(self.policy_core) + len(self.secondary) + best_action
						if links.agent1 == agents:
							
							# print('Before: ' + str(links.agent2.belieftree[0][best_action][0]))
							links.agent2.belieftree[0][best_action][0] += (agents.belieftree[0][best_action][0] - links.agent2.belieftree[0][best_action][0]) * \
								agents.resources[0] * resources_weight_action * links.aware * resources_potency
							# print('After: ' + str(links.agent2.belieftree[0][best_action][0]))
							# 1-1 check
							links.agent2.belieftree[0][best_action][0] = \
								self.one_minus_one_check2(links.agent2.belieftree[0][best_action][0])
							# Providing partial knowledge - Framing - 0.2 range from real value: (Acting agent)
							agents.belieftree[1 + links.agent2.unique_id][best_action][0] = links.agent2.belieftree[0][best_action][0] + (random.random()/5) - 0.1
							# 1-1 check
							agents.belieftree[1 + links.agent2.unique_id][best_action][0] = \
								self.one_minus_one_check2(agents.belieftree[1 + links.agent2.unique_id][best_action][0])
							# Providing partial knowledge - Framing - 0.2 range from real value: (Acted upon agent)
							links.agent2.belieftree[1 + agents.unique_id][best_action][0] = agents.belieftree[0][best_action][0] + (random.random()/5) - 0.1
							# 1-1 check
							links.agent2.belieftree[1 + agents.unique_id][best_action][0] = \
								self.one_minus_one_check2(links.agent2.belieftree[1 + agents.unique_id][best_action][0])

							# print(' ')
							# print('Causal change')
							# print(agents.belieftree[1 + links.agent2.unique_id])
							# print(agents.belieftree[1 + links.agent2.unique_id][best_action][0])

						# Checking which agent in the link is the original agent
						if links.agent2 == agents:
							# print('Before: ' + str(links.agent1.belieftree[0][best_action][0]))
							links.agent1.belieftree[0][best_action][0] += (agents.belieftree[0][best_action][0] - links.agent1.belieftree[0][best_action][0]) * \
								agents.resources[0] * resources_weight_action * links.aware * resources_potency
							# print('After: ' + str(links.agent1.belieftree[0][best_action][0]))
							# 1-1 check
							links.agent1.belieftree[0][best_action][0] = \
								self.one_minus_one_check2(links.agent1.belieftree[0][best_action][0])
							# Providing partial knowledge - Framing - 0.2 range from real value: (Acting agent)
							agents.belieftree[1 + links.agent1.unique_id][best_action][0] = links.agent1.belieftree[0][best_action][0] + (random.random()/5) - 0.1
							# 1-1 check
							agents.belieftree[1 + links.agent1.unique_id][best_action][0] = \
								self.one_minus_one_check2(agents.belieftree[1 + links.agent1.unique_id][best_action][0])
							# Providing partial knowledge - Framing - 0.2 range from real value: (Acted upon agent)
							links.agent1.belieftree[1 + agents.unique_id][best_action][0] = agents.belieftree[0][best_action][0] + (random.random()/5) - 0.1
							# 1-1 check
							links.agent1.belieftree[1 + agents.unique_id][best_action][0] = \
								self.one_minus_one_check2(links.agent1.belieftree[1 + agents.unique_id][best_action][0])

							# print(' ')
							# print('Causal change')
							# print(agents.belieftree[1 + links.agent1.unique_id])
							# print(agents.belieftree[1 + links.agent1.unique_id][best_action][0])

					# If the index is in the second part of the list, then the aim influence action is the best
					if best_action == len(cw_of_interest):
						# print('Implementing a aim influence action:')
						links.aware_decay = 5
						# print('Aim me - problem')

						if links.agent1 == agents:
							# print('Before: ' + str(links.agent2.belieftree[0][agents.select_as_issue][1]))
							links.agent2.belieftree[0][agents.select_as_issue][1] += (agents.belieftree[0][agents.select_as_issue][1] - links.agent2.belieftree[0][agents.select_as_issue][1]) * \
								agents.resources[0] * resources_weight_action * links.aware * resources_potency
							# print('After: ' + str(links.agent2.belieftree[0][agents.select_as_issue][1]))
							# 1-1 check
							links.agent2.belieftree[0][agents.select_as_issue][1] = \
								self.one_minus_one_check2(links.agent2.belieftree[0][agents.select_as_issue][1])
							# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acting agent)
							agents.belieftree[1 + links.agent2.unique_id][agents.select_as_issue][1] = links.agent2.belieftree[0][agents.select_as_issue][1]
							# 1-1 check
							agents.belieftree[1 + links.agent2.unique_id][agents.select_as_issue][1] = \
								self.one_minus_one_check2(agents.belieftree[1 + links.agent2.unique_id][agents.select_as_issue][1])
							# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acted upon agent)
							links.agent2.belieftree[1 + agents.unique_id][agents.select_as_issue][1] = agents.belieftree[0][agents.select_as_issue][1] + (random.random()/5) - 0.1
							# 1-1 check
							links.agent2.belieftree[1 + agents.unique_id][agents.select_as_issue][1] = \
								self.one_minus_one_check2(links.agent2.belieftree[1 + agents.unique_id][agents.select_as_issue][1])

							# print(' ')
							# print('Aim change')
							# print(agents.belieftree[1 + links.agent2.unique_id])

						if links.agent2 == agents:
							# print('Before: ' + str(links.agent1.belieftree[0][agents.select_as_issue][1]))
							links.agent1.belieftree[0][agents.select_as_issue][1] += (agents.belieftree[0][agents.select_as_issue][1] - links.agent1.belieftree[0][agents.select_as_issue][1]) * \
								agents.resources[0] * resources_weight_action * links.aware * resources_potency
							# print('After: ' + str(links.agent1.belieftree[0][agents.select_as_issue][1]))
							# 1-1 check
							links.agent1.belieftree[0][agents.select_as_issue][1] = \
								self.one_minus_one_check2(links.agent1.belieftree[0][agents.select_as_issue][1])
							# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acting agent)
							agents.belieftree[1 + links.agent1.unique_id][agents.select_as_issue][1] = links.agent2.belieftree[0][agents.select_as_issue][1]
							# 1-1 check
							agents.belieftree[1 + links.agent1.unique_id][agents.select_as_issue][1] = \
								self.one_minus_one_check2(agents.belieftree[1 + links.agent1.unique_id][agents.select_as_issue][1])
							# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acted upon agent)
							links.agent1.belieftree[1 + agents.unique_id][agents.select_as_issue][1] = agents.belieftree[0][agents.select_as_issue][1] + (random.random()/5) - 0.1
							# 1-1 check
							links.agent1.belieftree[1 + agents.unique_id][agents.select_as_issue][1] = \
								self.one_minus_one_check2(links.agent1.belieftree[1 + agents.unique_id][agents.select_as_issue][1])


					# If the index is in the first part of the list, then the state influence action is the best
					if best_action == len(cw_of_interest) + 1:
						# print('Implementing a state influence action:')
						links.aware_decay = 5
						# print('State me - problem')

						if links.agent1 == agents:
							# print('Before: ' + str(links.agent2.belieftree[0][len(self.deep_core) + agents.select_problem][0]))
							links.agent2.belieftree[0][agents.select_as_issue][0] += (agents.belieftree[0][agents.select_as_issue][0] - links.agent2.belieftree[0][agents.select_as_issue][0]) * \
								agents.resources[0] * resources_weight_action * links.aware * resources_potency
							# print('After: ' + str(links.agent2.belieftree[0][len(self.deep_core) + agents.select_problem][0]))
							links.agent2.belieftree[0][agents.select_as_issue][0] = \
								self.one_minus_one_check2(links.agent2.belieftree[0][agents.select_as_issue][0])
							# Providing partial knowledge - State problem - 0.2 range from real value: (Acting agent)
							agents.belieftree[1 + links.agent2.unique_id][agents.select_as_issue][0] = links.agent2.belieftree[0][agents.select_as_issue][0] + (random.random()/5) - 0.1
							# 1-1 check
							agents.belieftree[1 + links.agent2.unique_id][agents.select_as_issue][0] = \
								self.one_minus_one_check2(agents.belieftree[1 + links.agent2.unique_id][agents.select_as_issue][0])
							# Providing partial knowledge - State problem - 0.2 range from real value: (Acted upon agent)
							links.agent2.belieftree[1 + agents.unique_id][agents.select_as_issue][0] = agents.belieftree[0][agents.select_as_issue][0] + (random.random()/5) - 0.1
							# 1-1 check
							links.agent2.belieftree[1 + agents.unique_id][agents.select_as_issue][0] = \
								self.one_minus_one_check2(links.agent2.belieftree[1 + agents.unique_id][agents.select_as_issue][0])

							# print(' ')
							# print('State change')
							# print(agents.belieftree[1 + links.agent2.unique_id])

						if links.agent2 == agents:
							# print('Before: ' + str(links.agent1.belieftree[0][len(self.deep_core) + agents.select_problem][0]))
							links.agent1.belieftree[0][agents.select_as_issue][0] += (agents.belieftree[0][agents.select_as_issue][0] - links.agent1.belieftree[0][agents.select_as_issue][0]) * \
								agents.resources[0] * resources_weight_action * links.aware * resources_potency
							# print('After: ' + str(links.agent1.belieftree[0][len(self.deep_core) + agents.select_problem][0]))
							# 1-1 check
							links.agent1.belieftree[0][agents.select_as_issue][0] = \
								self.one_minus_one_check2(links.agent1.belieftree[0][agents.select_as_issue][0])
							# Providing partial knowledge - State problem - 0.2 range from real value: (Acting agent)
							agents.belieftree[1 + links.agent1.unique_id][agents.select_as_issue][0] = links.agent1.belieftree[0][agents.select_as_issue][0] + (random.random()/5) - 0.1
							# 1-1 check
							agents.belieftree[1 + links.agent1.unique_id][agents.select_as_issue][0] = \
								self.one_minus_one_check2(agents.belieftree[1 + links.agent1.unique_id][agents.select_as_issue][0])
							# Providing partial knowledge - State problem - 0.2 range from real value: (Acted upon agent)
							links.agent1.belieftree[1 + agents.unique_id][agents.select_as_issue][0] = agents.belieftree[0][agents.select_as_issue][0] + (random.random()/5) - 0.1
							# 1-1 check
							links.agent1.belieftree[1 + agents.unique_id][agents.select_as_issue][0] = \
								self.one_minus_one_check2(links.agent1.belieftree[1 + agents.unique_id][agents.select_as_issue][0])

							# print(' ')
							# print('State change')
							# print(agents.belieftree[1 + links.agent1.unique_id])

			# agents.resources_actions -= agents.resources
			agents.resources_actions -= agents.resources[0] * resources_weight_action

	def pm_pe_actions_pf(self, agents, link_list, deep_core, policy_core, secondary, causalrelation_number, agenda_as_issue, instruments, resources_weight_action, resources_potency, AS_theory):


		len_DC = len(deep_core)
		len_PC = len(policy_core)
		len_S = len(secondary)

		# Here are the modifications related to the policy formulation
		# Looking for the relevant causal relations for the policy formulation
		of_interest = []
		cw_of_interest = []
		# We only consider the causal relations related to the problem on the agenda
		for cw_choice in range(len(secondary)):
			if agents.belieftree[0][len_DC + len_PC + len_S + (len_DC * len_PC) + (agenda_as_issue - len_DC)*len_S + cw_choice][0] \
				* instruments[agents.select_pinstrument][cw_choice] != 0:
				cw_of_interest.append(len_DC + len_PC + len_S + (len_DC * len_PC) + (agenda_as_issue - len_DC)*len_S + cw_choice)
		of_interest.append(cw_of_interest)
		# Looking for the relevant issues for the policy formulation
		issue_of_interest = []
		for issue_choice in range(len(secondary)):
			if instruments[agents.select_pinstrument][issue_choice] != 0:
				issue_of_interest.append(len_DC + len_PC + issue_choice)
		of_interest.append(issue_of_interest)

		# Making sure there are enough resources
		while agents.resources_actions > 0.001:
			# Going through all the links in the model
			# print(agents)
			total_grade_list = []
			total_grade_list_links = []
			for links in link_list:
				
				# Making sure that the link is attached to the agent and has a aware higher than 0
				if (links.agent1 == agents or links.agent2 == agents) and links.aware > 0:
					total_grade_list_links.append(links)
					# Definition the action weight parameter
					if type(links.agent1) == Policymakers or type(links.agent2) == Policymakers:
						actionWeight = 1
					else:
						actionWeight = 0.95

					
					# 1. Grading all framing actions:
					# Checking through all possible framing - This is all based on partial knowledge!
					for cw in range(len(cw_of_interest)):
						# Checking which agent in the link is the original agent
						if links.agent1 == agents:
							# Check if no partial knowledge (initial value)
							check_none = 0
							if agents.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0] == None:
								agents.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0] = 0
								check_none = 1
							# Memorising the original belief values
							original_belief = [0]
							original_belief[0] = copy.copy(agents.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0])
							# Performing the action
							# print(' ')
							# print('Old value of the CR: ' + str(agents.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0]))
							agents.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0] += \
								(agents.belieftree[0][cw_of_interest[cw]][0] - agents.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0]) * \
								agents.resources[0] * resources_weight_action * links.aware * resources_potency
							# print('New value of the CR: ' + str(agents.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0]))
							# 1-1 check
							agents.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0] = \
								self.one_minus_one_check2(agents.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0])
							# Update the preferences for that partial knowledge agent
							self.instrument_preference_update(agents, 1 + links.agent2.unique_id, AS_theory, len_DC, len_PC, len_S, instruments)
							# Calculation of the new grade - Based on the preference for the instrument
							cw_grade = abs(agents.instrument_preferences[0][agents.select_pinstrument] - agents.instrument_preferences[1 + links.agent2.unique_id][agents.select_pinstrument])
							# print('cw_grade: ' + str(cw_grade))
							# Restoring the initial values
							agents.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0] = original_belief[0]
							# Re-updating the preference levels
							self.instrument_preference_update(agents, 1 + links.agent2.unique_id, AS_theory, len_DC, len_PC, len_S, instruments)
							# Adding the grade to the grade list
							total_grade_list.append(cw_grade)
							# Reset to None after finding the grade
							if check_none == 1:
								agents.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0] = None

						# Checking which agent in the link is the original agent
						if links.agent2 == agents:
							# Check if no partial knowledge (initial value)
							check_none = 0
							if agents.belieftree[1 + links.agent1.unique_id][cw_of_interest[cw]][0] == None:
								agents.belieftree[1 + links.agent1.unique_id][cw_of_interest[cw]][0] = 0
								check_none = 1
							# Memorising the original belief values
							original_belief = [0]
							original_belief[0] = copy.copy(agents.belieftree[1 + links.agent1.unique_id][cw_of_interest[cw]][0])
							# Performing the action
							# print(' ')
							# print('Old value of the CR: ' + str(agents.belieftree[1 + links.agent1.unique_id][cw_of_interest[cw]][0]))
							agents.belieftree[1 + links.agent1.unique_id][cw_of_interest[cw]][0] += \
								(agents.belieftree[0][cw_of_interest[cw]][0] - agents.belieftree[1 + links.agent1.unique_id][cw_of_interest[cw]][0]) * \
								agents.resources[0] * resources_weight_action * links.aware * resources_potency
							# print('New value of the CR: ' + str(agents.belieftree[1 + links.agent1.unique_id][cw_of_interest[cw]][0]))
							# 1-1 check
							agents.belieftree[1 + links.agent1.unique_id][cw_of_interest[cw]][0] = \
								self.one_minus_one_check2(agents.belieftree[1 + links.agent1.unique_id][cw_of_interest[cw]][0])
							# Update the preferences for that partial knowledge agent
							self.instrument_preference_update(agents, 1 + links.agent1.unique_id, AS_theory, len_DC, len_PC, len_S, instruments)
							# Calculation of the new grade - Based on the preference for the instrument
							cw_grade = abs(agents.instrument_preferences[0][agents.select_pinstrument] - agents.instrument_preferences[1 + links.agent1.unique_id][agents.select_pinstrument])
							# print('cw_grade: ' + str(cw_grade))
							# Restoring the initial values
							agents.belieftree[1 + links.agent1.unique_id][cw_of_interest[cw]][0] = original_belief[0]
							# Re-updating the preference levels
							self.instrument_preference_update(agents, 1 + links.agent1.unique_id, AS_theory, len_DC, len_PC, len_S, instruments)
							# Adding the grade to the grade list
							total_grade_list.append(cw_grade)
							# Reset to None after finding the grade
							if check_none == 1:
								agents.belieftree[1 + links.agent1.unique_id][cw_of_interest[cw]][0] = None

					# print(total_grade_list)

					# 2. Grading all individual actions - Aim change

					# Going though all possible choices of issue
					for issue_num in range(len(issue_of_interest)):
					
						if links.agent1 == agents:
							# Looking at the policy chosen by the agent.
							# Check if no partial knowledge (initial value)
							check_none = 0
							if agents.belieftree[1 + links.agent2.unique_id][issue_of_interest[issue_num]][1] == None:
								agents.belieftree[1 + links.agent2.unique_id][issue_of_interest[issue_num]][1] = 0
								check_none = 1
							# Memorising the original belief values
							original_belief = [0]
							original_belief[0] = copy.copy(agents.belieftree[1 + links.agent2.unique_id][issue_of_interest[issue_num]][1])
							# If it knows that the agent has no interest in this issue, then set the grade to 0
							if agents.belieftree[1 + links.agent2.unique_id][issue_of_interest[issue_num]][0] == 'No' or \
							  agents.belieftree[0][issue_of_interest[issue_num]][0] == 'No':
								aim_grade = 0
							else:	
								# Performing the action
								# print(' ')
								# print('Old value of the aim: ' + str(agents.belieftree[1 + links.agent2.unique_id][issue_of_interest[issue_num]][1]))
								agents.belieftree[1 + links.agent2.unique_id][issue_of_interest[issue_num]][1] += \
									(agents.belieftree[0][issue_of_interest[issue_num]][1] - agents.belieftree[1 + links.agent2.unique_id][issue_of_interest[issue_num]][1]) * \
									agents.resources[0] * resources_weight_action * links.aware * links.conflict_level[0][issue_of_interest[issue_num]][1] * actionWeight * resources_potency
								# 1-1 check
								agents.belieftree[1 + links.agent2.unique_id][issue_of_interest[issue_num]][1] = \
									self.one_minus_one_check2(agents.belieftree[1 + links.agent2.unique_id][issue_of_interest[issue_num]][1])
								# Re-updating the preference levels
								self.instrument_preference_update(agents, 1 + links.agent2.unique_id, AS_theory, len_DC, len_PC, len_S, instruments)
								# Calculation of the new grade
								aim_grade = abs(agents.instrument_preferences[0][agents.select_pinstrument] - agents.instrument_preferences[1 + links.agent2.unique_id][agents.select_pinstrument])
							# print('New value of the aim: ' + str(agents.belieftree[1 + links.agent2.unique_id][issue_of_interest[issue_num]][1]))
							# print('aim_grade: ' + str(aim_grade))
							# Restoring the initial values
							agents.belieftree[1 + links.agent2.unique_id][issue_of_interest[issue_num]][1] = original_belief[0]
							# Re-updating the preference levels
							self.instrument_preference_update(agents, 1 + links.agent2.unique_id, AS_theory, len_DC, len_PC, len_S, instruments)
							# Adding the grade to the grade list
							total_grade_list.append(aim_grade)
							# Reset to None after finding the grade
							if check_none == 1:
								agents.belieftree[1 + links.agent2.unique_id][issue_of_interest[issue_num]][1] = None
							
						if links.agent2 == agents:

							# Looking at the policy chosen by the agent.
							# Check if no partial knowledge (initial value)
							check_none = 0
							if agents.belieftree[1 + links.agent1.unique_id][issue_of_interest[issue_num]][1] == None:
								agents.belieftree[1 + links.agent1.unique_id][issue_of_interest[issue_num]][1] = 0
								check_none = 1
							# Memorising the original belief values
							original_belief = [0]
							original_belief[0] = copy.copy(agents.belieftree[1 + links.agent1.unique_id][issue_of_interest[issue_num]][1])
							# If it knows that the agent has no interest in this issue, then set the grade to 0
							if agents.belieftree[1 + links.agent1.unique_id][issue_of_interest[issue_num]][0] == 'No' or \
							  agents.belieftree[0][issue_of_interest[issue_num]][0] == 'No':
								aim_grade = 0
							else:	
								# Performing the action
								# print(' ')
								# print('Old value of the aim: ' + str(agents.belieftree[1 + links.agent1.unique_id][issue_of_interest[issue_num]][1]))
								agents.belieftree[1 + links.agent1.unique_id][issue_of_interest[issue_num]][1] += \
									(agents.belieftree[0][issue_of_interest[issue_num]][1] - agents.belieftree[1 + links.agent1.unique_id][issue_of_interest[issue_num]][1]) * \
									agents.resources[0] * resources_weight_action * links.aware * links.conflict_level[1][issue_of_interest[issue_num]][1] * actionWeight * resources_potency
								# 1-1 check
								agents.belieftree[1 + links.agent1.unique_id][issue_of_interest[issue_num]][1] = \
									self.one_minus_one_check2(agents.belieftree[1 + links.agent1.unique_id][issue_of_interest[issue_num]][1])
								# Re-updating the preference levels
								self.instrument_preference_update(agents, 1 + links.agent1.unique_id, AS_theory, len_DC, len_PC, len_S, instruments)
								# Calculation of the new grade
								aim_grade = abs(agents.instrument_preferences[0][agents.select_pinstrument] - agents.instrument_preferences[1 + links.agent1.unique_id][agents.select_pinstrument])
							# print('New value of the aim: ' + str(agents.belieftree[1 + links.agent1.unique_id][issue_of_interest[issue_num]][1]))
							# print('aim_grade: ' + str(aim_grade))
							# Restoring the initial values
							agents.belieftree[1 + links.agent1.unique_id][issue_of_interest[issue_num]][1] = original_belief[0]
							# Re-updating the preference levels
							self.instrument_preference_update(agents, 1 + links.agent1.unique_id, AS_theory, len_DC, len_PC, len_S, instruments)
							# Adding the grade to the grade list
							total_grade_list.append(aim_grade)
							# Reset to None after finding the grade
							if check_none == 1:
								agents.belieftree[1 + links.agent1.unique_id][issue_of_interest[issue_num]][1] = None

						# print(total_grade_list)

					# 3. Grading all individual actions - State change

					# Going though all possible choices of issue
					for issue_num in range(len(issue_of_interest)):

						if links.agent1 == agents:
								
							# Looking at the policy chosen by the agent.
							# Check if no partial knowledge (initial value)
							check_none = 0
							if agents.belieftree[1 + links.agent2.unique_id][issue_of_interest[issue_num]][0] == None:
								agents.belieftree[1 + links.agent2.unique_id][issue_of_interest[issue_num]][0] = 0
								check_none = 1
							# Memorising the original belief values
							original_belief = [0]
							original_belief[0] = copy.copy(agents.belieftree[1 + links.agent2.unique_id][issue_of_interest[issue_num]][0])
							# If it knows that the agent has no interest in this issue, then set the grade to 0
							if agents.belieftree[1 + links.agent2.unique_id][issue_of_interest[issue_num]][0] == 'No' or \
							  agents.belieftree[0][issue_of_interest[issue_num]][0] == 'No':
								state_grade = 0
							else:	
								# Performing the action
								# print(' ')
								# print('Old value of the aim: ' + str(agents.belieftree[1 + links.agent2.unique_id][issue_of_interest[issue_num]][0]))
								agents.belieftree[1 + links.agent2.unique_id][issue_of_interest[issue_num]][0] += \
									(agents.belieftree[0][issue_of_interest[issue_num]][0] - agents.belieftree[1 + links.agent2.unique_id][issue_of_interest[issue_num]][0]) * \
									agents.resources[0] * resources_weight_action * links.aware * links.conflict_level[0][issue_of_interest[issue_num]][0] * actionWeight * resources_potency
								# 1-1 check
								agents.belieftree[1 + links.agent2.unique_id][issue_of_interest[issue_num]][0] = \
									self.one_minus_one_check2(agents.belieftree[1 + links.agent2.unique_id][issue_of_interest[issue_num]][0])
								# Re-updating the preference levels
								self.instrument_preference_update(agents, 1 + links.agent2.unique_id, AS_theory, len_DC, len_PC, len_S, instruments)
								# Calculation of the new grade
								state_grade = abs(agents.instrument_preferences[0][agents.select_pinstrument] - agents.instrument_preferences[1 + links.agent2.unique_id][agents.select_pinstrument])
							# print('New value of the aim: ' + str(agents.belieftree[1 + links.agent2.unique_id][issue_of_interest[issue_num]][0]))
							# print('state_grade: ' + str(state_grade))
							# Restoring the initial values
							agents.belieftree[1 + links.agent2.unique_id][issue_of_interest[issue_num]][0] = original_belief[0]
							# Re-updating the preference levels
							self.instrument_preference_update(agents, 1 + links.agent2.unique_id, AS_theory, len_DC, len_PC, len_S, instruments)
							# Adding the grade to the grade list
							total_grade_list.append(state_grade)
							# Reset to None after finding the grade
							if check_none == 1:
								agents.belieftree[1 + links.agent2.unique_id][issue_of_interest[issue_num]][0] = None

						if links.agent2 == agents:

							# Looking at the policy chosen by the agent.
							# Check if no partial knowledge (initial value)
							check_none = 0
							if agents.belieftree[1 + links.agent1.unique_id][issue_of_interest[issue_num]][0] == None:
								agents.belieftree[1 + links.agent1.unique_id][issue_of_interest[issue_num]][0] = 0
								check_none = 1
							# Memorising the original belief values
							original_belief = [0]
							original_belief[0] = copy.copy(agents.belieftree[1 + links.agent1.unique_id][issue_of_interest[issue_num]][0])
							# If it knows that the agent has no interest in this issue, then set the grade to 0
							if agents.belieftree[1 + links.agent1.unique_id][issue_of_interest[issue_num]][0] == 'No' or \
							  agents.belieftree[0][issue_of_interest[issue_num]][0] == 'No':
								state_grade = 0
							else:	
								# Performing the action
								# print(' ')
								# print('Old value of the aim: ' + str(agents.belieftree[1 + links.agent1.unique_id][issue_of_interest[issue_num]][0]))
								agents.belieftree[1 + links.agent1.unique_id][issue_of_interest[issue_num]][0] += \
									(agents.belieftree[0][issue_of_interest[issue_num]][0] - agents.belieftree[1 + links.agent1.unique_id][issue_of_interest[issue_num]][0]) * \
									agents.resources[0] * resources_weight_action * links.aware * links.conflict_level[0][issue_of_interest[issue_num]][0] * actionWeight * resources_potency
								# 1-1 check
								agents.belieftree[1 + links.agent1.unique_id][issue_of_interest[issue_num]][0] = \
									self.one_minus_one_check2(agents.belieftree[1 + links.agent1.unique_id][issue_of_interest[issue_num]][0])
								# Re-updating the preference levels
								self.instrument_preference_update(agents, 1 + links.agent1.unique_id, AS_theory, len_DC, len_PC, len_S, instruments)
								# Calculation of the new grade
								state_grade = abs(agents.instrument_preferences[0][agents.select_pinstrument] - agents.instrument_preferences[1 + links.agent1.unique_id][agents.select_pinstrument])
							# print('New value of the aim: ' + str(agents.belieftree[1 + links.agent1.unique_id][issue_of_interest[issue_num]][0]))
							# print('state_grade: ' + str(state_grade))
							# Restoring the initial values
							agents.belieftree[1 + links.agent1.unique_id][issue_of_interest[issue_num]][0] = original_belief[0]
							# Re-updating the preference levels
							self.instrument_preference_update(agents, 1 + links.agent1.unique_id, AS_theory, len_DC, len_PC, len_S, instruments)
							# Adding the grade to the grade list
							total_grade_list.append(state_grade)
							# Reset to None after finding the grade
							if check_none == 1:
								agents.belieftree[1 + links.agent1.unique_id][issue_of_interest[issue_num]][0] = None

			# print(' ')
			# print(total_grade_list)

			# 4. Choosing an action
			best_action_index = total_grade_list.index(min(total_grade_list))

			# print(' ')
			# print('------ New action grade check -------')
			# print('Grade length: ' + str(len(total_grade_list)))
			# print('Best index: ' + str(best_action_index))
			# print('Number of links: ' + str(len(total_grade_list_links)))
			# print('Number of grades per link: ' + str(len(cw_of_interest) + 2 * len(issue_of_interest)))
			# print('Link for this action: ' + str(int(best_action_index / (len(cw_of_interest) + 2 * len(issue_of_interest) ) )))
			
			best_action = best_action_index - ((len(cw_of_interest) + 2 * len(issue_of_interest)) * int(best_action_index / (len(cw_of_interest) + 2 * len(issue_of_interest) ) ))
			# print('Best action selected: ' + str(best_action))

			for links in link_list:

				if links == total_grade_list_links[int(best_action_index / (len(cw_of_interest) + 2 * len(issue_of_interest) ) )]:
					# print(links)					

					# 5. Performing the actual action
					# If the index is in the first part of the list, then the framing action is the best
					if best_action <= len(cw_of_interest) - 1:

						# print(' ')
						# print('Framing action - causal relation')
						# print('best_action: ' + str(best_action))
						# print('of_interest[0]: ' + str(of_interest[0]))
						# print('of_interest[0][best_action]: ' + str(of_interest[0][best_action]))

						# Update of the aware decay parameter
						links.aware_decay = 5

						if links.agent1 == agents:
							# print('Before: ' + str(links.agent2.belieftree[0][len(self.deep_core) + len(self.policy_core) + len(self.secondary) + best_action][0]))
							links.agent2.belieftree[0][of_interest[0][best_action]][0] += \
								(agents.belieftree[0][of_interest[0][best_action]][0] - links.agent2.belieftree[0][of_interest[0][best_action]][0]) * \
								agents.resources[0] * resources_weight_action * links.aware * resources_potency
							# print('After: ' + str(links.agent2.belieftree[0][len(self.deep_core) + len(self.policy_core) + len(self.secondary) + best_action][0]))
							# 1-1 check
							if links.agent2.belieftree[0][of_interest[0][best_action]][0] > 1:
								links.agent2.belieftree[0][of_interest[0][best_action]][0] = 1
							if links.agent2.belieftree[0][of_interest[0][best_action]][0] < - 1:
								links.agent2.belieftree[0][of_interest[0][best_action]][0] = -1
							# self.one_minus_one_check(links.agent2.belieftree[0][of_interest[0][best_action]][0])
							# Providing partial knowledge - Framing - 0.2 range from real value: (Acting agent)
							agents.belieftree[1 + links.agent2.unique_id][of_interest[0][best_action]][0] = links.agent2.belieftree[0][of_interest[0][best_action]][0] + (random.random()/5) - 0.1
							# 1-1 check
							if agents.belieftree[1 + links.agent2.unique_id][of_interest[0][best_action]][0] > 1:
								agents.belieftree[1 + links.agent2.unique_id][of_interest[0][best_action]][0] = 1
							if agents.belieftree[1 + links.agent2.unique_id][of_interest[0][best_action]][0] < -1:
								agents.belieftree[1 + links.agent2.unique_id][of_interest[0][best_action]][0] = -1
							# self.one_minus_one_check(agents.belieftree[1 + links.agent2.unique_id][of_interest[0][best_action]][0])
							# Providing partial knowledge - Framing - 0.2 range from real value: (Acted upon agent)
							links.agent2.belieftree[1 + agents.unique_id][of_interest[0][best_action]][0] = agents.belieftree[0][of_interest[0][best_action]][0] + (random.random()/5) - 0.1
							# 1-1 check
							if links.agent2.belieftree[1 + agents.unique_id][of_interest[0][best_action]][0] > 1:
								links.agent2.belieftree[1 + agents.unique_id][of_interest[0][best_action]][0] = 1
							if links.agent2.belieftree[1 + agents.unique_id][of_interest[0][best_action]][0] < -1:
								links.agent2.belieftree[1 + agents.unique_id][of_interest[0][best_action]][0] = -1
							# self.one_minus_one_check(links.agent2.belieftree[1 + agents.unique_id][of_interest[0][best_action]][0])

						# Checking which agent in the link is the original agent
						if links.agent2 == agents:
							# print('Before: ' + str(links.agent1.belieftree[0][len(self.deep_core) + len(self.policy_core) + len(self.secondary) + best_action][0]))
							links.agent1.belieftree[0][of_interest[0][best_action]][0] += \
								(agents.belieftree[0][of_interest[0][best_action]][0] - links.agent1.belieftree[0][of_interest[0][best_action]][0]) * \
								agents.resources[0] * resources_weight_action * links.aware * resources_potency
							# print('After: ' + str(links.agent1.belieftree[0][len(self.deep_core) + len(self.policy_core) + len(self.secondary) + best_action][0]))
							# 1-1 check
							if links.agent1.belieftree[0][of_interest[0][best_action]][0] > 1:
								links.agent1.belieftree[0][of_interest[0][best_action]][0] = -1
							if links.agent1.belieftree[0][of_interest[0][best_action]][0] < -1:
								links.agent1.belieftree[0][of_interest[0][best_action]][0] = -1
							# self.one_minus_one_check(links.agent1.belieftree[0][of_interest[0][best_action]][0])
							# Providing partial knowledge - Framing - 0.2 range from real value: (Acting agent)
							agents.belieftree[1 + links.agent1.unique_id][of_interest[0][best_action]][0] = links.agent1.belieftree[0][of_interest[0][best_action]][0] + (random.random()/5) - 0.1
							# 1-1 check
							if agents.belieftree[1 + links.agent1.unique_id][of_interest[0][best_action]][0] > 1:
								agents.belieftree[1 + links.agent1.unique_id][of_interest[0][best_action]][0] = 1
							if agents.belieftree[1 + links.agent1.unique_id][of_interest[0][best_action]][0] < -1:
								agents.belieftree[1 + links.agent1.unique_id][of_interest[0][best_action]][0] = -1
							# self.one_minus_one_check(agents.belieftree[1 + links.agent1.unique_id][of_interest[0][best_action]][0])
							# Providing partial knowledge - Framing - 0.2 range from real value: (Acted upon agent)
							links.agent1.belieftree[1 + agents.unique_id][of_interest[0][best_action]][0] = agents.belieftree[0][of_interest[0][best_action]][0] + (random.random()/5) - 0.1
							# 1-1 check
							if links.agent1.belieftree[1 + agents.unique_id][of_interest[0][best_action]][0] > 1:
								links.agent1.belieftree[1 + agents.unique_id][of_interest[0][best_action]][0] = 1
							if links.agent1.belieftree[1 + agents.unique_id][of_interest[0][best_action]][0] < -1:
								links.agent1.belieftree[1 + agents.unique_id][of_interest[0][best_action]][0] = -1
							# self.one_minus_one_check(links.agent1.belieftree[1 + agents.unique_id][of_interest[0][best_action]][0])

					# If the index is in the second part of the list, then the aim influence action on the problem is the best
					if best_action > len(cw_of_interest) - 1 and best_action < len(cw_of_interest) + len(issue_of_interest) - 1:

						# print(' ')
						# print('Aim influence action')
						# print('best_action: ' + str(best_action))
						# print('of_interest[1]: ' + str(of_interest[1]))
						# print('of_interest[1][best_action - len(cw_of_interest)]: ' + str(of_interest[1][best_action - len(cw_of_interest)]))
						
						# Update of the aware decay parameter
						links.aware_decay = 5

						if links.agent1 == agents:
							links.agent2.belieftree[0][of_interest[1][best_action - len(cw_of_interest)] ][1] += \
								(agents.belieftree[0][of_interest[1][best_action - len(cw_of_interest)] ][1] - links.agent2.belieftree[0][agenda_as_issue][1]) * \
								agents.resources[0] * resources_weight_action * links.aware * resources_potency
							# 1-1 check
							links.agent2.belieftree[0][of_interest[1][best_action - len(cw_of_interest)]][1] = \
								self.one_minus_one_check2(links.agent2.belieftree[0][of_interest[1][best_action - len(cw_of_interest)]][1])		
							# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acting agent)
							agents.belieftree[1 + links.agent2.unique_id][of_interest[1][best_action - len(cw_of_interest)] ][1] = links.agent2.belieftree[0][of_interest[1][best_action - len(cw_of_interest)] ][1] + (random.random()/5) - 0.1
							# 1-1 check
							agents.belieftree[1 + links.agent2.unique_id][of_interest[1][best_action - len(cw_of_interest)] ][1] = \
								self.one_minus_one_check2(agents.belieftree[1 + links.agent2.unique_id][of_interest[1][best_action - len(cw_of_interest)] ][1])
							# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acted upon agent)
							links.agent2.belieftree[1 + agents.unique_id][of_interest[1][best_action - len(cw_of_interest)] ][1] = agents.belieftree[0][of_interest[1][best_action - len(cw_of_interest)] ][1] + (random.random()/5) - 0.1
							# 1-1 check
							links.agent2.belieftree[1 + agents.unique_id][of_interest[1][best_action - len(cw_of_interest)] ][1] = \
								self.one_minus_one_check2(links.agent2.belieftree[1 + agents.unique_id][of_interest[1][best_action - len(cw_of_interest)] ][1])

						if links.agent2 == agents:
							# print('Before: ' + str(links.agent1.belieftree[0][len(self.deep_core) + agents.select_problem][1]))
							links.agent1.belieftree[0][of_interest[1][best_action - len(cw_of_interest)] ][1] += \
								(agents.belieftree[0][of_interest[1][best_action - len(cw_of_interest)] ][1] - links.agent1.belieftree[0][of_interest[1][best_action - len(cw_of_interest)] ][1]) * \
								agents.resources[0] * resources_weight_action * links.aware * resources_potency
							# print('After: ' + str(links.agent1.belieftree[0][len(self.deep_core) + agents.select_problem][1]))
							# 1-1 check
							links.agent1.belieftree[0][of_interest[1][best_action - len(cw_of_interest)]][1] = \
								self.one_minus_one_check2(links.agent1.belieftree[0][of_interest[1][best_action - len(cw_of_interest)]][1]   )		
							# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acting agent)
							agents.belieftree[1 + links.agent1.unique_id][of_interest[1][best_action - len(cw_of_interest)]][1] = links.agent1.belieftree[0][of_interest[1][best_action - len(cw_of_interest)] ][1] + (random.random()/5) - 0.1
							# 1-1 check
							agents.belieftree[1 + links.agent1.unique_id][of_interest[1][best_action - len(cw_of_interest)]][1] = \
								self.one_minus_one_check2(agents.belieftree[1 + links.agent1.unique_id][of_interest[1][best_action - len(cw_of_interest)]][1])
							# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acted upon agent)
							links.agent1.belieftree[1 + agents.unique_id][of_interest[1][best_action - len(cw_of_interest)] ][1] = agents.belieftree[0][of_interest[1][best_action - len(cw_of_interest)] ][1] + (random.random()/5) - 0.1
							# 1-1 check
							links.agent1.belieftree[1 + agents.unique_id][of_interest[1][best_action - len(cw_of_interest)] ][1] = \
								self.one_minus_one_check2(links.agent1.belieftree[1 + agents.unique_id][of_interest[1][best_action - len(cw_of_interest)] ][1])

					# If the index is in the first part of the list, then the aim influence action on the policy is the best
					if best_action >= len(cw_of_interest) + len(issue_of_interest) - 1:

						# print(' ')
						# print('Aim influence action')
						# print('best_action: ' + str(best_action))
						# print('of_interest[1]: ' + str(of_interest[1]))
						# print('of_interest[1][best_action - len(cw_of_interest) - len(issue_of_interest)]: ' + str(of_interest[1][best_action - len(cw_of_interest) - len(issue_of_interest)]))

						# Update of the aware decay parameter
						links.aware_decay = 5

						if links.agent1 == agents:
							links.agent2.belieftree[0][of_interest[1][best_action - len(cw_of_interest) - len(issue_of_interest)]][0] += \
								(agents.belieftree[0][of_interest[1][best_action - len(cw_of_interest) - len(issue_of_interest)]][0] - \
								links.agent2.belieftree[0][of_interest[1][best_action - len(cw_of_interest) - len(issue_of_interest)]][1]) * \
								agents.resources[0] * resources_weight_action * links.aware * resources_potency
							# 1-1 check
							links.agent2.belieftree[0][of_interest[1][best_action - len(cw_of_interest) - len(issue_of_interest)]][0] = \
								self.one_minus_one_check2(links.agent2.belieftree[0][of_interest[1][best_action - len(cw_of_interest) - len(issue_of_interest)]][0])
							# Providing partial knowledge - Aim policy - 0.2 range from real value: (Acting agent)
							agents.belieftree[1 + links.agent2.unique_id][of_interest[1][best_action - len(cw_of_interest) - len(issue_of_interest)]][0] = \
								links.agent2.belieftree[0][of_interest[1][best_action - len(cw_of_interest) - len(issue_of_interest)]][0] + (random.random()/5) - 0.1
							# 1-1 check
							agents.belieftree[1 + links.agent2.unique_id][of_interest[1][best_action - len(cw_of_interest) - len(issue_of_interest)]][0] = \
								self.one_minus_one_check2(agents.belieftree[1 + links.agent2.unique_id][of_interest[1][best_action - len(cw_of_interest) - len(issue_of_interest)]][0])
							# Providing partial knowledge - Aim policy - 0.2 range from real value: (Acted upon agent)
							links.agent2.belieftree[1 + agents.unique_id][of_interest[1][best_action - len(cw_of_interest) - len(issue_of_interest)]][0] = \
								agents.belieftree[0][of_interest[1][best_action - len(cw_of_interest) - len(issue_of_interest)]][0] + (random.random()/5) - 0.1
							# 1-1 check
							links.agent2.belieftree[1 + agents.unique_id][of_interest[1][best_action - len(cw_of_interest) - len(issue_of_interest)]][0] = \
								self.one_minus_one_check2(links.agent2.belieftree[1 + agents.unique_id][of_interest[1][best_action - len(cw_of_interest) - len(issue_of_interest)]][0])

						if links.agent2 == agents:
							links.agent1.belieftree[0][of_interest[1][best_action - len(cw_of_interest) - len(issue_of_interest)]][0] += \
								(agents.belieftree[0][of_interest[1][best_action - len(cw_of_interest) - len(issue_of_interest)]][0] - \
								links.agent1.belieftree[0][of_interest[1][best_action - len(cw_of_interest) - len(issue_of_interest)]][0]) * \
								agents.resources[0] * resources_weight_action * links.aware * resources_potency
							# 1-1 check
							links.agent1.belieftree[0][of_interest[1][best_action - len(cw_of_interest) - len(issue_of_interest)]][0] = \
								self.one_minus_one_check2(links.agent1.belieftree[0][of_interest[1][best_action - len(cw_of_interest) - len(issue_of_interest)]][0])
							# Providing partial knowledge - Aim policy - 0.2 range from real value: (Acting agent)
							agents.belieftree[1 + links.agent1.unique_id][of_interest[1][best_action - len(cw_of_interest) - len(issue_of_interest)]][0] = \
								links.agent1.belieftree[0][of_interest[1][best_action - len(cw_of_interest) - len(issue_of_interest)]][0] + (random.random()/5) - 0.1
							# 1-1 check
							agents.belieftree[1 + links.agent1.unique_id][of_interest[1][best_action - len(cw_of_interest) - len(issue_of_interest)]][0] = \
								self.one_minus_one_check2(agents.belieftree[1 + links.agent1.unique_id][of_interest[1][best_action - len(cw_of_interest) - len(issue_of_interest)]][0])
							# Providing partial knowledge - Aim policy - 0.2 range from real value: (Acted upon agent)
							links.agent1.belieftree[1 + agents.unique_id][of_interest[1][best_action - len(cw_of_interest) - len(issue_of_interest)]][0] = \
								agents.belieftree[0][of_interest[1][best_action - len(cw_of_interest) - len(issue_of_interest)]][0] + (random.random()/5) - 0.1
							# 1-1 check
							links.agent1.belieftree[1 + agents.unique_id][of_interest[1][best_action - len(cw_of_interest) - len(issue_of_interest)]][0] = \
								self.one_minus_one_check2(links.agent1.belieftree[1 + agents.unique_id][of_interest[1][best_action - len(cw_of_interest) - len(issue_of_interest)]][0])

			# print('Resources left: ' + str(agents.resources_actions))
			agents.resources_actions -= agents.resources[0] * resources_weight_action

	def pm_pe_actions_as_3S(self, agents, link_list, deep_core, policy_core, secondary, resources_weight_action, resources_potency):

		len_DC = len(deep_core)
		len_PC = len(policy_core)
		len_S = len(secondary)

		# Selection of the cw of interest
		cw_of_interest = []
		# We only consider the causal relations related to the problem selected by the agent
		for cw_choice in range(len(deep_core)):
				cw_of_interest.append(len_DC + len_PC + len_S + (agents.select_problem_3S_as - len_DC) + cw_choice * len(policy_core))

		# Selection of the impact of interest
		impact_number = len(agents.belieftree_policy[0][agents.select_policy_3S_as])

		# print(' ')
		# print('Causal relations of interest: ' + str(cw_of_interest))

		# Making sure there are enough resources
		while agents.resources_actions > 0.001:

			# Going through all the links in the model
			# print(agents)
			total_grade_list = []
			total_grade_list_links = []
			for links in link_list:

				# Making sure that the link is attached to the agent and has a aware higher than 0
				if (links.agent1 == agents or links.agent2 == agents) and links.aware > 0:
					total_grade_list_links.append(links)

					# Definition the action weight parameter
					if type(links.agent1) == Policymakers or type(links.agent2) == Policymakers:
						actionWeight = 1
					else:
						actionWeight = 0.95
					
					# 1. Framing on causal relation and policy impacts

					# If the agent is advocating or a problem, the following tasks are performed
					if agents.select_issue_3S_as == 'problem':
						# 1.a. Grading all framing actions on causal relations:
						# Checking through all possible framing - This is all based on partial knowledge!
						for cw in range(len(cw_of_interest)):

							# Checking which agent in the link is the original agent
							if links.agent1 == agents:
								# Check if no partial knowledge (initial value)
								check_none = 0
								if agents.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0] == None:
									agents.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0] = 0
									check_none = 1
								# Performing the action
								cw_grade = (agents.belieftree[0][cw_of_interest[cw]][0] - agents.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0]) * \
									agents.resources[0] * resources_weight_action * links.aware * resources_potency
								# Adding the grade to the grade list
								total_grade_list.append(cw_grade)
								#  Reset to None after finding the grade
								if check_none == 1:
									agents.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0] = None

							# Checking which agent in the link is the original agent
							if links.agent2 == agents:
								#  Check if no partial knowledge (initial value)
								check_none = 0
								if agents.belieftree[1 + links.agent1.unique_id][cw_of_interest[cw]][0] == None:
									agents.belieftree[1 + links.agent1.unique_id][cw_of_interest[cw]][0] = 0
									check_none = 1
								# Performing the action
								cw_grade = (agents.belieftree[0][cw_of_interest[cw]][0] - agents.belieftree[1 + links.agent1.unique_id][cw_of_interest[cw]][0]) * \
									agents.resources[0] * resources_weight_action * links.aware * resources_potency
								# Adding the grade to the grade list
								total_grade_list.append(cw_grade)
								# Reset to None after finding the grade
								if check_none == 1:
									agents.belieftree[1 + links.agent1.unique_id][cw_of_interest[cw]][0] = None

					# If the agent is advocating or a policy, the following tasks are performed
					if agents.select_issue_3S_as == 'policy':
						# 1.b. Grading all framing actions on policy impacts:

						# Checking through all possible framing - This is all based on partial knowledge!
						for impact in range(impact_number):

							# Checking which agent in the link is the original agent
							if links.agent1 == agents:
								# Check if no partial knowledge (initial value)
								check_none = 0
								if agents.belieftree_policy[1 + links.agent2.unique_id][agents.select_policy_3S_as][impact] == None:
									agents.belieftree_policy[1 + links.agent2.unique_id][agents.select_policy_3S_as][impact] = 0
									check_none = 1
								# Performing the action
								impact_grade = (agents.belieftree_policy[0][agents.select_policy_3S_as][impact] - agents.belieftree_policy[1 + links.agent2.unique_id][agents.select_policy_3S_as][impact]) * \
									agents.resources[0] * resources_weight_action * links.aware * resources_potency
								# Adding the grade to the grade list
								total_grade_list.append(impact_grade)
								#  Reset to None after finding the grade
								if check_none == 1:
									agents.belieftree_policy[1 + links.agent2.unique_id][agents.select_policy_3S_as][impact] = None

							# Checking which agent in the link is the original agent
							if links.agent2 == agents:
								#  Check if no partial knowledge (initial value)
								check_none = 0
								if agents.belieftree_policy[1 + links.agent1.unique_id][agents.select_policy_3S_as][impact] == None:
									agents.belieftree_policy[1 + links.agent1.unique_id][agents.select_policy_3S_as][impact] = 0
									check_none = 1
								impact_grade = (agents.belieftree_policy[0][agents.select_policy_3S_as][impact] - agents.belieftree_policy[1 + links.agent1.unique_id][agents.select_policy_3S_as][impact]) * \
									agents.resources[0] * resources_weight_action * links.aware * resources_potency
								# Adding the grade to the grade list
								total_grade_list.append(impact_grade)
								# Reset to None after finding the grade
								if check_none == 1:
									agents.belieftree_policy[1 + links.agent1.unique_id][agents.select_policy_3S_as][impact] = None

					# 2. Grading all individual actions - Aim change
					if links.agent1 == agents:
						# Check if no partial knowledge (initial value)
						check_none = 0
						if agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][1] == None:
							agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][1] = 0
							check_none = 1
						# Performing the action
						aim_grade_issue = (agents.belieftree[0][agents.select_problem_3S_as][1] - agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][1]) * \
							agents.resources[0] * resources_weight_action * links.aware * links.conflict_level[0][agents.select_problem_3S_as][1] * actionWeight * resources_potency
						#  Reset to None after finding the grade
						if check_none == 1:
							agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][1] = None
						# Adding the grade to the grade list
						total_grade_list.append(aim_grade_issue)

					if links.agent2 == agents:
						# Check if no partial knowledge (initial value)
						check_none = 0
						if agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][1] == None:
							agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][1] = 0
							check_none = 1
						# Performing the action
						aim_grade_issue = (agents.belieftree[0][agents.select_problem_3S_as][1] - agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][1]) * \
							agents.resources[0] * resources_weight_action * links.aware * links.conflict_level[1][agents.select_problem_3S_as][1] * actionWeight * resources_potency
						#  Reset to None after finding the grade
						if check_none == 1:
							agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][1] = None
						# Adding the grade to the grade list
						total_grade_list.append(aim_grade_issue)

					# 3. Grading all individual actions - State change
					if links.agent1 == agents:
						# Check if no partial knowledge (initial value)
						check_none = 0
						if agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][0] == None:
							agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][0] = 0
							check_none = 1
						# Performing the action
						state_grade_issue = (agents.belieftree[0][agents.select_problem_3S_as][0] - agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][0]) * \
							agents.resources[0] * resources_weight_action * links.aware * links.conflict_level[0][agents.select_problem_3S_as][0] * actionWeight * resources_potency
						#  Reset to None after finding the grade
						if check_none == 1:
							agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][0] = None
						# Adding the grade to the grade list
						total_grade_list.append(state_grade_issue)

					if links.agent2 == agents:
						# Check if no partial knowledge (initial value)
						check_none = 0
						if agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][0] == None:
							agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][0] = 0
							check_none = 1
						# Performing the action
						state_grade_issue = (agents.belieftree[0][agents.select_problem_3S_as][0] - agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][0]) * \
							agents.resources[0] * resources_weight_action * links.aware * links.conflict_level[1][agents.select_problem_3S_as][0] * actionWeight * resources_potency
						#  Reset to None after finding the grade
						if check_none == 1:
							agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][0] = None
						# Adding the grade to the grade list
						total_grade_list.append(state_grade_issue)
					# print(' ')

			# print(' ')
			# print('Number of actions: ' + str(len(total_grade_list)))
			# print(total_grade_list)

			# 4. Choosing an action

			# If the agent is advocating or a problem, the following tasks are performed
			if agents.select_issue_3S_as == 'problem':

				best_action_index = total_grade_list.index(max(total_grade_list))
				agent_best_action = int(best_action_index/(len(cw_of_interest) + 1 + 1))
				best_action = best_action_index - (agent_best_action)*(len(cw_of_interest) + 1 + 1)

				# print(' ')
				# print('----- Considering new action grading (problem) -----')
				# print('best_action_index: ' + str(best_action_index))
				# print('Number of actions per agent: ' + str(len(cw_of_interest) + 1 + 1))
				# print('Total number of agents being influenced: ' + str(len(total_grade_list_links)))
				# print('Action to be performed: ' + str(best_action))
				# print('Agent performing the action: ' + str(agent_best_action))

			# If the agent is advocating or a policy, the following tasks are performed
			if agents.select_issue_3S_as == 'policy':
				
				best_action_index = total_grade_list.index(max(total_grade_list))
				agent_best_action = int(best_action_index/(impact_number + 1 + 1))
				best_action = best_action_index - (agent_best_action)*(impact_number + 1 + 1)

				# print(' ')
				# print('----- Considering new action grading (policy) -----')
				# print('best_action_index: ' + str(best_action_index))
				# print('Number of actions per agent: ' + str(impact_number + 1 + 1))
				# print('Total number of agents being influenced: ' + str(len(total_grade_list_links)))
				# print('Action to be performed: ' + str(best_action))
				# print('Agent performing the action: ' + str(agent_best_action))


			# 5. Performing the actual action
			# Selecting the link:
			for links in link_list:

				# If the agent is advocating or a problem, the following tasks are performed
				if agents.select_issue_3S_as == 'problem':

					if (links.agent1 == agents and links.agent2.unique_id == agent_best_action) or (links.agent1.unique_id == agent_best_action and links.agent2 == agents):
						# print(links)

						# Updating the aware decay parameter
						links.aware_decay = 5

						# If the index is in the first part of the list, then the framing action is the best
						if best_action <= len(cw_of_interest) - 1:
							# print(' ')
							# print('Performing a causal relation framing action')
							# print('best_action: ' + str(best_action))
							# print('cw_of_interest: ' + str(cw_of_interest))
							# print('cw_of_interest[best_action]: ' + str(cw_of_interest[best_action]))
							
							# To simplify the notations
							best_action = cw_of_interest[best_action]

							if links.agent1 == agents:
								
								# print('Before: ' + str(links.agent2.belieftree[0][best_action][0]))
								links.agent2.belieftree[0][best_action][0] += (agents.belieftree[0][best_action][0] - links.agent2.belieftree[0][best_action][0]) * \
									agents.resources[0] * resources_weight_action * links.aware * resources_potency
								# print('After: ' + str(links.agent2.belieftree[0][best_action][0]))
								# 1-1 check
								links.agent2.belieftree[0][best_action][0] = \
									self.one_minus_one_check2(links.agent2.belieftree[0][best_action][0])
								# Providing partial knowledge - Framing - 0.2 range from real value: (Acting agent)
								agents.belieftree[1 + links.agent2.unique_id][best_action][0] = links.agent2.belieftree[0][best_action][0] + (random.random()/5) - 0.1
								# 1-1 check
								agents.belieftree[1 + links.agent2.unique_id][best_action][0] = \
									self.one_minus_one_check2(agents.belieftree[1 + links.agent2.unique_id][best_action][0])
								# Providing partial knowledge - Framing - 0.2 range from real value: (Acted upon agent)
								links.agent2.belieftree[1 + agents.unique_id][best_action][0] = agents.belieftree[0][best_action][0] + (random.random()/5) - 0.1
								# 1-1 check
								links.agent2.belieftree[1 + agents.unique_id][best_action][0] = \
									self.one_minus_one_check2(links.agent2.belieftree[1 + agents.unique_id][best_action][0])

								# print(' ')
								# print('Causal change')
								# print(agents.belieftree[1 + links.agent2.unique_id])
								# print(agents.belieftree[1 + links.agent2.unique_id][best_action][0])

							# Checking which agent in the link is the original agent
							if links.agent2 == agents:

								# print('Before: ' + str(links.agent1.belieftree[0][best_action][0]))
								links.agent1.belieftree[0][best_action][0] += (agents.belieftree[0][best_action][0] - links.agent1.belieftree[0][best_action][0]) * \
									agents.resources[0] * resources_weight_action * links.aware * resources_potency
								# print('After: ' + str(links.agent1.belieftree[0][best_action][0]))
								# 1-1 check
								links.agent1.belieftree[0][best_action][0] = \
									self.one_minus_one_check2(links.agent1.belieftree[0][best_action][0])
								# Providing partial knowledge - Framing - 0.2 range from real value: (Acting agent)
								agents.belieftree[1 + links.agent1.unique_id][best_action][0] = links.agent1.belieftree[0][best_action][0] + (random.random()/5) - 0.1
								# 1-1 check
								agents.belieftree[1 + links.agent1.unique_id][best_action][0] = \
									self.one_minus_one_check2(agents.belieftree[1 + links.agent1.unique_id][best_action][0])
								# Providing partial knowledge - Framing - 0.2 range from real value: (Acted upon agent)
								links.agent1.belieftree[1 + agents.unique_id][best_action][0] = agents.belieftree[0][best_action][0] + (random.random()/5) - 0.1
								# 1-1 check
								links.agent1.belieftree[1 + agents.unique_id][best_action][0] = \
									self.one_minus_one_check2(links.agent1.belieftree[1 + agents.unique_id][best_action][0])

								# print(' ')
								# print('Causal change')
								# print(agents.belieftree[1 + links.agent1.unique_id])
								# print(agents.belieftree[1 + links.agent1.unique_id][best_action][0])

						# If the index is in the second part of the list, then the aim influence action is the best
						if best_action == len(cw_of_interest):
							# print(' ')
							# print('Performing a state change action')
							# print('best_action: ' + str(best_action))

							if links.agent1 == agents:
								# print('Before: ' + str(links.agent2.belieftree[0][agents.select_problem_3S_as][1]))
								links.agent2.belieftree[0][agents.select_problem_3S_as][1] += (agents.belieftree[0][agents.select_problem_3S_as][1] - links.agent2.belieftree[0][agents.select_problem_3S_as][1]) * \
									agents.resources[0] * resources_weight_action * links.aware * resources_potency
								# print('After: ' + str(links.agent2.belieftree[0][agents.select_problem_3S_as][1]))
								# 1-1 check
								links.agent2.belieftree[0][agents.select_problem_3S_as][1] = \
									self.one_minus_one_check2(links.agent2.belieftree[0][agents.select_problem_3S_as][1])
								# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acting agent)
								agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][1] = links.agent2.belieftree[0][agents.select_problem_3S_as][1]
								# 1-1 check
								agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][1] = \
									self.one_minus_one_check2(agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][1])
								# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acted upon agent)
								links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][1] = agents.belieftree[0][agents.select_problem_3S_as][1] + (random.random()/5) - 0.1
								# 1-1 check
								links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][1] = \
									self.one_minus_one_check2(links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][1])

								# print(' ')
								# print('Aim change')
								# print(agents.belieftree[1 + links.agent2.unique_id])

							if links.agent2 == agents:

								# print('Before: ' + str(links.agent1.belieftree[0][agents.select_problem_3S_as][1]))
								links.agent1.belieftree[0][agents.select_problem_3S_as][1] += (agents.belieftree[0][agents.select_problem_3S_as][1] - links.agent1.belieftree[0][agents.select_problem_3S_as][1]) * \
									agents.resources[0] * resources_weight_action * links.aware * resources_potency
								# print('After: ' + str(links.agent1.belieftree[0][agents.select_problem_3S_as][1]))
								# 1-1 check
								links.agent1.belieftree[0][agents.select_problem_3S_as][1] = \
									self.one_minus_one_check2(links.agent1.belieftree[0][agents.select_problem_3S_as][1])
								# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acting agent)
								agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][1] = links.agent2.belieftree[0][agents.select_problem_3S_as][1]
								# 1-1 check
								agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][1] = \
									self.one_minus_one_check2(agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][1])
								# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acted upon agent)
								links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][1] = agents.belieftree[0][agents.select_problem_3S_as][1] + (random.random()/5) - 0.1
								# 1-1 check
								links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][1] = \
									self.one_minus_one_check2(links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][1])


						# If the index is in the first part of the list, then the state influence action is the best
						if best_action == len(cw_of_interest) + 1:
							# print(' ')
							# print('Performing an aim change action')
							# print('best_action: ' + str(best_action))

							if links.agent1 == agents:
								# print('Before: ' + str(links.agent2.belieftree[0][len(self.deep_core) + agents.select_problem][0]))
								links.agent2.belieftree[0][agents.select_problem_3S_as][0] += (agents.belieftree[0][agents.select_problem_3S_as][0] - links.agent2.belieftree[0][agents.select_problem_3S_as][0]) * \
									agents.resources[0] * resources_weight_action * links.aware * resources_potency
								# print('After: ' + str(links.agent2.belieftree[0][len(self.deep_core) + agents.select_problem][0]))
								links.agent2.belieftree[0][agents.select_problem_3S_as][0] = \
									self.one_minus_one_check2(links.agent2.belieftree[0][agents.select_problem_3S_as][0])
								# Providing partial knowledge - State problem - 0.2 range from real value: (Acting agent)
								agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][0] = links.agent2.belieftree[0][agents.select_problem_3S_as][0] + (random.random()/5) - 0.1
								# 1-1 check
								agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][0] = \
									self.one_minus_one_check2(agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][0])
								# Providing partial knowledge - State problem - 0.2 range from real value: (Acted upon agent)
								links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][0] = agents.belieftree[0][agents.select_problem_3S_as][0] + (random.random()/5) - 0.1
								# 1-1 check
								links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][0] = \
									self.one_minus_one_check2(links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][0])

								# print(' ')
								# print('State change')
								# print(agents.belieftree[1 + links.agent2.unique_id])

							if links.agent2 == agents:
								# print('Before: ' + str(links.agent1.belieftree[0][len(self.deep_core) + agents.select_problem][0]))
								links.agent1.belieftree[0][agents.select_problem_3S_as][0] += (agents.belieftree[0][agents.select_problem_3S_as][0] - links.agent1.belieftree[0][agents.select_problem_3S_as][0]) * \
									agents.resources[0] * resources_weight_action * links.aware * resources_potency
								# print('After: ' + str(links.agent1.belieftree[0][len(self.deep_core) + agents.select_problem][0]))
								# 1-1 check
								links.agent1.belieftree[0][agents.select_problem_3S_as][0] = \
									self.one_minus_one_check2(links.agent1.belieftree[0][agents.select_problem_3S_as][0])
								# Providing partial knowledge - State problem - 0.2 range from real value: (Acting agent)
								agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][0] = links.agent1.belieftree[0][agents.select_problem_3S_as][0] + (random.random()/5) - 0.1
								# 1-1 check
								agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][0] = \
									self.one_minus_one_check2(agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][0])
								# Providing partial knowledge - State problem - 0.2 range from real value: (Acted upon agent)
								links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][0] = agents.belieftree[0][agents.select_problem_3S_as][0] + (random.random()/5) - 0.1
								# 1-1 check
								links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][0] = \
									self.one_minus_one_check2(links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][0])

								# print(' ')
								# print('State change')
								# print(agents.belieftree[1 + links.agent1.unique_id])

				# If the agent is advocating or a policy, the following tasks are performed
				if agents.select_issue_3S_as == 'policy':
					
					if (links.agent1 == agents and links.agent2.unique_id == agent_best_action) or (links.agent1.unique_id == agent_best_action and links.agent2 == agents):
						# print(links)

						# Updating the aware decay parameter
						links.aware_decay = 5

						# If the index is in the first part of the list, then the framing action is the best
						if best_action <= impact_number - 1:
							# print(' ')
							# print('Performing a causal relation framing action')
							# print('best_action: ' + str(best_action))
							# print('impact_number: ' + str(impact_number))

							if links.agent1 == agents:
								
								# print('Before: ' + str(links.agent2.belieftree_policy[0][agents.select_policy_3S_as][best_action]))
								links.agent2.belieftree_policy[0][agents.select_policy_3S_as][best_action] += (agents.belieftree[0][agents.select_policy_3S_as][best_action] - \
									links.agent2.belieftree_policy[0][agents.select_policy_3S_as][best_action]) * \
									agents.resources[0] * resources_weight_action * links.aware * resources_potency
								# print('After: ' + str(links.agent2.belieftree_policy[0][agents.select_policy_3S_as][best_action]))
								# 1-1 check
								links.agent2.belieftree_policy[0][agents.select_policy_3S_as][best_action] = \
									self.one_minus_one_check2(links.agent2.belieftree_policy[0][agents.select_policy_3S_as][best_action])
								# Providing partial knowledge - Framing - 0.2 range from real value: (Acting agent)
								agents.belieftree_policy[1 + links.agent2.unique_id][agents.select_policy_3S_as][best_action] = links.agent2.belieftree_policy[0][agents.select_policy_3S_as][best_action] + (random.random()/5) - 0.1
								# 1-1 check
								agents.belieftree_policy[1 + links.agent2.unique_id][agents.select_policy_3S_as][best_action] = \
									self.one_minus_one_check2(agents.belieftree_policy[1 + links.agent2.unique_id][agents.select_policy_3S_as][best_action])
								# Providing partial knowledge - Framing - 0.2 range from real value: (Acted upon agent)
								links.agent2.belieftree_policy[1 + agents.unique_id][agents.select_policy_3S_as][best_action] = agents.belieftree_policy[0][agents.select_policy_3S_as][best_action] + (random.random()/5) - 0.1
								# 1-1 check
								links.agent2.belieftree_policy[1 + agents.unique_id][agents.select_policy_3S_as][best_action] = \
									self.one_minus_one_check2(links.agent2.belieftree_policy[1 + agents.unique_id][agents.select_policy_3S_as][best_action])

								# print(' ')
								# print('Causal change')
								# print(agents.belieftree_policy[1 + links.agent2.unique_id])
								# print(agents.belieftree_policy[1 + links.agent2.unique_id][agents.select_policy_3S_as][best_action])

							# Checking which agent in the link is the original agent
							if links.agent2 == agents:

								# print('Before: ' + str(links.agent1.belieftree_policy[0][agents.select_policy_3S_as][best_action]))
								links.agent1.belieftree_policy[0][agents.select_policy_3S_as][best_action] += (agents.belieftree_policy[0][agents.select_policy_3S_as][best_action] - \
									links.agent1.belieftree_policy[0][agents.select_policy_3S_as][best_action]) * \
									agents.resources[0] * resources_weight_action * links.aware * resources_potency
								# print('After: ' + str(links.agent1.belieftree_policy[0][agents.select_policy_3S_as][best_action]))
								# 1-1 check
								links.agent1.belieftree_policy[0][agents.select_policy_3S_as][best_action] = \
									self.one_minus_one_check2(links.agent1.belieftree_policy[0][agents.select_policy_3S_as][best_action])
								# Providing partial knowledge - Framing - 0.2 range from real value: (Acting agent)
								agents.belieftree_policy[1 + links.agent1.unique_id][agents.select_policy_3S_as][best_action] = links.agent1.belieftree_policy[0][agents.select_policy_3S_as][best_action] + (random.random()/5) - 0.1
								# 1-1 check
								agents.belieftree_policy[1 + links.agent1.unique_id][agents.select_policy_3S_as][best_action] = \
									self.one_minus_one_check2(agents.belieftree_policy[1 + links.agent1.unique_id][agents.select_policy_3S_as][best_action])
								# Providing partial knowledge - Framing - 0.2 range from real value: (Acted upon agent)
								links.agent1.belieftree_policy[1 + agents.unique_id][agents.select_policy_3S_as][best_action] = agents.belieftree_policy[0][agents.select_policy_3S_as][best_action] + (random.random()/5) - 0.1
								# 1-1 check
								links.agent1.belieftree_policy[1 + agents.unique_id][agents.select_policy_3S_as][best_action] = \
									self.one_minus_one_check2(links.agent1.belieftree_policy[1 + agents.unique_id][agents.select_policy_3S_as][best_action])

								# print(' ')
								# print('Causal change')
								# print(agents.belieftree_policy[1 + links.agent1.unique_id])
								# print(agents.belieftree_policy[1 + links.agent1.unique_id][agents.select_policy_3S_as][best_action])

						# If the index is in the second part of the list, then the aim influence action is the best
						if best_action == impact_number:
							# print(' ')
							# print('Performing a state change action')
							# print('best_action: ' + str(best_action))

							if links.agent1 == agents:
								# print('Before: ' + str(links.agent2.belieftree[0][agents.select_problem_3S_as][1]))
								links.agent2.belieftree[0][agents.select_problem_3S_as][1] += (agents.belieftree[0][agents.select_problem_3S_as][1] - links.agent2.belieftree[0][agents.select_problem_3S_as][1]) * \
									agents.resources[0] * resources_weight_action * links.aware * resources_potency
								# print('After: ' + str(links.agent2.belieftree[0][agents.select_problem_3S_as][1]))
								# 1-1 check
								links.agent2.belieftree[0][agents.select_problem_3S_as][1] = \
									self.one_minus_one_check2(links.agent2.belieftree[0][agents.select_problem_3S_as][1])
								# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acting agent)
								agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][1] = links.agent2.belieftree[0][agents.select_problem_3S_as][1]
								# 1-1 check
								agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][1] = \
									self.one_minus_one_check2(agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][1])
								# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acted upon agent)
								links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][1] = agents.belieftree[0][agents.select_problem_3S_as][1] + (random.random()/5) - 0.1
								# 1-1 check
								links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][1] = \
									self.one_minus_one_check2(links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][1])

								# print(' ')
								# print('Aim change')
								# print(agents.belieftree[1 + links.agent2.unique_id])

							if links.agent2 == agents:

								# print('Before: ' + str(links.agent1.belieftree[0][agents.select_problem_3S_as][1]))
								links.agent1.belieftree[0][agents.select_problem_3S_as][1] += (agents.belieftree[0][agents.select_problem_3S_as][1] - links.agent1.belieftree[0][agents.select_problem_3S_as][1]) * \
									agents.resources[0] * resources_weight_action * links.aware * resources_potency
								# print('After: ' + str(links.agent1.belieftree[0][agents.select_problem_3S_as][1]))
								# 1-1 check
								links.agent1.belieftree[0][agents.select_problem_3S_as][1] = \
									self.one_minus_one_check2(links.agent1.belieftree[0][agents.select_problem_3S_as][1])
								# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acting agent)
								agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][1] = links.agent2.belieftree[0][agents.select_problem_3S_as][1]
								# 1-1 check
								agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][1] = \
									self.one_minus_one_check2(agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][1])
								# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acted upon agent)
								links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][1] = agents.belieftree[0][agents.select_problem_3S_as][1] + (random.random()/5) - 0.1
								# 1-1 check
								links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][1] = \
									self.one_minus_one_check2(links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][1])


						# If the index is in the first part of the list, then the state influence action is the best
						if best_action == impact_number + 1:
							# print(' ')
							# print('Performing an aim change action')
							# print('best_action: ' + str(best_action))

							if links.agent1 == agents:
								# print('Before: ' + str(links.agent2.belieftree[0][len(self.deep_core) + agents.select_problem][0]))
								links.agent2.belieftree[0][agents.select_problem_3S_as][0] += (agents.belieftree[0][agents.select_problem_3S_as][0] - links.agent2.belieftree[0][agents.select_problem_3S_as][0]) * \
									agents.resources[0] * resources_weight_action * links.aware * resources_potency
								# print('After: ' + str(links.agent2.belieftree[0][len(self.deep_core) + agents.select_problem][0]))
								links.agent2.belieftree[0][agents.select_problem_3S_as][0] = \
									self.one_minus_one_check2(links.agent2.belieftree[0][agents.select_problem_3S_as][0])
								# Providing partial knowledge - State problem - 0.2 range from real value: (Acting agent)
								agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][0] = links.agent2.belieftree[0][agents.select_problem_3S_as][0] + (random.random()/5) - 0.1
								# 1-1 check
								agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][0] = \
									self.one_minus_one_check2(agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][0])
								# Providing partial knowledge - State problem - 0.2 range from real value: (Acted upon agent)
								links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][0] = agents.belieftree[0][agents.select_problem_3S_as][0] + (random.random()/5) - 0.1
								# 1-1 check
								links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][0] = \
									self.one_minus_one_check2(links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][0])

								# print(' ')
								# print('State change')
								# print(agents.belieftree[1 + links.agent2.unique_id])

							if links.agent2 == agents:
								# print('Before: ' + str(links.agent1.belieftree[0][len(self.deep_core) + agents.select_problem][0]))
								links.agent1.belieftree[0][agents.select_problem_3S_as][0] += (agents.belieftree[0][agents.select_problem_3S_as][0] - links.agent1.belieftree[0][agents.select_problem_3S_as][0]) * \
									agents.resources[0] * resources_weight_action * links.aware * resources_potency
								# print('After: ' + str(links.agent1.belieftree[0][len(self.deep_core) + agents.select_problem][0]))
								# 1-1 check
								links.agent1.belieftree[0][agents.select_problem_3S_as][0] = \
									self.one_minus_one_check2(links.agent1.belieftree[0][agents.select_problem_3S_as][0])
								# Providing partial knowledge - State problem - 0.2 range from real value: (Acting agent)
								agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][0] = links.agent1.belieftree[0][agents.select_problem_3S_as][0] + (random.random()/5) - 0.1
								# 1-1 check
								agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][0] = \
									self.one_minus_one_check2(agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][0])
								# Providing partial knowledge - State problem - 0.2 range from real value: (Acted upon agent)
								links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][0] = agents.belieftree[0][agents.select_problem_3S_as][0] + (random.random()/5) - 0.1
								# 1-1 check
								links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][0] = \
									self.one_minus_one_check2(links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][0])

								# print(' ')
								# print('State change')
								# print(agents.belieftree[1 + links.agent1.unique_id])


			# agents.resources_actions -= agents.resources
			agents.resources_actions -= agents.resources[0] * resources_weight_action

	def pm_pe_actions_pf_3S(self, agents, link_list, deep_core, policy_core, secondary, resources_weight_action, resources_potency, agenda_prob_3S_as):

		len_DC = len(deep_core)
		len_PC = len(policy_core)
		len_S = len(secondary)

		# Selection of the cw of interest
		cw_of_interest = []
		# Select one by one the DC
		j = agenda_prob_3S_as
		# for j in range(len_PC):
		# Selecting the causal relations starting from DC
		for k in range(len_S):
			# Contingency for partial knowledge issues
			# print(len_DC + len_PC + len_S + len_PC*len_DC + (j-len_DC) + k*len_PC)
			if (agents.belieftree[0][len_DC + len_PC + len_S + len_PC*len_DC + (j-len_DC) + k*len_PC][0] < 0 and (agents.belieftree[0][j][1] - agents.belieftree[0][j][0]) < 0) \
			  or (agents.belieftree[0][len_DC + len_PC + len_S + len_PC*len_DC + (j-len_DC) + k*len_PC][0] > 0 and (agents.belieftree[0][j][1] - agents.belieftree[0][j][0]) > 0):
				cw_of_interest.append(len_DC + len_PC + len_S + len_PC*len_DC + (j-len_DC) + k*len_PC)

		# Selection of the impact of interest
		impact_number = len(agents.belieftree_instrument[0][agents.select_policy_3S_pf])

		# print(' ')
		# print('Causal relations of interest: ' + str(cw_of_interest))

		# Making sure there are enough resources
		while agents.resources_actions > 0.001:

			# Going through all the links in the model
			# print(agents)
			total_grade_list = []
			total_grade_list_links = []
			for links in link_list:

				# Making sure that the link is attached to the agent and has a aware higher than 0
				if (links.agent1 == agents or links.agent2 == agents) and links.aware > 0:
					total_grade_list_links.append(links)

					# Definition the action weight parameter
					if type(links.agent1) == Policymakers or type(links.agent2) == Policymakers:
						actionWeight = 1
					else:
						actionWeight = 0.95
					
					# 1. Framing on causal relation and policy impacts

					# If the agent is advocating or a problem, the following tasks are performed
					if agents.select_issue_3S_pf == 'problem':
						# 1.a. Grading all framing actions on causal relations:
						# Checking through all possible framing - This is all based on partial knowledge!
						for cw in range(len(cw_of_interest)):

							# Checking which agent in the link is the original agent
							if links.agent1 == agents:
								# Check if no partial knowledge (initial value)
								check_none = 0
								if agents.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0] == None:
									agents.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0] = 0
									check_none = 1
								# Performing the action
								cw_grade = (agents.belieftree[0][cw_of_interest[cw]][0] - agents.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0]) * \
									agents.resources[0] * resources_weight_action * links.aware * resources_potency
								# Adding the grade to the grade list
								total_grade_list.append(cw_grade)
								#  Reset to None after finding the grade
								if check_none == 1:
									agents.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0] = None

							# Checking which agent in the link is the original agent
							if links.agent2 == agents:
								#  Check if no partial knowledge (initial value)
								check_none = 0
								if agents.belieftree[1 + links.agent1.unique_id][cw_of_interest[cw]][0] == None:
									agents.belieftree[1 + links.agent1.unique_id][cw_of_interest[cw]][0] = 0
									check_none = 1
								# Performing the action
								cw_grade = (agents.belieftree[0][cw_of_interest[cw]][0] - agents.belieftree[1 + links.agent1.unique_id][cw_of_interest[cw]][0]) * \
									agents.resources[0] * resources_weight_action * links.aware * resources_potency
								# Adding the grade to the grade list
								total_grade_list.append(cw_grade)
								# Reset to None after finding the grade
								if check_none == 1:
									agents.belieftree[1 + links.agent1.unique_id][cw_of_interest[cw]][0] = None

					# If the agent is advocating or a policy, the following tasks are performed
					if agents.select_issue_3S_pf == 'policy':
						# 1.b. Grading all framing actions on policy impacts:
						
						# Checking through all possible framing - This is all based on partial knowledge!
						for impact in range(impact_number):

							# Checking which agent in the link is the original agent
							if links.agent1 == agents:
								# Check if no partial knowledge (initial value)
								check_none = 0
								if agents.belieftree_instrument[1 + links.agent2.unique_id][agents.select_policy_3S_pf][impact] == None:
									agents.belieftree_instrument[1 + links.agent2.unique_id][agents.select_policy_3S_pf][impact] = 0
									check_none = 1
								# Performing the action
								impact_grade = (agents.belieftree_instrument[0][agents.select_policy_3S_pf][impact] - agents.belieftree_instrument[1 + links.agent2.unique_id][agents.select_policy_3S_pf][impact]) * \
									agents.resources[0] * resources_weight_action * links.aware * resources_potency
								# Adding the grade to the grade list
								total_grade_list.append(impact_grade)
								#  Reset to None after finding the grade
								if check_none == 1:
									agents.belieftree_instrument[1 + links.agent2.unique_id][agents.select_policy_3S_pf][impact] = None

							# Checking which agent in the link is the original agent
							if links.agent2 == agents:
								#  Check if no partial knowledge (initial value)
								check_none = 0
								if agents.belieftree_instrument[1 + links.agent1.unique_id][agents.select_policy_3S_pf][impact] == None:
									agents.belieftree_instrument[1 + links.agent1.unique_id][agents.select_policy_3S_pf][impact] = 0
									check_none = 1
								impact_grade = (agents.belieftree_instrument[0][agents.select_policy_3S_pf][impact] - agents.belieftree_instrument[1 + links.agent1.unique_id][agents.select_policy_3S_pf][impact]) * \
									agents.resources[0] * resources_weight_action * links.aware * resources_potency
								# Adding the grade to the grade list
								total_grade_list.append(impact_grade)
								# Reset to None after finding the grade
								if check_none == 1:
									agents.belieftree_instrument[1 + links.agent1.unique_id][agents.select_policy_3S_pf][impact] = None

					# 2. Grading all individual actions - Aim change
					if links.agent1 == agents:
						# Check if no partial knowledge (initial value)
						check_none = 0
						if agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][1] == None:
							agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][1] = 0
							check_none = 1
						# Performing the action
						aim_grade_issue = (agents.belieftree[0][agents.select_problem_3S_pf][1] - agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][1]) * \
							agents.resources[0] * resources_weight_action * links.aware * links.conflict_level[0][agents.select_problem_3S_pf][1] * actionWeight * resources_potency
						#  Reset to None after finding the grade
						if check_none == 1:
							agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][1] = None
						# Adding the grade to the grade list
						total_grade_list.append(aim_grade_issue)

					if links.agent2 == agents:
						# Check if no partial knowledge (initial value)
						check_none = 0
						if agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][1] == None:
							agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][1] = 0
							check_none = 1
						# Performing the action
						aim_grade_issue = (agents.belieftree[0][agents.select_problem_3S_pf][1] - agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][1]) * \
							agents.resources[0] * resources_weight_action * links.aware * links.conflict_level[1][agents.select_problem_3S_pf][1] * actionWeight * resources_potency
						#  Reset to None after finding the grade
						if check_none == 1:
							agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][1] = None
						# Adding the grade to the grade list
						total_grade_list.append(aim_grade_issue)

					# 3. Grading all individual actions - State change
					if links.agent1 == agents:
						# Check if no partial knowledge (initial value)
						check_none = 0
						if agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][0] == None:
							agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][0] = 0
							check_none = 1
						# Performing the action
						state_grade_issue = (agents.belieftree[0][agents.select_problem_3S_pf][0] - agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][0]) * \
							agents.resources[0] * resources_weight_action * links.aware * links.conflict_level[0][agents.select_problem_3S_pf][0] * actionWeight * resources_potency
						#  Reset to None after finding the grade
						if check_none == 1:
							agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][0] = None
						# Adding the grade to the grade list
						total_grade_list.append(state_grade_issue)

					if links.agent2 == agents:
						# Check if no partial knowledge (initial value)
						check_none = 0
						if agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][0] == None:
							agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][0] = 0
							check_none = 1
						# Performing the action
						state_grade_issue = (agents.belieftree[0][agents.select_problem_3S_pf][0] - agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][0]) * \
							agents.resources[0] * resources_weight_action * links.aware * links.conflict_level[1][agents.select_problem_3S_pf][0] * actionWeight * resources_potency
						#  Reset to None after finding the grade
						if check_none == 1:
							agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][0] = None
						# Adding the grade to the grade list
						total_grade_list.append(state_grade_issue)
					# print(' ')


			# 4. Choosing an action

			# If the agent is advocating or a problem, the following tasks are performed
			if agents.select_issue_3S_as == 'problem':

				best_action_index = total_grade_list.index(max(total_grade_list))
				agent_best_action = int(best_action_index/(len(cw_of_interest) + 1 + 1))
				best_action = best_action_index - (agent_best_action)*(len(cw_of_interest) + 1 + 1)

				# print(' ')
				# print('----- Considering new action grading (problem) -----')
				# print('best_action_index: ' + str(best_action_index))
				# print('Number of actions per agent: ' + str(len(cw_of_interest) + 1 + 1))
				# print('Total number of agents being influenced: ' + str(len(total_grade_list_links)))
				# print('Action to be performed: ' + str(best_action))
				# print('Agent performing the action: ' + str(agent_best_action))

			# If the agent is advocating or a policy, the following tasks are performed
			if agents.select_issue_3S_as == 'policy':
				
				best_action_index = total_grade_list.index(max(total_grade_list))
				agent_best_action = int(best_action_index/(impact_number + 1 + 1))
				best_action = best_action_index - (agent_best_action)*(impact_number + 1 + 1)

				# print(' ')
				# print('----- Considering new action grading (policy) -----')
				# print('best_action_index: ' + str(best_action_index))
				# print('Number of actions per agent: ' + str(impact_number + 1 + 1))
				# print('Total number of agents being influenced: ' + str(len(total_grade_list_links)))
				# print('Action to be performed: ' + str(best_action))
				# print('Agent performing the action: ' + str(agent_best_action))

			# 5. Performing the actual action
			# Selecting the link:
			for links in link_list:

				# If the agent is advocating or a problem, the following tasks are performed
				if agents.select_issue_3S_pf == 'problem':

					if (links.agent1 == agents and links.agent2.unique_id == agent_best_action) or (links.agent1.unique_id == agent_best_action and links.agent2 == agents):
						# print(links)

						# Updating the aware decay parameter
						links.aware_decay = 5

						# If the index is in the first part of the list, then the framing action is the best
						if best_action <= len(cw_of_interest) - 1:
							# print(' ')
							# print('Performing a causal relation framing action')
							# print('best_action: ' + str(best_action))
							# print('cw_of_interest: ' + str(cw_of_interest))
							# print('cw_of_interest[best_action]: ' + str(cw_of_interest[best_action]))
							
							# To simplify the notations
							best_action = cw_of_interest[best_action]

							if links.agent1 == agents:
								
								# print('Before: ' + str(links.agent2.belieftree[0][best_action][0]))
								links.agent2.belieftree[0][best_action][0] += (agents.belieftree[0][best_action][0] - links.agent2.belieftree[0][best_action][0]) * \
									agents.resources[0] * resources_weight_action * links.aware * resources_potency
								# print('After: ' + str(links.agent2.belieftree[0][best_action][0]))
								# 1-1 check
								links.agent2.belieftree[0][best_action][0] = \
									self.one_minus_one_check2(links.agent2.belieftree[0][best_action][0])
								# Providing partial knowledge - Framing - 0.2 range from real value: (Acting agent)
								agents.belieftree[1 + links.agent2.unique_id][best_action][0] = links.agent2.belieftree[0][best_action][0] + (random.random()/5) - 0.1
								# 1-1 check
								agents.belieftree[1 + links.agent2.unique_id][best_action][0] = \
									self.one_minus_one_check2(agents.belieftree[1 + links.agent2.unique_id][best_action][0])
								# Providing partial knowledge - Framing - 0.2 range from real value: (Acted upon agent)
								links.agent2.belieftree[1 + agents.unique_id][best_action][0] = agents.belieftree[0][best_action][0] + (random.random()/5) - 0.1
								# 1-1 check
								links.agent2.belieftree[1 + agents.unique_id][best_action][0] = \
									self.one_minus_one_check2(links.agent2.belieftree[1 + agents.unique_id][best_action][0])

								# print(' ')
								# print('Causal change')
								# print(agents.belieftree[1 + links.agent2.unique_id])
								# print(agents.belieftree[1 + links.agent2.unique_id][best_action][0])

							# Checking which agent in the link is the original agent
							if links.agent2 == agents:
								# print('Before: ' + str(links.agent1.belieftree[0][best_action][0]))
								links.agent1.belieftree[0][best_action][0] += (agents.belieftree[0][best_action][0] - links.agent1.belieftree[0][best_action][0]) * \
									agents.resources[0] * resources_weight_action * links.aware * resources_potency
								# print('After: ' + str(links.agent1.belieftree[0][best_action][0]))
								# 1-1 check
								links.agent1.belieftree[0][best_action][0] = \
									self.one_minus_one_check2(links.agent1.belieftree[0][best_action][0])
								# Providing partial knowledge - Framing - 0.2 range from real value: (Acting agent)
								agents.belieftree[1 + links.agent1.unique_id][best_action][0] = links.agent1.belieftree[0][best_action][0] + (random.random()/5) - 0.1
								# 1-1 check
								agents.belieftree[1 + links.agent1.unique_id][best_action][0] = \
									self.one_minus_one_check2(agents.belieftree[1 + links.agent1.unique_id][best_action][0])
								# Providing partial knowledge - Framing - 0.2 range from real value: (Acted upon agent)
								links.agent1.belieftree[1 + agents.unique_id][best_action][0] = agents.belieftree[0][best_action][0] + (random.random()/5) - 0.1
								# 1-1 check
								links.agent1.belieftree[1 + agents.unique_id][best_action][0] = \
									self.one_minus_one_check2(links.agent1.belieftree[1 + agents.unique_id][best_action][0])

								# print(' ')
								# print('Causal change')
								# print(agents.belieftree[1 + links.agent1.unique_id])
								# print(agents.belieftree[1 + links.agent1.unique_id][best_action][0])

						# If the index is in the second part of the list, then the aim influence action is the best
						if best_action == len(cw_of_interest):
							# print(' ')
							# print('Performing a state change action')
							# print('best_action: ' + str(best_action))

							if links.agent1 == agents:
								# print('Before: ' + str(links.agent2.belieftree[0][agents.select_problem_3S_pf][1]))
								links.agent2.belieftree[0][agents.select_problem_3S_pf][1] += (agents.belieftree[0][agents.select_problem_3S_pf][1] - links.agent2.belieftree[0][agents.select_problem_3S_pf][1]) * \
									agents.resources[0] * resources_weight_action * links.aware * resources_potency
								# print('After: ' + str(links.agent2.belieftree[0][agents.select_problem_3S_pf][1]))
								# 1-1 check
								links.agent2.belieftree[0][agents.select_problem_3S_pf][1] = \
									self.one_minus_one_check2(links.agent2.belieftree[0][agents.select_problem_3S_pf][1])
								# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acting agent)
								agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][1] = links.agent2.belieftree[0][agents.select_problem_3S_pf][1]
								# 1-1 check
								agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][1] = \
									self.one_minus_one_check2(agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][1])
								# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acted upon agent)
								links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][1] = agents.belieftree[0][agents.select_problem_3S_pf][1] + (random.random()/5) - 0.1
								# 1-1 check
								links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][1] = \
									self.one_minus_one_check2(links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][1])

								# print(' ')
								# print('Aim change')
								# print(agents.belieftree[1 + links.agent2.unique_id])

							if links.agent2 == agents:
								# print('Before: ' + str(links.agent1.belieftree[0][agents.select_problem_3S_pf][1]))
								links.agent1.belieftree[0][agents.select_problem_3S_pf][1] += (agents.belieftree[0][agents.select_problem_3S_pf][1] - links.agent1.belieftree[0][agents.select_problem_3S_pf][1]) * \
									agents.resources[0] * resources_weight_action * links.aware * resources_potency
								# print('After: ' + str(links.agent1.belieftree[0][agents.select_problem_3S_pf][1]))
								# 1-1 check
								links.agent1.belieftree[0][agents.select_problem_3S_pf][1] = \
									self.one_minus_one_check2(links.agent1.belieftree[0][agents.select_problem_3S_pf][1])
								# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acting agent)
								agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][1] = links.agent2.belieftree[0][agents.select_problem_3S_pf][1]
								# 1-1 check
								agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][1] = \
									self.one_minus_one_check2(agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][1])
								# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acted upon agent)
								links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][1] = agents.belieftree[0][agents.select_problem_3S_pf][1] + (random.random()/5) - 0.1
								# 1-1 check
								links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][1] = \
									self.one_minus_one_check2(links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][1])


						# If the index is in the first part of the list, then the state influence action is the best
						if best_action == len(cw_of_interest) + 1:
							# print(' ')
							# print('Performing an aim change action')
							# print('best_action: ' + str(best_action))

							if links.agent1 == agents:
								# print('Before: ' + str(links.agent2.belieftree[0][len(self.deep_core) + agents.select_problem][0]))
								links.agent2.belieftree[0][agents.select_problem_3S_pf][0] += (agents.belieftree[0][agents.select_problem_3S_pf][0] - links.agent2.belieftree[0][agents.select_problem_3S_pf][0]) * \
									agents.resources[0] * resources_weight_action * links.aware * resources_potency
								# print('After: ' + str(links.agent2.belieftree[0][len(self.deep_core) + agents.select_problem][0]))
								links.agent2.belieftree[0][agents.select_problem_3S_pf][0] = \
									self.one_minus_one_check2(links.agent2.belieftree[0][agents.select_problem_3S_pf][0])
								# Providing partial knowledge - State problem - 0.2 range from real value: (Acting agent)
								agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][0] = links.agent2.belieftree[0][agents.select_problem_3S_pf][0] + (random.random()/5) - 0.1
								# 1-1 check
								agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][0] = \
									self.one_minus_one_check2(agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][0])
								# Providing partial knowledge - State problem - 0.2 range from real value: (Acted upon agent)
								links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][0] = agents.belieftree[0][agents.select_problem_3S_pf][0] + (random.random()/5) - 0.1
								# 1-1 check
								links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][0] = \
									self.one_minus_one_check2(links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][0])

								# print(' ')
								# print('State change')
								# print(agents.belieftree[1 + links.agent2.unique_id])

							if links.agent2 == agents:
								# print('Before: ' + str(links.agent1.belieftree[0][len(self.deep_core) + agents.select_problem][0]))
								links.agent1.belieftree[0][agents.select_problem_3S_pf][0] += (agents.belieftree[0][agents.select_problem_3S_pf][0] - links.agent1.belieftree[0][agents.select_problem_3S_pf][0]) * \
									agents.resources[0] * resources_weight_action * links.aware * resources_potency
								# print('After: ' + str(links.agent1.belieftree[0][len(self.deep_core) + agents.select_problem][0]))
								# 1-1 check
								links.agent1.belieftree[0][agents.select_problem_3S_pf][0] = \
									self.one_minus_one_check2(links.agent1.belieftree[0][agents.select_problem_3S_pf][0])
								# Providing partial knowledge - State problem - 0.2 range from real value: (Acting agent)
								agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][0] = links.agent1.belieftree[0][agents.select_problem_3S_pf][0] + (random.random()/5) - 0.1
								# 1-1 check
								agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][0] = \
									self.one_minus_one_check2(agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][0])
								# Providing partial knowledge - State problem - 0.2 range from real value: (Acted upon agent)
								links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][0] = agents.belieftree[0][agents.select_problem_3S_pf][0] + (random.random()/5) - 0.1
								# 1-1 check
								links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][0] = \
									self.one_minus_one_check2(links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][0])

								# print(' ')
								# print('State change')
								# print(agents.belieftree[1 + links.agent1.unique_id])

				# If the agent is advocating or a policy, the following tasks are performed
				if agents.select_issue_3S_pf == 'policy':
					
					if (links.agent1 == agents and links.agent2.unique_id == agent_best_action) or (links.agent1.unique_id == agent_best_action and links.agent2 == agents):
						# print(links)

						# Updating the aware decay parameter
						links.aware_decay = 5

						# If the index is in the first part of the list, then the framing action is the best
						if best_action <= impact_number - 1:
							# print(' ')
							# print('Performing a causal relation framing action')
							# print('best_action: ' + str(best_action))
							# print('impact_number: ' + str(impact_number))

							if links.agent1 == agents:
								
								# print('Before: ' + str(links.agent2.belieftree_instrument[0][agents.select_policy_3S_pf][best_action]))
								links.agent2.belieftree_instrument[0][agents.select_policy_3S_pf][best_action] += (agents.belieftree_instrument[0][agents.select_policy_3S_pf][best_action] - \
									links.agent2.belieftree_instrument[0][agents.select_policy_3S_pf][best_action]) * \
									agents.resources[0] * resources_weight_action * links.aware * resources_potency
								# print('After: ' + str(links.agent2.belieftree_instrument[0][agents.select_policy_3S_pf][best_action]))
								# 1-1 check
								links.agent2.belieftree_instrument[0][agents.select_policy_3S_pf][best_action] = \
									self.one_minus_one_check2(links.agent2.belieftree_instrument[0][agents.select_policy_3S_pf][best_action])
								# Providing partial knowledge - Framing - 0.2 range from real value: (Acting agent)
								agents.belieftree_instrument[1 + links.agent2.unique_id][agents.select_policy_3S_pf][best_action] = links.agent2.belieftree_instrument[0][agents.select_policy_3S_pf][best_action] + (random.random()/5) - 0.1
								# 1-1 check
								agents.belieftree_instrument[1 + links.agent2.unique_id][agents.select_policy_3S_pf][best_action] = \
									self.one_minus_one_check2(agents.belieftree_instrument[1 + links.agent2.unique_id][agents.select_policy_3S_pf][best_action])
								# Providing partial knowledge - Framing - 0.2 range from real value: (Acted upon agent)
								links.agent2.belieftree_instrument[1 + agents.unique_id][agents.select_policy_3S_pf][best_action] = agents.belieftree_instrument[0][agents.select_policy_3S_pf][best_action] + (random.random()/5) - 0.1
								# 1-1 check
								links.agent2.belieftree_instrument[1 + agents.unique_id][agents.select_policy_3S_pf][best_action] = \
									self.one_minus_one_check2(links.agent2.belieftree_instrument[1 + agents.unique_id][agents.select_policy_3S_pf][best_action])

								# print(' ')
								# print('Causal change')
								# print(agents.belieftree_instrument[1 + links.agent2.unique_id])
								# print(agents.belieftree_instrument[1 + links.agent2.unique_id][agents.select_policy_3S_pf][best_action])

							# Checking which agent in the link is the original agent
							if links.agent2 == agents:

								# print('Before: ' + str(links.agent1.belieftree_instrument[0][agents.select_policy_3S_pf][best_action]))
								links.agent1.belieftree_instrument[0][agents.select_policy_3S_pf][best_action] += (agents.belieftree_instrument[0][agents.select_policy_3S_pf][best_action] - \
									links.agent1.belieftree_instrument[0][agents.select_policy_3S_pf][best_action]) * \
									agents.resources[0] * resources_weight_action * links.aware * resources_potency
								# print('After: ' + str(links.agent1.belieftree_instrument[0][agents.select_policy_3S_pf][best_action]))
								# 1-1 check
								links.agent1.belieftree_instrument[0][agents.select_policy_3S_pf][best_action] = \
									self.one_minus_one_check2(links.agent1.belieftree_instrument[0][agents.select_policy_3S_pf][best_action])
								# Providing partial knowledge - Framing - 0.2 range from real value: (Acting agent)
								agents.belieftree_instrument[1 + links.agent1.unique_id][agents.select_policy_3S_pf][best_action] = links.agent1.belieftree_instrument[0][agents.select_policy_3S_pf][best_action] + (random.random()/5) - 0.1
								# 1-1 check
								agents.belieftree_instrument[1 + links.agent1.unique_id][agents.select_policy_3S_pf][best_action] = \
									self.one_minus_one_check2(agents.belieftree_instrument[1 + links.agent1.unique_id][agents.select_policy_3S_pf][best_action])
								# Providing partial knowledge - Framing - 0.2 range from real value: (Acted upon agent)
								links.agent1.belieftree_instrument[1 + agents.unique_id][agents.select_policy_3S_pf][best_action] = agents.belieftree_instrument[0][agents.select_policy_3S_pf][best_action] + (random.random()/5) - 0.1
								# 1-1 check
								links.agent1.belieftree_instrument[1 + agents.unique_id][agents.select_policy_3S_pf][best_action] = \
									self.one_minus_one_check2(links.agent1.belieftree_instrument[1 + agents.unique_id][agents.select_policy_3S_pf][best_action])

								# print(' ')
								# print('Causal change')
								# print(agents.belieftree_instrument[1 + links.agent1.unique_id])
								# print(agents.belieftree_instrument[1 + links.agent1.unique_id][agents.select_policy_3S_pf][best_action])

						# If the index is in the second part of the list, then the aim influence action is the best
						if best_action == impact_number:
							# print(' ')
							# print('Performing a state change action')
							# print('best_action: ' + str(best_action))

							if links.agent1 == agents:
								# print('Before: ' + str(links.agent2.belieftree[0][agents.select_problem_3S_pf][1]))
								links.agent2.belieftree[0][agents.select_problem_3S_pf][1] += (agents.belieftree[0][agents.select_problem_3S_pf][1] - links.agent2.belieftree[0][agents.select_problem_3S_pf][1]) * \
									agents.resources[0] * resources_weight_action * links.aware * resources_potency
								# print('After: ' + str(links.agent2.belieftree[0][agents.select_problem_3S_pf][1]))
								# 1-1 check
								links.agent2.belieftree[0][agents.select_problem_3S_pf][1] = \
									self.one_minus_one_check2(links.agent2.belieftree[0][agents.select_problem_3S_pf][1])
								# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acting agent)
								agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][1] = links.agent2.belieftree[0][agents.select_problem_3S_pf][1]
								# 1-1 check
								agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][1] = \
									self.one_minus_one_check2(agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][1])
								# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acted upon agent)
								links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][1] = agents.belieftree[0][agents.select_problem_3S_pf][1] + (random.random()/5) - 0.1
								# 1-1 check
								links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][1] = \
									self.one_minus_one_check2(links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][1])

								# print(' ')
								# print('Aim change')
								# print(agents.belieftree[1 + links.agent2.unique_id])

							if links.agent2 == agents:

								# print('Before: ' + str(links.agent1.belieftree[0][agents.select_problem_3S_pf][1]))
								links.agent1.belieftree[0][agents.select_problem_3S_pf][1] += (agents.belieftree[0][agents.select_problem_3S_pf][1] - links.agent1.belieftree[0][agents.select_problem_3S_pf][1]) * \
									agents.resources[0] * resources_weight_action * links.aware * resources_potency
								# print('After: ' + str(links.agent1.belieftree[0][agents.select_problem_3S_pf][1]))
								# 1-1 check
								links.agent1.belieftree[0][agents.select_problem_3S_pf][1] = \
									self.one_minus_one_check2(links.agent1.belieftree[0][agents.select_problem_3S_pf][1])
								# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acting agent)
								agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][1] = links.agent2.belieftree[0][agents.select_problem_3S_pf][1]
								# 1-1 check
								agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][1] = \
									self.one_minus_one_check2(agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][1])
								# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acted upon agent)
								links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][1] = agents.belieftree[0][agents.select_problem_3S_pf][1] + (random.random()/5) - 0.1
								# 1-1 check
								links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][1] = \
									self.one_minus_one_check2(links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][1])


						# If the index is in the first part of the list, then the state influence action is the best
						if best_action == impact_number + 1:
							# print(' ')
							# print('Performing an aim change action')
							# print('best_action: ' + str(best_action))

							if links.agent1 == agents:
								# print('Before: ' + str(links.agent2.belieftree[0][len(self.deep_core) + agents.select_problem][0]))
								links.agent2.belieftree[0][agents.select_problem_3S_pf][0] += (agents.belieftree[0][agents.select_problem_3S_pf][0] - links.agent2.belieftree[0][agents.select_problem_3S_pf][0]) * \
									agents.resources[0] * resources_weight_action * links.aware * resources_potency
								# print('After: ' + str(links.agent2.belieftree[0][len(self.deep_core) + agents.select_problem][0]))
								links.agent2.belieftree[0][agents.select_problem_3S_pf][0] = \
									self.one_minus_one_check2(links.agent2.belieftree[0][agents.select_problem_3S_pf][0])
								# Providing partial knowledge - State problem - 0.2 range from real value: (Acting agent)
								agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][0] = links.agent2.belieftree[0][agents.select_problem_3S_pf][0] + (random.random()/5) - 0.1
								# 1-1 check
								agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][0] = \
									self.one_minus_one_check2(agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][0])
								# Providing partial knowledge - State problem - 0.2 range from real value: (Acted upon agent)
								links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][0] = agents.belieftree[0][agents.select_problem_3S_pf][0] + (random.random()/5) - 0.1
								# 1-1 check
								links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][0] = \
									self.one_minus_one_check2(links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][0])

								# print(' ')
								# print('State change')
								# print(agents.belieftree[1 + links.agent2.unique_id])

							if links.agent2 == agents:
								# print('Before: ' + str(links.agent1.belieftree[0][len(self.deep_core) + agents.select_problem][0]))
								links.agent1.belieftree[0][agents.select_problem_3S_pf][0] += (agents.belieftree[0][agents.select_problem_3S_pf][0] - links.agent1.belieftree[0][agents.select_problem_3S_pf][0]) * \
									agents.resources[0] * resources_weight_action * links.aware * resources_potency
								# print('After: ' + str(links.agent1.belieftree[0][len(self.deep_core) + agents.select_problem][0]))
								# 1-1 check
								links.agent1.belieftree[0][agents.select_problem_3S_pf][0] = \
									self.one_minus_one_check2(links.agent1.belieftree[0][agents.select_problem_3S_pf][0])
								# Providing partial knowledge - State problem - 0.2 range from real value: (Acting agent)
								agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][0] = links.agent1.belieftree[0][agents.select_problem_3S_pf][0] + (random.random()/5) - 0.1
								# 1-1 check
								agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][0] = \
									self.one_minus_one_check2(agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][0])
								# Providing partial knowledge - State problem - 0.2 range from real value: (Acted upon agent)
								links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][0] = agents.belieftree[0][agents.select_problem_3S_pf][0] + (random.random()/5) - 0.1
								# 1-1 check
								links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][0] = \
									self.one_minus_one_check2(links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][0])

								# print(' ')
								# print('State change')
								# print(agents.belieftree[1 + links.agent1.unique_id])



			# agents.resources_actions -= agents.resources
			agents.resources_actions -= agents.resources[0] * resources_weight_action

	def preference_udapte_as_PC(self, agent, who, len_DC, len_PC, len_S):

		# Preference calculation for the policy core issues
		PC_denominator = 0
		# Select one by one the DC
		for j in range(len_PC):
			PC_denominator = 0
			# Selecting the causal relations starting from DC
			for k in range(len_DC):
				# Contingency for partial knowledge issues
				if agent.belieftree[who][k][1] == None or agent.belieftree[who][k][0] == None or agent.belieftree[who][len_DC+len_PC+len_S+j+(k*len_PC)][0] == None:
					PC_denominator = 0
				else:
					# Check if causal relation and gap are both positive of both negative
					if (agent.belieftree[who][len_DC+len_PC+len_S+j+(k*len_PC)][0] < 0 and (agent.belieftree[who][k][1] - agent.belieftree[who][k][0]) < 0) \
					  or (agent.belieftree[who][len_DC+len_PC+len_S+j+(k*len_PC)][0] > 0 and (agent.belieftree[who][k][1] - agent.belieftree[who][k][0]) > 0):
						PC_denominator = PC_denominator + abs(agent.belieftree[who][len_DC+len_PC+len_S+j+(k*len_PC)][0]*\
						  (agent.belieftree[who][k][1] - agent.belieftree[who][k][0]))
					else:
						PC_denominator = PC_denominator	
		# Then adding the gap of the policy core:
		for i in range(len_PC):
			# Contingency for partial knowledge issues
			if agent.belieftree[who][len_DC + i][1] == None or agent.belieftree[who][len_DC + i][0] == None:
				PC_denominator = PC_denominator
			else:
				PC_denominator = PC_denominator + abs(agent.belieftree[who][len_DC + i][1] - agent.belieftree[who][len_DC + i][0])
		
		# Calculating the numerator and the preference of all policy core issues:
		# Select one by one the DC
		for j in range(len_PC):
			PC_numerator = 0
			# Selecting the causal relations starting from DC
			for k in range(len_DC):
				# Contingency for partial knowledge issues
				if agent.belieftree[who][k][1] == None or agent.belieftree[who][k][0] == None or agent.belieftree[who][len_DC+len_PC+len_S+j+(k*len_PC)][0] == None: 
					PC_numerator = 0
				else:
					# Check if causal relation and gap are both positive of both negative
					if (agent.belieftree[who][len_DC+len_PC+len_S+j+(k*len_PC)][0] < 0 and (agent.belieftree[who][k][1] - agent.belieftree[who][k][0]) < 0) \
					  or (agent.belieftree[who][len_DC+len_PC+len_S+j+(k*len_PC)][0] > 0 and (agent.belieftree[who][k][1] - agent.belieftree[who][k][0]) > 0):
						PC_numerator = PC_numerator + abs(agent.belieftree[who][len_DC+len_PC+len_S+j+(k*len_PC)][0]*\
						  (agent.belieftree[who][k][1] - agent.belieftree[who][k][0]))
					else:
						PC_numerator = PC_numerator	
			# Contingency for partial knowledge issues
			if agent.belieftree[who][len_DC + j][1] == None or agent.belieftree[who][len_DC + j][0] == None:
				PC_numerator = 0
			else:
				# Then adding the gap of the policy core:
				PC_numerator = PC_numerator + abs(agent.belieftree[who][len_DC + j][1] - agent.belieftree[who][len_DC + j][0])
			if PC_denominator != 0:
				agent.belieftree[who][len_DC+j][2] = PC_numerator/PC_denominator 
			else:
				agent.belieftree[who][len_DC+j][2] = 0

	def preference_udapte_pf_PC(self, agent, who, len_DC, len_PC, len_S, agenda_prob_3S_as):

		k = agenda_prob_3S_as

		# Calculating the numerator and the preference of all policy core issues:
		# Select one by one the DC
		S_denominator = 0
		for j in range(len_S):
			# print('Selection S' + str(j+1))
			# print('State of the S' + str(j+1) + ': ' + str(agent.belieftree[0][len_DC + j][0])) # the state printed
			# Selecting the causal relations starting from PC
			# print(' ')
			# print(len_DC + len_PC + len_S + len_DC*len_PC + j*len_PC + (k-len_DC))
			# Contingency for partial knowledge issues
			if agent.belieftree[0][k][1] != None and agent.belieftree[0][k][0] != None and agent.belieftree[0][len_DC + len_PC + len_S + len_DC*len_PC + j*len_PC + (k-len_DC)][0] != None:
				# print('Causal Relation S' + str(j+1) + ' - PC' + str(k+1) + ': ' + str(agent.belieftree[0][len_DC+len_PC+len_S+(j+(k*len_PC))][0]))
				# print('Gap of PC' + str(k+1) + ': ' + str(agent.belieftree[0][k][1] - agent.belieftree[0][k][0]))
				# Check if causal relation and gap are both positive of both negative
				if (agent.belieftree[0][len_DC + len_PC + len_S + len_DC*len_PC + j*len_PC + (k-len_DC)][0] < 0 and (agent.belieftree[0][k][1] - agent.belieftree[0][k][0]) < 0) \
					or (agent.belieftree[0][len_DC + len_PC + len_S + len_DC*len_PC + j*len_PC + (k-len_DC)][0] > 0 and (agent.belieftree[0][k][1] - agent.belieftree[0][k][0]) > 0):
					# print('Calculating')
					S_denominator = S_denominator + abs(agent.belieftree[0][len_DC + len_PC + len_S + len_DC*len_PC + j*len_PC + (k-len_DC)][0] * \
						(agent.belieftree[0][k][1] - agent.belieftree[0][k][0]))
					# print('This is the PC numerator: ' + str(S_denominator))
				else:
					S_denominator = S_denominator
			else:
				S_denominator = 0
			# Contingency for partial knowledge issues
			if agent.belieftree[0][len_DC + len_PC + j][1] == None or agent.belieftree[0][len_DC + len_PC + j][0] == None:
				S_denominator = S_denominator
			else:
				# Then adding the gap of the policy core:
				# print('This is the gap for the S' + str(j+1) + ': ' + str(agent.belieftree[0][len_DC + len_PC + j][1] - agent.belieftree[0][len_DC + len_PC + j][0]))
				S_denominator = S_denominator + abs(agent.belieftree[0][len_DC + len_PC + j][1] - agent.belieftree[0][len_DC + len_PC + j][0])


		# Calculating the numerator and the preference of all policy core issues:
		# Select one by one the DC
		for j in range(len_S):
			S_numerator = 0
			# Contingency for partial knowledge issues
			if agent.belieftree[0][k][1] != None and agent.belieftree[0][k][0] != None and agent.belieftree[0][len_DC + len_PC + len_S + len_DC*len_PC + j*len_PC + (k-len_DC)][0] != None:
				# Check if causal relation and gap are both positive of both negative
				if (agent.belieftree[0][len_DC + len_PC + len_S + len_DC*len_PC + j*len_PC + (k-len_DC)][0] < 0 and (agent.belieftree[0][k][1] - agent.belieftree[0][k][0]) < 0) \
					or (agent.belieftree[0][len_DC + len_PC + len_S + len_DC*len_PC + j*len_PC + (k-len_DC)][0] > 0 and (agent.belieftree[0][k][1] - agent.belieftree[0][k][0]) > 0):
					# print('Calculating')
					S_numerator = S_numerator + abs(agent.belieftree[0][len_DC + len_PC + len_S + len_DC*len_PC + j*len_PC + (k-len_DC)][0] * \
						(agent.belieftree[0][k][1] - agent.belieftree[0][k][0]))
					# print('This is the PC numerator: ' + str(S_numerator))
				else:
					S_numerator = S_numerator
			else:
				S_numerator = 0
			# Contingency for partial knowledge issues
			if agent.belieftree[0][len_DC + len_PC + j][1] == None or agent.belieftree[0][len_DC + len_PC + j][0] == None:
				S_numerator = 0
			else:
				# Then adding the gap of the policy core:
				S_numerator = S_numerator + abs(agent.belieftree[0][len_DC + len_PC + j][1] - agent.belieftree[0][len_DC + len_PC + j][0])
			if S_denominator != 0:
				agent.belieftree[who][len_DC + len_PC + j][2] = S_numerator/S_denominator 
			else:
				agent.belieftree[who][len_DC + len_PC + j][2] = 0

	def instrument_preference_update(self, agent, who, AS_theory, len_DC, len_PC, len_S, instruments):

		# print(' ')
		# print('Triggered for who in: ' + str(who))
		# print(' ')

		"""
		Instrument preference update function
		===========================

		This function is used to calculate the ranking of each of the instrument from 
		which the agents can choose from. This is done in two parts.

		1/ The first part consists of calculating the preference level for the different
		secondary issues (layer 3 in the belief tree). In this part, the preferences of
		the agents are updated similarly to the function where the preferences are calculated.
		The main difference is that this time, it is based on the agenda which means that
		only the secondary issues affecting the problem on the agenda are considered.

		2/ The second part consists of obtaining the grade for the policy instruments.
		This is calculated as shown in the formalisation with the equation given by:
		G = sum(impact * (Aim - State) * Preference_secondary)
		We make sure that the instruments impact are only taken into account if the
		impact is of the same sign as the gap between the state and the aim for the
		specific secondary issues. If this is not the case, the impact is not considered
		for that specific part of the instrument.

		Notes:
		1/ The secondary issues for which the agent is not interested (this applies to 
		the external parties only) are not taken into account in the calculation. They
		are marked as the 'No' values.

		"""

		######################################################################################################
		# 1/ Calculation of the preference level for the secondary issues based on the problem on the agenda #
		######################################################################################################

		S_denominator = 0
		if AS_theory != 2:
			j = agent.select_as_issue
		if AS_theory == 2:
			j = agent.select_problem_3S_as
		for k in range(len_S):
			if agent.belieftree[who][j][1] != None and agent.belieftree[who][j][0] != None and agent.belieftree[who][len_DC + len_PC + len_S + (len_DC*len_PC) + (j - len_DC)*len_S + k][0] != None:
				if (agent.belieftree[who][len_DC + len_PC + len_S + (len_DC*len_PC) + (j - len_DC)*len_S + k][0] < 0 and (agent.belieftree[who][j][1] - agent.belieftree[who][j][0]) < 0) \
					or (agent.belieftree[who][len_DC + len_PC + len_S + (len_DC*len_PC) + (j - len_DC)*len_S + k][0] > 0 and (agent.belieftree[who][j][1] - agent.belieftree[who][j][0]) > 0):
					S_denominator = S_denominator + abs(agent.belieftree[who][len_DC + len_PC + len_S + (len_DC*len_PC) + (j - len_DC)*len_S + k][0]*\
					  (agent.belieftree[who][j][1] - agent.belieftree[who][j][0]))
				else:
					S_denominator = S_denominator
			else:
				S_denominator = S_denominator

		for i in range(len_S):
			if agent.belieftree[who][len_DC + len_PC + i][0] != 'No':
				if agent.belieftree[who][len_DC + len_PC + i][1] != None and agent.belieftree[who][len_DC + len_PC + i][0] != None:
					S_denominator = S_denominator + abs(agent.belieftree[who][len_DC + len_PC + i][1] - agent.belieftree[who][len_DC + len_PC + i][0])
				else:
					S_denominator = 0

		S_numerator = 0
		
		for j in range(len_S):
			S_numerator = 0
			if AS_theory != 2:
				k = agent.select_as_issue
			if AS_theory == 2:
				k = agent.select_problem_3S_as
			if agent.belieftree[who][k][1] != None and agent.belieftree[who][k][0] != None and agent.belieftree[who][len_DC + len_PC + len_S + (len_DC*len_PC) + (k - len_DC)*len_S + j][0] != None:
				if (agent.belieftree[who][len_DC + len_PC + len_S + (len_DC*len_PC) + (k - len_DC)*len_S + j][0] < 0 and (agent.belieftree[who][k][1] - agent.belieftree[who][k][0]) < 0) \
					or (agent.belieftree[who][len_DC + len_PC + len_S + (len_DC*len_PC) + (k - len_DC)*len_S + j][0] > 0 and (agent.belieftree[who][k][1] - agent.belieftree[who][k][0]) > 0):
					S_numerator = S_numerator + abs(agent.belieftree[who][len_DC + len_PC + len_S + (len_DC*len_PC) + (k - len_DC)*len_S + j][0]*\
						  (agent.belieftree[who][k][1] - agent.belieftree[who][k][0]))
				else:
					S_numerator = S_numerator
			else:
				S_numerator = S_numerator
			if agent.belieftree[who][len_DC + len_PC + j][0] != 'No':
				if agent.belieftree[who][len_DC + len_PC + j][1] != None and agent.belieftree[who][len_DC + len_PC + j][0] != None:
					S_numerator = S_numerator + abs(agent.belieftree[who][len_DC + len_PC + j][1] - agent.belieftree[who][len_DC + len_PC + j][0])
				else:
					S_numerator = 0
			if S_denominator != 0:
				agent.belieftree[who][len_DC+len_PC+j][2] = S_numerator/S_denominator 
			else:
				agent.belieftree[who][len_DC+len_PC+j][2] = 0

		##################################################################################################
		# 2/ Calculation of the grade of each of the instruments based on impact on the secondary issues #
		##################################################################################################

		agent.instrument_preferences[who] = [0 for h in range(len(instruments))]
		for i in range(len(instruments)):
			for j in range(len_S):
				if agent.belieftree[who][len_DC + len_PC + j][0] != 'No':
					if agent.belieftree[who][len_DC + len_PC + j][1] != None and agent.belieftree[who][len_DC + len_PC + j][0] != None:
						if (instruments[i][j] > 0 and (agent.belieftree[who][len_DC + len_PC + j][1] - agent.belieftree[who][len_DC + len_PC + j][0]) > 0 ) \
							or (instruments[i][j] < 0 and (agent.belieftree[who][len_DC + len_PC + j][1] - agent.belieftree[who][len_DC + len_PC + j][0]) < 0 ):
							# print(' ')
							# print('agent.instrument_preferences[who][i]: ' + str(agent.instrument_preferences[who][i]))
							# print('instruments[i][j]: ' + str(instruments[i][j]))
							# print('agent.belieftree[' + str(who) + '][len_DC + len_PC + ' + str(j) + '][1]: ' + str(agent.belieftree[who][len_DC + len_PC + j][1]))
							# print('agent.belieftree[' + str(who) + '][len_DC + len_PC + ' + str(j) + '][0]: ' + str(agent.belieftree[who][len_DC + len_PC + j][0]))
							# print('agent.belieftree[' + str(who) + '][len_DC + len_PC + ' + str(j) + '][2]: ' + str(agent.belieftree[who][len_DC + len_PC + j][2]))
							agent.instrument_preferences[who][i] = agent.instrument_preferences[who][i] + \
								(instruments[i][j] * (agent.belieftree[who][len_DC + len_PC + j][1] - agent.belieftree[who][len_DC + len_PC + j][0]) * \
								(agent.belieftree[who][len_DC + len_PC + j][2]))
							# print('agent.instrument_preferences[who][i]: ' + str(agent.instrument_preferences[who][i]))
					else:
						agent.instrument_preferences[who][i] = 0

	def one_minus_one_check2(self, to_be_checked_parameter):

		checked_parameter = 0
		if to_be_checked_parameter > 1:
			checked_parameter = 1
		elif to_be_checked_parameter < -1:
			checked_parameter = -1
		else:
			checked_parameter = to_be_checked_parameter
		return checked_parameter

# Creation of the policy entrepreneur agents
class Policyentres(Agent):

	def __init__(self, run_number, agent_id, unique_id, pos, network_strategy, affiliation, resources, belieftree, instrument_preferences, belieftree_policy, belieftree_instrument, select_as_issue, select_pinstrument, select_issue_3S_as, \
		select_problem_3S_as, select_policy_3S_as, select_issue_3S_pf, select_problem_3S_pf, select_policy_3S_pf, team_as, team_pf, coalition_as, coalition_pf):
		# super().__init__(unique_id, model)
		self.run_number = run_number
		self.agent_id = agent_id
		self.unique_id = unique_id
		self.pos = pos
		self.network_strategy = network_strategy
		# self.model = model
		self.affiliation = affiliation
		self.resources = resources
		self.belieftree = belieftree
		self.belieftree_policy = belieftree_policy
		self.belieftree_instrument = belieftree_instrument
		self.instrument_preferences = instrument_preferences
		self.select_as_issue = select_as_issue
		self.select_pinstrument = select_pinstrument
		self.select_issue_3S_as = select_issue_3S_as
		self.select_problem_3S_as = select_problem_3S_as
		self.select_policy_3S_as = select_policy_3S_as
		self.select_issue_3S_pf = select_issue_3S_pf
		self.select_problem_3S_pf = select_problem_3S_pf
		self.select_policy_3S_pf = select_policy_3S_pf
		self.team_as = team_as
		self.team_pf = team_pf
		self.coalition_as = coalition_as
		self.coalition_pf = coalition_pf

	# def __str__(self):
	# 	return 'POLICYENTREPRENEUR - Affiliation: ' + str(self.affiliation) + ', Resources: ' + str(self.resources) + \
	# 	', Position: [' + str(self.pos[0]) + ',' + str(self.pos[1]) + '], ID: ' + str(self.unique_id) + \
	# 	', Problem selected: ' + str(self.select_problem) + ', Policy selected: ' + str(self.select_policy) + \
	# 	', Belief tree: ' + str(self.belieftree)

	# Simple print with ID
	def __str__(self):
		return 'Policy entrepreneur: ' + str(self.unique_id)

	def policyentres_states_update(self, agent, master_list, affiliation_weights):

		#' Addition of more than 3 affiliation will lead to unreported errors!')
		if len(affiliation_weights) != 3:
			print('WARNING - THIS CODE DOESNT WORK FOR MORE OR LESS THAN 3 AFFILIATIONS')

		# Defining the external parties list and the truth agent
		externalparties_list = []
		for agents in master_list:
			if type(agents) == Truth:
				truthagent = agents
			if type(agents) == Externalparties:
				externalparties_list.append(agents)

		# going through the different external parties:
		belief_sum_ep = [0 for k in range(len(truthagent.belieftree_truth))]
		# print(belief_sum_ep)
		for i in range(len(truthagent.belieftree_truth)):
			# print('NEW ISSUE! NEW ISSUES!')
			# This is used because in some cases, the external parties will have no impact on the agent (None values in the states of the EP)
			actual_length_ep = 0
			for j in range(len(externalparties_list)):
				# This line is added in case the EP has None states
				if externalparties_list[j].belieftree[0][i][0] != 'No':
					actual_length_ep += 1
					# Currently, the state of the policy makers is initialised as being equal to their initial aim:
					if agent.belieftree[0][i][0] == None:
						# print('Triggered - changed to: ' + str(agent.belieftree[0][i][1]))
						agent.belieftree[0][i][0] = agent.belieftree[0][i][1]
					# If they have the same affiliation, add without weight
					if externalparties_list[j].affiliation == agent.affiliation:
						# print('AFFILIATIONS ARE EQUAL')
						# print('issue ' + str(i+1) + ': ' + str(externalparties_list[j].belieftree[0][i][0]) +  /
						# ' and affiliation: ' + str(externalparties_list[j].affiliation) + '  ' + str(externalparties_list[j].unique_id))
						# print('This is the sum: ' + str(belief_sum_ep[i]))
						belief_sum_ep[i] = belief_sum_ep[i] + (externalparties_list[j].belieftree[0][i][0] - agent.belieftree[0][i][0])
						# print('The sum is equal to: ' + str(belief_sum_ep))
						# print('The change in state belief is equal to: ' + str(belief_sum_ep[i] / len(externalparties_list)))
					if (externalparties_list[j].affiliation == 0 and agent.affiliation == 1) or \
					   (externalparties_list[j].affiliation == 1 and agent.affiliation == 0):
						# print('AFFILIATION 1 AND 2')
						belief_sum_ep[i] = belief_sum_ep[i] + \
						   (externalparties_list[j].belieftree[0][i][0] - agent.belieftree[0][i][0]) * affiliation_weights[0]
					if (externalparties_list[j].affiliation == 0 and agent.affiliation == 2) or \
					   (externalparties_list[j].affiliation == 2 and agent.affiliation == 0):
						# print('AFFILIATION 1 AND 3')
						belief_sum_ep[i] = belief_sum_ep[i] + \
						   (externalparties_list[j].belieftree[0][i][0] - agent.belieftree[0][i][0]) * affiliation_weights[1]
					if (externalparties_list[j].affiliation == 1 and agent.affiliation == 2) or \
					   (externalparties_list[j].affiliation == 2 and agent.affiliation == 1):
						# print('AFFILIATION 2 AND 3')
						belief_sum_ep[i] = belief_sum_ep[i] + \
						   (externalparties_list[j].belieftree[0][i][0] - agent.belieftree[0][i][0]) * affiliation_weights[2]
			agent.belieftree[0][i][0] = agent.belieftree[0][i][0] + belief_sum_ep[i] / actual_length_ep
			# print('This is issue: ' + str(i+1) + ' and its new value is: ' + str(agent.belieftree[0][i][0]))
		# print(agent)

	def pm_pe_actions_as(self, agents, link_list, deep_core, policy_core, secondary, resources_weight_action, resources_potency):

		len_DC = len(deep_core)
		len_PC = len(policy_core)
		len_S = len(secondary)

		# Selection of the cw of interest
		cw_of_interest = []
		# We only consider the causal relations related to the problem on the agenda
		for cw_choice in range(len(deep_core)):
				cw_of_interest.append(len_DC + len_PC + len_S + (agents.select_as_issue - len_DC) + cw_choice * len(policy_core))

		# print(' ')
		# print('Causal relations of interest: ' + str(cw_of_interest))

		# Making sure there are enough resources
		while agents.resources_actions > 0.001:

			# Going through all the links in the model
			# print(agents)
			total_grade_list = []
			total_grade_list_links = []
			for links in link_list:

				# Making sure that the link is attached to the agent and has a aware higher than 0
				if (links.agent1 == agents or links.agent2 == agents) and links.aware > 0:
					total_grade_list_links.append(links)

					# Definition the action weight parameter
					if type(links.agent1) == Policymakers or type(links.agent2) == Policymakers:
						actionWeight = 1
					else:
						actionWeight = 0.95
					
					# 1. Grading all framing actions:
					# Checking through all possible framing - This is all based on partial knowledge!
					for cw in range(len(cw_of_interest)):

						# Checking which agent in the link is the original agent
						if links.agent1 == agents:
							# Check if no partial knowledge (initial value)
							check_none = 0
							if agents.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0] == None:
								agents.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0] = 0
								check_none = 1
							# Memorising the original belief values
							original_belief = [0]
							original_belief[0] = copy.copy(agents.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0])
							# Performing the action
							agents.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0] += \
								(agents.belieftree[0][cw_of_interest[cw]][0] - agents.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0]) * \
								agents.resources[0] * resources_weight_action * links.aware * resources_potency
							# 1-1 check
							agents.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0] = \
								self.one_minus_one_check2(agents.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0])
							# Update of the preferences for that partial knowledge agent
							self.preference_udapte_as_PC(agents, 1 + links.agent2.unique_id, len_DC, len_PC, len_S)
							# Calculation of the new grade - we check selected issue using partial knowledge updates
							cw_grade = abs(agents.belieftree[0][agents.select_as_issue][2] - agents.belieftree[1 + links.agent2.unique_id][agents.select_as_issue][2])
							# print('cw_grade: ' + str(cw_grade))
							# Restoring the initial values
							agents.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0] = original_belief[0]
							# Re-updating the preference levels
							self.preference_udapte_as_PC(agents, 1 + links.agent2.unique_id, len_DC, len_PC, len_S)
							# Adding the grade to the grade list
							total_grade_list.append(cw_grade)
							#  Reset to None after finding the grade
							if check_none == 1:
								agents.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0] = None

						# Checking which agent in the link is the original agent
						if links.agent2 == agents:
							#  Check if no partial knowledge (initial value)
							check_none = 0
							if agents.belieftree[1 + links.agent1.unique_id][cw_of_interest[cw]][0] == None:
								agents.belieftree[1 + links.agent1.unique_id][cw_of_interest[cw]][0] = 0
								check_none = 1
							# Memorising the original belief values
							original_belief = [0]
							original_belief[0] = copy.copy(agents.belieftree[1 + links.agent1.unique_id][cw_of_interest[cw]][0])
							# Performing the action
							agents.belieftree[1 + links.agent1.unique_id][cw_of_interest[cw]][0] += \
								(agents.belieftree[0][cw_of_interest[cw]][0] - agents.belieftree[1 + links.agent1.unique_id][cw_of_interest[cw]][0]) * \
								agents.resources[0] * resources_weight_action * links.aware * resources_potency
							# 1-1 check
							agents.belieftree[1 + links.agent1.unique_id][cw_of_interest[cw]][0] = \
								self.one_minus_one_check2(agents.belieftree[1 + links.agent1.unique_id][cw_of_interest[cw]][0])
							# Update of the preferences for that partial knowledge agent
							self.preference_udapte_as_PC(agents, 1 + links.agent1.unique_id, len_DC, len_PC, len_S)
							# Calculation of the new grade - we check selected issue using partial knowledge updates
							cw_grade = abs(agents.belieftree[0][agents.select_as_issue][2] - agents.belieftree[1 + links.agent1.unique_id][agents.select_as_issue][2])
							# print('cw_grade: ' + str(cw_grade))
							# Restoring the initial values
							agents.belieftree[1 + links.agent1.unique_id][cw_of_interest[cw]][0] = original_belief[0]
							# Re-updating the preference levels
							self.preference_udapte_as_PC(agents, 1 + links.agent1.unique_id, len_DC, len_PC, len_S)
							# Adding the grade to the grade list
							total_grade_list.append(cw_grade)
							# Reset to None after finding the grade
							if check_none == 1:
								agents.belieftree[1 + links.agent1.unique_id][cw_of_interest[cw]][0] = None

					# 2. Grading all individual actions - Aim change
					if links.agent1 == agents:
						# Check if no partial knowledge (initial value)
						check_none = 0
						if agents.belieftree[1 + links.agent2.unique_id][agents.select_as_issue][1] == None:
							agents.belieftree[1 + links.agent2.unique_id][agents.select_as_issue][1] = 0
							check_none = 1
						# Memorising is no partial knoweldge
						original_belief = [0]
						original_belief[0] = copy.copy(agents.belieftree[1 + links.agent2.unique_id][agents.select_as_issue][1])
						# Performing the action
						agents.belieftree[1 + links.agent2.unique_id][agents.select_as_issue][1] += \
							(agents.belieftree[0][agents.select_as_issue][1] - agents.belieftree[1 + links.agent2.unique_id][agents.select_as_issue][1]) * \
							agents.resources[0] * resources_weight_action * links.aware * links.conflict_level[0][agents.select_as_issue][1] * actionWeight * resources_potency
						# 1-1 check
						agents.belieftree[1 + links.agent2.unique_id][agents.select_as_issue][1] = \
							self.one_minus_one_check2(agents.belieftree[1 + links.agent2.unique_id][agents.select_as_issue][1])
						# Update of the preferences for that partial knowledge agent
						self.preference_udapte_as_PC(agents, 1 + links.agent2.unique_id, len_DC, len_PC, len_S)
						# Calculation of the new grade - we check selected issue using partial knowledge updates
						aim_grade_issue = abs(agents.belieftree[0][agents.select_as_issue][2] - agents.belieftree[1 + links.agent2.unique_id][agents.select_as_issue][2])
						# print('aim_grade_issue: ' + str(aim_grade_issue))
						# Restoring the initial values
						agents.belieftree[1 + links.agent2.unique_id][agents.select_as_issue][1] = original_belief[0]
						# Re-updating the preference levels
						self.preference_udapte_as_PC(agents, 1 + links.agent2.unique_id, len_DC, len_PC, len_S)
						#  Reset to None after finding the grade
						if check_none == 1:
							agents.belieftree[1 + links.agent2.unique_id][agents.select_as_issue][1] = None
						# Adding the grade to the grade list
						total_grade_list.append(aim_grade_issue)

					if links.agent2 == agents:
						# Check if no partial knowledge (initial value)
						check_none = 0
						if agents.belieftree[1 + links.agent1.unique_id][agents.select_as_issue][1] == None:
							agents.belieftree[1 + links.agent1.unique_id][agents.select_as_issue][1] = 0
							check_none = 1
						# Memorising is no partial knoweldge
						original_belief = [0]
						original_belief[0] = copy.copy(agents.belieftree[1 + links.agent1.unique_id][agents.select_as_issue][1])
						# Performing the action
						agents.belieftree[1 + links.agent1.unique_id][agents.select_as_issue][1] += \
							(agents.belieftree[0][agents.select_as_issue][1] - agents.belieftree[1 + links.agent1.unique_id][agents.select_as_issue][1]) * \
							agents.resources[0] * resources_weight_action * links.aware * links.conflict_level[1][agents.select_as_issue][1] * actionWeight * resources_potency
						# 1-1 check
						agents.belieftree[1 + links.agent1.unique_id][agents.select_as_issue][1] = \
							self.one_minus_one_check2(agents.belieftree[1 + links.agent1.unique_id][agents.select_as_issue][1])
						# Update of the preferences for that partial knowledge agent
						self.preference_udapte_as_PC(agents, 1 + links.agent1.unique_id, len_DC, len_PC, len_S)
						# Calculation of the new grade - we check selected issue using partial knowledge updates
						aim_grade_issue = abs(agents.belieftree[0][agents.select_as_issue][2] - agents.belieftree[1 + links.agent1.unique_id][agents.select_as_issue][2])
						# print('aim_grade_issue: ' + str(aim_grade_issue))
						# Restoring the initial values
						agents.belieftree[1 + links.agent1.unique_id][agents.select_as_issue][1] = original_belief[0]
						# Re-updating the preference levels
						self.preference_udapte_as_PC(agents, 1 + links.agent1.unique_id, len_DC, len_PC, len_S)
						#  Reset to None after finding the grade
						if check_none == 1:
							agents.belieftree[1 + links.agent1.unique_id][agents.select_as_issue][1] = None
						# Adding the grade to the grade list
						total_grade_list.append(aim_grade_issue)

					# 3. Grading all individual actions - State change
					if links.agent1 == agents:
						# Check if no partial knowledge (initial value)
						check_none = 0
						if agents.belieftree[1 + links.agent2.unique_id][agents.select_as_issue][0] == None:
							agents.belieftree[1 + links.agent2.unique_id][agents.select_as_issue][0] = 0
							check_none = 1
						# Memorising is no partial knoweldge
						original_belief = [0]
						original_belief[0] = copy.copy(agents.belieftree[1 + links.agent2.unique_id][agents.select_as_issue][0])
						# Performing the action
						agents.belieftree[1 + links.agent2.unique_id][agents.select_as_issue][0] += \
							(agents.belieftree[0][agents.select_as_issue][0] - agents.belieftree[1 + links.agent2.unique_id][agents.select_as_issue][0]) * \
							agents.resources[0] * resources_weight_action * links.aware * links.conflict_level[0][agents.select_as_issue][0] * actionWeight * resources_potency
						# 1-1 check
						agents.belieftree[1 + links.agent2.unique_id][agents.select_as_issue][0] = \
							self.one_minus_one_check2(agents.belieftree[1 + links.agent2.unique_id][agents.select_as_issue][0])
						# Update of the preferences for that partial knowledge agent
						self.preference_udapte_as_PC(agents, 1 + links.agent2.unique_id, len_DC, len_PC, len_S)
						# Calculation of the new grade - we check selected issue using partial knowledge updates
						state_grade_issue = abs(agents.belieftree[0][agents.select_as_issue][2] - agents.belieftree[1 + links.agent2.unique_id][agents.select_as_issue][2])
						# print('state_grade_issue: ' + str(state_grade_issue))
						# Restoring the initial values
						agents.belieftree[1 + links.agent2.unique_id][agents.select_as_issue][0] = original_belief[0]
						# Re-updating the preference levels
						self.preference_udapte_as_PC(agents, 1 + links.agent2.unique_id, len_DC, len_PC, len_S)
						#  Reset to None after finding the grade
						if check_none == 1:
							agents.belieftree[1 + links.agent2.unique_id][agents.select_as_issue][0] = None
						# Adding the grade to the grade list
						total_grade_list.append(state_grade_issue)

					if links.agent2 == agents:
						# Check if no partial knowledge (initial value)
						check_none = 0
						if agents.belieftree[1 + links.agent1.unique_id][agents.select_as_issue][0] == None:
							agents.belieftree[1 + links.agent1.unique_id][agents.select_as_issue][0] = 0
							check_none = 1
						# Memorising is no partial knoweldge
						original_belief = [0]
						original_belief[0] = copy.copy(agents.belieftree[1 + links.agent1.unique_id][agents.select_as_issue][0])
						# Performing the action
						agents.belieftree[1 + links.agent1.unique_id][agents.select_as_issue][0] += \
							(agents.belieftree[0][agents.select_as_issue][0] - agents.belieftree[1 + links.agent1.unique_id][agents.select_as_issue][0]) * \
							agents.resources[0] * resources_weight_action * links.aware * links.conflict_level[1][agents.select_as_issue][0] * actionWeight * resources_potency
						# 1-1 check
						agents.belieftree[1 + links.agent1.unique_id][agents.select_as_issue][0] = \
							self.one_minus_one_check2(agents.belieftree[1 + links.agent1.unique_id][agents.select_as_issue][0])
						# Update of the preferences for that partial knowledge agent
						self.preference_udapte_as_PC(agents, 1 + links.agent1.unique_id, len_DC, len_PC, len_S)
						# Calculation of the new grade - we check selected issue using partial knowledge updates
						state_grade_issue = abs(agents.belieftree[0][agents.select_as_issue][2] - agents.belieftree[1 + links.agent1.unique_id][agents.select_as_issue][2])
						# print('state_grade_issue: ' + str(state_grade_issue))
						# Restoring the initial values
						agents.belieftree[1 + links.agent1.unique_id][agents.select_as_issue][0] = original_belief[0]
						# Re-updating the preference levels
						self.preference_udapte_as_PC(agents, 1 + links.agent1.unique_id, len_DC, len_PC, len_S)
						#  Reset to None after finding the grade
						if check_none == 1:
							agents.belieftree[1 + links.agent1.unique_id][agents.select_as_issue][0] = None
						# Adding the grade to the grade list
						total_grade_list.append(state_grade_issue)
					# print(' ')

			# print(' ')
			# print('Number of actions: ' + str(len(total_grade_list)))
			# print(total_grade_list)

			# 4. Choosing an action
			# Check if several actions have the same grade
			min_best_action = min(total_grade_list)
			count_min_list = []
			count = 0
			for item in total_grade_list:
				if item == min_best_action:
					count_min_list.append(count)
				count += 1
			# print('List of indexes: ' + str(count_min_list))
			# print(' ')

			# If there are several grades at the same level, then choose a random action from these grades:
			if len(count_min_list) > 1:
				best_action_index = random.choice(count_min_list)
				# print('Randomly chosen best action: ' + str(best_action_index))
			else:
				best_action_index = total_grade_list.index(min(total_grade_list))
				# print('Not randomly chosen: ' + str(best_action_index))
			
			# print(' ')
			# print('----- New check for best action ------')
			# print('Action value: ' + str(min(total_grade_list)))
			# print('Index of the best action: ' + str(best_action_index))
			# print('This is the grade of the action: ' + str(total_grade_list[best_action_index]))
			# Make sure that we do not take into account the 0 from the list to perform the following calculations
			# best_action_index += 1
			# print('The total amount of links considered: ' + str(len(total_grade_list_links)))
			# print('The number of actions per link considered: ' + str(len(cw_of_interest) + 2))
			# print('The total amount of actions considered: ' + str(len(total_grade_list)))
			# print('The link for the action is: ' + str(int(best_action_index/(len(cw_of_interest) + 2))))
			best_action = best_action_index - (len(cw_of_interest) + 2) * int(best_action_index/(len(cw_of_interest) + 2))
			# print('The impacted index is: ' + str(best_action))
			# print('The would be index without the +1: ' + str((best_action_index - (len(cw_of_interest) + 2) * int(best_action_index/(len(cw_of_interest) + 2))) - 1))
			# print('   ')

			# 5. Performing the actual action
			# Selecting the link:
			for links in link_list:

				if links == total_grade_list_links[int(best_action_index/(len(cw_of_interest) + 2))]:
					# print(links)

					# If the index is in the first part of the list, then the framing action is the best
					if best_action <= len(cw_of_interest) -1:					
						# print(' ')
						# print('Framing action - causal relation')
						# print('best_action: ' + str(best_action))
						# print('cw_of_interest: ' + str(cw_of_interest))
						# print('cw_of_interest[best_action]: ' + str(cw_of_interest[best_action]))

						# To simplify the notations
						best_action = cw_of_interest[best_action]

						# Update of the aware decay parameter
						links.aware_decay = 5

						# print('Causal affected: ' + str(best_action))
						# best_action = len(self.deep_core) + len(self.policy_core) + len(self.secondary) + best_action
						if links.agent1 == agents:
							
							# print('Before: ' + str(links.agent2.belieftree[0][best_action][0]))
							links.agent2.belieftree[0][best_action][0] += (agents.belieftree[0][best_action][0] - links.agent2.belieftree[0][best_action][0]) * \
								agents.resources[0] * resources_weight_action * links.aware * resources_potency
							# print('After: ' + str(links.agent2.belieftree[0][best_action][0]))
							# 1-1 check
							links.agent2.belieftree[0][best_action][0] = \
								self.one_minus_one_check2(links.agent2.belieftree[0][best_action][0])
							# Providing partial knowledge - Framing - 0.2 range from real value: (Acting agent)
							agents.belieftree[1 + links.agent2.unique_id][best_action][0] = links.agent2.belieftree[0][best_action][0] + (random.random()/5) - 0.1
							# 1-1 check
							agents.belieftree[1 + links.agent2.unique_id][best_action][0] = \
								self.one_minus_one_check2(agents.belieftree[1 + links.agent2.unique_id][best_action][0])
							# Providing partial knowledge - Framing - 0.2 range from real value: (Acted upon agent)
							links.agent2.belieftree[1 + agents.unique_id][best_action][0] = agents.belieftree[0][best_action][0] + (random.random()/5) - 0.1
							# 1-1 check
							links.agent2.belieftree[1 + agents.unique_id][best_action][0] = \
								self.one_minus_one_check2(links.agent2.belieftree[1 + agents.unique_id][best_action][0])

							# print(' ')
							# print('Causal change')
							# print(agents.belieftree[1 + links.agent2.unique_id])
							# print(agents.belieftree[1 + links.agent2.unique_id][best_action][0])

						# Checking which agent in the link is the original agent
						if links.agent2 == agents:
							# print('Before: ' + str(links.agent1.belieftree[0][best_action][0]))
							links.agent1.belieftree[0][best_action][0] += (agents.belieftree[0][best_action][0] - links.agent1.belieftree[0][best_action][0]) * \
								agents.resources[0] * resources_weight_action * links.aware * resources_potency
							# print('After: ' + str(links.agent1.belieftree[0][best_action][0]))
							# 1-1 check
							links.agent1.belieftree[0][best_action][0] = \
								self.one_minus_one_check2(links.agent1.belieftree[0][best_action][0])
							# Providing partial knowledge - Framing - 0.2 range from real value: (Acting agent)
							agents.belieftree[1 + links.agent1.unique_id][best_action][0] = links.agent1.belieftree[0][best_action][0] + (random.random()/5) - 0.1
							# 1-1 check
							agents.belieftree[1 + links.agent1.unique_id][best_action][0] = \
								self.one_minus_one_check2(agents.belieftree[1 + links.agent1.unique_id][best_action][0])
							# Providing partial knowledge - Framing - 0.2 range from real value: (Acted upon agent)
							links.agent1.belieftree[1 + agents.unique_id][best_action][0] = agents.belieftree[0][best_action][0] + (random.random()/5) - 0.1
							# 1-1 check
							links.agent1.belieftree[1 + agents.unique_id][best_action][0] = \
								self.one_minus_one_check2(links.agent1.belieftree[1 + agents.unique_id][best_action][0])

							# print(' ')
							# print('Causal change')
							# print(agents.belieftree[1 + links.agent1.unique_id])
							# print(agents.belieftree[1 + links.agent1.unique_id][best_action][0])

					# If the index is in the second part of the list, then the aim influence action is the best
					if best_action == len(cw_of_interest):
						# print('Implementing a aim influence action:')
						links.aware_decay = 5
						# print('Aim me - problem')

						if links.agent1 == agents:
							# print('Before: ' + str(links.agent2.belieftree[0][agents.select_as_issue][1]))
							links.agent2.belieftree[0][agents.select_as_issue][1] += (agents.belieftree[0][agents.select_as_issue][1] - links.agent2.belieftree[0][agents.select_as_issue][1]) * \
								agents.resources[0] * resources_weight_action * links.aware * resources_potency
							# print('After: ' + str(links.agent2.belieftree[0][agents.select_as_issue][1]))
							# 1-1 check
							links.agent2.belieftree[0][agents.select_as_issue][1] = \
								self.one_minus_one_check2(links.agent2.belieftree[0][agents.select_as_issue][1])
							# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acting agent)
							agents.belieftree[1 + links.agent2.unique_id][agents.select_as_issue][1] = links.agent2.belieftree[0][agents.select_as_issue][1]
							# 1-1 check
							agents.belieftree[1 + links.agent2.unique_id][agents.select_as_issue][1] = \
								self.one_minus_one_check2(agents.belieftree[1 + links.agent2.unique_id][agents.select_as_issue][1])
							# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acted upon agent)
							links.agent2.belieftree[1 + agents.unique_id][agents.select_as_issue][1] = agents.belieftree[0][agents.select_as_issue][1] + (random.random()/5) - 0.1
							# 1-1 check
							links.agent2.belieftree[1 + agents.unique_id][agents.select_as_issue][1] = \
								self.one_minus_one_check2(links.agent2.belieftree[1 + agents.unique_id][agents.select_as_issue][1])

							# print(' ')
							# print('Aim change')
							# print(agents.belieftree[1 + links.agent2.unique_id])

						if links.agent2 == agents:
							# print('Before: ' + str(links.agent1.belieftree[0][agents.select_as_issue][1]))
							links.agent1.belieftree[0][agents.select_as_issue][1] += (agents.belieftree[0][agents.select_as_issue][1] - links.agent1.belieftree[0][agents.select_as_issue][1]) * \
								agents.resources[0] * resources_weight_action * links.aware * resources_potency
							# print('After: ' + str(links.agent1.belieftree[0][agents.select_as_issue][1]))
							# 1-1 check
							links.agent1.belieftree[0][agents.select_as_issue][1] = \
								self.one_minus_one_check2(links.agent1.belieftree[0][agents.select_as_issue][1])
							# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acting agent)
							agents.belieftree[1 + links.agent1.unique_id][agents.select_as_issue][1] = links.agent2.belieftree[0][agents.select_as_issue][1]
							# 1-1 check
							agents.belieftree[1 + links.agent1.unique_id][agents.select_as_issue][1] = \
								self.one_minus_one_check2(agents.belieftree[1 + links.agent1.unique_id][agents.select_as_issue][1])
							# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acted upon agent)
							links.agent1.belieftree[1 + agents.unique_id][agents.select_as_issue][1] = agents.belieftree[0][agents.select_as_issue][1] + (random.random()/5) - 0.1
							# 1-1 check
							links.agent1.belieftree[1 + agents.unique_id][agents.select_as_issue][1] = \
								self.one_minus_one_check2(links.agent1.belieftree[1 + agents.unique_id][agents.select_as_issue][1])


					# If the index is in the first part of the list, then the state influence action is the best
					if best_action == len(cw_of_interest) + 1:
						# print('Implementing a state influence action:')
						links.aware_decay = 5
						# print('State me - problem')

						if links.agent1 == agents:
							# print('Before: ' + str(links.agent2.belieftree[0][len(self.deep_core) + agents.select_problem][0]))
							links.agent2.belieftree[0][agents.select_as_issue][0] += (agents.belieftree[0][agents.select_as_issue][0] - links.agent2.belieftree[0][agents.select_as_issue][0]) * \
								agents.resources[0] * resources_weight_action * links.aware * resources_potency
							# print('After: ' + str(links.agent2.belieftree[0][len(self.deep_core) + agents.select_problem][0]))
							links.agent2.belieftree[0][agents.select_as_issue][0] = \
								self.one_minus_one_check2(links.agent2.belieftree[0][agents.select_as_issue][0])
							# Providing partial knowledge - State problem - 0.2 range from real value: (Acting agent)
							agents.belieftree[1 + links.agent2.unique_id][agents.select_as_issue][0] = links.agent2.belieftree[0][agents.select_as_issue][0] + (random.random()/5) - 0.1
							# 1-1 check
							agents.belieftree[1 + links.agent2.unique_id][agents.select_as_issue][0] = \
								self.one_minus_one_check2(agents.belieftree[1 + links.agent2.unique_id][agents.select_as_issue][0])
							# Providing partial knowledge - State problem - 0.2 range from real value: (Acted upon agent)
							links.agent2.belieftree[1 + agents.unique_id][agents.select_as_issue][0] = agents.belieftree[0][agents.select_as_issue][0] + (random.random()/5) - 0.1
							# 1-1 check
							links.agent2.belieftree[1 + agents.unique_id][agents.select_as_issue][0] = \
								self.one_minus_one_check2(links.agent2.belieftree[1 + agents.unique_id][agents.select_as_issue][0])

							# print(' ')
							# print('State change')
							# print(agents.belieftree[1 + links.agent2.unique_id])

						if links.agent2 == agents:
							# print('Before: ' + str(links.agent1.belieftree[0][len(self.deep_core) + agents.select_problem][0]))
							links.agent1.belieftree[0][agents.select_as_issue][0] += (agents.belieftree[0][agents.select_as_issue][0] - links.agent1.belieftree[0][agents.select_as_issue][0]) * \
								agents.resources[0] * resources_weight_action * links.aware * resources_potency
							# print('After: ' + str(links.agent1.belieftree[0][len(self.deep_core) + agents.select_problem][0]))
							# 1-1 check
							links.agent1.belieftree[0][agents.select_as_issue][0] = \
								self.one_minus_one_check2(links.agent1.belieftree[0][agents.select_as_issue][0])
							# Providing partial knowledge - State problem - 0.2 range from real value: (Acting agent)
							agents.belieftree[1 + links.agent1.unique_id][agents.select_as_issue][0] = links.agent1.belieftree[0][agents.select_as_issue][0] + (random.random()/5) - 0.1
							# 1-1 check
							agents.belieftree[1 + links.agent1.unique_id][agents.select_as_issue][0] = \
								self.one_minus_one_check2(agents.belieftree[1 + links.agent1.unique_id][agents.select_as_issue][0])
							# Providing partial knowledge - State problem - 0.2 range from real value: (Acted upon agent)
							links.agent1.belieftree[1 + agents.unique_id][agents.select_as_issue][0] = agents.belieftree[0][agents.select_as_issue][0] + (random.random()/5) - 0.1
							# 1-1 check
							links.agent1.belieftree[1 + agents.unique_id][agents.select_as_issue][0] = \
								self.one_minus_one_check2(links.agent1.belieftree[1 + agents.unique_id][agents.select_as_issue][0])

							# print(' ')
							# print('State change')
							# print(agents.belieftree[1 + links.agent1.unique_id])

			# agents.resources_actions -= agents.resources
			agents.resources_actions -= agents.resources[0] * resources_weight_action

	def pm_pe_actions_pf(self, agents, link_list, deep_core, policy_core, secondary, causalrelation_number, agenda_as_issue, instruments, resources_weight_action, resources_potency, AS_theory):


		len_DC = len(deep_core)
		len_PC = len(policy_core)
		len_S = len(secondary)

		# Here are the modifications related to the policy formulation
		# Looking for the relevant causal relations for the policy formulation
		of_interest = []
		cw_of_interest = []
		# We only consider the causal relations related to the problem on the agenda
		for cw_choice in range(len(secondary)):
			if agents.belieftree[0][len_DC + len_PC + len_S + (len_DC * len_PC) + (agenda_as_issue - len_DC)*len_S + cw_choice][0] \
				* instruments[agents.select_pinstrument][cw_choice] != 0:
				cw_of_interest.append(len_DC + len_PC + len_S + (len_DC * len_PC) + (agenda_as_issue - len_DC)*len_S + cw_choice)
		of_interest.append(cw_of_interest)
		# Looking for the relevant issues for the policy formulation
		issue_of_interest = []
		for issue_choice in range(len(secondary)):
			if instruments[agents.select_pinstrument][issue_choice] != 0:
				issue_of_interest.append(len_DC + len_PC + issue_choice)
		of_interest.append(issue_of_interest)

		# Making sure there are enough resources
		while agents.resources_actions > 0.001:
			# Going through all the links in the model
			# print(agents)
			total_grade_list = []
			total_grade_list_links = []
			for links in link_list:
				
				# Making sure that the link is attached to the agent and has a aware higher than 0
				if (links.agent1 == agents or links.agent2 == agents) and links.aware > 0:
					total_grade_list_links.append(links)
					# Definition the action weight parameter
					if type(links.agent1) == Policymakers or type(links.agent2) == Policymakers:
						actionWeight = 1
					else:
						actionWeight = 0.95

					
					# 1. Grading all framing actions:
					# Checking through all possible framing - This is all based on partial knowledge!
					for cw in range(len(cw_of_interest)):
						# Checking which agent in the link is the original agent
						if links.agent1 == agents:
							# Check if no partial knowledge (initial value)
							check_none = 0
							if agents.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0] == None:
								agents.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0] = 0
								check_none = 1
							# Memorising the original belief values
							original_belief = [0]
							original_belief[0] = copy.copy(agents.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0])
							# Performing the action
							# print(' ')
							# print('Old value of the CR: ' + str(agents.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0]))
							agents.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0] += \
								(agents.belieftree[0][cw_of_interest[cw]][0] - agents.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0]) * \
								agents.resources[0] * resources_weight_action * links.aware * resources_potency
							# print('New value of the CR: ' + str(agents.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0]))
							# 1-1 check
							agents.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0] = \
								self.one_minus_one_check2(agents.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0])
							# Update the preferences for that partial knowledge agent
							self.instrument_preference_update(agents, 1 + links.agent2.unique_id, AS_theory, len_DC, len_PC, len_S, instruments)
							# Calculation of the new grade - Based on the preference for the instrument
							cw_grade = abs(agents.instrument_preferences[0][agents.select_pinstrument] - agents.instrument_preferences[1 + links.agent2.unique_id][agents.select_pinstrument])
							# print('cw_grade: ' + str(cw_grade))
							# Restoring the initial values
							agents.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0] = original_belief[0]
							# Re-updating the preference levels
							self.instrument_preference_update(agents, 1 + links.agent2.unique_id, AS_theory, len_DC, len_PC, len_S, instruments)
							# Adding the grade to the grade list
							total_grade_list.append(cw_grade)
							# Reset to None after finding the grade
							if check_none == 1:
								agents.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0] = None

						# Checking which agent in the link is the original agent
						if links.agent2 == agents:
							# Check if no partial knowledge (initial value)
							check_none = 0
							if agents.belieftree[1 + links.agent1.unique_id][cw_of_interest[cw]][0] == None:
								agents.belieftree[1 + links.agent1.unique_id][cw_of_interest[cw]][0] = 0
								check_none = 1
							# Memorising the original belief values
							original_belief = [0]
							original_belief[0] = copy.copy(agents.belieftree[1 + links.agent1.unique_id][cw_of_interest[cw]][0])
							# Performing the action
							# print(' ')
							# print('Old value of the CR: ' + str(agents.belieftree[1 + links.agent1.unique_id][cw_of_interest[cw]][0]))
							agents.belieftree[1 + links.agent1.unique_id][cw_of_interest[cw]][0] += \
								(agents.belieftree[0][cw_of_interest[cw]][0] - agents.belieftree[1 + links.agent1.unique_id][cw_of_interest[cw]][0]) * \
								agents.resources[0] * resources_weight_action * links.aware * resources_potency
							# print('New value of the CR: ' + str(agents.belieftree[1 + links.agent1.unique_id][cw_of_interest[cw]][0]))
							# 1-1 check
							agents.belieftree[1 + links.agent1.unique_id][cw_of_interest[cw]][0] = \
								self.one_minus_one_check2(agents.belieftree[1 + links.agent1.unique_id][cw_of_interest[cw]][0])
							# Update the preferences for that partial knowledge agent
							self.instrument_preference_update(agents, 1 + links.agent1.unique_id, AS_theory, len_DC, len_PC, len_S, instruments)
							# Calculation of the new grade - Based on the preference for the instrument
							cw_grade = abs(agents.instrument_preferences[0][agents.select_pinstrument] - agents.instrument_preferences[1 + links.agent1.unique_id][agents.select_pinstrument])
							# print('cw_grade: ' + str(cw_grade))
							# Restoring the initial values
							agents.belieftree[1 + links.agent1.unique_id][cw_of_interest[cw]][0] = original_belief[0]
							# Re-updating the preference levels
							self.instrument_preference_update(agents, 1 + links.agent1.unique_id, AS_theory, len_DC, len_PC, len_S, instruments)
							# Adding the grade to the grade list
							total_grade_list.append(cw_grade)
							# Reset to None after finding the grade
							if check_none == 1:
								agents.belieftree[1 + links.agent1.unique_id][cw_of_interest[cw]][0] = None

					# print(total_grade_list)

					# 2. Grading all individual actions - Aim change

					# Going though all possible choices of issue
					for issue_num in range(len(issue_of_interest)):
					
						if links.agent1 == agents:
							# Looking at the policy chosen by the agent.
							# Check if no partial knowledge (initial value)
							check_none = 0
							if agents.belieftree[1 + links.agent2.unique_id][issue_of_interest[issue_num]][1] == None:
								agents.belieftree[1 + links.agent2.unique_id][issue_of_interest[issue_num]][1] = 0
								check_none = 1
							# Memorising the original belief values
							original_belief = [0]
							original_belief[0] = copy.copy(agents.belieftree[1 + links.agent2.unique_id][issue_of_interest[issue_num]][1])
							# If it knows that the agent has no interest in this issue, then set the grade to 0
							if agents.belieftree[1 + links.agent2.unique_id][issue_of_interest[issue_num]][0] == 'No' or \
							  agents.belieftree[0][issue_of_interest[issue_num]][0] == 'No':
								aim_grade = 0
							else:	
								# Performing the action
								# print(' ')
								# print('Old value of the aim: ' + str(agents.belieftree[1 + links.agent2.unique_id][issue_of_interest[issue_num]][1]))
								agents.belieftree[1 + links.agent2.unique_id][issue_of_interest[issue_num]][1] += \
									(agents.belieftree[0][issue_of_interest[issue_num]][1] - agents.belieftree[1 + links.agent2.unique_id][issue_of_interest[issue_num]][1]) * \
									agents.resources[0] * resources_weight_action * links.aware * links.conflict_level[0][issue_of_interest[issue_num]][1] * actionWeight * resources_potency
								# 1-1 check
								agents.belieftree[1 + links.agent2.unique_id][issue_of_interest[issue_num]][1] = \
									self.one_minus_one_check2(agents.belieftree[1 + links.agent2.unique_id][issue_of_interest[issue_num]][1])
								# Re-updating the preference levels
								self.instrument_preference_update(agents, 1 + links.agent2.unique_id, AS_theory, len_DC, len_PC, len_S, instruments)
								# Calculation of the new grade
								aim_grade = abs(agents.instrument_preferences[0][agents.select_pinstrument] - agents.instrument_preferences[1 + links.agent2.unique_id][agents.select_pinstrument])
							# print('New value of the aim: ' + str(agents.belieftree[1 + links.agent2.unique_id][issue_of_interest[issue_num]][1]))
							# print('aim_grade: ' + str(aim_grade))
							# Restoring the initial values
							agents.belieftree[1 + links.agent2.unique_id][issue_of_interest[issue_num]][1] = original_belief[0]
							# Re-updating the preference levels
							self.instrument_preference_update(agents, 1 + links.agent2.unique_id, AS_theory, len_DC, len_PC, len_S, instruments)
							# Adding the grade to the grade list
							total_grade_list.append(aim_grade)
							# Reset to None after finding the grade
							if check_none == 1:
								agents.belieftree[1 + links.agent2.unique_id][issue_of_interest[issue_num]][1] = None
							
						if links.agent2 == agents:

							# Looking at the policy chosen by the agent.
							# Check if no partial knowledge (initial value)
							check_none = 0
							if agents.belieftree[1 + links.agent1.unique_id][issue_of_interest[issue_num]][1] == None:
								agents.belieftree[1 + links.agent1.unique_id][issue_of_interest[issue_num]][1] = 0
								check_none = 1
							# Memorising the original belief values
							original_belief = [0]
							original_belief[0] = copy.copy(agents.belieftree[1 + links.agent1.unique_id][issue_of_interest[issue_num]][1])
							# If it knows that the agent has no interest in this issue, then set the grade to 0
							if agents.belieftree[1 + links.agent1.unique_id][issue_of_interest[issue_num]][0] == 'No' or \
							  agents.belieftree[0][issue_of_interest[issue_num]][0] == 'No':
								aim_grade = 0
							else:	
								# Performing the action
								# print(' ')
								# print('Old value of the aim: ' + str(agents.belieftree[1 + links.agent1.unique_id][issue_of_interest[issue_num]][1]))
								agents.belieftree[1 + links.agent1.unique_id][issue_of_interest[issue_num]][1] += \
									(agents.belieftree[0][issue_of_interest[issue_num]][1] - agents.belieftree[1 + links.agent1.unique_id][issue_of_interest[issue_num]][1]) * \
									agents.resources[0] * resources_weight_action * links.aware * links.conflict_level[1][issue_of_interest[issue_num]][1] * actionWeight * resources_potency
								# 1-1 check
								agents.belieftree[1 + links.agent1.unique_id][issue_of_interest[issue_num]][1] = \
									self.one_minus_one_check2(agents.belieftree[1 + links.agent1.unique_id][issue_of_interest[issue_num]][1])
								# Re-updating the preference levels
								self.instrument_preference_update(agents, 1 + links.agent1.unique_id, AS_theory, len_DC, len_PC, len_S, instruments)
								# Calculation of the new grade
								aim_grade = abs(agents.instrument_preferences[0][agents.select_pinstrument] - agents.instrument_preferences[1 + links.agent1.unique_id][agents.select_pinstrument])
							# print('New value of the aim: ' + str(agents.belieftree[1 + links.agent1.unique_id][issue_of_interest[issue_num]][1]))
							# print('aim_grade: ' + str(aim_grade))
							# Restoring the initial values
							agents.belieftree[1 + links.agent1.unique_id][issue_of_interest[issue_num]][1] = original_belief[0]
							# Re-updating the preference levels
							self.instrument_preference_update(agents, 1 + links.agent1.unique_id, AS_theory, len_DC, len_PC, len_S, instruments)
							# Adding the grade to the grade list
							total_grade_list.append(aim_grade)
							# Reset to None after finding the grade
							if check_none == 1:
								agents.belieftree[1 + links.agent1.unique_id][issue_of_interest[issue_num]][1] = None

						# print(total_grade_list)

					# 3. Grading all individual actions - State change

					# Going though all possible choices of issue
					for issue_num in range(len(issue_of_interest)):

						if links.agent1 == agents:
								
							# Looking at the policy chosen by the agent.
							# Check if no partial knowledge (initial value)
							check_none = 0
							if agents.belieftree[1 + links.agent2.unique_id][issue_of_interest[issue_num]][0] == None:
								agents.belieftree[1 + links.agent2.unique_id][issue_of_interest[issue_num]][0] = 0
								check_none = 1
							# Memorising the original belief values
							original_belief = [0]
							original_belief[0] = copy.copy(agents.belieftree[1 + links.agent2.unique_id][issue_of_interest[issue_num]][0])
							# If it knows that the agent has no interest in this issue, then set the grade to 0
							if agents.belieftree[1 + links.agent2.unique_id][issue_of_interest[issue_num]][0] == 'No' or \
							  agents.belieftree[0][issue_of_interest[issue_num]][0] == 'No':
								state_grade = 0
							else:	
								# Performing the action
								# print(' ')
								# print('Old value of the aim: ' + str(agents.belieftree[1 + links.agent2.unique_id][issue_of_interest[issue_num]][0]))
								agents.belieftree[1 + links.agent2.unique_id][issue_of_interest[issue_num]][0] += \
									(agents.belieftree[0][issue_of_interest[issue_num]][0] - agents.belieftree[1 + links.agent2.unique_id][issue_of_interest[issue_num]][0]) * \
									agents.resources[0] * resources_weight_action * links.aware * links.conflict_level[0][issue_of_interest[issue_num]][0] * actionWeight * resources_potency
								# 1-1 check
								agents.belieftree[1 + links.agent2.unique_id][issue_of_interest[issue_num]][0] = \
									self.one_minus_one_check2(agents.belieftree[1 + links.agent2.unique_id][issue_of_interest[issue_num]][0])
								# Re-updating the preference levels
								self.instrument_preference_update(agents, 1 + links.agent2.unique_id, AS_theory, len_DC, len_PC, len_S, instruments)
								# Calculation of the new grade
								state_grade = abs(agents.instrument_preferences[0][agents.select_pinstrument] - agents.instrument_preferences[1 + links.agent2.unique_id][agents.select_pinstrument])
							# print('New value of the aim: ' + str(agents.belieftree[1 + links.agent2.unique_id][issue_of_interest[issue_num]][0]))
							# print('state_grade: ' + str(state_grade))
							# Restoring the initial values
							agents.belieftree[1 + links.agent2.unique_id][issue_of_interest[issue_num]][0] = original_belief[0]
							# Re-updating the preference levels
							self.instrument_preference_update(agents, 1 + links.agent2.unique_id, AS_theory, len_DC, len_PC, len_S, instruments)
							# Adding the grade to the grade list
							total_grade_list.append(state_grade)
							# Reset to None after finding the grade
							if check_none == 1:
								agents.belieftree[1 + links.agent2.unique_id][issue_of_interest[issue_num]][0] = None

						if links.agent2 == agents:

							# Looking at the policy chosen by the agent.
							# Check if no partial knowledge (initial value)
							check_none = 0
							if agents.belieftree[1 + links.agent1.unique_id][issue_of_interest[issue_num]][0] == None:
								agents.belieftree[1 + links.agent1.unique_id][issue_of_interest[issue_num]][0] = 0
								check_none = 1
							# Memorising the original belief values
							original_belief = [0]
							original_belief[0] = copy.copy(agents.belieftree[1 + links.agent1.unique_id][issue_of_interest[issue_num]][0])
							# If it knows that the agent has no interest in this issue, then set the grade to 0
							if agents.belieftree[1 + links.agent1.unique_id][issue_of_interest[issue_num]][0] == 'No' or \
							  agents.belieftree[0][issue_of_interest[issue_num]][0] == 'No':
								state_grade = 0
							else:	
								# Performing the action
								# print(' ')
								# print('Old value of the aim: ' + str(agents.belieftree[1 + links.agent1.unique_id][issue_of_interest[issue_num]][0]))
								agents.belieftree[1 + links.agent1.unique_id][issue_of_interest[issue_num]][0] += \
									(agents.belieftree[0][issue_of_interest[issue_num]][0] - agents.belieftree[1 + links.agent1.unique_id][issue_of_interest[issue_num]][0]) * \
									agents.resources[0] * resources_weight_action * links.aware * links.conflict_level[0][issue_of_interest[issue_num]][0] * actionWeight * resources_potency
								# 1-1 check
								agents.belieftree[1 + links.agent1.unique_id][issue_of_interest[issue_num]][0] = \
									self.one_minus_one_check2(agents.belieftree[1 + links.agent1.unique_id][issue_of_interest[issue_num]][0])
								# Re-updating the preference levels
								self.instrument_preference_update(agents, 1 + links.agent1.unique_id, AS_theory, len_DC, len_PC, len_S, instruments)
								# Calculation of the new grade
								state_grade = abs(agents.instrument_preferences[0][agents.select_pinstrument] - agents.instrument_preferences[1 + links.agent1.unique_id][agents.select_pinstrument])
							# print('New value of the aim: ' + str(agents.belieftree[1 + links.agent1.unique_id][issue_of_interest[issue_num]][0]))
							# print('state_grade: ' + str(state_grade))
							# Restoring the initial values
							agents.belieftree[1 + links.agent1.unique_id][issue_of_interest[issue_num]][0] = original_belief[0]
							# Re-updating the preference levels
							self.instrument_preference_update(agents, 1 + links.agent1.unique_id, AS_theory, len_DC, len_PC, len_S, instruments)
							# Adding the grade to the grade list
							total_grade_list.append(state_grade)
							# Reset to None after finding the grade
							if check_none == 1:
								agents.belieftree[1 + links.agent1.unique_id][issue_of_interest[issue_num]][0] = None

			# print(' ')
			# print(total_grade_list)

			# 4. Choosing an action
			best_action_index = total_grade_list.index(min(total_grade_list))

			# print(' ')
			# print('------ New action grade check -------')
			# print('Grade length: ' + str(len(total_grade_list)))
			# print('Best index: ' + str(best_action_index))
			# print('Number of links: ' + str(len(total_grade_list_links)))
			# print('Number of grades per link: ' + str(len(cw_of_interest) + 2 * len(issue_of_interest)))
			# print('Link for this action: ' + str(int(best_action_index / (len(cw_of_interest) + 2 * len(issue_of_interest) ) )))
			
			best_action = best_action_index - ((len(cw_of_interest) + 2 * len(issue_of_interest)) * int(best_action_index / (len(cw_of_interest) + 2 * len(issue_of_interest) ) ))
			# print('Best action selected: ' + str(best_action))

			for links in link_list:

				if links == total_grade_list_links[int(best_action_index / (len(cw_of_interest) + 2 * len(issue_of_interest) ) )]:
					# print(links)					

					# 5. Performing the actual action
					# If the index is in the first part of the list, then the framing action is the best
					if best_action <= len(cw_of_interest) - 1:

						# print(' ')
						# print('Framing action - causal relation')
						# print('best_action: ' + str(best_action))
						# print('of_interest[0]: ' + str(of_interest[0]))
						# print('of_interest[0][best_action]: ' + str(of_interest[0][best_action]))

						# Update of the aware decay parameter
						links.aware_decay = 5

						if links.agent1 == agents:
							# print('Before: ' + str(links.agent2.belieftree[0][len(self.deep_core) + len(self.policy_core) + len(self.secondary) + best_action][0]))
							links.agent2.belieftree[0][of_interest[0][best_action]][0] += \
								(agents.belieftree[0][of_interest[0][best_action]][0] - links.agent2.belieftree[0][of_interest[0][best_action]][0]) * \
								agents.resources[0] * resources_weight_action * links.aware * resources_potency
							# print('After: ' + str(links.agent2.belieftree[0][len(self.deep_core) + len(self.policy_core) + len(self.secondary) + best_action][0]))
							# 1-1 check
							if links.agent2.belieftree[0][of_interest[0][best_action]][0] > 1:
								links.agent2.belieftree[0][of_interest[0][best_action]][0] = 1
							if links.agent2.belieftree[0][of_interest[0][best_action]][0] < - 1:
								links.agent2.belieftree[0][of_interest[0][best_action]][0] = -1
							# self.one_minus_one_check(links.agent2.belieftree[0][of_interest[0][best_action]][0])
							# Providing partial knowledge - Framing - 0.2 range from real value: (Acting agent)
							agents.belieftree[1 + links.agent2.unique_id][of_interest[0][best_action]][0] = links.agent2.belieftree[0][of_interest[0][best_action]][0] + (random.random()/5) - 0.1
							# 1-1 check
							if agents.belieftree[1 + links.agent2.unique_id][of_interest[0][best_action]][0] > 1:
								agents.belieftree[1 + links.agent2.unique_id][of_interest[0][best_action]][0] = 1
							if agents.belieftree[1 + links.agent2.unique_id][of_interest[0][best_action]][0] < -1:
								agents.belieftree[1 + links.agent2.unique_id][of_interest[0][best_action]][0] = -1
							# self.one_minus_one_check(agents.belieftree[1 + links.agent2.unique_id][of_interest[0][best_action]][0])
							# Providing partial knowledge - Framing - 0.2 range from real value: (Acted upon agent)
							links.agent2.belieftree[1 + agents.unique_id][of_interest[0][best_action]][0] = agents.belieftree[0][of_interest[0][best_action]][0] + (random.random()/5) - 0.1
							# 1-1 check
							if links.agent2.belieftree[1 + agents.unique_id][of_interest[0][best_action]][0] > 1:
								links.agent2.belieftree[1 + agents.unique_id][of_interest[0][best_action]][0] = 1
							if links.agent2.belieftree[1 + agents.unique_id][of_interest[0][best_action]][0] < -1:
								links.agent2.belieftree[1 + agents.unique_id][of_interest[0][best_action]][0] = -1
							# self.one_minus_one_check(links.agent2.belieftree[1 + agents.unique_id][of_interest[0][best_action]][0])

						# Checking which agent in the link is the original agent
						if links.agent2 == agents:
							# print('Before: ' + str(links.agent1.belieftree[0][len(self.deep_core) + len(self.policy_core) + len(self.secondary) + best_action][0]))
							links.agent1.belieftree[0][of_interest[0][best_action]][0] += \
								(agents.belieftree[0][of_interest[0][best_action]][0] - links.agent1.belieftree[0][of_interest[0][best_action]][0]) * \
								agents.resources[0] * resources_weight_action * links.aware * resources_potency
							# print('After: ' + str(links.agent1.belieftree[0][len(self.deep_core) + len(self.policy_core) + len(self.secondary) + best_action][0]))
							# 1-1 check
							if links.agent1.belieftree[0][of_interest[0][best_action]][0] > 1:
								links.agent1.belieftree[0][of_interest[0][best_action]][0] = -1
							if links.agent1.belieftree[0][of_interest[0][best_action]][0] < -1:
								links.agent1.belieftree[0][of_interest[0][best_action]][0] = -1
							# self.one_minus_one_check(links.agent1.belieftree[0][of_interest[0][best_action]][0])
							# Providing partial knowledge - Framing - 0.2 range from real value: (Acting agent)
							agents.belieftree[1 + links.agent1.unique_id][of_interest[0][best_action]][0] = links.agent1.belieftree[0][of_interest[0][best_action]][0] + (random.random()/5) - 0.1
							# 1-1 check
							if agents.belieftree[1 + links.agent1.unique_id][of_interest[0][best_action]][0] > 1:
								agents.belieftree[1 + links.agent1.unique_id][of_interest[0][best_action]][0] = 1
							if agents.belieftree[1 + links.agent1.unique_id][of_interest[0][best_action]][0] < -1:
								agents.belieftree[1 + links.agent1.unique_id][of_interest[0][best_action]][0] = -1
							# self.one_minus_one_check(agents.belieftree[1 + links.agent1.unique_id][of_interest[0][best_action]][0])
							# Providing partial knowledge - Framing - 0.2 range from real value: (Acted upon agent)
							links.agent1.belieftree[1 + agents.unique_id][of_interest[0][best_action]][0] = agents.belieftree[0][of_interest[0][best_action]][0] + (random.random()/5) - 0.1
							# 1-1 check
							if links.agent1.belieftree[1 + agents.unique_id][of_interest[0][best_action]][0] > 1:
								links.agent1.belieftree[1 + agents.unique_id][of_interest[0][best_action]][0] = 1
							if links.agent1.belieftree[1 + agents.unique_id][of_interest[0][best_action]][0] < -1:
								links.agent1.belieftree[1 + agents.unique_id][of_interest[0][best_action]][0] = -1
							# self.one_minus_one_check(links.agent1.belieftree[1 + agents.unique_id][of_interest[0][best_action]][0])

					# If the index is in the second part of the list, then the aim influence action on the problem is the best
					if best_action > len(cw_of_interest) - 1 and best_action < len(cw_of_interest) + len(issue_of_interest) - 1:

						# print(' ')
						# print('Aim influence action')
						# print('best_action: ' + str(best_action))
						# print('of_interest[1]: ' + str(of_interest[1]))
						# print('of_interest[1][best_action - len(cw_of_interest)]: ' + str(of_interest[1][best_action - len(cw_of_interest)]))
						
						# Update of the aware decay parameter
						links.aware_decay = 5

						if links.agent1 == agents:
							links.agent2.belieftree[0][of_interest[1][best_action - len(cw_of_interest)] ][1] += \
								(agents.belieftree[0][of_interest[1][best_action - len(cw_of_interest)] ][1] - links.agent2.belieftree[0][agenda_as_issue][1]) * \
								agents.resources[0] * resources_weight_action * links.aware * resources_potency
							# 1-1 check
							links.agent2.belieftree[0][of_interest[1][best_action - len(cw_of_interest)]][1] = \
								self.one_minus_one_check2(links.agent2.belieftree[0][of_interest[1][best_action - len(cw_of_interest)]][1])		
							# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acting agent)
							agents.belieftree[1 + links.agent2.unique_id][of_interest[1][best_action - len(cw_of_interest)] ][1] = links.agent2.belieftree[0][of_interest[1][best_action - len(cw_of_interest)] ][1] + (random.random()/5) - 0.1
							# 1-1 check
							agents.belieftree[1 + links.agent2.unique_id][of_interest[1][best_action - len(cw_of_interest)] ][1] = \
								self.one_minus_one_check2(agents.belieftree[1 + links.agent2.unique_id][of_interest[1][best_action - len(cw_of_interest)] ][1])
							# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acted upon agent)
							links.agent2.belieftree[1 + agents.unique_id][of_interest[1][best_action - len(cw_of_interest)] ][1] = agents.belieftree[0][of_interest[1][best_action - len(cw_of_interest)] ][1] + (random.random()/5) - 0.1
							# 1-1 check
							links.agent2.belieftree[1 + agents.unique_id][of_interest[1][best_action - len(cw_of_interest)] ][1] = \
								self.one_minus_one_check2(links.agent2.belieftree[1 + agents.unique_id][of_interest[1][best_action - len(cw_of_interest)] ][1])

						if links.agent2 == agents:
							# print('Before: ' + str(links.agent1.belieftree[0][len(self.deep_core) + agents.select_problem][1]))
							links.agent1.belieftree[0][of_interest[1][best_action - len(cw_of_interest)] ][1] += \
								(agents.belieftree[0][of_interest[1][best_action - len(cw_of_interest)] ][1] - links.agent1.belieftree[0][of_interest[1][best_action - len(cw_of_interest)] ][1]) * \
								agents.resources[0] * resources_weight_action * links.aware * resources_potency
							# print('After: ' + str(links.agent1.belieftree[0][len(self.deep_core) + agents.select_problem][1]))
							# 1-1 check
							links.agent1.belieftree[0][of_interest[1][best_action - len(cw_of_interest)]][1] = \
								self.one_minus_one_check2(links.agent1.belieftree[0][of_interest[1][best_action - len(cw_of_interest)]][1]   )		
							# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acting agent)
							agents.belieftree[1 + links.agent1.unique_id][of_interest[1][best_action - len(cw_of_interest)]][1] = links.agent1.belieftree[0][of_interest[1][best_action - len(cw_of_interest)] ][1] + (random.random()/5) - 0.1
							# 1-1 check
							agents.belieftree[1 + links.agent1.unique_id][of_interest[1][best_action - len(cw_of_interest)]][1] = \
								self.one_minus_one_check2(agents.belieftree[1 + links.agent1.unique_id][of_interest[1][best_action - len(cw_of_interest)]][1])
							# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acted upon agent)
							links.agent1.belieftree[1 + agents.unique_id][of_interest[1][best_action - len(cw_of_interest)] ][1] = agents.belieftree[0][of_interest[1][best_action - len(cw_of_interest)] ][1] + (random.random()/5) - 0.1
							# 1-1 check
							links.agent1.belieftree[1 + agents.unique_id][of_interest[1][best_action - len(cw_of_interest)] ][1] = \
								self.one_minus_one_check2(links.agent1.belieftree[1 + agents.unique_id][of_interest[1][best_action - len(cw_of_interest)] ][1])

					# If the index is in the first part of the list, then the aim influence action on the policy is the best
					if best_action >= len(cw_of_interest) + len(issue_of_interest) - 1:

						# print(' ')
						# print('Aim influence action')
						# print('best_action: ' + str(best_action))
						# print('of_interest[1]: ' + str(of_interest[1]))
						# print('of_interest[1][best_action - len(cw_of_interest) - len(issue_of_interest)]: ' + str(of_interest[1][best_action - len(cw_of_interest) - len(issue_of_interest)]))

						# Update of the aware decay parameter
						links.aware_decay = 5

						if links.agent1 == agents:
							links.agent2.belieftree[0][of_interest[1][best_action - len(cw_of_interest) - len(issue_of_interest)]][0] += \
								(agents.belieftree[0][of_interest[1][best_action - len(cw_of_interest) - len(issue_of_interest)]][0] - \
								links.agent2.belieftree[0][of_interest[1][best_action - len(cw_of_interest) - len(issue_of_interest)]][1]) * \
								agents.resources[0] * resources_weight_action * links.aware * resources_potency
							# 1-1 check
							links.agent2.belieftree[0][of_interest[1][best_action - len(cw_of_interest) - len(issue_of_interest)]][0] = \
								self.one_minus_one_check2(links.agent2.belieftree[0][of_interest[1][best_action - len(cw_of_interest) - len(issue_of_interest)]][0])
							# Providing partial knowledge - Aim policy - 0.2 range from real value: (Acting agent)
							agents.belieftree[1 + links.agent2.unique_id][of_interest[1][best_action - len(cw_of_interest) - len(issue_of_interest)]][0] = \
								links.agent2.belieftree[0][of_interest[1][best_action - len(cw_of_interest) - len(issue_of_interest)]][0] + (random.random()/5) - 0.1
							# 1-1 check
							agents.belieftree[1 + links.agent2.unique_id][of_interest[1][best_action - len(cw_of_interest) - len(issue_of_interest)]][0] = \
								self.one_minus_one_check2(agents.belieftree[1 + links.agent2.unique_id][of_interest[1][best_action - len(cw_of_interest) - len(issue_of_interest)]][0])
							# Providing partial knowledge - Aim policy - 0.2 range from real value: (Acted upon agent)
							links.agent2.belieftree[1 + agents.unique_id][of_interest[1][best_action - len(cw_of_interest) - len(issue_of_interest)]][0] = \
								agents.belieftree[0][of_interest[1][best_action - len(cw_of_interest) - len(issue_of_interest)]][0] + (random.random()/5) - 0.1
							# 1-1 check
							links.agent2.belieftree[1 + agents.unique_id][of_interest[1][best_action - len(cw_of_interest) - len(issue_of_interest)]][0] = \
								self.one_minus_one_check2(links.agent2.belieftree[1 + agents.unique_id][of_interest[1][best_action - len(cw_of_interest) - len(issue_of_interest)]][0])

						if links.agent2 == agents:
							links.agent1.belieftree[0][of_interest[1][best_action - len(cw_of_interest) - len(issue_of_interest)]][0] += \
								(agents.belieftree[0][of_interest[1][best_action - len(cw_of_interest) - len(issue_of_interest)]][0] - \
								links.agent1.belieftree[0][of_interest[1][best_action - len(cw_of_interest) - len(issue_of_interest)]][0]) * \
								agents.resources[0] * resources_weight_action * links.aware * resources_potency
							# 1-1 check
							links.agent1.belieftree[0][of_interest[1][best_action - len(cw_of_interest) - len(issue_of_interest)]][0] = \
								self.one_minus_one_check2(links.agent1.belieftree[0][of_interest[1][best_action - len(cw_of_interest) - len(issue_of_interest)]][0])
							# Providing partial knowledge - Aim policy - 0.2 range from real value: (Acting agent)
							agents.belieftree[1 + links.agent1.unique_id][of_interest[1][best_action - len(cw_of_interest) - len(issue_of_interest)]][0] = \
								links.agent1.belieftree[0][of_interest[1][best_action - len(cw_of_interest) - len(issue_of_interest)]][0] + (random.random()/5) - 0.1
							# 1-1 check
							agents.belieftree[1 + links.agent1.unique_id][of_interest[1][best_action - len(cw_of_interest) - len(issue_of_interest)]][0] = \
								self.one_minus_one_check2(agents.belieftree[1 + links.agent1.unique_id][of_interest[1][best_action - len(cw_of_interest) - len(issue_of_interest)]][0])
							# Providing partial knowledge - Aim policy - 0.2 range from real value: (Acted upon agent)
							links.agent1.belieftree[1 + agents.unique_id][of_interest[1][best_action - len(cw_of_interest) - len(issue_of_interest)]][0] = \
								agents.belieftree[0][of_interest[1][best_action - len(cw_of_interest) - len(issue_of_interest)]][0] + (random.random()/5) - 0.1
							# 1-1 check
							links.agent1.belieftree[1 + agents.unique_id][of_interest[1][best_action - len(cw_of_interest) - len(issue_of_interest)]][0] = \
								self.one_minus_one_check2(links.agent1.belieftree[1 + agents.unique_id][of_interest[1][best_action - len(cw_of_interest) - len(issue_of_interest)]][0])

			# print('Resources left: ' + str(agents.resources_actions))
			agents.resources_actions -= agents.resources[0] * resources_weight_action

	def pm_pe_actions_as_3S(self, agents, link_list, deep_core, policy_core, secondary, resources_weight_action, resources_potency):

		len_DC = len(deep_core)
		len_PC = len(policy_core)
		len_S = len(secondary)

		# Selection of the cw of interest
		cw_of_interest = []
		# We only consider the causal relations related to the problem on the agenda

		for cw_choice in range(len(deep_core)):
				cw_of_interest.append(len_DC + len_PC + len_S + (agents.select_problem_3S_as - len_DC) + cw_choice * len(policy_core))

		# Selection of the impact of interest
		impact_number = len(agents.belieftree_policy[0][agents.select_policy_3S_as])

		# print(' ')
		# print('Causal relations of interest: ' + str(cw_of_interest))

		# Making sure there are enough resources
		while agents.resources_actions > 0.001:

			# Going through all the links in the model
			# print(agents)
			total_grade_list = []
			total_grade_list_links = []
			for links in link_list:

				# Making sure that the link is attached to the agent and has a aware higher than 0
				if (links.agent1 == agents or links.agent2 == agents) and links.aware > 0:
					total_grade_list_links.append(links)

					# Definition the action weight parameter
					if type(links.agent1) == Policymakers or type(links.agent2) == Policymakers:
						actionWeight = 1
					else:
						actionWeight = 0.95
					
					# 1. Framing on causal relation and policy impacts

					# If the agent is advocating or a problem, the following tasks are performed
					if agents.select_issue_3S_as == 'problem':
						# 1.a. Grading all framing actions on causal relations:
						# Checking through all possible framing - This is all based on partial knowledge!
						for cw in range(len(cw_of_interest)):

							# Checking which agent in the link is the original agent
							if links.agent1 == agents:
								# Check if no partial knowledge (initial value)
								check_none = 0
								if agents.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0] == None:
									agents.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0] = 0
									check_none = 1
								# Performing the action
								cw_grade = (agents.belieftree[0][cw_of_interest[cw]][0] - agents.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0]) * \
									agents.resources[0] * resources_weight_action * links.aware * resources_potency
								# Adding the grade to the grade list
								total_grade_list.append(cw_grade)
								#  Reset to None after finding the grade
								if check_none == 1:
									agents.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0] = None

							# Checking which agent in the link is the original agent
							if links.agent2 == agents:
								#  Check if no partial knowledge (initial value)
								check_none = 0
								if agents.belieftree[1 + links.agent1.unique_id][cw_of_interest[cw]][0] == None:
									agents.belieftree[1 + links.agent1.unique_id][cw_of_interest[cw]][0] = 0
									check_none = 1
								# Performing the action
								cw_grade = (agents.belieftree[0][cw_of_interest[cw]][0] - agents.belieftree[1 + links.agent1.unique_id][cw_of_interest[cw]][0]) * \
									agents.resources[0] * resources_weight_action * links.aware * resources_potency
								# Adding the grade to the grade list
								total_grade_list.append(cw_grade)
								# Reset to None after finding the grade
								if check_none == 1:
									agents.belieftree[1 + links.agent1.unique_id][cw_of_interest[cw]][0] = None

					# If the agent is advocating or a policy, the following tasks are performed
					if agents.select_issue_3S_as == 'policy':
						# 1.b. Grading all framing actions on policy impacts:

						# Checking through all possible framing - This is all based on partial knowledge!
						for impact in range(impact_number):

							# Checking which agent in the link is the original agent
							if links.agent1 == agents:
								# Check if no partial knowledge (initial value)
								check_none = 0
								if agents.belieftree_policy[1 + links.agent2.unique_id][agents.select_policy_3S_as][impact] == None:
									agents.belieftree_policy[1 + links.agent2.unique_id][agents.select_policy_3S_as][impact] = 0
									check_none = 1
								# Performing the action
								impact_grade = (agents.belieftree_policy[0][agents.select_policy_3S_as][impact] - agents.belieftree_policy[1 + links.agent2.unique_id][agents.select_policy_3S_as][impact]) * \
									agents.resources[0] * resources_weight_action * links.aware * resources_potency
								# Adding the grade to the grade list
								total_grade_list.append(impact_grade)
								#  Reset to None after finding the grade
								if check_none == 1:
									agents.belieftree_policy[1 + links.agent2.unique_id][agents.select_policy_3S_as][impact] = None

							# Checking which agent in the link is the original agent
							if links.agent2 == agents:
								#  Check if no partial knowledge (initial value)
								check_none = 0
								if agents.belieftree_policy[1 + links.agent1.unique_id][agents.select_policy_3S_as][impact] == None:
									agents.belieftree_policy[1 + links.agent1.unique_id][agents.select_policy_3S_as][impact] = 0
									check_none = 1
								impact_grade = (agents.belieftree_policy[0][agents.select_policy_3S_as][impact] - agents.belieftree_policy[1 + links.agent1.unique_id][agents.select_policy_3S_as][impact]) * \
									agents.resources[0] * resources_weight_action * links.aware * resources_potency
								# Adding the grade to the grade list
								total_grade_list.append(impact_grade)
								# Reset to None after finding the grade
								if check_none == 1:
									agents.belieftree_policy[1 + links.agent1.unique_id][agents.select_policy_3S_as][impact] = None

					# 2. Grading all individual actions - Aim change
					if links.agent1 == agents:
						# Check if no partial knowledge (initial value)
						check_none = 0
						if agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][1] == None:
							agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][1] = 0
							check_none = 1
						# Performing the action
						aim_grade_issue = (agents.belieftree[0][agents.select_problem_3S_as][1] - agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][1]) * \
							agents.resources[0] * resources_weight_action * links.aware * links.conflict_level[0][agents.select_problem_3S_as][1] * actionWeight * resources_potency
						#  Reset to None after finding the grade
						if check_none == 1:
							agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][1] = None
						# Adding the grade to the grade list
						total_grade_list.append(aim_grade_issue)

					if links.agent2 == agents:
						# Check if no partial knowledge (initial value)
						check_none = 0
						if agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][1] == None:
							agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][1] = 0
							check_none = 1
						# Performing the action
						aim_grade_issue = (agents.belieftree[0][agents.select_problem_3S_as][1] - agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][1]) * \
							agents.resources[0] * resources_weight_action * links.aware * links.conflict_level[1][agents.select_problem_3S_as][1] * actionWeight * resources_potency
						#  Reset to None after finding the grade
						if check_none == 1:
							agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][1] = None
						# Adding the grade to the grade list
						total_grade_list.append(aim_grade_issue)

					# 3. Grading all individual actions - State change
					if links.agent1 == agents:
						# Check if no partial knowledge (initial value)
						check_none = 0
						if agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][0] == None:
							agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][0] = 0
							check_none = 1
						# Performing the action
						state_grade_issue = (agents.belieftree[0][agents.select_problem_3S_as][0] - agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][0]) * \
							agents.resources[0] * resources_weight_action * links.aware * links.conflict_level[0][agents.select_problem_3S_as][0] * actionWeight * resources_potency
						#  Reset to None after finding the grade
						if check_none == 1:
							agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][0] = None
						# Adding the grade to the grade list
						total_grade_list.append(state_grade_issue)

					if links.agent2 == agents:
						# Check if no partial knowledge (initial value)
						check_none = 0
						if agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][0] == None:
							agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][0] = 0
							check_none = 1
						# Performing the action
						state_grade_issue = (agents.belieftree[0][agents.select_problem_3S_as][0] - agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][0]) * \
							agents.resources[0] * resources_weight_action * links.aware * links.conflict_level[1][agents.select_problem_3S_as][0] * actionWeight * resources_potency
						#  Reset to None after finding the grade
						if check_none == 1:
							agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][0] = None
						# Adding the grade to the grade list
						total_grade_list.append(state_grade_issue)
					# print(' ')

			# print(' ')
			# print('Number of actions: ' + str(len(total_grade_list)))
			# print(total_grade_list)

			# 4. Choosing an action

			# If the agent is advocating or a problem, the following tasks are performed
			if agents.select_issue_3S_as == 'problem':

				best_action_index = total_grade_list.index(max(total_grade_list))
				agent_best_action = int(best_action_index/(len(cw_of_interest) + 1 + 1))
				best_action = best_action_index - (agent_best_action)*(len(cw_of_interest) + 1 + 1)

				# print(' ')
				# print('----- Considering new action grading (problem) -----')
				# print('best_action_index: ' + str(best_action_index))
				# print('Number of actions per agent: ' + str(len(cw_of_interest) + 1 + 1))
				# print('Total number of agents being influenced: ' + str(len(total_grade_list_links)))
				# print('Action to be performed: ' + str(best_action))
				# print('Agent performing the action: ' + str(agent_best_action))

			# If the agent is advocating or a policy, the following tasks are performed
			if agents.select_issue_3S_as == 'policy':
				
				best_action_index = total_grade_list.index(max(total_grade_list))
				agent_best_action = int(best_action_index/(impact_number + 1 + 1))
				best_action = best_action_index - (agent_best_action)*(impact_number + 1 + 1)

				# print(' ')
				# print('----- Considering new action grading (policy) -----')
				# print('best_action_index: ' + str(best_action_index))
				# print('Number of actions per agent: ' + str(impact_number + 1 + 1))
				# print('Total number of agents being influenced: ' + str(len(total_grade_list_links)))
				# print('Action to be performed: ' + str(best_action))
				# print('Agent performing the action: ' + str(agent_best_action))


			# 5. Performing the actual action
			# Selecting the link:
			for links in link_list:

				# If the agent is advocating or a problem, the following tasks are performed
				if agents.select_issue_3S_as == 'problem':

					if (links.agent1 == agents and links.agent2.unique_id == agent_best_action) or (links.agent1.unique_id == agent_best_action and links.agent2 == agents):
						# print(links)

						# Updating the aware decay parameter
						links.aware_decay = 5

						# If the index is in the first part of the list, then the framing action is the best
						if best_action <= len(cw_of_interest) - 1:
							# print(' ')
							# print('Performing a causal relation framing action')
							# print('best_action: ' + str(best_action))
							# print('cw_of_interest: ' + str(cw_of_interest))
							# print('cw_of_interest[best_action]: ' + str(cw_of_interest[best_action]))
							
							# To simplify the notations
							best_action = cw_of_interest[best_action]

							if links.agent1 == agents:
								
								# print('Before: ' + str(links.agent2.belieftree[0][best_action][0]))
								links.agent2.belieftree[0][best_action][0] += (agents.belieftree[0][best_action][0] - links.agent2.belieftree[0][best_action][0]) * \
									agents.resources[0] * resources_weight_action * links.aware * resources_potency
								# print('After: ' + str(links.agent2.belieftree[0][best_action][0]))
								# 1-1 check
								links.agent2.belieftree[0][best_action][0] = \
									self.one_minus_one_check2(links.agent2.belieftree[0][best_action][0])
								# Providing partial knowledge - Framing - 0.2 range from real value: (Acting agent)
								agents.belieftree[1 + links.agent2.unique_id][best_action][0] = links.agent2.belieftree[0][best_action][0] + (random.random()/5) - 0.1
								# 1-1 check
								agents.belieftree[1 + links.agent2.unique_id][best_action][0] = \
									self.one_minus_one_check2(agents.belieftree[1 + links.agent2.unique_id][best_action][0])
								# Providing partial knowledge - Framing - 0.2 range from real value: (Acted upon agent)
								links.agent2.belieftree[1 + agents.unique_id][best_action][0] = agents.belieftree[0][best_action][0] + (random.random()/5) - 0.1
								# 1-1 check
								links.agent2.belieftree[1 + agents.unique_id][best_action][0] = \
									self.one_minus_one_check2(links.agent2.belieftree[1 + agents.unique_id][best_action][0])

								# print(' ')
								# print('Causal change')
								# print(agents.belieftree[1 + links.agent2.unique_id])
								# print(agents.belieftree[1 + links.agent2.unique_id][best_action][0])

							# Checking which agent in the link is the original agent
							if links.agent2 == agents:

								# print('Before: ' + str(links.agent1.belieftree[0][best_action][0]))
								links.agent1.belieftree[0][best_action][0] += (agents.belieftree[0][best_action][0] - links.agent1.belieftree[0][best_action][0]) * \
									agents.resources[0] * resources_weight_action * links.aware * resources_potency
								# print('After: ' + str(links.agent1.belieftree[0][best_action][0]))
								# 1-1 check
								links.agent1.belieftree[0][best_action][0] = \
									self.one_minus_one_check2(links.agent1.belieftree[0][best_action][0])
								# Providing partial knowledge - Framing - 0.2 range from real value: (Acting agent)
								agents.belieftree[1 + links.agent1.unique_id][best_action][0] = links.agent1.belieftree[0][best_action][0] + (random.random()/5) - 0.1
								# 1-1 check
								agents.belieftree[1 + links.agent1.unique_id][best_action][0] = \
									self.one_minus_one_check2(agents.belieftree[1 + links.agent1.unique_id][best_action][0])
								# Providing partial knowledge - Framing - 0.2 range from real value: (Acted upon agent)
								links.agent1.belieftree[1 + agents.unique_id][best_action][0] = agents.belieftree[0][best_action][0] + (random.random()/5) - 0.1
								# 1-1 check
								links.agent1.belieftree[1 + agents.unique_id][best_action][0] = \
									self.one_minus_one_check2(links.agent1.belieftree[1 + agents.unique_id][best_action][0])

								# print(' ')
								# print('Causal change')
								# print(agents.belieftree[1 + links.agent1.unique_id])
								# print(agents.belieftree[1 + links.agent1.unique_id][best_action][0])

						# If the index is in the second part of the list, then the aim influence action is the best
						if best_action == len(cw_of_interest):
							# print(' ')
							# print('Performing a state change action')
							# print('best_action: ' + str(best_action))

							if links.agent1 == agents:
								# print('Before: ' + str(links.agent2.belieftree[0][agents.select_problem_3S_as][1]))
								links.agent2.belieftree[0][agents.select_problem_3S_as][1] += (agents.belieftree[0][agents.select_problem_3S_as][1] - links.agent2.belieftree[0][agents.select_problem_3S_as][1]) * \
									agents.resources[0] * resources_weight_action * links.aware * resources_potency
								# print('After: ' + str(links.agent2.belieftree[0][agents.select_problem_3S_as][1]))
								# 1-1 check
								links.agent2.belieftree[0][agents.select_problem_3S_as][1] = \
									self.one_minus_one_check2(links.agent2.belieftree[0][agents.select_problem_3S_as][1])
								# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acting agent)
								agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][1] = links.agent2.belieftree[0][agents.select_problem_3S_as][1]
								# 1-1 check
								agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][1] = \
									self.one_minus_one_check2(agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][1])
								# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acted upon agent)
								links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][1] = agents.belieftree[0][agents.select_problem_3S_as][1] + (random.random()/5) - 0.1
								# 1-1 check
								links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][1] = \
									self.one_minus_one_check2(links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][1])

								# print(' ')
								# print('Aim change')
								# print(agents.belieftree[1 + links.agent2.unique_id])

							if links.agent2 == agents:

								# print('Before: ' + str(links.agent1.belieftree[0][agents.select_problem_3S_as][1]))
								links.agent1.belieftree[0][agents.select_problem_3S_as][1] += (agents.belieftree[0][agents.select_problem_3S_as][1] - links.agent1.belieftree[0][agents.select_problem_3S_as][1]) * \
									agents.resources[0] * resources_weight_action * links.aware * resources_potency
								# print('After: ' + str(links.agent1.belieftree[0][agents.select_problem_3S_as][1]))
								# 1-1 check
								links.agent1.belieftree[0][agents.select_problem_3S_as][1] = \
									self.one_minus_one_check2(links.agent1.belieftree[0][agents.select_problem_3S_as][1])
								# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acting agent)
								agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][1] = links.agent2.belieftree[0][agents.select_problem_3S_as][1]
								# 1-1 check
								agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][1] = \
									self.one_minus_one_check2(agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][1])
								# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acted upon agent)
								links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][1] = agents.belieftree[0][agents.select_problem_3S_as][1] + (random.random()/5) - 0.1
								# 1-1 check
								links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][1] = \
									self.one_minus_one_check2(links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][1])


						# If the index is in the first part of the list, then the state influence action is the best
						if best_action == len(cw_of_interest) + 1:
							# print(' ')
							# print('Performing an aim change action')
							# print('best_action: ' + str(best_action))

							if links.agent1 == agents:
								# print('Before: ' + str(links.agent2.belieftree[0][len(self.deep_core) + agents.select_problem][0]))
								links.agent2.belieftree[0][agents.select_problem_3S_as][0] += (agents.belieftree[0][agents.select_problem_3S_as][0] - links.agent2.belieftree[0][agents.select_problem_3S_as][0]) * \
									agents.resources[0] * resources_weight_action * links.aware * resources_potency
								# print('After: ' + str(links.agent2.belieftree[0][len(self.deep_core) + agents.select_problem][0]))
								links.agent2.belieftree[0][agents.select_problem_3S_as][0] = \
									self.one_minus_one_check2(links.agent2.belieftree[0][agents.select_problem_3S_as][0])
								# Providing partial knowledge - State problem - 0.2 range from real value: (Acting agent)
								agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][0] = links.agent2.belieftree[0][agents.select_problem_3S_as][0] + (random.random()/5) - 0.1
								# 1-1 check
								agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][0] = \
									self.one_minus_one_check2(agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][0])
								# Providing partial knowledge - State problem - 0.2 range from real value: (Acted upon agent)
								links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][0] = agents.belieftree[0][agents.select_problem_3S_as][0] + (random.random()/5) - 0.1
								# 1-1 check
								links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][0] = \
									self.one_minus_one_check2(links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][0])

								# print(' ')
								# print('State change')
								# print(agents.belieftree[1 + links.agent2.unique_id])

							if links.agent2 == agents:
								# print('Before: ' + str(links.agent1.belieftree[0][len(self.deep_core) + agents.select_problem][0]))
								links.agent1.belieftree[0][agents.select_problem_3S_as][0] += (agents.belieftree[0][agents.select_problem_3S_as][0] - links.agent1.belieftree[0][agents.select_problem_3S_as][0]) * \
									agents.resources[0] * resources_weight_action * links.aware * resources_potency
								# print('After: ' + str(links.agent1.belieftree[0][len(self.deep_core) + agents.select_problem][0]))
								# 1-1 check
								links.agent1.belieftree[0][agents.select_problem_3S_as][0] = \
									self.one_minus_one_check2(links.agent1.belieftree[0][agents.select_problem_3S_as][0])
								# Providing partial knowledge - State problem - 0.2 range from real value: (Acting agent)
								agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][0] = links.agent1.belieftree[0][agents.select_problem_3S_as][0] + (random.random()/5) - 0.1
								# 1-1 check
								agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][0] = \
									self.one_minus_one_check2(agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][0])
								# Providing partial knowledge - State problem - 0.2 range from real value: (Acted upon agent)
								links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][0] = agents.belieftree[0][agents.select_problem_3S_as][0] + (random.random()/5) - 0.1
								# 1-1 check
								links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][0] = \
									self.one_minus_one_check2(links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][0])

								# print(' ')
								# print('State change')
								# print(agents.belieftree[1 + links.agent1.unique_id])

				# If the agent is advocating or a policy, the following tasks are performed
				if agents.select_issue_3S_as == 'policy':
					
					if (links.agent1 == agents and links.agent2.unique_id == agent_best_action) or (links.agent1.unique_id == agent_best_action and links.agent2 == agents):
						# print(links)

						# Updating the aware decay parameter
						links.aware_decay = 5

						# If the index is in the first part of the list, then the framing action is the best
						if best_action <= impact_number - 1:
							# print(' ')
							# print('Performing a causal relation framing action')
							# print('best_action: ' + str(best_action))
							# print('impact_number: ' + str(impact_number))

							if links.agent1 == agents:
								
								# print('Before: ' + str(links.agent2.belieftree_policy[0][agents.select_policy_3S_as][best_action]))
								links.agent2.belieftree_policy[0][agents.select_policy_3S_as][best_action] += (agents.belieftree[0][agents.select_policy_3S_as][best_action] - \
									links.agent2.belieftree_policy[0][agents.select_policy_3S_as][best_action]) * \
									agents.resources[0] * resources_weight_action * links.aware * resources_potency
								# print('After: ' + str(links.agent2.belieftree_policy[0][agents.select_policy_3S_as][best_action]))
								# 1-1 check
								links.agent2.belieftree_policy[0][agents.select_policy_3S_as][best_action] = \
									self.one_minus_one_check2(links.agent2.belieftree_policy[0][agents.select_policy_3S_as][best_action])
								# Providing partial knowledge - Framing - 0.2 range from real value: (Acting agent)
								agents.belieftree_policy[1 + links.agent2.unique_id][agents.select_policy_3S_as][best_action] = links.agent2.belieftree_policy[0][agents.select_policy_3S_as][best_action] + (random.random()/5) - 0.1
								# 1-1 check
								agents.belieftree_policy[1 + links.agent2.unique_id][agents.select_policy_3S_as][best_action] = \
									self.one_minus_one_check2(agents.belieftree_policy[1 + links.agent2.unique_id][agents.select_policy_3S_as][best_action])
								# Providing partial knowledge - Framing - 0.2 range from real value: (Acted upon agent)
								links.agent2.belieftree_policy[1 + agents.unique_id][agents.select_policy_3S_as][best_action] = agents.belieftree_policy[0][agents.select_policy_3S_as][best_action] + (random.random()/5) - 0.1
								# 1-1 check
								links.agent2.belieftree_policy[1 + agents.unique_id][agents.select_policy_3S_as][best_action] = \
									self.one_minus_one_check2(links.agent2.belieftree_policy[1 + agents.unique_id][agents.select_policy_3S_as][best_action])

								# print(' ')
								# print('Causal change')
								# print(agents.belieftree_policy[1 + links.agent2.unique_id])
								# print(agents.belieftree_policy[1 + links.agent2.unique_id][agents.select_policy_3S_as][best_action])

							# Checking which agent in the link is the original agent
							if links.agent2 == agents:

								# print('Before: ' + str(links.agent1.belieftree_policy[0][agents.select_policy_3S_as][best_action]))
								links.agent1.belieftree_policy[0][agents.select_policy_3S_as][best_action] += (agents.belieftree_policy[0][agents.select_policy_3S_as][best_action] - \
									links.agent1.belieftree_policy[0][agents.select_policy_3S_as][best_action]) * \
									agents.resources[0] * resources_weight_action * links.aware * resources_potency
								# print('After: ' + str(links.agent1.belieftree_policy[0][agents.select_policy_3S_as][best_action]))
								# 1-1 check
								links.agent1.belieftree_policy[0][agents.select_policy_3S_as][best_action] = \
									self.one_minus_one_check2(links.agent1.belieftree_policy[0][agents.select_policy_3S_as][best_action])
								# Providing partial knowledge - Framing - 0.2 range from real value: (Acting agent)
								agents.belieftree_policy[1 + links.agent1.unique_id][agents.select_policy_3S_as][best_action] = links.agent1.belieftree_policy[0][agents.select_policy_3S_as][best_action] + (random.random()/5) - 0.1
								# 1-1 check
								agents.belieftree_policy[1 + links.agent1.unique_id][agents.select_policy_3S_as][best_action] = \
									self.one_minus_one_check2(agents.belieftree_policy[1 + links.agent1.unique_id][agents.select_policy_3S_as][best_action])
								# Providing partial knowledge - Framing - 0.2 range from real value: (Acted upon agent)
								links.agent1.belieftree_policy[1 + agents.unique_id][agents.select_policy_3S_as][best_action] = agents.belieftree_policy[0][agents.select_policy_3S_as][best_action] + (random.random()/5) - 0.1
								# 1-1 check
								links.agent1.belieftree_policy[1 + agents.unique_id][agents.select_policy_3S_as][best_action] = \
									self.one_minus_one_check2(links.agent1.belieftree_policy[1 + agents.unique_id][agents.select_policy_3S_as][best_action])

								# print(' ')
								# print('Causal change')
								# print(agents.belieftree_policy[1 + links.agent1.unique_id])
								# print(agents.belieftree_policy[1 + links.agent1.unique_id][agents.select_policy_3S_as][best_action])

						# If the index is in the second part of the list, then the aim influence action is the best
						if best_action == impact_number:
							# print(' ')
							# print('Performing a state change action')
							# print('best_action: ' + str(best_action))

							if links.agent1 == agents:
								# print('Before: ' + str(links.agent2.belieftree[0][agents.select_problem_3S_as][1]))
								links.agent2.belieftree[0][agents.select_problem_3S_as][1] += (agents.belieftree[0][agents.select_problem_3S_as][1] - links.agent2.belieftree[0][agents.select_problem_3S_as][1]) * \
									agents.resources[0] * resources_weight_action * links.aware * resources_potency
								# print('After: ' + str(links.agent2.belieftree[0][agents.select_problem_3S_as][1]))
								# 1-1 check
								links.agent2.belieftree[0][agents.select_problem_3S_as][1] = \
									self.one_minus_one_check2(links.agent2.belieftree[0][agents.select_problem_3S_as][1])
								# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acting agent)
								agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][1] = links.agent2.belieftree[0][agents.select_problem_3S_as][1]
								# 1-1 check
								agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][1] = \
									self.one_minus_one_check2(agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][1])
								# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acted upon agent)
								links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][1] = agents.belieftree[0][agents.select_problem_3S_as][1] + (random.random()/5) - 0.1
								# 1-1 check
								links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][1] = \
									self.one_minus_one_check2(links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][1])

								# print(' ')
								# print('Aim change')
								# print(agents.belieftree[1 + links.agent2.unique_id])

							if links.agent2 == agents:

								# print('Before: ' + str(links.agent1.belieftree[0][agents.select_problem_3S_as][1]))
								links.agent1.belieftree[0][agents.select_problem_3S_as][1] += (agents.belieftree[0][agents.select_problem_3S_as][1] - links.agent1.belieftree[0][agents.select_problem_3S_as][1]) * \
									agents.resources[0] * resources_weight_action * links.aware * resources_potency
								# print('After: ' + str(links.agent1.belieftree[0][agents.select_problem_3S_as][1]))
								# 1-1 check
								links.agent1.belieftree[0][agents.select_problem_3S_as][1] = \
									self.one_minus_one_check2(links.agent1.belieftree[0][agents.select_problem_3S_as][1])
								# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acting agent)
								agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][1] = links.agent2.belieftree[0][agents.select_problem_3S_as][1]
								# 1-1 check
								agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][1] = \
									self.one_minus_one_check2(agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][1])
								# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acted upon agent)
								links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][1] = agents.belieftree[0][agents.select_problem_3S_as][1] + (random.random()/5) - 0.1
								# 1-1 check
								links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][1] = \
									self.one_minus_one_check2(links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][1])


						# If the index is in the first part of the list, then the state influence action is the best
						if best_action == impact_number + 1:
							# print(' ')
							# print('Performing an aim change action')
							# print('best_action: ' + str(best_action))

							if links.agent1 == agents:
								# print('Before: ' + str(links.agent2.belieftree[0][len(self.deep_core) + agents.select_problem][0]))
								links.agent2.belieftree[0][agents.select_problem_3S_as][0] += (agents.belieftree[0][agents.select_problem_3S_as][0] - links.agent2.belieftree[0][agents.select_problem_3S_as][0]) * \
									agents.resources[0] * resources_weight_action * links.aware * resources_potency
								# print('After: ' + str(links.agent2.belieftree[0][len(self.deep_core) + agents.select_problem][0]))
								links.agent2.belieftree[0][agents.select_problem_3S_as][0] = \
									self.one_minus_one_check2(links.agent2.belieftree[0][agents.select_problem_3S_as][0])
								# Providing partial knowledge - State problem - 0.2 range from real value: (Acting agent)
								agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][0] = links.agent2.belieftree[0][agents.select_problem_3S_as][0] + (random.random()/5) - 0.1
								# 1-1 check
								agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][0] = \
									self.one_minus_one_check2(agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][0])
								# Providing partial knowledge - State problem - 0.2 range from real value: (Acted upon agent)
								links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][0] = agents.belieftree[0][agents.select_problem_3S_as][0] + (random.random()/5) - 0.1
								# 1-1 check
								links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][0] = \
									self.one_minus_one_check2(links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][0])

								# print(' ')
								# print('State change')
								# print(agents.belieftree[1 + links.agent2.unique_id])

							if links.agent2 == agents:
								# print('Before: ' + str(links.agent1.belieftree[0][len(self.deep_core) + agents.select_problem][0]))
								links.agent1.belieftree[0][agents.select_problem_3S_as][0] += (agents.belieftree[0][agents.select_problem_3S_as][0] - links.agent1.belieftree[0][agents.select_problem_3S_as][0]) * \
									agents.resources[0] * resources_weight_action * links.aware * resources_potency
								# print('After: ' + str(links.agent1.belieftree[0][len(self.deep_core) + agents.select_problem][0]))
								# 1-1 check
								links.agent1.belieftree[0][agents.select_problem_3S_as][0] = \
									self.one_minus_one_check2(links.agent1.belieftree[0][agents.select_problem_3S_as][0])
								# Providing partial knowledge - State problem - 0.2 range from real value: (Acting agent)
								agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][0] = links.agent1.belieftree[0][agents.select_problem_3S_as][0] + (random.random()/5) - 0.1
								# 1-1 check
								agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][0] = \
									self.one_minus_one_check2(agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][0])
								# Providing partial knowledge - State problem - 0.2 range from real value: (Acted upon agent)
								links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][0] = agents.belieftree[0][agents.select_problem_3S_as][0] + (random.random()/5) - 0.1
								# 1-1 check
								links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][0] = \
									self.one_minus_one_check2(links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][0])

								# print(' ')
								# print('State change')
								# print(agents.belieftree[1 + links.agent1.unique_id])


			# agents.resources_actions -= agents.resources
			agents.resources_actions -= agents.resources[0] * resources_weight_action

	def pm_pe_actions_pf_3S(self, agents, link_list, deep_core, policy_core, secondary, resources_weight_action, resources_potency, agenda_prob_3S_as):

		len_DC = len(deep_core)
		len_PC = len(policy_core)
		len_S = len(secondary)

		# Selection of the cw of interest
		cw_of_interest = []
		# Select one by one the DC
		j = agenda_prob_3S_as
		# for j in range(len_PC):
		# Selecting the causal relations starting from DC
		for k in range(len_S):
			# Contingency for partial knowledge issues
			# print(len_DC + len_PC + len_S + len_PC*len_DC + (j-len_DC) + k*len_PC)
			if (agents.belieftree[0][len_DC + len_PC + len_S + len_PC*len_DC + (j-len_DC) + k*len_PC][0] < 0 and (agents.belieftree[0][j][1] - agents.belieftree[0][j][0]) < 0) \
			  or (agents.belieftree[0][len_DC + len_PC + len_S + len_PC*len_DC + (j-len_DC) + k*len_PC][0] > 0 and (agents.belieftree[0][j][1] - agents.belieftree[0][j][0]) > 0):
				cw_of_interest.append(len_DC + len_PC + len_S + len_PC*len_DC + (j-len_DC) + k*len_PC)

		# Selection of the impact of interest
		impact_number = len(agents.belieftree_instrument[0][agents.select_policy_3S_pf])

		# print(' ')
		# print('Causal relations of interest: ' + str(cw_of_interest))

		# Making sure there are enough resources
		while agents.resources_actions > 0.001:

			# Going through all the links in the model
			# print(agents)
			total_grade_list = []
			total_grade_list_links = []
			for links in link_list:

				# Making sure that the link is attached to the agent and has a aware higher than 0
				if (links.agent1 == agents or links.agent2 == agents) and links.aware > 0:
					total_grade_list_links.append(links)

					# Definition the action weight parameter
					if type(links.agent1) == Policymakers or type(links.agent2) == Policymakers:
						actionWeight = 1
					else:
						actionWeight = 0.95
					
					# 1. Framing on causal relation and policy impacts

					# If the agent is advocating or a problem, the following tasks are performed
					if agents.select_issue_3S_pf == 'problem':
						# 1.a. Grading all framing actions on causal relations:
						# Checking through all possible framing - This is all based on partial knowledge!
						for cw in range(len(cw_of_interest)):

							# Checking which agent in the link is the original agent
							if links.agent1 == agents:
								# Check if no partial knowledge (initial value)
								check_none = 0
								if agents.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0] == None:
									agents.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0] = 0
									check_none = 1
								# Performing the action
								cw_grade = (agents.belieftree[0][cw_of_interest[cw]][0] - agents.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0]) * \
									agents.resources[0] * resources_weight_action * links.aware * resources_potency
								# Adding the grade to the grade list
								total_grade_list.append(cw_grade)
								#  Reset to None after finding the grade
								if check_none == 1:
									agents.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0] = None

							# Checking which agent in the link is the original agent
							if links.agent2 == agents:
								#  Check if no partial knowledge (initial value)
								check_none = 0
								if agents.belieftree[1 + links.agent1.unique_id][cw_of_interest[cw]][0] == None:
									agents.belieftree[1 + links.agent1.unique_id][cw_of_interest[cw]][0] = 0
									check_none = 1
								# Performing the action
								cw_grade = (agents.belieftree[0][cw_of_interest[cw]][0] - agents.belieftree[1 + links.agent1.unique_id][cw_of_interest[cw]][0]) * \
									agents.resources[0] * resources_weight_action * links.aware * resources_potency
								# Adding the grade to the grade list
								total_grade_list.append(cw_grade)
								# Reset to None after finding the grade
								if check_none == 1:
									agents.belieftree[1 + links.agent1.unique_id][cw_of_interest[cw]][0] = None

					# If the agent is advocating or a policy, the following tasks are performed
					if agents.select_issue_3S_pf == 'policy':
						# 1.b. Grading all framing actions on policy impacts:
						
						# Checking through all possible framing - This is all based on partial knowledge!
						for impact in range(impact_number):

							# Checking which agent in the link is the original agent
							if links.agent1 == agents:
								# Check if no partial knowledge (initial value)
								check_none = 0
								if agents.belieftree_instrument[1 + links.agent2.unique_id][agents.select_policy_3S_pf][impact] == None:
									agents.belieftree_instrument[1 + links.agent2.unique_id][agents.select_policy_3S_pf][impact] = 0
									check_none = 1
								# Performing the action
								impact_grade = (agents.belieftree_instrument[0][agents.select_policy_3S_pf][impact] - agents.belieftree_instrument[1 + links.agent2.unique_id][agents.select_policy_3S_pf][impact]) * \
									agents.resources[0] * resources_weight_action * links.aware * resources_potency
								# Adding the grade to the grade list
								total_grade_list.append(impact_grade)
								#  Reset to None after finding the grade
								if check_none == 1:
									agents.belieftree_instrument[1 + links.agent2.unique_id][agents.select_policy_3S_pf][impact] = None

							# Checking which agent in the link is the original agent
							if links.agent2 == agents:
								#  Check if no partial knowledge (initial value)
								check_none = 0
								if agents.belieftree_instrument[1 + links.agent1.unique_id][agents.select_policy_3S_pf][impact] == None:
									agents.belieftree_instrument[1 + links.agent1.unique_id][agents.select_policy_3S_pf][impact] = 0
									check_none = 1
								impact_grade = (agents.belieftree_instrument[0][agents.select_policy_3S_pf][impact] - agents.belieftree_instrument[1 + links.agent1.unique_id][agents.select_policy_3S_pf][impact]) * \
									agents.resources[0] * resources_weight_action * links.aware * resources_potency
								# Adding the grade to the grade list
								total_grade_list.append(impact_grade)
								# Reset to None after finding the grade
								if check_none == 1:
									agents.belieftree_instrument[1 + links.agent1.unique_id][agents.select_policy_3S_pf][impact] = None

					# 2. Grading all individual actions - Aim change
					if links.agent1 == agents:
						# Check if no partial knowledge (initial value)
						check_none = 0
						if agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][1] == None:
							agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][1] = 0
							check_none = 1
						# Performing the action
						aim_grade_issue = (agents.belieftree[0][agents.select_problem_3S_pf][1] - agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][1]) * \
							agents.resources[0] * resources_weight_action * links.aware * links.conflict_level[0][agents.select_problem_3S_pf][1] * actionWeight * resources_potency
						#  Reset to None after finding the grade
						if check_none == 1:
							agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][1] = None
						# Adding the grade to the grade list
						total_grade_list.append(aim_grade_issue)

					if links.agent2 == agents:
						# Check if no partial knowledge (initial value)
						check_none = 0
						if agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][1] == None:
							agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][1] = 0
							check_none = 1
						# Performing the action
						aim_grade_issue = (agents.belieftree[0][agents.select_problem_3S_pf][1] - agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][1]) * \
							agents.resources[0] * resources_weight_action * links.aware * links.conflict_level[1][agents.select_problem_3S_pf][1] * actionWeight * resources_potency
						#  Reset to None after finding the grade
						if check_none == 1:
							agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][1] = None
						# Adding the grade to the grade list
						total_grade_list.append(aim_grade_issue)

					# 3. Grading all individual actions - State change
					if links.agent1 == agents:
						# Check if no partial knowledge (initial value)
						check_none = 0
						if agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][0] == None:
							agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][0] = 0
							check_none = 1
						# Performing the action
						state_grade_issue = (agents.belieftree[0][agents.select_problem_3S_pf][0] - agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][0]) * \
							agents.resources[0] * resources_weight_action * links.aware * links.conflict_level[0][agents.select_problem_3S_pf][0] * actionWeight * resources_potency
						#  Reset to None after finding the grade
						if check_none == 1:
							agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][0] = None
						# Adding the grade to the grade list
						total_grade_list.append(state_grade_issue)

					if links.agent2 == agents:
						# Check if no partial knowledge (initial value)
						check_none = 0
						if agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][0] == None:
							agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][0] = 0
							check_none = 1
						# Performing the action
						state_grade_issue = (agents.belieftree[0][agents.select_problem_3S_pf][0] - agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][0]) * \
							agents.resources[0] * resources_weight_action * links.aware * links.conflict_level[1][agents.select_problem_3S_pf][0] * actionWeight * resources_potency
						#  Reset to None after finding the grade
						if check_none == 1:
							agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][0] = None
						# Adding the grade to the grade list
						total_grade_list.append(state_grade_issue)
					# print(' ')


			# 4. Choosing an action

			# If the agent is advocating or a problem, the following tasks are performed
			if agents.select_issue_3S_as == 'problem':

				best_action_index = total_grade_list.index(max(total_grade_list))
				agent_best_action = int(best_action_index/(len(cw_of_interest) + 1 + 1))
				best_action = best_action_index - (agent_best_action)*(len(cw_of_interest) + 1 + 1)

				# print(' ')
				# print('----- Considering new action grading (problem) -----')
				# print('best_action_index: ' + str(best_action_index))
				# print('Number of actions per agent: ' + str(len(cw_of_interest) + 1 + 1))
				# print('Total number of agents being influenced: ' + str(len(total_grade_list_links)))
				# print('Action to be performed: ' + str(best_action))
				# print('Agent performing the action: ' + str(agent_best_action))

			# If the agent is advocating or a policy, the following tasks are performed
			if agents.select_issue_3S_as == 'policy':
				
				best_action_index = total_grade_list.index(max(total_grade_list))
				agent_best_action = int(best_action_index/(impact_number + 1 + 1))
				best_action = best_action_index - (agent_best_action)*(impact_number + 1 + 1)

				# print(' ')
				# print('----- Considering new action grading (policy) -----')
				# print('best_action_index: ' + str(best_action_index))
				# print('Number of actions per agent: ' + str(impact_number + 1 + 1))
				# print('Total number of agents being influenced: ' + str(len(total_grade_list_links)))
				# print('Action to be performed: ' + str(best_action))
				# print('Agent performing the action: ' + str(agent_best_action))

			# 5. Performing the actual action
			# Selecting the link:
			for links in link_list:

				# If the agent is advocating or a problem, the following tasks are performed
				if agents.select_issue_3S_pf == 'problem':

					if (links.agent1 == agents and links.agent2.unique_id == agent_best_action) or (links.agent1.unique_id == agent_best_action and links.agent2 == agents):
						# print(links)

						# Updating the aware decay parameter
						links.aware_decay = 5

						# If the index is in the first part of the list, then the framing action is the best
						if best_action <= len(cw_of_interest) - 1:
							# print(' ')
							# print('Performing a causal relation framing action')
							# print('best_action: ' + str(best_action))
							# print('cw_of_interest: ' + str(cw_of_interest))
							# print('cw_of_interest[best_action]: ' + str(cw_of_interest[best_action]))
							
							# To simplify the notations
							best_action = cw_of_interest[best_action]

							if links.agent1 == agents:
								
								# print('Before: ' + str(links.agent2.belieftree[0][best_action][0]))
								links.agent2.belieftree[0][best_action][0] += (agents.belieftree[0][best_action][0] - links.agent2.belieftree[0][best_action][0]) * \
									agents.resources[0] * resources_weight_action * links.aware * resources_potency
								# print('After: ' + str(links.agent2.belieftree[0][best_action][0]))
								# 1-1 check
								links.agent2.belieftree[0][best_action][0] = \
									self.one_minus_one_check2(links.agent2.belieftree[0][best_action][0])
								# Providing partial knowledge - Framing - 0.2 range from real value: (Acting agent)
								agents.belieftree[1 + links.agent2.unique_id][best_action][0] = links.agent2.belieftree[0][best_action][0] + (random.random()/5) - 0.1
								# 1-1 check
								agents.belieftree[1 + links.agent2.unique_id][best_action][0] = \
									self.one_minus_one_check2(agents.belieftree[1 + links.agent2.unique_id][best_action][0])
								# Providing partial knowledge - Framing - 0.2 range from real value: (Acted upon agent)
								links.agent2.belieftree[1 + agents.unique_id][best_action][0] = agents.belieftree[0][best_action][0] + (random.random()/5) - 0.1
								# 1-1 check
								links.agent2.belieftree[1 + agents.unique_id][best_action][0] = \
									self.one_minus_one_check2(links.agent2.belieftree[1 + agents.unique_id][best_action][0])

								# print(' ')
								# print('Causal change')
								# print(agents.belieftree[1 + links.agent2.unique_id])
								# print(agents.belieftree[1 + links.agent2.unique_id][best_action][0])

							# Checking which agent in the link is the original agent
							if links.agent2 == agents:
								# print('Before: ' + str(links.agent1.belieftree[0][best_action][0]))
								links.agent1.belieftree[0][best_action][0] += (agents.belieftree[0][best_action][0] - links.agent1.belieftree[0][best_action][0]) * \
									agents.resources[0] * resources_weight_action * links.aware * resources_potency
								# print('After: ' + str(links.agent1.belieftree[0][best_action][0]))
								# 1-1 check
								links.agent1.belieftree[0][best_action][0] = \
									self.one_minus_one_check2(links.agent1.belieftree[0][best_action][0])
								# Providing partial knowledge - Framing - 0.2 range from real value: (Acting agent)
								agents.belieftree[1 + links.agent1.unique_id][best_action][0] = links.agent1.belieftree[0][best_action][0] + (random.random()/5) - 0.1
								# 1-1 check
								agents.belieftree[1 + links.agent1.unique_id][best_action][0] = \
									self.one_minus_one_check2(agents.belieftree[1 + links.agent1.unique_id][best_action][0])
								# Providing partial knowledge - Framing - 0.2 range from real value: (Acted upon agent)
								links.agent1.belieftree[1 + agents.unique_id][best_action][0] = agents.belieftree[0][best_action][0] + (random.random()/5) - 0.1
								# 1-1 check
								links.agent1.belieftree[1 + agents.unique_id][best_action][0] = \
									self.one_minus_one_check2(links.agent1.belieftree[1 + agents.unique_id][best_action][0])

								# print(' ')
								# print('Causal change')
								# print(agents.belieftree[1 + links.agent1.unique_id])
								# print(agents.belieftree[1 + links.agent1.unique_id][best_action][0])

						# If the index is in the second part of the list, then the aim influence action is the best
						if best_action == len(cw_of_interest):
							# print(' ')
							# print('Performing a state change action')
							# print('best_action: ' + str(best_action))

							if links.agent1 == agents:
								# print('Before: ' + str(links.agent2.belieftree[0][agents.select_problem_3S_pf][1]))
								links.agent2.belieftree[0][agents.select_problem_3S_pf][1] += (agents.belieftree[0][agents.select_problem_3S_pf][1] - links.agent2.belieftree[0][agents.select_problem_3S_pf][1]) * \
									agents.resources[0] * resources_weight_action * links.aware * resources_potency
								# print('After: ' + str(links.agent2.belieftree[0][agents.select_problem_3S_pf][1]))
								# 1-1 check
								links.agent2.belieftree[0][agents.select_problem_3S_pf][1] = \
									self.one_minus_one_check2(links.agent2.belieftree[0][agents.select_problem_3S_pf][1])
								# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acting agent)
								agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][1] = links.agent2.belieftree[0][agents.select_problem_3S_pf][1]
								# 1-1 check
								agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][1] = \
									self.one_minus_one_check2(agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][1])
								# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acted upon agent)
								links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][1] = agents.belieftree[0][agents.select_problem_3S_pf][1] + (random.random()/5) - 0.1
								# 1-1 check
								links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][1] = \
									self.one_minus_one_check2(links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][1])

								# print(' ')
								# print('Aim change')
								# print(agents.belieftree[1 + links.agent2.unique_id])

							if links.agent2 == agents:
								# print('Before: ' + str(links.agent1.belieftree[0][agents.select_problem_3S_pf][1]))
								links.agent1.belieftree[0][agents.select_problem_3S_pf][1] += (agents.belieftree[0][agents.select_problem_3S_pf][1] - links.agent1.belieftree[0][agents.select_problem_3S_pf][1]) * \
									agents.resources[0] * resources_weight_action * links.aware * resources_potency
								# print('After: ' + str(links.agent1.belieftree[0][agents.select_problem_3S_pf][1]))
								# 1-1 check
								links.agent1.belieftree[0][agents.select_problem_3S_pf][1] = \
									self.one_minus_one_check2(links.agent1.belieftree[0][agents.select_problem_3S_pf][1])
								# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acting agent)
								agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][1] = links.agent2.belieftree[0][agents.select_problem_3S_pf][1]
								# 1-1 check
								agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][1] = \
									self.one_minus_one_check2(agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][1])
								# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acted upon agent)
								links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][1] = agents.belieftree[0][agents.select_problem_3S_pf][1] + (random.random()/5) - 0.1
								# 1-1 check
								links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][1] = \
									self.one_minus_one_check2(links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][1])


						# If the index is in the first part of the list, then the state influence action is the best
						if best_action == len(cw_of_interest) + 1:
							# print(' ')
							# print('Performing an aim change action')
							# print('best_action: ' + str(best_action))

							if links.agent1 == agents:
								# print('Before: ' + str(links.agent2.belieftree[0][len(self.deep_core) + agents.select_problem][0]))
								links.agent2.belieftree[0][agents.select_problem_3S_pf][0] += (agents.belieftree[0][agents.select_problem_3S_pf][0] - links.agent2.belieftree[0][agents.select_problem_3S_pf][0]) * \
									agents.resources[0] * resources_weight_action * links.aware * resources_potency
								# print('After: ' + str(links.agent2.belieftree[0][len(self.deep_core) + agents.select_problem][0]))
								links.agent2.belieftree[0][agents.select_problem_3S_pf][0] = \
									self.one_minus_one_check2(links.agent2.belieftree[0][agents.select_problem_3S_pf][0])
								# Providing partial knowledge - State problem - 0.2 range from real value: (Acting agent)
								agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][0] = links.agent2.belieftree[0][agents.select_problem_3S_pf][0] + (random.random()/5) - 0.1
								# 1-1 check
								agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][0] = \
									self.one_minus_one_check2(agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][0])
								# Providing partial knowledge - State problem - 0.2 range from real value: (Acted upon agent)
								links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][0] = agents.belieftree[0][agents.select_problem_3S_pf][0] + (random.random()/5) - 0.1
								# 1-1 check
								links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][0] = \
									self.one_minus_one_check2(links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][0])

								# print(' ')
								# print('State change')
								# print(agents.belieftree[1 + links.agent2.unique_id])

							if links.agent2 == agents:
								# print('Before: ' + str(links.agent1.belieftree[0][len(self.deep_core) + agents.select_problem][0]))
								links.agent1.belieftree[0][agents.select_problem_3S_pf][0] += (agents.belieftree[0][agents.select_problem_3S_pf][0] - links.agent1.belieftree[0][agents.select_problem_3S_pf][0]) * \
									agents.resources[0] * resources_weight_action * links.aware * resources_potency
								# print('After: ' + str(links.agent1.belieftree[0][len(self.deep_core) + agents.select_problem][0]))
								# 1-1 check
								links.agent1.belieftree[0][agents.select_problem_3S_pf][0] = \
									self.one_minus_one_check2(links.agent1.belieftree[0][agents.select_problem_3S_pf][0])
								# Providing partial knowledge - State problem - 0.2 range from real value: (Acting agent)
								agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][0] = links.agent1.belieftree[0][agents.select_problem_3S_pf][0] + (random.random()/5) - 0.1
								# 1-1 check
								agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][0] = \
									self.one_minus_one_check2(agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][0])
								# Providing partial knowledge - State problem - 0.2 range from real value: (Acted upon agent)
								links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][0] = agents.belieftree[0][agents.select_problem_3S_pf][0] + (random.random()/5) - 0.1
								# 1-1 check
								links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][0] = \
									self.one_minus_one_check2(links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][0])

								# print(' ')
								# print('State change')
								# print(agents.belieftree[1 + links.agent1.unique_id])

				# If the agent is advocating or a policy, the following tasks are performed
				if agents.select_issue_3S_pf == 'policy':
					
					if (links.agent1 == agents and links.agent2.unique_id == agent_best_action) or (links.agent1.unique_id == agent_best_action and links.agent2 == agents):
						# print(links)

						# Updating the aware decay parameter
						links.aware_decay = 5

						# If the index is in the first part of the list, then the framing action is the best
						if best_action <= impact_number - 1:
							# print(' ')
							# print('Performing a causal relation framing action')
							# print('best_action: ' + str(best_action))
							# print('impact_number: ' + str(impact_number))

							if links.agent1 == agents:
								
								# print('Before: ' + str(links.agent2.belieftree_instrument[0][agents.select_policy_3S_pf][best_action]))
								links.agent2.belieftree_instrument[0][agents.select_policy_3S_pf][best_action] += (agents.belieftree_instrument[0][agents.select_policy_3S_pf][best_action] - \
									links.agent2.belieftree_instrument[0][agents.select_policy_3S_pf][best_action]) * \
									agents.resources[0] * resources_weight_action * links.aware * resources_potency
								# print('After: ' + str(links.agent2.belieftree_instrument[0][agents.select_policy_3S_pf][best_action]))
								# 1-1 check
								links.agent2.belieftree_instrument[0][agents.select_policy_3S_pf][best_action] = \
									self.one_minus_one_check2(links.agent2.belieftree_instrument[0][agents.select_policy_3S_pf][best_action])
								# Providing partial knowledge - Framing - 0.2 range from real value: (Acting agent)
								agents.belieftree_instrument[1 + links.agent2.unique_id][agents.select_policy_3S_pf][best_action] = links.agent2.belieftree_instrument[0][agents.select_policy_3S_pf][best_action] + (random.random()/5) - 0.1
								# 1-1 check
								agents.belieftree_instrument[1 + links.agent2.unique_id][agents.select_policy_3S_pf][best_action] = \
									self.one_minus_one_check2(agents.belieftree_instrument[1 + links.agent2.unique_id][agents.select_policy_3S_pf][best_action])
								# Providing partial knowledge - Framing - 0.2 range from real value: (Acted upon agent)
								links.agent2.belieftree_instrument[1 + agents.unique_id][agents.select_policy_3S_pf][best_action] = agents.belieftree_instrument[0][agents.select_policy_3S_pf][best_action] + (random.random()/5) - 0.1
								# 1-1 check
								links.agent2.belieftree_instrument[1 + agents.unique_id][agents.select_policy_3S_pf][best_action] = \
									self.one_minus_one_check2(links.agent2.belieftree_instrument[1 + agents.unique_id][agents.select_policy_3S_pf][best_action])

								# print(' ')
								# print('Causal change')
								# print(agents.belieftree_instrument[1 + links.agent2.unique_id])
								# print(agents.belieftree_instrument[1 + links.agent2.unique_id][agents.select_policy_3S_pf][best_action])

							# Checking which agent in the link is the original agent
							if links.agent2 == agents:

								# print('Before: ' + str(links.agent1.belieftree_instrument[0][agents.select_policy_3S_pf][best_action]))
								links.agent1.belieftree_instrument[0][agents.select_policy_3S_pf][best_action] += (agents.belieftree_instrument[0][agents.select_policy_3S_pf][best_action] - \
									links.agent1.belieftree_instrument[0][agents.select_policy_3S_pf][best_action]) * \
									agents.resources[0] * resources_weight_action * links.aware * resources_potency
								# print('After: ' + str(links.agent1.belieftree_instrument[0][agents.select_policy_3S_pf][best_action]))
								# 1-1 check
								links.agent1.belieftree_instrument[0][agents.select_policy_3S_pf][best_action] = \
									self.one_minus_one_check2(links.agent1.belieftree_instrument[0][agents.select_policy_3S_pf][best_action])
								# Providing partial knowledge - Framing - 0.2 range from real value: (Acting agent)
								agents.belieftree_instrument[1 + links.agent1.unique_id][agents.select_policy_3S_pf][best_action] = links.agent1.belieftree_instrument[0][agents.select_policy_3S_pf][best_action] + (random.random()/5) - 0.1
								# 1-1 check
								agents.belieftree_instrument[1 + links.agent1.unique_id][agents.select_policy_3S_pf][best_action] = \
									self.one_minus_one_check2(agents.belieftree_instrument[1 + links.agent1.unique_id][agents.select_policy_3S_pf][best_action])
								# Providing partial knowledge - Framing - 0.2 range from real value: (Acted upon agent)
								links.agent1.belieftree_instrument[1 + agents.unique_id][agents.select_policy_3S_pf][best_action] = agents.belieftree_instrument[0][agents.select_policy_3S_pf][best_action] + (random.random()/5) - 0.1
								# 1-1 check
								links.agent1.belieftree_instrument[1 + agents.unique_id][agents.select_policy_3S_pf][best_action] = \
									self.one_minus_one_check2(links.agent1.belieftree_instrument[1 + agents.unique_id][agents.select_policy_3S_pf][best_action])

								# print(' ')
								# print('Causal change')
								# print(agents.belieftree_instrument[1 + links.agent1.unique_id])
								# print(agents.belieftree_instrument[1 + links.agent1.unique_id][agents.select_policy_3S_pf][best_action])

						# If the index is in the second part of the list, then the aim influence action is the best
						if best_action == impact_number:
							# print(' ')
							# print('Performing a state change action')
							# print('best_action: ' + str(best_action))

							if links.agent1 == agents:
								# print('Before: ' + str(links.agent2.belieftree[0][agents.select_problem_3S_pf][1]))
								links.agent2.belieftree[0][agents.select_problem_3S_pf][1] += (agents.belieftree[0][agents.select_problem_3S_pf][1] - links.agent2.belieftree[0][agents.select_problem_3S_pf][1]) * \
									agents.resources[0] * resources_weight_action * links.aware * resources_potency
								# print('After: ' + str(links.agent2.belieftree[0][agents.select_problem_3S_pf][1]))
								# 1-1 check
								links.agent2.belieftree[0][agents.select_problem_3S_pf][1] = \
									self.one_minus_one_check2(links.agent2.belieftree[0][agents.select_problem_3S_pf][1])
								# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acting agent)
								agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][1] = links.agent2.belieftree[0][agents.select_problem_3S_pf][1]
								# 1-1 check
								agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][1] = \
									self.one_minus_one_check2(agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][1])
								# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acted upon agent)
								links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][1] = agents.belieftree[0][agents.select_problem_3S_pf][1] + (random.random()/5) - 0.1
								# 1-1 check
								links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][1] = \
									self.one_minus_one_check2(links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][1])

								# print(' ')
								# print('Aim change')
								# print(agents.belieftree[1 + links.agent2.unique_id])

							if links.agent2 == agents:

								# print('Before: ' + str(links.agent1.belieftree[0][agents.select_problem_3S_pf][1]))
								links.agent1.belieftree[0][agents.select_problem_3S_pf][1] += (agents.belieftree[0][agents.select_problem_3S_pf][1] - links.agent1.belieftree[0][agents.select_problem_3S_pf][1]) * \
									agents.resources[0] * resources_weight_action * links.aware * resources_potency
								# print('After: ' + str(links.agent1.belieftree[0][agents.select_problem_3S_pf][1]))
								# 1-1 check
								links.agent1.belieftree[0][agents.select_problem_3S_pf][1] = \
									self.one_minus_one_check2(links.agent1.belieftree[0][agents.select_problem_3S_pf][1])
								# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acting agent)
								agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][1] = links.agent2.belieftree[0][agents.select_problem_3S_pf][1]
								# 1-1 check
								agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][1] = \
									self.one_minus_one_check2(agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][1])
								# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acted upon agent)
								links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][1] = agents.belieftree[0][agents.select_problem_3S_pf][1] + (random.random()/5) - 0.1
								# 1-1 check
								links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][1] = \
									self.one_minus_one_check2(links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][1])


						# If the index is in the first part of the list, then the state influence action is the best
						if best_action == impact_number + 1:
							# print(' ')
							# print('Performing an aim change action')
							# print('best_action: ' + str(best_action))

							if links.agent1 == agents:
								# print('Before: ' + str(links.agent2.belieftree[0][len(self.deep_core) + agents.select_problem][0]))
								links.agent2.belieftree[0][agents.select_problem_3S_pf][0] += (agents.belieftree[0][agents.select_problem_3S_pf][0] - links.agent2.belieftree[0][agents.select_problem_3S_pf][0]) * \
									agents.resources[0] * resources_weight_action * links.aware * resources_potency
								# print('After: ' + str(links.agent2.belieftree[0][len(self.deep_core) + agents.select_problem][0]))
								links.agent2.belieftree[0][agents.select_problem_3S_pf][0] = \
									self.one_minus_one_check2(links.agent2.belieftree[0][agents.select_problem_3S_pf][0])
								# Providing partial knowledge - State problem - 0.2 range from real value: (Acting agent)
								agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][0] = links.agent2.belieftree[0][agents.select_problem_3S_pf][0] + (random.random()/5) - 0.1
								# 1-1 check
								agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][0] = \
									self.one_minus_one_check2(agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][0])
								# Providing partial knowledge - State problem - 0.2 range from real value: (Acted upon agent)
								links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][0] = agents.belieftree[0][agents.select_problem_3S_pf][0] + (random.random()/5) - 0.1
								# 1-1 check
								links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][0] = \
									self.one_minus_one_check2(links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][0])

								# print(' ')
								# print('State change')
								# print(agents.belieftree[1 + links.agent2.unique_id])

							if links.agent2 == agents:
								# print('Before: ' + str(links.agent1.belieftree[0][len(self.deep_core) + agents.select_problem][0]))
								links.agent1.belieftree[0][agents.select_problem_3S_pf][0] += (agents.belieftree[0][agents.select_problem_3S_pf][0] - links.agent1.belieftree[0][agents.select_problem_3S_pf][0]) * \
									agents.resources[0] * resources_weight_action * links.aware * resources_potency
								# print('After: ' + str(links.agent1.belieftree[0][len(self.deep_core) + agents.select_problem][0]))
								# 1-1 check
								links.agent1.belieftree[0][agents.select_problem_3S_pf][0] = \
									self.one_minus_one_check2(links.agent1.belieftree[0][agents.select_problem_3S_pf][0])
								# Providing partial knowledge - State problem - 0.2 range from real value: (Acting agent)
								agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][0] = links.agent1.belieftree[0][agents.select_problem_3S_pf][0] + (random.random()/5) - 0.1
								# 1-1 check
								agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][0] = \
									self.one_minus_one_check2(agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][0])
								# Providing partial knowledge - State problem - 0.2 range from real value: (Acted upon agent)
								links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][0] = agents.belieftree[0][agents.select_problem_3S_pf][0] + (random.random()/5) - 0.1
								# 1-1 check
								links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][0] = \
									self.one_minus_one_check2(links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][0])

								# print(' ')
								# print('State change')
								# print(agents.belieftree[1 + links.agent1.unique_id])



			# agents.resources_actions -= agents.resources
			agents.resources_actions -= agents.resources[0] * resources_weight_action

	def preference_udapte_as_PC(self, agent, who, len_DC, len_PC, len_S):

		# Preference calculation for the policy core issues
		PC_denominator = 0
		# Select one by one the DC
		for j in range(len_PC):
			PC_denominator = 0
			# Selecting the causal relations starting from DC
			for k in range(len_DC):
				# Contingency for partial knowledge issues
				if agent.belieftree[who][k][1] == None or agent.belieftree[who][k][0] == None or agent.belieftree[who][len_DC+len_PC+len_S+j+(k*len_PC)][0] == None:
					PC_denominator = 0
				else:
					# Check if causal relation and gap are both positive of both negative
					if (agent.belieftree[who][len_DC+len_PC+len_S+j+(k*len_PC)][0] < 0 and (agent.belieftree[who][k][1] - agent.belieftree[who][k][0]) < 0) \
					  or (agent.belieftree[who][len_DC+len_PC+len_S+j+(k*len_PC)][0] > 0 and (agent.belieftree[who][k][1] - agent.belieftree[who][k][0]) > 0):
						PC_denominator = PC_denominator + abs(agent.belieftree[who][len_DC+len_PC+len_S+j+(k*len_PC)][0]*\
						  (agent.belieftree[who][k][1] - agent.belieftree[who][k][0]))
					else:
						PC_denominator = PC_denominator	
		# Then adding the gap of the policy core:
		for i in range(len_PC):
			# Contingency for partial knowledge issues
			if agent.belieftree[who][len_DC + i][1] == None or agent.belieftree[who][len_DC + i][0] == None:
				PC_denominator = PC_denominator
			else:
				PC_denominator = PC_denominator + abs(agent.belieftree[who][len_DC + i][1] - agent.belieftree[who][len_DC + i][0])
		
		# Calculating the numerator and the preference of all policy core issues:
		# Select one by one the DC
		for j in range(len_PC):
			PC_numerator = 0
			# Selecting the causal relations starting from DC
			for k in range(len_DC):
				# Contingency for partial knowledge issues
				if agent.belieftree[who][k][1] == None or agent.belieftree[who][k][0] == None or agent.belieftree[who][len_DC+len_PC+len_S+j+(k*len_PC)][0] == None:
					PC_numerator = 0
				else:
					# Check if causal relation and gap are both positive of both negative
					if (agent.belieftree[who][len_DC+len_PC+len_S+j+(k*len_PC)][0] < 0 and (agent.belieftree[who][k][1] - agent.belieftree[who][k][0]) < 0) \
					  or (agent.belieftree[who][len_DC+len_PC+len_S+j+(k*len_PC)][0] > 0 and (agent.belieftree[who][k][1] - agent.belieftree[who][k][0]) > 0):
						PC_numerator = PC_numerator + abs(agent.belieftree[who][len_DC+len_PC+len_S+j+(k*len_PC)][0]*\
						  (agent.belieftree[who][k][1] - agent.belieftree[who][k][0]))
					else:
						PC_numerator = PC_numerator	
			# Contingency for partial knowledge issues
			if agent.belieftree[who][len_DC + j][1] == None or agent.belieftree[who][len_DC + j][0] == None:
				PC_numerator = 0
			else:
				# Then adding the gap of the policy core:
				PC_numerator = PC_numerator + abs(agent.belieftree[who][len_DC + j][1] - agent.belieftree[who][len_DC + j][0])
			if PC_denominator != 0:
				agent.belieftree[who][len_DC+j][2] = PC_numerator/PC_denominator 
			else:
				agent.belieftree[who][len_DC+j][2] = 0

	def preference_udapte_pf_PC(self, agent, who, len_DC, len_PC, len_S, agenda_prob_3S_as):

		k = agenda_prob_3S_as

		# Calculating the numerator and the preference of all policy core issues:
		# Select one by one the DC
		S_denominator = 0
		for j in range(len_S):
			# print('Selection S' + str(j+1))
			# print('State of the S' + str(j+1) + ': ' + str(agent.belieftree[0][len_DC + j][0])) # the state printed
			# Selecting the causal relations starting from PC
			# print(' ')
			# print(len_DC + len_PC + len_S + len_DC*len_PC + j*len_PC + (k-len_DC))
			# Contingency for partial knowledge issues
			if agent.belieftree[0][k][1] != None and agent.belieftree[0][k][0] != None and agent.belieftree[0][len_DC + len_PC + len_S + len_DC*len_PC + j*len_PC + (k-len_DC)][0] != None:
				# print('Causal Relation S' + str(j+1) + ' - PC' + str(k+1) + ': ' + str(agent.belieftree[0][len_DC+len_PC+len_S+(j+(k*len_PC))][0]))
				# print('Gap of PC' + str(k+1) + ': ' + str(agent.belieftree[0][k][1] - agent.belieftree[0][k][0]))
				# Check if causal relation and gap are both positive of both negative
				if (agent.belieftree[0][len_DC + len_PC + len_S + len_DC*len_PC + j*len_PC + (k-len_DC)][0] < 0 and (agent.belieftree[0][k][1] - agent.belieftree[0][k][0]) < 0) \
					or (agent.belieftree[0][len_DC + len_PC + len_S + len_DC*len_PC + j*len_PC + (k-len_DC)][0] > 0 and (agent.belieftree[0][k][1] - agent.belieftree[0][k][0]) > 0):
					# print('Calculating')
					S_denominator = S_denominator + abs(agent.belieftree[0][len_DC + len_PC + len_S + len_DC*len_PC + j*len_PC + (k-len_DC)][0] * \
						(agent.belieftree[0][k][1] - agent.belieftree[0][k][0]))
					# print('This is the PC numerator: ' + str(S_denominator))
				else:
					S_denominator = S_denominator
			else:
				S_denominator = 0
			# Contingency for partial knowledge issues
			if agent.belieftree[0][len_DC + len_PC + j][1] == None or agent.belieftree[0][len_DC + len_PC + j][0] == None:
				S_denominator = S_denominator
			else:
				# Then adding the gap of the policy core:
				# print('This is the gap for the S' + str(j+1) + ': ' + str(agent.belieftree[0][len_DC + len_PC + j][1] - agent.belieftree[0][len_DC + len_PC + j][0]))
				S_denominator = S_denominator + abs(agent.belieftree[0][len_DC + len_PC + j][1] - agent.belieftree[0][len_DC + len_PC + j][0])


		# Calculating the numerator and the preference of all policy core issues:
		# Select one by one the DC
		for j in range(len_S):
			S_numerator = 0
			# Contingency for partial knowledge issues
			if agent.belieftree[0][k][1] != None and agent.belieftree[0][k][0] != None and agent.belieftree[0][len_DC + len_PC + len_S + len_DC*len_PC + j*len_PC + (k-len_DC)][0] != None:
				# Check if causal relation and gap are both positive of both negative
				if (agent.belieftree[0][len_DC + len_PC + len_S + len_DC*len_PC + j*len_PC + (k-len_DC)][0] < 0 and (agent.belieftree[0][k][1] - agent.belieftree[0][k][0]) < 0) \
					or (agent.belieftree[0][len_DC + len_PC + len_S + len_DC*len_PC + j*len_PC + (k-len_DC)][0] > 0 and (agent.belieftree[0][k][1] - agent.belieftree[0][k][0]) > 0):
					# print('Calculating')
					S_numerator = S_numerator + abs(agent.belieftree[0][len_DC + len_PC + len_S + len_DC*len_PC + j*len_PC + (k-len_DC)][0] * \
						(agent.belieftree[0][k][1] - agent.belieftree[0][k][0]))
					# print('This is the PC numerator: ' + str(S_numerator))
				else:
					S_numerator = S_numerator
			else:
				S_numerator = 0
			# Contingency for partial knowledge issues
			if agent.belieftree[0][len_DC + len_PC + j][1] == None or agent.belieftree[0][len_DC + len_PC + j][0] == None:
				S_numerator = 0
			else:
				# Then adding the gap of the policy core:
				S_numerator = S_numerator + abs(agent.belieftree[0][len_DC + len_PC + j][1] - agent.belieftree[0][len_DC + len_PC + j][0])
			if S_denominator != 0:
				agent.belieftree[who][len_DC + len_PC + j][2] = S_numerator/S_denominator 
			else:
				agent.belieftree[who][len_DC + len_PC + j][2] = 0

	def instrument_preference_update(self, agent, who, AS_theory, len_DC, len_PC, len_S, instruments):

		# print(' ')
		# print('Triggered for who in: ' + str(who))
		# print(' ')

		"""
		Instrument preference update function
		===========================

		This function is used to calculate the ranking of each of the instrument from 
		which the agents can choose from. This is done in two parts.

		1/ The first part consists of calculating the preference level for the different
		secondary issues (layer 3 in the belief tree). In this part, the preferences of
		the agents are updated similarly to the function where the preferences are calculated.
		The main difference is that this time, it is based on the agenda which means that
		only the secondary issues affecting the problem on the agenda are considered.

		2/ The second part consists of obtaining the grade for the policy instruments.
		This is calculated as shown in the formalisation with the equation given by:
		G = sum(impact * (Aim - State) * Preference_secondary)
		We make sure that the instruments impact are only taken into account if the
		impact is of the same sign as the gap between the state and the aim for the
		specific secondary issues. If this is not the case, the impact is not considered
		for that specific part of the instrument.

		Notes:
		1/ The secondary issues for which the agent is not interested (this applies to 
		the external parties only) are not taken into account in the calculation. They
		are marked as the 'No' values.

		"""

		######################################################################################################
		# 1/ Calculation of the preference level for the secondary issues based on the problem on the agenda #
		######################################################################################################

		S_denominator = 0
		if AS_theory != 2:
			j = agent.select_as_issue
		if AS_theory == 2:
			j = agent.select_problem_3S_as
		for k in range(len_S):
			if agent.belieftree[who][j][1] != None and agent.belieftree[who][j][0] != None and agent.belieftree[who][len_DC + len_PC + len_S + (len_DC*len_PC) + (j - len_DC)*len_S + k][0] != None:
				if (agent.belieftree[who][len_DC + len_PC + len_S + (len_DC*len_PC) + (j - len_DC)*len_S + k][0] < 0 and (agent.belieftree[who][j][1] - agent.belieftree[who][j][0]) < 0) \
					or (agent.belieftree[who][len_DC + len_PC + len_S + (len_DC*len_PC) + (j - len_DC)*len_S + k][0] > 0 and (agent.belieftree[who][j][1] - agent.belieftree[who][j][0]) > 0):
					S_denominator = S_denominator + abs(agent.belieftree[who][len_DC + len_PC + len_S + (len_DC*len_PC) + (j - len_DC)*len_S + k][0]*\
					  (agent.belieftree[who][j][1] - agent.belieftree[who][j][0]))
				else:
					S_denominator = S_denominator
			else:
				S_denominator = S_denominator

		for i in range(len_S):
			if agent.belieftree[who][len_DC + len_PC + i][0] != 'No':
				if agent.belieftree[who][len_DC + len_PC + i][1] != None and agent.belieftree[who][len_DC + len_PC + i][0] != None:
					S_denominator = S_denominator + abs(agent.belieftree[who][len_DC + len_PC + i][1] - agent.belieftree[who][len_DC + len_PC + i][0])
				else:
					S_denominator = 0

		S_numerator = 0
		
		for j in range(len_S):
			S_numerator = 0
			if AS_theory != 2:
				k = agent.select_as_issue
			if AS_theory == 2:
				k = agent.select_problem_3S_as
			if agent.belieftree[who][k][1] != None and agent.belieftree[who][k][0] != None and agent.belieftree[who][len_DC + len_PC + len_S + (len_DC*len_PC) + (k - len_DC)*len_S + j][0] != None:
				if (agent.belieftree[who][len_DC + len_PC + len_S + (len_DC*len_PC) + (k - len_DC)*len_S + j][0] < 0 and (agent.belieftree[who][k][1] - agent.belieftree[who][k][0]) < 0) \
					or (agent.belieftree[who][len_DC + len_PC + len_S + (len_DC*len_PC) + (k - len_DC)*len_S + j][0] > 0 and (agent.belieftree[who][k][1] - agent.belieftree[who][k][0]) > 0):
					S_numerator = S_numerator + abs(agent.belieftree[who][len_DC + len_PC + len_S + (len_DC*len_PC) + (k - len_DC)*len_S + j][0]*\
						  (agent.belieftree[who][k][1] - agent.belieftree[who][k][0]))
				else:
					S_numerator = S_numerator
			else:
				S_numerator = S_numerator
			if agent.belieftree[who][len_DC + len_PC + j][0] != 'No':
				if agent.belieftree[who][len_DC + len_PC + j][1] != None and agent.belieftree[who][len_DC + len_PC + j][0] != None:
					S_numerator = S_numerator + abs(agent.belieftree[who][len_DC + len_PC + j][1] - agent.belieftree[who][len_DC + len_PC + j][0])
				else:
					S_numerator = 0
			if S_denominator != 0:
				agent.belieftree[who][len_DC+len_PC+j][2] = S_numerator/S_denominator 
			else:
				agent.belieftree[who][len_DC+len_PC+j][2] = 0

		##################################################################################################
		# 2/ Calculation of the grade of each of the instruments based on impact on the secondary issues #
		##################################################################################################

		agent.instrument_preferences[who] = [0 for h in range(len(instruments))]
		for i in range(len(instruments)):
			for j in range(len_S):
				if agent.belieftree[who][len_DC + len_PC + j][0] != 'No':
					if agent.belieftree[who][len_DC + len_PC + j][1] != None and agent.belieftree[who][len_DC + len_PC + j][0] != None:
						if (instruments[i][j] > 0 and (agent.belieftree[who][len_DC + len_PC + j][1] - agent.belieftree[who][len_DC + len_PC + j][0]) > 0 ) \
							or (instruments[i][j] < 0 and (agent.belieftree[who][len_DC + len_PC + j][1] - agent.belieftree[who][len_DC + len_PC + j][0]) < 0 ):
							# print(' ')
							# print('agent.instrument_preferences[who][i]: ' + str(agent.instrument_preferences[who][i]))
							# print('instruments[i][j]: ' + str(instruments[i][j]))
							# print('agent.belieftree[' + str(who) + '][len_DC + len_PC + ' + str(j) + '][1]: ' + str(agent.belieftree[who][len_DC + len_PC + j][1]))
							# print('agent.belieftree[' + str(who) + '][len_DC + len_PC + ' + str(j) + '][0]: ' + str(agent.belieftree[who][len_DC + len_PC + j][0]))
							# print('agent.belieftree[' + str(who) + '][len_DC + len_PC + ' + str(j) + '][2]: ' + str(agent.belieftree[who][len_DC + len_PC + j][2]))
							agent.instrument_preferences[who][i] = agent.instrument_preferences[who][i] + \
								(instruments[i][j] * (agent.belieftree[who][len_DC + len_PC + j][1] - agent.belieftree[who][len_DC + len_PC + j][0]) * \
								(agent.belieftree[who][len_DC + len_PC + j][2]))
							# print('agent.instrument_preferences[who][i]: ' + str(agent.instrument_preferences[who][i]))
					else:
						agent.instrument_preferences[who][i] = 0

	def one_minus_one_check2(self, to_be_checked_parameter):

		checked_parameter = 0
		if to_be_checked_parameter > 1:
			checked_parameter = 1
		elif to_be_checked_parameter < -1:
			checked_parameter = -1
		else:
			checked_parameter = to_be_checked_parameter
		return checked_parameter








