from django.db import models

from users.models import CustomUser


class Blog(models.Model):
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    image = models.ImageField(upload_to='blog/', null=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    tag = models.ManyToManyField('Tag', blank=True)

    class Meta:
        db_table = 'blog'

    def __str__(self):
        return self.title + ' | ' + str(self.author)

    def summary(self):
        return self.content[:100]


class Comment(models.Model):
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'comment'

    def __str__(self):
        return self.content + ' | ' + str(self.author)


class Tag(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        db_table = 'tag'

    def __str__(self):
        return self.name


class Like(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True)
    likedUser = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    class Meta:
        db_table = 'like'

    def __str__(self):
        return self.blog.title + ' | ' + str(self.likedUser)
