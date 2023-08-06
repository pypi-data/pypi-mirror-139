class Error(Exception):
	pass



class LoginError(Error):
	def __init__(self):
		self.message = 'User login is invalid, please check Email or Password.'
		super(LoginError, self).__init__(message)

class CompanyError(Error):
	def __init__(self):
		self.message = 'Company data is invalid, please check Company -  Number, Name or Address.'
		super(CompanyError, self).__init__(message)


class JobError(Error):
	def __init__(self):
		self.message = 'Job data is invalid, please check Job - Email, Link or Phone.'
		super(JobError, self).__init__(message)