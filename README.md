# Alexa Notion Integration using Langchain Agent and Zapier NLA

This project connects Alexa to Notion using Langchain Agent and Zapier NLA to manipulate a Notion database. The original goal was to add information to a Notion database called "Activities" dynamically through Alexa. The interactive model JSON file is included, but the skill will still need to be set up, and the endpoint will need to be updated to point to your ngrok server address.

## Prerequisites

- Python 3.6 or higher
- Flask
- Pyngrok
- An Amazon Developer account to create an Alexa Skill
- A Notion account with a database named "Activities"
- A Zapier account for connecting Notion API and configuring NLA
- OpenAI API key
- Zapier NLA API key

## Setup

1. Clone the repository:

```bash
git clone https://github.com/yourusername/alexa-notion-integration.git
cd alexa-notion-integration
```

2. Create a virtual environment and install the required packages:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Set up your environment variables:

```
export OPENAI_API_KEY="your_openai_api_key"
export ZAPIER_NLA_API_KEY="your_zapier_nla_api_key"
```

4. Run the Flask server:

```
python app.py
```

5. Create an Alexa Skill on the Amazon Developer Console:
   - Use the Amazon Developer Console to create an Alexa Skill.
   - Set the skill's invocation name.
   - Add the required intents and slots, such as UpdateNotionIntent and Text.-
   - Import the included interactive model JSON file.
   - Set up the endpoint for the skill using the ngrok URL provided when you run the Flask server (e.g., https://your_ngrok_url/process_text).
6. Save and build your skill.

- Use the Amazon Developer Console or an Alexa-enabled device to test the skill.
- Invoke the skill and provide input to add information to the Notion database

# Troubleshooting

If you encounter issues, make sure that:

- Your environment variables are set correctly.
- Your Notion database is set up properly.
- Your Zapier account is connected to the Notion API and configured for NLA.
- Your Alexa Skill is set up correctly with the correct intents, slots, and endpoint.
  If you still face issues, refer to the error logs or open an issue on the GitHub repository.

# Contributing

Feel free to fork the repository, make changes, and submit a pull request if you think your changes can improve the project.
