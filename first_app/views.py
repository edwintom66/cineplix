from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import HttpResponse
import requests
from .forms import ContactForm
from django.core.mail import send_mail, BadHeaderError



# Create your views here.




def index(request):

    # for anime details 

    url_anime = 'https://api.jikan.moe/v3/top/anime/1/airing'

    req_anime = requests.get(url_anime).json()

    note = 0

    anime_data = []

    for death in range(10):

        anime_details = {
            'anime_title': req_anime['top'][note]['title'],
            'anime_date': req_anime['top'][note]['start_date'],
            'anime_jpg': req_anime['top'][note]['image_url'],
            'anime_rating': req_anime['top'][note]['score'],
            'anime_url': req_anime['top'][note]['url']
        }

        anime_data.append(anime_details)

        note = note + 1


    # for movie details

    url_movie = 'https://api.themoviedb.org/3/trending/movie/day?api_key=d8bf019d0cca372bd804735f172f67e8'

    x = requests.get(url_movie).json()


    list_movie = x['results']

    main_movie = []

    for i in list_movie:
        for j in i:
            if j == 'id':
                a = i['id']
                main_movie.append(a)

    main_movie = main_movie[:10] # get the first five elements.

    while len(main_movie) > 10:
      main_movie.pop()



    url_movie_1 = 'https://api.themoviedb.org/3/movie/{}?api_key=d8bf019d0cca372bd804735f172f67e8&language=en-US'
    url_movie_trailer = 'https://api.themoviedb.org/3/movie/{}/videos?api_key=d8bf019d0cca372bd804735f172f67e8&language=en-US'

    id_value_movie = ''


    # for id_value_movie in main_movie:

    #     s = requests.get(url_movie_1.format(id_value_movie)).json()


    #     movie_details = {
            # 'movie_title': r['title'],
            # 'movie_overview': r['overview'],
            # 'movie_date': r['release_date'],
            # 'movie_jpg': r['poster_path'],
            # 'movie_review': r['vote_average'],
    #     }

    #     movie_data.append(movie_details)


    # context_movie = {'movie_data':movie_data}


    # for tv details
    url_tv = 'https://api.themoviedb.org/3/trending/tv/day?api_key=d8bf019d0cca372bd804735f172f67e8'

    s = requests.get(url_tv).json()


    list_tv = s['results']

    main_tv = []


    for i in list_tv:
        for j in i:
            if j == 'id':
                a = i['id']
                main_tv.append(a)

    main_tv = main_tv[:10] # get the first five elements.

    while len(main_tv) > 10:
      main_tv.pop()



    url = 'https://api.themoviedb.org/3/tv/{}?api_key=d8bf019d0cca372bd804735f172f67e8&language=en-US'
    url_tv_trailer = 'https://api.themoviedb.org/3/tv/{}/videos?api_key=d8bf019d0cca372bd804735f172f67e8&language=en-US'

    id_value_tv = ''

    all_data = []
    tv_data = []


    for id_value_tv in main_tv:

        r = requests.get(url.format(id_value_tv)).json()
        u = requests.get(url_tv_trailer.format(id_value_tv)).json()

        tv_details = {
            'tv_title': r['name'],
            # 'tv_overview': r['overview'],
            'tv_date': r['first_air_date'],
            'tv_jpg': r['poster_path'],
            'tv_review': r['vote_average'],
        }

        try:
            link_you_tv = u['results'][0]['key']
        except:
            link_you_tv = 'fRh_vgS2dFE'

        tv_details['youtube_tv'] = link_you_tv

        tv_data.append(tv_details)

    for id_value_movie in main_movie:

        s = requests.get(url_movie_1.format(id_value_movie)).json()
        t = requests.get(url_movie_trailer.format(id_value_movie)).json()


        movie_details = {
            'movie_title': s['title'],
            'movie_date': s['release_date'],
            'movie_jpg': s['poster_path'],
            'movie_review': s['vote_average'],
            #'movie_overview': s['overview'],
        }

        try:
            link_you = t['results'][0]['key']

        except:

            link_you = 'fRh_vgS2dFE'


        

        movie_details['youtube'] = link_you

        all_data.append(movie_details)

    # search youtube movies


    # id_value_movie_trailer = ''


    # for id_value_movie_trailer in main_movie:



    context = {'tv_data':tv_data,'all_data':all_data,'anime_data':anime_data}

    print(len(all_data))

    return render(request,'index.html',context)

# def registration(request):
#     return render(request,'registration.html')








def landing(request):
    return HttpResponse('Landing page')

def about(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = f'Message from {form.cleaned_data["name"]}'
            message = form.cleaned_data["message"]
            sender = form.cleaned_data["email"]
            recipients = ['edwintom66@gmail.com']
            try:
                send_mail(subject, message, sender, recipients, fail_silently=True)
            except BadHeaderError:
                return HttpResponse('Invalid header found')
            return HttpResponse('Success...Your email has been sent')

    return render(request,'info.html',{'form':form})

