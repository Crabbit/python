<?php

/**
* @param-- name, 检查该用户是不是建库op
* @return -- 检查通过返回0，否则返回1
*/
function CheckOp($name){
	$all_zhiban_infourl = "http://zhiban.xx.com/xx/getDutyAllMemberWithDutyId?id=60623";
	$all_zhiban_curl = curl_init($all_zhiban_infourl);

	curl_setopt($all_zhiban_curl, CURLOPT_RETURNTRANSFER, true);
	curl_setopt($all_zhiban_curl, CURLOPT_BINARYTRANSFER, true);

	$output = curl_exec($all_zhiban_curl);
	
	$zhiban_json_array = json_decode($output, true);
	$array_length = count($zhiban_json_array);
	for($i = 0; $i <= $array_length; $i++){
		$op = $zhiban_json_array['dutyMembers'][$i]['itemValue'];
		if ($name == $op){
			return 0;
		}
	}
	return 1;
}
?>

