from django.db import models
from django.dispatch import receiver
from django.shortcuts import get_object_or_404

from djchat import settings


def category_icon_path(instance, filename):
    return f"category/{instance.name}/icon/{filename}"


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    icon = models.FileField(
        upload_to=category_icon_path, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.id:
            category = get_object_or_404(Category, id=self.id)
            if category.icon != self.icon:
                category.icon.delete(save=False)
        super(Category, self).save(*args, **kwargs)

    @receiver(models.signals.post_delete, sender='server.Category')
    def delete_category_icon(sender, instance, **kwargs):
        instance.icon.delete(save=False)

    def __str__(self) -> str:
        return self.name


class Server(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='server_owner')
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="server_category")
    description = models.CharField(max_length=250, blank=True, null=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL)

    def __str__(self) -> str:
        return self.name


class Channel(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='channel_owner')
    topic = models.CharField(max_length=50)
    server = models.ForeignKey(
        Server, on_delete=models.CASCADE, related_name="channels")

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super(Channel, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name
