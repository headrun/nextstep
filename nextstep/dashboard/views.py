import datetime
import traceback
from django.shortcuts import render
from common.utils import getHttpResponse as HttpResponse
from models import *
from django.views.decorators.csrf import csrf_exempt
from auth.decorators import loginRequired
#from file_import import *
from xlrd import open_workbook
import xlrd
from xlrd import open_workbook
from xlwt import Workbook, easyxf, XFStyle
import xlsxwriter
from src import *
from django.db.models import Sum
import redis


SOH_XL_HEADERS = ['Date', 'ID','Done','Passed / Cancelled','Platform','Emp id','Week','Month','Year','Target','Productivity','WC','WorkPacket']
SOH_XL_MAN_HEADERS = ['Date', 'Done','Platform','Emp id','Target']
customer_data = {}


# Create your views here.
@loginRequired
def last_week_stats(request):
    date_list = Productivity.objects.values_list('date').distinct()
    final_data = []
    date_data = []
    product_data = []
    for date_li in date_list:
        #date_data.append(str(date_li[0]))
        date_data.append(str(date_li[0].date()))
        productivity_list = Productivity.objects.filter(date=date_li[0]).values_list('value')
        total = 0
        for i in productivity_list:
            total = total+i[0]
        product_data.append(total)
    final_data.append({'date':date_data,'total':product_data})
    return HttpResponse(final_data)

@loginRequired
def last_week_stats_elaborate(request):
    product = []
    productivity_list = Productivity.objects.all()
    for productivity in productivity_list:
        agent   = str(productivity.agent)
        productivity_type = productivity.productivity_type
        per_day = productivity.value
        date    = str(productivity.date)
        product.append({'agent':agent,'productivity_type':productivity_type,'per_day':per_day,'date':date})
    return HttpResponse(product)

def persons_last_week_stats(request):
    persons_list = Productivity.objects.values_list('agent').distinct()
    final_data = []
    persons_data = []
    #date_data = []
    #value_data = []
    for person in persons_list : 
        #import pdb;pdb.set_trace()
        persons_data.append(str(person[0]))
        person_values_list = Productivity.objects.filter(agent=person[0]).values_list('value')
        person_dates_list = Productivity.objects.filter(agent=person[0]).values_list('date')
        person_dict={}
        for date,value in zip(person_dates_list,person_values_list):
            person_dict[str(date[0].date())]=value[0]
        agent_id = Agent.objects.filter(id=person[0]).values_list('name')[0][0]
        user_name = User.objects.filter(id=agent_id).values_list('username')[0][0]
        final_data.append({user_name:person_dict})
    return HttpResponse(final_data)

def final_data(request):
    var = request
    return HttpResponse(var)

def dashboard_insert(request):
    """
    loggedin_user = User.objects.filter(id=request.user.id)[0]
    loggedin_role = request.user.groups.values_list('name')[0][0]
    if loggedin_role == 'Agent':
        k=Agent.objects.filter(name_id=request.user.id).values_list('id')[0][0]
        prj_obj = Project.objects.filter(agent=k)[0]
        #prj_name = Project.objects.filter(agent=k).values_list('project_name')[0][0]
        #import pdb;pdb.set_trace() 
    prj_name = prj_obj.project_name
    data_dict = {}
    dates_list = RawTable.objects.values_list('date').distinct()
    all_dates = []
    for date in dates_list:
        part_date = str(date[0].date())
        #data_dict[part_date] = {}
        all_dates.append(part_date)
        volumes_list = RawTable.objects.filter(date=date[0]).values_list('volume_type').distinct()
        for volume in volumes_list:
            value_dict = {}
            redis_key = '{0}_{1}_{2}'.format(prj_name,volume[0],part_date)
            total = RawTable.objects.filter(volume_type=volume[0],date=date[0]).values_list('per_day').aggregate(Sum('per_day'))
            #data_dict[part_date][volume[0]]= int(total['per_day__sum'])
            value_dict[str(volume[0])] = str(total['per_day__sum'])
            data_dict[redis_key] = value_dict
    #import pdb;pdb.set_trace()
    print data_dict,all_dates

    conn = redis.Redis(host="localhost", port=6379, db=0)
    current_keys = []
    for key,value in data_dict.iteritems():
        current_keys.append(key)
        conn.hmset(key,value)
    """


    dates_list = RawTable.objects.values_list('date').distinct()
    all_dates = []
    for date in dates_list:
        part_date = str(date[0].date())
        all_dates.append(part_date)

    conn = redis.Redis(host="localhost", port=6379, db=0)
    result = {}
    volumes_dict = {}
    date_values = {}
    for date in all_dates:
        date_pattern = '*{0}*'.format(date)
        key_list = conn.keys(pattern=date_pattern)
        for cur_key in key_list:
            var = conn.hgetall(cur_key)
            for key,value in var.iteritems():
                if date_values.has_key(key):
                    date_values[key].append(int(value))
                else:
                    date_values[key]=[int(value)]
    volumes_dict['data'] = date_values
    volumes_dict['date'] = all_dates

    result['data'] = volumes_dict 
    print result
    var = final_data(result)
    return HttpResponse(result)

