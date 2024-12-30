from django.urls import path
from . import views
from .views import TableListAPIView, ContactAPIView

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
    path('reservations/', views.ReservationListCreateAPIView.as_view(), name='reservation-list-create'),
    path('reservations/<int:pk>/', views.ReservationRetrieveUpdateDestroyAPIView.as_view(), name='reservation-detail'),

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
]

# For token authentication:
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import LoginAPIView

urlpatterns += [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("login/", LoginAPIView.as_view(), name="login"),
]
