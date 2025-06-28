from django.shortcuts import render,get_object_or_404,redirect
from django.core.paginator import Paginator
from .forms import BusinessForm,BusinessFormForAdmin
from app.models import Business,Enquiry

# Create your views here.


def index(request):
    business = Business.objects.filter(user=request.user)
    return render(request,'dashboard/pages/index.html')


def delete_business(request, id):
    business = get_object_or_404(Business, id=id)
    if request.method == "POST":
        business.delete()
        return redirect('business_list')
    return redirect('business_list')



def user_business_list(request):
    if request.user.is_anonymous:
        return redirect('login')
    elif request.user.is_superuser:
        business = Business.objects.all()
        paginator = Paginator(business, 4)  # 8 business per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'dashboard/pages/business.html', {'business': page_obj})
    else:
        business = Business.objects.filter(user=request.user)
        paginator = Paginator(business, 4)  # 8 business per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'dashboard/pages/business.html', {'business': page_obj})
    
from django.contrib.auth.decorators import login_required

@login_required
def user_business_enquires(request):
    enquires = Enquiry.objects.filter(enquired_business__user=request.user)
    paginator = Paginator(enquires, 10)  # Adjust items per page as needed
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'dashboard/pages/business_enquires.html', {'enquires': page_obj})
 
from django.http import HttpResponseForbidden
@login_required
def delete_enquiry(request, id):
    enquiry = get_object_or_404(Enquiry, id=id)

    # Ensure the user owns the business
    if enquiry.enquired_business.user != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("You are not allowed to delete this enquiry.")

    if request.method == "POST":
        enquiry.delete()
        return redirect('user_business_enquires')  # Replace with your actual URL name

    return HttpResponseForbidden("Invalid request method.") 

def business_create(request):
    if request.method == "POST":
        form = BusinessForm(request.POST, request.FILES)
        if form.is_valid():
            business = form.save(commit=False)  # Don't save yet
            business.user = request.user  # Assign logged-in user
            business.save()  # Now save the object
            form.save()
            return redirect('business_list')
    else:
        form = BusinessForm()
    return render(request, 'dashboard/pages/create_business.html', {'form': form})



def business_edit(request, id):
    business = get_object_or_404(Business, id=id)
    if request.method == "POST":
        if request.user.is_superuser:
            form = BusinessFormForAdmin(request.POST, request.FILES, instance=business)
        else:
            form = BusinessForm(request.POST, request.FILES, instance=business)
        if form.is_valid():
            form.save()
            return redirect('user_business_list')
    else:
        if request.user.is_superuser:
            form = BusinessFormForAdmin(instance=business)
        else:
            form = BusinessForm(instance=business)
    return render(request, 'dashboard/pages/edit_business.html', {'form': form})
