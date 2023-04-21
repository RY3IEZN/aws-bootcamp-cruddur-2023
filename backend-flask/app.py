from flask import Flask
from flask import request, redirect, jsonify, abort

from flask_cors import CORS, cross_origin
import os

from services.home_activities import *
from services.notifications_activities import *
from services.user_activities import *
from services.create_activity import *
from services.create_reply import *
from services.search_activities import *
from services.message_groups import *
from services.messages import *
from services.create_message import *
from services.show_activity import *

from lib.coginto_token_verification import CognitoTokenVerification, extract_access_token, TokenVerifyError

#Rollbar for error monitoring
import rollbar
import rollbar.contrib.flask
from flask import got_request_exception

# honeycomb tracing
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Initialize tracing and an exporter that can send data to Honeycomb
provider = TracerProvider()
processor = BatchSpanProcessor(OTLPSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

app = Flask(__name__)
frontend = os.getenv('FRONTEND_URL')
backend = os.getenv('BACKEND_URL')
origins = [frontend, backend]
cors = CORS(app,
            resources={r"/api/*": {
                "origins": origins
            }},
            headers=['Content-Type', 'Authorization'],
            expose_headers='Authorization',
            methods="OPTIONS,GET,HEAD,POST")
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()


# rollbar
@app.before_first_request
def init_rollbar():
    """init rollbar module"""
    rollbar.init(
        # access token
        '5a6443e7544d49bb9a4369ff397d6ab6',
        # environment name
        'production',
        # server root directory, makes tracebacks prettier
        root=os.path.dirname(os.path.realpath(__file__)),
        # flask already sets up logging
        allow_logging_basic_config=False)

    # send exceptions from `app` to rollbar, using flask's signal system.
    got_request_exception.connect(rollbar.contrib.flask.report_exception, app)


## Simple flask app
@app.route('/rollbar/test')
def rollbar_test():
    rollbar.report_message('Hello World!', 'warning')
    return "Hello World!"


# rollbar end

cognito_token_verification = CognitoTokenVerification(
    user_pool_id=os.getenv("AWS_COGNITO_USER_POOL_ID"),
    user_pool_client_id=os.getenv("AWS_COGNITO_USER_POOL_CLIENT_ID"),
    region=os.getenv("AWS_DEFAULT_REGION"))


# main app
@app.route("/api/message_groups", methods=['GET'])
def data_message_groups():
    access_token = extract_access_token(request.headers)
    app.logger.debug("ratatat")
    app.logger.debug(request.headers.get("Authorization"))

    try:
        claims = cognito_token_verification.verify("eyJraWQiOiI4ZzNMWlVPY0xIXC9XWVhiYjltVTdZcGx2SVlNcFNDb0pxa21nWU1MWEtkdz0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJjZTFmMmJmNS1lMDc4LTRjOTItOGQwMy01YTgxYmRlNzZjNWIiLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAuZXUtd2VzdC0yLmFtYXpvbmF3cy5jb21cL2V1LXdlc3QtMl9Ja212MjNZZVEiLCJjbGllbnRfaWQiOiIzdXVmZzZkYmppcGs2b2ZpMTNkcmxvdTUycyIsIm9yaWdpbl9qdGkiOiIxM2ExYzVlMy1jM2M5LTQ4ZDctYTdkZi04MDkwNTgyZWVhNGYiLCJldmVudF9pZCI6ImM5ODYwM2QzLTY0MmItNDMwYi1hY2VmLWYzZjkzNjQ2ZjRiNSIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiYXdzLmNvZ25pdG8uc2lnbmluLnVzZXIuYWRtaW4iLCJhdXRoX3RpbWUiOjE2ODIwMDA1MDAsImV4cCI6MTY4MjAwNDEwMCwiaWF0IjoxNjgyMDAwNTAwLCJqdGkiOiI0MWJhYWZjNy0zODE5LTQyODktYjJkNS1lOTQ0MjI2Y2I1MDYiLCJ1c2VybmFtZSI6ImNlMWYyYmY1LWUwNzgtNGM5Mi04ZDAzLTVhODFiZGU3NmM1YiJ9.OMkyrCR7klYjtpnzQE6nrwLcMqlGDTaBi4RaQogysjydQ2WisXls34fGN5FDVneHTjkhYiFTXX5VEfeVqA_pykH6FVmNf4OcYoe5EJl2zz6myVvpqyoq8_PS0jHt4otyhko2URH8B8MZ-I3_clcJbS25YTGqQYKkZhQMQ1J8Fbcg-ab9F7eXDEBgd-KHJs8S9eQ3-fATIfQDuUZJCPk3QAcRxHHiZ_vQI5GCCZ4pSCK_9R8thFwgs5QOuQYdBXKAHrqoXgrN1OWK8_4od5wy6GLM_gzW0hxDL4cE5jqATVZwh5m2rfKbOkUFmYi1ai4f_pCGLkqDJMWTHiltyNeODw")
        app.logger.debug(claims)
        cognito_user_id = claims['sub']
        app.logger.debug("aaaaaaaaaaaaaaaaaa")
        app.logger.debug(cognito_user_id)
        app.logger.debug("aaaaaaaaaaaaaaaaaaa")
        
        model = MessageGroups.run(cognito_user_id=cognito_user_id)
        if model['errors'] is not None:
            return model['errors'], 422
        else:
            return model['data'], 200
    except TokenVerifyError as e:
        app.logger.debug(e)
        return {}, 401


@app.route("/api/messages/@<string:handle>", methods=['GET'])
def data_messages(handle):
    user_sender_handle = 'andrewbrown'
    user_receiver_handle = request.args.get('user_reciever_handle')

    model = Messages.run(user_sender_handle=user_sender_handle,
                         user_receiver_handle=user_receiver_handle)
    if model['errors'] is not None:
        return model['errors'], 422
    else:
        return model['data'], 200
    return


@app.route("/api/messages", methods=['POST', 'OPTIONS'])
@cross_origin()
def data_create_message():
    user_sender_handle = 'andrewbrown'
    user_receiver_handle = request.json['user_receiver_handle']
    message = request.json['message']

    model = CreateMessage.run(message=message,
                              user_sender_handle=user_sender_handle,
                              user_receiver_handle=user_receiver_handle)
    if model['errors'] is not None:
        return model['errors'], 422
    else:
        return model['data'], 200
    return


@app.route('/api/health-check')
def health_check():
    return {'success': True}, 200


@app.route("/api/activities/home", methods=['GET'])
def data_home():
    access_token = extract_access_token(request.headers)
    try:
        claims = cognito_token_verification.verify(access_token)
        app.logger.debug(claims)
        data = HomeActivities.run(cognito_user_id=claims['username'])
    except TokenVerifyError as e:
        data = HomeActivities.run()
    return data, 200


@app.route("/api/activities/notifications", methods=['GET'])
# @aws_auth.authentication_required
def data_notifications():
    data = NotificationsActivities.run()
    return data, 200


@app.route("/api/activities/@<string:handle>", methods=['GET'])
def data_handle(handle):
    model = UserActivities.run(handle)
    if model['errors'] is not None:
        return model['errors'], 422
    else:
        return model['data'], 200


@app.route("/api/activities/search", methods=['GET'])
def data_search():
    term = request.args.get('term')
    model = SearchActivities.run(term)
    if model['errors'] is not None:
        return model['errors'], 422
    else:
        return model['data'], 200
    return


@app.route("/api/activities", methods=['POST', 'OPTIONS'])
@cross_origin()
def data_activities():
    user_handle = 'andrewbrown'
    message = request.json['message']
    ttl = request.json['ttl']
    model = CreateActivity.run(message, user_handle, ttl)
    if model['errors'] is not None:
        return model['errors'], 422
    else:
        return model['data'], 200
    return


@app.route("/api/activities/<string:activity_uuid>", methods=['GET'])
def data_show_activity(activity_uuid):
    data = ShowActivity.run(activity_uuid=activity_uuid)
    return data, 200


@app.route("/api/activities/<string:activity_uuid>/reply",
           methods=['POST', 'OPTIONS'])
@cross_origin()
def data_activities_reply(activity_uuid):
    user_handle = 'andrewbrown'
    message = request.json['message']
    model = CreateReply.run(message, user_handle, activity_uuid)
    if model['errors'] is not None:
        return model['errors'], 422
    else:
        return model['data'], 200
    return


if __name__ == "__main__":
    app.run(debug=True)
