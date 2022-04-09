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
         self.set_status(HTTPStatus.TOO_MANY_REQUESTS,
                         'Too Many Requests')
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
          'ResultCode': result_code,
      }
      if message is not None:
         data['Message'] = message

      if additional_data is not None:
         data.update(additional_data)

      if response_data is not None:
         if isinstance(response_data, list):
            data['Data'] = response_data
         else:
            data['Data'] = [response_data]

      return data

   def success(self, result_code, response_data, additional_data=None):
      status_code = HTTPStatus.OK
      self.write_response(result_code, response_data, status_code,
                          additional_data=additional_data)

   def deleted(self, result_code):
      status_code = HTTPStatus.OK
      self.write_response(result_code, None, status_code, 'Record(s) Deleted.')

   def created(self, result_code, response_data, message='Success.'):
      status_code = HTTPStatus.CREATED
      self.write_response(result_code, response_data,
                          status_code, message=message)

   def updated(self, result_code, response_data, message='Record Updated.'):
      status_code = HTTPStatus.OK
      self.write_response(result_code, response_data,
                          status_code, message=message)

   def see_other(self, result_code, response_data, message='See Other.'):
      status_code = HTTPStatus.SEE_OTHER
      self.write_response(result_code, response_data, status_code, message)

   def no_content(self):
      status_code = HTTPStatus.NO_CONTENT
      self.clear()
      self.set_status(status_code)
      self.finish()
      raise Finish()

   def not_found(self, result_code, message):
      status_code = HTTPStatus.NOT_FOUND
      self.write_response(result_code, None, status_code, message=message)

   def not_allowed(self, result_code):
      status_code = HTTPStatus.METHOD_NOT_ALLOWED
      message = 'Not Allowed'
      self.write_response(result_code, None, status_code, message=message)

   def fail(self, result_code, response_data=None, message=None, code=400):
      status_code = code
      self.write_response(result_code, response_data, status_code, message)

   def conflict(self, result_code, message='Record Already Exists.'):
      status_code = HTTPStatus.CONFLICT
      self.write_response(result_code, code=status_code, message=message)

   def unprocessable_entity(self, result_code, message):
      status_code = HTTPStatus.UNPROCESSABLE_ENTITY
      self.write_response(result_code, code=status_code, message=message)

   def too_many_requests(self, result_code, message='Too many requests'):
      status_code = HTTPStatus.TOO_MANY_REQUESTS
      self.write_response(result_code, code=status_code, message=message)

   def forbidden(self):
      """ Do not send any response data.
      Send a 403
      """
      status_code = HTTPStatus.FORBIDDEN
      self.clear()
      self.set_status(status_code)
      self.finish()
      raise Finish()

   def unauthorized(self):
      """ Do not send any response data.
      Send a 401
      """
      status_code = HTTPStatus.UNAUTHORIZED
      self.clear()
      self.set_status(status_code)
      self.finish()
      raise Finish()

   def error(self, message, response_data=None, code=500):
      """ The request failed during execution of the input.
      An exception was thrown or other non user input related issue.
      """
      result = {'Status': 'error'}
      if response_data:
         result['Data'] = response_data
      if code:
         result['Code'] = code
      if message:
         result['Message'] = message
      self.write(result)
      self.set_status(code)
      self.finish()
      raise Finish()

   def service_unavailable(self):
      status_code = HTTPStatus.SERVICE_UNAVAILABLE
      self.clear()
      self.set_status(status_code)
      self.finish()
      raise Finish()
