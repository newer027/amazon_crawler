from django.db import models


class Url_to_wishlist(models.Model):
    url = models.URLField(max_length = 400)
    add = models.BooleanField(default=False)

    def __str__(self):
        return u'%s' %(self.url)