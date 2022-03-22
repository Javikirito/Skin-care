import random

import datetime
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from  .models import login,department,disease,doctor,schedule,symptoms,user,feedback,booking,payment,chat
# Create your views here.
def admin_home(request):

    return render(request,'admin/admin_home.html')


def patienthome(request):
    current_datetime = datetime.datetime.today().now()
    print("--------------",current_datetime)
    request.session['tdys']=current_datetime
    print(request.session["id"])
    data = user.objects.get(id=request.session["id"])
    return render(request, "patient/patient_temp.html",{'current_datetime' : current_datetime})


def login_load(request):
    return render(request,'login.html')
def login_load_post(request):
    if request.method == 'POST':
        uname = request.POST['textfield']
        password = request.POST['textfield2']

        log=login.objects.filter(username=uname,password=password)
        if log.exists():
            s=log[0]
            request.session['lid']=s.id
            if s.type=="admin":
                return render(request,"admin/admin_home.html")
            elif s.type=="patient":
                pa=user.objects.get(LOGIN_id=s.id)
                request.session["id"]=pa.id
                current_da = datetime.datetime.now()
                print("--------------",current_da)
                cc=str(current_da)
                x=cc.split()
                print(",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,",x[0])
                request.session['current_datetime']=x[0]
                return render(request,"patient/patient_home.html",{"current_datetime":x[0]})
            elif s.type=="doctor":
                pa = doctor.objects.get(LOGIN_id=s.id)
                request.session["id"] = pa.id
                return render(request,"doctor/doctor_home.html")
            else:
                return render(request,"login.html")
        else:
             return render(request,"login.html")
    return render(request,'login.html')


def admin_adddepartment(request):
    return render(request,"admin/Add Department.html")
def adddepartment_post(request):

    if request.method == 'POST':
        dep = request.POST['textfield']
        depobj=department()
        depobj.department=dep
        depobj.save()
    return render(request,'admin/Add Department.html')


def admin_addschedule(request):

    depall=department.objects.all()
    docall=doctor.objects.all()
    return render(request,"admin/Add shedule.html",{'dep':depall,'doc':docall})

def addschedule_post(request):
    if request.method == 'POST':
        department = request.POST['select']
        doctor = request.POST['select2']
        date = request.POST['textfield']
        time_from = request.POST['textfield2']
        time_to = request.POST['textfield3']

        obj=schedule()
        obj.DEPARTMENT_id=department
        obj.DOCTOR_id=doctor
        obj.date=date
        obj.time=time_from
        obj.timeto=time_to
        obj.save()
    return render(request,"admin/Add shedule.html")


def admin_adddisease(request):
    return render(request,"admin/Add_Disease.html")
def adddisease_post(request):
    if request.method == 'POST':
        dis = request.POST['textfield']
        description = request.POST['textarea']
        obj=disease()
        obj.disease=dis
        obj.description=description
        obj.save()

    return render(request,"admin/Add_Disease.html")


def admin_adddoctor(request):
    depall=department.objects.all()
    print(depall)
    return render(request,"admin/Add_Doctor.html",{'data' : depall})
def adddoctor_post(request):
    if request.method == 'POST':
        dr_name = request.POST['textfield']
        gender = request.POST['RadioGroup1']
        date_of_birth = request.POST['textfield2']
        qualification = request.POST['select']
        photo = request.FILES['file']
        place = request.POST['textfield3']
        pin = request.POST['textfield4']
        post = request.POST['textfield5']
        district = request.POST['textfield6']
        email= request.POST['textfield7']
        department = request.POST['select2']
        contact = request.POST['textfield8']

        fs = FileSystemStorage()
        nam = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
        filename = nam + ".jpg"
        print(filename)
        fs.save(filename, photo)

        url = '/media/' + nam + ".jpg"

        password = str(random.randint(1111,88888888))
        loginobj=login()
        loginobj.username=email
        loginobj.password=password
        loginobj.type="doctor"
        loginobj.save()


        obj=doctor()
        obj.name=dr_name
        obj.dob=date_of_birth
        obj.gender=gender
        obj.qual=qualification
        obj.photo=url
        obj.place=place
        obj.pin=pin
        obj.post=post
        obj.district=district
        obj.email=email
        obj.contact=contact
        obj.LOGIN=loginobj
        obj.DEPARTMENT_id=department
        obj.save()


    return render(request,"admin/Add_Doctor.html")


