from django.contrib import admin
from judge.models import Problem,Solution,TestCase
# Register your models here.
admin.site.register(Problem)
admin.site.register(Solution)
admin.site.register(TestCase)