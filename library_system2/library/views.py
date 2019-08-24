from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import *
from .models import *
import random,string
import datetime
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
from django.core.paginator import Paginator
import math
# Create your views here.

#ランダムなパスワード生成関数
def randompw(n):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))
###############################################################################
##関数

#session管理関数
# def session(request):
#     if 'user_id' not in request.session:
#         redirect(to='mlogin')
#     return 1

#ログイン失敗
def miss(request,message):
    params = {
        'form':StaffForm(),
        'message':message,
            }

    return render(request,'library/mlogin.html',params)
#パスワード関数
def passform(request,alert):
    form=EditPasswordForm()
    params={
        'alert':alert,
        'form':form,
    }
    return render(request,'library/edit_pass.html',params)
#貸出
def misslend(request,alert):
    params = {
        'alert':alert,
    }
    return render(request,'library/doc_lend_info.html',params)
#返却日取得
def limitday(docindex):
    #返却日付判定
    now = datetime.date.today()
    dif = now-docindex.publication_day              #現在の日付ー出版日

    #新刊判定
    if  dif.days <=90:
        #新刊だったら貸出期限10日
        delta = timedelta(days=+10)
    else:
        #新刊以外は貸出期限15日
        delta = timedelta(days=+15)

    return_limit = now + delta
    return return_limit
#返却
def userreturn(request,list,alert):
    params={
        'alert':alert,
        'list':list,
        }

    return render(request,'library/mreturn.html',params)

#ページネーション
def page(request,list,size,form,no,choices,find):
    kazu = len(list)
    page_kazu = math.ceil(kazu/size)
    plist = [i for i in range(1,page_kazu+1)]
    page = Paginator(list,size)
    records = page.get_page(no)
    params={
        'forms':form,
        'list':records,
        'plist':plist,
        'page':page,
        'num':no,
        'choices':choices,
        'find':find,
    }
    return params



#履歴表示
def userresult1(request,params):

    return render(request,'library/mresult.html',params)

def userresult2(request,params):

    return render(request,'library/mresult2.html',params)
#############################################################################
def mlogin(request):

    if 'user_id' in request.session:
        request.session.flush()

    message='会員IDとパスワードを入力してください'
    params = {
        'form':StaffForm(),
        'message':message,
    }
    return render(request,'library/mlogin.html',params)

def mmypage(request):
    if(request.method == 'POST'):
        #職員ID
        id = request.POST['ID']
        #職員パスワード
        pw = request.POST['password']
        ##E-1判定
        try:
            id=int(id)
        except Exception:
            message='会員IDは数字で入力してください'
            return miss(request,message)

        ##ログイン判定
        try:
            user = Member.objects.filter(quit_day=None).get(id=id,password=pw)
            params = {
                'user':user,
            }
            request.session['user_id'] = id
            return render(request,'library/mmypage.html',params)
        except:
            message='入力情報が間違っています'
            print(id)
            print(pw)
            return miss(request,message)

    else:
        #セッション判定
        if 'user_id' not in request.session:
            return redirect(to='mlogin')

        user = Member.objects.filter(id=request.session['user_id']).first()
        params = {'user':user}
        return render(request,'library/mmypage.html',params)

#会員情報詳細
def minfo(request):
    #セッション判定
    if 'user_id' not in request.session:
        return redirect(to='mlogin')

    id = request.session['user_id']

    try:
        member = Member.objects.filter(quit_day=None).get(id=id)
        params = {
            'member':member,
        }
    except:
        miss('ログインしてください')
    finally:
        return render(request,'library/m_info.html',params)

def mupdate(request):
        if 'user_id' not in request.session:
            return redirect(to='mlogin')
        #初期条件 会員情報取得
        id = request.session['user_id']
        member = Member.objects.filter(quit_day=None).get(id=id)

        #編集フォーム表示
        if request.method == 'GET':

            forms = MemberModelForm(instance=member)

            params = {
                'forms':forms,
                'id':id,
            }
            return render(request,'library/mupdate.html',params)

        #編集内容更新
        if request.method == 'POST':
            member = Member.objects.filter(quit_day=None).get(id=id)
            forms = MemberModelForm(request.POST,instance=member)
            #更新
            if forms.is_valid():
                forms.save()
                name = member.name
                params = {
                    'member':member,
                    'alert':name+'さんの会員情報を更新しました'
                }

                return render(request,'library/m_info.html',params)
            else:
                params = {
                    'forms':forms,
                    'id':id,
                }
                return render(request,'library/mupdate.html',params)


#パスワード変更
def editpass(request):
    #セッション判定
    if 'user_id' not in request.session:
        return redirect(to='mlogin')
    #初期条件 会員情報取得
    id = request.session['user_id']
    if request.method=='GET':
        return passform(request,'現在のパスワードと新規のパスワードを入力してください')

    else:
        member = Member.objects.filter(quit_day=None).get(id=id)
        #入力情報の取得
        pw=member.password
        pw0=request.POST['beforepass']
        pw1=request.POST['newpassword1']
        pw2=request.POST['newpassword2']

        #判定
        if (pw != pw0):
            return passform(request,'現在のパスワードが違います')

        if (pw1!=pw2):
            return passform(request,'新規パスワードの入力情報が異なります')
        else:
            if(pw1==pw):
                return passform(request,'現在のパスワードと新規パスワードが同じです')

        member.password=pw1
        member.save()
        print(member.password)
        name = member.name
        params = {
            'member':member,
            'alert':name+'さんのパスワードを更新しました'
        }

        return render(request,'library/m_info.html',params)

