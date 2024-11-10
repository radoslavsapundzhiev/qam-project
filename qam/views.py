from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.conf import settings
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils import calc_case_status
from django.core.paginator import Paginator

from .models import Case, Project, Product, Version, Report

def index(request):
    all_projects = Project.objects.all()
    all_cases = Case.objects.all()
    all_products = Product.objects.all()
    all_reports = Report.objects.all()
    context = {
        'title': 'Home',
        'all_projects': all_projects,
        'all_cases': all_cases,
        'all_products': all_products,
        'all_reports': all_reports
    }
    return render(request, 'index.html', context)

def get_cases(request):
    project = request.GET.get('project')
    product = request.GET.get('product')
    version = request.GET.get('version')
    cases = []
    context = {}

    if project:
        products = Product.objects.filter(project=project)
        cases = Case.objects.filter(products__in=products).distinct()
        context['products'] = products

    if project and product and products and int(product) in list(map(lambda p: p.id, products)):
        cases = cases.filter(products__id=product).distinct()
        versions = Version.objects.filter(product__id=product)
        context['product_id'] = int(product)
        context['versions'] = versions

    if version:
        context['version_id'] = int(version)

    context['cases'] = cases

    return render(request, 'case/partials/cases_by_project.html', context)

class VersionListView(LoginRequiredMixin, generic.ListView):
    model = Version
    context_object_name = 'versions'
    template_name = 'version/versions_page.html'
    paginate_by = settings.PAGINATE_BY

    def get_template_names(self):
        if self.request.htmx:
            return 'version/partials/versions_tbody.html'
        return 'version/versions_page.html'
    
    def get_queryset(self, **kwargs):
        queryset = []
        product_id = self.request.GET.get('product', '')
        queryset = Version.objects.all()

        if product_id:
            queryset = queryset.filter(product=product_id)

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super(VersionListView, self).get_context_data(**kwargs)
        context['title'] = 'Versions'
        return context
    
class VersionDetailView(generic.DetailView):
    template_name = 'version/version_detail.html'
    model = Version

    def get_context_data(self, **kwargs):
        context = super(VersionDetailView, self).get_context_data(**kwargs)
        context['title'] = 'Version Details'
        return context

class CaseListView(LoginRequiredMixin, generic.ListView):
    model = Case
    context_object_name = 'cases'
    template_name = 'case/cases_page.html'
    paginate_by = 10

    def get_template_names(self):
        if self.request.htmx:
            return 'case/partials/cases_tbody.html'
        return 'case/cases_page.html'

    def get_queryset(self, **kwargs):
        queryset = []
        search = self.request.GET.get('search', '')
        if search:
            queryset = Case.objects.filter(case_number__contains=search)
        else:
            queryset = Case.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super(CaseListView, self).get_context_data(**kwargs)
        context['title'] = 'Cases'
        return context

class ProjectListView(LoginRequiredMixin, generic.ListView):
    model = Project
    context_object_name = 'projects'
    template_name = 'project/projects_page.html'
    paginate_by = settings.PAGINATE_BY

    def get_template_names(self):
        if self.request.htmx:
            return 'project/partials/projects_tbody.html'
        return 'project/projects_page.html'

    def get_queryset(self, **kwargs):
        queryset = []
        search = self.request.GET.get('search', '')
        if search:
            queryset = Project.objects.filter(name__contains=search)
        else:
            queryset = Project.objects.all()
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs)
        context['title'] = 'Projects'
        return context
    
class ProjectDetailView(generic.DetailView):
    template_name = 'project/project_detail.html'
    model = Project

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        context['title'] = 'Project Details'
        return context
  
