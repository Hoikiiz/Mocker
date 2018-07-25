from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt

from . import controllers
from . import tools
import requests
import json
from rest_framework import viewsets
from .serializers import MockConditionSerializer, MockItemSerializer, MockSlotSerializer
from .models import MockItem, MockSlot, MockCondition


own_func_list = ['reportMock',
                 'mockitemlist']


# mock API

class MockItemViewSet(viewsets.ModelViewSet):
    queryset = MockItem.objects.all()
    serializer_class = MockItemSerializer


class MockSlotViewSet(viewsets.ModelViewSet):
    queryset = MockSlot.objects.all()
    serializer_class = MockSlotSerializer


class MockConditionViewSet(viewsets.ModelViewSet):
    queryset = MockCondition.objects.all()
    serializer_class = MockConditionSerializer


# mock process

def index(request):
    return HttpResponse("Welcome to mocker")


@csrf_exempt
def report_mock(request):
    if request.method == 'POST':
        json_body = handle_request(request)
        view_process = json_body['ViewProcesses']
        func_url = json_body['FuncUrl']
        response_json = controllers.report_mock(view_process=view_process, func_url=func_url)
        return JsonResponse(response_json)
    else:
        return Http404()


@csrf_exempt
def query_logs(request):
    if request.method == 'POST':
        json_body = handle_request(request)
        func_string = json_body['func']
        response_json = controllers.query_mock_log(func_string)
        return JsonResponse(response_json)
    else:
        return Http404()


def handle_request(request):
    print("=====Request=====")
    print(request.body)
    json_body = tools.json_loads_byteified(request.body)
    print(json_body)
    return json_body


@csrf_exempt
def redirector(request):
    mock_url = request.path_info
    temp = '/mocker/redirect/'
    print('Begin Redirect!!!!')
    date_begin = tools.get_current_time()
    print('--------' + mock_url)
    mock_url = mock_url[len(temp):]
    (status, result) = controllers.do_redirect(mock_url)
    if status == 1:
        if request.method == 'POST':
            content_type = request.META['CONTENT_TYPE']
            print(content_type)
            if content_type == 'application/json':
                request_post = tools.json_loads_byteified(request.body)
            elif content_type == 'application/x-www-form-urlencoded':
                request_post = tools.json_loads_byteified(json.dumps(request.POST))
            else:
                return JsonResponse(response_404())
            print('Request post is')
            print(request_post)
            r = requests.post(result+'/'+mock_url, data=request_post)
            controllers.save_mock_log(mock_url, 'Redirect', 'POST', request_post, tools.json_loads_byteified(r.text), date_begin, tools.get_current_time())
            json_result = tools.json_loads_byteified(r.text)
            json_result["active_type"] = "Redirect"
            return JsonResponse(json_result)
        elif request.method == 'GET':
            r = requests.get(result+'/'+mock_url, params=request.GET)
            controllers.save_mock_log(mock_url, 'Redirect', 'GET', request.GET, tools.json_loads_byteified(r.text), date_begin, tools.get_current_time())
            json_result = tools.json_loads_byteified(r.text)
            json_result["active_type"] = "Redirect"
            return JsonResponse(json_result)
    else:
        return response_404()



@csrf_exempt
def mocker(request, mock_url):
    print("Begin Mocker!!!!")
    date_begin = tools.get_current_time()
    if request.method == 'POST':
        print('===========================')
        print('MOCK POST ' + mock_url)

        content_type = request.META['CONTENT_TYPE']
        print(content_type)
        if content_type == 'application/json':
            request_post = tools.json_loads_byteified(request.body)
        elif content_type == 'application/x-www-form-urlencoded':
            request_post = tools.json_loads_byteified(json.dumps(request.POST))
        else:
            return JsonResponse(response_404())

        print('Request Body:')
        print(request_post)

        # Handle GET parameters
        # if request.GET:
        #     for o in request.GET.items():
        #         print(o)
        #     request_post = dict(request_post.items() + request.GET.items())

        # White List
        if 'func' in request_post.keys():
            func = request_post['func']
            if func == 'reportMock':
                request_params_string = request_post['params']
                request_params = tools.json_loads_byteified(request_params_string)
                print(request_params)
                view_process = request_params['ViewProcesses']
                func_url = request_params['FuncUrl']
                response_json = controllers.report_mock(view_process=view_process, func_url=func_url)
                return JsonResponse(response_json)

        (status, result) = controllers.do_mock(mock_url, request_post)
        if status == 0:
            controllers.save_mock_log(mock_url, 'Mock', 'POST', request_post, result, date_begin, tools.get_current_time())
            result["active_type"] = "Mock"
            return JsonResponse(result)
        elif status == 1:
            r = requests.post(result+'/'+mock_url, data=request_post)
            print('*****************')
            print(r.text)
            controllers.save_mock_log(mock_url, 'Redirect', 'POST', request_post, r.text, date_begin, tools.get_current_time())
            # json_result = tools.json_loads_byteified(r.text)
            json_result = json.loads(r.text)
            json_result["active_type"] = "Redirect"
            return JsonResponse(json_result)
        else:
            controllers.save_mock_log(mock_url, '404', 'POST', request_post, result, date_begin, tools.get_current_time())
            return JsonResponse(response_404())
    elif request.method == 'GET':
        print('===========================')
        print('MOCK GET ' + mock_url)
        print('Request Query String:')
        print(request.GET)
        (status, result) = controllers.do_mock(mock_url, request.GET)
        if status == 0:
            controllers.save_mock_log(mock_url, 'Mock', 'GET', request.GET, result, date_begin, tools.get_current_time())
            result["active_type"] = "Mock"
            return JsonResponse(result)
        elif status == 1:
            r = requests.get(result+'/'+mock_url, params=request.GET)
            controllers.save_mock_log(mock_url, 'Redirect', 'GET', request.GET, r.text, date_begin, tools.get_current_time())
            json_result = tools.json_loads_byteified(r.text)
            json_result["active_type"] = "Redirect"
            return JsonResponse(json_result)
        else:
            controllers.save_mock_log(mock_url, '404', 'GET', request.GET, result, date_begin, tools.get_current_time())
            return JsonResponse(response_404())
    else:
        return JsonResponse(response_404())


def response_404():
    ret_value = {'code': 404, 'message': 'Unrecognized Protocol'}
    return ret_value
