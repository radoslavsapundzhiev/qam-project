from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]

urlpatterns += [
    path('cases/', views.CaseListView.as_view(), name="cases"),
    path('cases-by-project/', views.get_cases, name="get_cases"),
    path('cases/add/', views.add_case, name="add_case"),
    path('cases/delete/<int:pk>/', views.delete_case, name="delete_case"),
    path('cases/get-edit-case/<int:pk>/', views.get_edit_case, name="get_edit_case"),
    path('cases/get/<int:pk>/', views.get_case, name="get_case"),
    path('cases/edit/<int:pk>/', views.update_case, name="update_case"),
    path('cases/get-case-status/<int:pk>/', views.get_case_status, name="get_case_status"),
    path('cases/check-case-number/', views.check_case_number, name="check_case_number"),
]

urlpatterns += [
    path('projects/', views.ProjectListView.as_view(), name="projects"),
    path('project-dropdown-options/', views.get_project_dropdown_options, name="get_project_dropdown_options"),
    path('projects/add/', views.add_project, name="add_project"),
    path('projects/check-project-name/', views.check_project_name, name="check_project_name"),
    path('projects/get-edit-project/<int:pk>/', views.get_edit_project, name="get_edit_project"),
    path('projects/get/<int:pk>/', views.get_project, name="get_project"),
    path('projects/edit/<int:pk>/', views.update_project, name="update_project"),
    path('projects/<int:pk>/', views.ProjectDetailView.as_view(), name="project-detail")
]

urlpatterns += [
    path('reports/', views.ReportListView.as_view(), name="reports"),
    path('reports/add/', views.add_report, name="add_report"),
    path('reports/get-edit-report/<int:pk>/', views.get_edit_report, name="get_edit_report"),
    path('reports/get/<int:pk>/', views.get_report, name="get_report"),
    path('reports/edit/<int:pk>/', views.update_report, name="update_report"),
    path('reports/delete/<int:pk>/', views.delete_report, name="delete_report")
]

urlpatterns += [
    path('products/', views.ProductListView.as_view(), name="products"),
    path('products/add/', views.add_product, name="add_product"),
    path('products/check-product-name/', views.check_product_name, name="check_product_name"),
    path('products/get-edit-product/<int:pk>/', views.get_edit_product, name="get_edit_product"),
    path('products/get/<int:pk>/', views.get_product, name="get_product"),
    path('products/edit/<int:pk>/', views.update_product, name="update_product"),
    path('products/get-products-multi-select-options/', views.get_products_multi_select_options, name="get_products_multi_select_options"),
    path('product-dropdown-options/', views.get_product_dropdown_options, name="get_product_dropdown_options"),
]

urlpatterns += [
    path('versions/', views.VersionListView.as_view(), name="versions"),
    path('versions/add/', views.add_version, name="add_version"),
    path('versions/get-edit-version/<int:pk>/', views.get_edit_version, name="get_edit_version"),
    path('versions/get/<int:pk>/', views.get_version, name="get_version"),
    path('versions/edit/<int:pk>/', views.update_version, name="update_version"),
    path('versions/delete/<int:pk>/', views.delete_version, name="delete_version"),
    path('versions/<int:pk>/', views.VersionDetailView.as_view(), name="version-detail")
]

urlpatterns += [
    path('clear/', views.clear, name="clear"),
]