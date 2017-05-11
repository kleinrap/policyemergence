import pandas as pd
import matplotlib.pyplot as plt
import ast

df = pd.read_csv('2_agents_B_0.csv')


# Getting all beliefs on agent 19 Aim DC1

agent19 = []
agent20 = []
agent21 = []
agent22 = []
issue = 7
parameter = 2
for index, row in df.iterrows():
	if row['AgentID'] == 5:
		# print('   ')
		test1 = row['Belieftree']
		# print(test1)
		# evals turns the string back into an array/list
		test2 = eval(test1)
		# print(type(test1))
		# print(test2[1])
		agent19.append(test2[issue][parameter])
	if row['AgentID'] == 6:
		test4 = row['Belieftree']
		# evals turns the string back into an array/list
		test5 = eval(test4)
		# print(type(test1))
		# print(test2[1])
		agent20.append(test5[issue][parameter])
	if row['AgentID'] == 7:
		# print('   ')
		test1 = row['Belieftree']
		# evals turns the string back into an array/list
		test2 = eval(test1)
		# print(type(test1))
		# print(test2[1])
		agent21.append(test2[issue][parameter])
	if row['AgentID'] == 8:
		test4 = row['Belieftree']
		# evals turns the string back into an array/list
		test5 = eval(test4)
		# print(type(test1))
		# print(test2[1])
		agent22.append(test5[issue][parameter])

# print(agent19)

plt.plot(agent19, linewidth=2.0)
plt.plot(agent20)
plt.plot(agent21)
plt.plot(agent22)
plt.show()