def admin_addsymptoms(request):
    return render(request,"admin/Add_Symptoms.html")
def addsymptoms_post(request):
    if request.method == 'POST':
        symp = request.POST['textarea']
        obj=symptoms()
        obj.sympt=symp
        obj.save()
    return render(request, "admin/Add_Symptoms.html")


def admin_changepassword(request):
    return render(request,"admin/Change password.html")
def changepassword_post(request):
    if request.method == 'POST':
        current_password = request.POST['textfield']
        new_password = request.POST['textfield2']
        confirm_password = request.POST['textfield3']
    return render(request, "changepassword.html")


def admin_viewdisease(request):
    vdis=disease.objects.all()
    return render(request,"admin/view disease.html",{"vdis":vdis})
def viewdisease(request):
    if request.method == 'POST':
        search = request.POST['textfield']
        vdis = disease.objects.filter(disease__icontains=search)
        return render(request, "admin/view disease.html", {"vdis": vdis})
    else:
        return render(request, "view disease.html")
def delete_disease(request,id):
    dis = disease.objects.get(id=id).delete()
    return admin_viewdisease(request)
def edit_disease(request,id):
    vdis = disease.objects.get(id=id)
    return render(request,"admin/edit_disease.html",{"vdis":vdis})

def edit_disease_post(request):
    if request.method == 'POST':
        dis = request.POST['textfield']
        disid = request.POST['disid']
        description = request.POST['textarea']
        obj=disease(id=disid)
        obj.disease=dis
        obj.description=description
        obj.save()

    return admin_viewdisease(request)


def admin_viewdoctor(request):
    vdr = doctor.objects.all()
    return render(request,"admin/view Doctor.html",{"vdr":vdr})
def viewdoctor_post(request):
    if request.method == 'POST':
        search = request.POST['textfield']
        vdr = doctor.objects.filter(name__icontains=search)
        return render(request, "admin/view Doctor.html", {"vdr": vdr})
    else:
        return render(request, "view Doctor.html")
def delete_doctor(request, id):
    doc = doctor.objects.get(id=id).delete()
    return admin_viewdoctor(request)

def edit_doctor(request,id):
    vdr = doctor.objects.get(id=id)
    obj2=department.objects.get(id=vdr.DEPARTMENT_id)
    data = department.objects.all()
    return render(request, "admin/edit_doctor.html", {"vdr": vdr,"depts":obj2,"data":data})


def edit_doctor_post(request):
    if request.method == 'POST':
        dr_name = request.POST['textfield']
        did = request.POST['did']
        gender = request.POST['RadioGroup1']
        date_of_birth = request.POST['textfield2']
        qualification = request.POST['select']
        photo = request.FILES['file']
        place = request.POST['textfield3']
        pin = request.POST['textfield4']
        post = request.POST['textfield5']
        district = request.POST['textfield6']
        email= request.POST['textfield7']
        department = request.POST['select2']
        contact = request.POST['textfield8']

        fs = FileSystemStorage()
        nam = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
        filename = nam + ".jpg"
        print(filename)
        fs.save(filename, photo)

        url = '/media/' + nam + ".jpg"
        # username = request.POST['textfield8']
        # password = request.POST['textfield9']
        # confirm_password = request.POST['textfield10']

        obj = doctor.objects.get(id=did)
        obj.name = dr_name
        obj.dob = date_of_birth
        obj.gender = gender
        obj.qual = qualification
        obj.photo = url
        obj.place = place
        obj.pin = pin
        obj.post = post
        obj.district = district
        obj.email = email
        obj.contact = contact
        obj.DEPARTMENT_id = department
        obj.save()

    return admin_viewdoctor(request)


