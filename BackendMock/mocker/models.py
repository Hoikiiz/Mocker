from django.db import models


class MockItem(models.Model):
    objects = models.Manager()
    created = models.DateTimeField(auto_now_add=True)
    activeType = models.BooleanField(default=True)
    redirect = models.CharField(max_length=255)
    finalTarget = models.CharField(max_length=255)
    desc = models.CharField(max_length=255, null=True, blank=True)
    url = models.CharField(max_length=255)

    class Meta:
        ordering = ('created', )

    def __str__(self):
        return self.url


class MockSlot(models.Model):
    objects = models.Manager()
    created = models.DateTimeField(auto_now_add=True)
    value = models.TextField(default='''{\n\t"data":\n\t{\n\n\t},\n\t"code": 0\n}''')
    desc = models.CharField(max_length=255, default='')
    compMethod = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    mockItem = models.ForeignKey("MockItem", default=1, on_delete=models.CASCADE, related_name='slots')

    class Meta:
        ordering = ('created', )

    def __str__(self):
        return self.desc


class MockCondition(models.Model):
    objects = models.Manager()
    created = models.DateTimeField(auto_now_add=True)
    key = models.CharField(max_length=32, default='key')
    value = models.CharField(max_length=255, default='value')
    compFunc = models.CharField(max_length=32, default='==')
    mockSlot = models.ForeignKey("MockSlot", related_name='conditions', null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ('created', )

    def __str__(self):
        return self.key + " " + self.compFunc + " " + self.value


class MockLog(models.Model):
    objects = models.Manager()
    url = models.CharField(max_length=255)
    active_type = models.CharField(max_length=11)
    method = models.CharField(max_length=10, default='')
    request = models.TextField()
    response = models.TextField()
    time_request = models.CharField(max_length=255)
    time_response = models.CharField(max_length=255)

    def __str__(self):
        return self.active_type + "--" + self.url
