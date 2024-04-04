from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from config import settings
from order.models import ContactUs

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(max_length=255, required=True)  # Change to EmailField for email validation

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use. Please use a different email address.")
        return email

    def send_welcome_email(self):
        subject = "Welcome to Ecommerce Company LMT!"
        username = self.cleaned_data['first_name']
        message = f"""
        <p>Dear {username},</p>
        <p>Welcome to Ecommerce company LMT! We're thrilled to have you join our community of savvy shoppers.</p>
        <p>At Ecommerce company LMT, we strive to provide an exceptional shopping experience, offering a wide range of
            products
            to suit your needs and preferences. Whether you're searching for the latest fashion trends, high-quality
            electronics, or
            everyday essentials, we've got you covered.</p>
        <p>As a new member, you now have access to exclusive benefits, including:</p>
        <ul>
            <li>Special discounts and promotions tailored just for you.</li>
            <li>Personalized recommendations based on your browsing and purchase history.</li>
            <li>Fast and secure checkout process for hassle-free shopping.</li>
            <li>Easy order tracking and updates on your deliveries.</li>
        </ul>
        <p>We're here to make your online shopping experience seamless and enjoyable. If you have any questions or need
            assistance,</p>
        <p>our customer support team is available to help you every step of the way.</p>
        <p>Thank you for choosing Ecommerce company LMT. We look forward to serving you and exceeding your expectations.</p>
        <p>Happy shopping!</p>
        <p>Best regards,</p>
        <p>[Ecommerce company Team]</p>
        """
        from_email = "Ecommerce company <{}>".format(settings.DEFAULT_FROM_EMAIL)  # Use the default from email
        recipient_list = [self.cleaned_data['email']]  # Use the user's email for recipient list

        send_mail(subject, message, from_email, recipient_list)

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            self.send_welcome_email()  # Send welcome email upon user creation
        return user



class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')



class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['full_name', 'email', 'phone', 'subject', 'message']