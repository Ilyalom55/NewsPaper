from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.Model)
    rating_author = models.SmallIntegerField(default=0)

    def update_rating(self):
        post_rating = self.post_set.all().aggregate(postRating=Sum('rating'))
        post_r = 0
        post_r += post_rating.get('postRating')

        comment_rating = self.user.comment_set.all().aggregate(commentRating=Sum('rating'))
        comment_r = 0
        comment_r += comment_rating.get('commentRating')

        self.rating_author = post_r * 3 + comment_r
        self.save()

    def __str__(self):
        return f"{self.user}"


class Category(models.Model):
    category_name = models.CharField(max_length=64, unique=True)
    subscribers = models.ManyToManyField(User, blank=True, null=True, related_name='postCategory')

    def __str__(self):
        return self.category_name

news = 'NE'
article = 'AR'

Category_Choices = [(news, 'Новость'),
                    (article, 'Статья')]


class Post(models.Model):
    objects = None
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    categoryChoice = models.CharField(max_length=30, choices=Category_Choices, default=article)
    post_time_in = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    post_title = models.CharField(max_length=255)
    post_text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating +=1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.post_text[0:125] + '...'

    def __str__(self):
        return str(self.post_title + ' | ' + self.preview())

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class PostCategory(models.Model):
    post_through = models.ForeignKey(Post, on_delete=models.CASCADE)
    category_through = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post_comment = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_comment = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    comment_data = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()





