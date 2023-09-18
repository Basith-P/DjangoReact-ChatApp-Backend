from django.db import models

from djchat import settings


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

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
