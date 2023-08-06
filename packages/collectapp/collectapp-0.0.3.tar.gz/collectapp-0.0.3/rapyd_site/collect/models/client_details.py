from django.db import models


class ClientDetail(models.Model):

    accept_header = models.CharField(max_length=2048,
                                     blank=True,
                                     null=True)
    ip_address = models.CharField(max_length=50,
                                  blank=True,
                                  null=True)
    java_enabled = models.BooleanField(blank=True,
                                       null=True)
    java_script_enabled = models.BooleanField(blank=True,
                                              null=True)
    language = models.CharField(max_length=50,
                                blank=True,
                                null=True)
    screen_color_depth = models.IntegerField(blank=True,
                                             null=True)
    screen_height = models.IntegerField(blank=True,
                                        null=True)
    screen_width = models.IntegerField(blank=True,
                                       null=True)
    time_zone_offset = models.IntegerField(blank=True,
                                           null=True)
    user_agent = models.CharField(max_length=50,
                                  blank=True,
                                  null=True)
