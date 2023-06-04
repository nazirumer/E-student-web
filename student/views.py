from django.shortcuts import render,redirect
from .forms import *
from django.forms import inlineformset_factory
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User,Group
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import *
from django.forms import inlineformset_factory
from ordered_set import OrderedSet
# Create your views here.
def setarrangementnull():
	sections=Section.objects.all()
	TeacherArrangment.objects.all().delete()
	for k in sections:
		courses=Course.objects.filter(grade=k.grade)
		for j in courses:
			k.withcourse[j.course_id]=0
			k.save()
def generatetranscript():
	students=Student.objects.all()
	for k in students:
		semister=Semister.objects.get(active=True)
		section=Assesment.objects.filter(student=k).first().section
		Transcript.objects.create(student=k,grade=k.enroll_year,semister=semister,section=section)

def generatewholetotal():
	students=Student.objects.all()
	semister=Semister.objects.get(active=True)
	for k in students:
		tot=0
		c=1
		transcript1=Transcript.objects.filter(student=k,semister=Semister.objects.first(),grade=k.enroll_year).first()
		transcript2=Transcript.objects.filter(student=k,semister=Semister.objects.last(),grade=k.enroll_year).first()
		if not transcript1 or not transcript2:
			continue
		if transcript1.total and transcript2.total:
			transcript1.wholetotal=(transcript1.total + transcript2.total)/2
			transcript1.save()
			transcript2.wholetotal=transcript1.wholetotal
			transcript2.save()
			transcript1.wholeavg=(transcript1.avg+transcript2.avg)/2
			transcript1.save()
			transcript2.wholeavg=transcript1.wholeavg
			transcript2.save()
def generatepassfail():
	students=Student.objects.all()
	semister=Semister.objects.get(active=True)
	
	for k in students:
		
		transcript1=Transcript.objects.filter(student=k,grade=k.enroll_year,semister=Semister.objects.first()).first()
		transcript2=Transcript.objects.filter(student=k,grade=k.enroll_year,semister=Semister.objects.last()).first()
		asses=Assesment.objects.filter(student=k,section__grade=k.enroll_year)
		tot=0
		c=1
		a=0
		for j in range(0,len(asses),2):
			
			if not asses[j].result or  not asses[j+1].result:
				asses[j].wholetot=None
				asses[j].wholeavg=None
				asses[j+1].wholetot=None
				asses[j+1].wholeavg=None
				asses[j+1].save()
				asses[j].save()
				c=0
			else:
				asses[j+1].wholetot=(asses[j+1].result + asses[j].result)/2
				asses[j+1].save()
				asses[j].wholetot=asses[j+1].wholetot
				asses[j].save()
				if asses[j].wholetot >= 50:
					asses[j].wholestatus='green'
				elif asses[j].wholetot>=40:
					asses[j].status='yellow'
					a+=1
				else:
					asses[j].wholestatus='red'
					if not transcript1 or  not transcript2:
						continue
					transcript1.complete=False
					transcript1.save()
					transcript2.complete=False
					transcript2.save()
					a+=1
				asses[j].save()
		if not transcript1 or  not transcript2:
						continue
		if not transcript1.wholeavg:
			transcript1.complete=False
			transcript1.save()
			transcript2.complete=False
			transcript2.save()
		elif (c==1) and (c==1 and  a>=4) or ( a==3 and transcript1.wholeavg<55) or ( a==2 and transcript1.wholeavg<53) or ( a==1 and transcript1.wholeavg<51):
			transcript1.complete=False
			transcript1.save()
			transcript2.complete=False
			transcript2.save()
		elif c==1:
			transcript1.complete=True
			transcript1.save()
			transcript2.complete=True
			transcript2.save()

		

