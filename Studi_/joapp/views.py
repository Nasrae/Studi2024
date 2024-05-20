import random
import string
import stripe
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from Studi.server import YOUR_DOMAIN
from .form import CustomUserCreationForm
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.utils.crypto import get_random_string


# Create your views here.

def activateEmail(request, user, to_email):
    mail_subject = 'Confirme ton adresse mail pour les JO 2024.'
    message = render_to_string('template_activate_account.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request,
                         f'Chère {user}, rend toi dans ta boite mail :{to_email} et clique sur le lien d\'activation'
                         f'pour compléter ton inscritpion.Note: Oubliez pas de contrôler votre dossier'
                         f'de SPAM.')
    else:
        messages.error(request, f'Un problème est survenu lors de l\'envoi à : {to_email}, contrôler que ce'
                                f' dernier à bien été renseigné lors de la saisie.')


def activate(request, uidb64, token):
    user = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = user.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, 'Merci d\'avoir confirmé votre compte, vous pouvez maintenant vous connecter.')
        return redirect('connexion')
    else:
        messages.error(request, 'Le lien de confirmation est invalide')

    return redirect('acceuil')


def inscription(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
            return redirect('connexion')
    else:
        form = CustomUserCreationForm()
    return render(request, 'inscription.html', {'form': form})


def connexion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('acceuil')
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
    return render(request, 'connexion.html')


# @login_required = requis une connexion pour accéder à la page
def acceuil(request):
    return render(request, 'acceuil.html')


def deconnexion(request):
    logout(request)
    return redirect('acceuil')


def offres(request):
    return render(request, 'offres.html')


def contact(request):
    return render(request, 'contact.html')


def checkout(request):
    return render(request, 'checkout.html')


@login_required(login_url='connexion/')
def create_checkout_session(request):
    if request.method == 'POST':
        try:
            selected_value = request.POST.get('offer')
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price': selected_value,
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=YOUR_DOMAIN + '/success/',
                cancel_url=YOUR_DOMAIN + '/cancel/',
            )
        except Exception as e:
            return str(e)

    return redirect(checkout_session.url, code=303)


def success(request):
    to_email = request.user.email
    username = request.user.username
    mail_subject = 'Tickets JO 2024'
    message = render_to_string('tickets.html', {
        'user': username,
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'email': to_email,
        'authentification': request.user.pk,
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        success(request)
    else:
        message.error(request, '')
    return render(request, 'success.html')


def cancel(request):
    return render(request, 'cancel.html')


def generate_random_string(length):
    letters = string.ascii_letters
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string


# Example usage: generate a random string of length 10
random_string = generate_random_string(50)
