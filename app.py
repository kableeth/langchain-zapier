import os
import logging
import json
from pprint import pprint
from pyngrok import ngrok
from flask import Flask, request, jsonify

#Alexa Skill Libraries
import ask_sdk_core.utils as ask_utils
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_model import RequestEnvelope
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response

#langchain Libraries
from langchain.llms import OpenAI
from langchain.agents import initialize_agent
from langchain.agents.agent_toolkits import ZapierToolkit
from langchain.agents import AgentType
from langchain.utilities.zapier import ZapierNLAWrapper

#no idea what this is for
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

#needed for local server hosting
http_tunnel = ngrok.connect(5000) 

#get env vars
os.environ["OPEN_API_KEY"] = os.environ.get("OPEN_API_KEY", "")
os.environ["ZAPIER_NLA_API_KEY"] = os.environ.get("ZAPIER_NLA_API_KEY", "")

#Init llm & zapier connect to Notion
llm = OpenAI(temperature=0)
zapier = ZapierNLAWrapper()
toolkit = ZapierToolkit.from_zapier_nla_wrapper(zapier)
agent = initialize_agent(toolkit.get_tools(), llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

#Handlers for Alexa responses
class UpdateNotionIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("UpdateNotionIntent")(handler_input)

    def handle(self, handler_input):
         #send to Zapier & Notion
        agent.run("Add Buy new Shoes as a task")
        speak_output = "Shoes have been added!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )
class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response
class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

#init app
app = Flask(__name__)

sb = SkillBuilder()
sb.add_request_handler(UpdateNotionIntentHandler())
sb.add_exception_handler(CatchAllExceptionHandler())

#ROUTES
@app.route('/process_text', methods=['POST'])
def process_text():
    print('before SkillBuilder')
    payload = request.json

    skill = sb.create()
    request_envelope = skill.serializer.deserialize(payload=json.dumps(payload), obj_type=RequestEnvelope)
    response_envelope = skill.invoke(request_envelope=request_envelope, context=None)
    response = skill.serializer.serialize(response_envelope)

    return jsonify(response)

#Init App
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)