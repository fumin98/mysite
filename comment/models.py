from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User



class Comment(models.Model):
    #通过外键将content_type和ContentType相连接
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type','object_id')

    text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)
    #谁评论
    user = models.ForeignKey(User ,related_name="comments" , on_delete=models.CASCADE)
    root = models.ForeignKey('self', related_name="root_comment", null=True,on_delete=models.CASCADE)
    parent = models.ForeignKey('self',related_name="parent_comment",null=True,on_delete=models.CASCADE)
    #回复谁
    reply_to = models.ForeignKey(User,related_name = "replies" , null=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.text
    #时间倒叙
    class Meta:
        ordering = ['comment_time']