class ProductListView(LoginRequiredMixin, generic.ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'product/products_page.html'
    paginate_by = settings.PAGINATE_BY

    def get_template_names(self):
        if self.request.htmx:
            return 'product/partials/products_tbody.html'
        return 'product/products_page.html'
    
    def get_queryset(self, **kwargs):
        queryset = []
        search = self.request.GET.get('search', '')
        project_filter = self.request.GET.get('project_filter', '')
        queryset = Product.objects.all()

        if search:
            queryset = queryset.filter(name__contains=search)

        if project_filter:
            queryset = queryset.filter(project=project_filter)

        return queryset

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['title'] = 'Products'
        return context

class ReportListView(generic.ListView):
    model = Report
    context_object_name = 'reports'
    template_name = 'report/reports.html'
    paginate_by = 5

    def get_template_names(self):
        is_show_more = self.request.GET.get('is_show_more', False)
        if is_show_more:
            return 'report/partials/reports_tbody.html'
        return 'report/reports.html'

    def get_queryset(self, **kwargs):
        queryset = []
        version = self.request.GET.get('version')
        case = self.request.GET.get('case')
        if version and case:
            queryset = Report.objects.filter(version=version, case=case)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super(ReportListView, self).get_context_data(**kwargs)
        case = self.request.GET.get('case')
        if case:
            context['case_id'] = case

        version = self.request.GET.get('version')
        if version:
            context['version_id'] = version

        options = [
            ('n', 'N.A.'), 
            ('p', 'PASSED'), 
            ('f', 'FAILED'), 
            ('r', 'PASSED WITH REMARKS'), 
            ('b', 'BLOCKED')
        ]

        context['options'] = options

        return context
    
def clear(request):
    return HttpResponse("")

def get_project_dropdown_options(request):
    is_add_case = request.GET.get('is_add_case', False)
    is_index_page = request.GET.get('is_index_page', False)
    is_edit_case = request.GET.get('is_edit_case', False)
    project_id = request.GET.get('project_id', '')
    product_id = request.GET.get('product_id', '')
    is_products_filter = request.GET.get('is_products_filter', False)
    is_versions_page = request.GET.get('is_versions_page', False)
    projects = Project.objects.all()
    context = { 'projects': projects }
    if is_add_case:
        context['is_add_case'] = True
    elif is_index_page:
        context['is_index_page'] = True
    elif product_id:
        product = get_object_or_404(Product, pk=product_id)
        context['project_id'] = product.project.id
    elif is_edit_case and project_id:
        context['project_id'] = int(project_id)
    elif is_edit_case:
        context['is_edit_case'] = True
    elif is_products_filter:
        context['is_products_filter'] = True
    elif is_versions_page:
        context['is_versions_page'] = True
    return render(request, 'project/partials/projects_dropdown_list.html', context)

@require_http_methods(['POST'])
def add_project(request):
    project = None
    name = request.POST.get('name', '')

    if name:
        try:
            project = Project.objects.create(name=name)
        except:
            messages.error(request, f"Error creating project with name {name}.")
        
    project_list = Project.objects.all()
    paginator = Paginator(project_list, settings.PAGINATE_BY)
    page_obj = paginator.get_page(1)

    if project:
        messages.success(request, f"Added project with name {project.name} to the list of projects.")

    return render(request, 'project/partials/projects.html', { 'page_obj': page_obj })

@require_http_methods(['POST'])
def check_project_name(request):
    name = request.POST.get('name')
    if not name:
        return HttpResponse()
    if Project.objects.filter(name=name).exists():
        return HttpResponse('<p class="help is-danger">The project name already exists.</p>')
    else:
        return HttpResponse('<p class="help is-success">The project name is available.</p>')
    
def get_edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'project/partials/project_edit.html', { 'project': project })

def get_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'project/partials/project_row.html', { 'project': project })

@require_http_methods(['POST'])
def update_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    name = request.POST.get('name', project.name)
    project.name = name
    project.save()
    return render(request, 'project/partials/project_row.html', { 'project': project })

@require_http_methods(['POST'])
def add_product(request):
    product = None
    name = request.POST.get('name', '')
    project_id = request.POST.get('project', '')

    if name and project_id:
        try:
            product = Product.objects.create(name=name)
            project = Project.objects.get(pk=project_id)
            project.product_set.add(product)
        except:
            messages.error(request, f"Error creating product with name {name}.")
    else:
        messages.error(request, "Unique name and project are required field!")
    
    products_list = Product.objects.all()
    paginator = Paginator(products_list, settings.PAGINATE_BY)
    page_obj = paginator.get_page(1)

    if product:
        messages.success(request, f"Added product with name {product.name} to the list of products.")

    return render(request, 'product/partials/products.html', { 'page_obj': page_obj })

@require_http_methods(['POST'])
def check_product_name(request):
    name = request.POST.get('name')
    if not name:
        return HttpResponse()
    if Product.objects.filter(name=name).exists():
        return HttpResponse('<p class="help is-danger">The product name already exists.</p>')
    else:
        return HttpResponse('<p class="help is-success">The product name is available.</p>')
    
