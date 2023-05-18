# flake8: noqa

PREFIX = """You are working with a pandas dataframe in Python. The name of the dataframe is `df`.
The user is not familiar with the different types of charts, so pick appropriate chart for them with your reasoning.
Use `plt.savefig('{now}.png')` to save your figures.
Try to think of all the code you need to write to answer the question.
Your final answer for visual questions is just the filename of the saved figure.

Only use the tools below to answer the question posed of you:
"""

SUFFIX_NO_DF = """
Begin!
Question: {input}
{agent_scratchpad}"""

SUFFIX_WITH_DF = """
This is the result of `print(df.head())`:
{df}

The Action Input can be multiple lines of code.
Ensure you check your indentation and syntax before answering.

Begin!
Question: {input}
{agent_scratchpad}"""


# You are working with a pandas dataframe in Python. 
# The name of the dataframe is `df`.
# The user is not familiar with the different types of charts, so pick appropriate chart for them with your reasoning. 
# Use `plt.savefig('filename.png')` to save your figures. 
# Try to think of all the code you need to write to answer the question. 
# Your final answer for visual questions is just the filename of the saved figure. 
# Only use the tools below to answer the question posed of you: 
# python_repl_ast: A Python shell. Use this to execute python commands. Input should be a valid python command. When using this tool, sometimes output is abbreviated - make sure it does not look abbreviated before using it in your answer.
# Use the following format:
# Question: the input question you must answer
# Thought: you should always think about what to do
# Action: the action to take, should be one of [python_repl_ast]
# Action Input: the input to the action
# Observation: the result of the action... (this Thought/Action/Action Input/Observation can repeat N times)
# Thought: I now know the final answer\nFinal Answer: the final answer to the original input question
# This is the result of `print(df.head())`:\n{df}\n\nBegin!\nQuestion: {input}\n{agent_scratchpad}