from agent.base import create_pandas_and_matplotlib_dataframe_agent
from langchain.llms import OpenAI
from langchain.callbacks.base import BaseCallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

from dotenv import load_dotenv
from utils import save_file
import threading
import queue

from flask import Flask, request, jsonify, Response
import pandas as pd
import matplotlib
matplotlib.use('agg')

load_dotenv()
app = Flask(__name__)

df = pd.read_csv('hi_2019.csv', encoding='ISO-8859-1')
plt = None

@app.route('/')
def index():
    return Response('''
<!DOCTYPE html>
<html>
<head><title>Flask Streaming Langchain Example</title></head>
<body>
    <input style="width:100%;" id="prompt" value="What is the perception of corruption like in each country?" />
    <div id="output"></div>
    <script>
        const outputEl = document.getElementById('output');
        const promptInput = document.getElementById('prompt');

        async function sendPrompt() {
            const prompt = promptInput.value;
            try {
                const response = await fetch('/chain', {
                    method: 'POST',
                    body: prompt
                });
                const reader = response.body.getReader();
                const decoder = new TextDecoder();
                while (true) {
                    const { done, value } = await reader.read();
                    if (done) { break; }
                    const decoded = decoder.decode(value, { stream: true });
                    if (decoded.trim().startsWith('https://')) {
                        // Display the image
                        outputEl.innerHTML += `<img src="${decoded}" />`;
                    } else {
                        // Append regular text to the output element
                        outputEl.innerText += decoded;
                    }
                }
            } catch (err) {
                console.error(err);
            }
        }

        promptInput.addEventListener('keypress', function (e) {
            if (e.key === 'Enter') {
                sendPrompt();
            }
        });
    </script>
</body>
</html>
''', mimetype='text/html')

class ThreadedGenerator:
    def __init__(self):
        self.queue = queue.Queue()

    def __iter__(self):
        return self

    def __next__(self):
        item = self.queue.get()
        if item is StopIteration: raise item
        return item

    def send(self, data):
        self.queue.put(data)

    def close(self):
        self.queue.put(StopIteration)


class ChainStreamHandler(StreamingStdOutCallbackHandler):
    def __init__(self, gen):
        super().__init__()
        self.gen = gen

    def on_llm_new_token(self, token: str, **kwargs):
        self.gen.send(token)

def llm_thread(g, prompt):
    try:
        llm = OpenAI(
            verbose=True,
            streaming=True,
            callbacks=[StreamingStdOutCallbackHandler(), ChainStreamHandler(g)],
            temperature=0,
        )
        agent = create_pandas_and_matplotlib_dataframe_agent(llm, df, plt)
        answer = agent.run(prompt)
        
        if answer.endswith('.png'):
            url = save_file(answer)
            g.send('\n' + url)
    finally:
        g.close()


def chain(prompt):
    g = ThreadedGenerator()
    threading.Thread(target=llm_thread, args=(g, prompt)).start()
    return g


@app.route('/chain', methods=['POST'])
def _chain():
    prompt = request.data.decode('utf-8')
    return Response(chain(prompt), mimetype='text/plain')

if __name__ == '__main__':
    app.run(threaded=True, debug=True)