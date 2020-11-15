from django.shortcuts import render
import requests


# Create your views here.



def search_api_func(request):
    search_data = []


    if request.method == 'POST':


        search_url = 'https://api.themoviedb.org/3/search/multi'
        

        search_params = {
            'api_key':'d8bf019d0cca372bd804735f172f67e8',
            'query': request.POST['search'],
        }


        r = requests.get(search_url,params=search_params).json()

        try:
            del r['page']
            del r['total_results']
            del r['total_pages']
        except:
            pass

        try:

            max_result = r['results'][:10] # get the first five elements.

            while len(max_result) > 10:
                max_result.pop()
        except:
            pass

        try:
            for result in max_result:
                search_details = {
                    'searc_jpg':result['poster_path'],
                    'rating':result['vote_average'],
                }
                try:
                    search_details['date'] = result['release_date']
                except:
                    search_details['date'] = result['first_air_date']
                try:
                    search_details['title'] = result['title']
                except:
                    search_details['title'] = result['name']

                search_data.append(search_details)
        except:
            pass              

    context = {
        'search_data':search_data
    }
    return render(request,'search.html',context)


    