#貸出
def mlend(request):
    #セッション判定
    if 'user_id' not in request.session:
        return redirect(to='mlogin')
    #初期条件 会員情報取得
    id = request.session['user_id']
    member=Member.objects.filter(quit_day=None).get(id=id)
    if request.method=='GET':
        forms = DocLendForm()
        params = {
            'forms':forms,
        }
        #申請者に貸出不可（貸出冊数6冊以上、延滞資料あり）を判定

        #貸出中の資料一覧
        lends = Lendlist.objects.filter(member_id=id).filter(return_day=None)
        if lends.first() is None:

            return render(request,'library/doc_lend.html',params)
        else:
            #貸出が5つまでか判定
            if lends.count() >= 5:
                return misslend(request,'申請者にはすでに5冊貸し出しています')
            else:
                #貸出5冊以内
                for lend in lends:
                    dif=datetime.date.today()-lend.return_limit
                    if dif.days > 0:
                        return misslend(request,'申請者に延滞資料があります')

        return render(request,'library/doc_lend.html',params)

    else:
        did = request.POST['did']

        try:
            doc = Doclist.objects.filter(disposal_day=None).get(id=did)
            docindex = Docindex.objects.get(isbn=doc.docindex_id)
        except:
            return misslend(request,'該当する資料がありません')

        #返却日取得
        return_limit=limitday(docindex)

        #貸出可能判定
        try:
            lend = Lendlist.objects.filter(doclist_id=doc).get(return_day = None)
            return misslend(request,'すでに貸し出された資料です 資料idを見直してください')
        except:
            try:
                reserve = Reservelist.objects.filter(doclist_id=doc).get(lent=False,cancel=False)

                #予約が申請者本人本人じゃないとき
                if reserve.member_id != id:
                    return misslend(request,'入力したIDの資料は予約済みです')
            except:
                #正規処理
                params = {
                    'doc':doc,
                    'docindex':docindex,
                    'member':member.name,
                    'today':datetime.date.today(),
                    'return_limit':return_limit,
                }
                return render(request,'library/doc_lend_info.html',params)

def mlendsave(request):
    #セッション判定
    if 'user_id' not in request.session:
        return redirect(to='mlogin')
    #初期条件 会員情報取得
    id = request.session['user_id']

    if request=='GET':
        return redirect(to='mlend')
    else:
        did = request.POST['did']
        remarks = request.POST['remarks']
        today = datetime.date.today()

        #資料があるか判定
        try:
            doc = Doclist.objects.filter(disposal_day=None).get(id=did)
            docindex = Docindex.objects.get(isbn=doc.docindex_id)
        except:
            return misslend(request,'該当する資料がありません')

        #入力したIDがすでに貸し出されている資料のIDのとき
        try:
            lend = Lendlist.objects.filter(doclist_id=doc).get(return_day=None)
            return misslend(request,'すでに貸出処理が完了しています')
        except:
            pass
        return_limit=limitday(docindex)


        #貸出インスタンスを生成
        lenddoc = Lendlist()
        #外部キーを参照させる
        lenddoc.member_id = id
        lenddoc.doclist = doc
        #貸出日返却日を記録
        lenddoc.return_limit = return_limit
        lenddoc.remarks = remarks
        #貸出インスタンス保存
        lenddoc.save()

        params = {
            'alert':'貸出が完了しました'
        }

        #資料が予約してあった場合
        try:
            reserve = Reservelist.objects.filter(member_id=id,docindex_id=docindex).get(lent=False,cancel=False)
            reserve.lent=True
            reserve.save()

        except:
            pass
        return render(request,'library/doc_lend_save.html',params)

#返却

def mreturn(request):
    #セッション判定
    if 'user_id' not in request.session:
        return redirect(to='mlogin')
    #初期条件 会員情報取得
    id = request.session['user_id']
    if request.method=='GET':
        mreturn=Lendlist.objects.filter(member_id=id,return_day=None)
        if mreturn.first() is None:
            return userreturn(request,mreturn,'貸出中の資料は存在しません')

        else:
            return userreturn(request,mreturn,'返却資料を選択してください')

    else:
        did = request.POST['did']
        member=Member.objects.filter(quit_day=None).get(id=id)
        #指定したidの資料があるか判定
        try:
            doc = Doclist.objects.filter(disposal_day=None).get(id=did)
            docindex = Docindex.objects.get(isbn=doc.docindex_id)
        except:
            params = {
                'alert':'該当する資料がありません'
            }
            return render(request,'library/doc_return_info.html',params)

        #入力したIDが間違っているまたはすでに返却処理がされたとき
        try:
            lend = Lendlist.objects.filter(doclist_id=doc).get(return_day=None)

        except:
            params = {
                'alert':'貸出情報が存在しません'
            }
            return render(request,'library/doc_return_info.html',params)


        #貸出日と返却期限を表示
        return_limit=lend.return_limit
        lend_day=lend.lend_day
        params = {
            'doc':doc,
            'docindex':docindex,
            'member':member,
            'lend_day':lend_day,
            'return_limit':return_limit
        }

        return render(request,'library/doc_return_info.html',params)

def mreturnsave(request):

    if 'user_id' not in request.session:
        return redirect(to='mlogin')
        #初期条件 会員情報取得
    id = request.session['user_id']

    if request=='GET':
            return redirect(to='mreturn')
    else:
        #ポストから情報を取得
        did = request.POST['did']

        #資料があるか判定
        try:
            doc = Doclist.objects.filter(disposal_day=None).get(id=did)
            docindex = Docindex.objects.get(isbn=doc.docindex_id)
        except:
            params = {
                'alert':'該当する資料がありません'
            }
            return render(request,'library/doc_return_save.html',params)

        #入力したIDがすでに返却されている資料のIDのとき
        try:
            lend = Lendlist.objects.filter(doclist_id=doc).get(return_day=None)
        except:
            params = {
                'alert':'すでに返却されているまたは貸出情報がありません'
            }
            return render(request,'library/doc_return_info.html',params)

        #返却日を記録する
        lend.return_day=datetime.date.today()
        lend.save()

        params = {
            'alert':'返却が完了しました。資料を整理待ち棚に入れてください。'
        }

        #返却した資料に予約が入っている場合
        try:
            reserve = Reservelist.objects.filter(docindex_id=docindex).filter(lent=False,cancel=False).order_by('reserve_day')

            reserve.first().doclist=doc
            reserve.first().save()

            params = {
                'alert':'返却が完了しました。予約された資料なので予約待ち棚に入れてください。'
            }
        except:
            pass

        return render(request,'library/doc_return_save.html',params)

