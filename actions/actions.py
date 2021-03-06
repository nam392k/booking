import mysql.connector as con
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, EventType, FollowupAction
import numpy as np
import requests
from datetime import datetime
from typing import Text, List, Any, Dict
from rasa_sdk import Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

# class ValidateBookingForm(FormValidationAction):
#     def name(self) -> Text:
#         return "validate_booking_form"
#     # def validate_time(
#     #     self,
#     #     slot_value: Any,
#     #     dispatcher: CollectingDispatcher,
#     #     tracker: Tracker,
#     #     domain: DomainDict,
#     # ) -> Dict[Text, Any]:
#     #     dentist = tracker.get_slot("dentist")
#     #     gender = tracker.get_slot("gender")
#     #     time = tracker.get_slot("time")
#     #     # layIDnhasi
#     #     response = requests.get("http://localhost:8080/api/get-all-doctors")
#     #     data = response.json()
#     #     for x in data['data']:
#     #         if (x['firstName'] == dentist):
#     #             idDentist = x['id']
#     #     print(idDentist)
#     #     # convert ngay
#     #     date = tracker.get_slot("date")
#     #     date_object = datetime.strptime(date, "%d/%m/%Y")
#     #     print("date_object =", date_object)

#     #     timestamp = datetime.timestamp(date_object)
#     #     dateChanged = str(timestamp).replace(".0", "") + '000'
#     #     print(dateChanged)
#     #     api = 'http://localhost:8080/api/get-schedule-doctor-by-date?doctorId=' + str(idDentist) + '&date=' + dateChanged
#     #     response2 = requests.get(api)
#     #     data2 = response2.json()
#     #     print(data2)
#     #     for x in data2['data']:
#     #         if (x['timeTypeData']['valueVi'] == time):
#     #             if (x['currentNumber'] == None):
#     #                 print(x['currentNumber'])
#     #                 return {"time": slot_value}
#     #             else:
#     #                 # validation failed, set this slot to None so that the
#     #                 # user will be asked for the slot again
#     #                 print(x['currentNumber'])
#     #                 dispatcher.utter_message('Khung gi??? ' + gender + ' v???a ch???n ???? c?? ng?????i ?????t!')
#     #                 dispatcher.utter_message('Vui l??ng ch???n khung gi??? kh??c')
#     #                 return {"time": None}
    # def validate_note(
    #     self,
    #     slot_value: Any,
    #     dispatcher: CollectingDispatcher,
    #     tracker: Tracker,
    #     domain: DomainDict,
    # ) -> Dict[Text, Any]:
    #     if(tracker.get_slot("note")=="Kh??ng"):
    #         return {"note": slot_value}
    #     else: 
    #         dispatcher.utter_message('Vui l??ng nh???p l??u ?? cho bu???i kh??m')
    #         return {"note": None}

class booking_form(Action):

    def name(self) -> Text:
        return "booking_form"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> List[EventType]:
        required_slots = ["service", "dentist", "customer", "phone", "email", "date", "time", "note"]


class submit_form_booking(Action):
    def name(self) -> Text:
        return "action_submit_form"

    def run(self, dispatcher, tracker: Tracker,
            domain: Dict, ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            template="utter_slots_values", gender=tracker.get_slot("gender"), service_book=tracker.get_slot("service"),
            dentist_book=tracker.get_slot("dentist"), customer_book=tracker.get_slot("customer"),
            phone_book=tracker.get_slot("phone"), email_book=tracker.get_slot("email"),
            date_book=tracker.get_slot("date"), time_book=tracker.get_slot("time"), note_book=tracker.get_slot("note")
        )
        select = ["?????ng ?? ?????t l???ch", "B??? ?????t l???ch"]
        button = []
        for x in select:
            button.append(
                {"title": x, "payload": '/book_intent{\"book_check\": \"' + x + '\"}'})

        dispatcher.utter_button_message(" ", button)
        return []