def generatetotal():
	students=Student.objects.all()
	semister=Semister.objects.get(active=True)
	
	for k in students:
		tot=0
		c=1
		transcript=Transcript.objects.filter(student=k,semister=semister,grade=k.enroll_year).first()
		asses=Assesment.objects.filter(student=k,semister=semister.semister,section__grade=k.enroll_year)
		a=0
		b=1
		if not transcript:
			continue
		for j in asses :
			if not j.result:
				transcript.total=None
				transcript.complete=False
				transcript.save()
				c=0
				break
			else:
				if j.result >= 50:
					j.status='green'
				elif j.result>=40:
					j.status='yellow'
					a+=1
				else:
					j.status='red'
					transcript.complete=False
					transcript.save()
					a+=1
				j.save()
				tot+=j.result
		asses=Assesment.objects.filter(student=k,semister=semister.semister,section__grade=k.enroll_year)
		if (c==1) and (c==1 and  a>=4) or ( a==3 and tot/len(asses)<55) or ( a==2 and tot/len(asses)<53) or ( a==1 and tot/len(asses)<51):
			transcript.total=tot
			transcript.complete=False
			transcript.avg=tot/len(asses)
			transcript.save()
		elif c==1:
			transcript.total=tot
			transcript.avg=tot/len(asses)
			transcript.complete=True
			transcript.save()

def generatecourseallstanding():
	
	semister=Semister.objects.get(active=True)
	grades=Grade.objects.all()
	for j in grades:
	
		courses=Course.objects.filter(grade=j)
		for m in courses:
			sturank =Assesment.objects.filter(semister=semister.semister).filter(section__grade=j).filter(course=m).order_by('-result')
			cval=-1
			s=1
			jum=0
			for k in  sturank:
				if not k.result:
					continue
				if k.result == cval:
					
					k.standing_all=s
					cval=k.result
					jum+=1
					k.save()
				else:
					s+=jum
					cval=k.result
					k.standing_all=s
					jum=1
					k.save()
				k.save()






def generatecoursesectionstanding():
	
	semister=Semister.objects.get(active=True)
	sections=Section.objects.all()
	for j in sections:
		courses=Course.objects.filter(grade=j.grade)
		for m in courses:
			sturank=Assesment.objects.filter(semister=semister.semister).filter(section=j).filter(course=m).order_by('-result')
			cval=-1
			s=1
			jum=0
			for k in  sturank:
				if not k.result:
					continue
				if k.result == cval:
					
					k.standing_sec=s
					cval=k.result
					jum+=1
					k.save()
				else:
					s+=jum
					cval=k.result
					k.standing_sec=s
					jum=1
					k.save()
				k.save()


def generatesectionstanding():
	semister=Semister.objects.get(active=True)
	sections=Section.objects.all()
	for j in sections:
		sturank=Transcript.objects.filter(complete=True,semister=semister,section=j).order_by('-total')
		cval=-1
		s=1
		jum=0
		for k in  sturank:
			if k.total == cval:
				
				k.standing_sec=s
				cval=k.total
				jum+=1
				k.save()
			else:
				s+=jum
				cval=k.total
				k.standing_sec=s
				jum=1
				k.save()
			k.save()

def generatewholesectionstanding():
	semister=Semister.objects.get(active=True)
	sections=Section.objects.all()
	for j in sections:
		sturank=Transcript.objects.filter(complete=True,semister=semister,section=j).order_by('-wholetotal')
		cval=-1
		s=1
		jum=0
		for k in  sturank:
			if k.wholetotal == cval:
				
				k.wholestanding_sec=s
				cval=k.wholetotal
				jum+=1
				k.save()
			else:
				s+=jum
				cval=k.wholetotal
				k.wholestanding_sec=s
				jum=1
				k.save()
			k.save()
def generatewholeallstanding():
	semister=Semister.objects.get(active=True)
	grades=Grade.objects.all()
	for j in grades:
		sturank=Transcript.objects.filter(complete=True,semister=semister,grade=j).order_by('-wholetotal')
		cval=-1
		s=1
		jum=0
		for k in  sturank:
			if k.wholetotal == cval:
				
				k.wholestanding_all=s
				cval=k.wholetotal
				jum+=1
				k.save()
			else:
				s+=jum
				cval=k.wholetotal
				k.wholestanding_all=s
				jum=1
				k.save()
			k.save()

			k.finished=True
			k.save()


