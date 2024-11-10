from django.db import models

from django.urls import reverse

from django.db.models.functions import Lower

class Project(models.Model):
    name = models.CharField(max_length=255, unique=True, help_text="Enter a project name.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']

    def get_absolute_url(self):
        return reverse('project-detail', args=[str(self.id)])
    
    def get_cases(self):
        products = Product.objects.filter(project=self)
        cases = Case.objects.filter(products__in=products).distinct()
        return cases
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255, unique=True, help_text="Enter a product name.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    project = models.ForeignKey('Project', on_delete=models.RESTRICT, null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def get_absolute_url(self):
        return reverse('product-detail', args=[str(self.id)])
    
    def __str__(self):
        return self.name
    
class Case(models.Model):
    name = models.CharField(max_length=255, help_text="Enter a case name.", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    case_number = models.CharField(max_length=255, help_text="Enter a case_number.", null=True)
    description = models.TextField(max_length=1000, help_text="Enter a description.", null=True, blank=True)
    expected_result = models.CharField(max_length=255, help_text="Enter an expected_result.", null=True, blank=True)
    init_conf = models.TextField(max_length=1000, help_text="Enter an initial configuration.", null=True, blank=True)
    products = models.ManyToManyField('Product', help_text="Select a product for this case.", blank=True)

    class Meta:
        ordering = ['case_number']

    def get_absolute_url(self):
        return reverse('case-detail', args=[str(self.id)])
    
    def get_project(self):
        project = None
        if self.products.first():
            project = self.products.first().project
        return project
    
    def __str__(self):
        return self.name
    
class Version(models.Model):
    name = models.CharField(max_length=255, help_text="Enter a version name.", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    product = models.ForeignKey('Product', on_delete=models.RESTRICT, null=True)

    class Meta:
        ordering = ['-created_at']

    def get_absolute_url(self):
        return reverse('version-detail', args=[str(self.id)])
    
    def __str__(self):
        return self.name
    
class Report(models.Model):
    RESULT_STATUS = (
        ('p', 'PASSED'),
        ('f', 'FAILED'),
        ('r', 'PASSED_WITH_REMARKS'),
        ('b', 'BLOCKED'),
        ('n', 'N.A.')
    )
    result = models.CharField(max_length=1, choices=RESULT_STATUS, blank=True, default='n', help_text="Report result.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    fail_reason = models.CharField(max_length=255, null=True, blank=True, help_text="Enter fail reason.")
    fail_location = models.CharField(max_length=255, null=True, blank=True, help_text="Enter fail location.")
    info_link =  models.CharField(max_length=255, null=True, blank=True, help_text="Enter info link.")
    params =  models.CharField(max_length=255, null=True, blank=True, help_text="Enter params.")
    info =  models.CharField(max_length=255, null=True, blank=True, help_text="Enter info.")
    reboot = models.BooleanField(null=True, blank=True, default=False, help_text="Enter reboot.")
    fast = models.BooleanField(null=True, blank=True, default=False, help_text="Enter fast.")
    login = models.BooleanField(null=True, blank=True, default=False, help_text="Enter login.")
    case = models.ForeignKey('Case', on_delete=models.CASCADE, null=True, blank=True)
    version = models.ForeignKey('Version', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def get_absolute_url(self):
        return reverse('result-detail', args=[str(self.id)])
    
    def __str__(self):
        return self.result