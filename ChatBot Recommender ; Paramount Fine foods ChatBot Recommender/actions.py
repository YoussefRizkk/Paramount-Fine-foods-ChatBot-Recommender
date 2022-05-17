# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
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

from typing import Any, Text, Dict, List
from pandas.core.indexes import category
from rasa_sdk.events import SlotSet
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import csv
import pandas as pd
import json


class ActionSearch_Category(Action):

    def name(self) -> Text:
        return "action_search_category"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            type = str(tracker.get_slot('type'))
            print(type)
            data = pd.read_csv('C:/Lambton/AI_Project/chatbot/actions/Test_file.csv')
            data = data[data["type"]==type]
            print(data)
            response =''
            count =0
            for i in data['category'].unique():
                print(i)
                response = response + str(i) + "\n"
                count += 1
            dispatcher.utter_message("Please Pick a Food Category")
            dispatcher.utter_message("\n"+ response)



class ActionSearch_Food_Category(Action):

    def name(self) -> Text:
        return "action_search_food_category"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            type = str(tracker.get_slot('type'))
            category = str(tracker.get_slot('category'))
            print(type)
            print(category)
            data = pd.read_csv('C:/Lambton/AI_Project/chatbot/actions/Test_file.csv')
            #data[data.columns] = data.apply(lambda x: x.strip())
            data = data[data["type"].str.strip()==type.strip()]
            data = data[data["category"].str.strip()==category.strip()]
            print(data)
            response =''
            count =0
            for i in data['food'].unique():
                print(i)
                response = response + str(i) + "\n"
                count += 1
            dispatcher.utter_message("Please Pick a Food Category")
            dispatcher.utter_message("\n"+ response)

class ActionSearch_Food_Based_Ingredient(Action):
	def name(self):
		return "action_search_food_based_ingredient"
	def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            type = str(tracker.get_slot('type')).lower().strip()
            category = str(tracker.get_slot('category')).lower().strip()
            food = str(tracker.get_slot('food')).lower().strip()
            print(type)
            print(category)
            data = pd.read_csv('C:/Lambton/AI_Project/chatbot/actions/Test_file.csv')
            data = data[data["type"].str.strip()==type]
            data = data[data["category"].str.strip()==category]
            data = data[data["food"].str.strip()==food]
            response = ''
            for label, row in data.iterrows():
                response = response + "\n"+ 'HERE IS ALL ABOUT THE FOOD YOU SELECTED :  ' +str(row["food"]) + "\n"+' INGREDIENTS : '+ str(row["ingredients"]) +" \n"+' CALORIES    : '+ str(row["calories"]) + "\n"+ ' PRICE       : '+     '$' +    str(row["price"])+ "\n"+' QUANTITY    : ' +str(row["quantity"])
            
            if response =='':
                response ="\n"+'This is no food available with your input or selection'
            else:
                dispatcher.utter_message("\n"+ response)
                dispatcher.utter_message("Here is the list of food based on the ingredient you choose")

class ActionSearch_By_Ingredient(Action):
	def name(self):
		return "action_search_by_ingredient"
	def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            ingredient = str(tracker.get_slot('ingredient')).strip()
            data = pd.read_csv('C:/Lambton/AI_Project/chatbot/actions/Test_file.csv')
            data['ingredients'] = data['ingredients'].str.strip()
            data = data[data["ingredients"].str.contains(ingredient)]
            response = ''
            for label, row in data.iterrows():
                response = response + "\n"+ 'HERE IS ALL ABOUT THE FOOD YOU SELECTED :  ' +str(row["food"]) + "\n"+' INGREDIENTS : '+ str(row["ingredients"]) +" \n"+' CALORIES    : '+ str(row["calories"]) + "\n"+ ' PRICE       : '+     '$' +    str(row["price"])+ "\n"+' QUANTITY    : ' +str(row["quantity"])
            
            if response =='':
                response ="\n"+'This is no food available with your input or selection'
            else:
                dispatcher.utter_message("\n"+ response)
                dispatcher.utter_message("Here is the list of food based on the ingredient you choose")

class ActionSearch_Food_Only(Action):
	def name(self):
		return "action_search_food_only"
	def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            food = str(tracker.get_slot('food')).lower().strip()
            data = pd.read_csv('C:/Lambton/AI_Project/chatbot/actions/Test_file.csv')
            data = data[data["food"].str.strip()==food]
            response = ''
            for label, row in data.iterrows():
                response = response + "\n"+ 'HERE IS ALL ABOUT THE FOOD YOU SELECTED :  ' +str(row["food"]) + "\n"+ ' TYPE        : '+ str(row["type"]) + "\n" +' INGREDIENTS : '+ str(row["ingredients"]) +" \n"+' CALORIES    : '+ str(row["calories"]) + "\n"+ ' PRICE       : '+   '$' +  str(row["price"])+ "\n"+' QUANTITY    : ' +str(row["quantity"])
            if response =='':
                response ="\n"+'This is no food available with your input or selection'
            else:
                dispatcher.utter_message("\n"+ response)
                dispatcher.utter_message("Here is the list of food based on the ingredient you choose")

                
 