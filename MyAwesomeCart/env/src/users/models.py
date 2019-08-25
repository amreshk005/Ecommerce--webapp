from django.db import models
from django.contrib.auth.models import User



class AccountRegister(CreateView):
    model = User
    form_class = forms.RegisterForm
    template_name = 'account/signup.html'
    success_url = reverse_lazy('account:verify_phone')

    def form_valid(self, form):
        user = form.save(self.request)

        if user.email:
            send_email_confirmation(self.request, user)

        if user.phone:
            device = VerificationDevice.objects.create(
                user=user, unverified_phone=user.phone)
            device.generate_challenge()

            message = _("Verification Token sent to {phone}")
            message = message.format(phone=user.phone)
            messages.add_message(self.request, messages.INFO, message)

        self.request.session['user_id'] = user.id

        message = _("We have created your account. You should have"
                    " received an email or a text to verify your account.")
        messages.add_message(self.request, messages.SUCCESS, message)

        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class ConfirmPhone(FormView):
    template_name = 'accounts/account_verification.html'
    form_class = forms.PhoneVerificationForm
    success_url = reverse_lazy('account:login')

    def get_user(self):
        user_id = self.request.session['user_id']
        user = User.objects.get(id=user_id)
        return user

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super().get_form_kwargs(*args, **kwargs)
        form_kwargs["user"] = self.get_user()
        return form_kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_user()
        if user.emailaddress_set.filter(verified=False).exists():
            context['email'] = user.email
        if VerificationDevice.objects.filter(
                user=user, verified=False).exists():
            context['phone'] = user.phone
        return context

    def form_valid(self, form):
        user = self.get_user()
        user.refresh_from_db()
        message = _("Successfully verified {phone}")
        message = message.format(phone=user.phone)
        messages.add_message(self.request, messages.SUCCESS, message)
        return super().form_valid(form)
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE) 
	image = models.ImageField(default='default.jpg', upload_to='profile_pics')


	def __str__(self):
		return f'{self.user.username} Profile'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()