#履歴
def mresult1(request,no):
    #セッション判定
    if 'user_id' not in request.session:
        return redirect(to='mlogin')
    #初期条件 会員情報取得
    id = request.session['user_id']

    if (request.method=='GET'):
        choices = 2
        find=''
        if 'choices' in request.GET:
            choices = request.GET['choices']
        if 'find' in request.GET:
            find = request.GET['find']

        form=MResultForm(request.GET)
        memberresult=Lendlist.objects.filter(member_id=id,return_day__contains='-')
        params=page(request,memberresult,5,form,no,choices,find)
        return userresult1(request,params)

def mresult2(request,no):
    if 'user_id' not in request.session:
        return redirect(to='mlogin')
    #初期条件 会員情報取得
    id = request.session['user_id']
    choices = 2
    find=''
    if 'choices' in request.GET:
        choices = int(request.GET['choices'])
    else:
        choices=int(request.GET['choices'])

    if 'find' in request.GET:
        find = request.GET['find']
        print('こっち')
        print(find)
    else:
        find=request.GET.get('find','')
        print('あっち')
        print(find)
    if (request.method == 'GET'):

        form=MResultForm(request.GET)
        if (choices == 1):
            #資料名検索
            memberresult=Lendlist.objects.filter(member_id=id,return_day__contains='-',doclist_id__docindex_id__name__contains=find)

        else:
            #出版社検索
            memberresult=Lendlist.objects.filter(member_id=id,return_day__contains='-',doclist_id__docindex_id__publisher__contains=find)

        params=page(request,memberresult,5,form,no,choices,find)
        return userresult2(request,params)


def comment(request):
    if 'user_id' not in request.session:
        return redirect(to='mlogin')
    #初期条件
    id = request.session['user_id']

    if (request.method=='GET'):
        return redirect(to='mresult1')
    else:
        userid=request.POST['userid']
        isbn=request.POST['isbn']
        try:
            det=Docindex.objects.get(isbn=isbn)
        except:
            form=MResultForm()
            params={
                'forms':form,
                'list':Lendlist.objects.filter(member_id=id,return_day__contains='-'),
                'alert':'資料は破棄されています',
                }
            return render(request,'library/mresult.html',params)

        form=ComentForm()
        params={
            'form':form,
            'det':det,
            'isbn':isbn,
        }
        return render(request,'library/comment.html',params)

def comment_conf(request):
    if 'user_id' not in request.session:
        return redirect(to='mlogin')
    #初期条件
    id = request.session['user_id']
    if (request.method=='GET'):
        return redirect(to='mresult')
    else:
        comment=request.POST['comment']
        evaluation=request.POST['evaluation']
        isbn=request.POST['isbn']
        params={
            'comment':comment,
            'evaluation':evaluation,
            'isbn':isbn,
        }
        return render(request,'library/comment_conf.html',params)

def comment_save(request):
    if 'user_id' not in request.session:
        return redirect(to='mlogin')
    #初期条件
    id = request.session['user_id']
    if (request.method=='GET'):
        return redirect(to='mresult')
    else:
        content=Evaluation()
        content.comment=request.POST['comment']
        content.evaluation=request.POST['evaluation']
        content.member_id=id

        isbn=int(request.POST['isbn'])
        content.docindex_id=isbn
        print(type(isbn))

        content.save()

        form=MResultForm()
        params={
            'forms':form,
            'list':Lendlist.objects.filter(member_id=id,return_day__contains='-'),
            'alert':'コメントを投稿しました',
            }
        return render(request,'library/mresult.html',params)


#検索
def searchhome(request,no):
    #セッション判定
    if 'user_id' not in request.session:
        return redirect(to='mlogin')
    #初期条件
    id = request.session['user_id']
    if(request.method == 'GET'):
        list = Docindex.objects.all()

        kazu = len(list)
        page_kazu = math.ceil(kazu/5)
        plist = [i for i in range(1,page_kazu+1)]

        page = Paginator(list,5)
        records = page.get_page(no)
        num = no
        params = {
            'objectlist':records,
            'form':DocSearchForm1(),
            'plist':plist,
            'page':page,
            'num':num
        }
        return render(request,'library/mdoc_search.html',params)

def mdoc_listsearch(request,no):

    choices = ''
    find = ''
    if 'choices' in request.GET:
        choices = request.GET['choices']
        print(choices)
    if 'find' in request.GET:
        find = request.GET['find']
        print(find)
    # if (choices == 'isbn'):
    #     object_list = Docindex.objects.filter(isbn = find)
    if (choices == 'name'):
        object_list = Docindex.objects.filter(name__contains = find)
    if (choices == 'author'):
        object_list = Docindex.objects.filter(author__contains = find)

    list = object_list
    kazu = len(list)
    page_kazu = math.ceil(kazu/3)
    plist = [i for i in range(1,page_kazu+1)]
    page = Paginator(list,3)
    records = page.get_page(no)

    params = {
        'form':DocSearchForm1(request.GET),
        'objectlist':records,
        'plist':plist,
        'page':page,
        'num':no,
        'choices':choices,
        'find':find
    }
    return render(request,'library/msearch_result.html',params)

def mdoc_detail(request):
    if 'user_id' not in request.session:
        return redirect(to='mlogin')
    #初期条件
    id = request.session['user_id']
    if(request.method == 'GET'):
        return redirect(to='searchhome')
    else:
        isbn=request.POST['isbn']

        index=Docindex.objects.get(isbn=isbn)
        list=Doclist.objects.filter(docindex_id=isbn)
        print(list)

        comm=Evaluation.objects.filter(docindex_id=isbn)

        print(index)
        params={
            'index':index,
            'comment':comm,
            'list':list,
        }

        return render(request,'library/mdoc_detail.html',params)
##############################################################################
#会員検索画面呼び出し
def member_manage(request):
    if request.method == 'GET':
        if 'sid' not in request.session:
            return redirect(to='slogin')

    form = MemberSearchForm()

    params = {
        'form':form
    }

    return render(request,'library/member_manage.html',params)

