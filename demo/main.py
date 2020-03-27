import requests
from flask import Flask, render_template, request, abort
application = Flask(__name__)


@application.route('/', methods=['GET', 'POST'])
def home():
    agent_token = None
    agent_role = None
    server_name = 'surfly.com'
    if request.args.get('s3', ''):
        server_name = 'surfly-s3.com'
    if request.method == 'POST':
        api_key = request.form.get('api_key')
        agent_id = request.form.get('agent_id')

        if (
            not api_key or
            not agent_id or
            not api_key.strip().isalnum() or
            not agent_id.strip().isdigit()
        ):
            return 'Please enter your REST key and the agent_id', 400

        api_key = api_key.strip()
        agent_id = int(agent_id.strip())

        resp = requests.post(
            'https://%s/v2/agents/access-token/?api_key=%s' % (server_name, api_key),
            verify=True,
            json={
                "agent_id": agent_id,
            }
        )

        if resp.status_code != 200:
            return 'API error', 400

        resp_data = resp.json()
        agent_token = resp_data['agent_token']
        agent_role = resp_data.get('agent_role')

    return render_template(
        'home.html',
        agent_token=agent_token,
        agent_role=agent_role,
        server_name=server_name,
    )

