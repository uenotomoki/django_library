from django.urls import path
from . import views

urlpatterns = [

    ########
    #職員機能
    ########
    path('slogin',views.slogin,name='slogin'),
    path('logout',views.logout,name='logout'),
    path('smypage',views.smypage,name='smypage'),
    # path('member_manage',views.member_manage,name='member_manage'),
    #会員管理関連
    path('member_manage',views.member_manage,name='member_manage'),
    path('member_create',views.member_create,name='member_create'),
    path('member_info',views.member_info,name='member_info'),
    path('member_info/<int:id>',views.member_info,name='member_info'),
    path('member_update/<int:id>',views.member_update,name='member_update'),
    path('member_update',views.member_update,name='member_update'),
    path('member_delete/<int:id>',views.member_delete,name='member_delete'),
    path('member_delete',views.member_delete,name='member_delete'),
    path('newmember_save',views.newmember_save,name='newmember_save'),
    path('member_update_save/<int:id>',views.member_update_save,name='member_update_save'),
    path('member_update_save',views.member_update_save,name='member_update_save'),
    #資料貸出返却
    path('document_lend',views.document_lend,name='document_lend'),
    path('document_lend_info',views.document_lend_info,name='document_lend_info'),
    path('document_lend_save',views.document_lend_save,name='document_lend_save'),
    path('document_return',views.document_return,name='document_return'),
    path('document_return_info',views.document_return_info,name='document_return_info'),
    path('document_return_save',views.document_return_save,name='document_return_save'),
    #資料管理関連
    path('registdoclist',views.create_doclist,name='registdoclist'),
    path('registdoc',views.create_doc,name='registdoc'),
    path('confirmation',views.confirmation,name='confirmation'),
    path('confirmationlist',views.confirmationdoclist,name='confirmationlist'),
    path('docnewcheck',views.docnewcheck,name='docnewcheck'),
    path('doc_list/<int:no>',views.doc_list,name='doc_list'),
    path('doc_list',views.doc_list,name='doc_list'),
    path('doc_listsearch/<int:no>',views.doc_listsearch,name='doc_listsearch'),
    path('doc_listsearch',views.doc_listsearch,name='doc_listsearch'),
    path('edit_doc',views.edit_doc,name='edit_doc'),
    path('edit_doc_save',views.edit_doc_save,name='edit_doc_save'),
    path('edit_doc/<int:num>',views.edit_doc,name='edit_doc'),
    path('delete_doc',views.delete_doc,name='delete_doc'),
    path('delete_doc/<int:num>',views.delete_doc,name='delete_doc'),
    path('doc_detail',views.doc_detail,name='doc_detail'),

    path('lend_list',views.lend_list,name='lend_list'),
    path('lend_list/<int:no>',views.lend_list,name='lend_list'),
    #資料予約
    path('document_reserve_top',views.document_reserve_top,name='document_reserve_top'),
    path('document_reserve',views.document_reserve,name='document_reserve'),
    path('document_reserve_info',views.document_reserve_info,name='document_reserve_info'),
    path('document_reserve_save',views.document_reserve_save,name='document_reserve_save'),
    path('document_reserve_cancel/<int:id>',views.document_reserve_cancel,name='document_reserve_cancel'),
    path('document_reserve_cancel',views.document_reserve_cancel,name='document_reserve_cancel'),
    path('document_reserve_cancel_save/<int:id>',views.document_reserve_cancel_save,name='document_reserve_cancel_save'),
    ########
    #会員機能
    ########
    #ログイン
    path('mlogin',views.mlogin,name='mlogin'),
    path('mmypage',views.mmypage,name='mmypage'),

    ##検索
    path('searchhome/<int:no>',views.searchhome,name='searchhome'),
    path('mdoc_listsearch/<int:no>',views.mdoc_listsearch,name='mdoc_listsearch'),
    path('mdoc_detail',views.mdoc_detail,name='mdoc_detail'),
    ##会員情報
    path('minfo',views.minfo,name='minfo'),
    path('mupdate',views.mupdate,name='mupdate'),
    path('editpass',views.editpass,name='editpass'),
    ##貸出返却
    path('mlend',views.mlend,name='mlend'),
    path('mlendsave',views.mlendsave,name='mlendsave'),
    path('mreturn',views.mreturn,name='mreturn'),
    path('mreturnsave',views.mreturnsave,name='mreturnsave'),
    #履歴コメント
    path('mresult1/<int:no>',views.mresult1,name='mresult1'),
    path('mresult2/<int:no>',views.mresult2,name='mresult2'),
    path('comment',views.comment,name='comment'),
    path('comment_conf',views.comment_conf,name='comment_conf'),
    path('comment_save',views.comment_save,name='comment_save'),

]
