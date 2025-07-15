from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            request.session['show_toast'] = True  
            return redirect('home')
        else:
            return render(request, 'restaurant_app/login.html', {'error': 'Invalid credentials'})
    return render(request, 'restaurant_app/login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def home(request):
    show_toast = request.session.pop('show_toast', False)
    return render(request, 'restaurant_app/home.html', {'show_toast': show_toast})

@login_required
def menu(request):
    return render(request, 'restaurant_app/menu.html')

@login_required
def contact(request):
    return render(request, 'restaurant_app/contact.html')

@login_required
def reservation(request):
    if request.method == 'POST':
        name = request.POST['name']
        date = request.POST['date']
        time = request.POST['time']
        people = request.POST.get('guests')  # ✅ Fixed indentation

        # Store details in session
        request.session['reservation_data'] = {
            'name': name,
            'date': date,
            'time': time,
            'people': people,
        }
        request.session['reservation_success'] = True
        return redirect('reservation')

    show_popup = request.session.pop('reservation_success', False)
    reservation_data = request.session.get('reservation_data', None)
    return render(request, 'restaurant_app/reservation.html', {
        'show_popup': show_popup,
        'reservation_data': reservation_data
    })