def admin_viewshedule(request):
    vsh=schedule.objects.all()
    return render(request,"admin/View shedule.html",{"vsh":vsh})
def viewschedule_post(request):
    if request.method == 'POST':
        type=request.POST["Submit"]
        if type=="view":
            search = request.POST['textfield3']
            vsh = schedule.objects.filter(DOCTOR__name__icontains=search)
            return render(request, "admin/View shedule.html", {"vsh": vsh})
        else:
            d1 = request.POST['d1']
            d2=request.POST["d2"]
            vsh = schedule.objects.filter(date__range=(d1, d2))
            return render(request, "admin/View shedule.html", {"vsh": vsh})

    else:
        return render(request, "view schedule.html")
def delete_schedule(request,id):
    sch = schedule.objects.get(id=id).delete()
    return admin_viewshedule(request)

def edit_schedule(request,id):
    vsh = schedule.objects.get(id=id)

    departmentall= department.objects.all()
    doctorall= doctor.objects.all()


    return render(request,"admin/edit_schedule.html",{"vsh":vsh,"dep":departmentall,'doc':doctorall})

def edit_schedule_post(request):
    if request.method == 'POST':
        department = request.POST['select']
        schid = request.POST['schid']
        doctor = request.POST['select2']
        date = request.POST['textfield']
        time_from = request.POST['textfield2']
        time_to = request.POST['textfield3']

        obj=schedule(id=schid)
        obj.DEPARTMENT_id=department
        obj.DOCTOR_id=doctor
        obj.date=date
        obj.time=time_from
        obj.timeto=time_to
        obj.save()
    return admin_viewshedule(request)


def admin_viewdepartment(request):
    vdep=department.objects.all()
    return render(request,"admin/view_Department.html",{"vdep":vdep})

def viewdepartment_post(request):
    if request.method == 'POST':
        search = request.POST['textfield']
        vdep = department.objects.filter(department__icontains=search)
        return render(request, "admin/view_Department.html", {"vdep": vdep})
    else:
        vdep = department.objects.all()
        return render(request, "admin/view_Department.html", {"vdep": vdep})
def delete_department(request,id):
    dep = department.objects.get(id=id)
    dep.delete()
    return viewdepartment_post(request)
def edit_department(request,id):
    vdep = department.objects.get(id=id)
    return render(request,"admin/edit_department.html",{"vdep":vdep})
def edit_department_post(request):
    if request.method == 'POST':
        dep = request.POST['textfield']
        depid = request.POST['depid']
        depobj=department(id=depid)
        depobj.department=dep
        depobj.save()
    return admin_viewdepartment(request)

def admin_viewsymptoms(request):
    vsp=symptoms.objects.all()
    return render(request,"admin/View Symptoms.html",{"vsp":vsp})
def viewsymptoms_post(request):
    if request.method == 'POST':
        search = request.POST['textfield']
        vsp = symptoms.objects.filter(sympt__icontains=search)
        return render(request, "admin/View Symptoms.html", {"vsp": vsp})
    else:
      return render(request, "View Symptoms.html")
def delete_symptoms(request,id):
    symp = symptoms.objects.get(id=id).delete()
    return admin_viewsymptoms(request)

def edit_symptoms(request,id):
    vsp = symptoms.objects.get(id=id)
    return render(request, "admin/edit_Symptoms.html", {"vsp": vsp})

def edit_symptoms_post(request):
    symp = request.POST['textfield']
    syid = request.POST['syid']
    obj = symptoms(id=syid)
    obj.sympt = symp
    obj.save()

    return admin_viewsymptoms(request)


def admin_viewfeedback(request):
    res=feedback.objects.all()
    return render(request,"admin/View_feedback.html",{"res": res})


