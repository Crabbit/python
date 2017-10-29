<html lang="zh-CN">
    <meta charset="utf-8">
</html>
<?php
include_once('uuap-php/index.php');
include_once('conf/mysql.php');
include_once('check_zhiban.php');
$login_user = phpCAS::getUser();
$check_ret = CheckOp($login_user);

if ($check_ret == '1'){
    echo "不是建库值班人员，不要乱点噢!";
    echo "<head>";
    echo "<meta http-equiv=\"refresh\" content=\"2;url=index.php\">";
    echo "</head>";
    exit (1);
}

if( isset($_POST['errorId']) ){
    $post_errorid = $_POST['errorId'];

    $date_datetime_now = date("Y-m-d H:i:s");

    $conn = mysqli_connect($ygg_monitor_host, $ygg_monitor_user, $ygg_monitor_password, $ygg_monitor_databases);
    if (!$conn) {
        die("Connection failed: " . mysqli_connect_error());
    }

    $sql = "update " . $ygg_monitor_table . " set operator=\"" . $login_user;
    $sql = $sql . "\", operatingTime=\"" . $date_datetime_now;
    $sql = $sql . "\" where operator is NULL ";
    $sql = $sql . "and currStatus != 1 ";
    if ( $post_errorid == 'all' ){
        $sql = $sql . ";";
    }
    else{
        $sql = $sql . "and errorId=\"" . $post_errorid . "\";";
    }
    if (mysqli_query($conn, $sql)){
        echo "认领成功";
        $cmd = "echo " . $login_user . "-" . $date_datetime_now . "-" . $post_errorid . ">> ./logs/handle.log";
        system($cmd);
        echo "<head>";
            echo "<meta http-equiv=\"refresh\" content=\"0;url=index.php\">";
        echo "</head>";
    }
    else{
        echo "失败, Error: " . $sql . "<br>" . mysqli_error($conn);
    }
}
?>
