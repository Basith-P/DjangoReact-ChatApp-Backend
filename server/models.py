from django.db import models
from django.dispatch import receiver
from django.shortcuts import get_object_or_404

from djchat import settings

from .validators import validate_icon_size, validate_image_extension


def category_icon_path(instance, filename):
    return f"category/{instance.name}/icon/{filename}"


def server_icon_path(instance, filename):
    return f"server/{instance.name}/icon/{filename}"


def server_banner_path(instance, filename):
    return f"server/{instance.name}/banner/{filename}"


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
    banner = models.ImageField(
        upload_to=server_banner_path,
        null=True,
        blank=True,
        validators=[validate_image_extension]
    )
    icon = models.ImageField(
        upload_to=server_icon_path,
        null=True,
        blank=True,
        validators=[validate_icon_size, validate_image_extension]
    )

    def save(self, *args, **kwargs):
        if self.id:
            channel = get_object_or_404(Channel, id=self.id)
            if channel.icon != self.icon:
                channel.icon.delete(save=False)
            if channel.banner != self.banner:
                channel.banner.delete(save=False)
        super(Channel, self).save(*args, **kwargs)

    @receiver(models.signals.post_delete, sender='server.Channel')
    def delete_channel_files(sender, instance, **kwargs):
        instance.icon.delete(save=False)
        instance.banner.delete(save=False)

    def __str__(self) -> str:
        return self.name
