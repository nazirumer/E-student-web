from django.db import models
from django.contrib.auth.models import User
import jsonfield
# Create your models here.
class Department(models.Model):
	user=models.OneToOneField(User,null=True,on_delete=models.CASCADE)
	name=models.CharField(max_length=200,null=True)
	logo=models.ImageField(null=True,default='profile1.jpg')
	def __str__(self):
		return self.name
class Grade(models.Model):
	year=models.IntegerField(null=True)
	def __str__(self):
		return str(self.year)
class Section(models.Model):
	grade=models.ForeignKey(Grade,null=True,on_delete=models.SET_NULL)
	room_num=models.IntegerField(null=True)
	withcourse=jsonfield.JSONField(blank=True,default={})
	class Meta:
		unique_together = ['grade', 'room_num']
	def __str__(self):
		return str(self.grade) + " --> " + str(self.room_num)
class Student(models.Model):
	user=models.OneToOneField(User,on_delete=models.CASCADE)
	first_name=models.CharField(max_length=200,null=True)
	last_name=models.CharField(max_length=200,null=True)
	ministry_result=models.FloatField(max_length=200,null=True)
	matric_result=models.FloatField(max_length=200,null=True,blank=True)
	emergency_contact_name=models.CharField(max_length=200,null=True,blank=True)
	emergency_phone_number=models.CharField(max_length=200,null=True,)
	enroll_year=models.ForeignKey(Grade,null=True,on_delete=models.SET_NULL)
	section = models.ForeignKey(Section,null=True,on_delete=models.SET_NULL)
	position=jsonfield.JSONField(default={'grade9':{'total':0,'pass':True,}})
	propic=models.ImageField(null=True,default='profile1.jpg')
	def __str__(self):
		return self.user.username

class Teacher(models.Model):
	user=models.OneToOneField(User,on_delete=models.CASCADE)
	first_name=models.CharField(max_length=200,null=True)
	last_name=models.CharField(max_length=200,null=True)
	department=models.ForeignKey(Department,null=True,on_delete=models.SET_NULL)
	propic=models.ImageField(null=True,default='profile1.jpg')
	def __str__(self):
		return str(self.user.username)
class Course(models.Model):
	course_id=models.CharField(max_length=40,null=True,unique=True)
	course_name=models.CharField(max_length=200,null=True)
	department=models.ForeignKey(Department,null=True,on_delete=models.SET_NULL)
	grade=models.ForeignKey(Grade,null=True,on_delete=models.SET_NULL)
	def __str__(self):
		return self.course_id
		
class Assesment(models.Model):
	course=models.ForeignKey(Course,null=True,on_delete=models.SET_NULL)
	student=models.ForeignKey(Student,null=True,on_delete=models.CASCADE)
	teacher=models.ForeignKey(Teacher,null=True,on_delete=models.SET_NULL)
	asgt=jsonfield.JSONField(default={})
	wholetot=models.FloatField(null=True)
	wholestatus=models.CharField(max_length=200,null=True,blank=True,choices=(('red','red'),('green','green'),('yellow','yellow')))
	result=models.FloatField(null=True)
	status=models.CharField(max_length=200,null=True,blank=True,choices=(('red','red'),('green','green'),('yellow','yellow')))
	section=models.ForeignKey(Section,null=True, on_delete=models.SET_NULL)
	semister=models.CharField(max_length=200,default='semisterI',choices=(('semisterI','semisterI'),('semisterII','semisterII')))
	standing_sec=models.IntegerField(null=True,blank=True)
	standing_all=models.IntegerField(null=True,blank=True)
	finished=models.BooleanField(default=False)
	class Meta:
		unique_together = ['course', 'student','semister']
	def __str__(self):
		return str(self.student) +"--->" + str(self.course)

class TeacherArrangment(models.Model):
	teacher=models.ForeignKey(Teacher,null=True,on_delete=models.CASCADE)
	section=models.ManyToManyField(Section,blank=True)
	course= models.ForeignKey(Course,null=True,on_delete=models.CASCADE)
	semister=models.CharField(max_length=200,default='semisterI',choices=(('semisterI','semisterI'),('semisterII','semisterII')))
	submitted=models.BooleanField(default=False)
	class Meta:
		unique_together = ['course', 'teacher']
	def __str__(self):
	 	return str(self.teacher) +"-->"  + str(self.course)

class jsoncheck(models.Model):
 	name=models.CharField(max_length=67,null=True)
 	exam=jsonfield.JSONField(null=True,default={})
 	total=models.FloatField(null=True)
 	def __str__(self):
 		return self.name
class Semister(models.Model):
	semister=models.CharField(max_length=200,default='semisterI',choices=(('semisterI','semisterI'),('semisterII','semisterII')))
	active=models.BooleanField()
	class Meta:
		unique_together = ['semister', 'active']

	def __str__(self):
		return self.semister
class Transcript(models.Model):
	student=models.ForeignKey(Student,null=True,on_delete=models.CASCADE)
	grade=models.ForeignKey(Grade,null=True,on_delete=models.SET_NULL)
	semister=models.ForeignKey(Semister,null=True,on_delete=models.SET_NULL)
	total=models.FloatField(null=True,blank=True)
	avg=models.FloatField(null=True,blank=True)
	complete=models.BooleanField(default=False)
	wholeavg=models.FloatField(null=True,blank=True)
	wholetotal=models.FloatField(null=True,blank=True)
	wholestanding_all=models.IntegerField(null=True,blank=True)
	wholestanding_sec=models.IntegerField(null=True,blank=True)
	standing_sec=models.IntegerField(null=True,blank=True)
	standing_all=models.IntegerField(null=True,blank=True)
	standing_sec=models.IntegerField(null=True,blank=True)
	finished=models.BooleanField(default=False)
	section=models.ForeignKey(Section,null=True,on_delete=models.SET_NULL)
	class Meta:
		unique_together = ['student', 'semister','grade']
		ordering = ['student']
	def __str__(self):
		return self.student.first_name + ' --> ' + str(self.grade.year)



class Upcoming(models.Model):
	title=models.CharField(null=True,max_length=2000)
	description=models.TextField(null=True)
	initial_date=models.DateField(null=True)
	final_date=models.DateField(null=True)
	def __str__(self):
		return self.title