def generateallstanding():
	semister=Semister.objects.get(active=True)
	grades=Grade.objects.all()
	for j in grades:
		sturank=Transcript.objects.filter(complete=True,semister=semister,grade=j).order_by('-total')
		cval=-1
		s=1
		jum=0
		for k in  sturank:
			if k.total == cval:
				
				k.standing_all=s
				cval=k.total
				jum+=1
				k.save()
			else:
				s+=jum
				cval=k.total
				k.standing_all=s
				jum=1
				k.save()
			k.save()

			k.finished=True
			k.save()




def generateteacher():
	x="teacher"
	gradelist=Grade.objects.all()
	n=len(gradelist)
	sectionlist=Section.objects.all()
	m=len(sectionlist)
	for j in range(25):
		group=Group.objects.get(name='teacher')
		User.objects.create(username=x+str(j)).groups.add(group)
		y=User.objects.last()
		y.set_password(2*(x+str(j)))
		user=y.save()
		y=User.objects.last()
		#user.groups.add(group)
		dep=Department.objects.all()
		teacher=Teacher.objects.create(user=y,first_name=x+str(j),last_name="myfa",department=dep[j%len(dep)])
def generate():
	x="student"
	gradelist=Grade.objects.get(year=9)
	for j in range(300):
		group=Group.objects.get(name='student')
		User.objects.create(username=x+str(j)).groups.add(group)
		y=User.objects.last()
		y.set_password(2*(x+str(j)))
		user=y.save()
		y=User.objects.last()
		#user.groups.add(group)
		std=Student.objects.create(user=y,first_name=x+str(j),last_name="myfa",ministry_result=85,matric_result=6.9,emergency_contact_name="emer",emergency_phone_number="gjj",enroll_year=gradelist)
		l=Course.objects.all().filter(grade=std.enroll_year)
		sectionlist=Section.objects.filter(grade=std.enroll_year)
		m=len(sectionlist)
		std.section = sectionlist[j%m]
		std.save()
		for k in l:
			Assesment.objects.create(course=k,student=std,section=std.section,semister='semisterI')
			Assesment.objects.create(course=k,student=std,section=std.section,semister='semisterII')
@login_required(login_url='login')
@allowed_users(['student'])
def registerstud(request):

	customerform=CustomerForm(instance=request.user.student)
	if request.method=="POST":
		customerform=CustomerForm(request.POST,request.FILES,instance=request.user.student)
		if  customerform.is_valid():
			customerform.save()
			messages.success(request,"registered successfully")
			return redirect('home')
	context={"customerform":customerform}
	return render(request,'student/accountsetting.html',context)

def teacher(request):
	form=CreateUserForm()
	customerform=TeacherForm()
	if request.method=="POST":
		form=CreateUserForm(request.POST)
		customerform=TeacherForm(request.POST)
		if form.is_valid() and customerform.is_valid():
			group=Group.objects.get(name='teacher')
			user=form.save()
			user.groups.add(group)
			customer=customerform.save(commit=False)
			customer.user=user
			customer.save()
			messages.success(request,"registered successfully" + str(user))
			return redirect('home')
	context={"form":form,"customerform":customerform}
	return render(request,'student/registerrr.html',context)
@login_required(login_url='login')
@allowed_users(['student'])
def arrangment(request):
	customerform=ArrangementForm()
	if request.method=="POST":
		customerform=ArrangementForm(request.POST)
		if customerform.is_valid():
			customer=customerform.save()
			messages.success(request,"registered successfully" )
			l=customer.section.all()
			for k in l:
				students=Student.objects.filter(section=k)
				for j in students:
					temp=Assesment.objects.get(student=j,course=customer.course)
					temp.teacher=customer.teacher
					temp.save()
			return redirect('home')
	context={"customerform":customerform}
	return render(request,'student/arrange.html',context)
