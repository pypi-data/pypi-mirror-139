# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from app.models import *

# Register your models here.
admin.site.register(status)
admin.site.register(MoveGroup)
admin.site.register(MoveGroupVM)
admin.site.register(MigrationCheckup)
admin.site.register(DRSRules)
admin.site.register(Storage)
admin.site.register(VMDetail)
admin.site.register(Network)
