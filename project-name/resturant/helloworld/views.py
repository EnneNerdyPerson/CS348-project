from django.shortcuts import render
from django.template import loader
from django.urls import reverse


from .models import States, City, Landmark, Resturant, Activity
from .forms import StateForm, LandmarkSort, ResturantSort, ActivitySort, LandmarkEdit, ResturantEdit, ActivityEdit




# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect


def index(request):
    state_list = States.objects.all()
    city_list = City.objects.all()
    landmarks = Landmark.objects.all()
    template = loader.get_template("polls/index.html")
    context = {
        "state_list": state_list,
        "city_list": city_list,
        "landmarks": landmarks
    }
    # output = ", ".join([s.name for s in state_list])

    return HttpResponse(template.render(context, request))

def get_name(request):
    if request.method == "POST":
        form = StateForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect("")
    else:
        form = StateForm()

    state_list = States.objects.all()
    city_list = City.objects.all()
    landmarks = Landmark.objects.all()
    resturants = Resturant.objects.all()
    activities = Activity.objects.all()
    context = {
        "form": form,
        "state_list": state_list,
        "landmarks": landmarks,
        "resturants": resturants,
        "activties": activities
    }

    return render(request, "polls/name.html", context)

def state_name(request):
    region_list = {}
    type_list = {}
    state_listing = {}
    
    form = StateForm(request.POST)
    if form.is_valid():
        region_list = form.cleaned_data['region']
        type_list = form.cleaned_data['type']
        state_listing = form.cleaned_data['states']
    else:
        region_list = "="

    if not region_list:
        region_list = [""]
    else:
        region_list = ','.join(region_list)

    if not type_list:
        type_list = [""]
    else:
        type_list = ','.join(type_list)

    if not state_listing:
        state_listing = [""]
    else:
        state_listing = ','.join(state_listing)
   
    return HttpResponseRedirect(reverse("helloworld:state", args=(region_list, type_list, state_listing, )))

def state(request, region_list, type_list, state_list):
    states_picked = {}
    city_list = {}
    landmarks = {}
    resturants = {}
    activties = {}


    region_arry = region_list.split(',')
    states_picked = States.objects.filter(region=region_arry[0])
    if states_picked:
        for i in region_arry:
            if i == 0:
                continue
            temp = States.objects.filter(region=i)
            states_picked = states_picked.union(temp)

    state_array = state_list.split(',')

    if state_list:
        for i in state_array:
            if i == 0:
                continue
            if i == "all":
                states_picked = States.objects.all()
            else:
                temp = States.objects.filter(name=i)
                states_picked = states_picked.union(temp)
    
    state_list = {}
    if state_array[0] == "all":
        state_list = "all"
    else:
        state_array = states_picked.values_list('name').order_by("name")
        for i in state_array:
            string = i
            state_list.update({i[0] : i[0]})
        state_list = ','.join(state_list)

    if ((not state_list) and (region_list)):
        print("Hello")

    if type_list:
        type_array = type_list.split(',')

        count = 0
        if states_picked:
            city_list = City.objects.filter(state=states_picked[0]);
            for i in states_picked:
                cities = City.objects.filter(state=i)
                city_list = city_list.union(cities)
                count += 1

        landmarks = Landmark.objects.filter(name="")
        resturants = Resturant.objects.filter(name="")
        activties = Activity.objects.filter(name="")

        for i in type_array:
            if i == "landmark":
                landmarks = Landmark.objects.all()
            elif i == "resturant":
                resturants = Resturant.objects.all()
            elif i == "activity":
                activties = Activity.objects.all()

        selected_states = []

        selected_landmarks = landmarks.values_list('city')
        for i in selected_landmarks:
            val = City.objects.get(id=i[0]).state.name
            if val not in selected_states:
                selected_states.append(City.objects.get(id=i[0]).state.name)

        resturants_landmarks = resturants.values_list('city')
        for i in resturants_landmarks:
            val = City.objects.get(id=i[0]).state.name
            if val not in selected_states:
                selected_states.append(City.objects.get(id=i[0]).state.name)

        activties_landmarks = activties.values_list('city')
        for i in activties_landmarks:
            val = City.objects.get(id=i[0]).state.name
            if val not in selected_states:
                selected_states.append(City.objects.get(id=i[0]).state.name)

    if request.method == "POST":
        landmark_form = LandmarkSort(request.POST)
        if landmark_form.is_valid():
            return HttpResponseRedirect("")
        
        resturant_form = ResturantSort(request.POST)
        if resturant_form.is_valid():
            return HttpResponseRedirect("")
        
        activities_form = ActivitySort(request.POST)
        if activities_form.is_valid():
            return HttpResponseRedirect("")
    else:
        landmark_form = LandmarkSort()
        resturant_form = ResturantSort()
        activities_form = ActivitySort()

    context = {
        "states_picked": states_picked,
        "city_list": city_list,
        "type_list": type_list,
        "state_list": state_list,
        "selected_states": selected_states,
        "landmarks": landmarks,
        "resturants": resturants,
        "activties": activties,
        "form1": landmark_form,
        "form2": resturant_form,
        "form3": activities_form
    }

    return render(request, "polls/state.html", context)