@unauthenticated_user
def loginpage(request):
	if request.method=="POST":
		username=request.POST.get('username')
		password=request.POST.get('password')
		user = authenticate(username=username,password=password)
		if user is not None:
			login(request ,user)
			return redirect('home')
	return render(request,'student/login.html')


def logoutpage(request):
	logout(request)
	return redirect('login')

def studentslist(request):
	students =Student.objects.all()
	context={'object_list':students}
	return render(request,'student/student_list.html',context)

@login_required(login_url='login')
@student_only
def studenthome(request):
	schedules=Upcoming.objects.all().order_by('-id')[:5]
	context={'schedules':schedules}
	return render(request,'student/homepage.html',context)
def teacherhome(request):
	context={}
	return render(request,'student/teacherhomepage.html',context)


@login_required(login_url='login')
@allowed_users(['teacher'])
def teacherpage(request):
	arr=TeacherArrangment.objects.filter(teacher=request.user.teacher)
	l=[]
	for k in arr:
		l+=k.section.all()

	context={'arr':arr,'sectionlist':l}
	return render(request,'student/teacherview.html',context)
@login_required(login_url='login')
@allowed_users(['student'])
def assesmentresult(request):
	semister=Semister.objects.get(active=True)
	assesments=Assesment.objects.filter(student=request.user.student).filter(asgt__contains = 'assesmenttype').filter(semister=semister.semister)
	context={'assesments':assesments}
	if request.method=='POST':
		c=request.POST.get('asm')
		result=Assesment.objects.get(id=c)
		tt=0
		tot=0
		xy=result.asgt
		for z in xy:
			if xy[z]['result']!='':
				tt+=float(xy[z]['result'])
			tot+=float(xy[z]['maximummark'])
		result.total=tt
					
	
		context={'assesments':assesments,'result':result,'total':tot}
		return render(request,'student/assesmentresult.html',context)
	return render(request,'student/assesmentresult.html',context)


def registeruser(request):
	if request.method=='POST':
		for n in range(8):
			mn=request.POST.get('user'+str(n))
	extras=[i for i in range(8)]
	context={'extra':extras}
	return render(request,'student/reg.html',context)

@login_required(login_url='login')
@allowed_users(['teacher'])
def assesmenttype(request):
	tar=TeacherArrangment.objects.filter(teacher=request.user.teacher)
	arras=TeacherArrangment.objects.filter(teacher=request.user.teacher)
	if request.method=='POST':
		z=request.POST.get('asm')
		x=request.POST.get('name')
		y=request.POST.get('maxmark')
		astpe=request.POST.get('tpe')
		ta=TeacherArrangment.objects.get(id=z)
		semister=Semister.objects.get(active=True)
		assesment=Assesment.objects.filter(teacher=ta.teacher,course=ta.course).filter(semister=semister.semister)
		for k in assesment:
			if x in k.asgt :
				return HttpResponse("2 names must not be the same ")
			k.asgt[x]={'assesmenttype':astpe,'maximummark':y,'result':''}
			
			k.save()
	context={'asm':tar}
	return render(request,'student/type.html',context)