#新規会員情報表示
def member_create(request):
    if request.method == 'GET':
        if 'sid' not in request.session:
            return redirect(to='slogin')

        forms = MemberModelForm()

        params = {
            'forms':forms,
        }

        return render(request,'library/member_create.html',params)

    if request.method == 'POST':
        member = Member()
        forms = MemberModelForm(request.POST,instance=member)

        #validationチェック
        if forms.is_valid():
            #フォーム情報取り出し
            name = request.POST['name']
            post_number = request.POST['post_number']
            address = request.POST['address']
            tel_number = request.POST['tel_number']
            email = request.POST['email']
            birthday = request.POST['birthday']


            params = {
                'name':name,
                'post_number':post_number,
                'address':address,
                'tel_number':tel_number,
                'email':email,
                'birthday':birthday,
                'forms':forms,
            }
            return render(request,'library/newmember_conf.html',params)

        else:
            params = {
                'forms':forms,

                }
            return render(request,'library/member_create.html',params)


#新規会員をデータベースに登録
def newmember_save(request):
    if request.method == 'GET':
        if 'sid' not in request.session:
            return redirect(to='slogin')

        return redirect(to='member_manage')
    if request.method == 'POST':
        member = Member()
        form = MemberModelForm(request.POST,instance=member)
        #仮パスワード発行
        pw = randompw(8)
        member.password = pw
        form.save()

        #id保存
        id = member.id
        name = member.name
        params = {
            'id':id,
            'pw':pw,
            'name':name,
        }
        return render(request,'library/temp_password.html',params)


#会員詳細画面表示
def member_info(request,id=0):
    if request.method == 'GET':
        if 'sid' not in request.session:
            return redirect(to='slogin')
        return redirect(to='member_manage')
    else:
        id = request.POST['id']

    try:
        member = Member.objects.filter(quit_day=None).get(id=id)
        params = {
            'member':member,
        }

        if member.quit_day is not None:
            alert = '該当する会員がいません'


            params = {
                'alert':alert,

            }
    except:
        alert = '該当する会員がいません'
        params={
            'alert':alert,
        }
    finally:

        return render(request,'library/member_info.html',params)

#会員情報更新
def member_update(request,id=0):
    if request.method == 'GET':
        if 'sid' not in request.session:
            return redirect(to='slogin')
        if id == 0:
            return redirect(to='member_manage')

        member = Member.objects.filter(quit_day=None).get(id=id)
        if member.quit_day == None:
            forms = MemberModelForm(instance=member)


            pw = member.password

            params = {
                'forms':forms,
                'pw':pw,
                'id':id,
            }
            return render(request,'library/member_update.html',params)

        else:
            return redirect(to='member_manage')


    if request.method == 'POST':
        member = Member.objects.filter(quit_day=None).get(id=id)
        forms = MemberModelForm(request.POST,instance=member)


        #フォーム情報取り出し
        if forms.is_valid():
            #フォーム情報取り出し
            name = request.POST['name']
            post_number = request.POST['post_number']
            address = request.POST['address']
            tel_number = request.POST['tel_number']
            email = request.POST['email']
            birthday = request.POST['birthday']


            params = {
                'name':name,
                'post_number':post_number,
                'address':address,
                'tel_number':tel_number,
                'email':email,
                'birthday':birthday,
                'forms':forms,
                'password':member.password,
                'id':id,
            }
            return render(request,'library/member_update_conf.html',params)

        else:

            params = {
                'forms':forms,
                'id':id,

                }
            # return HttpResponse(forms)
            return render(request,'library/member_update.html',params)
#更新情報保存
def member_update_save(request,id=0):
    if request.method == 'GET':
        if 'sid' not in request.session:
            return redirect(to='slogin')

        return redirect(to='member_manage')

    if request.method == 'POST':
        member = Member.objects.filter(quit_day=None).get(id=id)
        forms = MemberModelForm(request.POST,instance=member)

        forms.save()
        name = member.name
        params = {
            'user':'',
            'alert':name+'さんの会員情報を更新しました'
        }

        return render(request,'library/smypage.html',params)


#会員退会
def member_delete(request,id=0):

    if request.method == 'GET':
        if 'sid' not in request.session:
            return redirect(to='slogin')
        if id == 0:
            return redirect(to='member_manage')
        member = Member.objects.filter(quit_day=None).get(id=id)
        if member.quit_day == None:

            params = {
                'member':member,
                'id':id,
            }
            return render(request,'library/member_delete.html',params)

        else:
            return redirect(to='member_manage')


    if request.method == 'POST':

        member = Member.objects.filter(quit_day=None).get(id=id)
        member.quit_day = datetime.date.today()
        member.save()
        name = member.name
        params = {
            'user':'',
            'alert':name+'さんの退会処理が完了しました',
        }
        return render(request,'library/smypage.html',params)

#職員ログイン
def logout(request):
    if(request.method == 'GET'):
        if 'sid' in request.session:
            del request.session['sid']
        params = {
            'form':StaffForm(),
            # 'message':message,
        }
        return render(request, 'library/slogin.html', params)

def slogin(request):
    if(request.method == 'GET'):
        if 'sid' in request.session:
            del request.session['sid']
    message='職員IDとパスワードを入力してください'
    params = {
        'form':StaffForm(),
        'message':message,
    }
    return render(request,'library/slogin.html',params)

def smypage(request):
    if(request.method == 'POST'):

        #職員ID
        sid = request.POST['ID']
        #職員パスワード
        pw = request.POST['password']
        ##E-1判定
        try:
            sid=int(sid)
        except Exception:
            message='職員IDは数字で入力してください'
            params = {
                'form':StaffForm(),
                'message':message,
            }
            return render(request,'library/slogin.html',params)

        ##ログイン判定

        try:
            user = Staff.objects.get(id=sid,password=pw)
            params = {
                'message':'職員IDとパスワードを入力してください',
                'user':user,
                'msg':'さん、こんにちは。'
            }
            request.session['sid'] = sid
            return render(request,'library/smypage.html',params)
        except:
            params = {
                'form':StaffForm(),
                'message':'入力情報が間違っています'
                    }

            return render(request,'library/slogin.html',params)

    else:
        if 'sid' not in request.session:
            return redirect(to='slogin')
        user = Staff.objects.filter(id=request.session['sid']).first()
        params = {
            'user':user,
            'msg':'さん、こんにちは。'
            }
        return render(request,'library/smypage.html',params)


def document_lend(request):
    if request.method == 'GET':
        if 'sid' not in request.session:
            return redirect(to='slogin')
        forms = IdForm()
        params = {
         'forms':forms
        }
        return render(request,'library/document_lend.html',params)

