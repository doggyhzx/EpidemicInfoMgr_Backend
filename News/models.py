# models.py
from django.db import models
# 注意所有的user_id外键对应的是用户子系统的存储user信息的表，如果名称不对请根据实际表名更改


# 新闻信息表
class News(models.Model):
    news_id = models.BigAutoField(primary_key=True)
    news_title = models.CharField(max_length=64)    # 新闻标题
    news_url = models.URLField()    # 新闻链接
    news_gen_time = models.DateTimeField(auto_now_add=True)
    view_num = models.BigIntegerField(default=0)
    share_num = models.BigIntegerField(default=0)
    cmt_num = models.BigIntegerField(default=0)


# 栏目信息表
class Column(models.Model):
    cl_id = models.BigAutoField(primary_key=True)
    cl_name = models.CharField(max_length=64)
    cl_description = models.TextField(max_length=512, blank=True)
    cl_gen_time = models.DateTimeField(auto_now_add=True)
    parent_cl_id = models.ForeignKey('Column', on_delete=models.SET_NULL, null=True, default=None)  # 父栏目id，可以为空


class Comment(models.Model):    # 评论信息表
    cmt_id = models.BigAutoField(primary_key=True)
    reliable_choices=(
        (0, '内容违规'),
        (1, '收到举报'),
        (2, '正在审核'),
        (3, '正常')
    )
    is_reliable = models.IntegerField(default=3, choices=reliable_choices)  # 评论的状态
    cmt_content = models.TextField(max_length=1024)
    cmt_gen_time = models.DateTimeField(auto_now_add=True)
    like_num = models.BigIntegerField(default=0)    # 点赞数


class Files(models.Model):      # 其他格式文件信息表
    files_id = models.BigAutoField(primary_key=True)
    files_name = models.CharField(max_length=64)
    files_title = models.CharField(max_length=64)   # 这个是显示在网页上的标题而不是文件名
    files_path = models.FileField(upload_to='files/')   # 该实际文件被存储在MEDIA_ROOT下的files里，MEDIA_ROOT在setting中设置


class Images(models.Model):     # 图片信息表
    img_id = models.BigAutoField(primary_key=True)
    img_name = models.CharField(max_length=64)
    img_title = models.CharField(max_length=64)     # 这个是显示在网页上的标题而不是文件名
    img_path = models.ImageField(upload_to='images/')   # 该实际文件被存储在MEDIA_ROOT下的images里，MEDIA_ROOT在setting中设置


class PublishNews(models.Model):    # 管理员发布新闻表
    pub_news_id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey('users.UserInfo', on_delete=models.SET_NULL, null=True)   # 用户为空可以显示用户已注销或不存在，不需要删除记录
    news_id = models.ForeignKey('News', on_delete=models.CASCADE)


class ShareNews(models.Model):      # 用户分享新闻表
    share_id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey('users.UserInfo', on_delete=models.SET_NULL, null=True)   # 用户为空可以显示用户已注销或不存在，不需要删除记录
    news_id = models.ForeignKey('News', on_delete=models.CASCADE)
    share_text = models.TextField(max_length=512, blank=True)
    share_time = models.DateTimeField(auto_now_add=True)


class PublishComments(models.Model):    # 用户发表评论表
    pub_cmt_id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey('users.UserInfo', on_delete=models.SET_NULL, null=True)   # 用户为空可以显示用户已注销或不存在，不需要删除记录
    cmt_id = models.ForeignKey('Comment', on_delete=models.CASCADE)


class JudgeComment(models.Model):   # 用户点赞或举报评论表
    judge_cmt_id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey('users.UserInfo', on_delete=models.SET_NULL, null=True)   # 用户为空可以显示用户已注销或不存在，不需要删除记录
    cmt_id = models.ForeignKey('Comment', on_delete=models.CASCADE)
    report_text = models.TextField(max_length=1024, null=True, default=None)    # 举报的时候会有举报内容，点赞就算了，默认是空
    report_time = models.DateTimeField(auto_now_add=True)
    judge_choices=(
        (0, '点赞'),
        (1, '举报')
    )
    report_type = models.IntegerField(default=0, choices=judge_choices)     # 是点赞这个评论还是举报


class NewsComments(models.Model):   # 新闻评论关系
    news_cmt_id = models.BigAutoField(primary_key=True)
    news_id = models.ForeignKey('News', on_delete=models.CASCADE)
    cmt_id = models.ForeignKey('Comment', on_delete=models.CASCADE)


class NewsFiles(models.Model):  # 新闻文件关系
    news_files_id = models.BigAutoField(primary_key=True)
    news_id = models.ForeignKey('News', on_delete=models.CASCADE)
    files_id = models.ForeignKey('Files', on_delete=models.CASCADE)


class NewsImages(models.Model):     # 新闻图片关系
    news_files_id = models.BigAutoField(primary_key=True)
    news_id = models.ForeignKey('News', on_delete=models.CASCADE)
    img_id = models.ForeignKey('Images', on_delete=models.CASCADE)


class NewsColumn(models.Model):     # 新闻栏目关系
    news_cl_id = models.BigAutoField(primary_key=True)
    news_id = models.ForeignKey('News', on_delete=models.CASCADE)
    cl_id = models.ForeignKey('Column', on_delete=models.CASCADE)