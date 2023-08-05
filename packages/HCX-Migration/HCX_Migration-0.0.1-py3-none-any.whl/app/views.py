# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse,JsonResponse
from django import template

import pandas as pd
import sqlite3

from unipath import Path
from .functions import Executors


BASE_DIR = Path(__file__).parent.parent

def get_data_from_query(query,conn):
    cursor = conn.execute(query)
    columns = [column[0] for column in cursor.description]
    return pd.DataFrame([dict(zip(columns, row)) for row in cursor.fetchall() ])

@login_required(login_url="/login/")
def index(request):
    
    context = {}
    context['segment'] = 'index'

    html_template = loader.get_template( 'dashboard.html' )
    #html_template = loader.get_template( 'index.html' )
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        
        load_template      = request.path.split('/')[-1]
        context['segment'] = load_template
        
        html_template = loader.get_template( load_template )
        return HttpResponse(html_template.render(context, request))
        
    except template.TemplateDoesNotExist:

        html_template = loader.get_template( 'page-404.html' )
        return HttpResponse(html_template.render(context, request))

    except:
    
        html_template = loader.get_template( 'page-500.html' )
        return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def premigration(request):
    context = {}
    context['segment'] = 'premigration'
    page = request.path.split('/')[-1]
    context['page'] = page
    context['upload'] = 0
    classes = 'table table-centered table-nowrap mb-0 rounded'
    formatters = {'thead':[('class','thead-light')]}
    if page == 'generate':
        if request.is_ajax():
            #print(list(request.POST.values()))
            if 'movegroup' in request.POST and "vm_data[0][name]" in request.POST:
                # print(request.POST)
                # Create a Move Group with VMs
                mvid = Executors().insert_to_database(request.POST)
                return JsonResponse({'MoveGroup':mvid},safe=True)
            if 'runid' in request.POST and 'movegroup' in request.POST:
                print("runid is################",request.POST['runid'])
                # Execute the Pre Migration Checkup                
                Executors().execute_powershell(migration='Pre',movegroup=request.POST['movegroup'],runid=request.POST['runid'],avs=1)                
                return JsonResponse({'Execution':True},safe=True)
            if 'runid' in request.POST and 'func' in request.POST:
                #print("QQQQQQQQQQQQ")
                # Getting the status of the Migration Checkup
                status = Executors().select_from_database(report="Pre",procedure='status',runid=request.POST['runid'])
                #print("current status is",status)
                return JsonResponse( ( status[0] if status else status),safe=False)
            if 'formFile' in request.FILES:
                vm_res = [ {'VM NAME': line.decode('utf-8').replace('\r', '').replace('\n',''),'VM Tools Upgrade': '<input type="checkbox" class="form-check-input" name="vmtools[]" value="0">','Hardware Version Upgrade':'<input type="checkbox" class="form-check-input" name="hardware[]" value="0">','MAC Retain':'<input type="checkbox" class="form-check-input" name="mac[]" value="0">'} for line in request.FILES['formFile'] ]
                df = pd.DataFrame(vm_res)
                df = df[['VM NAME','VM Tools Upgrade','Hardware Version Upgrade','MAC Retain']]
                table = df.to_html(classes=classes,index=False,justify='center',border=0,table_id='vms_table')
                return JsonResponse( { 'table' : table.replace('VM Tools Upgrade</th>','VM Tools Upgrade</br><input type="checkbox" id="vmtools_all" class="form-check-input" name="vmtools_all" value="0"></th>').replace('Hardware Version Upgrade</th>','Hardware Version Upgrade</br><input type="checkbox" id="hardware_all" class="form-check-input" name="hardware_all" value="0"></th>').replace('MAC Retain</th>','MAC Retain</br><input type="checkbox" id="mac_all" class="form-check-input" name="mac_all" value="0"></th>').replace("<thead>",'<thead class="thead-light">').replace('<th></th>','<th><input name="select_all" class="form-check-input" value="1" id="example-select-all" type="checkbox" /></th>').replace('<th>','<th class="border-0">').replace('<tbody>','<tbody style="text-align:center;">').replace('&lt;','<').replace('&gt;','>')}, safe=True)
                
        
    if page == 'report':
        if request.is_ajax():
            if 'movegroup' in request.POST and 'runid' in request.POST:
                drs,vmd,ntwk,strg = Executors().select_from_database(report='Pre',procedure='View',movegruop=request.POST['movegroup'],runid=request.POST['runid'])
                drs,vmd,ntwk,strg = pd.DataFrame(drs),pd.DataFrame(vmd),pd.DataFrame(ntwk),pd.DataFrame(strg)
                #print(drs)
                drs['No of VM\'s'] = drs['VM']
                columns = drs.columns.to_list()
                for x,y in enumerate(drs['VM']):
                    if ',' in y:
                        hdlen =  len(y.split(','))
                        df = pd.DataFrame(list(zip( [drs['Name'][x]] * hdlen , [drs['Type'][x]] * hdlen , y.split(','), [len(y.split(','))] * hdlen)),columns=columns)
                        drs = pd.concat([drs, df], ignore_index = True)
                        drs.reset_index()
                        
                for x,y in enumerate(drs['VM']):
                    if ',' in y:
                        drs = drs.drop(index=int(x))
                #drs['No of VM\'s'] = [ len(x.split(',')) for x in drs['VM']]
                drs = drs[['Name','Type','No of VM\'s','VM']]

                columns = strg.columns.to_list()
                for x,y in enumerate(strg['HardDiskName']):
                    if ',' in y:
                        hdlen =  len(y.split(','))
                        df = pd.DataFrame(list(zip( [strg['VM'][x]] * hdlen , y.split(','), strg['DiskSize'][x].split(',') , [strg['DiskCount'][x]] * hdlen , strg['Multi_Writer'][x].split(','), strg['Disk_Type'][x].split(','), strg['StoragePolicy'][x].split(','))),columns=columns)
                        #print(df)
                        strg = pd.concat([strg, df], ignore_index = True)
                        strg.reset_index()
                        
                for x,y in enumerate(strg['HardDiskName']):
                    if ',' in y:
                        strg = strg.drop(index=int(x))
                strg = strg[['VM', 'DiskCount','HardDiskName', 'DiskSize', 'Multi_Writer', 'Disk_Type', 'StoragePolicy']]
                #print(eval(vmd.to_json(orient='split',index=False).replace('null','None')))
                return JsonResponse({'drs':eval(drs.to_json(orient='split',index=False).replace('null','None')),'vmd':eval(vmd.to_json(orient='split',index=False).replace('null','None')),'ntwk':eval(ntwk.to_json(orient='split',index=False).replace('null','None')),'strg':eval(strg.to_json(orient='split',index=False).replace('null','None')),'maps':{'drs':'DRS Rules','vmd':'VM Deatils','ntwk':'Network','strg':'Storage'}}, safe=True)            
                
            
        vm_res = Executors().select_from_database(report="Pre")
        print(vm_res)
        if vm_res:
            df = pd.DataFrame(vm_res)
            df['No'] = range(1,len(df)+1)
            df = df[['No','Move Group Name','No of VM','Generated On','View Report']]
            table = df.to_html(classes=classes,index=False,justify='center',border=0,table_id='report_table')
            context['table'] = table.replace("<thead>",'<thead class="thead-light">').replace('<th>','<th class="border-0">').replace('<tbody>','<tbody style="text-align:center;">').replace('&lt;','<').replace('&gt;','>')
        else:
            context['table'] = '<table border="0" class="dataframe table table-centered table-nowrap mb-0 rounded" id="report_table"><thead class="thead-light"><tr style="text-align: center;"><th class="border-0">No</th><th class="border-0">Move Group Name</th><th class="border-0">No of VM</th><th class="border-0">Generated On</th><th class="border-0">View Report</th></tr></thead><tbody><tr><td colspan="5" class="fw-bolder">No Records Found</td></tr></tbody></table>'
    html_template = loader.get_template( 'pre-migration.html' )
    return HttpResponse(html_template.render(context, request))
			
