from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    authorRating = models.IntegerField(default=0)

    def update_rating(self):
        postRat = self.post_set.all().aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += postRat.get('postRating')

        commentRat = self.authorUser.comment_set.all().aggregate(commentRauthorUserating=Sum('rating'))
        cRat = 0
        cRat += commentRat.get('commentRating')

        allcommentsRat = Comment.objects.filter(commentPost_id__author_id=self.id).aggregate(acRating=Sum('rating'))
        acRat = 0
        acRat += allcommentsRat.get('acRating')

        self.authorRating = pRat * 3 + cRat + acRat
        self.save()

        return self.authorRating

    def __str__(self):
        return self.authorUser.username


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    subscriber = models.ManyToManyField(User, through='CategorySubscriber')

    def __str__(self):
        return self.name


class Post(models.Model):
    category = models.ManyToManyField(Category, through='PostCategory')
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=2, choices=[(
        'AR', 'Article'), ('NW', 'News')], default='NW')
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=128)
    content = models.TextField(blank=True)
    rating = models.IntegerField(default=0)
    category_id = models.ForeignKey(Category, null=True, on_delete=models.CASCADE, related_name='category_id')

    def preview(self):
        return self.content[:100] + '...'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def get_absolute_url(self):  # добавим абсолютный путь, чтобы после создания нас перебрасывало на страницу с товаром
        return f'/news/{self.id}'

    def __str__(self):
        return self.title


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


class CategorySubscriber(models.Model):
    classTrough = models.ForeignKey(Category, on_delete=models.CASCADE)
    userTrough = models.ForeignKey(User, on_delete=models.CASCADE)
