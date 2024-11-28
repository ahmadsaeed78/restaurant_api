"""
URL configuration for restaurant_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from core import views
from core.views import login_view, signup_view, logout_view, success_view, manage_tables, add_table, delete_table, change_status, generate_bill
urlpatterns = [
    path('admin/', admin.site.urls),
    #path('api/', include('core.urls')),
    path('api/', include('core.api_urls')),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('menu/', views.menu_view, name='menu'),
    path('reservation/', views.reservation_view, name='reservation'),
    path('reserve_table/', views.reserve_table, name='reserve_table'),  # Reservation submission endpoint
    path('contact/', views.contact, name='contact'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('success/', success_view, name='success_page'),  # Ensure this is defined
    path('customer/', views.customer_dashboard, name='customer_dashboard'),
    path('admin_page/', views.admin_dashboard, name='admin_dashboard'),
    path('chief/dashboard/', views.chief_dashboard, name='chief_dashboard'),
    path('chief/menu_item/', views.menu_management, name='menu_management'),
    path('chief/menu_item/add/', views.add_menu_item, name='add_menu_item'),
    path('chief/menu_item/update/<int:item_id>/', views.update_menu_item, name='update_menu_item'),
    path('chief/menu_item/delete/<int:item_id>/', views.delete_menu_item, name='delete_menu_item'),
    path('menu/toggle/<int:item_id>/', views.toggle_availability, name='toggle_availability'),
    path('menu/<int:menu_item_id>/place_order/', views.place_order, name='place_order'),
    path('chief/manage_orders/', views.manage_orders, name='manage_orders'),
    path('chief/update_order_status/<int:order_id>/<str:new_status>/', views.update_order_status, name='update_order_status'),
    path('generate-bill/<int:order_id>/', generate_bill, name='generate_bill'),

    path('chief/menus/', views.menu_list, name='menu_list'),
    path('chief/menu/add/', views.add_menu, name='add_menu'),
    path('chief/menu/update/<int:menu_id>/', views.update_menu, name='update_menu'),
    path('chief/menu/delete/<int:menu_id>/', views.delete_menu, name='delete_menu'),

    path('chief/menu_groups/', views.menu_group_list, name='menu_group_list'),
    path('chief/menu_group/add/', views.add_menu_group, name='add_menu_group'),
    path('chief/menu_group/update/<int:menu_group_id>/', views.update_menu_group, name='update_menu_group'),
    path('chief/menu_group/delete/<int:menu_group_id>/', views.delete_menu_group, name='delete_menu_group'),

    path('scan-menu/', views.scan_menu, name='scan_menu'),
    path('place-order-unregistered/<int:item_id>/<int:table_id>/', views.place_order_unregistered, name='place_order_unregistered'),
    path('chief/manage_unregistered_orders/', views.manage_unregistered_orders, name='manage_unregistered_orders'),
    path('chief/change-status/<int:order_id>/<str:new_status>/', change_status, name='change_status'),

    path('chief/manage-tables/', views.manage_tables_chief, name='manage_tables_chief'),
    path('chief/generate-table-qr/<int:table_id>/', views.generate_table_qr, name='generate_table_qr'),

    path('admin_page/manage-tables/', manage_tables, name='manage_tables'),
    path('admin_page/add-table/', add_table, name='add_table'),
    path('admin_page/delete-table/<int:table_id>/', delete_table, name='delete_table'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)