def get_edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product/partials/product_edit.html', { 'product': product })

def get_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product/partials/product_row.html', { 'product': product })

@require_http_methods(['POST'])
def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    name = request.POST.get('name', '')
    project_id = request.POST.get('project', '')

    if name:
        product.name = name
        product.save()
    
    if project_id:
        project = get_object_or_404(Project, pk=project_id)
        project.product_set.add(product)

    return render(request, 'product/partials/product_row.html', { 'product': product })

@require_http_methods(['POST'])
def add_report(request):
    report = None
    version_id = request.POST.get('version', '')
    case_id = request.POST.get('case', '')
    result = request.POST.get('result', 'n')
    fail_reason = request.POST.get('fail_reason', '')
    fail_location = request.POST.get('fail_location', '')

    if version_id and case_id:
        try:
            report = Report.objects.create(result=result, fail_reason=fail_reason, fail_location=fail_location)
            case = get_object_or_404(Case, pk=case_id)
            version = get_object_or_404(Version, pk=version_id)
            case.report_set.add(report)
            version.report_set.add(report)
        except:
            messages.error(request, f"Error creating report.")
        
    reports = Report.objects.filter(case=case_id, version=version_id)

    if report:
        messages.success(request, f"Added report to the list of reports.")

    return render(request, 'report/partials/reports_table.html', { 'reports': reports, 'case_id': case_id })

def get_products_multi_select_options(request):
    project_id = request.GET.get('project', '')
    case_id = request.GET.get('case', '')
    context = {}
    products = []
    if project_id:
        products = Product.objects.filter(project=project_id)
        context['products'] = products
    if case_id:
        case = get_object_or_404(Case, pk=case_id)
        context['case_products'] = list(map(lambda p: p.id, case.products.all()))
    return render(request, 'product/partials/products_multi_select_list.html', context)

@require_http_methods(['POST'])
def add_case(request):
    case = None
    case_number = request.POST.get('case_number', '')
    name = request.POST.get('name', '')
    description = request.POST.get('description', '')
    expected_result = request.POST.get('expected_result', '')
    init_conf = request.POST.get('init_conf', '')
    products = request.POST.getlist('products', [])

    if case_number and name:
        try:
            case = Case.objects.filter(case_number=case_number)
            if case:
                messages.error(request, f"Case with case number: {case_number} already exists!")
                case = None
            else:
                case = Case.objects.create(
                    case_number=case_number, 
                    name=name,
                    description=description,
                    expected_result=expected_result,
                    init_conf=init_conf
                )
                case.products.add(*products)
        except:
            messages.error(request, f"Error creating case.")
    else:
        messages.error(request, "Case number and name are required!")

    cases_list = Case.objects.all()
    paginator = Paginator(cases_list, 10)
    page_obj = paginator.get_page(1)

    if case:
        messages.success(request, f"Added case with name {case.name} to the list of cases.")

    return render(request, 'case/partials/cases.html', { 'page_obj': page_obj })

def get_product_dropdown_options(request):
    version_id = request.GET.get('version_id', '')
    project_id = request.GET.get('project', '')
    is_versions_page = request.GET.get('is_versions_page', False)
    products = Product.objects.all()
    context = {}
    if version_id:
        version = get_object_or_404(Version, pk=version_id)
        product = get_object_or_404(Product, pk=version.product.id)
        project = get_object_or_404(Project, pk=product.project.id)
        products = products.filter(project=project)
        context['product_id'] = version.product.id

    if is_versions_page:
        context['is_versions_page'] = True

    if project_id:
        products = products.filter(project=project_id)

    if not project_id and is_versions_page:
        products = []

    context['products'] = products
    
    return render(request, 'product/partials/products_dropdown_list.html', context)

@require_http_methods(['POST'])
def add_version(request):
    version = None
    name = request.POST.get('name', '')
    product_id = request.POST.get('product', '')

    if name and product_id:
        try:
            version = Version.objects.create(name=name)
            product = Product.objects.get(pk=product_id)
            product.version_set.add(version)
        except:
            messages.error(request, f"Error creating version with name {name}.")

    else:
        messages.error(request, "Name and product are required fields!")
    
    version_list = Version.objects.all()
    paginator = Paginator(version_list, settings.PAGINATE_BY)
    page_obj = paginator.get_page(1)

    if version:
        messages.success(request, f"Added version with name {version.name} to the list of versions.")

    return render(request, 'version/partials/versions.html', { 'page_obj': page_obj })