class insert_form_booking(Action):
    def name(self) -> Text:
        return "action_insert_val_form"

    def run(self, dispatcher, tracker: Tracker,
            domain: Dict, ) -> List[Dict[Text, Any]]:

        book_check = tracker.get_slot("book_check")
        print('book check: ', book_check)

        if (book_check == "?????ng ?? ?????t l???ch"):
            service = tracker.get_slot("service")
            dentist = tracker.get_slot("dentist")
            customer = tracker.get_slot("customer")
            phone = tracker.get_slot("phone")
            email = tracker.get_slot("email")
            note = tracker.get_slot("note")
            gender = tracker.get_slot("gender")

            if (gender == 'Anh'):
                genderChanged = 'M'
            elif (gender == 'Ch???'):
                genderChanged = 'F'
            print(genderChanged)
            #################################################
            # lay id dich vu
            response = requests.get("http://localhost:8080/api/service-chatbot")
            data = response.json()
            for x in data['data']:
                if (x['ServiceData']['valueVi'] == service):
                    idService = x['serviceId']
            print(idService)

            # convert ngay
            date = tracker.get_slot("date")
            date_object = datetime.strptime(date, "%d/%m/%Y")
            print("date_object =", date_object)

            timestamp = datetime.timestamp(date_object)
            dateChanged = str(timestamp).replace(".0", "") + '000'
            print(dateChanged)
            # layIDnhasi
            response = requests.get("http://localhost:8080/api/get-all-doctors")
            data = response.json()
            for x in data['data']:
                if (x['firstName'] == dentist):
                    idDentist = x['id']
            print(idDentist)
            # timeChanged
            time = tracker.get_slot("time")
            timeChanged = 'T1'
            if (time == '8:00 - 9:00'):
                timeChanged = 'T2'
            elif (time == '9:00 - 10:00'):
                timeChanged = 'T3'
            elif (time == '10:00 - 11:00'):
                timeChanged = 'T4'
            elif (time == '11:00 - 12:00'):
                timeChanged = 'T5'
            elif (time == '13:00 - 14:00'):
                timeChanged = 'T6'
            elif (time == '15:00 - 16:00'):
                timeChanged = 'T7'
            elif (time == '16:00 - 17:00'):
                timeChanged = 'T8'
            print(timeChanged)
            #apipost
            user = {"doctorId": idDentist, "timeType": timeChanged, "date": dateChanged, "email": email, "fullName": customer, "gender": genderChanged, "service": idService, "phoneNumber": phone, "note": note}
            response = requests.post("http://localhost:8080/api/patient-book-appointment", data = user)
            # print (str(response.content)) == response.text
            user2 = {"doctorId": idDentist, "date": dateChanged, "timeType": timeChanged}
            res = response.json()
            if (res['errCode'] == 0):
                dispatcher.utter_message("?????t l???ch th??nh c??ng")
                response2 = requests.post("http://localhost:8080/api/update-slot-schedule", data = user2)

            elif (res['errCode'] == 1):
                dispatcher.utter_message("?????t l???ch kh??ng th??nh c??ng, vui l??ng ?????t l???i !")
            

        if (book_check == "B??? ?????t l???ch"):
            dispatcher.utter_message("???? hu??? ?????t l???ch")




class AskSlotServiceAction(Action):
    def name(self) -> Text:
        return "action_ask_service"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:

        services = []
        response = requests.get("http://localhost:8080/api/service-chatbot")
        data = response.json()
        for x in data['data']:
            services.append(x['ServiceData']['valueVi'])
        print(services)
        button = []
        gender = tracker.get_slot('gender')
        dispatcher.utter_message(gender + ' vui l??ng cho ch???n d???ch v??? mu???n kh??m')
        for x in services:
            button.append(
                {"title": x, "payload": '/give_service{\"service\": \"' + x + '\"}'})
        dispatcher.utter_button_message(" ", button)
        return []
        # current_service = tracker.get_slot("service")
        # if cancel != None:
        #     dispatcher.utter_message("B???n c?? mu???n tho??t kh??ng")
        #     listcancel = ["C??", "Kh??ng"]
        #     button = []
        #     for x in listcancel:
        #         button.append(
        #             {"title": x, "payload": '/book_cancel{\"cancel\": \"' + x + '\"}'})
        #     dispatcher.utter_button_message(" ", button)

        # if(cancel=="C??"):
        #     return action_deactivate_form