def landmark_get(request, states_picked_list, type_list):
    form = LandmarkSort(request.POST)
    start = 10
    end = 10
    landtype_list = "none"
    if form.is_valid():
        landtype_list = form.cleaned_data['landmark_type']
        print(landtype_list)
        if landtype_list == "":
            landtype_list = "none";
        start_time = form.cleaned_data['start_time']
        if start_time is not None:
            start = start_time.hour + start_time.minute / 60 + start_time.second / 3600
        else:
            start = 10

        end_time = form.cleaned_data['end_time']
        if end_time is not None:
            end = end_time.hour + end_time.minute / 60 + end_time.second / 3600
        else:
            end = 10
    else:
        print(form.errors)
        
    if not landtype_list:
        landtype_list = "none"
    else:
        landtype_list = ','.join(landtype_list)
   
    return HttpResponseRedirect(reverse("helloworld:landmark_sort", args=(states_picked_list, type_list, landtype_list, start, end, )))

def landmark_sort(request, states_picked_list, type_list, landtype_list, start, end):
    print("HELLLO WORLD")
    print(landtype_list)

    if states_picked_list:
        if states_picked_list == "all":
            states_picked = States.objects.all()
        else:
            states_picked = States.objects.filter(region=states_picked_list[0])

            state_array = states_picked_list.split(',')
            if state_array:
                for i in state_array:
                    temp = States.objects.filter(name=i)
                    states_picked = states_picked.union(temp)
    
    city_list = {}
    landmarks = {}
    resturants = {}
    activties = {}

    if type_list:
        type_array = type_list.split(',')
        (type_array)
        if states_picked:
            city_list = City.objects.filter(state=states_picked[0]);
            for i in states_picked:
                cities = City.objects.filter(state=i)
                city_list = city_list.union(cities)

        landmarks = Landmark.objects.filter(name="")
        resturants = Resturant.objects.filter(name="")
        activties = Activity.objects.filter(name="")

        for i in type_array:
            if i == "landmark":
                landmarks = Landmark.objects.none()
                print("list:")
                print(landtype_list)
                # landtype_array = landtype_list.split(",")
                temp1 = Landmark.objects.none()
                temp2 = Landmark.objects.none()
                temp3 = Landmark.objects.none()
                if landtype_list != "none":
                    if "C" in landtype_list:
                        temp1 = Landmark.objects.filter(type="C")
                    if "H" in landtype_list:
                        temp2 = Landmark.objects.filter(type="H")
                    if "N" in landtype_list:
                        temp3 = Landmark.objects.filter(type="N")

                    landmarks = temp1.union(temp2)
                    landmarks = landmarks.union(temp3)
            
                if start != 10:
                    start_landmark = Landmark.objects.filter(opening_time__lt=start)
                    landmarks = landmarks.intersection(start_landmark)

                if start != 10:
                    close_landmark = Landmark.objects.filter(closing_time__gt=end)
                    landmarks = landmarks.intersection(close_landmark)

            elif i == "resturant":
                resturants = Resturant.objects.all()

            elif i == "activity":
                activties = Activity.objects.all()
    

    if request.method == "POST":
        landmark_form = LandmarkSort(request.POST)
        if landmark_form.is_valid():
            return HttpResponseRedirect("")
        
        resturant_form = ResturantSort(request.POST)
        if resturant_form.is_valid():
            return HttpResponseRedirect("")
        
        activities_form = ActivitySort(request.POST)
        if activities_form.is_valid():
            return HttpResponseRedirect("")
    else:
        landmark_form = LandmarkSort()
        resturant_form = ResturantSort()
        activities_form = ActivitySort()
    
    selected_states = []

    selected_landmarks = landmarks.values_list('city')
    for i in selected_landmarks:
        val = City.objects.get(id=i[0]).state.name
        if val not in selected_states:
            selected_states.append(City.objects.get(id=i[0]).state.name)

    resturants_landmarks = resturants.values_list('city')
    for i in resturants_landmarks:
        val = City.objects.get(id=i[0]).state.name
        if val not in selected_states:
            selected_states.append(City.objects.get(id=i[0]).state.name)

    activties_landmarks = activties.values_list('city')
    for i in activties_landmarks:
        val = City.objects.get(id=i[0]).state.name
        if val not in selected_states:
            selected_states.append(City.objects.get(id=i[0]).state.name)

    context = {
        "states_picked": states_picked,
        "city_list": city_list,
        "type_list": type_list,
        "state_list": states_picked_list,
        "selected_states": selected_states,
        "landmarks": landmarks,
        "resturants": resturants,
        "activties": activties,
        "form1": landmark_form,
        "form2": resturant_form,
        "form3": activities_form
    }

    return render(request, "polls/state.html", context)

