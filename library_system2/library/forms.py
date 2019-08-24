from django import forms
from .models import *
import re



#会員検索画面フォーム
class MemberSearchForm(forms.Form):
    id = forms.IntegerField(label='ID')

#新規会員登録フォーム
class MemberModelForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['name','post_number','address','tel_number','email','birthday']
        labels = {
            'name': '氏名',
            'post_number':'郵便番号',
            'address':'住所',
            'tel_number':'電話番号',
            'email':'E-mail',
            'birthday':'誕生日',
        }
        widgets = {
            'name':forms.TextInput(attrs={'placeholder':'山田太郎'}),
            'post_number':forms.TextInput(attrs={'placeholder':'000-0000'}),
            'address':forms.TextInput(attrs={'placeholder':'都道府県市区町村番地'}),
            'tel_number':forms.TextInput(attrs={'placeholder':'000-0000-0000'}),
            'email':forms.TextInput(attrs={'placeholder':'example@example.com'}),
            'birthday':forms.TextInput(attrs={'placeholder':'yyyy-mm-dd'})
        }


#memberフォーム
class MemberForm(forms.Form):
    # now = datetime.year.now()
    # now = int(now)
    name = forms.CharField(label='名前',widget=forms.TextInput(attrs={'placeholder':'山田太郎'}),max_length=20)
    post_number = forms.CharField(label='郵便番号',widget=forms.TextInput(attrs={'placeholder':'000-0000'}),max_length=8)
    address = forms.CharField(label='住所',widget=forms.TextInput(attrs={'placeholder':'都道府県市区町村番地マンション名'}),max_length=60)
    tel_number = forms.CharField(label='電話番号',widget=forms.TextInput(attrs={'placeholder':'000-0000-0000'}),max_length=20)
    email = forms.EmailField(label='E-mail',widget=forms.TextInput(attrs={'placeholder':'example@example.com'}),max_length=30)
    birthday = forms.DateField(label='誕生日',required=False,input_formats=['%y-%m-%d'],widget=forms.TextInput(attrs={'placeholder':'yyyy-mm-dd'}))



#パスワードを入れるフォーム
class PasswordForm(forms.Form):
    password = forms.CharField(label='パスワード',min_length=8,max_length=16)


class PasswordModelForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['password']
        labels = {
            'password':'パスワード'
        }


class StaffForm(forms.Form):
    ID = forms.CharField(label='id')
    password = forms.CharField(max_length=16,min_length=8,widget=forms.PasswordInput)


#資料を貸し出すときのフォーム
class IdForm(forms.Form):
    mid = forms.IntegerField(label='申請者ID')
    did = forms.IntegerField(label='資料ID')


class DocindexModelForm(forms.ModelForm):
    class Meta:
        model = Docindex
        fields = ['name','type_code','author','publisher','publication_day']
        labels ={
            'name':'本タイトル',
            'type_code':'分類コード',
            'author':'著者名',
            'publisher':'出版社名',
            'publication_day':'出版日'
        }
        widgets = {
                    'type_code':forms.TextInput(attrs={'pattern':'^[0-9]{1}$', 'title':'数字1桁で入力してください'})
        }

class DoclistForm(forms.Form):
    docindex = forms.CharField(max_length=13,label='isbn番号',widget=forms.TextInput(attrs={'pattern':'^[0-9]{13}$', 'title':'数字13桁で入力してください'}))
    arrival_day = forms.DateField(label='入荷日',initial=timezone.now)
    remarks = forms.CharField(max_length=300,label='備考',required=False)



class DocSearchForm(forms.Form):
    data = [
        ('isbn','isbn番号'),
        ('name','本タイトル'),
        ('author','著者'),
    ]
    choices = forms.ChoiceField(choices=data)
    find = forms.CharField()
#会員用サーチフォーム
class DocSearchForm1(forms.Form):
    data = [
        ('name','本タイトル'),
        ('author','著者'),
    ]
    choices = forms.ChoiceField(choices=data)
    find = forms.CharField()
#資料を予約する時のフォーム
class ReserveForm(forms.Form):
    mid = forms.IntegerField(label='申請者ID')
    dname = forms.CharField(label='予約したい資料名')

#############################################################################

#パスワード変更フォーム
class EditPasswordForm(forms.Form):
    beforepass=forms.CharField(label='現在のパスワード',min_length=8,max_length=16)
    newpassword1 = forms.CharField(label='新規パスワード',min_length=8,max_length=16,widget=forms.PasswordInput())
    newpassword2 = forms.CharField(label='新規パスワード(確認用)',min_length=8,max_length=16,widget=forms.PasswordInput())

#会員貸出フォーム
class DocLendForm(forms.Form):
    did = forms.IntegerField(label='資料ID',min_value=1)

class MResultForm(forms.Form):
    data=[
    (1,'資料名'),
    (2,'著者名'),
    ]
    choices = forms.ChoiceField(label='検索フォーム',choices=data)
    find = forms.CharField(required=False)

class ComentForm(forms.Form):
    evaluation=forms.IntegerField(label='評価', max_value=5,min_value=1)
    comment= forms.CharField(label='コメント',widget=forms.Textarea,max_length=144)
