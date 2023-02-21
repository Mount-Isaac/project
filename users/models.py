from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	image = models.ImageField(default='media/me_hood.jpg', upload_to='media/')



	def __str__(self):
		return f'{self.user.username} profile'


	def save(self):
		super().save()

		img = Image.open(self.image.path)

		if img.height > 150 or img.width > 150:
			output_size = (150, 150)
			img.thumbnail(output_size)
			img.save(self.image.path)