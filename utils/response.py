from tornado.web import Finish
from http import HTTPStatus
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
                       result_code,
                       response_data=None,
                       code=None,
                       message=None,
                       additional_data=None):

        if code == HTTPStatus.TOO_MANY_REQUESTS:
            self.set_status(HTTPStatus.TOO_MANY_REQUESTS.value, 'Too Many Requests')
        else:
            self.set_status(code)
        self.write(
            self.generate_response_data(
                result_code, response_data, message, additional_data))
        self.finish()

    def generate_response_data(self,
                               result_code,
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
            'resultCode': result_code,
        }
        if message is not None:
            data['message'] = message

        if additional_data is not None:
            data.update(additional_data)

        if response_data is not None:
            if isinstance(response_data, list):
                data['data'] = response_data
            else:
                data['data'] = [response_data]

        return data

    # def success(self,result_code, response_data, additional_data=None):
    #     status_code = HTTPStatus.OK.value
    #     self.write_response(result_code, response_data, status_code,
    #                         additional_data=additional_data)

    def deleted(self, result_code):
        status_code = HTTPStatus.OK.value
        self.write_response(result_code, None, status_code, 'Record(s) Deleted.')

    def created(self, result_code, response_data, message='Success.'):
        status_code = HTTPStatus.CREATED.value
        self.write_response(result_code, response_data, status_code, message=message)

    def updated(self, result_code, response_data, message='Record Updated.'):
        status_code = HTTPStatus.OK.value
        self.write_response(result_code, response_data, status_code, message=message)

    def see_other(self, result_code, response_data, message='See Other.'):
        status_code = HTTPStatus.SEE_OTHER.value
        self.write_response(result_code, response_data, status_code, message)

    def no_content(self):
        status_code = HTTPStatus.NO_CONTENT.value
        self._audit(status_code)
        self.clear()
        self.set_status(status_code)
        self.finish()
        raise Finish()

    def not_found(self, result_code, message):
        status_code = HTTPStatus.NOT_FOUND.value
        self.write_response(result_code, None, status_code, message=message)

    def not_allowed(self, result_code):
        status_code = HTTPStatus.METHOD_NOT_ALLOWED.value
        message = 'Not Allowed'
        self.write_response(result_code, None, status_code, message=message)

    # def fail(self, response_data=None, message=None, code=400):
    #     status_code = code
    #     self.write_response('Failure', response_data, status_code, message)

    def conflict(self, result_code, message='Record Already Exists.'):
        status_code = HTTPStatus.CONFLICT.value
        self.write_response(result_code, code=status_code, message=message)

    def unprocessable_entity(self, result_code, message):
        status_code = HTTPStatus.UNPROCESSABLE_ENTITY.value
        self.write_response(result_code, code=status_code, message=message)

    def too_many_requests(self, result_code, message='Too many requests'):
        status_code = HTTPStatus.TOO_MANY_REQUESTS.value
        self.write_response(result_code, code=status_code, message=message)

    def forbidden(self):
        """ Do not send any response data.
        Send a 403
        """
        status_code = HTTPStatus.FORBIDDEN.value
        self.clear()
        self.set_status(status_code)
        self.finish()
        raise Finish()

    def unauthorized(self):
        """ Do not send any response data.
        Send a 401
        """
        status_code = HTTPStatus.UNAUTHORIZED.value
        self.clear()
        self.set_status(status_code)
        self.finish()
        raise Finish()

    def error(self, message, response_data=None, code=500):
        """ The request failed during execution of the input.
        An exception was thrown or other non user input related issue.
        """
        result = {'status': 'error'}
        if response_data:
            result['data'] = response_data
        if code:
            result['code'] = code
        if message:
            result['message'] = message
        self.write(result)
        self.set_status(code)
        self.finish()
        raise Finish()

    def service_unavailable(self):
        status_code = HTTPStatus.SERVICE_UNAVAILABLE.value
        self.clear()
        self.set_status(status_code)
        self.finish()
        raise Finish()
