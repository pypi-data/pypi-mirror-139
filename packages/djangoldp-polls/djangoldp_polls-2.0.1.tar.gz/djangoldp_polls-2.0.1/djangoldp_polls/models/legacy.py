from django.conf import settings
from django.db import models, transaction

from djangoldp.models import Model



#========================

#========================

class Tag (Model):
	name = models.CharField(max_length=250, null=True, blank=True, verbose_name="Name")

	class Meta(Model.Meta):
		serializer_fields = ['@id','name']
		anonymous_perms = ['view']
		authenticated_perms = ['inherit','add']
		rdf_type = 'sib:tag'

	def __str__(self):
		return self.name




