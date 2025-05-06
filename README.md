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
  * **justification of indexes**:
    * **opening_time**: Landmarks can be sorted/filtered in the report based on their opening time, as such having an index will reduce the stress for ranged queries on the opening time
      * 287    start_landmark = Landmark.objects.filter(opening_time__lt=start)
    * **closing_time**: Landmarks can be sorted/filtered in the report based on their closing time, as such having an index will reduce the stress for ranged queries on the opening time
      * 291    close_landmark = Landmark.objects.filter(closing_time__gt=end)
    * **type**: Another query which Landmarks can be sorted/filtered is their type. Having types be adjacent to one-another will reudce the stree of querying based on type, and thus, you would not need to make as many page requests as if there was no index.
      * 277    temp1 = Landmark.objects.filter(type="C")
      * 279    temp2 = Landmark.objects.filter(type="H")
      * 281    temp3 = Landmark.objects.filter(type="N")
   
* Resturant
  * **attributes**: city, name, cusine, rating, price, opening_time, closing_time
  * **indexes**: opening_time, closing_time, price, rating
  * **justification of indexes**:
    * **opening_time**: Resturant can be sorted/filtered in the report based on their opening time, as such having an index will reduce the stress for ranged queries on the opening time
      * 447    resturants = resturants.filter(opening_time__lt=start)
    * **closing_time**: Resturant can be sorted/filtered in the report based on their closing time, as such having an index will reduce the stress for ranged queries on the opening time
      * 449    resturants = resturants.filter(closing_time__gt=end)
    * **price**: Another attriute that you can sort based on is price. Keeping in mind that price is seperated into 4 categorties only and since you can only request one price point, having price points adjacent to each other will reduce the number of page I/O and speed up the querying process
      * 440    resturants = resturants.filter(price=price_range)
    * **rating**: This is a ranged query which (especially with high ratings), benefits from this index.
      * 444    resturants = resturants.filter(rating__gte=rating)
   
* Activity
  * **attributes**: city, name, description, type
  * **indexes**: none

## Queries
The file views.py is where all queries are held: prepared statements, and ORM. The most important
functions are:
- **Creating new rows**:
 - add_edit_activity
 - add_edit_resturant
 - add_edit_landmark
-  **Request a specific object**:
 -  edit_activity_edit
 -  edit_resturant_edit
 -  edit_landmark_edit
-  **Large queries with multiple filtering/sort/gets**:
 -  activity_sort
 -  resturant_sort
 -  landmark_sort
 -  state
-  **Requesting lots of data (little to no filtering)**:
 -  get_name
 -  index