def admin_viewpayments(request):
    vps=payment.objects.all()
    return render(request,"admin/View_Payment.html",{"vps":vps})
def viewpayments_post(request):
    if request.method == 'POST':
        search = request.POST['textfield']
        vps = payment.objects.filter(date=search)
        print("0000",search)
        return render(request, "admin/View_Payment.html", {"vps": vps})
    else:
        return render(request, "view_payments.html")


def admin_chat_to_doctor(request):
    return render(request,"admin/chat to doctor.html")
def chat_to_doctor_post(request):
    if request.method == 'POST':
        search = request.POST['textfield']
    return render(request, "chat to doctor.html")


def admin_doctor_payment(request):
    return render(request,"admin/doctor payment.html")
def doctor_payment_post(request):
    if request.method == 'POST':
        bank = request.POST['select']
        account_number = request.post['textfield']
        password = request.POST['textfield2']
        return render(request, "doctor payment.html")

def admin_chat_with_doctor(request,id):
     return render(request, "admin/chat with doctor.html",{'dlid':id,'fromid':request.session["lid"]})


def admin_view_msg(request,receiverid):

    obj=chat.objects.all()
    user_data=doctor.objects.get(LOGIN=receiverid)
    print("********************",obj)

    res = []
    for i in obj:
        s = {'id':i.pk, 'date':i.date,'msg':i.message,'fromid':i.LOGINFROM.id,'toid':i.LOGINTO.id}
        res.append(s)
    print(res)
    return JsonResponse({'status': 'ok', 'data': res,'name':user_data.name,'image':user_data.photo})

def admin_insert_chat(request,receiverid,msg,senid):

    print(receiverid,msg,senid)


    obj=chat()
    obj.LOGINFROM_id=senid
    obj.LOGINTO_id=receiverid
    obj.message=msg
    obj.date=datetime.datetime.now().date()
    obj.save()
    return JsonResponse({'status':'ok'})



def chatv(request,dlid):
    da = doctor.objects.filter(LOGIN=dlid)
    res = []
    for i in da:
        s = {'id': i.pk, 'name': i.name, 'email': i.email,'image':i.photo}
        res.append(s)
    print(res)
    return JsonResponse({'status': 'ok', 'data': res})







# ///////////////////3rd_module/////////////////#


def doctor_home(request):
    return render(request,"doctor/doctor_home.html")


def doctor_viewmyfeedback(request):
    res=feedback.objects.filter(DOCTOR=request.session["id"])
    return render(request,"doctor/View myFeedback.html",{"res":res})


def doctor_viewpaymentsofdoctor(request):
    dps =payment.objects.all()
    return render(request,"doctor/View payment of Doctor.html",{"dps":dps})


def doctor_viewmybooking(request):
    vdb=booking.objects.filter(SCHEDULE__DOCTOR=request.session["id"])
    return render(request,"doctor/View_myBooking.html",{"vdb":vdb})

def view_booking_post(request):
    if request.method=='POST':
       return render(request,"doctor/View_myBooking.html")



def doctor_viewmyschedule(request):
    x=request.session['lid']
    dobj=doctor.objects.get(LOGIN=x)
    a=schedule.objects.filter(DOCTOR=dobj.id)
    return render(request,"doctor/View_myschedule.html",{'a':a})


def doctor_viewpatient(request,sid):
    x = str(request.session['lid'])
    dobj = doctor.objects.get(LOGIN_id=x)
    a = booking.objects.filter(SCHEDULE_id=sid)
    print(a)
    return render(request,"doctor/View_Patient.html",{'a':a})

def doctor_Viewpatients(request):
    x = str(request.session['lid'])
    vdb = booking.objects.filter(SCHEDULE__DOCTOR=request.session["id"])

    res=[]
    userid=[]
    for i in vdb:

        print(userid,i.USER.id )
        if i.USER.id  in userid:

            print("llllllllllll")

            pass
        else:
            userid.append(i.USER.id)
            a = {'id': i.USER.LOGIN.pk, 'name': i.USER.name, 'email': i.USER.email, 'photo': i.USER.photo}
            res.append(a)
    return render(request,"doctor/view patients.html",{'a':res})

