# -*- coding: UTF-8 -*-
from .models import MockItem, MockCondition, MockSlot, MockLog
import json

__author__ = 'sun_yang'


# -----------GET CONTROLLER-----------


def get_mock_item_list_control(url=None):
    if url:
        try:
            items = MockItem.objects.filter(url=url)
            if len(items) > 0:
                return 1, items
            else:
                return 0, items
        except:
            return 0, ""
    else:
        response = {}
        try:
            items = MockItem.objects.all()
            item_data_list = []
            for i in items:
                temp = {'url': i.url, 'desc': i.desc, 'id': i.id}
                item_data_list.append(temp)
            response["code"] = 0
            data = {"item_list": item_data_list}
            response["data"] = data
        except Exception as e:
            response = process_error_value(e, 1001)
        return response


def get_mock_detail(item_id):
    response = {}
    try:
        item = MockItem.objects.get(id=item_id)

        slots = MockSlot.objects.filter(mockItem=item)
        item_data = {"activeType": item.activeType,
                     "redirect": item.redirect,
                     "finalTarget": item.finalTarget,
                     "desc": item.desc,
                     "url": item.url,
                     "id": item.id}
        slots_data = []
        if len(slots) >= 1:
            for s in slots:
                slots_data.append(get_mock_slot_data(s.id))
            item_data["slots"] = slots_data
        else:
            item_data["slots"] = []
        response["code"] = 0
        response["data"] = item_data
    except MockSlot.DoesNotExist as e:
        response = process_error_value(e, 1002)
    except Exception as e:
        response = process_error_value(e, 1001)
    return response


def get_mock_slot_data(slot_id):
    slot = MockSlot.objects.get(id=slot_id)
    conditions = MockCondition.objects.filter(mockSlot=slot)
    slot_data = {"id": slot.id,
                 "value": slot.value,
                 "desc": slot.desc,
                 "compMethod": slot.compMethod}
    conditions_data = []
    if len(conditions) >= 1:
        for c in conditions:
            conditions_data.append({"key": c.key, "value": c.value, "compFunc": c.compFunc, "id": c.id})
        slot_data["conditions"] = conditions_data
    else:
        slot_data["conditions"] = []
    return slot_data


def get_mock_slot(slot_id):
    response = {}
    try:
        response["code"] = 0
        response["data"] = get_mock_slot_data(slot_id)
    except Exception as e:
        response = process_error_value(e, 1001)
    return response


# -----------ADD CONTROLLER -----------


def add_condition(key, value, compFunc, slot_id):
    response = {}
    try:
        condition = MockCondition()
        condition.key = key
        condition.compFunc = compFunc
        condition.value = value
        condition.mockSlot = MockSlot.objects.get(id=slot_id)
        condition.save()
        response["code"] = 0
        response["data"] = {}
    except Exception as e:
        response = process_error_value(e, 1001)
    return response


def add_slot(value, comp, item_id, conditions, desc):
    response = {}
    try:
        slot = MockSlot()
        slot.value = value
        slot.compMethod = comp
        slot.desc = desc
        slot.mockItem = MockItem.objects.get(id=item_id)
        slot.save()
        conds = tools.json_loads_byteified(conditions)
        for condition_dic in conds:
            key = condition_dic["key"]
            value = condition_dic["value"]
            compFunc = condition_dic["compFunc"]
            add_condition(key, value, compFunc, slot.id)
        response["code"] = 0
        response["data"] = {}
    except Exception as e:
        response = process_error_value(e, 1001)
    return response


def add_item(activeType, redirect, finalTarget, desc, url):
    response = {}
    try:
        item = MockItem()
        item.activeType = activeType
        item.redirect = redirect
        item.finalTarget = finalTarget
        item.desc = desc
        item.url = url
        item.save()
        response["code"] = 0
        response["data"] = {}
    except Exception as e:
        response = process_error_value(e, 1001)
    return response

# -----------DELETE CONTROLLER-----------


def delete_condition(condition_id):
    response = {}
    try:
        MockCondition.objects.get(id=condition_id).delete()
        response["code"] = 0
        response["data"] = {}
    except Exception as e:
        response = process_error_value(e, 1001)
    return response


def delete_slot(slot_id):
    response = {}
    try:
        MockSlot.objects.get(id=slot_id).delete()
        response["code"] = 0
        response["data"] = {}
    except Exception as e:
        response = process_error_value(e, 1001)
    return response


def delete_item(item_id):
    response = {}
    try:
        MockCondition.objects.get(id=item_id).delete()
        response["code"] = 0
        response["data"] = {}
    except Exception as e:
        response = process_error_value(e, 1001)
    return response


# -----------UPDATE CONTROLLER-----------


def update_condition(key, value, compFunc, solt_id,condition_id):
    response = {}
    try:
        condition = MockCondition.objects.get(id=condition_id)
        condition.key = key
        condition.compFunc = compFunc
        condition.value = value
        condition.mockSlot = MockSlot.objects.get(id=solt_id)
        condition.save()
        response["code"] = 0
        response["data"] = {}
    except Exception as e:
        response = process_error_value(e, 1001)
    return response


def update_slot(value, comp, item_id, slot_id, conditions):
    response = {}
    try:
        slot = MockSlot.objects.get(id=slot_id)
        slot.value = value
        slot.compMethod = comp
        slot.mockItem = MockItem.objects.get(id=item_id)
        slot.save()
        desc = ""
        for c in conditions:
            condition = MockCondition.objects.get(id=c)
            condition.mockSlot = slot
            condition.save()
            desc += condition.key + condition.compFunc + condition.value + "|"
        response["code"] = 0
        response["data"] = {}
    except Exception as e:
        response = process_error_value(e, 1001)
    return response


