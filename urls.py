from django.contrib import admin
from django.urls import path 
from . import views


admin.site.site_header = "Lifeblood | Admin"
admin.site.site_title = "Lifeblood"
admin.site.index_title = "Welcome Admin"

urlpatterns = [
    path('',views.home),
    path('login/',views.login_user),
    path('logout/',views.logout_user),
    path('user/home/',views.user_home),
    path('create_user/',views.create_user),
    path('user/complete_profile/',views.complete_profile),

    # BLOOD BANK URLS
    path('user/blood_bank/',views.user_blood_bank),
    path('user/blood_bank/blood_bank_details/<int:id>/',views.user_blood_bank_details_id),
    path('user/blood_bank/blood_bank_details/<int:id>/donate/',views.user_blood_bank_details_id_donate),
    path('user/blood_bank/blood_bank_details/<int:id>/receive/',views.user_blood_bank_details_id_receive),
    path('user/blood_bank/<str:state>/<str:city>/',views.user_blood_bank_state_city),
    
    # AMBULANCE URLS
    path('user/ambulance/',views.user_ambulance),
    path('user/ambulance/<str:state>/<str:city>/',views.user_ambulance_state_city),

    # USER INBOX URLS
    path('user/inbox/',views.user_inbox),
    path('user/inbox/read/<int:id>/',views.user_inbox_read),
    path('user/inbox/read/<int:id>/mark_read/',views.user_inbox_read_mark_read),
    
    # USER APPOINTMENT URLS
    path('user/appointments/',views.user_appointments),
    path('user/appointments/view/<int:id>/',views.user_appointments_view),
    
    # USER SETTINGS URLS
    path('user/settings/',views.user_settings),
    path('user/settings/edit_profile/',views.user_settings_edit_profile),
    path('user/settings/memeber/blood_bank/',views.user_settings_member_blood_bank),


    # STAFF RECEIVING BLOOD REQUESTS URLS
    path('user/staff/requests/',views.user_staff_requests),
    path('user/staff/requests/<int:id>/',views.user_staff_requests_id),
    path('user/staff/requests/<int:id>/book_appointment/',views.user_staff_requests_id_book_appointment),
    path('user/staff/requests/<int:id>/cancel_request/',views.user_staff_requests_id_cancel_requests),

    # STAFF SETTINGS URLS
    path('user/staff/settings/',views.user_staff_settings),
    path('user/staff/settings/edit_profile/',views.user_staff_settings_edit_profile),
    path('user/staff/settings/edit_bank_profile/',views.user_staff_settings_edit_bank_profile),
    
    # STAFF ANNOUNCEMENT URLS
    path('user/staff/announce/all/',views.user_staff_announce_all),
    path('user/staff/announce/all/<int:id>/',views.user_staff_announce_all_id),
    path('user/staff/announce/all/<int:id>/mark_read/',views.user_staff_announce_all_id_readed),

    # STAFF APPOINTMENT URLS
    path('user/staff/appointments/',views.user_staff_appointments),
    path('user/staff/appointments/view/<int:id>/',views.user_staff_appointments_view),
    path('user/staff/appointments/view/<int:id>/complete/',views.user_staff_appointments_view_complete),

    # ADMIN BLOOD BANK MEMBERSHIP REQUESTS URLS
    path('user/admin/membership_requests/',views.user_admin_membership_requests),
    path('user/admin/membership_requests/open/<int:id>',views.user_admin_membership_requests_open),
    path('user/admin/membership_requests/open/<int:id>/accept/',views.user_admin_membership_requests_open_accept),
    path('user/admin/membership_requests/open/<int:id>/decline/',views.user_admin_membership_requests_open_decline),
   
    # ADMIN ANNOUNCEMENT URLS
    path('user/admin/announce/',views.user_admin_announce),
    path('user/admin/announce/all/',views.user_admin_announce_all),
    path('user/admin/announce/all/<int:id>/',views.user_admin_announce_all_id),
    path('user/admin/announce/all/<int:id>/mark_read/',views.user_admin_announce_all_id_readed),
]




