from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.template import RequestContext, loader
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views import generic
from nb_webapp.models import *
from django.core.context_processors import csrf
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

#import oauth2 as oauth

def home(request):
    # Fetch the user's information from request.user
    #print(request.user.username)
    user = BasicInfo.objects.get(user=request.user)
    #print(user)
    card_list_dict = {} # Dictionary for user_id-card_list mapping
    following_id_list = []
    following_dict = {} # Dictionary for user_id-basic_info mapping

    following_list = FollowingInfo.objects.filter(basic_info_id=user.user_id)
    for following_user in following_list:
        following_user_id = following_user.following_info_id
        following_id_list.append(following_user_id)
        cards = KnowledgeCard.objects.filter(basic_info_id=following_user_id)
        card_list = []
        for card in cards:
            card_list.append(card)
        card_list_dict[following_user_id] = card_list # Cards information
        following_dict[following_user_id] = BasicInfo.objects.get(user_id = following_user_id) # Following user information

    return render(request, 'Temp/homepage.html',
                  {'CardsDict': card_list_dict,'FollowingDict': following_dict,
                   'FollowingIDList': following_id_list, 'user': user})


def hello(request):
    p = BasicInfo.objects.get(user_id=1);
    return render(request, 'nb_webapp/liangruiTest.html',
                  {'name': p.account_email, 'id': p.user_id})


class IndexView(generic.ListView):
    template_name = 'nb_webapp/index.html'

    def get_queryset(self):
        """Return the last five published polls."""
        return "asdf"


# Save member id into db and connect with a internal id.
def register(request):
    error = False
    if 'linkedin-id' in request.GET:
        this_linkedin_id = request.GET['linkedin-id']
        this_name = request.GET['name']
        if not this_linkedin_id:
            error = True
        else:
            getLinkedinData(this_linkedin_id)
            return render(request, 'nb_webapp/register.html',
                          {'LINKEDIN_ID': this_linkedin_id, 'name': this_name})
    return render(request, 'nb_webapp/register.html', {'error': error})


def getLinkedinData(linkedin_id):
    consumer_key = 'gxls9vtr7moe'
    consumer_secret = 'efjIUM6aj3Fza2Nh'
    user_token = '33713a5e-5c84-48b4-a19d-56f9333d5e99'
    user_secret = '2f6c10e6-2413-4fb6-adb4-47c728fbcb2f'

    # Use your API key and secret to instantiate consumer object
    consumer = oauth.Consumer(consumer_key, consumer_secret)

    # Use your developer token and secret to instantiate access token object
    access_token = oauth.Token(
        key=user_token,
        secret=user_secret)
    client = oauth.Client(consumer, access_token)

    # Make call to LinkedIn to retrieve your own profile
    resp, content = client.request(
        "http://api.linkedin.com/v1/people/id=" + linkedin_id + ":(first-name,last-name,id,email-address,phone-numbers,industry)",
        "GET", "")
    basicInfo = BasicInfo(linkedin_member_id=linkedin_id)
    basicInfo.save()
    print content


def welcome(request):
    return render(request, 'Temp/welcome.html')


def page_signup(request):
    return render(request, 'Temp/signup.html')


def nb_signup(request): # Use the django authentication tool
    try:
        signup = request.POST['signup']
    except MultiValueDictKeyError:
        return render(request, "Temp/welcome.html")
    post_account_email = request.POST['account_email']
    post_password = request.POST['password']
    post_re_password = request.POST['re_password']
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    if post_account_email == '' or post_password == '' or post_re_password == '' or first_name == '' or last_name == '':
        error_message = "Please fill in all the forms."
        return render(request, "Temp/signup.html", {'error_message': error_message})
    if post_password != post_re_password:
        error_message = "Password mismatch!"
        return render(request, "Temp/signup.html", {'error_message': error_message})
    # Check for existence
    if User.objects.filter(username=post_account_email).exists():
        error_message = "User already exists!"
        return render(request, "Temp/signup.html", {'error_message': error_message})
    else:
        # Create a BasicInfo entry
        new_user = User.objects.create_user(post_account_email, post_account_email, post_password)
        new_user.first_name = first_name
        new_user.last_name = last_name
        new_user.save()
        qB = BasicInfo(user=new_user)
        qB.save()
        # Initialize the user's knowledge profile
        qK = KnowledgeProfile(basic_info=qB, num_flowers=0, num_posts=0, num_tags=0, num_thumbs=0, num_followings=0, num_followers=0)
        qK.save()
        success_message = "Sign up successfully!"
#        template = loader.get_template('Temp/welcome.html')
 #       context = RequestContext(request, {'success_message': success_message})
        #return HttpResponseRedirect(reverse('nb_webapp:success_signup', args=(success_message)))
        return render(request, 'Temp/welcome.html', {'success_message': success_message})

def nb_login(request): # Use the django authentication tool
    post_account_email = request.POST['account_email']
    post_password = request.POST['password']
    if post_account_email == '' or post_password == '':
        error_message = "Please fill in the account and the password."
        return render(request, "Temp/welcome.html", {'error_message': error_message})
    # Check for existence of the account
    #try:
    #    user = BasicInfo.objects.get(account_email = post_account_email)
    #except BasicInfo.DoesNotExist:
    #    error_message = "Account does not exist!"
    #    return render(request, "Temp/welcome.html", {'error_message': error_message})
    #if user.password != post_password:
    #    error_message = "Password error!"
    #    return render(request, "Temp/welcome.html", {'error_message': error_message})
    user = authenticate(username = post_account_email, password = post_password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect(reverse('nb_webapp:home'))
        else:
            error_message = "Account disabled!"
            return render(request, "Temp/welcome.html", {'error_message': error_message})
    else:
        error_message = "Wrong account information!"
        return render(request, "Temp/welcome.html", {'error_message': error_message})