def document_lend_info(request):
    if request.method == 'GET':
        if 'sid' not in request.session:
            return redirect(to='slogin')
        return redirect(to='document_lend')

    #ポスト情報の取り出し
    mid = request.POST['mid']
    did = request.POST['did']

    #指定したidの会員がいるか判定
    try:
        member = Member.objects.filter(quit_day=None).get(id=mid)
    except:
        params = {
            'alert':'該当する会員がいません'
        }
        return render(request,'library/document_lend_info.html',params)

    #申請者に貸出不可（貸出冊数6冊以上、延滞資料あり）を判定
    try:
        #貸出中の資料一覧
        lends = Lendlist.objects.filter(member_id=member).filter(return_day=None)

        #延滞資料があるか
        for lend in lends:
            dif=datetime.date.today()-lend.return_limit
            if dif.days > 0:
                params = {
                    'alert':'申請者に延滞資料があります'
                }
                return render(request,'library/document_lend_info.html',params)
        #貸出が5つまでか判定
        if lends.count() >= 5:
            params = {
                'alert':'申請者にはすでに5冊貸し出しています'
            }
            return render(request,'library/document_lend_info.html',params)

    except:
        pass


    #指定したidの資料があるか判定
    try:
        doc = Doclist.objects.filter(disposal_day=None).get(id=did)
        docindex = Docindex.objects.get(isbn=doc.docindex_id)


    except:
        params = {
            'alert':'該当する資料がありません'
        }

        return render(request,'library/document_lend_info.html',params)

    #入力したIDがすでに貸し出されている資料のIDのとき
    try:
        lend = Lendlist.objects.filter(doclist_id=doc).get(return_day=None)
        params = {
            'alert':'すでに貸し出された資料です 資料idを見直してください'
        }
        return render(request,'library/document_lend_info.html',params)
    except:
        pass

    #入力したIDが予約済みの資料IDのとき
    try:
        reserve = Reservelist.objects.filter(doclist_id=doc).get(lent=False,cancel=False)

        #予約が申請者本人の時
        if reserve.member_id == mid:
            pass
        #本人じゃないとき
        else:
            params = {
                'alert':'入力したIDの資料は予約済みです'
            }
            return render(request,'library/document_lend_info.html',params)
    except:
        pass

    #返却日付判定
    now = datetime.date.today()
    dif = now-docindex.publication_day              #現在の日付ー出版日

    #新刊判定
    if  dif.days <=90:
        #新刊だったら貸出期限10日
        delta = timedelta(days=+10)
    else:
        #新刊以外は貸出期限15日
        delta = timedelta(days=+15)


    return_limit = now + delta
    #文字型
    # test=datetime.date.today()
    # test2=test.strftime('%Y/%m/%d')

    params = {
        'doc':doc,
        'docindex':docindex,
        'member':member,
        'today':now,
        'return_limit':return_limit
    }


    return render(request,'library/document_lend_info.html',params)

def document_lend_save(request):
    if request.method == 'GET':
        if 'sid' not in request.session:
            return redirect(to='slogin')
        return redirect(to='document_lend')

    #POSTの情報を取得
    did = request.POST['did']
    today = datetime.date.today()
    # print(today)
    # test = datetime.strptime(today,'%Y-%m-%d')
    # print(test)

    #資料があるか判定
    try:
        doc = Doclist.objects.filter(disposal_day=None).get(id=did)
        docindex = Docindex.objects.get(isbn=doc.docindex_id)


    except:
        params = {
            'alert':'該当する資料がありません'
        }

        return render(request,'library/document_lend_info.html',params)
    #入力したIDがすでに貸し出されている資料のIDのとき
    try:
        lend = Lendlist.objects.filter(doclist_id=doc).get(return_day=None)
        params = {
            'alert':'すでに貸出処理が完了しています'
        }
        return render(request,'library/document_lend_info.html',params)
    except:
        pass


    #返却日付判定
    now = datetime.date.today()
    dif = now-docindex.publication_day              #現在の日付ー出版日

    #新刊判定
    if  dif.days <=90:
        #新刊だったら貸出期限10日
        delta = timedelta(days=+10)
    else:
        #新刊以外は貸出期限15日
        delta = timedelta(days=+15)

    return_limit = now + delta


    mid = request.POST['mid']
    remarks = request.POST['remarks']

    try:
        #会員が存在するか確認
        member = Member.objects.filter(quit_day=None).get(id=mid)
    except:
        params = {
            'alert':'該当する会員がいません'
        }
        return render(request,'library/document_lend_save.html',params)

    #貸出インスタンスを生成
    lenddoc = Lendlist()
    #外部キーを参照させる
    lenddoc.member = member
    lenddoc.doclist = doc
    #貸出日返却日を記録
    lenddoc.return_limit = return_limit
    lenddoc.remarks = remarks
    #貸出インスタンス保存
    lenddoc.save()

    params = {
        'alert':'貸出が完了しました'
    }

    #資料が予約してあった場合
    try:
        reserve = Reservelist.objects.filter(member_id=member,docindex_id=docindex).get(lent=False,cancel=False)
        reserve.lent=True
        reserve.save()

    except:
        pass
    return render(request,'library/document_lend_save.html',params)


def document_return(request):
    if request.method == 'GET':
        if 'sid' not in request.session:
            return redirect(to='slogin')
        forms = IdForm()
        params = {
         'forms':forms
        }
        return render(request,'library/document_return.html',params)