def resturant_get(request, states_picked_list, type_list):
    form = ResturantSort(request.POST)
    start = 10
    end = 10
    price_range = "$"
    rating = 10
    cusine= {"none": "="}
    print(form.is_valid())
    if form.is_valid():
        print("HELLO")
        price_range = form.cleaned_data['price_range']
        print(price_range)
        print("==============================")
        if len(price_range) == 0:
            price_range = "none"

        rating = form.cleaned_data['rating']
        if rating is None:
            rating = 10

        start_time = form.cleaned_data['start_time']
        if start_time is not None:
            start = start_time.hour + start_time.minute / 60 + start_time.second / 3600
        else:
            start = 10

        end_time = form.cleaned_data['end_time']
        if end_time is not None:
            end = end_time.hour + end_time.minute / 60 + end_time.second / 3600
        else:
            end = 10
        
        cusine = form.cleaned_data['cusine']
    else:
        print(form.errors)
    
    if not cusine:
        cusine = "none"
    else:
        cusine = ','.join(cusine)
   
    return HttpResponseRedirect(reverse("helloworld:resturant_sort", args=(states_picked_list, type_list, price_range, rating, start, end, cusine, )))

def resturant_sort(request, states_picked_list, type_list, price_range, rating, start, end, cusine):

    if states_picked_list:
        if states_picked_list == "all":
            states_picked = States.objects.all()
        else:
            states_picked = States.objects.filter(region=states_picked_list[0])

            state_array = states_picked_list.split(',')
            if state_array:
                for i in state_array:
                    temp = States.objects.filter(name=i)
                    states_picked = states_picked.union(temp)
    
    city_list = {}
    landmarks = {}
    resturants = {}
    activties = {}

    if type_list:
        type_array = type_list.split(',')
        print(type_array)
        count = 0
        if states_picked:
            city_list = City.objects.filter(state=states_picked[0]);
            for i in states_picked:
                cities = City.objects.filter(state=i)
                city_list = city_list.union(cities)
                count += 1

        landmarks = Landmark.objects.filter(name="")
        resturants = Resturant.objects.filter(name="")
        activties = Activity.objects.filter(name="")

        for i in type_array:
            if i == "landmark":
                landmarks = Landmark.objects.all()
            elif i == "resturant":
                resturants = Resturant.objects.all()
                print(price_range)
                if price_range != "none":
                    print(price_range)
                    # str = price_range.toString()
                    resturants = resturants.filter(price=price_range)
                print(resturants)
                
                if rating != "10":
                    resturants = resturants.filter(rating__gte=rating)

                if start != "10":
                    resturants = resturants.filter(opening_time__lt=start)
                if end != "10":
                    resturants = resturants.filter(closing_time__gt=end)

                cusine_list = Resturant.objects.none()
                cusine_array = cusine.split(',')
                if cusine != "none":
                    for i in cusine_array:
                        temp = Resturant.objects.filter(cusine=i)
                        cusine_list = cusine_list.union(temp)
                else:
                    cusine_list = Resturant.objects.all()
                resturants = resturants.intersection(cusine_list)
                print(resturants)

            elif i == "activity":
                activties = Activity.objects.all()
    
    selected_states = []

    selected_landmarks = landmarks.values_list('city')
    for i in selected_landmarks:
        val = City.objects.get(id=i[0]).state.name
        if val not in selected_states:
            selected_states.append(City.objects.get(id=i[0]).state.name)

    resturants_landmarks = resturants.values_list('city')
    for i in resturants_landmarks:
        val = City.objects.get(id=i[0]).state.name
        if val not in selected_states:
            selected_states.append(City.objects.get(id=i[0]).state.name)

    activties_landmarks = activties.values_list('city')
    for i in activties_landmarks:
        val = City.objects.get(id=i[0]).state.name
        if val not in selected_states:
            selected_states.append(City.objects.get(id=i[0]).state.name)

    if request.method == "POST":
        landmark_form = LandmarkSort(request.POST)
        if landmark_form.is_valid():
            return HttpResponseRedirect("")
        
        resturant_form = ResturantSort(request.POST)
        if resturant_form.is_valid():
            return HttpResponseRedirect("")
        
        activities_form = ActivitySort(request.POST)
        if activities_form.is_valid():
            return HttpResponseRedirect("")
    else:
        landmark_form = LandmarkSort()
        resturant_form = ResturantSort()
        activities_form = ActivitySort()
    
    context = {
        "states_picked": states_picked,
        "city_list": city_list,
        "type_list": type_list,
        "state_list": states_picked_list,
        "selected_states": selected_states,
        "landmarks": landmarks,
        "resturants": resturants,
        "activties": activties,
        "form1": landmark_form,
        "form2": resturant_form,
        "form3": activities_form
    }

    return render(request, "polls/state.html", context)

