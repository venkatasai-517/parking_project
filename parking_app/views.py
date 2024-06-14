from django.shortcuts import render, redirect
from .models import category, vehicle_entry
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.db.models import Count
from itertools import zip_longest
from datetime import datetime, timedelta
from django.utils.cache import add_never_cache_headers
# def transfer_data(request):
#     # Retrieve data from SourceTable
#     source_entries = category.objects.all()
#
#     # Iterate over each source entry and update corresponding destination entry
#     for source_entry in source_entries:
#         try:
#             # Retrieve the corresponding destination entry based on the foreign key relationship
#             dest_entry = vehicle_entry.objects.get(parking_area_number=source_entry)
#
#             # Update fields in the destination entry with values from the source entry
#             dest_entry.vehicle_type = source_entry.vehicle_type
#             dest_entry.parking_charge = source_entry.parking_charge
#             # dest_entry.unique_field_destination = source_entry.unique_field_source
#
#             # Save the updated destination entry
#             dest_entry.save()
#             vehicles = vehicle_entry.objects.all()
#             # context = {'vehicles': vehicles}
#
#         except vehicle_entry.DoesNotExist:
#             # Handle the case where no corresponding destination entry is found
#             # This could happen if a source entry doesn't have a matching destination entry
#             pass
#
#     return render(request, 'transfer_success.html')

def add_category(request):
    #fetching data from frontend using get method
    search_query = request.GET.get('query')
    if search_query:
        categoryy = category.objects.filter(vehicle_type__icontains=search_query)
    else:
        categoryy = category.objects.all()

    if request.method == 'POST':
        parking = request.POST['parking']
        type = request.POST['type']
        limit = request.POST['limit']
        charge = request.POST['charge']

        creating = category(parking_area_number=parking, vehicle_type=type, vehicle_limit=limit, parking_charge=charge)
        creating.save()
        return redirect('create_category')
    page_num = request.GET.get('pagee')  # creating the total pages
    paginator = Paginator(categoryy, 2)  # setting total number of products in a page : 2

    try:
        categoryy = paginator.page(page_num)
    except PageNotAnInteger:
        categoryy = paginator.page(1)
    except EmptyPage:
        categoryy = paginator.page(paginator.num_pages)

    categoriess = category.objects.all()
    context = {'categoryy': categoryy, 'categoriess':categoriess}


    return render(request, 'category.html', context)

def deactivate_category(request, id):
    Category = category.objects.get(id=id)
    Category.status = "deactivated"
    Category.save()
    return redirect('create_category')
# activating the category


def activate_category(request, id):
    Category = category.objects.get(id=id)
    Category.status = "activated"
    Category.save()
    return redirect('create_category')

def delete_category(request, id):
    Category = category.objects.get(id=id)
    Category.delete()
    return redirect('create_category')


def vehicles_entry(request):
    vehicle_type = category.objects.values_list('vehicle_type', flat=True).distinct()
    parking_charge = category.objects.values_list('parking_charge', flat=True).distinct()
    search_query = request.GET.get('query')
    if search_query:
        vehi = vehicle_entry.objects.filter(vehicle_no__contains=search_query)
    else:
        vehi = vehicle_entry.objects.all()
    if request.method == 'POST':
        vehicle_number = request.POST['vehicle_number']
        type = request.POST['type']
        parking_area_number_id = request.POST['parking_area_number']
        author = category.objects.get(parking_area_number=parking_area_number_id)
        charge = request.POST['charge']
        vehicle_entry.objects.create(vehicle_no=vehicle_number, vehicle_type=type, parking_area_number=author, parking_charge=charge)
        return redirect('vehicles_entry')
    page_num = request.GET.get('pagee')  # creating the total pages
    paginator = Paginator(vehi, 20)  # setting total number of products in a page : 2
    try:
        vehi = paginator.page(page_num)
    except PageNotAnInteger:
        vehi = paginator.page(1)
    except EmptyPage:
        vehi = paginator.page(paginator.num_pages)
    categoryy = category.objects.values_list('parking_area_number', flat=True)
    sai = category.objects.all()
    prasad = category.objects.values_list('vehicle_limit', flat=True)
    final=[]
    for category_instance in sai:
        count_per_category = vehicle_entry.objects.filter(parking_area_number=category_instance,status='parked').values('vehicle_type').annotate(total=Count('vehicle_type')).values_list('total', flat=True)
        vehicle_limit = category_instance.vehicle_limit
        available_space = int(vehicle_limit) - sum(count_per_category)
        final.append(available_space)
    # for j in vehicle_type_counts:
    #        n = int(j)
    #        l.append(n)
    # print(l)
    # s = []
    # for i in prasad:
    #     m = int(i)
    #     s.append(m)
    # final = []
    # for i in range(0, len(s)):
    #     final.append(s[i]-l[i])
    zipped_data = zip_longest(sai, final)
    context = {'vehicle_type': vehicle_type, 'parking_charge': parking_charge, 'vehi': vehi, 'categoryy': categoryy,'sai':zipped_data,'prasad': prasad}
    return render(request, 'vehicle_entry.html', context)

