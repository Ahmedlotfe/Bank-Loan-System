from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, LoanFundViewSet, LoanViewSet, AmortizationScheduleViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'loan-funds', LoanFundViewSet)
router.register(r'loans', LoanViewSet)
router.register(r'amortization', AmortizationScheduleViewSet)

urlpatterns = [
    path('', include(router.urls)),
    
    # JWT Authentication Endpoints
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
