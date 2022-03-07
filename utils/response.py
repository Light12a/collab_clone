from tornado.web import Finish

class ResponseMixin(object):
    """
    TODO: add a compat layer between the request handler and the response
    mixin class which will serialize API response values
    to the requested Content-Type value. Currently we ignore content type
    and always return json.
    """

    def raw_response(self, response_string, status_code=200):

        self.clear_header("Content-Type")
        self.set_status(status_code)
        self.flush()
        self.write(response_string)
        self.finish()

    def write_response(self,
                       status,
                       response_data=None,
                       code=None,
                       message=None,
                       additional_data=None):

        if code == 429:
            self.set_status(429, 'Too Many Requests')
        else:
            self.set_status(code)
        self.write(
            self.generate_response_data(
                status, response_data, message, additional_data))
        self.finish()

    def generate_response_data(self,
                               status,
                               response_data=None,
                               message=None,
                               additional_data=None):
        """ To keep our data consistent across endpoints, add additional
        fields and values that may not be present.
        :param status: (str): "Success"|"Failure"|"Error"
        :param response_data: (json serialisable object) the body of the response.
        :param code: (int) HTTP status code of the executed request.
        :param message: (str): In the case of an error, provide additional
           information.
        :param additional_data: (dict) Additional data to be updated the response
                                object with.
        """
        data = {
            'status': status,
        }
        if additional_data is not None:
            data.update(additional_data)
        if response_data is not None:
            if isinstance(response_data, list):
                data['records'] = len(response_data)
                data['data'] = response_data
            else:
                data['records'] = 1
                data['data'] = [response_data]
            self.response_length = data['records']

        if message is not None:
            data['message'] = message

        return data

    def success(self, response_data, additional_data=None):
        status_code = 200
        self.write_response('Success', response_data, status_code,
                            additional_data=additional_data)

    def deleted(self, response_data):
        status_code = 200
        self.write_response('Success', None, status_code, 'Record(s) Deleted.')

    def created(self, response_data, message='Record(s) Created.'):
        status_code = 201
        self.write_response('Success', response_data, status_code, message)

    def updated(self, response_data, message='Record Updated.'):
        status_code = 200
        self.write_response('Success', response_data, 200, message)

    def no_content(self):
        status_code = 204
        self._audit(status_code)
        self.clear()
        self.set_status(status_code)
        self.finish()
        raise Finish()

    def not_found(self, message):
        status_code = 404
        self.write_response('Failure', None, status_code, message)

    def not_allowed(self):
        status_code = 405
        message = 'Not Allowed'
        self.write_response('Failure', None, status_code, )

    def fail(self, response_data=None, message=None, code=400):
        status_code = code
        self._audit(status_code, message, response_data)
        self.write_response('Failure', response_data, status_code, message)

    def conflict(self, message='Record Already Exists.'):
        status_code = 409
        self.write_response('Failure', code=status_code, message=message)

    def unprocessable_entity(self, message):
        status_code = 422
        self.write_response('Failure', code=status_code, message=message)

    def too_many_requests(self, message='Too many requests'):
        status_code = 429
        self.write_response('Failure', code=status_code, message=message)

    def forbidden(self):
        """ Do not send any response data.
        Send a 403
        """
        status_code = 403
        self.clear()
        self.set_status(status_code)
        self.finish()
        raise Finish()

    def unauthorized(self):
        """ Do not send any response data.
        Send a 401
        """
        status_code = 401
        self.clear()
        self.set_status(status_code)
        self.finish()
        raise Finish()

    def error(self, message, response_data=None, code=500):
        """ The request failed during execution of the input.
        An exception was thrown or other non user input related issue.
        """
        result = {'status': 'error', 'message': message}
        if response_data:
            result['data'] = response_data
        if code:
            result['code'] = code
        self.write(result)
        self.set_status(code)
        self.finish()
        raise Finish()
