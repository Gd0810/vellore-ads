from django.shortcuts import render
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required

def role_required(role):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.role == role:
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("You are not authorized to view this page.")
        return _wrapped_view
    return decorator

@login_required
@role_required('client')
def client_dashboard(request):
    return render(request, 'client_dashboard.html')

@login_required
@role_required('user')
def user_dashboard(request):
    return render(request, 'user_dashboard.html')


def index(request):
    return render(request,'index.html')




from django.shortcuts import get_object_or_404, render
# from .models import Category

def category_detail(request, **kwargs):
    slug = kwargs.get('slug')
    parent_slug = kwargs.get('parent_slug')
    grandparent_slug = kwargs.get('grandparent_slug')

    if grandparent_slug:
        # Sub-subcategory
        category = get_object_or_404(
            Category,
            slug=slug,
            parent__slug=parent_slug,
            parent__parent__slug=grandparent_slug
        )
    elif parent_slug:
        # Subcategory
        category = get_object_or_404(
            Category,
            slug=slug,
            parent__slug=parent_slug
        )
    else:
        # Top-level category
        category = get_object_or_404(
            Category,
            slug=slug,
            parent=None
        )

    return render(request, 'category_detail.html', {
        'category': category,
        'subcategories': category.get_subcategories()
    })

