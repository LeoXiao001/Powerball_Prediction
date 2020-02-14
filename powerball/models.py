from django.db import models
from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFit
from django.urls import reverse


class History(models.Model):
    draw_date = models.DateField(unique=True)
    white_ball = models.CharField(max_length=15)
    red_ball = models.CharField(max_length=2)
    recode = models.BooleanField(default=False)

    class Meta:
        ordering = ['-draw_date']


    def __str__(self):
        return '{}: {} {}'.format(self.draw_date, self.white_ball, self.red_ball)

    def save(self, *args, **kwargs):
        if self.recode:
            super().save(*args, **kwargs)
        else:
            wb = self.white_ball.split(' ')
            # update white ball numbers
            for num in wb:
                if WhiteBall.objects.filter(number=num).exists():
                    item = WhiteBall.objects.get(number=num)
                else:
                    item = WhiteBall.objects.create(number=num)
                item.frequency += 1
                item.save()

            # update red ball number
            rb = self.red_ball
            if RedBall.objects.filter(number=rb).exists():
                item = RedBall.objects.get(number=rb)
            else:
                item = RedBall.objects.create(number=rb)
            item.frequency += 1
            item.save()

            self.record = True
            super().save(*args, **kwargs)


class WhiteBall(models.Model):
    number = models.CharField(max_length=2, unique=True)
    frequency = models.IntegerField(default=0)

    class Meta:
        ordering = ['frequency', 'number']

    def __str__(self):
        return '{}: {}'.format(self.number, self.frequency)


class RedBall(models.Model):
    number = models.CharField(max_length=2, unique=True)
    frequency = models.IntegerField(default=0)

    class Meta:
        ordering = ['frequency', 'number']

    def __str__(self):
        return '{}: {}'.format(self.number, self.frequency)


class Picture(models.Model):
    image = ProcessedImageField(upload_to='images', format='JPEG')
    thumb = ImageSpecField(source='image', processors=[ResizeToFit(300, 300)],
                                format='JPEG', options={'quality': 80})
    alt = models.CharField(max_length=255, default='', blank=True)
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-create_date', '-id']

    def __str__(self):
        return self.alt