@loginRequired
def dashboard(request):
    result = {}
    volumes_dict = {}
    conn = redis.Redis(host="localhost", port=6379, db=0)
    keys = conn.keys()
    result['date']=keys
    for key in keys:
        var = conn.hgetall(key)
        for key,value in var.iteritems():
            if volumes_dict.has_key(key):
                volumes_dict[key].append(int(value))
            else:
                volumes_dict[key]=[int(value)]
    result['data'] = volumes_dict
    return HttpResponse(result)

def get_order_of_headers(open_sheet, Default_Headers, mandatory_fileds=[]):
    indexes, sheet_indexes = {}, {}
    sheet_headers = open_sheet.row_values(0)
    lower_sheet_headers = [i.lower() for i in sheet_headers]
    if not mandatory_fileds:
        mandatory_fileds = Default_Headers

    max_index = len(sheet_headers)
    is_mandatory_available = set([i.lower() for i in mandatory_fileds]) - set([j.lower() for j in sheet_headers])
    for ind, val in enumerate(Default_Headers):
        val = val.lower()
        if val in lower_sheet_headers:
            ind_sheet = lower_sheet_headers.index(val)
            sheet_indexes.update({val: ind_sheet})
        else:
            ind_sheet = max_index
            max_index += 1
        #comparing with lower case for case insensitive
        #Change the code as declare *_XL_HEADEERS and *_XL_MAN_HEADERS
        indexes.update({val: ind_sheet})
    return is_mandatory_available, sheet_indexes, indexes


def validate_sheet(open_sheet, request):
    sheet_headers = []
    #brand_channels = bran_chan_func(request)
    if open_sheet.nrows > 0:
        is_mandatory_available, sheet_headers, all_headers = get_order_of_headers(open_sheet, SOH_XL_HEADERS, SOH_XL_MAN_HEADERS)
        sheet_headers = sorted(sheet_headers.items(), key=lambda x: x[1])
        all_headers = sorted(all_headers.items(), key=lambda x: x[1])
        if is_mandatory_available:
            status = ["Fields are not available: %s" % (", ".join(list(is_mandatory_available)))]
            index_status.update({1: status})
            return "Failed", status
    else:
        status = "Number of Rows: %s" % (str(open_sheet.nrows))
        index_status.update({1: status})
    return sheet_headers

def get_cell_data(open_sheet, row_idx, col_idx):
    try:
        cell_data = open_sheet.cell(row_idx, col_idx).value
        cell_data = str(cell_data)
        if isinstance(cell_data, str):
            cell_data = cell_data.strip()
    except IndexError:
        cell_data = ''
    return cell_data

