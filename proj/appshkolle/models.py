from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, time, timezone
from django.db.models import Count



class Author(models.Model):
    nameavtor = models.CharField(max_length = 255, verbose_name='препод')
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Author преподаватель"
        verbose_name_plural = "Author преподаватели"


class Product(models.Model):
    nameprod = models.CharField(max_length = 255, verbose_name='название_продукта')
    datestart = models.DateTimeField(blank=True, null=True, verbose_name='дата_начала')
    price = models.FloatField(default=0.0, verbose_name='стоимость')
    kolvomin = models.IntegerField(default=1, verbose_name='наим_колво_в_группе')
    kolvomax = models.IntegerField(default=1, verbose_name='наиб_колво_в_группе')
    user = models.ManyToManyField(User, through='UserProduct')
    is_done = models.BooleanField(default=False, blank=True, verbose_name='продукт заполнен')

    class Meta:
        verbose_name = "Product курс"
        verbose_name_plural = "Product курсы"

    #распределение по группам
    def get_raspredelenie_groups(self, min, max, itogo):
        grupi = {}
        x = (itogo // max) + 1
        z = max * x - itogo

        if min == max and max >= itogo:
            grupi = {1: itogo}
        else:
            for i in range(1, x + 1):
                grupi[i] = max
            while z > 0:
                for key, value in grupi.items():
                    if z > 0:
                        grupi[key] = value - 1
                        z -= 1
        return grupi

    def raspred(self,groups,product):
        users = User.objects.filter(product__id=product.id)
        number_of_user = 0
        for number_of_group, kolvo in groups.items():
            group = Group.objects.create(namegroup=f'gr{product.id}-{number_of_group}', product=product)
            for i in range(kolvo):
                UserGroup.objects.create(user=users[number_of_user + i], group=group)
            number_of_user +=i+1

    def do_groups(self):
        products = Product.objects.filter(is_done=False)
        for product in products:
            p1 = Product.objects.filter(id=product.id, is_done=False).first()
            kolvo_users = Product.objects.filter(id=p1.id).annotate(total=Count('user')).values('total')[0]['total']
            groups = p1.get_raspredelenie_groups(p1.kolvomin, p1.kolvomax, kolvo_users)
            p1.raspred(groups, p1)
            p1.is_done=True
            p1.save()


class UserProduct(models.Model):
    is_paid = models.BooleanField(default=False, verbose_name='оплачено')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "UserProduct набор_на_курс"
        verbose_name_plural = "UserProduct наборы_на_курсы"


class Group(models.Model):
    namegroup = models.CharField(max_length = 255, verbose_name='название_группы')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ManyToManyField(User, through='UserGroup')

    class Meta:
        verbose_name = "Group группа"
        verbose_name_plural = "Group группы"
    #Количество учеников занимающихся на продукте.
    def get_nxenesit(self):
        group1 = Group.objects.values('product').annotate(total=Count('user'))


class UserGroup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "UserGroup набор_в_группу"
        verbose_name_plural = "UserGroup наборы_в_группы"


class Videos(models.Model):
    videolink = models.FileField(upload_to='video/', unique=True, verbose_name='ссылка_на_видео')

    class Meta:
        verbose_name = "Videos видео"
        verbose_name_plural = "Videos видевы"


class Lesson(models.Model):
    nameless = models.CharField(max_length = 255, verbose_name='название_урока')
    videos = models.ManyToManyField(Videos, through='VideosLesson')

    class Meta:
        verbose_name = "Lesson урок"
        verbose_name_plural = "Lesson уроки"


class VideosLesson(models.Model):
    videos = models.ForeignKey(Videos, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)