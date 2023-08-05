"""
Methods Library
"""

import os
import time
from .models import *
from django.db import connection
from django.http import HttpResponse,JsonResponse

class Executors:
	def __init__(self) -> None:
		self.cursor = connection.cursor()
		pass

	def dictfetchall(self,query):
		#print(query)
		cursor = self.cursor.execute(query)
		"Return all rows from a cursor as a dict"
		columns = [col[0] for col in cursor.description]
		return [
			dict(zip(columns, row))
			for row in cursor.fetchall()
		]

	def execute_powershell(self,migration,movegroup,runid,avs):
		print("TTTTTTTTTTTTTt")
		print(os.popen('powershell.exe -ExecutionPolicy Bypass -file "'+os.path.join(os.getcwd(),'app\pwsh\get_report.ps1') +'" '+str(migration)+' '+str(movegroup)+' '+str(runid)+' '+str(avs)).read().splitlines())
		print("migration is movegroup is runid is",migration,movegroup,runid)
		self.insert_to_database({'migration':migration,'movegroup':movegroup,'runid':runid});

	def insert_to_database(self,data):
		print("IIIIIIIIIIIIIIIIIIIIIIIIIII")
		if 'movegroup' in data and 'vm_data[0][name]' in data:
			print("Entered Hereeeeeeeeeeeee")
			mg = MoveGroup(name = data['movegroup'])
			mg.save()
			for x in range(int(data['length'])):
				MoveGroupVM( name= data['vm_data['+ str(x) +'][name]'],
                vmtools = int(data['vm_data['+ str(x) +'][vmtools]']),
                hardware = int(data['vm_data['+ str(x) +'][hardware]']),
                mac = int(data['vm_data['+ str(x) +'][mac]']),
                movegroup = mg).save()
			return mg.id
		elif 'migration' in data and 'movegroup' in data and 'runid' in data:
			print("MMMMMMMMMM")
			MigrationCheckup(runid = data['runid'],vmgrpid = data['movegroup'],extype = data['migration']).save()
		elif 'movegroup' in data:
			MoveGroup(name = data['movegroup']).save()
   
	def select_from_database(self,report='Pre',procedure=None,movegruop=None,runid=None):
		try:
			if movegruop is None and procedure == "Generate":
				print("KKKKKKKKKKkppppppppppppp")
				# To display the list of Move Group and No of VMs For Post Migration
				query = "SELECT a.name AS 'Move Group NAME',count(b.name) As 'No of VM', ( case when 1 = 1 then '<button data-runid=\"' || c.runid || '\" data-movegroup=\"' || a.id || '\" class=\"btn btn-sm btn-primary generate_report rounded-0\">Start Checkup</button>' end) as 'Action' FROM app_MoveGroup As a LEFT JOIN app_MoveGroupVM As b on a.id = b.movegroup_id join app_migrationcheckup as c on b.movegroup_id = c.vmgrpid where c.extype = 'Pre' group by b.movegroup_id;"
				return self.dictfetchall(query)
			elif runid and procedure == "status":
				print("runid is!!!!!!!!!!!!!!!",runid)
				# To display the status for the For Pre/Post Migration
				query = "SELECT runid,total,drstotal,drs,vmdetail,network,storage FROM app_status where runid = " + runid + ";"
				#print(query)
				return self.dictfetchall(query)
			elif movegruop and procedure == "View":
				print("&&&&&&&&&&&&&&&")	
				q1="SELECT b.Name,b.Type,b.VM FROM app_migrationcheckup AS a JOIN app_drsrules AS b ON a.runid = b.runid_id WHERE a.extype = '" + report + "' AND a.runid = '"+ runid +"';"
				print("q1 is",q1)
				q2="SELECT b.VM,b.Powerstate,b.ToolsVersion,b.HardwareVersion,b.Snapshot,b.OS,b.ISO,b.Host,b.Datastore,b.Uptime FROM app_migrationcheckup AS a JOIN app_VMDetail AS b ON a.runid = b.runid_id WHERE a.extype = '" + report + "' AND a.runid = '"+ runid +"';"
				print("q2 is",q2)
				q3="SELECT b.VM,b.NIC,b.IPAddress,b.PortGroup,b.MacAddress,b.ConnectionStatus,b.Ping_Status,b.RDP FROM app_migrationcheckup AS a JOIN app_Network AS b ON a.runid = b.runid_id WHERE a.extype = '" + report + "' AND a.runid = '"+ runid +"';"
				print("q3 is",q3)
				q4="SELECT b.VM,b.HardDiskName,b.DiskSize,b.DiskCount,b.Multi_Writer,b.Disk_Type,b.StoragePolicy FROM app_migrationcheckup AS a JOIN app_Storage AS b ON a.runid = b.runid_id WHERE a.extype = '" + report + "' AND a.runid = '"+ runid +"';"

				print("q4 is",q4)			
				# To display result After the Migration Checkup on Pre & Post Migration
				return [ self.dictfetchall("SELECT b.Name,b.Type,b.VM FROM app_migrationcheckup AS a JOIN app_drsrules AS b ON a.runid = b.runid_id WHERE a.extype = '" + report + "' AND a.runid = '"+ runid +"';"),self.dictfetchall("SELECT b.VM,b.Powerstate,b.ToolsVersion,b.HardwareVersion,b.Snapshot,b.OS,b.ISO,b.Host,b.Datastore,b.Uptime FROM app_migrationcheckup AS a JOIN app_VMDetail AS b ON a.runid = b.runid_id WHERE a.extype = '" + report + "' AND a.runid = '"+ runid +"';"),
				self.dictfetchall("SELECT b.VM,b.NIC,b.IPAddress,b.PortGroup,b.MacAddress,b.ConnectionStatus,b.Ping_Status,b.RDP FROM app_migrationcheckup AS a JOIN app_Network AS b ON a.runid = b.runid_id WHERE a.extype = '" + report + "' AND a.runid = '"+ runid +"';"),
				self.dictfetchall("SELECT b.VM,b.HardDiskName,b.DiskSize,b.DiskCount,b.Multi_Writer,b.Disk_Type,b.StoragePolicy FROM app_migrationcheckup AS a JOIN app_Storage AS b ON a.runid = b.runid_id WHERE a.extype = '" + report + "' AND a.runid = '"+ runid +"';")]
			elif movegruop is None:
				print("BBBBBBBBB")
				print("report is",report)
				# To display no of records in View Reports on Pre & Post Migration
				query = "SELECT datetime(a.runid, 'unixepoch', 'localtime') as 'Generated On',b.name as 'Move Group Name',count( distinct c.id) as 'No of VM',( case when 1 = 1 then '<button data-runid=\"' || a.runid || '\" data-movegroup=\"' || b.id || '\" class=\"btn btn-sm btn-primary view_report rounded-0\">Click Here</button>' end) as 'View Report' FROM app_migrationcheckup As a JOIN app_MoveGroup As b on a.vmgrpid = b.id JOIN app_MoveGroupVM AS c on b.id = c.movegroup_id WHERE a.extype = '"+report+"' Group by a.vmgrpid;"
				return self.dictfetchall(query)
		except Exception as ex:
			print("Entered exception",ex)

def check_for_duplicate_MG(request):
	cursor = connection.cursor()
	movegroup=request.path.split('/')[-1]
	try:
		if movegroup is not None:
			d={'count_of_MG':0}
            # To check if the move group name is already available
			query = "SELECT count(id) from app_MoveGroup where name= '"+movegroup+"'"
			cursor.execute(query)
			result_set = cursor.fetchall()[0][0]
			d['count_of_MG']=result_set
			return JsonResponse(d,safe=True)
	except Exception as ex:
		return JsonResponse(d,safe=True)
