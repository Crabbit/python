<html lang="zh-CN">
    <meta charset="utf-8">
</html>
<?php

include_once('uuap-php/index.php');
include_once('conf/mysql.php');
include_once('check_zhiban.php');
$login_user = phpCAS::getUser();
$check_ret = CheckOp($login_user);

function exit_abnormal(){
    echo "<head>";
        echo "<meta http-equiv=\"refresh\" content=\"2;url=index.php\">";
    echo "</head>";
    exit (1);
}

if ($check_ret == '1'){
    echo "不是建库值班人员，不要乱点噢!";
    exit_abnormal();
}

//$python_bin = "/home/myperson/tools/build_submitter/usr/bin/python2.7";
$python_bin = "/home/work/.jumbo/bin/python2.7";
$ygg_top_dir = "components/ygg_bin/";
$ygg_bin_dir = $ygg_top_dir . "bin/";
$ygg_conf_dir = $ygg_top_dir . "conf/";
$ygg_bin = $ygg_bin_dir . "Yggdrasil.py";
$ygg_server = $ygg_conf_dir . "server.yaml";
$ygg_build01 = $ygg_conf_dir . "server.yaml.build01";
$ygg_build02 = $ygg_conf_dir . "server.yaml.build02";

if( isset($_POST['restart_errorid_list']) ){
    $post_errorid = $_POST['restart_errorid_list'];
    $errorid_array = explode( ",", $post_errorid);
    $errorid_count = count($errorid_array);
    //print_r($errorid_array);

    $date_datetime_now = date("Y-m-d H:i:s");

    // ----------------------------------------------------------
    //初始化库种配置，当前主要获取compass集群信息
    $kutype_conf_conn = mysqli_connect($ygg_kutype_host, $ygg_kutype_user, $ygg_kutype_password, $ygg_kutype_databases);
    if (!$kutype_conf_conn) {
        die("Connection failed: " . mysqli_connect_error());
    }
    $sql = "SELECT buildEnv,cluster,compassDomain FROM ygg_kuType GROUP BY buildEnv";
    $kutype_conf_result = mysqli_query($kutype_conf_conn, $sql);
    if (mysqli_num_rows($kutype_conf_result) > 0){
        while( $single_kutype_conf_array = mysqli_fetch_assoc($kutype_conf_result )){
            $all_kutype_conf_array[$single_kutype_conf_array["buildEnv"]] = $single_kutype_conf_array;
        }
    }
    else{
        echo "初始化库种配置失败" . $sql . "<br>" . mysqli_error($conn);
        exit_abnormal();
    }
    print_r($all_kutype_conf_array);


    // ----------------------------------------------------------
    ///开始获取异常信息，准备重启
    $sql_condition = "errorId = '" . $errorid_array[0] . "'";
    for($i = 1; $i < $errorid_count; $i++){
        $sql_condition = $sql_condition . " or errorId = '" . $errorid_array[$i] . "'";
    }
    $sql = "SELECT errorId,projectName,execId,errorName,jobHadoopLink FROM ygg_monitor where (" . $sql_condition;
    $sql = $sql . ") and (currStatus = '3') GROUP by execId,errorName";
    $cmd = "echo '|---" . $login_user . "-" . $date_datetime_now . " : [" . $sql . "]----|' >> ./logs/restart.log";
    system($cmd);

    $error_info_conn = mysqli_connect($ygg_monitor_host, $ygg_monitor_user, $ygg_monitor_password, $ygg_monitor_databases);
    if (!$error_info_conn) {
        die("Connection failed: " . mysqli_connect_error());
    }
    $error_info_result = mysqli_query($error_info_conn, $sql);
    $total_error_count = mysqli_num_rows($error_info_result);
    if ( $total_error_count > 0){
        while( $single_error_info_array = mysqli_fetch_assoc($error_info_result)){
            $all_error_info_array[$single_error_info_array["errorId"]] = $single_error_info_array;
        }
    }
    else{
        $error_log = "获取重启任务信息失败" . $sql;
        $cmd = "echo '" . $error_log . "' >> ./logs/restart.log.wf";
        system($cmd);
        echo "</br></br>获取重启任务信息为空";
        exit_abnormal();
    }


    // ----------------------------------------------------------
    //重启
    echo "-start-</br>";
    foreach( $all_error_info_array as $single_error_id=>$single_error_info_array ){
        $single_error_project_name = $single_error_info_array["projectName"];
        $single_error_exec_id = $single_error_info_array["execId"];
        $single_error_jobname = $single_error_info_array["errorName"];

        //获取compass domain地址
        $single_buildenv_conf_array = $all_kutype_conf_array[$single_error_project_name];
        $single_buildenv_compass_domain = $single_buildenv_conf_array["compassDomain"];

        echo $single_error_project_name;
        echo $single_buildenv_compass_domain;
        echo " ---|</br>";
        if( $single_buildenv_compass_domain == "http://xx-compass10.xx:xx" ){
            //替换compass domain配置
            $cmd_1_to_server = "cp " . $ygg_build01 . " " . $ygg_server;
        }
        if( $single_buildenv_compass_domain == "http://xx-compass.xx.com:xx" ){
            $cmd_2_to_server = "cp " . $ygg_build02 . " " . $ygg_server;
        }
        system($cmd_2_to_server);

        //开始重启
        $cmd_restart = $python_bin . " " . $ygg_bin . " start-job -e " . $single_error_exec_id. " -j " . $single_error_jobname;
        system($cmd_restart);
        $cmd = "echo '[" . $cmd_restart . "]' >> ./logs/restart.log";
        system($cmd);
    }

    echo "<head>";
        echo "<meta http-equiv=\"refresh\" content=\"9;url=index.php\">";
    echo "</head>";
}
else{
    echo "fxxxx";
}
?>
