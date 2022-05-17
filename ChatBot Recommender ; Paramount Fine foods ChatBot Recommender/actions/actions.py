# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
#
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from sklearn.metrics.pairwise import cosine_similarity
import pickle, pandas as pd
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
#############################################################################
# Setting up the model and dataframe
df = pd.read_excel('TEST.xlsx')
ing_list = []
with open('count_vectorizer_model', 'rb') as f:
    cv = pickle.load(f)
with open('ingredients_model', 'rb') as f:
    ingredients_model = pickle.load(f)
#############################################################################

class ActionSetMealPreference(Action):  # Name of the class for Action


    def name(self):
        return 'setMealPreference'  # The name variable that should be added to stories.yml and domain.yml

    def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker, domain: "DomainDict") -> List[Dict[Text, Any]]:


        buttons = [
            {'payload':'/meal_preference{"meal_type":"vegeterian"}', 'title':'Vegeterian'},
            {'payload':'/meal_preference{"meal_type":"non-vegeterian"}','title':'Non-Vegeterian'}
        ]

    
        
        dispatcher.utter_message(text=f'Do you prefer vegeterian or non-vegeterian food?', buttons=buttons)

        slot_meal_type = tracker.get_slot('meal_type')
        # print(f'The set slot is {slot_meal_type}')
        # text = tracker.latest_message['text']
        # return await super().run(dispatcher, tracker, domain)
        return []


class ActionSetFoodCatogery(Action):  # Name of the class for Action


    def name(self):
        return 'setFoodCatogery'  # The name variable that should be added to stories.yml and domain.yml

    def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker, domain: "DomainDict") -> List[Dict[Text, Any]]:


        buttons1 = [
            {'payload':'/food_preference{"food_catogery":"Appetizer"}','title':'Appetizer'},
            {'payload':'/food_preference{"food_catogery":"Salad"}','title':'Salads'},
            {'payload':'/food_preference{"food_catogery":"Mains"}','title':'Mains'},
            {'payload':'/food_preference{"food_catogery":"Wraps"}','title':'Wraps'},
            {'payload':'/food_preference{"food_catogery":"Mashrooha"}','title':'Mashrooha'},
            {'payload':'/food_preference{"food_catogery":"Manakeesh"}','title':'Manakeesh'},
            {'payload':'/food_preference{"food_catogery":"Platters"}','title':'Platters'},
            {'payload':'/food_preference{"food_catogery":"Crispy"}','title':'Crispy'},
            {'payload':'/food_preference{"food_catogery":"Masemo"}','title':'Masemo'},
            {'payload':'/food_preference{"food_catogery":"Drinks"}','title':'Drinks'},
            {'payload':'/food_preference{"food_catogery":"Dessert"}','title':'Desserts'}
        ]

    
        
        dispatcher.utter_message(text=f'What is your prefered food Catogery?', buttons=buttons1)

        # slot_food_type = tracker.get_slot('food_catogery')
        # print(f'The set slot is {slot_food_type}')
        # text = tracker.latest_message['text']
        # return await super().run(dispatcher, tracker, domain)
        return []

class ActionSelectIngredient1(Action):  # Name of the class for Action


    def name(self):
        return 'actionSelectIngerident1'  


    def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker, domain: "DomainDict") -> List[Dict[Text, Any]]:



        slot_value_meal = tracker.get_slot("meal_type").lower()
        slot_value_food_type = tracker.get_slot("food_catogery").lower()
    
        ingredients_list_for_user_selected_food = []
        for ingredients in df[(df.type==slot_value_meal)&(df.category==slot_value_food_type)].ingredients:
            for i in ingredients.split(','):
                ingredients_list_for_user_selected_food.append(i)
        ingredients_list_for_user_selected_food = set(ingredients_list_for_user_selected_food)


        if ingredients_list_for_user_selected_food:
            print(ingredients_list_for_user_selected_food)
            buttons2 = []
            for ingredient in ingredients_list_for_user_selected_food:
                pl = "/ingredient_from_user{\"ingredients_list\":\"" + ingredient + "\"}"
                buttons2.append({'payload':pl, 'title':ingredient, })
                
        else:
            print(f'Sorry no combination found')

        dispatcher.utter_message(text=f'Select food from the list:', buttons=buttons2)
        return []

class ActionAddIngToList(Action):

    def name(self) -> Text:
        return "actionAddIngToList"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        ing_list.append(tracker.get_slot("ingredients_list"))

        return []

class ActionRecommendFood(Action):

    def name(self) -> Text:
        return "actionRecommendFood"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        slot_value_meal = tracker.get_slot("meal_type").lower()
        slot_value_food_type = tracker.get_slot("food_catogery").lower()

        count_matrix_user_selected_ingridents = cv.transform(ing_list)
        cosine_sim_between_ingredients = cosine_similarity(ingredients_model, count_matrix_user_selected_ingridents)
        
        df['cosine_sim_between_ingrd'] = cosine_sim_between_ingredients.mean(axis=1)

        df_recommendation = pd.DataFrame(columns=df.columns)
        for idx, similarity_score_mean in enumerate(cosine_sim_between_ingredients.mean(axis=1)):
            if similarity_score_mean > 0:
                df_recommendation = df_recommendation.append(df.iloc[idx], ignore_index=True)
        df_recommendation = df_recommendation.sort_values(by='cosine_sim_between_ingrd', ascending=False, ignore_index=True)
        print(df_recommendation[(df_recommendation.category==slot_value_food_type)&(df_recommendation.type==slot_value_meal)])
        # print(df_recommendation)
        return []

class ActionReceiveUserFood(Action):

    def name(self) -> Text:
        return "action_receive_user_food"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        text = tracker.latest_message['text']

        return [SlotSet("user_choice_food", text)]

class ActionTellUserFood(Action):

    def name(self) -> Text:
        return "action_tell_user_food"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        food_selected = tracker.get_slot("user_choice_food")
        ing_list2 = list(df.ingredients[df.food == food_selected])
        count_matrix_user_selected_ingridents = cv.transform(ing_list2)
        cosine_sim_between_ingredients = cosine_similarity(ingredients_model, count_matrix_user_selected_ingridents)
        
        df['cosine_sim_between_ingrd'] = cosine_sim_between_ingredients.mean(axis=1)

        df_recommendation = pd.DataFrame(columns=df.columns)
        for idx, similarity_score_mean in enumerate(cosine_sim_between_ingredients.mean(axis=1)):
            if similarity_score_mean > 0:
                df_recommendation = df_recommendation.append(df.iloc[idx], ignore_index=True)
        df_recommendation = df_recommendation.sort_values(by='cosine_sim_between_ingrd', ascending=False, ignore_index=True)
        print(df_recommendation)

        dispatcher.utter_message(text=f'Your selected food is {food_selected}')
        # print(df[df.food == food_selected])
        return []