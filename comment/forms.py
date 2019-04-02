from django import forms
from django.contrib.contenttypes.models import ContentType
#评论对象不存在的错误类型
from django.db.models import ObjectDoesNotExist
from ckeditor.widgets import CKEditorWidget
from.models import Comment 

class CommentForm(forms.Form):
    content_type = forms.CharField(widget=forms.HiddenInput)
#整形，所有model中的主键值,hiddenInput隐藏字段
    object_id = forms.IntegerField(widget=forms.HiddenInput)
#forms.Textarea为可换行输入
    text = forms.CharField(widget=CKEditorWidget(config_name='comment_ckeditor'),
                            error_messages={'required':'写点话'})

    reply_comment_id = forms.IntegerField(widget=forms.HiddenInput(attrs={'id':'reply_comment_id'}))

#  *args表示无名参数,**kwargs表示关键字参数
    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(CommentForm, self).__init__(*args, **kwargs)

    def clean(self):
        #判断用户是否登陆
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else: 
            raise forms.ValidationError('用户尚未登陆')
        
        #评论对象验证
        content_type = self.cleaned_data['content_type']
        object_id  =  self.cleaned_data['object_id']
        try:
            #依靠contenttype这个方法获取到了blogAPP中的model然后使用model_class这个函数提取出了Blog这个模型
            model_class = ContentType.objects.get(model=content_type).model_class()
            #此时的model_class就相当于Blog，所以使用objects.get()得到主键值
            model_obj = model_class.objects.get(pk=object_id)
            self.cleaned_data['content_object'] = model_obj
        except ObjectDoesNotExist:
            raise forms.ValidationError('评论对象不存在')

        return self.cleaned_data

    def clean_reply_comment_id(self):
        reply_comment_id = self.cleaned_data['reply_comment_id']
        if reply_comment_id < 0:
            raise form.ValidationError('回复出错')
        elif reply_comment_id == 0:
            self.cleaned_data['parent'] = None
        elif Comment.objects.filter(pk=reply_comment_id).exists():
            self.cleaned_data['parent'] = Comment.objects.get(pk=reply_comment_id)
        else:
            raise forms.ValidationError('回复错误')
        return reply_comment_id