def activity_get(request, states_picked_list, type_list):
    form = ActivitySort(request.POST)
    activity_type="none"
    keyword="="
    if form.is_valid():
        activity_type = form.cleaned_data['activity_type']
        keyword = form.cleaned_data['keyword']
       
    return HttpResponseRedirect(reverse("helloworld:activity_sort", args=(states_picked_list, type_list, activity_type, keyword, )))

def activity_sort(request, states_picked_list, type_list, activity_type, keyword):

    if states_picked_list:
        if states_picked_list == "all":
            states_picked = States.objects.all()
        else:
            states_picked = States.objects.filter(region=states_picked_list[0])

            state_array = states_picked_list.split(',')
            if state_array:
                for i in state_array:
                    temp = States.objects.filter(name=i)
                    states_picked = states_picked.union(temp)
    
    city_list = {}
    landmarks = {}
    resturants = {}
    activties = {}

    if type_list:
        type_array = type_list.split(',')
        print(type_array)
        count = 0
        if states_picked:
            city_list = City.objects.filter(state=states_picked[0]);
            for i in states_picked:
                cities = City.objects.filter(state=i)
                city_list = city_list.union(cities)
                count += 1

        landmarks = Landmark.objects.filter(name="")
        resturants = Resturant.objects.filter(name="")
        activties = Activity.objects.filter(name="")

        for i in type_array:
            if i == "landmark":
                landmarks = Landmark.objects.all()
            elif i == "resturant":
                resturants = Resturant.objects.all()

            elif i == "activity":
                activties = Activity.objects.all()
                if activity_type != "B":
                    print(activity_type)
                    activties.filter(type=activity_type)
                
                print(keyword)

                if keyword != "=":
                    print("checking in")
                    listing = activties
                    for val in listing:
                        str = val.description
                        if keyword not in str:
                            activties = activties.exclude(name=val.name)
    
    selected_states = []

    selected_landmarks = landmarks.values_list('city')
    for i in selected_landmarks:
        val = City.objects.get(id=i[0]).state.name
        if val not in selected_states:
            selected_states.append(City.objects.get(id=i[0]).state.name)

    resturants_landmarks = resturants.values_list('city')
    for i in resturants_landmarks:
        val = City.objects.get(id=i[0]).state.name
        if val not in selected_states:
            selected_states.append(City.objects.get(id=i[0]).state.name)

    activties_landmarks = activties.values_list('city')
    for i in activties_landmarks:
        val = City.objects.get(id=i[0]).state.name
        if val not in selected_states:
            selected_states.append(City.objects.get(id=i[0]).state.name)

    if request.method == "POST":
        landmark_form = LandmarkSort(request.POST)
        if landmark_form.is_valid():
            return HttpResponseRedirect("")
        
        resturant_form = ResturantSort(request.POST)
        if resturant_form.is_valid():
            return HttpResponseRedirect("")
        
        activities_form = ActivitySort(request.POST)
        if activities_form.is_valid():
            return HttpResponseRedirect("")
    else:
        landmark_form = LandmarkSort()
        resturant_form = ResturantSort()
        activities_form = ActivitySort()
    
    context = {
        "states_picked": states_picked,
        "city_list": city_list,
        "type_list": type_list,
        "state_list": states_picked_list,
        "selected_states": selected_states,
        "landmarks": landmarks,
        "resturants": resturants,
        "activties": activties,
        "form1": landmark_form,
        "form2": resturant_form,
        "form3": activities_form
    }

    return render(request, "polls/state.html", context)

