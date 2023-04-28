from django.test import TestCase

from django.contrib.auth.models import User
from django.contrib import messages

from .forms import UserRegisterForm, UserUpdateForm

from .views import profile

# Create your tests here.



""" class TestModels(TestCase):
    
    # Tests that a logged in user can successfully update their account information and is redirected to their profile page. 
    def test_profile_logged_in_success(self, client, user):
        # Setup
        client.force_login(user)
        data = {
            'username': 'new_username',
            'email': 'new_email@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'new_password',
            'password2': 'new_password'
        }

        # Exercise
        response = client.post('/profile/', data=data)

        # Verify
        assert response.status_code == 302
        assert response.url == '/profile/'
        assert messages.get_messages(response.wsgi_request)[0].message == "Your account has been updated"
        user.refresh_from_db()
        assert user.username == 'new_username'
        assert user.email == 'new_email@example.com'
        assert user.first_name == 'New'
        assert user.last_name == 'User'

        #TypeError: TestModels.test_profile_logged_in_success() missing 2 required positional arguments: 'client' and 'user'
        # where is the mistake show me in text




    # Tests that a user who is not logged in is redirected to the login page when trying to access their profile page. 
    def test_profile_not_logged_in(self, client):
        # Exercise
        response = client.get('/profile/')

        # Verify
        assert response.status_code == 302
        assert response.url == '/login/?next=/profile/'

    # Tests that an error message is displayed to the user when they enter invalid information in the update form. 
    def test_profile_update_form_invalid(self, client, user):
        # Setup
        client.force_login(user)
        data = {
            'username': '',
            'email': 'invalid_email',
            'first_name': '',
            'last_name': '',
            'password1': '',
            'password2': ''
        }

        # Exercise
        response = client.post('/profile/', data=data)

        # Verify
        assert response.status_code == 200
        assert 'This field is required.' in response.content.decode()
        assert 'Enter a valid email address.' in response.content.decode()
        user.refresh_from_db()
        assert user.username != ''
        assert user.email != 'invalid_email'

    # Tests that an error message is displayed to the user when they enter mismatched passwords in the update form.  
    def test_profile_update_form_mismatched_passwords(self, mocker):
        # Create a mock request object
        request = mocker.Mock()
        request.method = 'POST'
        request.user = User.objects.create_user(username='testuser', email='testuser@test.com', password='testpassword')

        # Create a mock form with mismatched passwords
        form_data = {'username': 'testuser', 'email': 'testuser@test.com', 'first_name': 'Test', 'last_name': 'User', 'password1': 'testpassword1', 'password2': 'testpassword2'}
        form = UserUpdateForm(data=form_data)

        # Call the profile view function with the mock request and form
        response = profile(request, form)

        # Assert that the form is not valid and an error message is displayed
        assert not form.is_valid()
        assert response.context_data['update_form'].errors['password2'] == ['The two password fields didn’t match.']

    # Tests that an error message is displayed to the user when they try to update their username.  
    def test_profile_update_username(self, mocker):
        # Create a mock request object
        request = mocker.Mock()
        request.method = 'POST'
        request.user = User.objects.create_user(username='testuser', email='testuser@test.com', password='testpassword')

        # Create a mock form with updated username
        form_data = {'username': 'newusername', 'email': 'testuser@test.com', 'first_name': 'Test', 'last_name': 'User', 'password1': 'testpassword', 'password2': 'testpassword'}
        form = UserUpdateForm(data=form_data)

        # Call the profile view function with the mock request and form
        response = profile(request, form)

        # Assert that the form is not valid and an error message is displayed
        assert not form.is_valid()
        assert response.context_data['update_form'].errors['username'] == ['This field is not allowed to be updated.']

    # Tests that an error message is displayed to the user when they try to update their email to an already existing email.  
    def test_profile_update_existing_email(self, mocker):
        # Create a mock request object
        request = mocker.Mock()
        request.method = 'POST'
        request.user = User.objects.create_user(username='testuser', email='testuser@test.com', password='testpassword')
        User.objects.create_user(username='testuser2', email='testuser2@test.com', password='testpassword')

        # Create a mock form with updated email
        form_data = {'username': 'testuser', 'email': 'testuser2@test.com', 'first_name': 'Test', 'last_name': 'User', 'password1': 'testpassword', 'password2': 'testpassword'}
        form = UserUpdateForm(data=form_data)

        # Call the profile view function with the mock request and form
        response = profile(request, form)

        # Assert that the form is not valid and an error message is displayed
        assert not form.is_valid()
        assert response.context_data['update_form'].errors['email'] == ['Email already exists.'] """

class TestRegister:

    # Tests that a user is redirected to the login page and a success message is displayed after submitting a valid registration form. 
    def test_register_valid_form_submission(self, mocker, client):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword'
        }
        form = UserRegisterForm(data=form_data)
        mocker.patch('webapp.views.UserRegisterForm', return_value=form)
        mocker.patch('webapp.views.messages.success')
        response = client.post('/register/', data=form_data)
        assert response.status_code == 302
        assert response.url == '/login/'
        messages.success.assert_called_once_with(
            response.wsgi_request, "Your account has been created!"
        )

    # Tests that an error message is displayed when a user submits an invalid registration form. 
    def test_register_invalid_form_submission(self, mocker, client):
        form_data = {
            'username': '',
            'email': '',
            'password1': '',
            'password2': ''
        }
        form = UserRegisterForm(data=form_data)
        mocker.patch('webapp.views.UserRegisterForm', return_value=form)
        response = client.post('/register/', data=form_data)
        assert response.status_code == 200
        assert 'This field is required.' in response.content.decode()

    # Tests that an error message is displayed when a user submits a registration form with an existing username or email. 
    def test_register_existing_username_email(self, mocker, client):
        User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword'
        }
        form = UserRegisterForm(data=form_data)
        mocker.patch('webapp.views.UserRegisterForm', return_value=form)
        response = client.post('/register/', data=form_data)
        assert response.status_code == 200
        assert 'A user with that username already exists.' in response.content.decode()
        assert 'A user with that email already exists.' in response.content.decode()

    # Tests that an error message is displayed when a user submits a registration form with a weak password.  
    def test_register_weak_password(self, mocker):
        mocker.patch('django.contrib.messages.success')
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'weakpassword',
            'password2': 'weakpassword'
        }
        form = UserRegisterForm(data=data)
        assert not form.is_valid()
        messages.success.assert_not_called()

    # Tests that an error message is displayed when a user submits a registration form with mismatched passwords.  
    def test_register_mismatched_passwords(self, mocker):
        mocker.patch('django.contrib.messages.success')
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'strongpassword',
            'password2': 'differentpassword'
        }
        form = UserRegisterForm(data=data)
        assert not form.is_valid()
        messages.success.assert_not_called()

    # Tests that the form fields are properly displayed with correct attributes and help text for form fields is removed.  
    def test_register_form_display(self, client):
        response = client.get('/register/')
        assert response.status_code == 200
        assert b'name="username"' in response.content
        assert b'name="email"' in response.content
        assert b'name="password1"' in response.content
        assert b'name="password2"' in response.content
        assert b'placeholder="enter your username"' in response.content
        assert b'placeholder="enter your password"' in response.content
        assert b'placeholder="repeat your password"' in response.content
        assert b'placeholder="enter your email"' in response.content
        assert b'help_text' not in response.content