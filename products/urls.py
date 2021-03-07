from rest_framework.routers import DefaultRouter

from .views import CategoryViewSets, ProductViewSets

router = DefaultRouter()
router.register(r'categories', CategoryViewSets, basename='category')
router.register(r'products', ProductViewSets, basename='products')
urlpatterns = router.urls