def update_item(activeType, redirect, finalTarget, desc, url, item_id, slots):
    response = {}
    try:
        item = MockItem.objects.get(id=item_id)
        item.activeType = activeType
        item.redirect = redirect
        item.finalTarget = finalTarget
        item.desc = desc
        item.url = url
        item.save()
        for s in slots:
            slot = MockSlot.objects.get(id=s)
            slot.mockItem = item
            slot.save()
        response["code"] = 0
        response["data"] = {}
    except Exception as e:
        response = process_error_value(e, 1001)
    return response

# -----------ERROR HANDLE-----------


def process_error_value(e, code):
    return {"code": code, "data":{"error_msg": str(e)}}

# Mocker logic


def save_mock_log(log_url, log_activetype, log_method, log_request, log_response, log_time_req, log_time_resp):
    log_item = MockLog()
    log_item.url = log_url
    log_item.active_type = log_activetype
    log_item.method = log_method
    log_item.request = log_request
    log_item.response = log_response
    log_item.time_request = log_time_req
    log_item.time_response = log_time_resp
    log_item.save()
    pass


def do_redirect(mock_url):
    print('-------' + mock_url + '-------')
    (items_status, items) = get_mock_item_list_control(mock_url)
    if items_status:
        item = items[0]
        print('redirect is')
        print(item.redirect)
        return 1, item.redirect
    else:
        return 3, "un_setting"


# code = 0, result = json
# code = 1, result = redirect url
# code = 2, result = mock setting error
# code = 3, result = unsetting
def do_mock(mock_url, parameters):
    (items_status, items) = get_mock_item_list_control(mock_url)
    if items_status:
        item = items[0]
        if item.activeType:
            mock_slots = MockSlot.objects.filter(mockItem=item)
            for slot in mock_slots:
                if hit_slot(slot, parameters):
                    print('Go to Mock')
                    return 0, tools.json_loads_byteified(slot.value)
            if len(item.finalTarget) > 0:
                print('Go to Final Target')
                return 1, item.finalTarget
            else:
                return 4, "internal error"
        else:
            if item.redirect:
                print('Go to Redirect')
                return 1, item.redirect
            else:
                return 3, "un_setting"

    else:
        return 3, "un_setting"


def hit_slot(slot, parameters):
    if not slot.active:
        return False
    mock_conditions = MockCondition.objects.filter(mockSlot=slot)
    if slot.compMethod:
        for condition in mock_conditions:
            if not hit_condition(condition, parameters):
                return False
    else:
        for condition in mock_conditions:
            if hit_condition(condition, parameters):
                return True
        return False


def hit_condition(condition, parameters):
    condition_key = condition.key
    condition_value = condition.value

    temp_obj = parameters.copy()
    key_parts = condition_key.split('.')
    for i in range(0, len(key_parts)):
        current_key = key_parts[i]
        if current_key in temp_obj.keys():
            temp_obj = temp_obj[current_key]
            if i is len(key_parts) - 1:
                return handle_value(condition, temp_obj, condition_value)
            if not isinstance(temp_obj, dict):
                return False
        else:
            return False
    return False


def dict_get(dic, obj_key, de_value):
    temp = dic
    for k, v in temp.items():
        if k == obj_key:
            return v
        else:
            if isinstance(v, dict):
                ret = dict_get(dic=v, obj_key=obj_key, de_value=de_value)
                if ret is not de_value:
                    return ret
    return de_value


def handle_value(condition, value1, value2):
    if condition.compFunc == '==':
        return value2 == value1
    elif condition.compFunc == '>':
        return value2 > value1
    elif condition.value2 == '<':
        return value2 < value1
    elif condition.compFunc == '<=':
        return value2 <= value1
    elif condition.compFunc == '>=':
        return value2 >= value1
    else:
        return False


# ----------- MOCK Tool --------------
def report_mock(view_process, func_url):
    response = empty_success_response()
    try:
        report_item = MockReport()
        view_process_json_string = json.dumps(view_process)
        func_url_string = ','.join(func_url)
        report_item.ViewProcesses = view_process_json_string
        report_item.FuncUrl = func_url_string
        report_item.ReportTime = tools.get_current_time()
        report_item.save()
    except Exception as e:
        response = process_error_value(e, 1001)
    return response


def query_mock_log(func):
    result_data = empty_success_response()
    try:
        log_list = MockLog.objects.all()
        temp_arr = []
        wrong_code = ''

        for log in log_list:
            request_string = log.request.replace('\'', '\"').replace('\\n', '').replace('\"{', '{').replace('}\"', '}')
            try:
                request = json.loads(request_string)
                func_string = request['func']
                if func_string == func:
                    response_string = log.response.encode('utf-8')
                    response_string = response_string.replace('\'', '\"')
                    response_string = response_string.replace('\\n', '')
                    response_string = response_string.replace('\"{', '{')
                    response_string = response_string.replace('}\"', '}')
                    response_string = response_string.decode('utf-8')
                    # print(response_string)
                    try:
                        response = json.loads(response_string)
                        print(response)
                        code = response['code']
                        if code == 0:
                            print("Got it")
                            temp_dict = {'request': log.request,
                                         'response': log.response,
                                         'type': log.active_type}
                            temp_arr.append(temp_dict)
                        else:
                            wrong_code = '存在Code不为0'
                    except Exception as e:
                        print(" ")
                        print('Response error is ' + str(e))
            except Exception as e:
                print("Request error is " + str(e))
                # print(request_string)
                continue
        result_data['data']['log_list'] = temp_arr
        result_data['data']['error_reason'] = wrong_code
    except Exception as e:
        result_data = process_error_value(e, 1001)
    return result_data


def empty_success_response():
    return {'code': 0,
            'data': {}}
