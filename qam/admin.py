from django.contrib import admin

from .models import Project, Product, Case, Version, Report

class ReportAdmin(admin.ModelAdmin):
    list_display = ('result', 'case', 'version', 'created_at')

admin.site.register(Project)
admin.site.register(Product)
admin.site.register(Case)
admin.site.register(Version)
admin.site.register(Report, ReportAdmin)