def edit_landmark(request):
    form = LandmarkEdit()
    context = {
        "form": form
    }
    template = loader.get_template("polls/edit-landmark.html")
    return HttpResponse(template.render(context, request))

def edit_landmark_edit(request, name):
    landmark = Landmark.objects.get(name=name)
    form = LandmarkEdit(initial={"name": landmark.name, 
                                 "state": landmark.city.state,
                                 "city": landmark.city.name, 
                                 "landmark_type": landmark.type, 
                                 "price": landmark.price, 
                                 "start_time": landmark.opening_time, 
                                 "end_time": landmark.closing_time}, 
                                 auto_id=False)
    context = {
        "form_name": form
    }
    # template = loader.get_template("polls/edit-landmark.html")
    return render(request, "polls/edit-landmark.html", context)

def edit_landmark_get(request):
    form = LandmarkEdit(request.POST)
    start = 0
    end = 24
    landtype = "none"
    city = "none"
    name = "none"
    state = "none"
    price = 0
    if form.is_valid():
        start_time = form.cleaned_data['start_time']
        if start_time is not None:
            start = start_time.hour + start_time.minute / 60 + start_time.second / 3600
        else:
            start = 0
        end_time = form.cleaned_data['end_time']
        if end_time is not None:
            end = end_time.hour + end_time.minute / 60 + end_time.second / 3600
        else:
            end = 24
        landtype = form.cleaned_data['landmark_type']
        if landtype == "":
            landtype = "none";
        city = form.cleaned_data['city']
        if city == "":
            city = "none";
        name = form.cleaned_data['name']
        if name == "":
            name = "none";
        state = form.cleaned_data['state']
        if state == "":
            state = "none";
        price = form.cleaned_data['price']
        if price is None:
            price = 0
    else:
        print(form.errors)
   
    return HttpResponseRedirect(reverse("helloworld:add_edit_landmark", args=(name, state, city, landtype, price, start, end, )))
    