def Viewpatients_post(request):
    if request.method=='POST':
       return render(request,"doctor/Viewpatients.html")

def doctor_chat_with_admin(request,id):
    return render(request,"doctor/chat with admin.html",{'dlid':id,'fromid':request.session["lid"]})



def doctor_chat_with_patient(request,ID):
    request.session['selids']=ID
    return render(request,"doctor/chat with patient.html",{'toid':ID,'fromid':request.session["id"]})




# )))))))))))))))))))=====================================doc_chat=========================

def patient_chat_with_doctor(request,dlid):
    # return render(request,"patient/chat with doctor.html",{'dlid':dlid,'fromid':request.session["lid"]})
    return render(request, "doctor/chat with patient.html")

def Pat_view_msg(request,receiverid):


    # doc=doctor.objects.get(L=receiverid)
    obj=chat.objects.all()
    user_data=doctor.objects.get(LOGIN=receiverid)
    print("********************",obj)

    res = []
    for i in obj:
        s = {'id':i.pk, 'date':i.date,'msg':i.message,'fromid':i.LOGINFROM.id,'toid':i.LOGINTO.id}
        res.append(s)
    print(res)
    return JsonResponse({'status': 'ok', 'data': res,'name':user_data.name,'image':user_data.photo})

def chatview(request,dlid):
    da = doctor.objects.filter(LOGIN=dlid)
    res = []
    for i in da:
        s = {'id': i.pk, 'name': i.name, 'email': i.email,'image':i.photo}
        res.append(s)
    print(res)
    return JsonResponse({'status': 'ok', 'data': res})


def chatview_dtop(request):
    print(request.session["selids"])
    da = user.objects.filter(LOGIN_id=request.session['selids'])
    res = []
    for i in da:
        s = {'id': i.LOGIN.id, 'name': i.name, 'email': i.email,'image':i.photo}
        res.append(s)
    print(res)
    return JsonResponse({'status': 'ok', 'data': res})


def doctor_insert_chat(request,receiverid,msg,senid):

    print(receiverid,msg,senid)


    obj=chat()
    obj.LOGINFROM_id=senid
    obj.LOGINTO_id=receiverid
    obj.message=msg
    obj.date=datetime.datetime.now().date()
    obj.save()
    return JsonResponse({'status':'ok'})

def patient_insert_chat(request,receiverid,msg):

    print(receiverid,msg)


    obj=chat()
    obj.LOGINFROM_id=request.session["lid"]
    obj.LOGINTO_id=receiverid
    obj.message=msg
    obj.date=datetime.datetime.now().date()
    obj.save()
    return JsonResponse({'status':'ok'})



# ===========================================================================================================
def doctor_doctor_profile(request):
    ddp = doctor.objects.get(id=request.session["id"])
    return render(request,"doctor/doctor_profile.html", {"ddp":ddp})

# ////////////////////chat with admin///////////////////////

def doc_view_msg(request,receiverid):

    obj=chat.objects.all()
    user_data=doctor.objects.get(LOGIN=receiverid)
    print("********************",obj)

    res = []
    for i in obj:
        s = {'id':i.pk, 'date':i.date,'msg':i.message,'fromid':i.LOGINFROM.id,'toid':i.LOGINTO.id}
        res.append(s)
    print(res)
    return JsonResponse({'status': 'ok', 'data': res,'name':user_data.name,'image':user_data.photo})

def doc_insert_chat(request,receiverid,msg,senid):

    print(receiverid,msg,senid)


    obj=chat()
    obj.LOGINFROM_id=senid
    obj.LOGINTO_id=receiverid
    obj.message=msg
    obj.date=datetime.datetime.now().date()
    obj.save()
    return JsonResponse({'status':'ok'})



