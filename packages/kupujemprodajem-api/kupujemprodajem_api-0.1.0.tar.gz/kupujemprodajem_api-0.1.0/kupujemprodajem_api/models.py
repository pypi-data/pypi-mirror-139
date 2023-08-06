from .exceptions import CompanyError
from .exceptions import JobError


class Advertisment:
	def __init__(self,
				title,
				description,
				price_currency,
				price,
				images,
				condition,
				category,
				subcategory,
				city,
				name,
				phone,
				user_type='person',
				ad_type='goods'):

		self.title = title
		self.description = description
		self.price_currency = price_currency  # eur or rsd
		self.price = price
		# ad_type is only one of follwing: stvar / usluga / posao
		self.ad_type = ad_type  # default - stvar
		self.images = images
		# condition: new_company (company) - new_personal (not used) - used, faulty
		self.condition = condition

		# Category and subcategory information - data: id (both)
		self.category = category
		self.subcategory = subcategory

		self.user_type = user_type  # person or company
		# if user_type = company then you must use: set_company(number, name, address)
		# to add additional information about the company

		# User information
		self.city = city
		self.name = name
		self.phone = phone

		# Company
		self.company_number = None
		self.company_name = None
		self.company_address = None

		# Job
		self.job_email = None
		self.job_link = None
		self.job_phone = None

		if self.user_type == 'company':
			self._check_company()




		self.is_car = False  # by default not posting a car ad
		self.is_job = False  # by default not posting a job ad

		# perform data validation
		self._check_condition()
		self._check_user_type()
		# add check_car, check_job - if it's a car or a job then validate data

		self.data = None

	# getters
	def get_data(self):
		return self._request_data

	# setters
	def set_company(self, number, name, address):
		self.company_number = number
		self.company_name = name
		self.company_address = address

	# utils

	def _request_data(self):
		data = {
			'submit[post]': 'Postavite oglas',
			'action': 'ajax_save',
			'form_id': '61d6ea85a28845fe4361d14db2c8bce9',
			'data[service_top_price_displayed]': str(self.price),
			'return_url': '',
			'data[promo_gold_ad]': '',
			'data[ad_kind]': self.ad_type,
			'data[category_id]': str(self.category),
			'data[group_id]': str(self.subcategory),
			'data[car_model]': '',
			'data[car_model_desc]': '',
			'data[vehicle_make_year]': '',
			'data[vehicle_km]': '',
			'data[vehicle_fuel_type]': '',
			'data[car_body_type]': '',
			'data[car_doors]': '',
			'data[vehicle_seats]': '',
			'data[vehicle_cc]': '',
			'data[vehicle_power]': '',
			'data[vehicle_power_h]': '',
			'data[vehicle_drive]': '',
			'data[vehicle_exterior_color]': '',
			'data[car_gearbox]': '',
			'data[vehicle_aircondition]': '',
			'data[vehicle_owner_type]': '',
			'data[vehicle_origin]': '',
			'data[vehicle_registered_date]': '',
			'data[vehicle_emission_class]': '',
			'data[name]': self.title,
			'data[ad_type]': 'sell',
			'data[price]': str(self.price),
			'data[currency]': self.price_currency,
			'data[price_text]': '',
			'data[description]': self.description,
			'data[location_id]': str(self.city),
			'data[owner]': self.name,
			'data[phone]': self.phone,
			'data[job_application_email]': '',
			'data[job_application_link]': '',
			'data[job_application_phone]': '',
			'data[promo_type]': 'none',
			'data[promo_service_id][top]': '5',
			'data[website]': '',
			'data[video_url]': '',
			'data[declaration_type]': self.user_type,
			'data[d_registration_number]': str(company_number),
			'data[d_company_name]': self.company_name,
			'data[d_address]': self.company_address,
			'data[accept]': 'yes'
		}
		return data

	def _is_car(self):
		if self.category == 323 and self.ad_type == 'stvar':
			self.is_car = True
			return True
		return False

	def _is_job(self):
		if self.ad_type == 'posao':
			self.is_job = True
			return True
		return False


	def _check_condition(self, condition):
		if condition in ('new_company', 'new_personal', 'used', 'faulty'):
			self.condition = condition
		else:
			raise TypeError

	def _check_user_type(self, user_type):
		if user_type in ('person', 'company'):
			self.user_type = user_type
		else:
			raise TypeError

	def _check_company(self):
		'''Checks if Company data is valid
		
		If an ad is being posted by a company, certain fields are required
		company number, company name, company address
		
		Returns:
			if data valid then True else Error
			bool
		'''
		if all((self.company_number, self.company_name, self.company_address)):
			return True
		else:
			raise 'Custom Exception: Company is missing parameter (number or name or address)'

	def _check_job(self):
		'''Check job data is valid
		
		If an ad is being posted by a job, certain fields are required
		job email, job link, job phone
		
		Returns:
			if data valid then True else Error
			bool
		'''
		if all((self.job_email, self.job_link, self.job_phone)):
			return True
		else:
			raise JobError

