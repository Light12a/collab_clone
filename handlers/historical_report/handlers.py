import imp
import datetime
import uuid
import json

from sqlalchemy import delete
from ..base import BaseHandler
from .models import (HistoricalReportCallCols, HistoricalReportCcCols, HistoricalReportGroup, HistoricalReportProjects,
                     HistoricalReportSetting, HistoricalReportSkill, HistoricalReportSkillColsSetting, HistoricalReportUser, HistoricalReportUserCols)
from http import HTTPStatus
from utils.config import config
from tornado import gen


class HistoricalReportSearchHandler(BaseHandler):

    @gen.coroutine
    def post(self, *args, **kwargs):
        pass


class HistoricalReportGetHandler(BaseHandler):

    @gen.coroutine
    def post(self, *args, **kwargs):
        pass


class HistoricalReportDeleteHandler(BaseHandler):

    @gen.coroutine
    def post(self, *args, **kwargs):
        pass


class HistoricalReportCreateHandler(BaseHandler):

    @gen.coroutine
    def post(self, *args, **kwargs):
        pass


class HistoricalReportUpdateHandler(BaseHandler):

    @gen.coroutine
    def post(self, *args, **kwargs):
        pass


class HistoricalReportTabulatedGetHandler(BaseHandler):

    @gen.coroutine
    def post(self, *args, **kwargs):
        pass


class HistoricalReportTabulatedCSVHandler(BaseHandler):

    @gen.coroutine
    def post(self, *args, **kwargs):
        pass


class HistoricalReportListGetHandler(BaseHandler):

    @gen.coroutine
    def post(self, *args, **kwargs):
        pass


class HistoricalReportViewCallCenterHandler(BaseHandler):

    @gen.coroutine
    def post(self, *args, **kwargs):
        pass

    def response_rate(self):
        """Output the response rate.
        The value calculated by ""Number of answered calls / Number of incoming calls"" is output."""
        pass

    def abandoned_rate(self):
        """Output the abandonment rate.
        Output the value calculated by "Number of abandoned calls / Number of incoming calls"."""
        pass

    def number_of_SLA_response(self):
        """Outputs the number of calls answered in the SLA set for each job."""
        pass

    def sla_response_rate(self):
        """Output the SLA response rate.
        Output the value calculated by ""SLA response rate / number of response calls""."""
        pass

    def number_of_imcoming_call(self):
        """Outputs the number of incoming calls to business."""
        pass

    def skill_incoming_call_count(self):
        """The skill is received, the user answers, and the number of calls for which post-processing is completed is output.
        After receiving the skill"""
        pass

    def number_of_answer_call(self):
        """ Outputs the number of calls answered by the user among the calls received in the business.
        Includes ""waiting answer count""."""
        pass

    def number_of_waiting_call(self):
        """Outputs the number of calls in the waiting call status for each job (the end user is waiting for a user response).
        It is the target of threshold display."""
        pass

    def number_of_abandoned_call(self):
        """Output the number of disconnected calls before the user for each job answers."""
        pass

    def number_of_compulsion_cutting(self):
        """A call received from the end user (customer) to the call center (business) becomes a waiting call, and the call that was forcibly disconnected by the system."""
        pass

    def number_of_hold(self):
        """Outputs the number of times the user has been put on hold during a call.
        If one call is held multiple times, the number of times is counted."""
        pass

    def average_hold_time(self):
        """Output the value calculated by the total hold time / number of holds for each business."""
        pass

    def maximum_hold_time(self):
        """Outputs the maximum hold time for each job."""
        pass

    def total_hold_time(self):
        """Output the total hold time for each job."""
        pass

    def average_of_response_time(self):
        """Response time = time from incoming call to user response
        Outputs the value calculated by the total response time / number of response calls for each job."""
        pass

    def maximum_response_time(self):
        """Outputs the maximum response time for each job."""
        pass

    def average_abandonment_time(self):
        """Abandonment time = Time from incoming call to abandonment (end user disconnects or forcibly disconnects from system)
        Outputs the value calculated by the total abandoned time / number of abandoned calls for each business."""
        pass

    def maximum_abandonment_time(self):
        """Output the maximum value of abandonment time for each business."""
        pass

    def average_talk_time(self):
        """Talk time = time from user answer to disconnection
        Outputs the value calculated by the total call time / number of calls for each business."""
        pass

    def maximum_talk_time(self):
        """Outputs the maximum value of talk time for each business."""
        pass

    def total_talk_time(self):
        """Outputs the total value of talk time for each business."""
        pass

    def correspondence_memo(self):
        pass