def chatviewdoc(request,dlid):
    da = doctor.objects.filter(LOGIN=dlid)
    res = []
    for i in da:
        s = {'id': i.pk, 'name': i.name, 'email': i.email,'image':i.photo}
        res.append(s)
    print(res)
    return JsonResponse({'status': 'ok', 'data': res})





#///////////////2nd_module///////////////////#


def patient_home(request):
    data = user.objects.get(id=request.session["id"])
    return render(request,"patient/patient_home.html",{'data':data})


def patient_booking(request,bok):
    bookings=booking()
    bookings.SCHEDULE_id=bok
    bookings.USER=user.objects.get(LOGIN_id=request.session['lid'])
    bookings.save()
    return render(request,"patient/booking.html",{'a':bookings})

def booking_post(request):
    if request.method == 'POST':
        first_name = request.POST['textfield']
        last_name = request.POST['textfield2']
        place = request.POST['textfield3']
        doctor_name = request.POST['textfield4']
        department = request.POST['textfield5']
        date = request.POST['textfield6']
        time_from = request.POST['textfield7']
        time_to = request.POST['textfield8']
        return render(request, "booking.html")


def patient_registration(request):
    return render(request,"patient/registration.html")

def registration_post(request):

        name = request.POST['textfield']
        age = request.POST['textfield2']
        gender = request.POST['radio']
        place = request.POST['textfield3']
        pin = request.POST['textfield4']
        post = request.POST['textfield5']
        contact = request.POST['textfield6']
        email = request.POST['textfield7']
        photo = request.FILES['file']

        fs = FileSystemStorage()
        nam = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
        filename = nam + ".jpg"
        print(filename)
        fs.save(filename, photo)

        url = '/media/' + nam + ".jpg"
        # username = request.POST['textfield8']
        password = request.POST['textfield9']
        # confirm_password = request.POST['textfield10']
        obj1=login()
        obj1.username=email
        obj1.password=password
        obj1.type='patient'
        obj1.save()

        obj=user()
        obj.name=name
        obj.age=age
        obj.gender=gender
        obj.place=place
        obj.pin=pin
        obj.post=post
        obj.contact=contact
        obj.email=email
        obj.photo=url
        obj.LOGIN_id=obj1.id
        obj.save()

        return render(request, "login.html")


def patient_view_doctor(request):
    vdoc=doctor.objects.all()
    return render(request,"patient/view doctor.html",{"vdoc":vdoc})

def view_doctor_post(request):
    if request.method == 'POST':
        search = request.POST['textfield']
        vdoc = doctor.objects.filter(name__icontains=search)
        return render(request, "patient/view doctor.html", {"vdoc": vdoc})
    else:
        return render(request, "view doctor.html")


def patient_view_schedule(request,did):
    res=schedule.objects.filter(DOCTOR=did)
    return render(request,"patient/view schedule.html",{"res":res})

def view_schedule_post(request):
    if request.method == 'POST':
        search = request.POST['textfield']
    return render(request, "view schedule.html")




def chat_with_doctor_post(request):
    if request.method == 'POST':
        search = request.POST['textfield']
    return render(request, "chat with doctor.html")


def patient_payment(request):
    return render(request,"patient/payment.html")
def payment_post(request):
    if request.method == 'POST':
        bank = request.POST['select']
        account_number = request.POST['textfield']
        password = request.POST['textfield2']
        return render(request, "payment.html")


def patient_send_feedback_abt_dct(request,feed):
    return render(request,"patient/send feedback abt dct.html",{"feed":feed})
def send_feedback_abt_dct_post(request):
    if request.method == 'POST':
        feed= request.POST['textfield']
        doctorid = request.POST['did']
        pat_id=request.session["id"]
        from datetime import date
        today = date.today()
        obj=feedback()
        obj.feedback=feed
        obj.USER_id=pat_id
        obj.DOCTOR_id=doctorid
        obj.date=today
        obj.save()
        return render(request,"patient/send feedback abt dct.html")