def document_return_info(request):
    if request.method == 'GET':
        if 'sid' not in request.session:
            return redirect(to='slogin')
        return redirect(to='document_return')

    #ポスト情報の取り出し
    mid = request.POST['mid']
    did = request.POST['did']

    #指定したidの会員がいるか判定
    try:
        member = Member.objects.filter(quit_day=None).get(id=mid)
    except:
        params = {
            'alert':'該当する会員がいません'
        }
        return render(request,'library/document_return_info.html',params)

    #指定したidの資料があるか判定
    try:
        doc = Doclist.objects.filter(disposal_day=None).get(id=did)
        docindex = Docindex.objects.get(isbn=doc.docindex_id)

    except:
        params = {
            'alert':'該当する資料がありません'
        }
        return render(request,'library/document_return_info.html',params)

    #入力したIDが間違っているまたはすでに返却処理がされたとき
    try:
        lend = Lendlist.objects.filter(doclist_id=doc).get(return_day=None)

    except:
        params = {
            'alert':'貸出情報が存在しません'
        }
        return render(request,'library/document_return_info.html',params)


    #貸出日と返却期限を表示
    return_limit=lend.return_limit
    lend_day=lend.lend_day
    params = {
        'doc':doc,
        'docindex':docindex,
        'member':member,
        'lend_day':lend_day,
        'return_limit':return_limit
    }

    return render(request,'library/document_return_info.html',params)

def document_return_save(request):
    if request.method == 'GET':
        if 'sid' not in request.session:
            return redirect(to='slogin')
        return redirect(to='document_return')

    #ポストから情報を取得
    mid = request.POST['mid']
    did = request.POST['did']

    #資料があるか判定
    try:
        doc = Doclist.objects.filter(disposal_day=None).get(id=did)
        docindex = Docindex.objects.get(isbn=doc.docindex_id)

    except:
        params = {
            'alert':'該当する資料がありません'
        }
        return render(request,'library/document_return_save.html',params)

    #入力したIDがすでに返却されている資料のIDのとき
    try:
        lend = Lendlist.objects.filter(doclist_id=doc).get(return_day=None)
    except:
        params = {
            'alert':'すでに返却されているまたは貸出情報がありません'
        }
        return render(request,'library/document_return_info.html',params)

    #返却日を記録する
    lend.return_day=datetime.date.today()
    lend.save()

    try:
        #会員が存在するか確認
        member = Member.objects.filter(quit_day=None).get(id=mid)
    except:
        params = {
            'alert':'該当する会員がいません'
        }
        return render(request,'library/document_return_save.html',params)


    params = {
        'alert':'返却が完了しました。資料を整理待ち棚に入れてください。'
    }

    #返却した資料に予約が入っている場合
    try:
        reserve = Reservelist.objects.filter(docindex_id=docindex).filter(lent=False,cancel=False).order_by('reserve_day')

        reserve.first().doclist=doc
        reserve.first().save()

        params = {
            'alert':'返却が完了しました。予約された資料なので予約待ち棚に入れてください。'
        }
    except:
        pass

    return render(request,'library/document_return_save.html',params)


##############################################################################


def lend_list(request, no):
    if 'sid' not in request.session:
        return redirect(to='slogin')
    now = datetime.date.today()
    data = Lendlist.objects.filter(return_day=None)
    data = checkoverthirty(data)

    if(request.method == 'GET'):
        kazu = len(data)
        page_kazu = math.ceil(kazu/5)
        plist = [i for i in range(1,page_kazu+1)]

        page = Paginator(data,5)
        records = page.get_page(no)
        num = no
        params = {
            'data':records,
            'check':False,
            'plist':plist,
            'page':page,
            'num':num

        }
        return render(request,'library/lend_list.html',params)

    if(request.method == 'POST'):
        checkday = now - timedelta(days=10)
        data = data.filter(return_limit__lte=checkday)
        data = checkoverthirty(data)
        kazu = len(data)
        page_kazu = math.ceil(kazu/5)
        plist = [i for i in range(1,page_kazu+1)]

        page = Paginator(data,5)
        records = page.get_page(no)
        num = no
        params = {
            'data':records,
            'check':True,
            'plist':plist,
            'page':page,
            'num':num
        }
        return render(request,'library/lend_list.html',params)

def checkoverthirty(data):
    now = datetime.date.today()
    for item in data:
        if item.return_limit <= now - timedelta(days=30):
            item.overthiity = '〇'
    return data

class doc:
    #完了画面のメッセージ
    def messagedone(self,message,title):
        self.params = {
            'title':message,
            'message':title,
        }
        return self.params
#新規資料を登録する
def create_doc(request):
    if 'sid' not in request.session:
        return redirect(to='slogin')
    if(request.method == 'GET'):
        return redirect(to='registdoclist')
    if(request.method == 'POST'):
        isbn = request.session['isbn']

        #新規資料情報を保存
        name = request.POST['name']
        type_code = request.POST['type_code']
        author = request.POST['author']
        publisher = request.POST['publisher']
        publication_day = request.POST['publication_day']
        docindex = Docindex(isbn=isbn,name = name,type_code = type_code,author = author,\
                        publisher = publisher,publication_day = publication_day)
        docindex.save()

        #資料情報を保存
        arrival_day = request.session['arrival_day']
        remarks = request.session['remarks']
        doclist = Doclist(docindex_id = docindex.isbn,arrival_day = arrival_day,remarks = remarks)
        doclist.save()

        params = doc().messagedone('登録完了','登録が完了しました')

    return redirect(to='doc_list')

def create_doclist(request):
    #資料情報登録画面表示
    if 'sid' not in request.session:
        return redirect(to='slogin')
    if(request.method == 'GET'):
        params = {
            'form':DoclistForm()
        }
        return render(request,'library/registdoclist.html',params)
    if(request.method == 'POST'):
        isbn = request.POST['docindex']
        docindex = Docindex(isbn=isbn)

        arrival_day = request.POST['arrival_day']
        remarks = request.POST['remarks']
        #form = DoclistForm(request.POST,instance=Doclist())
        form = Doclist(docindex_id = docindex.isbn,arrival_day = arrival_day,remarks = remarks)
        form.save()
        params = doc().messagedone('登録完了','登録が完了しました')
        return render(request,'library/done.html',params)

def confirmationdoclist(request):
    if 'sid' not in request.session:
        return redirect(to='slogin')
    if(request.method == 'GET'):
        return redirect(to='registdoclist')
    params = {
        'form':DoclistForm(request.POST)
    }
    return render(request,'library/confirmationdoclist.html',params)

def confirmation(request):
    if 'sid' not in request.session:
        return redirect(to='slogin')
    if(request.method == 'GET'):
        return redirect(to='registdoclist')

    form = DocindexModelForm(request.POST)
    isbn = request.session['isbn']
    params = {
        'form':form,
        'isbn':isbn
    }
    if form.is_valid():


        return render(request,'library/confirmation.html',params)
    else:
        return render(request,'library/registdoc.html',params)


