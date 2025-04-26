from django.shortcuts import render , HttpResponse , redirect
from django.contrib.auth import logout , login , authenticate
from django.contrib.auth.models import User
from .models import RegisteredUser
import csv
from .models import BloodBank , Ambulance , AnnouncementStaff , AddStaffRequest , MessageUser , Requests , Appointments
import indian_names
import random
import datetime
 

# ERROR MESSAGES
def error_404(request,exception):
    return render(request, 'error_page.html',status=404)

def error_500(request):
     return render(request, 'error_page.html',status=500)




# █▀▀ █▀█ █▀▄▀█ █▀▄▀█ █▀█ █▄░█   ▀█▀ █▀█   ▄▀█ █░░ █░░
# █▄▄ █▄█ █░▀░█ █░▀░█ █▄█ █░▀█   ░█░ █▄█   █▀█ █▄▄ █▄▄

# URL : /
# DESC : this is welcome page 
def home(request):
    return render(request,"welcome.html")

# URL : /user/home/
# DESC : this is the home page and for each category of user different pages are rendered
# and if the user is not logged in he will be redirected to login page
def user_home(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return render(request,"admin_home.html")    
        if request.user.is_staff:
            return render(request,"staff_home.html")    
        else:
            return render(request,"user_home.html")
    return redirect('/login/')

# URL : /login/
# DESC : this is login page 
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user:
            login(request,user)
            return redirect('/user/home/')
    return render(request,"login_user.html")

# URL : /logout/
# DESC : this is logout page
def logout_user(request):
    logout(request)
    return redirect('/')

# URL : /create_user/
# DESC : this is create user page
def create_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if username and email and password:
            user = User.objects.create_user(username=username,email=email,password=password)
            user.save()
            user = authenticate(request,username=username,password=password)
            if user:
                login(request,user)
                return redirect('/user/complete_profile/')
    return render(request,"create_user.html")

# URL : /cuser/complete_profile/
# DESC : this page comes only after create user page and store the addition 
# information about user appart from email and password
def complete_profile(request):
    if request.method == 'POST':
        user_id = request.user.id
        user_username = request.user.username
        name = request.POST.get('name')
        email = request.user.email
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')
        if user_id and user_username and name and email and mobile and address:
            ru = RegisteredUser(user_id=user_id , user_username=user_username , name=name , email=email , mobile=mobile , address=address)
            ru.save()
            return redirect('/user/home/')
    return render(request,"user_complete_profile.html")




# █▄░█ █▀█ █▀█ █▀▄▀█ ▄▀█ █░░   █░█ █▀ █▀▀ █▀█   █▀▀ ▄▀█ █▀▀ █ █░░ █ ▀█▀ █ █▀▀ █▀
# █░▀█ █▄█ █▀▄ █░▀░█ █▀█ █▄▄   █▄█ ▄█ ██▄ █▀▄   █▀░ █▀█ █▄▄ █ █▄▄ █ ░█░ █ ██▄ ▄█




# BLOOD SECTION FUNCTIONS________________________

# URL : /user/blood_bank/
# DESC : this is the input page for blood bank and then redirect to the blood bank query page
def user_blood_bank(request):
    cities = []
    for i in BloodBank.objects.values('state','city').distinct():
        cities.append([i['state'],i['city']])
    data = tuple(cities)
    context = {
        'data':data
    }
    return render(request,"user_blood_bank.html",context)

# URL : /user/blood_bank/<str:state>/<str:city>/
# DESC : this is the query page for blood bank and it shows all the data of the given state , city
def user_blood_bank_state_city(request,state,city):
    state = state.lower()
    city = city.lower()
    cities = []
    for i in BloodBank.objects.values('state','city').distinct():
        cities.append([i['state'],i['city']])
    data = tuple(cities)
    context = {
        'state':state,
        'city':city,
        'data':BloodBank.objects.all().filter(state=state.strip(),city=city.strip()),
        'inps':data
    }
    return render(request,"user_blood_bank_state_city.html",context)

# URL : /user/blood_bank/blood_bank_details/<int:id>/
# DESC : this page takes a id and return all the information of blood ban having that id
def user_blood_bank_details_id(request,id):
    data = BloodBank.objects.get(id=id)
    context = {
        'data':data,
        'id':id,
    }
    return render(request,"bank_details.html",context)

# URL : /user/blood_bank/blood_bank_details/<int:id>/donate/
# DESC : this page opens when user click on donate button. 
# this page takes some user details regarding blood donation
# then it send that request message to the bank on whose page we clicked the button 
def user_blood_bank_details_id_donate(request,id):
    if request.method == 'POST':
        user_id = request.user.id
        bank_id = id
        service = 'donate'
        blood_units = request.POST.get('units')
        blood_type = request.POST.get('group')
        diseases = request.POST.get('diseases')
        request_message = request.POST.get('message')
        print(user_id,bank_id,service,blood_units,blood_type,diseases,request_message)
        request_donate = Requests(
            user_id = user_id,
            bank_id = bank_id,
            service = service,
            blood_units = blood_units,
            blood_type = blood_type,
            diseases = diseases,
            request_message = request_message,
        )
        request_donate.save()
        msg = MessageUser(
            user_id = request.user.id,
            admin_id = ' ',
            staff_id = ' ',
            sent_admin = False,
            date_send = datetime.datetime.now().date(),
            message = "Your Donate Blood Request Has been Sent",
        )
        msg.save()
        return redirect(f'/user/home/')
    return render(request,"user_donate_form.html",{'id':id})

# URL : /user/blood_bank/blood_bank_details/<int:id>/receive/
# DESC : this page opens when user click on receive button. 
# this page takes some user details regarding blood receiving
# then it send that request message to the bank on whose page we clicked the button 
def user_blood_bank_details_id_receive(request,id):
    if request.method == 'POST':
        user_id = request.user.id
        bank_id = id
        service = 'receive'
        blood_units = request.POST.get('units')
        blood_type = request.POST.get('group')
        diseases = request.POST.get('diseases')
        request_message = request.POST.get('message')
        print(user_id,bank_id,service,blood_units,blood_type,diseases,request_message)
        request_donate = Requests(
            user_id = user_id,
            bank_id = bank_id,
            service = service,
            blood_units = blood_units,
            blood_type = blood_type,
            diseases = diseases,
            request_message = request_message,
        )
        request_donate.save()
        msg = MessageUser(
            user_id = request.user.id,
            admin_id = ' ',
            staff_id = ' ',
            sent_admin = False,
            date_send = datetime.datetime.now().date(),
            message = "Your Receive Blood Request Has been Sent",
        )
        msg.save()
        return redirect(f'/user/home/')
    return render(request,"user_donate_form.html",{'id':id})




# AMBULANCE SECTION FUNCTIONS______________________

# URL : /user/ambulance/
# DESC : this is the input page for ambulance and then redirect to the ambulance query page
def user_ambulance(request):
    cities = []
    for i in Ambulance.objects.values('state','city').distinct():
        cities.append([i['state'],i['city']])
    data = tuple(cities)
    context = {
        'data':data
    }
    return render(request,"user_ambulance.html",context)

# URL : /user/ambulance/<str:state>/<str:city>/
# DESC : this is the query page for ambulance and it returns all the ambulances data in the given state , city
def user_ambulance_state_city(request,state,city):
    state = state.lower()
    city = city.lower()
    cities = []
    for i in Ambulance.objects.values('state','city').distinct():
        cities.append([i['state'],i['city']])
    data = tuple(cities)
    context = {
        'state':state,
        'city':city,
        'data':Ambulance.objects.all().filter(state=state.strip(),city=city.strip()),
        'inps':data
    }
    return render(request,"user_ambulance_state_city.html",context)




# SETTINGS SECTION FUNCTIONS _________________________________

# URL : /user/settings/
# DESC : this page all the additional options regarding user
def user_settings(request):
    return render(request,"user_settings.html")

# URL : /user/settings/edit_profile/
# DESC : this page allows the user to update the details given in complete profile page
def user_settings_edit_profile(request):
    if request.method == 'POST':
        profile = RegisteredUser.objects.get(user_id=request.user.id)
        profile.user_id=request.user.id
        profile.user_username = User.objects.get(id=request.user.id).username
        profile.name = request.POST.get('name')
        profile.email = User.objects.get(id=request.user.id).email
        profile.mobile = request.POST.get('mobile')
        profile.age = request.POST.get('age')
        profile.address = request.POST.get('address')
        profile.save()
        return redirect('/user/settings/')
    context = {
        'data':RegisteredUser.objects.get(user_id=request.user.id)
    }
    return render(request,'user_seting_edit_profile.html',context)

# URL : /user/settings/memeber/blood_bank/
# DESC : this page allows the user to send the request to admin for regestring its blood 
# bank and become a member 
def user_settings_member_blood_bank(request):
    if request.method == 'POST':
        blood_groups = request.POST.get('bank_groups')
        r = AddStaffRequest(
            user_id = request.user.id,
            admin_id = User.objects.all().filter(is_superuser=True)[0],
            blood_bank_name = request.POST.get('bank_name'),
            address = request.POST.get('bank_address'),
            state = f'{request.POST.get('bank_state')}'.lower(),
            city = f'{request.POST.get('bank_city')}'.lower(),
            mobile = request.POST.get('bank_mobile'),
            email = request.POST.get('bank_email'),
            category = f'{request.POST.get('bank_category')}'.lower(),
            status = request.POST.get('bank_status'),
            website = request.POST.get('bank_website'),
            blood_groups =  blood_groups.split(','),
            A_positive_units = request.POST.get('A_positive_units'),
            A_negative_units = request.POST.get('A_negative_units'),
            B_positive_units = request.POST.get('B_positive_units'),
            B_negative_units = request.POST.get('B_negative_units'),
            AB_positive_units = request.POST.get('O_positive_units'),
            AB_negative_units = request.POST.get('O_negative_units'),
            O_positive_units = request.POST.get('AB_positive_units'),
            O_negative_units = request.POST.get('AB_negative_units'),
            date_send = datetime.datetime.now().date(),
            request_message = request.POST.get('request_message'),
        )
        r.save()
        msg = MessageUser(
            user_id = request.user.id,
            admin_id = ' ',
            staff_id = ' ',
            sent_admin = False,
            date_send = datetime.datetime.now().date(),
            message = "Your Blood Bank Request Has been Sent",
        )
        msg.save()
        return redirect('/user/settings/')
    return render(request,'user_add_blood_bank.html')




# INBOX SECTION FUNCTION _________________________________________

# URL : /user/inbox/
# DESC : this page displays all the messages sent to user's id 
def user_inbox(request):
    data = []
    for i in MessageUser.objects.all().filter(user_id=request.user.id):
        lst = [i]
        if i.message.startswith('[Accepted!]'):
            lst.append(['Request Accepted !!','check','success','Admin',i.id])
        elif i.message.startswith('[Declined!]'):
            lst.append(['Request Declined !!','xmark','fail','Admin',i.id])

        elif i.message.startswith('Your Donate Blood Request Has been Sent'):
            lst.append(['Request Sent !!','check','success','You',i.id])
        elif i.message.startswith('Your Receive Blood Request Has been Sent'):
            lst.append(['Request Sent !!','check','success','You',i.id])

        elif i.message.startswith('Your Blood Bank Request Has been Sent'):
            lst.append(['Request Sent !!','check','success','You',i.id])

        elif i.message.startswith('[Appointment Booked]'):
            lst.append(['Appointment Booked !!','check','success','Blood Bank',i.id])
        elif i.message.startswith('[Appointment Request Declined]'):
            lst.append(['Appointment Request Canceled !!','xmark','fail','Blood Bank',i.id])
        data.append(lst)
    context = {
        'data':data,
    }
    return render(request,"user_inbox.html",context)

# URL : /user/inbox/read/<int:id>/
# DESC : this page dallows the user to open and view complete message
def user_inbox_read(request,id):
    data = MessageUser.objects.get(id=id)
    context = {
        'data':data,
        'id':id,
    }
    return render(request,"user_inbox_read.html",context)

# URL : /user/inbox/read/<int:id>/mark_read/
# DESC : this is not a its a funtion which deletes the message after user read and click on done
def user_inbox_read_mark_read(request,id):
    data = MessageUser.objects.get(id=id)
    data.delete()
    return redirect('/user/inbox/')


# APPOINTMENT SECTION FUNCTIONS ____________________________________________

# URL : /user/appointments/
# DESC : this page all the appointments of the user
def user_appointments(request):
    data_all = Appointments.objects.all().filter(user_id=request.user.id)
    data = []
    for i in data_all:
        lst = [BloodBank.objects.get(id=i.bank_id).name , i.id , i.on_date]
        data.append(lst)
    context = {
        'data_all':data_all,
        'data':data,
    }
    return render(request,"user_appointments.html",context)

# URL : /user/appointments/view/<int:id>/
# DESC : this page show details of a perticular appointment using its id
def user_appointments_view(request,id):
    data = Appointments.objects.get(id=id)
    context = {
        'data':data,
        'bank':BloodBank.objects.get(id=data.bank_id).name
        # 'data':data,
    }
    return render(request,"user_appointment_view.html",context)





# ▄▀█ █▀▄ █▀▄▀█ █ █▄░█   █░█ █▀ █▀▀ █▀█   █▀▀ ▄▀█ █▀▀ █ █░░ █ ▀█▀ █ █▀▀ █▀
# █▀█ █▄▀ █░▀░█ █ █░▀█   █▄█ ▄█ ██▄ █▀▄   █▀░ █▀█ █▄▄ █ █▄▄ █ ░█░ █ ██▄ ▄█



# MEMBERSHIP SECTION ADMIN______________________________________

# URL : /user/admin/membership_requests/
# DESC : this shows all the requests from users
def user_admin_membership_requests(request):
    data = []
    for i in AddStaffRequest.objects.all():
        data.append([i,User.objects.all().get(id=i.user_id).username])
    context = {
        'data': data,
        'bank':'fa-hand-holding-droplet',
        # 'ambulance':'fa-truck-medical',

    }
    return render(request,"admin_membership.html",context)

# URL : /user/admin/membership_requests/open/<int:id>
# DESC : displays all the details of the select request using its id
def user_admin_membership_requests_open(request,id):
    context = {
        'data': AddStaffRequest.objects.all().get(id=id),
        'id':id,
    }
    return render(request,"member_request_details.html",context)

# URL : /user/admin/membership_requests/open/<int:id>/accept/
# DESC : this is not a page its a function which is executed when admin accepts a request.
# this function takes all the data of the users blood bank and add it to database 
# and it also update the user profile to staff profile. 
# Then it send a congratulations message to the user
def user_admin_membership_requests_open_accept(request,id):
    obj = AddStaffRequest.objects.all().get(id=id)
    msg = MessageUser(
        user_id = obj.user_id,
        admin_id = request.user.id,
        staff_id = ' ',
        sent_admin = True,
        date_send = datetime.datetime.now().date(),
        message = '''[Accepted!]
                    Admin 
                    Congratulations !! .
                    Your request has been accepted. 
                    Your account has been update to staff account. '''
    )
    msg.save()
    d = BloodBank(
        user_id = obj.user_id,
        name = obj.blood_bank_name,
        address = obj.address,
        state = obj.state,
        city = obj.city,
        mobile = obj.mobile,
        email = obj.email,
        category = obj.category,
        status = obj.status,
        website = obj.website,
        blood_groups =  obj.blood_groups,
        A_positive_units = obj.A_positive_units,
        A_negative_units = obj.A_negative_units,
        B_positive_units = obj.B_positive_units,
        B_negative_units = obj.B_negative_units,
        AB_positive_units = obj.AB_positive_units,
        AB_negative_units = obj.AB_negative_units,
        O_positive_units = obj.O_positive_units,
        O_negative_units = obj.O_negative_units,
    )
    d.save()
    user = User.objects.get(id=obj.user_id)
    user.is_staff = True
    user.save()
    AddStaffRequest.objects.all().get(id=id).delete()
    return redirect('/user/admin/membership_requests/')

# URL : /user/admin/membership_requests/open/<int:id>/decline/
# DESC : this is not a page its a function which is executed when admin declines a request.
# this function deletes all the given data and send the user a message that their request has been denied
def user_admin_membership_requests_open_decline(request,id):
    msg = MessageUser(
        user_id = AddStaffRequest.objects.all().get(id=id).user_id,
        admin_id = request.user.id,
        staff_id = ' ',
        sent_admin = True,
        date_send = datetime.datetime.now().date(),
        message = '''[Declined!]
                    Admin ,
                    Sorry !! .
                    Your request has been declined.'''
    )
    msg.save()
    AddStaffRequest.objects.all().get(id=id).delete()
    return redirect('/user/admin/membership_requests/')



# ANNOUNCE SECTION FUNCTION ____________________________________________

# URL : /user/admin/announce/
# DESC : this is the announcement form which takes data from admin and anunce it to all staff
def user_admin_announce(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        message = request.POST.get('message')
        if title and message:
            staff = User.objects.all().filter(is_staff=True)
            for i in staff:
                a = AnnouncementStaff(
                    message = message,
                    title = title,
                    admin_id = request.user.id,
                    staff_id = i.id,
                )
                a.save()
            return redirect('/user/admin/announce/all/')
    return render(request,"admin_staff_announcement_form.html")
    
# URL : /user/admin/announce/all/
# DESC : this page displays the announcement sent on his user id
def user_admin_announce_all(request):
    data = AnnouncementStaff.objects.all().filter(staff_id=request.user.id)
    # print()
    context = {
        'data':data,
    }
    return render(request,"admin_announcements.html",context)

# URL : /user/admin/announce/all/<int:id>/
# DESC : this page displays the full anouncement using the anouncement id
def user_admin_announce_all_id(request,id):
    data = AnnouncementStaff.objects.get(id=id)
    # print()
    context = {
        'data':data,
    }
    return render(request,"admin_anouncement_view.html",context)

# URL : /user/admin/announce/all/<int:id>/mark_read/
# DESC : this is not a page it a function which is executed when user click on mark read.
# it deletes the announcement having the user id
def user_admin_announce_all_id_readed(request,id):
    data = AnnouncementStaff.objects.get(id=id)
    data.delete()
    return redirect('/user/admin/announce/all/')





# █▀ ▀█▀ ▄▀█ █▀▀ █▀▀   █░█ █▀ █▀▀ █▀█   █▀▀ ▄▀█ █▀▀ █ █░░ █ ▀█▀ █ █▀▀ █▀
# ▄█ ░█░ █▀█ █▀░ █▀░   █▄█ ▄█ ██▄ █▀▄   █▀░ █▀█ █▄▄ █ █▄▄ █ ░█░ █ ██▄ ▄█



# REQUEST SECTION OF STAFF USERS __________________________________

# URL : /user/staff/requests/
# DESC : this page show all the blood request send to their blood bank
def user_staff_requests(request):
    bank_id = BloodBank.objects.get(user_id=request.user.id).id
    requests = Requests.objects.all().filter(bank_id=bank_id)
    data = []
    for i in requests:
        lst = [RegisteredUser.objects.get(user_id=i.user_id).name,BloodBank.objects.get(id=bank_id).name , i.id,i.service]
        data.append(lst)
    context = {
        'data':data,
    }
    return render(request,"staff_requests.html",context)

# URL : /user/staff/requests/<int:id>/
# DESC : this page show all the details of the selected blood bank
def user_staff_requests_id(request,id):
    bank_id = BloodBank.objects.get(user_id=request.user.id).id
    requests = Requests.objects.get(id=id)
    diseases = "No Diseases"
    if requests.diseases:
        diseases = request.diseases
    context = {
        'data':requests,
        'name':RegisteredUser.objects.get(user_id=requests.user_id).name,
        'blood_bank_name':BloodBank.objects.get(id=bank_id).name,
        'service':requests.service,
        'diseases':diseases,
        'id':id,
    }
    return render(request,"request_details.html",context)


# URL : /user/staff/requests/<int:id>/book_appointment/
# DESC : this page take the date and time from blood bank user and book the appointment
# it also send a appointment confirmation message to the user
def user_staff_requests_id_book_appointment(request,id):
    if request.method == 'POST':
        data = Requests.objects.get(id=id)
        app = Appointments(
            user_id = data.user_id,
            name = RegisteredUser.objects.get(user_id=data.user_id).name,
            bank_id = data.bank_id,
            on_date = request.POST.get('date'),
            service = data.service,
            blood_type = data.blood_type,
            blood_units = data.blood_units,
            time_from = request.POST.get('from'),
            time_to = request.POST.get('to'),
            )
        app.save()
        msg = MessageUser(
            user_id = data.user_id,
            admin_id = ' ',
            staff_id = request.user.id,
            sent_admin = False,
            date_send = datetime.datetime.now().date(),
            message = '''[Appointment Booked]
                        Bank ,
                        Congratulations !! .
                        Your appointment is booked successfully.'''
        )
        msg.save()  
        data.delete()
        return redirect('/user/home/')
    return render(request,'staff_book_appointment_form.html')

# URL : /user/staff/requests/<int:id>/cancel_request/
# DESC : this page cancels the request and it also sends a cancel appointment message to the user
def user_staff_requests_id_cancel_requests(request,id):
    data = Requests.objects.get(id=id)
    msg = MessageUser(
        user_id = data.user_id,
        admin_id = ' ',
        staff_id = request.user.id,
        sent_admin = False,
        date_send = datetime.datetime.now().date(),
        message = '''[Appointment Request Declined]
                    Bank ,
                    Congratulations !! .
                    Your appointment is booked successfully.'''
    )
    msg.save()  
    data.delete()
    return redirect('/user/home/')


# SETTINGS SECTION OF STAFF __________________________________

# URL : /user/staff/settings/
# DESC : this page all the additional options regarding staff
def user_staff_settings(request):
    return render(request,"staff_settings.html")

# URL : /user/staff/settings/edit_profile/
# DESC : this page allows the user to update the details given in complete profile page
def user_staff_settings_edit_profile(request):
    if request.method == 'POST':
        profile = RegisteredUser.objects.get(user_id=request.user.id)
        profile.user_id=request.user.id
        profile.user_username = User.objects.get(id=request.user.id).username
        profile.name = request.POST.get('name')
        profile.email = User.objects.get(id=request.user.id).email
        profile.mobile = request.POST.get('mobile')
        profile.age = request.POST.get('age')
        profile.address = request.POST.get('address')
        profile.save()
        return redirect('/user/settings/')
    context = {
        'data':RegisteredUser.objects.get(user_id=request.user.id)
    }
    return render(request,'staff_seting_edit_profile.html',context)

# URL : /user/staff/settings/edit_bank_profile/
# DESC : this page allows the user to update the blood bank details
def user_staff_settings_edit_bank_profile(request):
    if request.method == 'POST':
        blood_groups = request.POST.get('bank_groups')
        bank = BloodBank.objects.get(user_id=request.user.id)
        bank.user_id = request.user.id
        bank.name = request.POST.get('bank_name')
        bank.address = request.POST.get('bank_address')
        bank.state = f'{request.POST.get('bank_state')}'.lower()
        bank.city = f'{request.POST.get('bank_city')}'.lower()
        bank.mobile = request.POST.get('bank_mobile')
        bank.email = request.POST.get('bank_email')
        bank.category = f'{request.POST.get('bank_category')}'.lower()
        bank.status = request.POST.get('bank_status')
        bank.website = request.POST.get('bank_website')
        bank.blood_groups =  blood_groups.split(',')
        bank.A_positive_units = request.POST.get('A_positive_units')
        bank.A_negative_units = request.POST.get('A_negative_units')
        bank.B_positive_units = request.POST.get('B_positive_units')
        bank.B_negative_units = request.POST.get('B_negative_units')
        bank.AB_positive_units = request.POST.get('O_positive_units')
        bank.AB_negative_units = request.POST.get('O_negative_units')
        bank.O_positive_units = request.POST.get('AB_positive_units')
        bank.O_negative_units = request.POST.get('AB_negative_units')
        bank.save()
        return redirect('/user/staff/settings/')
    context = {
        'data':BloodBank.objects.get(user_id=request.user.id)
    }
    return render(request,'edit_blood_bank_details.html',context)



# ANNOUNCE SECTION IN STAFF ____________________________________________________

# URL : /user/staff/announce/all/
# DESC : this page displays the announcement sent on his user id
def user_staff_announce_all(request):
    data = AnnouncementStaff.objects.all().filter(staff_id=request.user.id)
    # print()
    context = {
        'data':data,
    }
    return render(request,"staff_announcements.html",context)

# URL : /user/staff/announce/all/<int:id>/
# DESC : this page displays the full anouncement using the anouncement id
def user_staff_announce_all_id(request,id):
    data = AnnouncementStaff.objects.get(id=id)
    # print()
    context = {
        'data':data,
    }
    return render(request,"staff_anouncement_view.html",context)

# URL : /user/staff/announce/all/<int:id>/mark_read/
# DESC : this is not a page it a function which is executed when user click on mark read.
# it deletes the announcement having the user id
def user_staff_announce_all_id_readed(request,id):
    data = AnnouncementStaff.objects.get(id=id)
    data.delete()
    return redirect('/user/staff/announce/all/')




# STAFF ANOUNCEMENT FUNCTIONS ______________________________

# URL : /user/staff/appointments/
# DESC : this page all the appointments of the user
def user_staff_appointments(request):
    bank = BloodBank.objects.get(user_id=request.user.id).id
    data_all = Appointments.objects.all().filter(bank_id=bank)
    data = []
    for i in data_all:
        # lst = [BloodBank.objects.get(id=i.bank_id).name , i.id , i.on_date]
        lst = [i.name , i.id , i.on_date]
        data.append(lst)
    context = {
        'data_all':data_all,
        'data':data,
    }
    return render(request,"user_staff_appointments.html",context)

# URL : /user/staff/appointments/view/<int:id>/
# DESC : this page show details of a perticular appointment using its id
def user_staff_appointments_view(request,id):
    data = Appointments.objects.get(id=id)
    context = {
        'data':data,
        'bank':BloodBank.objects.get(id=data.bank_id).name
        # 'data':data,
    }
    return render(request,"user_staff_appointment_view.html",context)

# URL : /user/staff/appointments/view/<int:id>/complete/
# DESC : this is function which deletes the appointment from the database when complete is clicked
def user_staff_appointments_view_complete(request,id):
    data = Appointments.objects.get(id=id)
    data.delete()
    return redirect('/user/staff/appointments/')



