from ast import Pass
import imp
import datetime
import uuid
import json

from sqlalchemy import delete
from ..base import BaseHandler
from .models import (RealtimeReportProject, RealtimeReportSetting)
from http import HTTPStatus
from utils.config import config
from tornado import gen


class RealtimeReportSearchHandler(BaseHandler):

    @gen.coroutine
    def post(self, *args, **kwargs):
        pass


class RealtimeReportGetHandler(BaseHandler):

    @gen.coroutine
    def post(self, *args, **kwargs):
        pass


class RealtimeReportDeleteHandler(BaseHandler):

    @gen.coroutine
    def post(self, *args, **kwargs):
        pass


class RealtimeReportCreateHandler(BaseHandler):

    @gen.coroutine
    def post(self, *args, **kwargs):
        pass


class RealtimeReportUpdateHandler(BaseHandler):

    @gen.coroutine
    def post(self, *args, **kwargs):
        pass


class RealtimeReportListGetHandler(BaseHandler):

    @gen.coroutine
    def post(self, *args, **kwargs):
        pass


class RealtimeReportViewCallCenterHandler(BaseHandler):
    """This function calculate and show data to CPM"""

    @gen.coroutine
    def post(self):
        pass

    def number_of_total_call(self):
        """Outputs the total number of calls for each business (call + pending + number of waiting calls)."""
        pass

    def during_call(self):
        """Outputs the number of calls during a call for each business."""
        pass

    def number_call_on_hold(self):
        """Outputs the number of calls which is on hold for each call center."""
        pass

    def number_of_waiting_call(self):
        """Outputs the number of calls in the waiting call status for each job (the end user is waiting for a user response).
         It is the target of threshold display."""
        pass

    def number_of_incoming_call(self):
        """Outputs the number of calls received by the user for skill incoming calls for each job."""
        pass

    def number_of_response(self):
        """Outputs the number of calls answered by the user for each business."""
        pass

    def number_of_hold(self):
        """Outputs the number of times the user has been put on hold for each business.
         If one call is put on hold multiple times, the number of times is counted."""
        pass

    def number_of_abandoned_calls(self):
        """Output the number of disconnected calls before the user for each job answers."""
        pass

    def number_of_compulsion_cutting(self):
        """Outputs the number of calls that were forcibly disconnected by the system for each business."""
        pass

    def response_rate(self):
        """Outputs the value calculated by the number of responses / the number of incoming calls for each business."""
        pass

    def abandonment_rate(self):
        """Outputs the value calculated by the number of abandoned calls / the number of incoming calls for each business."""
        pass

    def number_of_sla_response(self):
        """Outputs the number of calls answered within the SLA time for each job."""
        pass

    def sla_response_rate(self):
        """Outputs the value calculated by the number of SLA responses / the number of responses for each job. 
        (Of the number of responses, the number of calls answered within the SLA time)"""
        pass

    def average_call_duration(self):
        """Outputs the value calculated by the total talk time / number of responses for each business."""
        pass

    def maximum_waiting_time(self):
        """Outputs the maximum value of the waiting time for each job (the time that the end user waits for the user's response)"""
        pass

    def average_hold_time(self):
        """Outputs the value calculated by the total hold time / number of holds for each job."""
        pass

class RealtimeReportViewUserHandler(BaseHandler):

    def get_user_info(self):
        """Output the extension number used by the target user.
            Info: extensions of user, username, userID"""
        pass

    def get_user_state(self):
        """Output the status of the target user. (Acceptable, post-processing, leaving (displaying the details of leaving),
         calling, pending)"""
        pass

    def get_elapsed_time(self):
        """Outputs the elapsed time since the target user became the current status.
            It is the target of threshold display."""
        pass

    def number_of_response(self):
        """Outputs the number of calls answered by the target user."""
        pass

    def number_of_hold(self):
        """Output the number of times the target user has been put on hold.
            If one call is put on hold multiple times, the number of times is counted."""
        pass

    def average_call_duration(self):
        """Output the average talk time for each user. It is necessary to calculate the value considering both incoming and outgoing calls."""
        pass

    def average_response_time(self):
        """Output the value calculated by the total response time / number of responses for each user."""
        pass

    def average_post_processing(self):
        """Output the average post-processing time for each user.
        It is necessary to calculate the value considering both incoming and outgoing calls.
        """
        pass

    def average_time(self):
        """Output the average of "answer time + talk time + hold time + post-processing time".
        Outputs the value calculated by (response time + call time + hold time + post-processing time) / number of responses for each user.
        Response time = time from incoming call to user response"""
        pass
    
    def direction_of_telephone(self):
        """Incoming | outcoming"""
        pass

    def destination_phone_number(self):
        """"Destination phone number
        Output the telephone number of the other party. It will be blank when you are not on a call."""
        pass

    def number_of_outgoing_call(self):
        """Outputs the number of calls made by the target user."""
        pass

    def number_of_forwarding(self):
        pass

    def number_of_forwarding_response(self):
        pass
