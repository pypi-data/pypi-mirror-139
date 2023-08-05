# -*- coding: utf-8 -*-
from .lib import *
from .fundinginstrument import FundingInstrument

class Webhook(MoipEntity):

	def __init__(cls, **kw):

		cls.__route__ = '/webhooks'
		cls.__metadata__ = {}
		cls.__requireid__ = True

		# FIELDS
		cls.id = String(max=55)
		cls.resourceId = String(max=255)
		cls.event = String(max=255)
		cls.url = String(max=655)
		cls.status = String(max=55)
		cls.sentAt = String(max=55)

		super().__init__(**kw)