def patient_photo_prediction(request):
    return render(request,"patient/photo prediction.html")
def photo_prediction_post(request):
    if request.method == 'POST':
        browser = request.POST['file']


def patient_symptom_selection(request):
    return render(request,"patient/symptom selection.html")
def symptom_selection_post(request):
    if request.method == 'POST':
        symptom = request.POST['checkbox']

def patient_user_profile(request):
    pup = user.objects.get(id=request.session["id"])
    return render(request,"patient/user_profile.html", {"pup":pup})

def patient_view_booking(request):
    pvb=booking.objects.filter(USER=request.session["id"])
    return render(request,"patient/view_booking.html",{"pvb":pvb})

def view_p_booking_post(request):
    if request.method=='POST':
        d1 = request.POST['d1']
        d2 = request.POST["d2"]
        pvb = booking.objects.filter(USER=request.session["id"],SCHEDULE__date__range=(d1,d2))
        return render(request, "patient/view_booking.html", {"pvb": pvb})

def delete_pschedule(request, id):
    schd = booking.objects.get(id=id).delete()
    return patient_view_booking(request)

def patient_chat_with_doctor(request,dlid):
    return render(request,"patient/chat with doctor.html",{'dlid':dlid,'fromid':request.session["lid"]})

def Pat_view_msg(request,receiverid):


    # doc=doctor.objects.get(L=receiverid)
    obj=chat.objects.all()
    user_data=doctor.objects.get(LOGIN=receiverid)
    print("********************",obj)

    res = []
    for i in obj:
        s = {'id':i.pk, 'date':i.date,'msg':i.message,'fromid':i.LOGINFROM.id,'toid':i.LOGINTO.id}
        res.append(s)
    print(res)
    return JsonResponse({'status': 'ok', 'data': res,'name':user_data.name,'image':user_data.photo})

def doc_view_msg(request,receiverid):


    pobj=login.objects.get(pk=receiverid)


    dlid=request.session['lid']

    print(receiverid, "aaaaaabbbbbbbbb",dlid)

    dobj=login.objects.get(id=dlid)

    res = []

    # doc=doctor.objects.get(L=receiverid)
    obj=chat.objects.all() #filter(LOGINFROM=pobj,LOGINTO=dobj)
    obj1 = chat.objects.filter(LOGINFROM=dobj, LOGINTO=pobj)
    user_data=user.objects.get(LOGIN=pobj)
    print("********************",obj)

    for i in obj:

        if (i.LOGINFROM_id==dobj.id and i.LOGINTO_id==pobj.id) or (i.LOGINFROM_id==pobj.id and i.LOGINTO_id==dobj.id):


            s = {'id':i.pk, 'date':i.date,'msg':i.message,'fromid':i.LOGINFROM.id,'toid':i.LOGINTO.id}
            res.append(s)



    # for i in obj1:
    #     s = {'id': i.pk, 'date': i.date, 'msg': i.message, 'fromid': i.LOGINFROM.id, 'toid': i.LOGINTO.id}
    #     res.append(s)


    print(res)
    return JsonResponse({'status': 'ok', 'data': res,'name':user_data.name,'image':user_data.photo})

def chatview(request,dlid):
    da = doctor.objects.filter(LOGIN=dlid)
    res = []
    for i in da:
        s = {'id': i.pk, 'name': i.name, 'email': i.email,'image':i.photo}
        res.append(s)
    print(res)
    return JsonResponse({'status': 'ok', 'data': res})
def doctor_insert_chat(request,receiverid,msg,senid):

    print(receiverid,msg,senid)


    obj=chat()
    obj.LOGINFROM_id=senid
    obj.LOGINTO_id=receiverid
    obj.message=msg
    obj.date=datetime.datetime.now().date()
    obj.save()
    return JsonResponse({'status':'ok'})

