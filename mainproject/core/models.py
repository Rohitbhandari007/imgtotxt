from django.db import models

class ImageHistory(models.Model):
    name=models.CharField(max_length=10000)
    image=models.ImageField(max_length=99999999, upload_to="media")
    date_created = models.DateTimeField(auto_now=True)
    is_converted = models.BooleanField(default=False)
    converted_text=models.TextField(null=True)
    # boxed_image=models.ImageField(max_length=9999,upload_to="media/boxed_images",null=True)

    def __str__(self):
        return self.name
    

