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

}
$vpn_gateway_line_id = 1;
$dc_dev=$context['dc_dev'];
$dc_dev = getIdFromUbiId($dc_dev);
$components=$context['components'];
foreach ($components as $item){
    $service=$item['service'];
    $type=$item['service_type'];
    if($type === 'DataCenter' || $type === 'DC'){
        //
        //Get the line id of the DC that is chosen for the DC service
        $response = _configuration_variable_list ($dc_dev);
        logToFile(debug_dump($response, "VAR LIST\n"));
        $response = json_decode($response, true);
        if ($response['wo_status'] !== ENDED) {
            $response = json_encode($response);
            echo $response;
            exit();
        }
        if (isset($response['wo_newparams']) && ! empty($response['wo_newparams'])) {
            foreach ($response['wo_newparams'] as &$conf_variable) {
                $name = $conf_variable['name'];
                $value = $conf_variable['value'];
                if($name === 'LINE_ID'){
                    $dc_line_id=$value;
                    break;
                }
            }
        }
        if(empty($dc_line_id)){
            task_error('Task FAILED: DC does not have a line id');
        }
        $context['routes'][2]['line_id'] = $dc_line_id;
        break;
    }
}

 $context['routes'][1]['line_id'] = $vpn_gateway_line_id;

task_success('Task OK');
task_error('Task FAILED');
?>