class AskSlotDentistAction(Action):
    def name(self) -> Text:
        return "action_ask_dentist"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:

        dentists = []
        response = requests.get("http://localhost:8080/api/get-all-doctors")
        data = response.json()
        for x in data['data']:
            dentists.append(x['firstName'])
        print(dentists)
        button = []
        gender = tracker.get_slot('gender')
        dispatcher.utter_message(gender + ' vui l??ng cho ch???n nha s?? mu???n kh??m')
        for x in dentists:
            button.append(
                {"title": "" + x, "payload": '/give_dentist{\"dentist\": \"' + x + '\"}'})
        dispatcher.utter_button_message(" ", button)
        return []


class AskSlotTimeAction(Action):
    def name(self) -> Text:
        return "action_ask_time"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        service = tracker.get_slot("service")
        dentist = tracker.get_slot("dentist")

        # layIDnhasi
        response = requests.get("http://localhost:8080/api/get-all-doctors")
        data = response.json()
        for x in data['data']:
            if (x['firstName'] == dentist):
                idDentist = x['id']
        print(idDentist)
        # convert ngay
        date = tracker.get_slot("date")
        date_object = datetime.strptime(date, "%d/%m/%Y")
        print("date_object =", date_object)

        timestamp = datetime.timestamp(date_object)
        dateChanged = str(timestamp).replace(".0", "") + '000'
        print(dateChanged)
        # lay khung gio
        api = 'http://localhost:8080/api/get-schedule-doctor-by-date?doctorId=' + str(
            idDentist) + '&date=' + dateChanged
        response2 = requests.get(api)
        data2 = response2.json()
        arr = []  # listtime
        for x in data2['data']:
            if (x['currentNumber'] != 1):
                arr.append(x['timeTypeData']['valueVi'])
        print(arr)
        if not arr:
            dispatcher.utter_message('Ng??y v???a ch???n kh??ng c?? khung gi??? tr???ng')
            dispatcher.utter_message('Vui l??ng ch???n ng??y kh??c!')
        else:
            dispatcher.utter_message('H??y ch???n th???i gian ?????n kh??m b???nh:')
        button = []
        for x in arr:
            button.append(
                {"title": x, "payload": '/give_time{\"time\": \"' + x + '\"}'})
        dispatcher.utter_button_message(" ", button)

        return []

class AskSlotNoteAction(Action):
    def name(self) -> Text:
        return "action_ask_note"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        gender = tracker.get_slot("gender")
        dispatcher.utter_message(gender + ' c?? l??u ?? g?? kh??ng ???')
        dispatcher.utter_message("N???u c?? l??u ??, vui l??ng nh???p ph??a d?????i")
        select2 = ["Kh??ng"]
        button = []
        for x in select2:
            button.append(
                {"title": x, "payload": '/book_note{\"note\": \"' + x + '\"}'})
        dispatcher.utter_button_message(" ", button)
        return []


class Greet(Action):

    def name(self) -> Text:
        return "rep_greet"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            'D??? ????? ti???n x??ng h??, anh/ch??? vui l??ng ch???n gi??p em danh x??ng m??nh mu???n ???????c g???i nh??:')
        select = ['Anh', 'Ch???']
        button = []
        for x in select:
            button.append(
                {"title": x, "payload": '/get_gender{\"gender\": \"' + x + '\"}'})

        dispatcher.utter_button_message(" ", button)
        return []