@login_required(login_url='login')
@allowed_users(['teacher'])
def fillmark(request,pk):
	y=Section.objects.get(id=pk)
	semister=Semister.objects.get(active=True)
	z=Assesment.objects.filter(semister=semister.semister).filter(teacher=request.user.teacher).filter(finished=False).filter(section=y)
	if z:
		tt=z[0].asgt
		
	else:
		return HttpResponse('<h1>you have submitted the form to change you should goto administrator<h1/>')
	if request.method=='POST':
		calctot=request.POST.get('calculatetotal')
		fin=request.POST.get('finished')
		
		
		for j in z:
			tot=0
			for m in tt:
				asde=request.POST.get(str(j.student)+str(m))
				if calctot !='None':
					if asde:
						try:
							if float(asde)>float(j.asgt[m]['maximummark']) or float(asde)<0:
								return HttpResponse('<h1> input either negative number or greaterthan maximum number for ' +str(j.student) +'<h1/>')
							tot+=float(asde)
						except:
							return HttpResponse('<h1><script> alert(invalid input for )' +str(j.student) +'</script><h1/>')

				j.asgt[m]['result']=asde
				
				j.save()
			fin = str(fin)	
			if fin !='None':
				j.result=tot
				if tot<40:
					j.status='red'
				if tot<50:
					j.status='yellow'
				else:
					j.status='green'
				
				j.save()
		if fin !='None':
			sturank=z.order_by('-result')
			cval=-1
			s=1
			jum=0
			for k in  sturank:
				k.finished=True
				k.save()
				if not k.result:
					continue
				if k.result == cval:
					
					k.standing_sec=s
					cval=k.result
					jum+=1
					k.save()
				else:
					s+=jum
					cval=k.result
					k.standing_sec=s
					jum=1
					k.save()
				k.save()

	context={'students':z,'tt':tt}
	return render(request,'student/fill.html',context)



@login_required(login_url='login')
@allowed_users(['department'])
def arrangetea(request):
	depart=Department.objects.get(id=request.user.department.id)
	arranges=TeacherArrangment.objects.filter(course__department=depart)
	courses=Course.objects.filter(department=depart)
	teachers=Teacher.objects.filter(department=depart)
	if request.method=='POST':
		tchr=Teacher.objects.get(id=request.POST.get('tr'))
		crse=Course.objects.get(id=request.POST.get('cr'))
		semister=Semister.objects.get(active=True)
		TeacherArrangment.objects.create(teacher=tchr,course=crse,semister=semister.semister)
	context={'courses':courses,'teachers':teachers,'course':'Course:-','teacher':'Teacher:-','arranges':arranges,}
	return render(request,'student/registerrr.html',context)

@login_required(login_url='login')
@allowed_users(['department'])
def sectioning(request,pk):
	tar=TeacherArrangment.objects.get(id=pk)
	cour=tar.course.grade
	cid=tar.course

	cid=cid.course_id
	
	mysection=set({})
	m=Section.objects.filter(grade=cour)
	for k in m:
		if not k.withcourse[cid]:
			mysection.add(k)
	courses=tar.course
	teachers=tar.teacher
	se=TeacherArrangment.objects.all()
	allocatedsection=TeacherArrangment.objects.filter(teacher=teachers).filter(course__course_id=cid)
	
	if request.method=='POST':
		checkedlis=request.POST.getlist('check')
		for j in checkedlis:
			se=Section.objects.get(id=j)
			se.withcourse[cid]=1
			se.save()
			tar.section.add(se)
			tar.save()
			asesmentss=Assesment.objects.filter(course=tar.course).filter(section=Section.objects.get(id=j))
			for asm in asesmentss:
				asm.teacher=teachers
				asm.save()

	context={'courses':courses,'teachers':teachers,'sections':mysection,'course':'Course:-','section':'unallocated Sections:-','teacher':'Teacher:-','allocatedsection':allocatedsection}
	return render(request,'student/sectioning.html',context)
@login_required(login_url='login')
@allowed_users(['department'])
def teacherarrange(request):
	depart=Department.objects.get(id=request.user.department.id)
	
	courses=Course.objects.filter(department=depart)
	teachers=Teacher.objects.filter(department=depart)
	sections=Section.objects.all()
	if request.method=='POST':
		tchr=Teacher.objects.get(id=request.POST.get('tr'))
		crse=Course.objects.get(id=request.POST.get('cr'))
		checkedlis=request.POST.getlist('check')
		arran=TeacherArrangment.objects.filter(teacher=tchr,course=crse)
		x=TeacherArrangment.objects.create(teacher=tchr,course=crse)
		for j in checkedlis:
			x.section.add(Section.objects.get(id=j))
			x.save()
			asesmentss=Assesment.objects.filter(course=x.course).filter(section=Section.objects.get(id=j))
			for asm in asesmentss:
				asm.teacher=tchr
				asm.save()


	context={'courses':courses,'teachers':teachers,'sections':sections,'course':'Course:-','section':'Sections:-','teacher':'Teacher:-'}
	return render(request,'student/registerrr.html',context)
