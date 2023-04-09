import os
from flask import Flask, request, jsonify
from langchain.llms import OpenAI
from langchain.agents import initialize_agent
from langchain.agents.agent_toolkits import ZapierToolkit
from langchain.agents import AgentType
from langchain.utilities.zapier import ZapierNLAWrapper

os.environ["OPEN_API_KEY"] = os.environ.get("OPEN_API_KEY", "")
os.environ["ZAPIER_NLA_API_KEY"] = os.environ.get("ZAPIER_NLA_API_KEY", "")

llm = OpenAI(temperature=0)
zapier = ZapierNLAWrapper()
toolkit = ZapierToolkit.from_zapier_nla_wrapper(zapier)
agent = initialize_agent(toolkit.get_tools(), llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

app = Flask(__name__)

@app.route('/process_text', methods=['POST'])
def process_text():
    input_text = request.json.get('text', '')
    if not input_text:
            return jsonify({'error': 'No text provded'}), 400

    result = agent.run(input_text)
    return jsonify({'result': result})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)