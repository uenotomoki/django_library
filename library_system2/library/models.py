from django.db import models
from django.core.validators import *
from django.utils import timezone
# Create your models here.

#Membersテーブルの定義
class Member(models.Model):
    name = models.CharField(max_length=20)
    post_number = models.CharField(max_length=8,validators=[RegexValidator(r'[0-9]{3}-[0-9]{4}', '正しい形式(ooo-oooo)で入力してください。')])
    address = models.CharField(max_length=60)
    tel_number = models.CharField(max_length=20,validators=[RegexValidator(r'[0-9]{2,4}-[0-9]{3,4}-[0-9]{3,4}', '[-]つきの形式で入力してください。')])
    email = models.EmailField(max_length=30)
    birthday = models.DateField(blank=True,null=True)
    entry_day = models.DateField(auto_now_add=True)
    quit_day = models.DateField(blank=True,null=True)
    password = models.CharField(max_length=16,validators=[RegexValidator(r'[a-zA-Z0-9]{8,16}')])

    def __str__(self):
        return self.name

#Staffsテーブルの定義
class Staff(models.Model):
    name = models.CharField(max_length=20)
    password = models.CharField(max_length=16)

    def __str__(self):
        return self.name

#資料目録の定義
class Docindex(models.Model):
    isbn = models.CharField(primary_key=True,max_length=13,validators=[RegexValidator(r'[0-9]{13}','isbn番号は13桁の数字で入力してください')])
    name = models.CharField(max_length=100)
    type_code = models.IntegerField(validators = [RegexValidator(r'[0-9]{1}','分類コードは1桁の数字を入力してください')])
    author = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100)
    publication_day = models.DateField()

#資料台帳の定義
class Doclist(models.Model):
    docindex = models.ForeignKey(Docindex,on_delete=models.CASCADE)
    arrival_day = models.DateField(auto_now_add=True)
    disposal_day = models.DateField(blank=True,null=True)
    remarks = models.CharField(max_length=300,blank=True,null=True)

#貸出台帳の定義
class Lendlist(models.Model):
    member = models.ForeignKey(Member,on_delete=models.CASCADE)
    doclist = models.ForeignKey(Doclist,on_delete=models.CASCADE)
    lend_day = models.DateField(auto_now_add=True)
    return_limit = models.DateField()
    return_day = models.DateField(blank=True,null=True)
    remarks = models.CharField(max_length=300,blank=True,null=True)

#予約台帳の定義
class Reservelist(models.Model):
    member = models.ForeignKey(Member,on_delete=models.CASCADE)
    docindex = models.ForeignKey(Docindex,on_delete=models.CASCADE)
    doclist = models.ForeignKey(Doclist,on_delete=models.CASCADE,blank=True,null=True)
    reserve_day = models.DateField(auto_now_add=True)
    lent = models.BooleanField(default=False)
    cancel = models.BooleanField(default=False)
    remarks = models.CharField(max_length=300,blank=True,null=True)


#評価コメントテーブルの定義
class Evaluation(models.Model):
    member = models.ForeignKey(Member,on_delete=models.CASCADE)
    docindex = models.ForeignKey(Docindex,on_delete=models.CASCADE)
    evaluation = models.IntegerField(validators = [MinValueValidator(1),MaxValueValidator(5)])
    comment = models.CharField(max_length=144)