@login_required(login_url="/login/")
def postmigration(request):
    print("WWWWWWWWWWWWWW")
    context = {}
    context['segment'] = 'postmigration'
    page = request.path.split('/')[-1]
    context['page'] = page
    classes = 'table table-centered table-nowrap mb-0 rounded table-responsive'
    formatters = {'thead':[('class','thead-light')]}
    if page == 'generate':
        #print("^^^^^^^^^^^^^^^^^^^")
        runid=request.POST.get('runid')
        #print("runid is",runid)
        if request.is_ajax():
            if 'runid' in request.POST and 'movegroup' in request.POST:
                print("LLLLLLLLLLL")
                # Execute the Post Migration Checkup
                Executors().execute_powershell(migration='Post',movegroup=request.POST['movegroup'],runid=request.POST['runid'],avs=2)
                return JsonResponse({'Execution':True},safe=True)
            if 'runid' in request.POST and 'func' in request.POST:
                print(")))))))))))))))")
                # Getting the status of the Migration Checkup
                status = Executors().select_from_database(report="Post",procedure='status',runid=request.POST['runid'])
                return JsonResponse( ( status[0] if status else status),safe=False)
        vm_res = Executors().select_from_database(report="Post",procedure='Generate')
        # vm_res = [{'Move Group NAME': 'Move_Group 1','No of VM': '8'},
        #           {'Move Group NAME': 'Move_Group 2','No of VM': '20'},
        #           {'Move Group NAME': 'Move_Group 3','No of VM': '30'},
        #           {'Move Group NAME': 'Move_Group 4','No of VM': '15'}]
        print(vm_res)
        if vm_res:
            df = pd.DataFrame(vm_res)
            #df[''] = ''
            df = df[['Move Group NAME','No of VM','Action']]
            table = df.to_html(classes=classes,index=False,justify='center',border=0,table_id='vms_table')
            context['table'] = table.replace("<thead>",'<thead class="thead-light">').replace('<th></th>','<th><input name="select_all" class="form-check-input" value="1" id="example-select-all" type="checkbox"/></th>').replace('<th>','<th class="border-0">').replace('<tbody>','<tbody style="text-align:center;">').replace('&lt;','<').replace('&gt;','>')
        else:
            context['table'] = '<table border="0" class="dataframe table table-centered table-nowrap mb-0 rounded" id="report_table"><thead class="thead-light"><tr style="text-align: center;"><th class="border-0"></th><th class="border-0">Move Group Name</th><th class="border-0">No of VM</th></tr></thead></table>'
    if page == 'report':
        print("YYYYYYYYYYYYYYYYY")
        #print("run id is",request.POST['runid'])
        #print("move group is",request.POST.get('movegroup'))
        if request.is_ajax():
            #print("#############")
            if 'movegroup' in request.POST and 'runid' in request.POST:
                #print("!!!!!!!!1######")
                drs,vmd,ntwk,strg = Executors().select_from_database(report='Post',procedure='View',movegruop=request.POST['movegroup'],runid=request.POST['runid'])
                drs,vmd,ntwk,strg = pd.DataFrame(drs),pd.DataFrame(vmd),pd.DataFrame(ntwk),pd.DataFrame(strg)
                #print("drs is",drs)
                drs['No of VM\'s'] = drs['VM']
                columns = drs.columns.to_list()
                for x,y in enumerate(drs['VM']):
                    if ',' in y:
                        hdlen =  len(y.split(','))
                        df = pd.DataFrame(list(zip( [drs['Name'][x]] * hdlen , [drs['Type'][x]] * hdlen , y.split(','), [len(y.split(','))] * hdlen)),columns=columns)
                        drs = pd.concat([drs, df], ignore_index = True)
                        drs.reset_index()
                        
                for x,y in enumerate(drs['VM']):
                    if ',' in y:
                        drs = drs.drop(index=int(x))
                #drs['No of VM\'s'] = [ len(x.split(',')) for x in drs['VM']]
                drs = drs[['Name','Type','No of VM\'s','VM']]

                columns = strg.columns.to_list()
                for x,y in enumerate(strg['HardDiskName']):
                    if ',' in y:
                        hdlen =  len(y.split(','))
                        df = pd.DataFrame(list(zip( [strg['VM'][x]] * hdlen , y.split(','), strg['DiskSize'][x].split(',') , [strg['DiskCount'][x]] * hdlen , strg['Multi_Writer'][x].split(','), strg['Disk_Type'][x].split(','), strg['StoragePolicy'][x].split(','))),columns=columns)
                        #print(df)
                        strg = pd.concat([strg, df], ignore_index = True)
                        strg.reset_index()
                        
                for x,y in enumerate(strg['HardDiskName']):
                    if ',' in y:
                        strg = strg.drop(index=int(x))
                strg = strg[['VM', 'DiskCount','HardDiskName', 'DiskSize', 'Multi_Writer', 'Disk_Type', 'StoragePolicy']]
                #print(eval(vmd.to_json(orient='split',index=False).replace('null','None')))
                return JsonResponse({'drs':eval(drs.to_json(orient='split',index=False).replace('null','None')),'vmd':eval(vmd.to_json(orient='split',index=False).replace('null','None')),'ntwk':eval(ntwk.to_json(orient='split',index=False).replace('null','None')),'strg':eval(strg.to_json(orient='split',index=False).replace('null','None')),'maps':{'drs':'DRS Rules','vmd':'VM Deatils','ntwk':'Network','strg':'Storage'}}, safe=True)

        vm_res = Executors().select_from_database(report="Post")
        print("VM result is",vm_res)
        if vm_res:
            df = pd.DataFrame(vm_res)
            df['No'] = range(1,len(df)+1)
            df = df[['No','Move Group Name','No of VM','Generated On','View Report']]
            table = df.to_html(classes=classes,index=False,justify='center',border=0,table_id='report_table')
            context['table'] = table.replace("<thead>",'<thead class="thead-light">').replace('<th>','<th class="border-0">').replace('<tbody>','<tbody style="text-align:center;">').replace('&lt;','<').replace('&gt;','>')
        else:
            context['table'] = '<table border="0" class="dataframe table table-centered table-nowrap mb-0 rounded" id="report_table"><thead class="thead-light"><tr style="text-align: center;"><th class="border-0">No</th><th class="border-0">Move Group Name</th><th class="border-0">No of VM</th><th class="border-0">Generated On</th><th class="border-0">View Report</th></tr></thead><tbody><tr><td colspan="5" class="fw-bolder">No Records Found</td></tr></tbody></table>'
    html_template = loader.get_template( 'post-migration.html' )
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def compliance(request):
    context = {}
    context['segment'] = 'compliance'
    page = request.path.split('/')[-1]
    context['page'] = page
    classes = 'table table-centered table-nowrap mb-0 rounded table-responsive'
    formatters = {'thead':[('class','thead-light')]}
    if page == 'generate':
        vm_res = [{'VM NAME': 'name1','Cluster Name': 'Cluster1','Datacenter':'dc1'},{'VM NAME': 'name2','Cluster Name': 'Cluster1','Datacenter':'dc1'},{'VM NAME': 'name3','Cluster Name': 'Cluster1','Datacenter':'dc1'},{'VM NAME': 'name4','Cluster Name': 'Cluster1','Datacenter':'dc1'}]
        df = pd.DataFrame(vm_res)
        df[''] = ''
        df = df[['','VM NAME','Cluster Name','Datacenter']]
        table = df.to_html(classes=classes,index=False,justify='center',border=0,table_id='vms_table')
        context['table'] = table.replace("<thead>",'<thead class="thead-light">').replace('<th></th>','<th><input name="select_all" class="form-check-input" value="1" id="example-select-all" type="checkbox" /></th>').replace('<th>','<th class="border-0">').replace('<tbody>','<tbody style="text-align:center;">')
    if page == 'report':
        if request.is_ajax():
            conn = sqlite3.connect(Path(BASE_DIR,'HCX-Pre.SQLite'))
            drs = get_data_from_query("Select * From DRSRules;",conn)
            drs['No of VM\'s'] = drs['VM']
            columns = drs.columns.to_list()
            for x,y in enumerate(drs['VM']):
                if ',' in y:
                    hdlen =  len(y.split(','))
                    df = pd.DataFrame(list(zip( [drs['Name'][x]] * hdlen , [drs['Type'][x]] * hdlen , y.split(','), [len(y.split(','))] * hdlen)),columns=columns)
                    #print(df)
                    drs = pd.concat([drs, df], ignore_index = True)
                    drs.reset_index()
                    
            for x,y in enumerate(drs['VM']):
                if ',' in y:
                    drs = drs.drop(index=int(x))
            #drs['No of VM\'s'] = [ len(x.split(',')) for x in drs['VM']]
            drs = drs[['Name','Type','No of VM\'s','VM']]

            vmd = get_data_from_query("Select * From VMDetail;",conn)

            ntwk = get_data_from_query("Select * From Network;",conn)

            strg = get_data_from_query("Select * From Storage;",conn)

            columns = strg.columns.to_list()
            for x,y in enumerate(strg['HardDiskName']):
                if ',' in y:
                    hdlen =  len(y.split(','))
                    df = pd.DataFrame(list(zip( [strg['VM'][x]] * hdlen , y.split(','), strg['DiskSize'][x].split(',') , [strg['DiskCount'][x]] * hdlen , strg['Multi_Writer'][x].split(','), strg['Disk_Type'][x].split(','), strg['StoragePolicy'][x].split(','))),columns=columns)
                    #print(df)
                    strg = pd.concat([strg, df], ignore_index = True)
                    strg.reset_index()
                    
            for x,y in enumerate(strg['HardDiskName']):
                if ',' in y:
                    strg = strg.drop(index=int(x))
            strg = strg[['VM', 'DiskCount','HardDiskName', 'DiskSize', 'Multi_Writer', 'Disk_Type', 'StoragePolicy']]
            #print(eval(vmd.to_json(orient='split',index=False).replace('null','None')))
            return JsonResponse({'drs':eval(drs.to_json(orient='split',index=False).replace('null','None')),'vmd':eval(vmd.to_json(orient='split',index=False).replace('null','None')),'ntwk':eval(ntwk.to_json(orient='split',index=False).replace('null','None')),'strg':eval(strg.to_json(orient='split',index=False).replace('null','None')),'maps':{'drs':'DRS Rules','vmd':'VM Deatils','ntwk':'Network','strg':'Storage'}}, safe=True)
        vm_res = [{'Generated On': '01-06-2021 10:20:31','No of VM': 6,'View Report':'<button class="btn btn-sm btn-primary view_report">Click Here</button>'},{'Generated On': '01-06-2021 10:20:31','No of VM': 6,'View Report':'<button class="btn btn-sm btn-primary view_report">Click Here</button>'},{'Generated On': '01-06-2021 10:20:31','No of VM': 6,'View Report':'<button class="btn btn-sm btn-primary view_report">Click Here</button>'},{'Generated On': '01-06-2021 10:20:31','No of VM': 6,'View Report':'<button class="btn btn-sm btn-primary view_report">Click Here</button>'}]
        df = pd.DataFrame(vm_res)
        df['No'] = range(1,len(df)+1)
        df = df[['No','Generated On','No of VM','View Report']]
        table = df.to_html(classes=classes,index=False,justify='center',border=0,table_id='report_table')
        context['table'] = table.replace("<thead>",'<thead class="thead-light">').replace('<th>','<th class="border-0">').replace('<tbody>','<tbody style="text-align:center;">').replace('&lt;','<').replace('&gt;','>')
    html_template = loader.get_template( 'compliance.html' )
    return HttpResponse(html_template.render(context, request))
