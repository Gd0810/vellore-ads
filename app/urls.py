from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('all-categories/',views.all_categories,name='all_categories'),
    path('business-detail/<slug:slug>/',views.business_detail,name='business_detail'),
    path('business-blog/<slug:slug>/',views.business_blog,name='business_blog'),
    path('tourism-in-vellore/<slug:slug>/',views.tourism,name='tourism'),



    path('business/<int:business_id>/reviews/', views.business_reviews, name='business_reviews'),
    path('business/<int:business_id>/reviews/load/', views.load_more_reviews, name='load_more_reviews'),
    path('business-reviews-add/<int:business_id>/', views.add_review, name='add_review'),
    path('search/', views.search_business, name='search_business'),
    path('submit-enquiry/', views.submit_enquiry, name='submit_enquiry'),

    # Sub-subcategory route (deepest first to avoid conflict)
    path('<slug:location>/<slug:grandparent_slug>/<slug:parent_slug>/<slug:slug>/', views.category_detail, name='sub_subcategory_detail'),
    # Subcategory route
    path('<slug:location>/<slug:parent_slug>/<slug:slug>/', views.category_detail, name='subcategory_detail'),
    # Top-level category
    path('<slug:location>/<slug:slug>/', views.category_detail, name='category_detail'),
]
