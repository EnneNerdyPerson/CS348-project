README
# Relevent Files
I have uploaded the whole project, however, there are many files that are not relevent to grading 
(since they are libraries or code for running dganjo). As such, this is a list of the relevent 
files and what each file has. Please note, all revelent files will be in the folder:
project-name/resturant/helloworld

## Models and Indexes
The models.py file contains the models created for this project as well as the indexes for each model.
### Index Report
* States
  * **attributes**: name, region
  * **indexes**: region
  * **justification of indexes**:
    * **region**: The States are on occations requested based off of the region they exist in. As such,
having a indexes on States will allow you to request States based on regions fasters since the regions
will be adjacent to each other. Another thing to note, since this is one of the main ways which you 
would request a list of states, this query happens very often, making an Index helpful and relevent.
In file view.py:
      * 92     States.objects.filter(region=_region_)
      * 97     temp = States.objects.filter(region=i)
      * 240    states_picked = States.objects.filter(region=states_picked_list[0])
      * 403    states_picked = States.objects.filter(region=states_picked_list[0])
      * 534    states_picked = States.objects.filter(region=states_picked_list[0])
* City
  * **attribtues**: id, state, name
  * **indexes**: state
  * **justification of indexes**:
    * **state**: The Cities that are picked are often chosen based on the State they exist in and 
indexing based on a State will reduce the overhead of querying based on state, since cities that are 
being found will ba adjacent to each other. In file view.py
      * 130    city_list = City.objects.filter(state=states_picked[0]);
      * 132    cities = City.objects.filter(state=i)
      * 257    city_list = City.objects.filter(state=states_picked[0]);
      * 259    cities = City.objects.filter(state=i)
      * 421    city_list = City.objects.filter(state=states_picked[0]);
      * 423    cities = City.objects.filter(state=i)
      * 552    city_list = City.objects.filter(state=states_picked[0]);
      * 554    cities = City.objects.filter(state=i)
* Landmark
  * **attributes**: city, name, type, price, opening_time, closing_time
  * **indexes**: opening_time, closing_time, type
