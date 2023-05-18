from agent.base import create_pandas_and_matplotlib_dataframe_agent
from langchain.llms import OpenAI
import pandas as pd
import os
import supabase
import uuid
from dotenv import load_dotenv
import io
from utils import save_file
from lanarky.responses import StreamingResponse

df = pd.read_csv('hi_2019.csv', encoding='ISO-8859-1')
llm=OpenAI(temperature=0)
plt = None

agent = create_pandas_and_matplotlib_dataframe_agent(llm, df, plt, verbose=True)
answer = agent.run("What is the perception of corruption like in each country?")

# If answer is an image filename, upload it to Supabase Storage
if answer.endswith('.png'):
    url = save_file(answer)
    print(url)