def add_edit_landmark(request, name, state, city, landtype, price, start, end):
    city_count = City.objects.all().count()
    if City.objects.get(name=city):
        if not (Landmark.objects.filter(name=name).exists()):
            landmark = Landmark.objects.create(
                city = City.objects.get(name=city),
                name = name,
                type=landtype,
                price=price,
                opening_time=start,
                closing_time=end
            )
        else:
            Landmark.objects.filter(name = name).update(
                city = City.objects.get(name=city),
                type=landtype,
                price=price,
                opening_time=start,
                closing_time=end
            )
    else:
        city_count += 1
        new_city = City.objects.create(
            id=city_count,
            state=States.objects.get(name=state),
            name=city
        )
        if not (Landmark.objects.filter(name=name).exists()):

            landmark = Landmark.objects.create(
                city = new_city,
                name = name,
                type=landtype,
                price=price,
                opening_time=start,
                closing_time=end
            )
        else:
            Landmark.objects.filter(name = name).update(
                city = new_city,
                type=landtype,
                price=price,
                opening_time=start,
                closing_time=end
            )

    return HttpResponseRedirect(reverse("helloworld:get_state", args=( )))

def edit_resturant(request):
    form = ResturantEdit()
    context = {
        "form": form
    }
    template = loader.get_template("polls/edit-resturant.html")
    return HttpResponse(template.render(context, request))

def edit_resturant_edit(request, name):
    resturant = Resturant.objects.get(name=name)
    form = ResturantEdit(initial={"name": resturant.name, 
                                "state": resturant.city.state,
                                "city": resturant.city.name, 
                                "type": resturant.cusine, 
                                "rating": resturant.rating,
                                "price_range": resturant.price, 
                                "start_time": resturant.opening_time, 
                                "end_time": resturant.closing_time}, 
                                auto_id=False)
    context = {
        "form_name": form
    }
    # template = loader.get_template("polls/edit-landmark.html")
    return render(request, "polls/edit-resturant.html", context)

def edit_resturant_get(request):
    form = ResturantEdit(request.POST)
    start = 0
    end = 24
    type = "none"
    city = "none"
    name = "none"
    state = "none"
    price = "none"
    rating = 0
    if form.is_valid():
        start_time = form.cleaned_data['start_time']
        if start_time is not None:
            start = start_time.hour + start_time.minute / 60 + start_time.second / 3600
        else:
            start = 0
        end_time = form.cleaned_data['end_time']
        if end_time is not None:
            end = end_time.hour + end_time.minute / 60 + end_time.second / 3600
        else:
            end = 24
        type = form.cleaned_data['type']
        if type == "":
            type = "none";
        city = form.cleaned_data['city']
        if city == "":
            city = "none";
        name = form.cleaned_data['name']
        if name == "":
            name = "none";
        state = form.cleaned_data['state']
        if state == "":
            state = "none";
        price = form.cleaned_data['price_range']
        if price is None:
            price = "none"
        rating = form.cleaned_data['rating']
        if rating is None:
            rating = 0
        
    else:
        print(form.errors)
   
    return HttpResponseRedirect(reverse("helloworld:add_edit_resturant", args=(name, state, city, type, price, rating, start, end, )))

