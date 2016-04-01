from django.contrib import admin
import models


# Register your models here.
admin.site.register(models.Author)
admin.site.register(models.Post)
admin.site.register(models.Comment)
admin.site.register(models.Friend)
admin.site.register(models.ForeignHost)
admin.site.register(models.Img)