def manage_vehicles(request):
    search_query = request.GET.get('search')
    if search_query == None:
        ten_days_ago = datetime.now() - timedelta(days=3)
        vehicles = vehicle_entry.objects.filter(arrival_time__range=[ten_days_ago, datetime.now()])
    else:
        vehicles = vehicle_entry.objects.filter(vehicle_type__icontains=search_query)

    page_num = request.GET.get('pagee')  # creating the total pages
    paginator = Paginator(vehicles, 2)  # setting total number of products in a page : 2

    try:
        vehicles = paginator.page(page_num)
    except PageNotAnInteger:
        vehicles = paginator.page(1)
    except EmptyPage:
        vehicles = paginator.page(paginator.num_pages)


    context = {'vehicles': vehicles}
    return render(request, 'manage_vehicles.html', context)

def changing_status_based_on_action(request, id):
    manage = vehicle_entry.objects.get(id=id)
    if manage.status == "parked":
        manage.status = "leaved"
    else:
        manage.status = "parked"
    manage.save()
    return redirect('manage_vehicles')


def search(request):
    search_query = request.GET.get('search')
    if search_query == None:
        vehicles = vehicle_entry.objects.all()
    else:
        vehicles = vehicle_entry.objects.filter(vehicle_no__contains=search_query)
    context = {'vehicles': vehicles}
    return render(request, 'search.html', context)

def login(request):
    if request.method == "POST":
        users = request.POST['user']
        password = request.POST['pass']

        user = authenticate(request, username=users, password=password)
        if user is not None:
            return redirect('dashboard')
        else:
            return redirect('login')

    response = render(request, 'login.html')
    # Add cache control headers to prevent caching
    add_never_cache_headers(response)

    return response







def dashboard(request):
    vehicles_parked = vehicle_entry.objects.filter(status='parked').count()
    vehicles_departed = vehicle_entry.objects.filter(status='leaved').count()
    avail_cate = category.objects.all().count()
    earnings = vehicle_entry.objects.values_list('parking_charge', flat=True).filter(status='leaved')

    sh = 0
    for i in earnings:
           sh = sh + float(i)
    tot_earnings = int(sh)


    t_records = vehicle_entry.objects.all().count()
    vehicle_limits = category.objects.values_list('vehicle_limit', flat=True)
    total_vehicle_limit = sum(int(limit) for limit in vehicle_limits if limit.isdigit())

    context = {'parked': vehicles_parked, 'departed': vehicles_departed, 'tot_cate': avail_cate,'tot_earnings': tot_earnings, 't_records': t_records, 't_v_limit': total_vehicle_limit}
    response = render(request, 'dashboard.html', context)
    # Add cache control headers to prevent caching
    add_never_cache_headers(response)

    return response


def change_password(request):
    if request.method == "POST":
        password = request.POST.get('current', '')
        password1 = request.POST.get('n_pass1', '')
        password2 = request.POST.get('n_pass2', '')

        user = authenticate(request, username=request.user.username, password=password)
        if user is not None:
            if password1 == password2:
                user.set_password(password1)
                user.save()
    return render(request, 'account.html')
# def change_password(request):
#     if request.method == "POST":
#         current_password = request.POST.get('current', '')
#         new_password1 = request.POST.get('n_pass1', '')
#         new_password2 = request.POST.get('n_pass2', '')
#
#         user = authenticate(request, username=request.user.username, password=current_password)
#
#         if user is not None:
#             if new_password1 == new_password2:
#                 # Change password only if new passwords match
#                 user.set_password(new_password1)
#                 user.save()
#                 messages.success(request, 'Password successfully updated!')
#
#             else:
#                 messages.error(request, 'New passwords do not match.')
#         else:
#             messages.error(request, 'Invalid current password.')
#
#     return render(request, 'account.html')

def logouts(request):
    logout(request)
    return redirect('login')






def base(request):
    # Assuming there's only one superuser in the system
    superuser = User.objects.filter(is_superuser=True).first()
    superuser_username = superuser.username if superuser else None
    # Now you can use superuser_username in your view logic
    # For example, you can pass it to the template context or perform any further operations

    return render(request, 'base.html', {'user': superuser_username})

def editss(request,id):
    edits = vehicle_entry.objects.get(id=id)
    context = {'edits': edits}
    return render(request, 'category.html', context)
def navbar(request):
    return render(request,"main.html")













