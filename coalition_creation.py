import random
from network_creation import PolicyNetworkLinks
import copy

class Coalition():

	def __init__(self, unique_id, lead, members, members_id, issue, creation, resources):

		self.unique_id = unique_id
		self.lead = lead
		self.members = members
		self.members_id = members_id
		self.issue = issue
		self.creation = creation
		self.resources = resources


	def __str__(self):
		return 'Coalition - ' + str(self.unique_id) + ' created at tick: ' + str(self.creation) + ' and a total of: ' + str(len(self.members)) + ' members.'

	# def __str__(self):
	# 	return 'Coalition - ' + str(self.unique_id)

	def coalition_belief_actions_ACF_as(self, coalitions, causalrelation_number, deep_core, policy_core, secondary, agent_action_list, ACF_link_list_as, ACF_link_list_as_total, \
		ACF_link_id_as, link_list, affiliation_weights, conflict_level_coef):

		"""
		The coalition belief actions function (agenda setting)
		===========================

		This function is used to perform the actions of the coalitions
		in the agenda setting. The actions of the coalitions are the 
		same actions as the one of the individual agents. The main
		differences here are the amount of resources used and the fact
		that all actions are estimated and performed by the coalition
		leader based on the coalition leader's partial knowledge.

		"""

		len_DC = len(deep_core)
		len_PC = len(policy_core)
		len_S = len(secondary)

		# print(coalitions)

		# print('The belief actions now have to be performed for each team!')
		# Make sure that the coalition actually axists:
		if len(coalitions.members) > 0:

			# 0. Asssigning the resources
			coalitions.resources[1] = coalitions.resources[0]

			cw_of_interest = []
			# We only consider the causal relations related to the problem on the agenda
			for cw_choice in range(len(deep_core)):
					cw_of_interest.append(len_DC + len_PC + len_S + (coalitions.issue - len_DC) + cw_choice * len(policy_core))
			# print(' ')
			# print('cw_of_interest: ' + str(cw_of_interest))

			# 1. Intra-team actions (actions performed on agents inside the team)
			# This step is only performed if there is more than one team member in the coalition
			if len(coalitions.members) != 1 and len(cw_of_interest) > 0:

				# As long as there are enough resources (50% of the total)
				while True:
					# a. First exchange of information on all causal relations and the policy issue of the team
					#  Exchange of knowledge on the policy (state and aim)
					
					self.knowledge_exchange_coalition(coalitions, coalitions.issue, 0)
					self.knowledge_exchange_coalition(coalitions, coalitions.issue, 1)
					# Exchange of knowledge on the causal relations

					for cw in cw_of_interest:
						self.knowledge_exchange_coalition(coalitions, cw, 0)
					
					# b. Compiling all actions for each actor

					# This will need to be adjusted at a later point.
					actionWeight = 1

					#  We look at one causal relation at a time:
					# print(' ')
					# print(coalitions.lead)
					total_agent_grades = []
					for cw in range(len(cw_of_interest)):
						cw_grade_list = []
						# We then go through all agents
						for agent_inspected in coalitions.members:
							# Take the list of links
							for links in link_list:
								# Check that the list has an awareness level
								if links.aware != -1:
									# Check that only the link of interest is selected
									if links.agent1 == coalitions.lead and links.agent2 == agent_inspected or links.agent2 == coalitions.lead and links.agent1 == agent_inspected:
										# Make sure to look at the right direction of the conflict level
										if links.agent1 == coalitions.lead:
											
											# Grade calculation using the likelihood method
											# Same affiliation
											if links.agent1.affiliation == links.agent2.affiliation:
												cw_grade = links.conflict_level[0][cw_of_interest[cw]][0] * links.aware * actionWeight

											# Affiliation 1-2
											if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
												(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
												cw_grade = links.conflict_level[0][cw_of_interest[cw]][0] * links.aware * actionWeight * affiliation_weights[0]

											# Affiliation 1-3
											if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
												(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
												cw_grade = links.conflict_level[0][cw_of_interest[cw]][0] * links.aware * actionWeight * affiliation_weights[1]

											# Affiliation 2-3
											if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
												(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
												cw_grade = links.conflict_level[0][cw_of_interest[cw]][0] * links.aware * actionWeight * affiliation_weights[2]

											cw_grade_list.append(cw_grade)

										if links.agent2 == coalitions.lead:
											
											# Grade calculation using the likelihood method
											# Same affiliation
											if links.agent1.affiliation == links.agent2.affiliation:
												cw_grade = links.conflict_level[1][cw_of_interest[cw]][0] * links.aware * actionWeight

											# Affiliation 1-2
											if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
												(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
												cw_grade = links.conflict_level[1][cw_of_interest[cw]][0] * links.aware * actionWeight * affiliation_weights[0]

											# Affiliation 1-3
											if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
												(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
												cw_grade = links.conflict_level[1][cw_of_interest[cw]][0] * links.aware * actionWeight * affiliation_weights[1]

											# Affiliation 2-3
											if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
												(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
												cw_grade = links.conflict_level[1][cw_of_interest[cw]][0] * links.aware * actionWeight * affiliation_weights[2]
											
											cw_grade_list.append(cw_grade)

								# If the link has a negative awareness, set the grade of the action to 0
								else:
									# Check that only the link of interest is selected
									if links.agent1 == coalitions.lead and links.agent2 == agent_inspected or links.agent2 == coalitions.lead and links.agent1 == agent_inspected:
										cw_grade_list.append(0)

							# if coalitions.lead.affiliation == agent_inspected.affiliation:
							# 	cw_grade = abs((coalitions.lead.belieftree[0][cw_of_interest[cw]][0] - coalitions.lead.belieftree[1 + agent_inspected.unique_id][cw_of_interest[cw]][0]) * \
							# 		coalitions.resources[0] * 0.1 / (len(coalitions.members)))

							# if (coalitions.lead.affiliation == 0 and agent_inspected.affiliation == 1) or (coalitions.lead.affiliation == 1 and agent_inspected.affiliation == 0):
							# 	cw_grade = abs((coalitions.lead.belieftree[0][cw_of_interest[cw]][0] - coalitions.lead.belieftree[1 + agent_inspected.unique_id][cw_of_interest[cw]][0]) * \
							# 		coalitions.resources[0] * 0.1 * affiliation_weights[0] / (len(coalitions.members)))

							# if (coalitions.lead.affiliation == 0 and agent_inspected.affiliation == 2) or (coalitions.lead.affiliation == 2 and agent_inspected.affiliation == 0):
							# 	cw_grade = abs((coalitions.lead.belieftree[0][cw_of_interest[cw]][0] - coalitions.lead.belieftree[1 + agent_inspected.unique_id][cw_of_interest[cw]][0]) * \
							# 		coalitions.resources[0] * 0.1 * affiliation_weights[1] / (len(coalitions.members)))

							# if (coalitions.lead.affiliation == 1 and agent_inspected.affiliation == 2) or (coalitions.lead.affiliation == 2 and agent_inspected.affiliation == 1):
							# 	cw_grade = abs((coalitions.lead.belieftree[0][cw_of_interest[cw]][0] - coalitions.lead.belieftree[1 + agent_inspected.unique_id][cw_of_interest[cw]][0]) * \
							# 		coalitions.resources[0] * 0.1 * affiliation_weights[2] / (len(coalitions.members)))

							# cw_grade_list.append(cw_grade)
							
						total_agent_grades.append(sum(cw_grade_list))

						# print('CR: ' + str(cw) + ' with grade: ' + str(sum(cw_grade_list)))

					# We look at the state for the policy
					state_grade_list = []
					# We then go through all agents
					for agent_inspected in coalitions.members:
						# Take the list of links
						for links in link_list:
							# Check that the list has an awareness level
							if links.aware != -1:
								# Check that only the link of interest is selected
								if links.agent1 == coalitions.lead and links.agent2 == agent_inspected or links.agent2 == coalitions.lead and links.agent1 == agent_inspected:

									# Make sure to look at the right direction of the conflict level
									if links.agent1 == coalitions.lead:
									
										# Grade calculation using the likelihood method
										# Same affiliation
										if links.agent1.affiliation == links.agent2.affiliation:
											state_grade = links.conflict_level[0][coalitions.issue][0] * links.aware * actionWeight

										# Affiliation 1-2
										if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
											(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
											state_grade = links.conflict_level[0][coalitions.issue][0] * links.aware * actionWeight * affiliation_weights[0]

										# Affiliation 1-3
										if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
											(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
											state_grade = links.conflict_level[0][coalitions.issue][0] * links.aware * actionWeight * affiliation_weights[1]

										# Affiliation 2-3
										if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
											(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
											state_grade = links.conflict_level[0][coalitions.issue][0] * links.aware * actionWeight * affiliation_weights[2]

										state_grade_list.append(state_grade)

									if links.agent2 == coalitions.lead:
									
										# Grade calculation using the likelihood method
										# Same affiliation
										if links.agent1.affiliation == links.agent2.affiliation:
											state_grade = links.conflict_level[1][coalitions.issue][0] * links.aware * actionWeight

										# Affiliation 1-2
										if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
											(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
											state_grade = links.conflict_level[1][coalitions.issue][0] * links.aware * actionWeight * affiliation_weights[0]

										# Affiliation 1-3
										if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
											(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
											state_grade = links.conflict_level[1][coalitions.issue][0] * links.aware * actionWeight * affiliation_weights[1]

										# Affiliation 2-3
										if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
											(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
											state_grade = links.conflict_level[1][coalitions.issue][0] * links.aware * actionWeight * affiliation_weights[2]
									
										state_grade_list.append(state_grade)
							# If the link has a negative awareness, set the grade of the action to 0
							else:
								# Check that only the link of interest is selected
								if links.agent1 == coalitions.lead and links.agent2 == agent_inspected or links.agent2 == coalitions.lead and links.agent1 == agent_inspected:
									state_grade_list.append(0)



						# if coalitions.lead.affiliation == agent_inspected.affiliation:
						# 	state_grade = abs((coalitions.lead.belieftree[0][coalitions.issue][0] - \
						# 	  coalitions.lead.belieftree[1 + agent_inspected.unique_id][coalitions.issue][0]) * coalitions.resources[0] * 0.1 / (len(coalitions.members)))

						# if (coalitions.lead.affiliation == 0 and agent_inspected.affiliation == 1) or (coalitions.lead.affiliation == 1 and agent_inspected.affiliation == 0):
						# 	state_grade = abs((coalitions.lead.belieftree[0][coalitions.issue][0] - coalitions.lead.belieftree[1 + agent_inspected.unique_id][coalitions.issue][0]) \
	    	# 					* coalitions.resources[0] * 0.1 * affiliation_weights[0] / (len(coalitions.members)))

						# if (coalitions.lead.affiliation == 0 and agent_inspected.affiliation == 2) or (coalitions.lead.affiliation == 2 and agent_inspected.affiliation == 0):
						# 	state_grade = abs((coalitions.lead.belieftree[0][coalitions.issue][0] - coalitions.lead.belieftree[1 + agent_inspected.unique_id][coalitions.issue][0]) \
	    	# 					* coalitions.resources[0] * 0.1 * affiliation_weights[1] / (len(coalitions.members)))

						# if (coalitions.lead.affiliation == 1 and agent_inspected.affiliation == 2) or (coalitions.lead.affiliation == 2 and agent_inspected.affiliation == 1):
						# 	state_grade = abs((coalitions.lead.belieftree[0][coalitions.issue][0] - coalitions.lead.belieftree[1 + agent_inspected.unique_id][coalitions.issue][0]) \
	    	# 					* coalitions.resources[0] * 0.1 * affiliation_weights[2] / (len(coalitions.members)))

						# state_grade_list.append(state_grade)

					total_agent_grades.append(sum(state_grade_list))
					# print('State: ' + str(sum(state_grade_list)))
					
					# We look at the aim for the policy
					aim_grade_list = []
					# We then go through all agents
					for agent_inspected in coalitions.members:
						# Take the list of links
						for links in link_list:
							# Check that the list has an awareness level
							if links.aware != -1:
								# Check that only the link of interest is selected
								if links.agent1 == coalitions.lead and links.agent2 == agent_inspected or links.agent2 == coalitions.lead and links.agent1 == agent_inspected:

									# Make sure to look at the right direction of the conflict level
									if links.agent1 == coalitions.lead:
									
										# Grade calculation using the likelihood method
										# Same affiliation
										if links.agent1.affiliation == links.agent2.affiliation:
											aim_grade = links.conflict_level[0][coalitions.issue][1] * links.aware * actionWeight

										# Affiliation 1-2
										if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
											(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
											aim_grade = links.conflict_level[0][coalitions.issue][1] * links.aware * actionWeight * affiliation_weights[0]

										# Affiliation 1-3
										if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
											(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
											aim_grade = links.conflict_level[0][coalitions.issue][1] * links.aware * actionWeight * affiliation_weights[1]

										# Affiliation 2-3
										if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
											(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
											aim_grade = links.conflict_level[0][coalitions.issue][1] * links.aware * actionWeight * affiliation_weights[2]

										aim_grade_list.append(aim_grade)

									if links.agent1 == coalitions.lead:
									
										# Grade calculation using the likelihood method
										# Same affiliation
										if links.agent1.affiliation == links.agent2.affiliation:
											aim_grade = links.conflict_level[1][coalitions.issue][1] * links.aware * actionWeight

										# Affiliation 1-2
										if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
											(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
											aim_grade = links.conflict_level[1][coalitions.issue][1] * links.aware * actionWeight * affiliation_weights[0]

										# Affiliation 1-3
										if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
											(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
											aim_grade = links.conflict_level[1][coalitions.issue][1] * links.aware * actionWeight * affiliation_weights[1]

										# Affiliation 2-3
										if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
											(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
											aim_grade = links.conflict_level[1][coalitions.issue][1] * links.aware * actionWeight * affiliation_weights[2]
									
										aim_grade_list.append(aim_grade)
							# If the link has a negative awareness, set the grade of the action to 0
							else:
								# Check that only the link of interest is selected
								if links.agent1 == coalitions.lead and links.agent2 == agent_inspected or links.agent2 == coalitions.lead and links.agent1 == agent_inspected:
									aim_grade_list.append(0)

						# if coalitions.lead.affiliation == agent_inspected.affiliation:
						# 	aim_grade = abs((coalitions.lead.belieftree[0][coalitions.issue][1] - \
						# 	  coalitions.lead.belieftree[1 + agent_inspected.unique_id][coalitions.issue][1]) * coalitions.resources[0] * 0.1 / (len(coalitions.members)))

						# if (coalitions.lead.affiliation == 0 and agent_inspected.affiliation == 1) or (coalitions.lead.affiliation == 1 and agent_inspected.affiliation == 0):
						# 	aim_grade = abs((coalitions.lead.belieftree[0][coalitions.issue][1] - \
						# 	  coalitions.lead.belieftree[1 + agent_inspected.unique_id][coalitions.issue][1]) * coalitions.resources[0] * 0.1 * affiliation_weights[0] / (len(coalitions.members)))

						# if (coalitions.lead.affiliation == 0 and agent_inspected.affiliation == 2) or (coalitions.lead.affiliation == 2 and agent_inspected.affiliation == 0):
						# 	aim_grade = abs((coalitions.lead.belieftree[0][coalitions.issue][1] - \
						# 	  coalitions.lead.belieftree[1 + agent_inspected.unique_id][coalitions.issue][1]) * coalitions.resources[0] * 0.1 * affiliation_weights[1] / (len(coalitions.members)))

						# if (coalitions.lead.affiliation == 1 and agent_inspected.affiliation == 2) or (coalitions.lead.affiliation == 2 and agent_inspected.affiliation == 1):
						# 	aim_grade = abs((coalitions.lead.belieftree[0][coalitions.issue][1] - \
						# 	  coalitions.lead.belieftree[1 + agent_inspected.unique_id][coalitions.issue][1]) * coalitions.resources[0] * 0.1 * affiliation_weights[2] / (len(coalitions.members)))

						# aim_grade_list.append(aim_grade)

					total_agent_grades.append(sum(aim_grade_list))
					# print('Aim: ' + str(sum(aim_grade_list)))

					# c. Finding the best action
					best_action = total_agent_grades.index(max(total_agent_grades))

					# print(' ')
					# print('----- Considering new action grading -----')
					# print('Action to be performed: ' + str(best_action))


					# d. Implementation the best action

					# The causal relation action is performed
					if best_action <= len(cw_of_interest) - 1:
						# print(' ')
						# print('Performing a causal relation framing action')
						# print('best_action: ' + str(best_action))
						# print('cw_of_interest: ' + str(cw_of_interest))
						# print('cw_of_interest[best_action]: ' + str(cw_of_interest[best_action]))

						# It is the agent that has the best action that performs the action
						for agent_impacted in coalitions.members:

							if agent_impacted.affiliation == coalitions.lead.affiliation:
								agent_impacted.belieftree[0][cw_of_interest[best_action]][0] += \
									(coalitions.lead.belieftree[0][cw_of_interest[best_action]][0]) - agent_impacted.belieftree[0][cw_of_interest[best_action]][0] * \
									coalitions.resources[0] * 0.1 / len(coalitions.members)

							if (agent_impacted.affiliation == 0 and coalitions.lead.affiliation == 1) or (agent_impacted.affiliation == 1 and coalitions.lead.affiliation == 0):
								agent_impacted.belieftree[0][cw_of_interest[best_action]][0] += \
								  (coalitions.lead.belieftree[0][cw_of_interest[best_action]][0]) - agent_impacted.belieftree[0][cw_of_interest[best_action]][0] * \
								  coalitions.resources[0] * 0.1 * affiliation_weights[0] / len(coalitions.members)

							if (agent_impacted.affiliation == 0 and coalitions.lead.affiliation == 2) or (agent_impacted.affiliation == 2 and coalitions.lead.affiliation == 0):
								agent_impacted.belieftree[0][cw_of_interest[best_action]][0] += \
									(coalitions.lead.belieftree[0][cw_of_interest[best_action]][0]) - agent_impacted.belieftree[0][cw_of_interest[best_action]][0] * \
									coalitions.resources[0] * 0.1 * affiliation_weights[1] / len(coalitions.members)

							if (agent_impacted.affiliation == 1 and coalitions.lead.affiliation == 2) or (agent_impacted.affiliation == 2 and coalitions.lead.affiliation == 1):
								agent_impacted.belieftree[0][cw_of_interest[best_action]][0] += \
									(coalitions.lead.belieftree[0][cw_of_interest[best_action]][0]) - agent_impacted.belieftree[0][cw_of_interest[best_action]][0] * \
									coalitions.resources[0] * 0.1 * affiliation_weights[2] / len(coalitions.members)

							# 1-1 check
							agent_impacted.belieftree[0][cw_of_interest[best_action]][0] = self.one_minus_one_check(agent_impacted.belieftree[0][cw_of_interest[best_action]][0])
							
					# The state change is performed
					if best_action == len(cw_of_interest):
						# print(' ')
						# print('Performing a state change action')
						# print('best_action: ' + str(best_action))

						# It is the agent that has the best action that performs the action
						for agent_impacted in coalitions.members:

							if agent_impacted.affiliation == coalitions.lead.affiliation:
								agent_impacted.belieftree[0][coalitions.issue][0] += (coalitions.lead.belieftree[0][coalitions.issue][0] - \
								  agent_impacted.belieftree[0][coalitions.issue][0]) * coalitions.resources[0] * 0.1 / (len(coalitions.members))

							if (agent_impacted.affiliation == 0 and coalitions.lead.affiliation == 1) or (agent_impacted.affiliation == 1 and coalitions.lead.affiliation == 0):
								agent_impacted.belieftree[0][coalitions.issue][0] += (coalitions.lead.belieftree[0][coalitions.issue][0] - \
								  agent_impacted.belieftree[0][coalitions.issue][0]) * coalitions.resources[0] * 0.1 * affiliation_weights[0] / (len(coalitions.members))

							if (agent_impacted.affiliation == 0 and coalitions.lead.affiliation == 2) or (agent_impacted.affiliation == 2 and coalitions.lead.affiliation == 0):
								agent_impacted.belieftree[0][coalitions.issue][0] += (coalitions.lead.belieftree[0][coalitions.issue][0] - \
								  agent_impacted.belieftree[0][coalitions.issue][0]) * coalitions.resources[0] * 0.1 * affiliation_weights[1] / (len(coalitions.members))

							if (agent_impacted.affiliation == 1 and coalitions.lead.affiliation == 2) or (agent_impacted.affiliation == 2 and coalitions.lead.affiliation == 1):
								agent_impacted.belieftree[0][coalitions.issue][0] += (coalitions.lead.belieftree[0][coalitions.issue][0] - \
								  agent_impacted.belieftree[0][coalitions.issue][0]) * coalitions.resources[0] * 0.1 * affiliation_weights[2] / (len(coalitions.members))

							# 1-1 check
							agent_impacted.belieftree[0][coalitions.issue][0] = self.one_minus_one_check(agent_impacted.belieftree[0][coalitions.issue][0])

					# The aim change is performed
					if best_action == len(cw_of_interest) + 1:
						# print(' ')
						# print('Performing an aim change action')
						# print('best_action: ' + str(best_action))

						for agent_impacted in coalitions.members:

							if agent_impacted.affiliation == coalitions.lead.affiliation:
								agent_impacted.belieftree[0][coalitions.issue][1] += (coalitions.lead.belieftree[0][coalitions.issue][1] - \
								  agent_impacted.belieftree[0][coalitions.issue][1]) * coalitions.resources[0] * 0.1 / (len(coalitions.members))

							if (agent_impacted.affiliation == 0 and coalitions.lead.affiliation == 1) or (agent_impacted.affiliation == 1 and coalitions.lead.affiliation == 0):
								agent_impacted.belieftree[0][coalitions.issue][1] += (coalitions.lead.belieftree[0][coalitions.issue][1] - \
								  agent_impacted.belieftree[0][coalitions.issue][1]) * coalitions.resources[0] * 0.1 * affiliation_weights[0] / (len(coalitions.members))

							if (agent_impacted.affiliation == 0 and coalitions.lead.affiliation == 2) or (agent_impacted.affiliation == 2 and coalitions.lead.affiliation == 0):
								agent_impacted.belieftree[0][coalitions.issue][1] += (coalitions.lead.belieftree[0][coalitions.issue][1] - \
								  agent_impacted.belieftree[0][coalitions.issue][1]) * coalitions.resources[0] * 0.1 * affiliation_weights[1] / (len(coalitions.members))

							if (agent_impacted.affiliation == 1 and coalitions.lead.affiliation == 2) or (agent_impacted.affiliation == 2 and coalitions.lead.affiliation == 1):
								agent_impacted.belieftree[0][coalitions.issue][1] += (coalitions.lead.belieftree[0][coalitions.issue][1] - \
								  agent_impacted.belieftree[0][coalitions.issue][1]) * coalitions.resources[0] * 0.1 * affiliation_weights[2] / (len(coalitions.members))

							# 1-1 check
							agent_impacted.belieftree[0][coalitions.issue][1] = self.one_minus_one_check(agent_impacted.belieftree[0][coalitions.issue][1])
					
					# Updating the resources of the team
					coalitions.resources[1] -= coalitions.resources[0]*0.1

					# Resources check
					if coalitions.resources[1] <= 0.5 * coalitions.resources[0]:
						# print('RAN OUT OF RESOURCES!')
						break

			# 2. Inter-team actions (actions performed on agents outside the team)

			# Only perform this if not all agents are in the coalition
			if len(coalitions.members) < len(agent_action_list) and len(cw_of_interest) > 0:

				# Creation of the list of agents to be considered:
				inter_agent_list = []
				for potential_agent in agent_action_list:
					if potential_agent not in coalitions.members:
						inter_agent_list.append(potential_agent)
				# print(' ')
				# print('# of agents not in the team: ' + str(len(inter_agent_list)))

				# Creation of the shadow network for this coalition
				# print('We need to create a link network for this team!')
				for agent_network in inter_agent_list:
					# Do not take into account EP with no interest in that issue for the network
					if agent_network.belieftree[0][coalitions.issue][0] != 'No':
						# print(' ')
						# print('Added 1 - ' + str(agent_network))
						self.new_link_ACF_as(link_list, agent_network, coalitions, ACF_link_list_as, ACF_link_list_as_total, ACF_link_id_as, len_DC, len_PC, len_S, conflict_level_coef)

				# Performing the actions using the shadow network and the individual agents within the team

				# As long as there are enough resources (50% of the total)
				while True:

					# print('Performing inter-team actions')

					total_agent_grades = []
					# for agents_in_team in teams.members:
					# Going through all agents that are not part of the team
					link_count = 0
					for links in ACF_link_list_as:
						# Make sure to select an existing link
						if links.aware != -1:
							# Make sure to only select the links related to this team
							if coalitions == links.agent1:
								# print(links)
								link_count += 1
								# Setting the action weight
								# Removed for now for technical issues
								# if type(links.agent2) == Policymakers:
								# 		actionWeight = 1
								# else:
								# 	actionWeight = 0.95
								actionWeight = 1
								# Framing actions:
								for cw in range(len(cw_of_interest)):

									# Grade calculation using the likelihood method
									# Same affiliation
									if coalitions.lead.affiliation == links.agent2.affiliation:
										cw_grade = links.conflict_level[2 + cw_of_interest[cw] - (len_DC + len_PC + len_S)] * links.aware * actionWeight
										total_agent_grades.append(cw_grade)

									# Affiliation 1-2
									if (coalitions.lead.affiliation == 0 and links.agent2.affiliation == 1) or \
										(coalitions.lead.affiliation == 1 and links.agent2.affiliation == 0):
										cw_grade = links.conflict_level[2 + cw_of_interest[cw] - (len_DC + len_PC + len_S)] * links.aware * actionWeight * affiliation_weights[0]
										total_agent_grades.append(cw_grade)

									# Affiliation 1-3
									if (coalitions.lead.affiliation == 0 and links.agent2.affiliation == 2) or \
										(coalitions.lead.affiliation == 2 and links.agent2.affiliation == 0):
										cw_grade = links.conflict_level[2 + cw_of_interest[cw] - (len_DC + len_PC + len_S)] * links.aware * actionWeight * affiliation_weights[1]
										total_agent_grades.append(cw_grade)

									# Affiliation 2-3
									if (coalitions.lead.affiliation == 1 and links.agent2.affiliation == 2) or \
										(coalitions.lead.affiliation == 2 and links.agent2.affiliation == 1):
										cw_grade = links.conflict_level[2 + cw_of_interest[cw] - (len_DC + len_PC + len_S)] * links.aware * actionWeight * affiliation_weights[2]
										total_agent_grades.append(cw_grade)

									# OLD OLD OLD OLD OLD OLD 
									# check_none = 0
									# if coalitions.lead.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0] == None:
									# 	coalitions.lead.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0] = 0
									# 	check_none = 1
									# cw_grade = abs((coalitions.lead.belieftree[0][cw_of_interest[cw]][0] - \
									#   coalitions.lead.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0]) * \
									#   coalitions.resources[0] * 0.1 * links.aware * actionWeight)
									# total_agent_grades.append(cw_grade)
									# # None reset
									# if check_none == 1:
									# 	coalitions.lead.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0] = None
									
								# State influence actions
								# Grade calculation using the likelihood method
								# Same affiliation
								if coalitions.lead.affiliation == links.agent2.affiliation:
									state_grade = links.conflict_level[0] * links.aware * actionWeight
									total_agent_grades.append(state_grade)

								# Affiliation 1-2
								if (coalitions.lead.affiliation == 0 and links.agent2.affiliation == 1) or \
									(coalitions.lead.affiliation == 1 and links.agent2.affiliation == 0):
									state_grade = links.conflict_level[0] * links.aware * actionWeight * affiliation_weights[0]
									total_agent_grades.append(state_grade)

								# Affiliation 1-3
								if (coalitions.lead.affiliation == 0 and links.agent2.affiliation == 2) or \
									(coalitions.lead.affiliation == 2 and links.agent2.affiliation == 0):
									state_grade = links.conflict_level[0] * links.aware * actionWeight * affiliation_weights[1]
									total_agent_grades.append(state_grade)

								# Affiliation 2-3
								if (coalitions.lead.affiliation == 1 and links.agent2.affiliation == 2) or \
									(coalitions.lead.affiliation == 2 and links.agent2.affiliation == 1):
									state_grade = links.conflict_level[0] * links.aware * actionWeight * affiliation_weights[2]
									total_agent_grades.append(state_grade)

								# Aim influence actions
								# Grade calculation using the likelihood method
								# Same affiliation
								if coalitions.lead.affiliation == links.agent2.affiliation:
									aim_grade = links.conflict_level[1] * links.aware * actionWeight
									total_agent_grades.append(aim_grade)

								# Affiliation 1-2
								if (coalitions.lead.affiliation == 0 and links.agent2.affiliation == 1) or \
									(coalitions.lead.affiliation == 1 and links.agent2.affiliation == 0):
									aim_grade = links.conflict_level[1] * links.aware * actionWeight * affiliation_weights[0]
									total_agent_grades.append(aim_grade)

								# Affiliation 1-3
								if (coalitions.lead.affiliation == 0 and links.agent2.affiliation == 2) or \
									(coalitions.lead.affiliation == 2 and links.agent2.affiliation == 0):
									aim_grade = links.conflict_level[1] * links.aware * actionWeight * affiliation_weights[1]
									total_agent_grades.append(aim_grade)

								# Affiliation 2-3
								if (coalitions.lead.affiliation == 1 and links.agent2.affiliation == 2) or \
									(coalitions.lead.affiliation == 2 and links.agent2.affiliation == 1):
									aim_grade = links.conflict_level[1] * links.aware * actionWeight * affiliation_weights[2]
									total_agent_grades.append(aim_grade)


								# OLD OLD OLD OLD OLD OLD 
								# State influence actions
								# check_none = 0
								# if coalitions.lead.belieftree[1 + links.agent2.unique_id][coalitions.issue][0] == None:
								# 	coalitions.lead.belieftree[1 + links.agent2.unique_id][coalitions.issue][0] = 0
								# 	check_none = 1
								# state_grade = abs((coalitions.lead.belieftree[0][coalitions.issue][0] - \
								#   coalitions.lead.belieftree[1 + links.agent2.unique_id][coalitions.issue][0]) * coalitions.resources[0] * 0.1 * links.aware * links.conflict_level[0] * actionWeight)
								# total_agent_grades.append(state_grade)
								# # None reset
								# if check_none == 1:
								# 	coalitions.lead.belieftree[1 + links.agent2.unique_id][coalitions.issue][0] = None

								# # Aim influence actions
								# check_none = 0
								# if coalitions.lead.belieftree[1 + links.agent2.unique_id][coalitions.issue][1] == None:
								# 	coalitions.lead.belieftree[1 + links.agent2.unique_id][coalitions.issue][1] = 0
								# 	check_none = 1
								# aim_grade = abs((coalitions.lead.belieftree[0][coalitions.issue][1] - \
								#   coalitions.lead.belieftree[1 + links.agent2.unique_id][coalitions.issue][1]) * coalitions.resources[0] * 0.1 * links.aware * links.conflict_level[1] * actionWeight)
								# total_agent_grades.append(aim_grade)
								# # None reset
								# if check_none == 1:
								# 	coalitions.lead.belieftree[1 + links.agent2.unique_id][coalitions.issue][1] = None									

					# Choosing the best action
					best_action_index = total_agent_grades.index(max(total_agent_grades))
					best_action = best_action_index - int(best_action_index/(len(cw_of_interest) + 1 + 1))*(len(cw_of_interest) + 1 + 1)
					acted_upon_agent = int(best_action_index/(len(cw_of_interest) + 1 + 1))

					# print(' ')
					# print('----- Considering new action grading -----')
					# print('Original index: ' + str(best_action_index))
					# print('Number of actions that can be performed: ' + str(len(cw_of_interest) + 1 + 1))
					# print('Action to be performed: ' + str(best_action))
					# print('This is the agent on which the action is performed: ' + str(acted_upon_agent))

					# Actually performing the action:
					# Getting a list of the links related to this team
					list_links_coalitions = []
					for links in ACF_link_list_as:
							# Make sure to only select the links related to this team
							if coalitions == links.agent1:
								# Make sure to select an existing link
								if links.aware != -1:
									list_links_coalitions.append(links)

					# Implement framing action
					if best_action <= len(cw_of_interest) - 1:
						# print(' ')
						# print('Performing a causal relation framing action')
						# print('best_action: ' + str(best_action))
						# print('cw_of_interest: ' + str(cw_of_interest))
						# print('cw_of_interest[best_action]: ' + str(cw_of_interest[best_action]))

						# print('Before: ', list_links_coalitions[acted_upon_agent].agent2.belieftree[0][len(deep_core) + len(policy_core) + len(secondary) + best_action - 1][0])

						if coalitions.lead.affiliation == list_links_coalitions[acted_upon_agent].agent2.affiliation:
							list_links_coalitions[acted_upon_agent].agent2.belieftree[0][cw_of_interest[best_action]][0] += \
								(coalitions.lead.belieftree[0][cw_of_interest[best_action]][0] - list_links_coalitions[acted_upon_agent].agent2.belieftree[0][cw_of_interest[best_action]][0]) * \
								coalitions.resources[0] * 0.1

						# Affiliation 1-2
						if (coalitions.lead.affiliation == 0 and list_links_coalitions[acted_upon_agent].agent2.affiliation == 1) or \
							(coalitions.lead.affiliation == 1 and list_links_coalitions[acted_upon_agent].agent2.affiliation == 0):
							list_links_coalitions[acted_upon_agent].agent2.belieftree[0][cw_of_interest[best_action]][0] += \
								(coalitions.lead.belieftree[0][cw_of_interest[best_action]][0] - list_links_coalitions[acted_upon_agent].agent2.belieftree[0][cw_of_interest[best_action]][0]) * \
								coalitions.resources[0] * 0.1 * affiliation_weights[0]

						# Affiliation 1-3
						if (coalitions.lead.affiliation == 0 and list_links_coalitions[acted_upon_agent].agent2.affiliation == 2) or \
							(coalitions.lead.affiliation == 2 and list_links_coalitions[acted_upon_agent].agent2.affiliation == 0):
							list_links_coalitions[acted_upon_agent].agent2.belieftree[0][cw_of_interest[best_action]][0] += \
								(coalitions.lead.belieftree[0][cw_of_interest[best_action]][0] - list_links_coalitions[acted_upon_agent].agent2.belieftree[0][cw_of_interest[best_action]][0]) * \
								coalitions.resources[0] * 0.1 * affiliation_weights[1]

						# Affiliation 2-3
						if (coalitions.lead.affiliation == 1 and list_links_coalitions[acted_upon_agent].agent2.affiliation == 2) or \
							(coalitions.lead.affiliation == 2 and list_links_coalitions[acted_upon_agent].agent2.affiliation == 1):
							list_links_coalitions[acted_upon_agent].agent2.belieftree[0][cw_of_interest[best_action]][0] += \
								(coalitions.lead.belieftree[0][cw_of_interest[best_action]][0] - list_links_coalitions[acted_upon_agent].agent2.belieftree[0][cw_of_interest[best_action]][0]) * \
								coalitions.resources[0] * 0.1 * affiliation_weights[2]

						# print('After: ', list_links_coalitions[acted_upon_agent].agent2.belieftree[0][len(deep_core) + len(policy_core) + len(secondary) + best_action - 1][0])
						
						# Checks and transfer of partial knowledge
						# 1-1 check
						list_links_coalitions[acted_upon_agent].agent2.belieftree[0][cw_of_interest[best_action]][0] = \
							self.one_minus_one_check(list_links_coalitions[acted_upon_agent].agent2.belieftree[0][cw_of_interest[best_action]][0])
						# Exchange of knowledge - 0.2 - From acted upon to acting
						coalitions.lead.belieftree[1 + acted_upon_agent][cw_of_interest[best_action]][0] = \
						  list_links_coalitions[acted_upon_agent].agent2.belieftree[0][cw_of_interest[best_action]][0] + (random.random()/5) - 0.1
						# 1-1 check
						coalitions.lead.belieftree[1 + acted_upon_agent][cw_of_interest[best_action]][0] = \
							self.one_minus_one_check(coalitions.lead.belieftree[1 + acted_upon_agent][cw_of_interest[best_action]][0])
						# Exchange of knowledge - 0.2 - From acting to acted upon
						list_links_coalitions[acted_upon_agent].agent2.belieftree[1 + coalitions.lead.unique_id][cw_of_interest[best_action]][0] = \
						  coalitions.lead.belieftree[0][cw_of_interest[best_action]][0] + (random.random()/5) - 0.1
						# 1-1 check
						list_links_coalitions[acted_upon_agent].agent2.belieftree[1 + coalitions.lead.unique_id][cw_of_interest[best_action]][0] = \
							self.one_minus_one_check(list_links_coalitions[acted_upon_agent].agent2.belieftree[1 + coalitions.lead.unique_id][cw_of_interest[best_action]][0])

					# Implement state influence action
					if best_action == len(cw_of_interest):
						# print(' ')
						# print('Performing a state change action')
						# print('best_action: ' + str(best_action))

						if coalitions.lead.affiliation == list_links_coalitions[acted_upon_agent].agent2.affiliation:
							list_links_coalitions[acted_upon_agent].agent2.belieftree[0][coalitions.issue][0] += \
								(coalitions.lead.belieftree[0][coalitions.issue][0] - list_links_coalitions[acted_upon_agent].agent2.belieftree[0][coalitions.issue][0]) * \
								coalitions.resources[0] * 0.1

						# Affiliation 1-2
						if (coalitions.lead.affiliation == 0 and list_links_coalitions[acted_upon_agent].agent2.affiliation == 1) or \
							(coalitions.lead.affiliation == 1 and list_links_coalitions[acted_upon_agent].agent2.affiliation == 0):
							list_links_coalitions[acted_upon_agent].agent2.belieftree[0][coalitions.issue][0] += \
								(coalitions.lead.belieftree[0][coalitions.issue][0] - list_links_coalitions[acted_upon_agent].agent2.belieftree[0][coalitions.issue][0]) * \
								coalitions.resources[0] * 0.1 * affiliation_weights[0]

						# Affiliation 1-3
						if (coalitions.lead.affiliation == 0 and list_links_coalitions[acted_upon_agent].agent2.affiliation == 2) or \
							(coalitions.lead.affiliation == 2 and list_links_coalitions[acted_upon_agent].agent2.affiliation == 0):
							list_links_coalitions[acted_upon_agent].agent2.belieftree[0][coalitions.issue][0] += \
								(coalitions.lead.belieftree[0][coalitions.issue][0] - list_links_coalitions[acted_upon_agent].agent2.belieftree[0][coalitions.issue][0]) * \
								coalitions.resources[0] * 0.1 * affiliation_weights[1]

						# Affiliation 2-3
						if (coalitions.lead.affiliation == 1 and list_links_coalitions[acted_upon_agent].agent2.affiliation == 2) or \
							(coalitions.lead.affiliation == 2 and list_links_coalitions[acted_upon_agent].agent2.affiliation == 1):
							list_links_coalitions[acted_upon_agent].agent2.belieftree[0][coalitions.issue][0] += \
								(coalitions.lead.belieftree[0][coalitions.issue][0] - list_links_coalitions[acted_upon_agent].agent2.belieftree[0][coalitions.issue][0]) * \
								coalitions.resources[0] * 0.1 * affiliation_weights[2]
						
						# Checks and transfer of partial knowledge
						# 1-1 check
						list_links_coalitions[acted_upon_agent].agent2.belieftree[0][coalitions.issue][0] = \
							self.one_minus_one_check(list_links_coalitions[acted_upon_agent].agent2.belieftree[0][coalitions.issue][0])
						# Exchange of knowledge - 0.2 - From acted upon to acting
						coalitions.lead.belieftree[1 + acted_upon_agent][coalitions.issue][0] = \
						  list_links_coalitions[acted_upon_agent].agent2.belieftree[0][coalitions.issue][0] + (random.random()/5) - 0.1
						# 1-1 check
						coalitions.lead.belieftree[1 + acted_upon_agent][coalitions.issue][0] = \
							self.one_minus_one_check(coalitions.lead.belieftree[1 + acted_upon_agent][coalitions.issue][0])
						# Exchange of knowledge - 0.2 - From acting to acted upon
						list_links_coalitions[acted_upon_agent].agent2.belieftree[1 + coalitions.lead.unique_id][coalitions.issue][0] = \
						  coalitions.lead.belieftree[0][coalitions.issue][0] + (random.random()/5) - 0.1
						# 1-1 check
						list_links_coalitions[acted_upon_agent].agent2.belieftree[1 + coalitions.lead.unique_id][coalitions.issue][0] = \
							self.one_minus_one_check(list_links_coalitions[acted_upon_agent].agent2.belieftree[1 + coalitions.lead.unique_id][coalitions.issue][0])

					# Implement aim influence action
					if best_action == len(cw_of_interest) + 1:
						# print(' ')
						# print('Performing an aim change action')
						# print('best_action: ' + str(best_action))


						if coalitions.lead.affiliation == list_links_coalitions[acted_upon_agent].agent2.affiliation:
							list_links_coalitions[acted_upon_agent].agent2.belieftree[0][coalitions.issue][1] += \
								(coalitions.lead.belieftree[0][coalitions.issue][1] - list_links_coalitions[acted_upon_agent].agent2.belieftree[0][coalitions.issue][1]) * \
								coalitions.resources[0] * 0.1

						# Affiliation 1-2
						if (coalitions.lead.affiliation == 0 and list_links_coalitions[acted_upon_agent].agent2.affiliation == 1) or \
							(coalitions.lead.affiliation == 1 and list_links_coalitions[acted_upon_agent].agent2.affiliation == 0):
							list_links_coalitions[acted_upon_agent].agent2.belieftree[0][coalitions.issue][1] += \
								(coalitions.lead.belieftree[0][coalitions.issue][1] - list_links_coalitions[acted_upon_agent].agent2.belieftree[0][coalitions.issue][1]) * \
								coalitions.resources[0] * 0.1 * affiliation_weights[0]

						# Affiliation 1-3
						if (coalitions.lead.affiliation == 0 and list_links_coalitions[acted_upon_agent].agent2.affiliation == 2) or \
							(coalitions.lead.affiliation == 2 and list_links_coalitions[acted_upon_agent].agent2.affiliation == 0):
							list_links_coalitions[acted_upon_agent].agent2.belieftree[0][coalitions.issue][1] += \
								(coalitions.lead.belieftree[0][coalitions.issue][1] - list_links_coalitions[acted_upon_agent].agent2.belieftree[0][coalitions.issue][1]) * \
								coalitions.resources[0] * 0.1 * affiliation_weights[1]

						# Affiliation 2-3
						if (coalitions.lead.affiliation == 1 and list_links_coalitions[acted_upon_agent].agent2.affiliation == 2) or \
							(coalitions.lead.affiliation == 2 and list_links_coalitions[acted_upon_agent].agent2.affiliation == 1):
							list_links_coalitions[acted_upon_agent].agent2.belieftree[0][coalitions.issue][1] += \
								(coalitions.lead.belieftree[0][coalitions.issue][1] - list_links_coalitions[acted_upon_agent].agent2.belieftree[0][coalitions.issue][1]) * \
								coalitions.resources[0] * 0.1 * affiliation_weights[2]
						
						# Checks and transfer of partial knowledge
						# 1-1 check
						list_links_coalitions[acted_upon_agent].agent2.belieftree[0][coalitions.issue][1] = \
							self.one_minus_one_check(list_links_coalitions[acted_upon_agent].agent2.belieftree[0][coalitions.issue][1])
						# Exchange of knowledge - 0.2 - From acted upon to acting
						coalitions.lead.belieftree[1 + acted_upon_agent][coalitions.issue][1] = \
						  list_links_coalitions[acted_upon_agent].agent2.belieftree[0][coalitions.issue][1] + (random.random()/5) - 0.1
						# 1-1 check
						coalitions.lead.belieftree[1 + acted_upon_agent][coalitions.issue][1] = \
							self.one_minus_one_check(coalitions.lead.belieftree[1 + acted_upon_agent][coalitions.issue][1])
						# Exchange of knowledge - 0.2 - From acting to acted upon
						list_links_coalitions[acted_upon_agent].agent2.belieftree[1 + coalitions.lead.unique_id][coalitions.issue][1] = \
						  coalitions.lead.belieftree[0][coalitions.issue][1] + (random.random()/5) - 0.1
						# 1-1 check
						list_links_coalitions[acted_upon_agent].agent2.belieftree[1 + coalitions.lead.unique_id][coalitions.issue][1] = \
							self.one_minus_one_check(list_links_coalitions[acted_upon_agent].agent2.belieftree[1 + coalitions.lead.unique_id][coalitions.issue][1])


					# Updating the resources of the team
					coalitions.resources[1] -= coalitions.resources[0]*0.1

					# Resources check
					if coalitions.resources[1] <= 0 * coalitions.resources[0]:
						break
			
	def coalition_belief_actions_ACF_pf(self, coalitions, causalrelation_number, deep_core, policy_core, secondary, agent_action_list, ACF_link_list_pf, ACF_link_list_pf_total, \
		ACF_link_id_pf, link_list, affiliation_weights, agenda_as_issue, instruments, conflict_level_coef):

		"""
		The coalition belief actions function (policy formulation)
		===========================

		This function is used to perform the actions of the coalitions
		in the policy formulation. The actions of the coalitions are the 
		same actions as the one of the individual agents. The main
		differences here are the amount of resources used and the fact
		that all actions are estimated and performed by the coalition
		leader based on the coalition leader's partial knowledge.

		Note: This function is the same as the previous one but with 
		changes associated with the already selected agenda.

		"""

		len_DC = len(deep_core)
		len_PC = len(policy_core)
		len_S = len(secondary)

		# print(coalitions)

		# print('The belief actions now have to be performed for each team!')
		# Make sure that the coalition actually axists:
		if len(coalitions.members) > 0:

			# 0. Asssigning the resources
			coalitions.resources[1] = coalitions.resources[0]

			# Looking for the relevant causal relations for the policy formulation
			of_interest = []
			cw_of_interest = []
			# We only consider the causal relations related to the problem on the agenda
			for cw_choice in range(len(secondary)):
				if coalitions.lead.belieftree[0][len_DC + len_PC + len_S + (len_DC * len_PC) + (agenda_as_issue - len_DC)*len_S + cw_choice][0] \
					* instruments[coalitions.issue][cw_choice] != 0:
					cw_of_interest.append(len_DC + len_PC + len_S + (len_DC * len_PC) + (agenda_as_issue - len_DC)*len_S + cw_choice)
			of_interest.append(cw_of_interest)
			# Looking for the relevant issues for the policy formulation
			# That is we choose the secondary issues that are impacted by the policy instrument
			# that the agent has selected.
			issue_of_interest = []
			for issue_choice in range(len(secondary)):
				if instruments[coalitions.issue][issue_choice] != 0:
					issue_of_interest.append(len_DC + len_PC + issue_choice)
			of_interest.append(issue_of_interest)
			# print(' ')
			# print('of_interest: ' + str(of_interest))

			# 1. Intra-team actions (actions performed on agents inside the team)
			# This step is only performed if there is more than one team member in the coalition
			if len(coalitions.members) != 1 and len(cw_of_interest) > 0:

				# As long as there are enough resources (50% of the total)
				while True:
					# a. First exchange of information on all causal relations and the policy issue of the team
					#  Exchange of knowledge on the policy (state and aim)
					
					for issues in issue_of_interest:
						self.knowledge_exchange_coalition(coalitions, issues, 0)
						self.knowledge_exchange_coalition(coalitions, issues, 1)
					# Exchange of knowledge on the causal relations

					for cw in range(causalrelation_number):
						self.knowledge_exchange_coalition(coalitions, len_DC + len_PC + len_S + cw, 0)
					
					# b. Compiling all actions for each actor

					# This will need to be adjusted at a later point.
					actionWeight = 1

					#  We look at one causal relation at a time:
					# print(' ')
					# print(coalitions.lead)
					total_agent_grades = []
					for cw in range(len(cw_of_interest)):
						cw_grade_list = []
						# We then go through all agents
						for agent_inspected in coalitions.members:
							# Take the list of links
							for links in link_list:
								# Check that the list has an awareness level
								if links.aware != -1:
									# Check that only the link of interest is selected
									if links.agent1 == coalitions.lead and links.agent2 == agent_inspected or links.agent2 == coalitions.lead and links.agent1 == agent_inspected:
										# Make sure to look at the right direction of the conflict level
										if links.agent1 == coalitions.lead:
											
											# Grade calculation using the likelihood method
											# Same affiliation
											if links.agent1.affiliation == links.agent2.affiliation:
												cw_grade = links.conflict_level[0][cw_of_interest[cw]][0] * links.aware * actionWeight

											# Affiliation 1-2
											if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
												(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
												cw_grade = links.conflict_level[0][cw_of_interest[cw]][0] * links.aware * actionWeight * affiliation_weights[0]

											# Affiliation 1-3
											if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
												(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
												cw_grade = links.conflict_level[0][cw_of_interest[cw]][0] * links.aware * actionWeight * affiliation_weights[1]

											# Affiliation 2-3
											if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
												(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
												cw_grade = links.conflict_level[0][cw_of_interest[cw]][0] * links.aware * actionWeight * affiliation_weights[2]

											cw_grade_list.append(cw_grade)

										if links.agent2 == coalitions.lead:
											
											# Grade calculation using the likelihood method
											# Same affiliation
											if links.agent1.affiliation == links.agent2.affiliation:
												cw_grade = links.conflict_level[1][cw_of_interest[cw]][0] * links.aware * actionWeight

											# Affiliation 1-2
											if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
												(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
												cw_grade = links.conflict_level[1][cw_of_interest[cw]][0] * links.aware * actionWeight * affiliation_weights[0]

											# Affiliation 1-3
											if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
												(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
												cw_grade = links.conflict_level[1][cw_of_interest[cw]][0] * links.aware * actionWeight * affiliation_weights[1]

											# Affiliation 2-3
											if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
												(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
												cw_grade = links.conflict_level[1][cw_of_interest[cw]][0] * links.aware * actionWeight * affiliation_weights[2]
											
											cw_grade_list.append(cw_grade)

								# If the link has a negative awareness, set the grade of the action to 0
								else:
									cw_grade_list.append(0)

							# if coalitions.lead.affiliation == agent_inspected.affiliation:
							# 	cw_grade = abs((coalitions.lead.belieftree[0][cw_of_interest[cw]][0] - \
							# 	  coalitions.lead.belieftree[1 + agent_inspected.unique_id][cw_of_interest[cw]][0]) * \
							# 	  coalitions.resources[0] * 0.1 / (len(coalitions.members)))

							# if (coalitions.lead.affiliation == 0 and agent_inspected.affiliation == 1) or (coalitions.lead.affiliation == 1 and agent_inspected.affiliation == 0):
							# 	cw_grade = abs((coalitions.lead.belieftree[0][cw_of_interest[cw]][0] - \
							# 	  coalitions.lead.belieftree[1 + agent_inspected.unique_id][cw_of_interest[cw]][0]) * \
							# 	  coalitions.resources[0] * 0.1 * affiliation_weights[0] / (len(coalitions.members)))

							# if (coalitions.lead.affiliation == 0 and agent_inspected.affiliation == 2) or (coalitions.lead.affiliation == 2 and agent_inspected.affiliation == 0):
							# 	cw_grade = abs((coalitions.lead.belieftree[0][cw_of_interest[cw]][0] - \
							# 	  coalitions.lead.belieftree[1 + agent_inspected.unique_id][cw_of_interest[cw]][0]) * \
							# 	  coalitions.resources[0] * 0.1 * affiliation_weights[1] / (len(coalitions.members)))

							# if (coalitions.lead.affiliation == 1 and agent_inspected.affiliation == 2) or (coalitions.lead.affiliation == 2 and agent_inspected.affiliation == 1):
							# 	cw_grade = abs((coalitions.lead.belieftree[0][cw_of_interest[cw]][0] - \
							# 	  coalitions.lead.belieftree[1 + agent_inspected.unique_id][cw_of_interest[cw]][0]) * \
							# 	  coalitions.resources[0] * 0.1 * affiliation_weights[2] / (len(coalitions.members)))

							# cw_grade_list.append(cw_grade)
							
						total_agent_grades.append(sum(cw_grade_list))

						# print('CR: ' + str(cw) + ' with grade: ' + str(sum(cw_grade_list)))

					# We look at the state for the policy
					for issue_num in issue_of_interest:
						state_grade_list = []
						# We then go through all agents
						for agent_inspected in coalitions.members:
							# Take the list of links
							for links in link_list:
								# Check that the list has an awareness level
								if links.aware != -1:
									# Check that only the link of interest is selected
									if links.agent1 == coalitions.lead and links.agent2 == agent_inspected or links.agent2 == coalitions.lead and links.agent1 == agent_inspected:

										# Make sure to look at the right direction of the conflict level
										if links.agent1 == coalitions.lead:
										
											# Grade calculation using the likelihood method
											# Same affiliation
											if links.agent1.affiliation == links.agent2.affiliation:
												state_grade = links.conflict_level[0][issue_num][0] * links.aware * actionWeight

											# Affiliation 1-2
											if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
												(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
												state_grade = links.conflict_level[0][issue_num][0] * links.aware * actionWeight * affiliation_weights[0]

											# Affiliation 1-3
											if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
												(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
												state_grade = links.conflict_level[0][issue_num][0] * links.aware * actionWeight * affiliation_weights[1]

											# Affiliation 2-3
											if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
												(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
												state_grade = links.conflict_level[0][issue_num][0] * links.aware * actionWeight * affiliation_weights[2]

											state_grade_list.append(state_grade)

										if links.agent2 == coalitions.lead:
										
											# Grade calculation using the likelihood method
											# Same affiliation
											if links.agent1.affiliation == links.agent2.affiliation:
												state_grade = links.conflict_level[1][issue_num][0] * links.aware * actionWeight

											# Affiliation 1-2
											if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
												(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
												state_grade = links.conflict_level[1][issue_num][0] * links.aware * actionWeight * affiliation_weights[0]

											# Affiliation 1-3
											if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
												(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
												state_grade = links.conflict_level[1][issue_num][0] * links.aware * actionWeight * affiliation_weights[1]

											# Affiliation 2-3
											if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
												(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
												state_grade = links.conflict_level[1][issue_num][0] * links.aware * actionWeight * affiliation_weights[2]
										
											state_grade_list.append(state_grade)
								# If the link has a negative awareness, set the grade of the action to 0
								else:
									state_grade_list.append(0)


							# if coalitions.lead.affiliation == agent_inspected.affiliation:
							# 	state_grade = abs((coalitions.lead.belieftree[0][issue_num][0] - \
							# 	  coalitions.lead.belieftree[1 + agent_inspected.unique_id][issue_num][0]) * coalitions.resources[0] * 0.1 / (len(coalitions.members)))

							# if (coalitions.lead.affiliation == 0 and agent_inspected.affiliation == 1) or (coalitions.lead.affiliation == 1 and agent_inspected.affiliation == 0):
							# 	state_grade = abs((coalitions.lead.belieftree[0][issue_num][0] - coalitions.lead.belieftree[1 + agent_inspected.unique_id][issue_num][0]) \
		    	# 					* coalitions.resources[0] * 0.1 * affiliation_weights[0] / (len(coalitions.members)))

							# if (coalitions.lead.affiliation == 0 and agent_inspected.affiliation == 2) or (coalitions.lead.affiliation == 2 and agent_inspected.affiliation == 0):
							# 	state_grade = abs((coalitions.lead.belieftree[0][issue_num][0] - coalitions.lead.belieftree[1 + agent_inspected.unique_id][issue_num][0]) \
		    	# 					* coalitions.resources[0] * 0.1 * affiliation_weights[1] / (len(coalitions.members)))

							# if (coalitions.lead.affiliation == 1 and agent_inspected.affiliation == 2) or (coalitions.lead.affiliation == 2 and agent_inspected.affiliation == 1):
							# 	state_grade = abs((coalitions.lead.belieftree[0][issue_num][0] - coalitions.lead.belieftree[1 + agent_inspected.unique_id][issue_num][0]) \
		    	# 					* coalitions.resources[0] * 0.1 * affiliation_weights[2] / (len(coalitions.members)))

							# state_grade_list.append(state_grade)

						total_agent_grades.append(sum(state_grade_list))

					# print('State: ' + str(sum(state_grade_list)))
					
					# We look at the aim for the policy
					aim_grade_list = []
					for issue_num in issue_of_interest:
						# We then go through all agents
						for agent_inspected in coalitions.members:
							# Take the list of links
							for links in link_list:
								# Check that the list has an awareness level
								if links.aware != -1:
									# Check that only the link of interest is selected
									if links.agent1 == coalitions.lead and links.agent2 == agent_inspected or links.agent2 == coalitions.lead and links.agent1 == agent_inspected:

										# Make sure to look at the right direction of the conflict level
										if links.agent1 == coalitions.lead:
										
											# Grade calculation using the likelihood method
											# Same affiliation
											if links.agent1.affiliation == links.agent2.affiliation:
												aim_grade = links.conflict_level[0][issue_num][1] * links.aware * actionWeight

											# Affiliation 1-2
											if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
												(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
												aim_grade = links.conflict_level[0][issue_num][1] * links.aware * actionWeight * affiliation_weights[0]

											# Affiliation 1-3
											if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
												(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
												aim_grade = links.conflict_level[0][issue_num][1] * links.aware * actionWeight * affiliation_weights[1]

											# Affiliation 2-3
											if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
												(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
												aim_grade = links.conflict_level[0][issue_num][1] * links.aware * actionWeight * affiliation_weights[2]

											aim_grade_list.append(aim_grade)

										if links.agent1 == coalitions.lead:
										
											# Grade calculation using the likelihood method
											# Same affiliation
											if links.agent1.affiliation == links.agent2.affiliation:
												aim_grade = links.conflict_level[1][issue_num][1] * links.aware * actionWeight

											# Affiliation 1-2
											if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
												(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
												aim_grade = links.conflict_level[1][issue_num][1] * links.aware * actionWeight * affiliation_weights[0]

											# Affiliation 1-3
											if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
												(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
												aim_grade = links.conflict_level[1][issue_num][1] * links.aware * actionWeight * affiliation_weights[1]

											# Affiliation 2-3
											if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
												(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
												aim_grade = links.conflict_level[1][issue_num][1] * links.aware * actionWeight * affiliation_weights[2]
										
											aim_grade_list.append(aim_grade)
								# If the link has a negative awareness, set the grade of the action to 0
								else:
									aim_grade_list.append(0)



							# if coalitions.lead.affiliation == agent_inspected.affiliation:
							# 	aim_grade = abs((coalitions.lead.belieftree[0][issue_num][1] - \
							# 	  coalitions.lead.belieftree[1 + agent_inspected.unique_id][issue_num][1]) * coalitions.resources[0] * 0.1 / (len(coalitions.members)))

							# if (coalitions.lead.affiliation == 0 and agent_inspected.affiliation == 1) or (coalitions.lead.affiliation == 1 and agent_inspected.affiliation == 0):
							# 	aim_grade = abs((coalitions.lead.belieftree[0][issue_num][1] - \
							# 	  coalitions.lead.belieftree[1 + agent_inspected.unique_id][issue_num][1]) * coalitions.resources[0] * 0.1 * affiliation_weights[0] / (len(coalitions.members)))

							# if (coalitions.lead.affiliation == 0 and agent_inspected.affiliation == 2) or (coalitions.lead.affiliation == 2 and agent_inspected.affiliation == 0):
							# 	aim_grade = abs((coalitions.lead.belieftree[0][issue_num][1] - \
							# 	  coalitions.lead.belieftree[1 + agent_inspected.unique_id][issue_num][1]) * coalitions.resources[0] * 0.1 * affiliation_weights[1] / (len(coalitions.members)))

							# if (coalitions.lead.affiliation == 1 and agent_inspected.affiliation == 2) or (coalitions.lead.affiliation == 2 and agent_inspected.affiliation == 1):
							# 	aim_grade = abs((coalitions.lead.belieftree[0][issue_num][1] - \
							# 	  coalitions.lead.belieftree[1 + agent_inspected.unique_id][issue_num][1]) * coalitions.resources[0] * 0.1 * affiliation_weights[2] / (len(coalitions.members)))

							# aim_grade_list.append(aim_grade)

						total_agent_grades.append(sum(aim_grade_list))

					# c. Finding the best action
					best_action_index = total_agent_grades.index(min(total_agent_grades))

					# print(' ')
					# print('----- Considering new action grading -----')
					# print('Action to be performed: ' + str(best_action_index))

					# d. Implementation the best action

					# The causal relation action is performed
					if best_action_index <= len(cw_of_interest) - 1:
						# print(' ')
						# print('Performing a CR action')
						# print(of_interest[0])
						# print('best_action_index: ' + str(best_action_index))
						# print(of_interest[0][best_action_index])

						# It is the agent that has the best action that performs the action
						for agent_impacted in coalitions.members:

							if agent_impacted.affiliation == coalitions.lead.affiliation:
								agent_impacted.belieftree[0][of_interest[0][best_action_index]][0] += \
									(coalitions.lead.belieftree[0][of_interest[0][best_action_index]][0]) - agent_impacted.belieftree[0][of_interest[0][best_action_index]][0] * \
									coalitions.resources[0] * 0.1 / len(coalitions.members)

							if (agent_impacted.affiliation == 0 and coalitions.lead.affiliation == 1) or (agent_impacted.affiliation == 1 and coalitions.lead.affiliation == 0):
								agent_impacted.belieftree[0][of_interest[0][best_action_index]][0] += \
									(coalitions.lead.belieftree[0][of_interest[0][best_action_index]][0]) - agent_impacted.belieftree[0][of_interest[0][best_action_index]][0] * \
									coalitions.resources[0] * 0.1 * affiliation_weights[0] / len(coalitions.members)

							if (agent_impacted.affiliation == 0 and coalitions.lead.affiliation == 2) or (agent_impacted.affiliation == 2 and coalitions.lead.affiliation == 0):
								agent_impacted.belieftree[0][of_interest[0][best_action_index]][0] += \
									(coalitions.lead.belieftree[0][of_interest[0][best_action_index]][0]) - agent_impacted.belieftree[0][of_interest[0][best_action_index]][0] * \
									coalitions.resources[0] * 0.1 * affiliation_weights[1] / len(coalitions.members)

							if (agent_impacted.affiliation == 1 and coalitions.lead.affiliation == 2) or (agent_impacted.affiliation == 2 and coalitions.lead.affiliation == 1):
								agent_impacted.belieftree[0][of_interest[0][best_action_index]][0] += \
									(coalitions.lead.belieftree[0][of_interest[0][best_action_index]][0]) - agent_impacted.belieftree[0][of_interest[0][best_action_index]][0] * \
									coalitions.resources[0] * 0.1 * affiliation_weights[2] / len(coalitions.members)

							# 1-1 check
							agent_impacted.belieftree[0][of_interest[0][best_action_index]][0] = \
								self.one_minus_one_check(agent_impacted.belieftree[0][of_interest[0][best_action_index]][0])
							
					# The state change is performed
					elif best_action_index > len(cw_of_interest) - 1 and best_action_index < len(cw_of_interest) + len(issue_of_interest) - 1:
						# print(' ')
						# print('Performing a state action')
						# print(of_interest[1])
						# print('best_action_index - len(cw_of_interest): ' + str(best_action_index - len(cw_of_interest)))
						# print(of_interest[1][best_action_index - len(cw_of_interest)])
						
						# It is the agent that has the best action that performs the action
						for agent_impacted in coalitions.members:

							if agent_impacted.affiliation == coalitions.lead.affiliation:
								agent_impacted.belieftree[0][of_interest[1][best_action_index - len(cw_of_interest)]][0] += \
								(coalitions.lead.belieftree[0][of_interest[1][best_action_index - len(cw_of_interest)]][0] - agent_impacted.belieftree[0][of_interest[1][best_action_index - len(cw_of_interest)]][0]) * \
									coalitions.resources[0] * 0.1 / (len(coalitions.members))

							if (agent_impacted.affiliation == 0 and coalitions.lead.affiliation == 1) or (agent_impacted.affiliation == 1 and coalitions.lead.affiliation == 0):
								agent_impacted.belieftree[0][of_interest[1][best_action_index - len(cw_of_interest)]][0] += \
									(coalitions.lead.belieftree[0][of_interest[1][best_action_index - len(cw_of_interest)]][0] - agent_impacted.belieftree[0][of_interest[1][best_action_index - len(cw_of_interest)]][0]) * \
									coalitions.resources[0] * 0.1 * affiliation_weights[0] / (len(coalitions.members))

							if (agent_impacted.affiliation == 0 and coalitions.lead.affiliation == 2) or (agent_impacted.affiliation == 2 and coalitions.lead.affiliation == 0):
								agent_impacted.belieftree[0][of_interest[1][best_action_index - len(cw_of_interest)]][0] += \
									(coalitions.lead.belieftree[0][of_interest[1][best_action_index - len(cw_of_interest)]][0] - agent_impacted.belieftree[0][of_interest[1][best_action_index - len(cw_of_interest)]][0]) * \
									coalitions.resources[0] * 0.1 * affiliation_weights[1] / (len(coalitions.members))

							if (agent_impacted.affiliation == 1 and coalitions.lead.affiliation == 2) or (agent_impacted.affiliation == 2 and coalitions.lead.affiliation == 1):
								agent_impacted.belieftree[0][of_interest[1][best_action_index - len(cw_of_interest)]][0] += \
									(coalitions.lead.belieftree[0][of_interest[1][best_action_index - len(cw_of_interest)]][0] - agent_impacted.belieftree[0][of_interest[1][best_action_index - len(cw_of_interest)]][0]) * \
									coalitions.resources[0] * 0.1 * affiliation_weights[2] / (len(coalitions.members))

							# 1-1 check
							agent_impacted.belieftree[0][best_action_index - len(cw_of_interest)][0] = \
								self.one_minus_one_check(agent_impacted.belieftree[0][best_action_index - len(cw_of_interest)][0])

					# The aim change is performed
					elif best_action_index >= len(cw_of_interest) + len(issue_of_interest) - 1:
						# print(' ')
						# print('Performing an aim action')
						# print(of_interest[1])
						# print('best_action_index - len(cw_of_interest) - len(cw_of_interest): ' + str(best_action_index - len(cw_of_interest) - len(cw_of_interest)))
						# print(of_interest[1][best_action_index - len(cw_of_interest) - len(cw_of_interest)])
						
						for agent_impacted in coalitions.members:

							if agent_impacted.affiliation == coalitions.lead.affiliation:
								agent_impacted.belieftree[0][of_interest[1][best_action_index - len(cw_of_interest) - len(cw_of_interest)]][1] += \
									(coalitions.lead.belieftree[0][of_interest[1][best_action_index - len(cw_of_interest) - len(cw_of_interest)]][1] - \
									agent_impacted.belieftree[0][of_interest[1][best_action_index - len(cw_of_interest) - len(cw_of_interest)]][1]) * \
									coalitions.resources[0] * 0.1 / (len(coalitions.members))

							if (agent_impacted.affiliation == 0 and coalitions.lead.affiliation == 1) or (agent_impacted.affiliation == 1 and coalitions.lead.affiliation == 0):
								agent_impacted.belieftree[0][of_interest[1][best_action_index - len(cw_of_interest) - len(cw_of_interest)]][1] += \
									(coalitions.lead.belieftree[0][of_interest[1][best_action_index - len(cw_of_interest) - len(cw_of_interest)]][1] - \
									agent_impacted.belieftree[0][of_interest[1][best_action_index - len(cw_of_interest) - len(cw_of_interest)]][1]) * \
									coalitions.resources[0] * 0.1 * affiliation_weights[0] / (len(coalitions.members))

							if (agent_impacted.affiliation == 0 and coalitions.lead.affiliation == 2) or (agent_impacted.affiliation == 2 and coalitions.lead.affiliation == 0):
								agent_impacted.belieftree[0][of_interest[1][best_action_index - len(cw_of_interest) - len(cw_of_interest)]][1] += \
									(coalitions.lead.belieftree[0][of_interest[1][best_action_index - len(cw_of_interest) - len(cw_of_interest)]][1] - \
									agent_impacted.belieftree[0][of_interest[1][best_action_index - len(cw_of_interest) - len(cw_of_interest)]][1]) * \
									coalitions.resources[0] * 0.1 * affiliation_weights[1] / (len(coalitions.members))

							if (agent_impacted.affiliation == 1 and coalitions.lead.affiliation == 2) or (agent_impacted.affiliation == 2 and coalitions.lead.affiliation == 1):
								agent_impacted.belieftree[0][of_interest[1][best_action_index - len(cw_of_interest) - len(cw_of_interest)]][1] += \
									(coalitions.lead.belieftree[0][of_interest[1][best_action_index - len(cw_of_interest) - len(cw_of_interest)]][1] - \
									agent_impacted.belieftree[0][of_interest[1][best_action_index - len(cw_of_interest) - len(cw_of_interest)]][1]) * \
									coalitions.resources[0] * 0.1 * affiliation_weights[2] / (len(coalitions.members))

							# 1-1 check
							agent_impacted.belieftree[0][of_interest[1][best_action_index - len(cw_of_interest) - len(cw_of_interest)]][1] = \
								self.one_minus_one_check(agent_impacted.belieftree[0][of_interest[1][best_action_index - len(cw_of_interest) - len(cw_of_interest)]][1])
					
					# Updating the resources of the team
					coalitions.resources[1] -= coalitions.resources[0]*0.1

					# Resources check
					if coalitions.resources[1] <= 0.5 * coalitions.resources[0]:
						# print('RAN OUT OF RESOURCES!')
						break

			# 2. Inter-team actions (actions performed on agents outside the team)

			# Only perform this if not all agents are in the coalition
			if len(coalitions.members) < len(agent_action_list) and len(cw_of_interest) > 0:

				# Creation of the list of agents to be considered:
				inter_agent_list = []
				for potential_agent in agent_action_list:
					if potential_agent not in coalitions.members:
						inter_agent_list.append(potential_agent)
				# print(' ')
				# print('# of agents not in the team: ' + str(len(inter_agent_list)))

				# Creation of the shadow network for this coalition
				# print('We need to create a link network for this team!')
				for agent_network in inter_agent_list:
					# Do not take into account EP with no interest in that issue for the network
					if agent_network.belieftree[0][coalitions.issue][0] != 'No':
						# print(' ')
						# print('Added 1 - ' + str(agent_network))
						self.new_link_ACF_pf(link_list, agent_network, coalitions, ACF_link_list_pf, ACF_link_list_pf_total, ACF_link_id_pf, len_DC, len_PC, len_S, conflict_level_coef)

				# Performing the actions using the shadow network and the individual agents within the team

				# As long as there are enough resources (50% of the total)
				while True:

					# print('Performing inter-team actions')

					total_agent_grades = []
					# for agents_in_team in teams.members:
					# Going through all agents that are not part of the team
					link_count = 0
					for links in ACF_link_list_pf:
						# Make sure to select an existing link
						if links.aware != -1:
							# Make sure to only select the links related to this team
							if coalitions == links.agent1:
								link_count += 1
								# Setting the action weight
								# Removed for now for technical issues
								# if type(links.agent2) == Policymakers:
								# 		actionWeight = 1
								# else:
								# 	actionWeight = 0.95
								actionWeight = 1
								# Framing actions:
								for cw in range(len(cw_of_interest)):

									# Grade calculation using the likelihood method
									# Same affiliation
									if coalitions.lead.affiliation == links.agent2.affiliation:
										cw_grade = links.conflict_level[len_S + cw_of_interest[cw] - (len_DC + len_PC + len_S)] * links.aware * actionWeight
										total_agent_grades.append(cw_grade)

									# Affiliation 1-2
									if (coalitions.lead.affiliation == 0 and links.agent2.affiliation == 1) or \
										(coalitions.lead.affiliation == 1 and links.agent2.affiliation == 0):
										cw_grade = links.conflict_level[len_S + cw_of_interest[cw] - (len_DC + len_PC + len_S)] * links.aware * actionWeight * affiliation_weights[0]
										total_agent_grades.append(cw_grade)

									# Affiliation 1-3
									if (coalitions.lead.affiliation == 0 and links.agent2.affiliation == 2) or \
										(coalitions.lead.affiliation == 2 and links.agent2.affiliation == 0):
										cw_grade = links.conflict_level[len_S + cw_of_interest[cw] - (len_DC + len_PC + len_S)] * links.aware * actionWeight * affiliation_weights[1]
										total_agent_grades.append(cw_grade)

									# Affiliation 2-3
									if (coalitions.lead.affiliation == 1 and links.agent2.affiliation == 2) or \
										(coalitions.lead.affiliation == 2 and links.agent2.affiliation == 1):
										cw_grade = links.conflict_level[len_S + cw_of_interest[cw] - (len_DC + len_PC + len_S)] * links.aware * actionWeight * affiliation_weights[2]
										total_agent_grades.append(cw_grade)

									# check_none = 0
									# if coalitions.lead.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0] == None:
									# 	coalitions.lead.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0] = 0
									# 	check_none = 1
									# cw_grade = abs((coalitions.lead.belieftree[0][cw_of_interest[cw]][0] - \
									#   coalitions.lead.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0]) * \
									#   coalitions.resources[0] * 0.1 * links.aware * actionWeight)
									# total_agent_grades.append(cw_grade)
									# # None reset
									# if check_none == 1:
									# 	coalitions.lead.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0] = None
								
								# State influence actions
								for issue_num in range(len(issue_of_interest)):

									# Grade calculation using the likelihood method
									# Same affiliation
									if coalitions.lead.affiliation == links.agent2.affiliation:
										state_grade = links.conflict_level[issue_of_interest[issue_num] - (len_DC + len_PC)][0] * links.aware * actionWeight
										total_agent_grades.append(state_grade)

									# Affiliation 1-2
									if (coalitions.lead.affiliation == 0 and links.agent2.affiliation == 1) or \
										(coalitions.lead.affiliation == 1 and links.agent2.affiliation == 0):
										state_grade = links.conflict_level[issue_of_interest[issue_num] - (len_DC + len_PC)][0] * links.aware * actionWeight * affiliation_weights[0]
										total_agent_grades.append(state_grade)

									# Affiliation 1-3
									if (coalitions.lead.affiliation == 0 and links.agent2.affiliation == 2) or \
										(coalitions.lead.affiliation == 2 and links.agent2.affiliation == 0):
										state_grade = links.conflict_level[issue_of_interest[issue_num] - (len_DC + len_PC)][0] * links.aware * actionWeight * affiliation_weights[1]
										total_agent_grades.append(state_grade)

									# Affiliation 2-3
									if (coalitions.lead.affiliation == 1 and links.agent2.affiliation == 2) or \
										(coalitions.lead.affiliation == 2 and links.agent2.affiliation == 1):
										state_grade = links.conflict_level[issue_of_interest[issue_num] - (len_DC + len_PC)][0] * links.aware * actionWeight * affiliation_weights[2]
										total_agent_grades.append(state_grade)
									
									# check_none = 0
									# if coalitions.lead.belieftree[1 + links.agent2.unique_id][issue_of_interest[issue_num]][0] == None:
									# 	coalitions.lead.belieftree[1 + links.agent2.unique_id][issue_of_interest[issue_num]][0] = 0
									# 	check_none = 1
									# state_grade = abs((coalitions.lead.belieftree[0][issue_of_interest[issue_num]][0] - \
									#   coalitions.lead.belieftree[1 + links.agent2.unique_id][issue_of_interest[issue_num]][0]) * coalitions.resources[0] * 0.1 * links.aware * links.conflict_level[issue_of_interest[issue_num] - (len_DC + len_PC)][0] * actionWeight)
									# total_agent_grades.append(state_grade)
									# # None reset
									# if check_none == 1:
									# 	coalitions.lead.belieftree[1 + links.agent2.unique_id][issue_of_interest[issue_num]][0] = None

								# Aim influence actions
								for issue_num in range(len(issue_of_interest)):

									# Grade calculation using the likelihood method
									# Same affiliation
									if coalitions.lead.affiliation == links.agent2.affiliation:
										aim_grade = links.conflict_level[issue_of_interest[issue_num] - (len_DC + len_PC)][1] * links.aware * actionWeight
										total_agent_grades.append(aim_grade)

									# Affiliation 1-2
									if (coalitions.lead.affiliation == 0 and links.agent2.affiliation == 1) or \
										(coalitions.lead.affiliation == 1 and links.agent2.affiliation == 0):
										aim_grade = links.conflict_level[issue_of_interest[issue_num] - (len_DC + len_PC)][1] * links.aware * actionWeight * affiliation_weights[0]
										total_agent_grades.append(aim_grade)

									# Affiliation 1-3
									if (coalitions.lead.affiliation == 0 and links.agent2.affiliation == 2) or \
										(coalitions.lead.affiliation == 2 and links.agent2.affiliation == 0):
										aim_grade = links.conflict_level[issue_of_interest[issue_num] - (len_DC + len_PC)][1] * links.aware * actionWeight * affiliation_weights[1]
										total_agent_grades.append(aim_grade)

									# Affiliation 2-3
									if (coalitions.lead.affiliation == 1 and links.agent2.affiliation == 2) or \
										(coalitions.lead.affiliation == 2 and links.agent2.affiliation == 1):
										aim_grade = links.conflict_level[issue_of_interest[issue_num] - (len_DC + len_PC)][1] * links.aware * actionWeight * affiliation_weights[2]
										total_agent_grades.append(aim_grade)

									# check_none = 0
									# if coalitions.lead.belieftree[1 + links.agent2.unique_id][issue_of_interest[issue_num]][1] == None:
									# 	coalitions.lead.belieftree[1 + links.agent2.unique_id][issue_of_interest[issue_num]][1] = 0
									# 	check_none = 1
									# aim_grade = abs((coalitions.lead.belieftree[0][issue_of_interest[issue_num]][1] - \
									#   coalitions.lead.belieftree[1 + links.agent2.unique_id][issue_of_interest[issue_num]][1]) * coalitions.resources[0] * 0.1 * links.aware * links.conflict_level[issue_of_interest[issue_num] - (len_DC + len_PC)][1] * actionWeight)
									# total_agent_grades.append(aim_grade)
									# # None reset
									# if check_none == 1:
									# 	coalitions.lead.belieftree[1 + links.agent2.unique_id][issue_of_interest[issue_num]][1] = None									

					# Choosing the best action
					best_action_index = total_agent_grades.index(max(total_agent_grades))
					best_action = best_action_index - int(best_action_index/(len(cw_of_interest) + 2*len(issue_of_interest)))*(len(cw_of_interest) + 2*len(issue_of_interest))
					acted_upon_agent = int(best_action_index/(len(cw_of_interest) + 2*len(issue_of_interest)))

					# print(' ')
					# print('----- Considering new action grading -----')
					# print('Original index: ' + str(best_action_index))
					# print('Number of actions that can be performed: ' + str(len(cw_of_interest) + + 2*len(issue_of_interest)))
					# print('Action to be performed: ' + str(best_action))
					# print('This is the agent on which the action is performed: ' + str(acted_upon_agent))

					# Actually performing the action:
					# Getting a list of the links related to this team
					list_links_coalitions = []
					for links in ACF_link_list_pf:
							# Make sure to only select the links related to this team
							if coalitions == links.agent1:
								# Make sure to select an existing link
								if links.aware != -1:
									list_links_coalitions.append(links)

					# Implement framing action
					if best_action <= len(cw_of_interest) - 1:
						# print(' ')
						# print('Performing a CR action')
						# print(of_interest[0])
						# print('best_action: ' + str(best_action))
						# print(of_interest[0][best_action])

						# print('Before: ' + str(list_links_coalitions[acted_upon_agent].agent2.belieftree[0][len(deep_core) + len(policy_core) + len(secondary) + best_action - 1][0]))

						# Same affiliation
						if coalitions.lead.affiliation == list_links_coalitions[acted_upon_agent].agent2.affiliation:
							list_links_coalitions[acted_upon_agent].agent2.belieftree[0][of_interest[0][best_action]][0] += \
								(coalitions.lead.belieftree[0][of_interest[0][best_action]][0] - list_links_coalitions[acted_upon_agent].agent2.belieftree[0][of_interest[0][best_action]][0]) * \
								coalitions.resources[0] * 0.1

						# Affiliation 1-2
						if (coalitions.lead.affiliation == 0 and list_links_coalitions[acted_upon_agent].agent2.affiliation == 1) or \
							(coalitions.lead.affiliation == 1 and list_links_coalitions[acted_upon_agent].agent2.affiliation == 0):
							list_links_coalitions[acted_upon_agent].agent2.belieftree[0][of_interest[0][best_action]][0] += \
								(coalitions.lead.belieftree[0][of_interest[0][best_action]][0] - list_links_coalitions[acted_upon_agent].agent2.belieftree[0][of_interest[0][best_action]][0]) * \
								coalitions.resources[0] * 0.1 * affiliation_weights[0]

						# Affiliation 1-3
						if (coalitions.lead.affiliation == 0 and list_links_coalitions[acted_upon_agent].agent2.affiliation == 2) or \
							(coalitions.lead.affiliation == 2 and list_links_coalitions[acted_upon_agent].agent2.affiliation == 0):
							list_links_coalitions[acted_upon_agent].agent2.belieftree[0][of_interest[0][best_action]][0] += \
								(coalitions.lead.belieftree[0][of_interest[0][best_action]][0] - list_links_coalitions[acted_upon_agent].agent2.belieftree[0][of_interest[0][best_action]][0]) * \
								coalitions.resources[0] * 0.1 * affiliation_weights[1]

						# Affiliation 2-3
						if (coalitions.lead.affiliation == 1 and list_links_coalitions[acted_upon_agent].agent2.affiliation == 2) or \
							(coalitions.lead.affiliation == 2 and list_links_coalitions[acted_upon_agent].agent2.affiliation == 1):
							list_links_coalitions[acted_upon_agent].agent2.belieftree[0][of_interest[0][best_action]][0] += \
								(coalitions.lead.belieftree[0][of_interest[0][best_action]][0] - list_links_coalitions[acted_upon_agent].agent2.belieftree[0][of_interest[0][best_action]][0]) * \
								coalitions.resources[0] * 0.1 * affiliation_weights[2]

						# print('After: ' + str(list_links_coalitions[acted_upon_agent].agent2.belieftree[0][len(deep_core) + len(policy_core) + len(secondary) + best_action - 1][0]))
						
						# Checks and transfer of partial knowledge
						# 1-1 check
						list_links_coalitions[acted_upon_agent].agent2.belieftree[0][of_interest[0][best_action]][0] = \
							self.one_minus_one_check(list_links_coalitions[acted_upon_agent].agent2.belieftree[0][of_interest[0][best_action]][0])
						# Exchange of knowledge - 0.2 - From acted upon to acting
						coalitions.lead.belieftree[1 + acted_upon_agent][of_interest[0][best_action]][0] = \
						  list_links_coalitions[acted_upon_agent].agent2.belieftree[0][of_interest[0][best_action]][0] + (random.random()/5) - 0.1
						# 1-1 check
						coalitions.lead.belieftree[1 + acted_upon_agent][of_interest[0][best_action]][0] = \
							self.one_minus_one_check(coalitions.lead.belieftree[1 + acted_upon_agent][of_interest[0][best_action]][0])
						# Exchange of knowledge - 0.2 - From acting to acted upon
						list_links_coalitions[acted_upon_agent].agent2.belieftree[1 + coalitions.lead.unique_id][of_interest[0][best_action]][0] = \
						  coalitions.lead.belieftree[0][of_interest[0][best_action]][0] + (random.random()/5) - 0.1
						# 1-1 check
						list_links_coalitions[acted_upon_agent].agent2.belieftree[1 + coalitions.lead.unique_id][of_interest[0][best_action]][0] = \
							self.one_minus_one_check(list_links_coalitions[acted_upon_agent].agent2.belieftree[1 + coalitions.lead.unique_id][of_interest[0][best_action]][0])

					# Implement state influence action
					elif best_action > len(cw_of_interest) - 1 and best_action < len(cw_of_interest) + len(issue_of_interest) - 1:
						# print(' ')
						# print('Performing a state action')
						# print(of_interest[1])
						# print('best_action - len(cw_of_interest): ' + str(best_action - len(cw_of_interest)))
						# print(of_interest[1][best_action - len(cw_of_interest)])

						# Same affiliation
						if coalitions.lead.affiliation == list_links_coalitions[acted_upon_agent].agent2.affiliation:
							list_links_coalitions[acted_upon_agent].agent2.belieftree[0][of_interest[1][best_action - len(cw_of_interest)]][0] += \
								(coalitions.lead.belieftree[0][of_interest[1][best_action - len(cw_of_interest)]][0] - \
								list_links_coalitions[acted_upon_agent].agent2.belieftree[0][of_interest[1][best_action - len(cw_of_interest)]][0]) * \
								coalitions.resources[0] * 0.1

						# Affiliation 1-2
						if (coalitions.lead.affiliation == 0 and list_links_coalitions[acted_upon_agent].agent2.affiliation == 1) or \
							(coalitions.lead.affiliation == 1 and list_links_coalitions[acted_upon_agent].agent2.affiliation == 0):
							list_links_coalitions[acted_upon_agent].agent2.belieftree[0][of_interest[1][best_action - len(cw_of_interest)]][0] += \
								(coalitions.lead.belieftree[0][of_interest[1][best_action - len(cw_of_interest)]][0] - \
								list_links_coalitions[acted_upon_agent].agent2.belieftree[0][of_interest[1][best_action - len(cw_of_interest)]][0]) * \
								coalitions.resources[0] * 0.1 * affiliation_weights[0]

						# Affiliation 1-3
						if (coalitions.lead.affiliation == 0 and list_links_coalitions[acted_upon_agent].agent2.affiliation == 2) or \
							(coalitions.lead.affiliation == 2 and list_links_coalitions[acted_upon_agent].agent2.affiliation == 0):
							list_links_coalitions[acted_upon_agent].agent2.belieftree[0][of_interest[1][best_action - len(cw_of_interest)]][0] += \
								(coalitions.lead.belieftree[0][of_interest[1][best_action - len(cw_of_interest)]][0] - \
								list_links_coalitions[acted_upon_agent].agent2.belieftree[0][of_interest[1][best_action - len(cw_of_interest)]][0]) * \
								coalitions.resources[0] * 0.1 * affiliation_weights[1]

						# Affiliation 2-3
						if (coalitions.lead.affiliation == 1 and list_links_coalitions[acted_upon_agent].agent2.affiliation == 2) or \
							(coalitions.lead.affiliation == 2 and list_links_coalitions[acted_upon_agent].agent2.affiliation == 1):
							list_links_coalitions[acted_upon_agent].agent2.belieftree[0][of_interest[1][best_action - len(cw_of_interest)]][0] += \
								(coalitions.lead.belieftree[0][of_interest[1][best_action - len(cw_of_interest)]][0] - \
								list_links_coalitions[acted_upon_agent].agent2.belieftree[0][of_interest[1][best_action - len(cw_of_interest)]][0]) * \
								coalitions.resources[0] * 0.1 * affiliation_weights[2]

						# Checks and transfer of partial knowledge
						# 1-1 check
						list_links_coalitions[acted_upon_agent].agent2.belieftree[0][of_interest[1][best_action - len(cw_of_interest)]][0] = \
							self.one_minus_one_check(list_links_coalitions[acted_upon_agent].agent2.belieftree[0][of_interest[1][best_action - len(cw_of_interest)]][0])
						# Exchange of knowledge - 0.2 - From acted upon to acting
						coalitions.lead.belieftree[1 + acted_upon_agent][of_interest[1][best_action - len(cw_of_interest)]][0] = \
						  list_links_coalitions[acted_upon_agent].agent2.belieftree[0][of_interest[1][best_action - len(cw_of_interest)]][0] + (random.random()/5) - 0.1
						# 1-1 check
						coalitions.lead.belieftree[1 + acted_upon_agent][of_interest[1][best_action - len(cw_of_interest)]][0] = \
							self.one_minus_one_check(coalitions.lead.belieftree[1 + acted_upon_agent][of_interest[1][best_action - len(cw_of_interest)]][0])
						# Exchange of knowledge - 0.2 - From acting to acted upon
						list_links_coalitions[acted_upon_agent].agent2.belieftree[1 + coalitions.lead.unique_id][of_interest[1][best_action - len(cw_of_interest)]][0] = \
						  coalitions.lead.belieftree[0][of_interest[1][best_action - len(cw_of_interest)]][0] + (random.random()/5) - 0.1
						# 1-1 check
						list_links_coalitions[acted_upon_agent].agent2.belieftree[1 + coalitions.lead.unique_id][of_interest[1][best_action - len(cw_of_interest)]][0] = \
							self.one_minus_one_check(list_links_coalitions[acted_upon_agent].agent2.belieftree[1 + coalitions.lead.unique_id][of_interest[1][best_action - len(cw_of_interest)]][0])

					# Implement aim influence action
					elif best_action >= len(cw_of_interest) + len(issue_of_interest) - 1:
						# print(' ')
						# print('Performing an aim action')
						# print(of_interest[1])
						# print('best_action - len(cw_of_interest) - len(cw_of_interest): ' + str(best_action - len(cw_of_interest) - len(cw_of_interest)))
						# print(of_interest[1][best_action - len(cw_of_interest) - len(cw_of_interest)])

						if coalitions.lead.affiliation == list_links_coalitions[acted_upon_agent].agent2.affiliation:
							list_links_coalitions[acted_upon_agent].agent2.belieftree[0][of_interest[1][best_action - len(cw_of_interest) - len(cw_of_interest)]][1] += \
								(coalitions.lead.belieftree[0][of_interest[1][best_action - len(cw_of_interest) - len(cw_of_interest)]][1] - \
								list_links_coalitions[acted_upon_agent].agent2.belieftree[0][of_interest[1][best_action - len(cw_of_interest) - len(cw_of_interest)]][1]) * \
								coalitions.resources[0] * 0.1

						# Affiliation 1-2
						if (coalitions.lead.affiliation == 0 and list_links_coalitions[acted_upon_agent].agent2.affiliation == 1) or \
							(coalitions.lead.affiliation == 1 and list_links_coalitions[acted_upon_agent].agent2.affiliation == 0):
							list_links_coalitions[acted_upon_agent].agent2.belieftree[0][of_interest[1][best_action - len(cw_of_interest) - len(cw_of_interest)]][1] += \
								(coalitions.lead.belieftree[0][of_interest[1][best_action - len(cw_of_interest) - len(cw_of_interest)]][1] - \
								list_links_coalitions[acted_upon_agent].agent2.belieftree[0][of_interest[1][best_action - len(cw_of_interest) - len(cw_of_interest)]][1]) * \
								coalitions.resources[0] * 0.1 * affiliation_weights[0]

						# Affiliation 1-3
						if (coalitions.lead.affiliation == 0 and list_links_coalitions[acted_upon_agent].agent2.affiliation == 2) or \
							(coalitions.lead.affiliation == 2 and list_links_coalitions[acted_upon_agent].agent2.affiliation == 0):
							list_links_coalitions[acted_upon_agent].agent2.belieftree[0][of_interest[1][best_action - len(cw_of_interest) - len(cw_of_interest)]][1] += \
								(coalitions.lead.belieftree[0][of_interest[1][best_action - len(cw_of_interest) - len(cw_of_interest)]][1] - \
								list_links_coalitions[acted_upon_agent].agent2.belieftree[0][of_interest[1][best_action - len(cw_of_interest) - len(cw_of_interest)]][1]) * \
								coalitions.resources[0] * 0.1 * affiliation_weights[1]

						# Affiliation 2-3
						if (coalitions.lead.affiliation == 1 and list_links_coalitions[acted_upon_agent].agent2.affiliation == 2) or \
							(coalitions.lead.affiliation == 2 and list_links_coalitions[acted_upon_agent].agent2.affiliation == 1):
							list_links_coalitions[acted_upon_agent].agent2.belieftree[0][of_interest[1][best_action - len(cw_of_interest) - len(cw_of_interest)]][1] += \
								(coalitions.lead.belieftree[0][of_interest[1][best_action - len(cw_of_interest) - len(cw_of_interest)]][1] - \
								list_links_coalitions[acted_upon_agent].agent2.belieftree[0][of_interest[1][best_action - len(cw_of_interest) - len(cw_of_interest)]][1]) * \
								coalitions.resources[0] * 0.1 * affiliation_weights[2]
						
						# Checks and transfer of partial knowledge
						# 1-1 check
						list_links_coalitions[acted_upon_agent].agent2.belieftree[0][of_interest[1][best_action - len(cw_of_interest) - len(cw_of_interest)]][1] = \
							self.one_minus_one_check(list_links_coalitions[acted_upon_agent].agent2.belieftree[0][of_interest[1][best_action - len(cw_of_interest) - len(cw_of_interest)]][1])
						# Exchange of knowledge - 0.2 - From acted upon to acting
						coalitions.lead.belieftree[1 + acted_upon_agent][of_interest[1][best_action - len(cw_of_interest) - len(cw_of_interest)]][1] = \
						  list_links_coalitions[acted_upon_agent].agent2.belieftree[0][of_interest[1][best_action - len(cw_of_interest) - len(cw_of_interest)]][1] + (random.random()/5) - 0.1
						# 1-1 check
						coalitions.lead.belieftree[1 + acted_upon_agent][of_interest[1][best_action - len(cw_of_interest) - len(cw_of_interest)]][1] = \
							self.one_minus_one_check(coalitions.lead.belieftree[1 + acted_upon_agent][of_interest[1][best_action - len(cw_of_interest) - len(cw_of_interest)]][1])
						# Exchange of knowledge - 0.2 - From acting to acted upon
						list_links_coalitions[acted_upon_agent].agent2.belieftree[1 + coalitions.lead.unique_id][of_interest[1][best_action - len(cw_of_interest) - len(cw_of_interest)]][1] = \
						  coalitions.lead.belieftree[0][of_interest[1][best_action - len(cw_of_interest) - len(cw_of_interest)]][1] + (random.random()/5) - 0.1
						# 1-1 check
						list_links_coalitions[acted_upon_agent].agent2.belieftree[1 + coalitions.lead.unique_id][of_interest[1][best_action - len(cw_of_interest) - len(cw_of_interest)]][1] = \
							self.one_minus_one_check(list_links_coalitions[acted_upon_agent].agent2.belieftree[1 + coalitions.lead.unique_id][of_interest[1][best_action - len(cw_of_interest) - len(cw_of_interest)]][1])


					# Updating the resources of the team
					coalitions.resources[1] -= coalitions.resources[0]*0.1

					# Resources check
					if coalitions.resources[1] <= 0 * coalitions.resources[0]:
						break
	
	def new_link_ACF_as(self, link_list, outsider_agent, coalitions, ACF_link_list_as, ACF_link_list_as_total, ACF_link_id_as, len_DC, len_PC, len_S, conflict_level_coef):

		"""
		The new link function - ACF shadow network (agenda setting)
		===========================

		This function is used to create new links for the coalitions shadow
		networks. These links are obtained through looking at whichever
		member in the coalition has the highest awareness level for that agent.

		When creating a new link, the conflict level is also set along with the
		awareness decay. This is the agenda setting version of the function. 

		"""

		# First we look for the highest aware level
		team_aware = 0
		for agent_check_aware in coalitions.members:
			for links_check in link_list:
				if outsider_agent == links_check.agent1 and agent_check_aware == links_check.agent2:
					if links_check.aware > team_aware:
						team_aware = links_check.aware
				if outsider_agent == links_check.agent2 and agent_check_aware == links_check.agent1:
					if links_check.aware > team_aware:
						team_aware = links_check.aware
						# print(team_aware)

		# Second we calculate the conflict level
		# Note that the conflict level is only of interest for the issue advocated by the coalition leader (simplifying things)
		# The conflict level is calculated based on the beliefs of the whole coalition leader on the issue for state and aim
		conflict_level = [conflict_level_coef[1], conflict_level_coef[1]]
		for p in range(len_DC*len_PC + len_PC*len_S):
			conflict_level.append(conflict_level_coef[1])

		# Looking at the state and aim to calculate the conflict level
		check_none0 = 0
		if coalitions.lead.belieftree[1 + outsider_agent.unique_id][coalitions.issue][0] == None:
			coalitions.lead.belieftree[1 + outsider_agent.unique_id][coalitions.issue][0] = 0
			check_none0 = 1
		check_none1 = 0
		if coalitions.lead.belieftree[1 + outsider_agent.unique_id][coalitions.issue][1] == None:
			coalitions.lead.belieftree[1 + outsider_agent.unique_id][coalitions.issue][1] = 0
			check_none1 = 1
		
		state_cf_difference = abs(coalitions.lead.belieftree[1 + outsider_agent.unique_id][coalitions.issue][0] - coalitions.lead.belieftree[0][coalitions.issue][0])
		aim_cf_difference = abs(coalitions.lead.belieftree[1 + outsider_agent.unique_id][coalitions.issue][1] - coalitions.lead.belieftree[0][coalitions.issue][1])
		if check_none0 == 1:
			coalitions.lead.belieftree[1 + outsider_agent.unique_id][coalitions.issue][0] = None
		if check_none1 == 1:
			coalitions.lead.belieftree[1 + outsider_agent.unique_id][coalitions.issue][1] = None

		# State conflict level
		if state_cf_difference <= 0.25:
			conflict_level[0] = conflict_level_coef[0]
		if state_cf_difference > 0.25 and state_cf_difference <=1.75:
			conflict_level[0] = conflict_level_coef[2]
		if state_cf_difference > 1.75:
			conflict_level[0] = conflict_level_coef[1]
		
		# Aim conflict level
		if aim_cf_difference <= 0.25:
			conflict_level[1] = conflict_level_coef[0]
		if aim_cf_difference > 0.25 and aim_cf_difference <=1.75:
			conflict_level[1] = conflict_level_coef[2]
		if aim_cf_difference > 1.75:
			conflict_level[1] = conflict_level_coef[1]

		# Conflict level for the causal relations
		for p in range(len_DC*len_PC + len_PC*len_S):
			cw_difference = abs(coalitions.lead.belieftree[1 + outsider_agent.unique_id][len_DC + len_PC + len_S + p][0] - coalitions.lead.belieftree[0][len_DC + len_PC + len_S + p][0])
			if cw_difference <= 0.25:
				conflict_level[2+p] = conflict_level_coef[0]
			if cw_difference > 0.25 and cw_difference <=1.75:
				conflict_level[2+p] = conflict_level_coef[2]
			if cw_difference > 1.75:
				conflict_level[2+p] = conflict_level_coef[1]

		# Third we set the aware decay
		aware_decay = 0

		# Fifth we create the link
		coalition_link = PolicyNetworkLinks(ACF_link_id_as[0], coalitions, outsider_agent, team_aware, aware_decay, conflict_level)
		ACF_link_list_as.append(coalition_link)
		ACF_link_list_as_total.append(coalition_link)
		ACF_link_id_as[0] += 1

	def new_link_ACF_pf(self, link_list, outsider_agent, coalitions, ACF_link_list_pf, ACF_link_list_pf_total, ACF_link_id_pf, len_DC, len_PC, len_S, conflict_level_coef):

		"""
		The new link function - ACF shadow network (policy formulation)
		===========================

		This function is used to create new links for the coalitions shadow
		networks. These links are obtained through looking at whichever
		member in the coalition has the highest awareness level for that agent.

		When creating a new link, the conflict level is also set along with the
		awareness decay. This is the policy formulation version of the function. 

		"""

		# First we look for the highest aware level
		team_aware = 0
		for agent_check_aware in coalitions.members:
			for links_check in link_list:
				if outsider_agent == links_check.agent1 and agent_check_aware == links_check.agent2:
					if links_check.aware > team_aware:
						team_aware = links_check.aware
				if outsider_agent == links_check.agent2 and agent_check_aware == links_check.agent1:
					if links_check.aware > team_aware:
						team_aware = links_check.aware
						# print(team_aware)

		# Second we calculate the conflict level
		# Note that the conflict level is only of interest for the issue advocated by the coalition leader (simplifying things)
		# The conflict level is calculated based on the beliefs of the whole coalition leader on the issue for state and aim
		conflict_level = []
		conflict_level_init = [conflict_level_coef[1], conflict_level_coef[1]]
		for p in range(len_S):
			conflict_level.append(copy.copy(conflict_level_init))

		for p in range(len_DC*len_PC + len_PC*len_S):
			conflict_level.append(conflict_level_coef[1])

		# Looking at the state and aim to calculate the conflict level
		for p in range(len_S):
			check_none0 = 0
			if coalitions.lead.belieftree[1 + outsider_agent.unique_id][len_DC + len_PC + p][0] == None:
				coalitions.lead.belieftree[1 + outsider_agent.unique_id][len_DC + len_PC + p][0] = 0
				check_none0 = 1
			check_none1 = 0
			if coalitions.lead.belieftree[1 + outsider_agent.unique_id][len_DC + len_PC + p][1] == None:
				coalitions.lead.belieftree[1 + outsider_agent.unique_id][len_DC + len_PC + p][1] = 0
				check_none1 = 1
			state_cf_difference = abs(coalitions.lead.belieftree[1 + outsider_agent.unique_id][len_DC + len_PC + p][0] - coalitions.lead.belieftree[0][len_DC + len_PC + p][0])
			aim_cf_difference = abs(coalitions.lead.belieftree[1 + outsider_agent.unique_id][len_DC + len_PC + p][1] - coalitions.lead.belieftree[0][len_DC + len_PC + p][1])
			if check_none0 == 1:
				coalitions.lead.belieftree[1 + outsider_agent.unique_id][len_DC + len_PC + p][0] = None
			if check_none1 == 1:
				coalitions.lead.belieftree[1 + outsider_agent.unique_id][len_DC + len_PC + p][1] = None

			# State conflict level
			if state_cf_difference <= 0.25:
				conflict_level[p][0] = conflict_level_coef[0]
			if state_cf_difference > 0.25 and state_cf_difference <=1.75:
				conflict_level[p][0] = conflict_level_coef[2]
			if state_cf_difference > 1.75:
				conflict_level[p][0] = conflict_level_coef[1]
			
			# Aim conflict level
			if aim_cf_difference <= 0.25:
				conflict_level[p][1] = conflict_level_coef[0]
			if aim_cf_difference > 0.25 and aim_cf_difference <=1.75:
				conflict_level[p][1] = conflict_level_coef[2]
			if aim_cf_difference > 1.75:
				conflict_level[p][1] = conflict_level_coef[1]

		# Conflict level for the causal relations
		for p in range(len_DC*len_PC + len_PC*len_S):
			cw_difference = abs(coalitions.lead.belieftree[1 + outsider_agent.unique_id][len_DC + len_PC + len_S + p][0] - coalitions.lead.belieftree[0][len_DC + len_PC + len_S + p][0])
			if cw_difference <= 0.25:
				conflict_level[len_S+p] = conflict_level_coef[0]
			if cw_difference > 0.25 and cw_difference <=1.75:
				conflict_level[len_S+p] = conflict_level_coef[2]
			if cw_difference > 1.75:
				conflict_level[len_S+p] = conflict_level_coef[1]

		# Third we set the aware decay
		aware_decay = 0

		# Fifth we create the link
		coalition_link = PolicyNetworkLinks(ACF_link_id_pf[0], coalitions, outsider_agent, team_aware, aware_decay, conflict_level)
		ACF_link_list_pf.append(coalition_link)
		ACF_link_list_pf_total.append(coalition_link)
		ACF_link_id_pf[0] += 1

	def knowledge_exchange_coalition(self, team, cw_knowledge, parameter):

		"""
		Knowledge exchange function - coalitions
		===========================

		This function is used for the exchange of partial knowledge between agents
		within the same coalition. This only regards the issue that is selected by the
		coalition and is kept with a certain amount of randomness.
		
		"""

		# Exchange of partial knowledge between the agents in the team
		for agent_exchange1 in team.members:
			for agent_exchange2 in team.members:
				# Actual knowledge exchange with a randomness of 0.2
				# print('Before: ' + str(agent_exchange1.belieftree[1 + agent_exchange2.unique_id][team.issue][0]))
				agent_exchange1.belieftree[1 + agent_exchange2.unique_id][cw_knowledge][parameter] = \
				  agent_exchange2.belieftree[0][cw_knowledge][0] + (random.random()/5) - 0.1
				# print('After: ' + str(agent_exchange1.belieftree[1 + agent_exchange2.unique_id][team.issue][0]))
				# 1-1 check
				if agent_exchange1.belieftree[1 + agent_exchange2.unique_id][cw_knowledge][parameter] > 1:
					agent_exchange1.belieftree[1 + agent_exchange2.unique_id][cw_knowledge][parameter] = 1
				if agent_exchange1.belieftree[1 + agent_exchange2.unique_id][cw_knowledge][parameter] < -1:
					agent_exchange1.belieftree[1 + agent_exchange2.unique_id][cw_knowledge][parameter]  = -1

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