def bulk_update(request,user,project_obj):
    name   = request.get('emp_id')
    target = int(float(request.get('target')))
    done_target = int(float(request.get('cmplt_target')))
    volume = request.get('volume_type')
    date = request.get('date')
    #import pdb;pdb.set_trace()
    volume_dict = {'DataDownload':'DD', 'CompanyCoordinates':'CC' , 'DetailFinancial':'DF'}
    if volume in volume_dict.keys():
        volume = volume_dict[volume]
    new_can = RawTable(project=project_obj, employee=name, volume_type=volume, per_hour=0, per_day=done_target, date=date, norm=target)
    #import pdb;pdb.set_trace()
    try:
        new_can.save()
    except:
        traceback.print_exc()
        return 'Duplicate Record'

    return 'Candidate added'

def redis_insert(request):
    loggedin_user = User.objects.filter(id=request.user.id)[0]
    loggedin_role = request.user.groups.values_list('name')[0][0]
    if loggedin_role == 'Agent':
        k=Agent.objects.filter(name_id=request.user.id).values_list('id')[0][0]
        prj_obj = Project.objects.filter(agent=k)[0]
        #prj_name = Project.objects.filter(agent=k).values_list('project_name')[0][0]
        #import pdb;pdb.set_trace() 
    prj_name = prj_obj.project_name
    data_dict = {}
    dates_list = RawTable.objects.values_list('date').distinct()
    all_dates = []
    for date in dates_list:
        part_date = str(date[0].date())
        #data_dict[part_date] = {}
        all_dates.append(part_date)
        volumes_list = RawTable.objects.filter(date=date[0]).values_list('volume_type').distinct()
        for volume in volumes_list:
            value_dict = {}
            redis_key = '{0}_{1}_{2}'.format(prj_name,volume[0],part_date)
            total = RawTable.objects.filter(volume_type=volume[0],date=date[0]).values_list('per_day').aggregate(Sum('per_day'))
            #data_dict[part_date][volume[0]]= int(total['per_day__sum'])
            value_dict[str(volume[0])] = str(total['per_day__sum'])
            data_dict[redis_key] = value_dict
    #import pdb;pdb.set_trace()
    print data_dict,all_dates

    conn = redis.Redis(host="localhost", port=6379, db=0)
    current_keys = []
    for key,value in data_dict.iteritems():
        current_keys.append(key)
        conn.hmset(key,value)




def upload(request):
    loggedin_user = User.objects.filter(id=request.user.id)[0]
    loggedin_role = request.user.groups.values_list('name')[0][0]
    if loggedin_role == 'Agent':
        k=Agent.objects.filter(name_id=request.user.id).values_list('id')[0][0]
        prj_obj = Project.objects.filter(agent=k)[0]
        #prj_name = Project.objects.filter(agent=k).values_list('project_name')[0][0]
        #import pdb;pdb.set_trace()
    fname = request.FILES['myfile']
    var = fname.name.split('.')[-1].lower()
    if var not in ['xls', 'xlsx', 'xlsb']:
        return HttpResponse("Invalid File")
    else:
        try:
            open_book = open_workbook(filename=None, file_contents=fname.read())
            open_sheet = open_book.sheet_by_index(0)
        except:
            return HttpResponse("Invalid File")
        sheet_headers = validate_sheet(open_sheet, request)
        for row_idx in range(1, open_sheet.nrows):
            for column, col_idx in sheet_headers:
                cell_data = get_cell_data(open_sheet, row_idx, col_idx)
                if column == 'done':
                    customer_data['cmplt_target'] = ''.join(cell_data)
                if column == 'platform':
                    customer_data['volume_type'] = ''.join(cell_data)
                if column == 'emp id':
                    customer_data['emp_id'] = ''.join(cell_data)
                if column == 'target':
                    customer_data['target'] = ''.join(cell_data)
                if column == 'date':
                    cell_data = xlrd.xldate_as_tuple(int(cell_data.split('.')[0]), 0)
                    cell_data ='%s-%s-%s' % (cell_data[0], cell_data[1], cell_data[2])
                    customer_data['date'] = ''.join(cell_data)
            var = bulk_update(customer_data,loggedin_user,prj_obj)
        #insert = dashboard_insert('hai',loggedin_user,loggedin_role,prj_obj)
        insert = redis_insert(request)
    return HttpResponse(var)
