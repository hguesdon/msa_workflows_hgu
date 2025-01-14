<?php

/**
 * This file is necessary to include to use all the in-built libraries of /opt/fmc_repository/Reference/Common
 */
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

/**
 * List all the parameters required by the task
 */
function list_args()
{
  create_var_def('relatedParties.0.role', 'String');
  create_var_def('relatedParties.0.id', 'String');
  create_var_def('relatedParties.0.name', 'String');
}

$found ='';
$relatedParties=$context['relatedParties'];
foreach ($relatedParties as $relatedPartie){
	if (isset ($relatedPartie["role"]) && isset ($relatedPartie["id"]) ) {
		if ($relatedPartie["role"] == 'SERVICE_PROVIDER'){
			$found = $relatedPartie["id"];
		}
	}
}

if (not $found ){
 task_error('Can not get relatedParties with "SERVICE_PROVIDER"');
	
}


## Getting access_token

$headers = ['Accept' => 'application/json' ] ;

$body_request = [
    'client_id' => 'tm-nodered',
    'client_secret' => 'AzKvAsmdxe',
    'grant_type' => 'password',
    'username' => 'admin_aws_us',
    'password' => 'Demo123!' ];

$_headers = ['Accept'       => 'application/json',
             'Content-Type' =>  'application/json' ]
        
# response = requests.request("POST", url='https://eu01.sb.infonova.com/auth/realms/SB_CATALYST/protocol/openid-connect/token', headers=_headers, data=data, verify=False)

$ci = curl_init();
curl_setopt($ci, CURLOPT_URL,'https://eu01.sb.infonova.com/auth/realms/SB_CATALYST/protocol/openid-connect/token');
curl_setopt($ci, CURLOPT_TIMEOUT, 200);
curl_setopt($ci, CURLOPT_RETURNTRANSFER, 1);
curl_setopt($ci, CURLOPT_FORBID_REUSE, 0);
curl_setopt($ci, CURLOPT_CUSTOMREQUEST, 'POST');
curl_setopt($ci, CURLOPT_POSTFIELDS, $body_request);
curl_setopt($ci, CURLOPT_HTTPHEADER, $_headers );
$result= curl_exec($ci);

/* Store the result in a variable      */    
$context['token_result']=$result;	


task_exit(ENDED, 'OK');



/* 
context['infonova_access_token']=r_json.get('access_token')


##Sent notification
auth='Bearer ' +context['infonova_access_token']+''
_headers2 = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization':''+auth+'',
}

now = datetime.now(pytz.timezone("Europe/Paris"))
date_time = now.strftime("%Y-%m-%dT%H:%M:%S%z")

date_time_str = "{0}:{1}".format(
  date_time[:-2],
  date_time[-2:]
)

next_date_time=datetime.strptime(date_time,"%Y-%m-%dT%H:%M:%S%z")
next_date_time=next_date_time  + timedelta(days=1)
next_date_time=next_date_time.strftime("%Y-%m-%dT%H:%M:%S%z")
next_date_time_str = "{0}:{1}".format(
  next_date_time[:-2],
  next_date_time[-2:]
)

data2 = {
    'id': ''+context['externalId']+'',
    'dateTime': ''+date_time_str+'',
    'eventType': 'orderStateChangeNotification',
    'serviceOrder': {
    'id': ''+context['externalId']+'',
    'externalId': ''+context['externalId']+'',
    'state':'Completed',
    'priority': 4,
    'expectedCompletionDate': ''+next_date_time_str+''
    }
}

context['data2']=data2

infonova_url = "https://eu01.sb.infonova.com/r6-api/"+found_value+"/serviceordering/v1/notification"

context['infonova_url'] = infonova_url

response2 = requests.request("POST", url=infonova_url, headers=_headers2, data=json.dumps(data2), verify=False)
r_json2 = response2.json()
context.update(infonova = dict(response=r_json2,satus_code=response2.status_code))

MSA_API.task_success('Infonova Order state Change Notification for order sent\n Status Code : '+str(response2.status_code)+'', context, True)
*/

?>