def add_edit_resturant(request, name, state, city, type, price, rating, start, end):
    city_count = City.objects.all().count()
    if (City.objects.filter(name=city).exists()):
        if not Resturant.objects.filter(name=name).exists():
            resturant = Resturant.objects.create(
                city = City.objects.get(name=city),
                name = name,
                cusine=type,
                rating=rating,
                price=price,
                opening_time=start,
                closing_time=end
            )
        else:
            Resturant.objects.filter(name = name).update(
                city = City.objects.get(name=city),
                cusine=type,
                rating=rating,
                price=price,
                opening_time=start,
                closing_time=end
            )
    else:
        city_count = city_count + 2
        new_city = City.objects.create(
            id=city_count,
            state=States.objects.get(name=state),
            name=city
        )
        if not Resturant.objects.filter(name=name).exists():
            resturant = Resturant.objects.create(
                city = new_city,
                name = name,
                cusine=type,
                rating=rating,
                price=price,
                opening_time=start,
                closing_time=end
            )
        else:
            Resturant.objects.filter(name = name).update(
                city = new_city,
                cusine=type,
                rating=rating,
                price=price,
                opening_time=start,
                closing_time=end
            )

    return HttpResponseRedirect(reverse("helloworld:get_state", args=( )))

def edit_activity(request):
    form = ActivityEdit()
    context = {
        "name": "",
        "form": form,
        "form-name": form
    }
    template = loader.get_template("polls/edit-activity.html")
    return HttpResponse(template.render(context, request))

def edit_activity_edit(request, name):
    if (Activity.objects.filter(name=name).exists()):
        activity = Activity.objects.get(name=name)
        form_name = ActivityEdit(initial={"name": activity.name, 
                                    "state": activity.city.state,
                                    "city": activity.city.name, 
                                    "description": activity.description,
                                    "type": activity.type}, 
                                    auto_id=False)
        context = {
            # "activity": True,
            "form_name": form_name
        }
        # template = loader.get_template("polls/edit-landmark.html")
        # return HttpResponseRedirect(reverse("helloworld:edit-activity", args=( )))
        return render(request, "polls/edit-activity.html", context)

def edit_activity_get(request):
    form = ActivityEdit(request.POST)
    type = "none"
    city = "none"
    name = "none"
    state = "none"
    description = "none"
    if form.is_valid():
        type = form.cleaned_data['type']
        if type == "":
            type = "none";
        city = form.cleaned_data['city']
        if city == "":
            city = "none";
        name = form.cleaned_data['name']
        if name == "":
            name = "none";
        state = form.cleaned_data['state']
        if state == "":
            state = "none";
        description = form.cleaned_data['description']
        if description == "":
            description = "none"
        
    else:
        print(form.errors)
   
    return HttpResponseRedirect(reverse("helloworld:add_edit_activity", args=(name, state, city, type, description, )))

def add_edit_activity(request, name, state, city, type, description):
    city_count = City.objects.all().count()
    if (City.objects.filter(name=city).exists()):
        if not (Activity.objects.filter(name=name).exists()):
            activity = Activity.objects.create(
                city = City.objects.get(name=city),
                name = name,
                description=description,
                type = type
            )
        else:
            Activity.objects.filter(name=name).update(
                city = City.objects.get(name=city),
                name = name,
                description=description,
                type = type
            )
    else:
        city_count = city_count + 2
        new_city = City.objects.create(
            id=city_count,
            state=States.objects.get(name=state),
            name=city
        )
        if not (Activity.objects.filter(name=name).exists()):
            activity = Activity.objects.create(
                city = new_city,
                name = name,
                description=description,
                type = type
            )
        else:
            Activity.objects.filter(name=name).update(
                city = new_city,
                name = name,
                description=description,
                type = type
            )

    return HttpResponseRedirect(reverse("helloworld:get_state", args=( )))
