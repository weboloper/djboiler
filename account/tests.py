from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.utils import timezone
from .models import Profile

User = get_user_model()

class UserManagerTests(TestCase):
    
    def test_create_user(self):
        """Test that a user is created successfully with valid credentials."""
        email = 'testuser@example.com'
        username = 'testuser'
        password = 'password123'
        
        user = User.objects.create_user(email=email, username=username, password=password)
        
        self.assertEqual(user.email, email)
        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertIsNone(user.deleted_at)
    
    def test_create_superuser(self):
        """Test that a superuser is created successfully with the correct fields."""
        email = 'admin@example.com'
        username = 'adminuser'
        password = 'adminpassword123'
        
        superuser = User.objects.create_superuser(email=email, username=username, password=password)
        
        self.assertEqual(superuser.email, email)
        self.assertEqual(superuser.username, username)
        self.assertTrue(superuser.check_password(password))
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
    
    def test_create_user_without_email(self):
        """Test that a ValueError is raised if no email is provided."""
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', username='testuser', password='password123')
    
    def test_create_user_without_username(self):
        """Test that a ValueError is raised if no username is provided."""
        with self.assertRaises(ValueError):
            User.objects.create_user(email='testuser@example.com', username='', password='password123')
    
    def test_invalid_username(self):
        """Test that invalid username raises a ValidationError."""
        invalid_username = 'invalid@username'
        
        with self.assertRaises(ValidationError):
            user = User(email='testuser@example.com', username=invalid_username)
            user.full_clean()  # This triggers validation
    
    def test_create_user_with_deleted_at(self):
        """Test that user can be deleted (soft delete)."""
        user = User.objects.create_user(email='testuser@example.com', username='testuser', password='password123')
        user.deleted_at = timezone.now()
        user.save()

        self.assertIsNotNone(user.deleted_at)


class ProfileModelTests(TestCase):

    def setUp(self):
        """Create a user instance to associate a profile with."""
        self.user = User.objects.create_user(email='testuser@example.com', username='testuser', password='password123')
    
    def test_create_profile(self):
        """Test that a profile is created when a user is created."""
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertEqual(self.user.profile.user, self.user)
    
    def test_profile_str_method(self):
        """Test the string representation of the profile."""
        profile = self.user.profile
        expected_str = f'{self.user.email} Profile'
        self.assertEqual(str(profile), expected_str)
    
    def test_profile_avatar_validation(self):
        """Test that an invalid avatar extension raises a validation error."""
        from django.core.files.uploadedfile import SimpleUploadedFile

        invalid_avatar = SimpleUploadedFile('avatar.txt', b'file_content', content_type='text/plain')
        
        profile = self.user.profile
        profile.avatar = invalid_avatar
        
        with self.assertRaises(ValidationError):
            profile.full_clean()  # Trigger validation to check the avatar file type


    def test_profile_social_media_fields(self):
        """Test social media fields on the profile."""
        profile = self.user.profile
        profile.twitter = 'https://twitter.com/testuser'
        profile.instagram = 'https://instagram.com/testuser'
        profile.facebook = 'https://facebook.com/testuser'
        profile.pinterest = 'https://pinterest.com/testuser'
        profile.save()

        self.assertEqual(profile.twitter, 'https://twitter.com/testuser')
        self.assertEqual(profile.instagram, 'https://instagram.com/testuser')
        self.assertEqual(profile.facebook, 'https://facebook.com/testuser')
        self.assertEqual(profile.pinterest, 'https://pinterest.com/testuser')
    

class SignalTests(TestCase):

    def setUp(self):
        """Create a user instance to associate a profile with."""
        # Ensure you create a user that all test methods can use
        self.user = User.objects.create_user(email='testuser@example.com', username='testuser', password='password123')
        
    def test_create_profile_on_user_creation(self):
        """Test that a profile is created when a new user is created."""
        user = User.objects.create_user(email='newuser@example.com', username='newuser', password='password123')
        
        # Check that a profile is automatically created for the user
        profile = Profile.objects.get(user=user)
        self.assertEqual(profile.user, user)
    
    def test_save_profile_on_user_save(self):
        """Test that the profile is saved when the user is saved."""
        user = self.user  # Using user from the setup
        profile = user.profile
        profile.bio = 'This is a bio.'
        profile.save()
        
        # Check that the profile is saved correctly
        updated_profile = Profile.objects.get(user=user)
        self.assertEqual(updated_profile.bio, 'This is a bio.')