#@login_required(login_url='login')
#@allowed_users(['teacher'])
def registercourse(request):
	#generatetranscript()
	generatetotal()
	generatecoursesectionstanding()
	generatecourseallstanding()
	generatesectionstanding()
	generateallstanding()
	
	
	#generate()
	#generateteacher()
	depts=Department.objects.all()
	grades=Grade.objects.all()
	if request.method=='POST':
		x=request.POST.get('crid')
		y=request.POST.get('crn')
		t=request.POST.get('dp')
		u=request.POST.get('gr')
		c=Course.objects.create(course_id=x,course_name=y,department=Department.objects.get(id=t),grade=Grade.objects.get(id=u))
		sec=Section.objects.filter(grade=u)
		for j in sec:
			j.withcourse[c.course_id]=0
			j.save()
	context={'depts':depts,'grades':grades}
	return render(request,'student/regcourse.html',context)



@login_required(login_url='login')
@allowed_users(['teacher'])
def teacherupdate(request):
	tear=request.user.teacher
	customerform=TeacherForm(instance=tear)
	if request.method=="POST":
		customerform=TeacherForm(request.POST,request.FILES,instance=tear)
		if   customerform.is_valid():
			customer=customerform.save()
			messages.success(request,"registered successfully")
			
	context={"customerform":customerform}
	return render(request,'student/accountsetting.html',context)

@login_required(login_url='login')
@allowed_users(['department'])
def departmenthomepage(request):
	context={}
	return render(request,'student/departmenthomepage.html',context)
@login_required(login_url='login')
@allowed_users(['student'])
def transcript(request):
	semister=Semister.objects.get(active=False)
	st={}
	z=request.user.student.enroll_year.year
	for j in range(8,z):
		x=Assesment.objects.filter(student=request.user.student).filter(semister='semisterI').filter(section__grade__year=j+1)
		y=Assesment.objects.filter(student=request.user.student).filter(semister='semisterII').filter(section__grade__year=j+1)
		ttt=Transcript.objects.filter(student=request.user.student).filter(semister=Semister.objects.first()).filter(grade__year=j+1).first()
		ddd=Transcript.objects.filter(student=request.user.student).filter(semister=Semister.objects.last()).filter(grade__year=j+1).first()
		x=OrderedSet(x)
		x.add(ttt)
		y=OrderedSet(y)
		y.add(ddd)
		st[str(j)+'semisterI']=x
		st[str(j)+'semisterII']=y
	context={'assesments':st}
	return render(request,'student/transcript.html',context)
@login_required(login_url='login')
@allowed_users(['department'])
def submitted_list(request):
	x=TeacherArrangment.objects.filter(teacher__department=request.user.department)
	context={"teacherarrangements":x}
	return render(request,'student/submittedlist.html',context)
@login_required(login_url='login')
@allowed_users(['department'])
def resubmit(request,pk):
	y=TeacherArrangment.objects.get(id=pk)
	semister=Semister.objects.get(active=True)
	z=Assesment.objects.filter(teacher=y.teacher).filter(semister=semister.semister).filter(course__course_id=y.course.course_id)
	for k in z:
		k.finished=False
		k.save()
	context={'y':y}
	return render(request,'student/resubmit.html',context)
@login_required(login_url='login')
@allowed_users(['department'])
def teacherarrangementUpdate(request,crs,sect,arr):
	secti=Section.objects.get(id=sect)
	secti.withcourse[crs]=0
	secti.save()
	y=TeacherArrangment.objects.get(id=arr).section.remove(secti)
	return redirect("teacherarrange")