def registdoclist(request):
    if 'sid' not in request.session:
        return redirect(to='slogin')
    if(request.method == 'GET'):
        return redirect(to='registdoclist')
    form = DoclistForm(request.POST,instance=Doclist())
    form.save()
    return render(request,'library/done.html')

def docnewcheck(request):
    if 'sid' not in request.session:
        return redirect(to='slogin')
    if(request.method == 'GET'):
        return redirect(to='registdoclist')
    if(request.method == 'POST'):
        docindexisbn = request.POST['docindex']
        arrival_day = request.POST['arrival_day']
        remarks = request.POST['remarks']
        form = DocindexModelForm()
        isbn = Docindex.objects.filter(isbn=docindexisbn).count()
        print(isbn)
        #isbnがなかった場合
        if isbn == 0:
            print('isbn番号ありません')
            if 'isbn' in request.session:
                del request.session['isbn']
            if 'isbn' not in request.session:
                request.session['isbn'] = docindexisbn
            if 'arrival_day' in request.session:
                del request.session['arrival_day']
            if 'arrival_day' not in request.session:
                request.session['arrival_day'] = arrival_day
            if 'remarks' in request.session:
                del request.session['remarks']
            if 'remarks' not in request.session:
                request.session['remarks'] = remarks

            params = {
                'isbn':request.session['isbn'],
                'form':DocindexModelForm(),
            }
            return render(request,'library/registdoc.html',params)
            #cd C:\Users\student\Desktop\チーム開発\新しく作った\moui_library_system
            #python manage.py runserver
        #isbnがあった場合
        return confirmationdoclist(request)
###################################################################################################
#資料検索
def doc_list(request,no=1):
    if 'sid' not in request.session:
        return redirect(to='slogin')
    if(request.method == 'GET'):
        list = Doclist.objects.all()

        kazu = len(list)
        page_kazu = math.ceil(kazu/5)
        plist = [i for i in range(1,page_kazu+1)]

        page = Paginator(list,5)
        records = page.get_page(no)
        num = no
        params = {
            'objectlist':records,
            'form':DocSearchForm(),
            'plist':plist,
            'page':page,
            'num':num
        }
        return render(request,'library/docmanage.html',params)

def doc_listsearch(request,no=1):
    if 'sid' not in request.session:
        return redirect(to='slogin')
    choices = ''
    find = ''
    if 'choices' in request.GET:
        choices = request.GET['choices']
    if 'find' in request.GET:
        find = request.GET['find']

    if (choices == 'isbn'):
        object_list = Doclist.objects.filter(docindex__isbn = find)
    if (choices == 'name'):
        object_list = Doclist.objects.filter(docindex__name__contains = find)
    if (choices == 'author'):
        object_list = Doclist.objects.filter(docindex__author__contains = find)

    list = object_list
    kazu = len(list)
    page_kazu = math.ceil(kazu/5)
    plist = [i for i in range(1,page_kazu+1)]
    page = Paginator(list,5)
    records = page.get_page(no)
    num = no
    params = {
        'form':DocSearchForm(request.GET),
        'objectlist':records,
        'plist':plist,
        'page':page,
        'num':no,
        'choices':choices,
        'find':find
    }
    return render(request,'library/docmanagesearch.html',params)

def edit_doc(request,num=0):
    if 'sid' not in request.session:
        return redirect(to='slogin')
    if num == 0:
        return redirect(to='doc_list')
    if(request.method == 'GET'):
        obj = Doclist.objects.filter(disposal_day=None).get(id=num)
        objindex = Docindex.objects.get(isbn=obj.docindex.isbn)
        #########################################
        params = {
            'form':Doclist.objects.filter(disposal_day=None).get(id=num),
            #'formindex':DocindexAllModelForm(instance=obj),
            'formindex':DocindexModelForm(instance=objindex),
        }
        return render(request,'library/editdoc.html',params)

    if(request.method == 'POST'):
        obj = Doclist.objects.filter(disposal_day=None).get(id=num)
        objindex = Docindex.objects.get(isbn=obj.docindex.isbn)
        docindex = DocindexModelForm(request.POST,instance=objindex)
        isbn=request.POST['isbn']
        print(isbn)
        name=request.POST['name']
        print(name)
        type_code=request.POST['type_code']
        author=request.POST['author']
        publisher=request.POST['publisher']
        publication_day=request.POST['publication_day']

        # params = doc().messagedone('編集確認画面','この内容でよろしいでしょうか')

        params = {
            'title':'編集完了画面',
            'message':'この内容でよろしいでしょうか',
            'isbn':isbn,
            'name':name,
            'type_code':type_code,
            'author':author,
            'publisher':publisher,
            'publication_day':publication_day,
        }
        return render(request,'library/editdoc_conf.html',params)

def edit_doc_save(request):
    isbn=request.POST['isbn']
    try:
        index=Docindex.objects.get(isbn=isbn)
    except:
        print('エラー')
        list = Doclist.objects.all()

        kazu = len(list)
        page_kazu = math.ceil(kazu/5)
        plist = [i for i in range(1,page_kazu+1)]

        page = Paginator(list,5)
        records = page.get_page(no)
        num = no
        params = {
            'objectlist':records,
            'form':DocSearchForm(),
            'plist':plist,
            'page':page,
            'num':num,
            'alert':'編集する資料は存在しません',
        }
        return render(request,'library/docmanage.html',params)
    print('ここまでは来てる')

    index.name=request.POST['name']
    index.type_code=request.POST['type_code']
    index.author=request.POST['author']
    index.publisher=request.POST['publisher']
    index.publication_day=request.POST['publication_day']

    index.save()

    params = doc().messagedone('編集完了画面','編集完了しました')
    return render(request,'library/done.html',params)

