from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
	def create_user(self, phone_number, email, sur_name, for_name, password):
		if not phone_number:
			raise ValueError("user must have phone number")

		if not email:
			raise ValueError("user must have email")

		if not sur_name:
			raise ValueError("user must have full name")

		if not for_name:
			raise ValueError("user must have full name")

		user = self.model(phone_number=phone_number, email=self.normalize_email(email),
                                                     sur_name=sur_name, for_name=for_name)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, phone_number, email, sur_name, for_name, password):
		user = self.create_user(phone_number, email, sur_name, for_name, password)
		user.is_admin = True
		user.is_superuser = True
		user.save(using=self._db)
		return user