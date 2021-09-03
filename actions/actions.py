import mysql.connector as con
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, EventType, FollowupAction
import numpy as np
import requests
from datetime import datetime

class booking_form(Action):

    def name(self) -> Text:
        return "booking_form"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> List[EventType]:
        required_slots = ["service", "dentist", "customer", "phone", "email", "date", "time", "note"]


class SaveInfoBook(Action):
    def name(self) -> Text:
        return "save_info_book"

    def run(self, dispatcher, tracker: Tracker,
            domain: Dict):
        service = tracker.get_slot("service")
        dentist = tracker.get_slot("dentist")
        customer = tracker.get_slot("customer")
        phone = tracker.get_slot("phone")
        email = tracker.get_slot("email")
        date = tracker.get_slot("date")
        time = tracker.get_slot("time")
        note = tracker.get_slot("note")
        return [SlotSet("service_booked", service),
                SlotSet("dentist_booked", dentist),
                SlotSet("customer_booked", customer),
                SlotSet("phone_booked", phone),
                SlotSet("email_booked", email),
                SlotSet("date_booked", date),
                SlotSet("time_booked", time),
                SlotSet("note_booked", note)]


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
        # # layIDnhasi
        # gender = tracker.get_slot("gender")
        # dentist = tracker.get_slot("dentist")
        # response = requests.get("http://localhost:8080/api/get-all-doctors")
        # data = response.json()
        # for x in data['data']:
        #     if (x['firstName'] == dentist):
        #         idDentist = x['id']
        # print(idDentist)

        # date = tracker.get_slot("date")
        # date_object = datetime.strptime(date, "%d/%m/%Y")
        # print("date_object =", date_object)

        # timestamp = datetime.timestamp(date_object)
        # dateChanged = str(timestamp).replace(".0", "") + '000'
        # print(dateChanged)
        # ##call api 
        # api = 'http://localhost:8080/api/get-schedule-doctor-by-date?doctorId=' + str(idDentist) + '&date=' + dateChanged
        # response2 = requests.get(api)
        # data2 = response2.json()
        # arr = []  # listtime
        # for x in data2['data']:
        #     if (x['currentNumber'] != 1):
        select = ["Đồng ý đặt lịch", "Bỏ đặt lịch"]
        button = []
        for x in select:
            button.append(
                {"title": x, "payload": '/book_intent{\"book_check\": \"' + x + '\"}'})

        dispatcher.utter_button_message(" ", button)
            # elif (x['currentNumber'] == 1):
            #     api = 'http://localhost:8080/api/get-schedule-doctor-by-date?doctorId=' + str(idDentist) + '&date=' + dateChanged
            #     response2 = requests.get(api)
            #     data2 = response2.json()
            #     arr = []  # listtime
            #     for x in data2['data']:
            #         if (x['currentNumber'] != 1):
            #             arr.append(x['timeTypeData']['valueVi'])
            #     print(arr)
            #     dispatcher.utter_message(text='Xin ' + gender + ' hãy chọn thời gian đến khám bệnh:')
            #     button = []
            #     for x in arr:
            #         button.append(
            #             {"title": x, "payload": '/give_time{\"time\": \"' + x + '\"}'})
            #     dispatcher.utter_button_message(" ", button)
                

        return []


