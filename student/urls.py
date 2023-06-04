from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.studenthome,name="home"),
    path('teacherhome/', views.teacherhome,name="teacherhomepage"),
    path('teacher/', views.teacherupdate,name="teacher"),
    path('arrange/',views.arrangment,name="arrangment"),
    path('login/',views.loginpage,name="login"),
    path('logout/',views.logoutpage,name="logout"),
    path('asses/<str:pk>/',views.fillmark,name='assesment'),
    path('students/',views.studentslist,name="sts"),
    path('teacherarrange/',views.arrangetea,name="teacherarrange"),
    path('fillmark/',views.teacherpage,name='fillmark'),
    path('assesmentresult/',views.assesmentresult,name='assesmentresult'),
    path('assessmenttpe/',views.assesmenttype,name='assessmenttype'),
    path('accountsetting/',views.registerstud,name='accountsetting'),
    path('teacherarrange/<str:pk>/',views.sectioning,name='reg'),
    path('regcourse/',views.registercourse,name='regcourse'),
    path('departmenthomepage/',views.departmenthomepage,name='departmenthomepage'),
    path('transcript/',views.transcript,name='transcript'),
    path('submittedlist/',views.submitted_list,name='submitted_list'),
    path('resubmit/<str:pk>/',views.resubmit,name='resubmit'),
    path('updatearrangment/<str:crs>/<str:sect>/<str:arr>/',views.teacherarrangementUpdate,name='resmit'),
    path('adminpage/',views.adminpage,name='adminpage'),
    path('paschan',views.changepassword,name='passch'),
    path('transfer/',views.transfer,name="transfer"),
    path('reset_password/',
     auth_views.PasswordResetView.as_view(template_name="student/password_reset.html"),
     name="reset_password"),

    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="student/password_reset_sent.html"), 
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name="student/password_reset_form.html"), 
     name="password_reset_confirm"),

    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="student/password_reset_done.html"), 
        name="password_reset_complete"),


]