class Gender(Action):

    def name(self) -> Text:
        return "rep_get_gender"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        service = tracker.get_slot("gender")
        dispatcher.utter_message(
            'Xin ch??o ' + service + ' ???? ?????n v???i Nha khoa SMILE')
        return []


class Ask(Action):

    def name(self) -> Text:
        return "rep_ask"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        gender = tracker.get_slot("gender")
        dispatcher.utter_message(
            'D??? ' + gender + ' vui l??ng ch???n d???ch v??? m??nh mu???n ???????c t?? v???n ???:')

        services = []
        response = requests.get("http://localhost:8080/api/service-chatbot")
        data = response.json()
        for x in data['data']:
            services.append(x['ServiceData']['valueVi'])
        button = []
        for x in services:
            button.append(
                {"title": x, "payload": '/ask_service{\"service\": \"' + x + '\"}'})
        dispatcher.utter_button_message(" ", button)

        return []


class AskService(Action):

    def name(self) -> Text:
        return "rep_ask_service"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        response = requests.get("http://localhost:8080/api/service-chatbot")
        data = response.json()
        service = tracker.get_slot("service")
        arr = {}
        for x in data['data']:
            arr[x['ServiceData']['valueVi']] = x['description']
        dispatcher.utter_message(arr[service])

        return []


class AskPrice(Action):

    def name(self) -> Text:
        return "rep_ask_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # mydb = con.connect(
        #     host="localhost",
        #     user="root",
        #     password="",
        #     database="chatbot"
        # )
        #
        # mycursor = mydb.cursor()
        # price = tracker.get_slot("price")
        # mycursor.execute(
        #     "SELECT giaDV from dichvu where tenDV ='" + price + "'"
        # )
        # resultSpeciality = [x[0] for x in mycursor.fetchall()]
        # specialityCode = ' '.join(map(str, resultSpeciality))
        # dispatcher.utter_message(specialityCode)

        response = requests.get("http://localhost:8080/api/service-chatbot")
        data = response.json()
        price = tracker.get_slot('price')
        arr = []
        for x in data['data']:
            if (x['ServiceData']['valueVi']) == price:
                arr.append(x['PriceData']['valueVi'])
        dispatcher.utter_message(str(arr[0]))
        return []


class AskTimeToDo(Action):

    def name(self) -> Text:
        return "rep_ask_timetodo"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        response = requests.get("http://localhost:8080/api/service-chatbot")
        data = response.json()
        timetodo = tracker.get_slot('timetodo')
        arr = {}
        for x in data['data']:
            arr[x['ServiceData']['valueVi']] = x['timetodo']
        dispatcher.utter_message(arr[timetodo])

        return []


class AskDoctor(Action):

    def name(self) -> Text:
        return "rep_ask_doctor"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        doctor = tracker.get_slot("doctor")
        response = requests.get("http://localhost:8080/api/get-all-doctors")
        data = response.json()
        id = ''
        for x in data['data']:
            if (x['firstName'] == doctor):
                id += str(x['id'])

        api = 'http://localhost:8080/api/get-detail-doctor-by-id?id=' + id
        response2 = requests.get(api)
        data2 = response2.json()
        # if(data2['data']['Markdown']['description'] == null):
        dispatcher.utter_message(data2['data']['Markdown']['description'])
        return []


class AskListDoctor(Action):

    def name(self) -> Text:
        return "rep_ask_list_doctor"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            'D??? ????y l?? danh s??ch nha s?? c???a ph??ng kh??m ???:')
        dentists = []
        response = requests.get("http://localhost:8080/api/get-all-doctors")
        data = response.json()
        for x in data['data']:
            dentists.append(x['firstName'])
        button = []
        for x in dentists:
            button.append(
                {"title": x, "payload": '/ask_doctor{\"doctor\": \"' + x + '\"}'})
        dispatcher.utter_button_message(" ", button)

        return []