def adminpage(request):
	semisters=Semister.objects.all()
	if request.method=='POST':
		"""generatetotal()
		generatecoursesectionstanding()
		generatecourseallstanding()
		generatesectionstanding()
		generatewholetotal()
		generateallstanding()
		generatewholetotal()
		#setarrangementnull()
		generatewholesectionstanding()
		generatewholeallstanding()
		generatepassfail()
		setarrangementnull()"""
		checkedlis=request.POST.getlist('semister')
		print(checkedlis)
		if len(checkedlis)==2 or len(checkedlis)==0:
			return HttpResponse('<h1> only one must be activated and not two semisters can be not activated </h1>')
		sem=Semister.objects.get(id=checkedlis[0])
		sem.active=True
		sem.save()
		sr=Semister.objects.all()
		for m in sr:
			if m.id != int(checkedlis[0]):
				m.active=False
				m.save()
				print("congra worked")
	context={'semisters':semisters}
	return render(request,'student/adminpage.html',context)






def registeration(request):
	year=request.user.student.enroll_year.year
	year+=1
	grade=Grade.objects.get(year=year)
	courses=Course.objects.get(grade=grade)
	y=request.user.student
	if request.method=='POST':
		for course in courses:
			Assesment.objects.create(course=course,student=request.user.student,semister='semisterI')
			Assesment.objects.create(course=course,student=request.user.student,semister='semisterII')
	y.enroll_year=grade
	y.save()
	return HttpResponse("<h2>Registered</h2>")
	return render(request,'student/register.html',context)

def transfer(request):
	y=Transcript.objects.filter(student=request.user.student,grade = request.user.student.enroll_year,semister=Semister.objects.last()).first()
	if y.complete:
		courses=Course.objects.filter(grade__year = request.user.student.enroll_year.year + 1)
	else:
		return HttpResponse("<h2>you have registered successfulyy  for the  grade"+str(request.user.student.enroll_year.year)+" </h2>")
	if request.method=="POST":
		x=request.user.student
		gr=Grade.objects.get(year=request.user.student.enroll_year.year+1)
		x.enroll_year=gr
		x.save()
		sections=Section.objects.filter(grade=gr)
		for k in courses:
			Assesment.objects.create(course=k,student=request.user.student,semister=Semister.objects.first().semister,section=sections[x.id % len(sections)])
			Assesment.objects.create(course=k,student=request.user.student,semister=Semister.objects.last().semister,section=sections[x.id % len(sections)])
		Transcript.objects.create(student=request.user.student,semister=Semister.objects.first(),grade=gr,section=sections[x.id % len(sections)])
		Transcript.objects.create(student=request.user.student,semister=Semister.objects.last(),grade=gr,section=sections[x.id % len(sections)])
	context={}
	return render(request,'student/transfer.html',context)






def registerstus():
		stus=Student.objects.filter(enroll_year=Grade.objects.get(year=9))
		for j in stus:
			y=Transcript.objects.filter(student=j,grade = j.enroll_year,semister=Semister.objects.last()).first()
			if not y.complete:
				courses=Course.objects.filter(grade__year = j.enroll_year.year)
				gr=Grade.objects.get(year=9)
				sections=Section.objects.filter(grade=gr)
				for k in courses:
					x=Assesment.objects.get(course=k,student=j,semister=Semister.objects.first().semister)
					x.finished=False
					x.save()
					y=Assesment.objects.get(course=k,student=j,semister=Semister.objects.last().semister)
					y.finished=False
					y.save()


					
					
					
@login_required(login_url='login')
def changepassword(request):
	if request.method=='POST':
		passw1=request.POST.get('passw1')
		passw2=request.POST.get('passw2')
		if passw1 != passw2 or len(passw1)<4:
			return HttpResponse('two passwords didnot match or lessthan 4 characters')
		x=request.user
		x.set_password(passw1)
		x.save()
		return redirect('/')
	return render(request,'student/passchange.html',{})					
					
					
					
					
					
					
					
					
					
					
					
					
					
					
					
					
					
					
				
