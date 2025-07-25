from django.urls import path
from . import views
from .views import TableListAPIView, ContactAPIView, update_item_availability, MenuItemList
from .views import RecommendFoodByWeather, get_unregistered_orders, change_order_status, generate_bill
from .views_multorder import create_aggregate_order, AggregateOrderListAPIView, AggregateOrderRetrieveAPIView, update_order_status, download_bill, ReservationCreateView, ReservationListView, approve_reservation
from . import views_multorder
from .views_multorder import TableStatusUpdateAPIView
from .views import TestimonialListAPIView

urlpatterns = [
    # User API
    path('users/', views.UserListCreateAPIView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', views.UserRetrieveUpdateDestroyAPIView.as_view(), name='user-detail'),

    # Menu APIs
    path('menus/', views.MenuListCreateAPIView.as_view(), name='menu-list-create'),
    path('menus/<int:pk>/', views.MenuRetrieveUpdateDestroyAPIView.as_view(), name='menu-detail'),

    # Menu Group APIs
    path('menu_groups/', views.MenuGroupListCreateAPIView.as_view(), name='menu-group-list-create'),
    path('menu_groups/<int:pk>/', views.MenuGroupRetrieveUpdateDestroyAPIView.as_view(), name='menu-group-detail'),

    # Menu Item APIs
    path('menu_items/', views.MenuItemListCreateAPIView.as_view(), name='menu-item-list-create'),
    path('menu_items/<int:pk>/', views.MenuItemRetrieveUpdateDestroyAPIView.as_view(), name='menu-item-detail'),

    # Reservation APIs
    #path('reservations/', views.ReservationListCreateAPIView.as_view(), name='reservation-list-create'),
    #path('reservations/<int:pk>/', views.ReservationRetrieveUpdateDestroyAPIView.as_view(), name='reservation-detail'),

    # Order APIs
    path('orders/', views.OrderListCreateAPIView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', views.OrderRetrieveUpdateDestroyAPIView.as_view(), name='order-detail'),

    # Table APIs
    path('tables/', views.TableListCreateAPIView.as_view(), name='table-list-create'),
    path('tables/<int:pk>/', views.TableRetrieveUpdateDestroyAPIView.as_view(), name='table-detail'),

    # Unregistered Order APIs
    path('unregistered_orders/', views.UnregisteredOrderListCreateAPIView.as_view(), name='unregistered-order-list-create'),
    path('unregistered_orders/<int:pk>/', views.UnregisteredOrderRetrieveUpdateDestroyAPIView.as_view(), name='unregistered-order-detail'),

    # Herirchy response
    path('menu_herirchy/', views.MenuListView.as_view(), name='menu-list'),
    path('menu_group_hierarchy/', views.MenuGroupHierarchyView.as_view(), name='menu-group'),
    path('api/tables/', TableListAPIView.as_view(), name='table-list'),
    path('contact/', ContactAPIView.as_view(), name='contact_api'),
    path('menu_items/<int:item_id>/availability/', update_item_availability, name='update_item_availability'),
    #unregistered orders apis
    path('unregistered-orders/', get_unregistered_orders, name='get_unregistered_orders'),
    path('change-status/<int:order_id>/<str:new_status>/', change_order_status, name='change_order_status'),
    path('generate-bill/<int:order_id>/', generate_bill, name='generate_bill'),
    path('menu-items/', MenuItemList.as_view(), name='menu-items-list'),



    #new addition
    path('aggregate_orders/', create_aggregate_order, name='create_aggregate_order'),
    path('api/aggregate-orders/', AggregateOrderListAPIView.as_view(), name='aggregate_order_list'),
    path('api/aggregate-orders/<int:pk>/', AggregateOrderRetrieveAPIView.as_view(), name='aggregate_order_detail'),
    path("update-order-status/<int:order_id>/", update_order_status, name="update-order-status"),
    path("download-bill/<int:order_id>/", download_bill, name="download-bill"),
    path('generate-qrcode/<int:table_id>/', views_multorder.generate_qr_code, name='generate_qr_code'),
    path('reservations/', ReservationCreateView.as_view(), name='reservation-create'),
    path('reservations/list/', ReservationListView.as_view(), name='reservation-list'),
    path('reservations/approve/<int:reservation_id>/', approve_reservation, name='approve_reservation'),
    path('table-status/<int:id>/', TableStatusUpdateAPIView.as_view(), name='table-status-update'),
    path('recommend-weather/', RecommendFoodByWeather.as_view()),
    path('testimonials/', TestimonialListAPIView.as_view(), name='testimonial-list'),
]

# For token authentication:
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import LoginAPIView

urlpatterns += [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("login/", LoginAPIView.as_view(), name="login"),
]