class insert_form_booking(Action):
    def name(self) -> Text:
        return "action_insert_val_form"

    def run(self, dispatcher, tracker: Tracker,
            domain: Dict, ) -> List[Dict[Text, Any]]:

        book_check = tracker.get_slot("book_check")
        print('book check: ', book_check)

        if (book_check == "Đồng ý đặt lịch"):
            service = tracker.get_slot("service")
            dentist = tracker.get_slot("dentist")
            customer = tracker.get_slot("customer")
            phone = tracker.get_slot("phone")
            email = tracker.get_slot("email")
            note = tracker.get_slot("note")
            gender = tracker.get_slot("gender")

            if (gender == 'Anh'):
                genderChanged = 'M'
            elif (gender == 'Chị'):
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
            if (time == '7:00 - 8:00'):
                timeChanged = 'T1'
            elif (time == '8:00 - 9:00'):
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


            api = 'http://localhost:8080/api/get-schedule-doctor-by-date?doctorId=' + str(idDentist) + '&date=' + dateChanged
            response2 = requests.get(api)
            data2 = response2.json()
            for x in data2['data']:
                if (x['currentNumber'] != 1):
                    # apipost
                    user = {"doctorId": idDentist, "fullName": customer, "phoneNumber": phone, "timeType": timeChanged,
                            "date": dateChanged, "email": email, "gender": genderChanged, "service": idService, "note": note}
                    response = requests.post("http://localhost:8080/api/patient-book-appointment", data=user)
                    # print (str(response.content)) == response.text
                    user2 = {"doctorId": idDentist, "timeType": timeChanged, "date": dateChanged}
                    res = response.json()
                    if (res['errCode'] == 0):
                        dispatcher.utter_message(gender + customer + ' đã đặt lịch thành công.')
                        dispatcher.utter_message('Hẹn gặp lại '+ gender + ' tại nha khoa Smile.')
                        response2 = requests.post("http://localhost:8080/api/update-slot-schedule", data=user2)
                        return [SlotSet("service", None),
                                SlotSet("dentist", None),
                                SlotSet("customer", None),
                                SlotSet("phone", None),
                                SlotSet("email", None),
                                SlotSet("date", None),
                                SlotSet("time", None),
                                SlotSet("note", None),
                                SlotSet("book_check", None),
                                ]
                    elif (res['errCode'] == 1):
                        dispatcher.utter_message('Đã xảy ra sự cố, Quý khách vui lòng đặt lịch lại')
                elif (x['currentNumber'] == 1):
                    SlotSet("time", None)
                    api3 = 'http://localhost:8080/api/get-schedule-doctor-by-date?doctorId=' + str(idDentist) + '&date=' + dateChanged
                    response3 = requests.get(api3)
                    data3 = response3.json()
                    arr2 = []  # listtime
                    for x in data3['data']:
                        if (x['currentNumber'] != 1):
                            arr2.append(x['timeTypeData']['valueVi'])
                    print(arr2)
                    dispatcher.utter_message('Khung giờ ' + gender + ' chọn đã có người đặt!')
                    dispatcher.utter_message(gender + ' vui lòng chọn khung giờ khác:')
                    button = []
                    for x in arr2:
                        button.append(
                            {"title": x, "payload": '/give_time{\"time\": \"' + x + '\"}'})
                    dispatcher.utter_button_message(" ", button)

                    time = tracker.get_slot("time")
                    if (time == '7:00 - 8:00'):
                        timeChanged = 'T1'
                    elif (time == '8:00 - 9:00'):
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

                    # apipost
                    user3 = {"doctorId": idDentist, "fullName": customer, "phoneNumber": phone, "timeType": timeChanged,
                            "date": dateChanged, "email": email, "gender": genderChanged, "service": idService, "note": note}
                    response3 = requests.post("http://localhost:8080/api/patient-book-appointment", data=user3)
                    # print (str(response.content)) == response.text
                    user4 = {"doctorId": idDentist, "timeType": timeChanged, "date": dateChanged}
                    res = response3.json()
                    if (res['errCode'] == 0):
                        dispatcher.utter_message(gender + ' ' + customer + ' đã đặt lịch thành công.')
                        dispatcher.utter_message('Hẹn gặp lại '+ gender + ' tại nha khoa Smile.')
                        response4 = requests.post("http://localhost:8080/api/update-slot-schedule", data=user4)
                        return [SlotSet("service", None),
                                SlotSet("dentist", None),
                                SlotSet("customer", None),
                                SlotSet("phone", None),
                                SlotSet("email", None),
                                SlotSet("date", None),
                                SlotSet("time", None),
                                SlotSet("note", None),
                                SlotSet("book_check", None),
                                ]
                    elif (res['errCode'] == 1):
                        dispatcher.utter_message('Đã xảy ra sự cố, Quý khách vui lòng đặt lịch lại')

        if (book_check == "Bỏ đặt lịch"):
            dispatcher.utter_message("Đã huỷ đặt lịch thành công")
            dispatcher.utter_message('Hẹn gặp lại ' + gender)
            return [SlotSet("service", None),
                    SlotSet("dentist", None),
                    SlotSet("customer", None),
                    SlotSet("phone", None),
                    SlotSet("email", None),
                    SlotSet("date", None),
                    SlotSet("time", None),
                    SlotSet("note", None),
                    SlotSet("book_check", None),
                    ]


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
        dispatcher.utter_message(gender + ' vui lòng cho chọn dịch vụ muốn khám')
        for x in services:
            button.append(
                {"title": x, "payload": '/give_service{\"service\": \"' + x + '\"}'})
        dispatcher.utter_button_message(" ", button)
        return []


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
        dispatcher.utter_message(gender + ' vui lòng cho chọn nha sĩ muốn khám')
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
        dispatcher.utter_message(text="Hãy chọn thời gian đến khám bệnh:")
        button = []
        for x in arr:
            button.append(
                {"title": x, "payload": '/give_time{\"time\": \"' + x + '\"}'})
        dispatcher.utter_button_message(" ", button)

        return []

class Greet(Action):

    def name(self) -> Text:
        return "rep_greet"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            'Dạ để tiện xưng hô, anh/chị vui lòng chọn giúp em danh xưng mình muốn được gọi nhé:')
        select = ['Anh', 'Chị']
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
            'Xin chào ' + service + ' đã đến với Nha khoa SMILE')
        return []


class Ask(Action):

    def name(self) -> Text:
        return "rep_ask"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        gender = tracker.get_slot("gender")
        dispatcher.utter_message(
            'Dạ ' + gender + ' vui lòng chọn dịch vụ mình muốn được tư vấn ạ:')

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

        api = 'http://localhost:8080/api/get-detail-doctor-by-id?id=' + id;
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
            'Dạ đây là danh sách nha sĩ của phòng khám ạ:')
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
