ACCOUNT_SIGNUP_FIELDS = ['email', 'password1*', 'password2*']
ACCOUNT_LOGIN_METHODS = ["email"]
ACCOUNT_USER_MODEL_USERNAME_FIELD = None 

ACCOUNT_ADAPTER = 'user_management.adapters.NoSignupAccountAdapter'

ACCOUNT_FORMS = {
    'signup': 'user_management.forms.MyCustomSignupForm',
}