class HistoricalReportViewUserHandlers(BaseHandler):

    def post(self):
        pass

    def user_info(self):
        pass

    def outgoing_number_of_sending(self):
        """Outputs the number of calls made by the user.
        It is the same value as the number of (calling) calls + the number of (calling) non-answers."""
        pass

    def outgoing_number_of_answer_call(self):
        """Outputs the number of calls made by the user and answered by the other party."""
        pass

    def outgoing_number_of_no_answer_call(self):
        """Outputs the number of calls made by the user and not answered by the other party.
        Announcements such as unused phone numbers are also subject to non-response."""
        pass

    def outgoing_number_of_hold(self):
        """Outputs the number of times the call was put on hold for the call made by the user."""
        pass

    def outgoing_average_hold_time(self):
        """For the call made by the user, the value calculated by the total hold time / number of holds is output."""
        pass

    def outgoing_maximum_hold_time(self):
        """Outputs the maximum hold time for calls made by the user."""
        pass

    def outgoing_total_hold_time(self):
        """Outputs the total hold time for calls made by the user."""
        pass

    def outgoing_average_post_processing_time(self):
        """For post-processing after transmission, the value calculated by the total post-processing time / number of post-processing is output."""
        pass

    def outgoing_maximum_post_processing_time(self):
        pass

    def outgoing_total_post_processing_time(self):
        pass

    def outgoing_average_talk_time(self):
        """Outputs the maximum call duration for calls made by the user."""
        pass

    def outgoing_maximum_talk_time(self):
        pass

    def outgoing_total_talk_time(self):
        pass

    def outgoing_number_of_forwarding(self):
        pass

    def outgoing_number_of_forwarding_responsed(self):
        pass

    def incoming_number_of_arriving(self):
        """Output the number of incoming calls to the user.
        It becomes the same value as the number of (arrival) response + (arrival) non-response."""
        pass

    def incoming_number_of_response(self):
        pass

    def incoming_number_of_no_response(self):
        pass

    def incoming_number_of_hold(self):
        pass

    def incoming_total_reception_time(self):
        """Outputs the total value of the user's available hours."""
        pass

    def incoming_total_post_processing_time(self):
        pass

    def incoming_average_post_processing_time(self):
        pass

    def incoming_maximum_average_post_processing_time(self):
        pass

    def total_leave_seat_time(self):
        pass

    def average_leave_seat_time(self):
        pass

    def content_leave_seat_time(self):
        pass

    def total_login_time(self):
        """Outputs the total login time of the user.
        The management screen is not included in the login time recording target, but softphones, browser phones, and hardphones are targeted."""
        pass
    
    def incoming_average_response_time(self):
        """Total value of user's acceptable time Outputs the value calculated by the maximum response time / number of responses to the call received by the user is output."""
        pass

    def incoming_maximum_response_time(self):
        """Outputs the maximum response time for incoming calls to the user."""
        pass

    def incoming_maximum_no_response_time(self):
        """Outputs the maximum non-answer time for incoming calls to the user."""
        pass

    def incoming_average_talk_time(self):
        """Output the value calculated by total talk time/number of responses for incoming calls to the user."""
        pass

    def incoming_maximum_talk_time(self):
        pass

    def incoming_total_talk_time(self):
        pass

    def incoming_number_of_forwarding(self):
        pass

    def incoming_number_of_forwarding_responsed(self):
        pass

    def total_monitor_time(self):
        pass

    def total_coach_time(self):
        pass

    def incoming_average_hold_time(self):
        """For the call received by the user, the value calculated by the total hold time / number of holds is output."""
        pass

    def incoming_maximum_hold_time(self):
        pass

    def incoming_total_hold_time(self):
        pass

    def incoming_correspondence_memo(self):
        pass


class HistoricalReportViewSkill(BaseHandler):

    def post(self):
        pass

    def skill_info(self):
        pass

    def number_of_arriving(self):
        pass

    def number_of_response(self):
        pass

    def number_of_no_response(self):
        pass

    def average_response_time(self):
        pass

    def maximum_response_time(self):
        pass

    def maximum_non_response_time(self):
        pass

    def average_talk_time(self):
        pass

    def maximum_talk_time(self):
        pass

    def total_talk_time(self):
        pass

    def average_post_processing_time(self):
        pass

    def maximum_post_processing_time(self):
        pass

    def average_hold_time(self):
        pass

    def maximum_hold_time(self):
        pass


class HistoricalReportViewCallRecords(BaseHandler):

    def post(self):
        pass

    def get_data(self):
        pass