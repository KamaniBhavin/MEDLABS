from django.db import models
from django.contrib.auth.models import User

class File(models.Model):

    file = models.FileField(blank=False, null=False)
    remark = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "File"

class Key(models.Model):
    private_key = models.TextField()
    public_key= models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "keys"
    
    def __str__(self):
        return self.user.username


class file_storage(models.Model):
    encrypted_blob = models.FileField(upload_to='encrypted_data/', blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "encrypted_storage"