def delete_doc(request,num=0):
    if 'sid' not in request.session:
        return redirect(to='slogin')
    if num == 0:
        return redirect(to='doc_list')
    if(request.method == 'GET'):
        params = {
            'form':Doclist.objects.filter(disposal_day=None).get(id=num),
            #'formindex':Docindex.objects.get(id=num),
        }
        return render(request,'library/deletedoc.html',params)

    if(request.method == 'POST'):
        docindex = Doclist.objects.filter(disposal_day=None).get(id=num)
        #docindex.disposal_day=datetime.date.today()
        #docindex.save()
        docindex.delete()
        params = doc().messagedone('削除完了','削除が完了しました')
        return render(request,'library/done.html',params)

def doc_detail(request):
    if 'sid' not in request.session:
        return redirect(to='slogin')
    #初期条件

    if(request.method == 'GET'):
        return redirect(to='doc_list')
    else:
        isbn=request.POST['isbn']

        index=Docindex.objects.get(isbn=isbn)
        list=Doclist.objects.filter(docindex_id=isbn)
        print(list)

        comm=Evaluation.objects.filter(docindex_id=isbn)

        print(index)
        params={
            'index':index,
            'comment':comm,
            'list':list,
        }

        return render(request,'library/doc_detail.html',params)

##予約機能
def document_reserve_top(request):
    if 'sid' not in request.session:
        return redirect(to='slogin')
    reserves = Reservelist.objects.filter(lent=False,cancel=False).order_by('reserve_day')
    params = {
        'reserves':reserves,

    }

    return render(request,'library/document_reserve_top.html',params)

def document_reserve(request):
    if 'sid' not in request.session:
        return redirect(to='slogin')
    if request.method == 'GET':
        forms = ReserveForm()
        params = {
         'forms':forms,
        }
        return render(request,'library/document_reserve.html',params)

    if request.method == 'POST':
        forms = ReserveForm(request.POST)
        mid = request.POST['mid']
        dname = request.POST['dname']

        alert='s'
        ############################################################
        try:
            member = Member.objects.filter(quit_day=None).get(id=mid)
        except:
            alert='該当する会員がいません'
        ############################################################
        docindexes = Docindex.objects.filter(name__contains=dname)
        if docindexes.first() is not None:
            alert2 = ''
        else:
            alert2 = '該当する資料は存在しません。'

        params = {
            'alert':alert,
            'alert2':alert2,
            'forms':forms,
            'mid':mid,
            'dname':dname,
            'docindexes':docindexes,
        }

        return render(request,'library/document_reserve.html',params)

def document_reserve_info(request):
    if 'sid' not in request.session:
        return redirect(to='slogin')
    if request.method == 'GET':
        return redirect(to='document_reserve')

    #ポスト情報の取り出し
    mid = request.POST['mid']
    isbn = request.POST['isbn']

    #指定したidの会員がいるか判定
    try:
        member = Member.objects.filter(quit_day=None).get(id=mid)
    except:
        params = {
            'alert':'該当する会員がいません'
        }
        return render(request,'library/document_reserve_info.html',params)


    #指定したidの資料があるか判定
    try:

        docindex = Docindex.objects.get(isbn=isbn)

    except:
        params = {
            'alert':'該当する資料がありません'
        }
        return render(request,'library/document_reserve_info.html',params)

    #########################################################################################
    #二重予約回避

    reserve = Reservelist.objects.filter(member_id=member,docindex_id=docindex).filter(lent=False,cancel=False)
    if reserve.count() >= 1:
        params = {
            'alert':'同じ予約情報があります'
        }
        return render(request,'library/document_reserve_info.html',params)

    ########################################################################################
    params = {
        'docindex':docindex,
        'member':member,
        'reserve_day':datetime.date.today(),
    }

    return render(request,'library/document_reserve_info.html',params)

def document_reserve_save(request):
    if 'sid' not in request.session:
        return redirect(to='slogin')
    if request.method == 'GET':
        return redirect(to='document_reserve')

    #ポスト情報の取り出し
    mid = request.POST['mid']
    isbn = request.POST['isbn']
    remarks = request.POST['remarks']

    #指定したidの会員がいるか判定
    try:
        member = Member.objects.filter(quit_day=None).get(id=mid)
    except:
        params = {
            'alert':'該当する会員がいません'
        }
        return render(request,'library/document_reserve_save.html',params)


    #指定したidの資料があるか判定
    try:

        docindex = Docindex.objects.get(isbn=isbn)

    except:
        params = {
            'alert':'該当する資料がありません'
        }
        return render(request,'library/document_reserve_info.save.html',params)

    #########################################################################################
    #二重予約回避

    reserve = Reservelist.objects.filter(member_id=member,docindex_id=docindex).filter(lent=False,cancel=False)
    if reserve.count() >= 1:
        params = {
            'alert':'同じ予約情報があります'
        }
        return render(request,'library/document_reserve_save.html',params)

    ############################################################################################

    #予約の保存
    reserve = Reservelist()
    reserve.member = member
    reserve.docindex = docindex
    reserve.remarks = remarks
    reserve.save()

    params = {
        'alert':'予約が完了しました'
    }

    return render(request,'library/document_reserve_save.html',params)

def document_reserve_cancel(request,id=0):
    if 'sid' not in request.session:
        return redirect(to='slogin')
    if id == 0:
        return redirect(to='document_reserve_top')
    if request.method == "GET":
        return redirect(to='document_reserve_top')


    try:
        reserve = Reservelist.objects.filter(lent=False,cancel=False).get(id=id)
        params = {
            'reserve':reserve,
        }

        return render(request,'library/document_reserve_cancel.html',params)

    except:
        params = {
            'alert':'すでに予約がキャンセルされています'
        }

        return render(request,'library/document_reserve_cancel.html',params)

def document_reserve_cancel_save(request,id=0):
    if 'sid' not in request.session:
        return redirect(to='slogin')
    if id == 0:
        return redirect(to='document_reserve_top')
    if request.method == "GET":
        return redirect(to='document_reserve_top')

    try:
        reserve = Reservelist.objects.filter(lent=False,cancel=False).get(id=id)
        reserve.cancel=True
        reserve.save()

        params = {
            'alert':'予約をキャンセルしました'
        }
        return render(request,'library/document_reserve_cancel_save.html',params)

    except:
        params = {
            'alert':'すでに予約がキャンセルされています'
        }

        return render(request,'library/document_reserve_cancel.html',params)