def get_edit_version(request, pk):
    version = get_object_or_404(Version, pk=pk)
    return render(request, 'version/partials/version_edit.html', { 'version': version })

def get_version(request, pk):
    version = get_object_or_404(Version, pk=pk)
    return render(request, 'version/partials/version_row.html', { 'version': version })

@require_http_methods(['POST'])
def update_version(request, pk):
    version = get_object_or_404(Version, pk=pk)
    name = request.POST.get('name', '')
    product_id = request.POST.get('product', '')

    if name:
        version.name = name
        version.save()

    if product_id:
        product = get_object_or_404(Product, pk=product_id)
        product.version_set.add(version)

    return render(request, 'version/partials/version_row.html', { 'version': version })

@require_http_methods(['DELETE'])
def delete_version(request, pk):
    version = get_object_or_404(Version, pk=pk)
    version.delete()
    return HttpResponse()

@require_http_methods(['DELETE'])
def delete_case(request, pk):
    case = get_object_or_404(Case, pk=pk)
    case.delete()
    return HttpResponse()

def get_edit_case(request, pk):
    case = get_object_or_404(Case, pk=pk)
    return render(request, 'case/partials/case_edit.html', { 'case': case })

def get_case(request, pk):
    case = get_object_or_404(Case, pk=pk)
    return render(request, 'case/partials/case_row.html', { 'case': case })

@require_http_methods(['POST'])
def update_case(request, pk):
    case = get_object_or_404(Case, pk=pk)
    case_number = request.POST.get('case_number', case.case_number)
    name = request.POST.get('name', case.name)
    description = request.POST.get('description', case.description)
    expected_result = request.POST.get('expected_result', case.expected_result)
    init_conf = request.POST.get('init_conf', case.init_conf)
    products = request.POST.getlist('products', [])

    case.case_number = case_number
    case.name = name
    case.description = description
    case.expected_result = expected_result
    case.init_conf = init_conf
    case.products.clear()
    case.products.add(*products)

    case.save()

    return render(request, 'case/partials/case_row.html', { 'case': case })

def get_case_status(request, pk):
    version_id = request.GET.get('version', '')
    status = 'TODO'
    color = 'grey'

    if version_id:
        all_items = Report.objects.filter(case=pk, version=version_id)
        blocked = all_items.filter(result='b')
        remarks = all_items.filter(result='r')
        passed = all_items.filter(result='p')
        failed = all_items.filter(result='f')
        if len(all_items) > 0:
            status_info = calc_case_status(passed, failed, blocked, remarks, all_items)
            status = status_info[0]
            color = status_info[1]
    
    return HttpResponse(f"<div style='background-color: {color}; border-radius: 1rem; padding: 1rem;'>{status}</div>")

def get_edit_report(request, pk):
    report = get_object_or_404(Report, pk=pk)
    options = [
        ('n', 'N.A.'), 
        ('p', 'PASSED'), 
        ('f', 'FAILED'), 
        ('r', 'PASSED WITH REMARKS'), 
        ('b', 'BLOCKED')
    ]
    return render(request, 'report/partials/report_edit.html', { 'report': report, 'options': options })

def get_report(request, pk):
    report = get_object_or_404(Report, pk=pk)
    return render(request, 'report/partials/report_row.html', { 'report': report })

@require_http_methods(['POST'])
def update_report(request, pk):
    report = get_object_or_404(Report, pk=pk)
    result = request.POST.get('result', report.result)
    fail_reason = request.POST.get('fail_reason', report.fail_reason)
    fail_location = request.POST.get('fail_location', report.fail_location)

    report.result = result
    report.fail_reason = fail_reason
    report.fail_location = fail_location

    report.save()

    return render(request, 'report/partials/report_row.html', { 'report': report })

@require_http_methods(['DELETE'])
def delete_report(request, pk):
    report = get_object_or_404(Report, pk=pk)
    report.delete()
    return HttpResponse()

@require_http_methods(['POST'])
def check_case_number(request):
    case_number = request.POST.get('case_number')
    if not case_number:
        return HttpResponse()
    if Case.objects.filter(case_number=case_number).exists():
        return HttpResponse('<p class="help is-danger">The case number already exists.</p>')
    else:
        return HttpResponse('<p class="help is-success">The case number is available.</p>')