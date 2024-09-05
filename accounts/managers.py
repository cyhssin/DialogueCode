from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, phone_number, email, sur_name, fore_name, password):
        if not phone_number:
            raise ValueError("User must have phone number")
        
        if not email:
            raise ValueError("User must have email")
        
        if not sur_name:
            raise ValueError("User must have surname")
        
        if not fore_name:
            raise ValueError("User must have forename")
        
        user = self.model(phone_number=phone_number, email=self.normalize_email(email),
                           sur_name=sur_name, fore_name=fore_name)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, phone_number, email, sur_name, fore_name, password):
        user = self.create_user(phone_number, email, sur_name, fore_name,    password)
        user.is_admin = True
        user.save(using=self._db)
        return user