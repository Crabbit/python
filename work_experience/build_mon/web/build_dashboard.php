<?php
include_once('uuap-php/index.php');
include_once('conf/mysql.php');

//	echo 'php'
$conn = mysqli_connect($ygg_monitor_host, $ygg_monitor_user, $ygg_monitor_password, $ygg_monitor_databases);
if (!$conn) {
	    die("Connection failed: " . mysqli_connect_error());
}

?>

<!DOCTYPE html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Build_DashBoard</title>

    <!-- Bootstrap -->
    <link href="components/bootstrap-3.3.5/css/bootstrap.min.css" rel="stylesheet">
	<!-- DataTables -->
	<link rel="stylesheet" type="text/css" href="components/datatables/media/css/jquery.dataTables.min.css">
	<!-- calendar -->
	<link rel="stylesheet" href="components/calendar/css/calendar.css">


    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
      <script src="https://cdn.bootcss.com/html5shiv/3.7.3/html5shiv.min.js"></script>
      <script src="https://cdn.bootcss.com/respond.js/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>

  <body>
	<div class="container-fluid jumbotron" style="padding-top: 1px; padding-bottom: 1px;">
		<div class="container-fluid" style="padding-top: 1px; padding-bottom: 1px;" id="">
        <div class="row">
			<div class="col-xs-12" style="margin-top: 1px; margin-bottom: 1px">
				<div class="col-xs-2" style="margin-top: 1px; margin-bottom: 1x">
					<h4 class="text-right">当前值班人:</h4>
				</div>
				<div class="col-xs-10" style="">
					<h4 style="">
						<?php
							$first_op_infourl = "http://zhiban.xx.com/xx/getDNById?id=60623";
							$first_op_curl = curl_init($first_op_infourl);
							curl_setopt($first_op_curl, CURLOPT_RETURNTRANSFER, true);
							curl_setopt($first_op_curl, CURLOPT_BINARYTRANSFER, true);
							$output = curl_exec($first_op_curl);
						
							$first_op = explode( ";", $output);
							echo $first_op[0];
						?>
					</h4>
				</div>
			</div>
        </div>
        <div class="row">
			<div class="col-xs-12">
				<div class="col-xs-2">
					<h4 class="text-right" >异常的库种:</h4>
				</div>
				<div class="col-xs-10" >
					<ul class="nav nav-pills" role="tablist">
						<?php
						$sql = "select projectName, count(*) from " . $ygg_monitor_table . " where currStatus != 1 group by projectName;";
						$abnormal_project = mysqli_query($conn, $sql);

						if (mysqli_num_rows($abnormal_project) > 0) {
							while($row = mysqli_fetch_assoc($abnormal_project)){
								echo "<li role=\"presentation\"><a onclick=\"click_search('";
								echo $row["projectName"];
								echo "')\" style=\"padding-left:0px; padding-right:25px; font-size:18px;\">";
								echo $row["projectName"];
								echo "<span class=\"badge\">";
								echo $row["count(*)"];
								echo "</span></a></li>";
							}
						}
						?>
					</ul>
				</div>
			</div>
        </div>
        <div class="row">
			<div class="col-xs-12" >
				<div class="col-xs-2">
					<h4 class="text-right">未认领条数:</h4>
				</div>
				<div class="col-xs-1" style="margin-top: 1px; margin-bottom: 1px">
						<h4 style="margin-top: 10px; margin-bottom: 5px; padding-top: 0px;">
						<?php
						$sql = "select count(*) from " . $ygg_monitor_table . " where currStatus != 1 and operator is null;";
						$wait_claim = mysqli_query($conn, $sql);

						if (mysqli_num_rows($wait_claim) > 0) {
							$row = mysqli_fetch_assoc($wait_claim);
							echo $row["count(*)"];
						}
						?>
						</h4>
				</div>
				<div class="col-xs-1" style="padding-top: 5px;">
					<form role="form" action="handle.php" method="post">
						<button type="submit" class="btn btn-danger" name="errorId" value="all">一键认领</button>
					</form>
				</div>
				<div class="col-xs-1" style="padding-top: 5px;">
					<form role="form" action="restart_job.php" method="post">
						<!--
						<button type="submit" form="job_restart" class="btn btn-info" value="all">选中重启</button>
						-->
						<button type="submit" id="submit_restart_errorid_list" class="btn btn-info" onclick="restart_by_select('restart_error_id')" name="restart_errorid_list" value="">选中重启</button>
					</form>
				</div>
				<!--
				<div class="col-xs-7" id="restartJob" style="padding-top: 5px;">
					<form class="form-inline">
						<div class="form-group" class="col-xs-2" >
								<input type="text" class="form-control" id="buildEnv" placeholder="建库环境">
						</div>
						<div class="form-group" class="col-xs-2" >
								<input type="text" class="form-control" id="execId" placeholder="Exec Id">
						</div>
						<div class="form-group" class="col-xs-2" >
								<input type="text" class="form-control" id="jobName" placeholder="Job Name">
						</div>
						<div class="form-group" class="col-xs-1" >
                            <button type="submit" class="btn btn-default">重启</button>
                        </div>
					</form>
				</div>
				-->
			</div>
		</div>
        </div>
        <div class="row">
			<div class="col-xs-12" >
            </div>
        </div>
        <div class="row">
        <div class="col-xs-1"></div>
		<div class="col-xs-10" style="margin-top: 1px; margin-bottom: 1px; padding-left: 1px; padding-right: 1px;">
			<div class="btn-group btn-group-justified" aria-label="...">
				<div class="btn-group" role="group">
					<button type="button" class="btn btn-default" data-toggle="collapse" data-target="#calendarSpace">建库安排</button>
				</div>
			</div>
		</div>
		</div>
		<div id="calendarSpace" class="collapse">
			<div class="page-header">
				<div class="pull-right form-inline">
					<div class="btn-group">
						<button class="btn btn-primary" data-calendar-nav="prev"><< Prev</button>
						<button class="btn" data-calendar-nav="today">Today</button>
						<button class="btn btn-primary" data-calendar-nav="next">Next >></button>
					</div>
					<div class="btn-group">
						<button class="btn btn-warning" data-calendar-view="year">Year</button>
						<button class="btn btn-warning active" data-calendar-view="month">Month</button>
						<button class="btn btn-warning" data-calendar-view="day">Day</button>
					</div>
				</div>
				<h3></h3>
			</div>

			<div class="jumbotron" style="background-color: #fff;" id="calendar">
			</div>
		</div>
	</div>

	<div class="container-fluid" style="padding-top: 20px">
		<!--建库看板-->
		<div class="row" style="">
			<table class="table" id="build_error_info">
				<thead>
					<tr>
						<th class="text-center">建库环境</th>
						<th class="text-center">迭代号</th>
						<th class="text-center">轮次号</th>
						<th class="text-center">execId</th>
						<th class="text-center">异常名称</th>
						<th class="text-center">异常状态</th>
						<th class="text-center">当前状态</th>
						<th class="text-center">异常开始运行时间</th>
						<th class="text-center">异常感知时间</th>
						<th class="text-center">链接1</th>
						<th class="text-center">链接2</th>
						<th class="text-center">认领人</th>
						<th class="text-center">认领时间</th>
						<th><button type="submit" class="btn btn-info" onclick="checkbox_all_error('restart_error_id')">全选</button></th>
						<th class="text-center">备注</th>
					</tr>
					<tbody>
					<?php
					$sql = "select * from " . $ygg_monitor_table . " where currStatus != 1;";
					$result = mysqli_query($conn, $sql);
					// 获取总共异常条数
					$error_total_num = mysqli_num_rows($result);
					// 给下面每条异常计数
					$error_count = 0;

					if ($error_total_num > 0) {
						while($row = mysqli_fetch_assoc($result)){
							$mysql_info[$row["errorId"]] = $row;
							switch ($row["errorName"]){
								case "kutype_monitor":
									$tr_lable = "<tr class=\"danger\">";
									break;
								case "flow_monitor":
									$tr_lable = "<tr class=\"warning\">";
									break;
								default:
									$tr_lable = "<tr>";
							}
							echo $tr_lable;
							echo "<td>";
							echo $row["projectName"];
							echo "</td>";
							echo "<td>";
							echo $row["iterId"];
							echo "</td>";
							echo "<td>";
							echo $row["cycleId"];
							echo "</td>";
							echo "<td>";
							echo $row["execId"];
							echo "</td>";
							echo "<td>";
							echo $row["errorName"];
							echo "</td>";
							echo "<td>";
							echo $row["errorStatus"];
							echo "</td>";
							switch ($row["currStatus"]){
								case "0":
									echo "<td>NotStart</td>";
									break;
								case "1":
									echo "<td class=\"text-success\">success</td>";
									break;
								case "2":
									echo "<td class=\"text-info\">Running</td>";
									break;
								case "3":
									echo "<td class=\"text-danger\">Failed</td>";
									break;
								case "4":
									echo "<td class=\"text-warning\">Skipped</td>";
									break;
								case "5":
									echo "<td class=\"text-warning\">Killed</td>";
									break;
								default:
									echo "<td></td>";
							}
							echo "<td>";
							echo $row["errorStarttime"];
							echo "</td>";
							echo "<td>";
							echo $row["errorAppeartime"];
							echo "</td>";
							echo "<td>";
							if ($row["jobHadoopLink"] != "None"){
								echo "<a style=\"color:#d9534f\" href=\"" . $row["jobHadoopLink"] . "\" target=\"_blank\">链接</a>";
							}
							else{
								echo "";
							}
							echo "</td>";
							echo "<td>";
							echo "<a style=\"color:#d9534f\" href=\"" . $row["jobStderrLink"] . "\" target=\"_blank\">链接</a>";
							echo "</td>";
							//认领情况的处理
							if ($row["operator"] == ""){
								echo "<td>";
								echo "</td>";
                                echo "<td class=\"text-center\">";
								echo "<form role=\"form\" action=\"handle.php\" method=\"post\">";
									echo "<button type=\"submit\" class=\"btn btn-danger\"";
									echo "name=\"errorId\" value=\"" . $row["errorId"] . "\">";
									echo "认领</button>";
								echo "</form>";
								echo "</td>";
								//echo "<td>";
								//echo "</td>";
							}
							else{
								echo "<td>";
								echo $row["operator"];
								echo "</td>";
								echo "<td>";
								echo $row["operatingTime"];
								echo "</td>";
								//echo "<td>";
								//echo $row["operating"];
								//echo "</td>";
							}
							//选中重启情况处理
							if ($row["operating"] == ""){
								echo "<td>";
								if ($row["errorName"] != "kutype_monitor" && $row["errorName"] != "flow_monitor"){
									echo "<div class=\"checkbox text-center\">";
											echo "<input type=\"checkbox\" name=\"restart_error_id\" value=\"";
											echo $row["errorId"];
											echo "\">";
									echo "</div>";
								}
								echo "</td>";
							}
                            else{
								echo "<td>";
								echo "</td>";
                            }
							//备注按钮的功能
							if ($row["remarks"] == ""){
								echo "<td>";
								echo "<button type=\"button\" class=\"btn btn-default\" data-toggle=\"modal\" data-target=\"#insert_remark\" ";
								$error_info_string = implode(",", $row);
								echo "onclick=\"error_info_projectname('" . $error_info_string . "')\"";
								echo ">录入</button></td>";
							}
							else{
								echo "<td>";
								echo "<a herf=\"#modal-details\">";
								echo "<button type=\"button\" class=\"btn btn-info\" data-toggle=\"modal\" data-target=\"#insert_remark\">查看</button>";
								echo "</td>";
							}
							echo "</tr>";
						}
					}
					else{
						echo "人品不错!";
					}

					mysqli_close($conn);
					?>
				</tbody>
			</table>
		</div>
	</div>

	<!--录入-->
	<div class="modal fade bs-example-modal-lg" id="insert_remark" tabindex="-1" role="dialog" aria-labelledby="myLargeModalLabel">
		<div class="modal-dialog modal-lg" role="document">
			<div class="modal-content">
				<div class="modal-header">
					<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">×</span></button>
					<h4 class="modal-title" id="myModalLabel">详细信息</h4>
				</div>
				<div class="modal-body">
					<div class="container-fluid">
						<div class="bs-callout bs-callout-info">
							<table class="table table-condensed">
								<tbody>
									<tr>
										<th class="text-center" style="width: 50%">建库环境</th>
										<th class="text-center" style="width: 50%" id="error_info_projectname"></th>
									</tr>
									<tr>
										<th class="text-center" style="width: 50%">Exec id</th>
										<th class="text-center" style="width: 50%" id="error_info_execid"></th>
									</tr>
									<tr>
										<th class="text-center" style="width: 50%">Iteration id</th>
										<th class="text-center" style="width: 50%" id="error_info_iterid"></th>
									</tr>
									<tr>
										<th class="text-center" style="width: 50%">Cycle id</th>
										<th class="text-center" style="width: 50%" id="error_info_cycleid"></th>
									</tr>
									<tr>
										<th class="text-center" style="width: 50%">异常名称</th>
										<th class="text-center" style="width: 50%" id="error_info_name"></th>
									</tr>
									<tr>
										<th class="text-center" style="width: 50%">异常状态</th>
										<th class="text-center" style="width: 50%" id="error_info_status"></th>
									</tr>
									<tr>
										<th class="text-center" style="width: 50%">当前状态</th>
										<th class="text-center" style="width: 50%" id="error_info_currstatus"></th>
									</tr>
								</tbody>
							<table>
							<hr>
							<h4>处理操作<h4>
							<textarea class="form-control" rows="3"></textarea>
							<hr>
							<h4>备注<h4>
							<textarea class="form-control" rows="3"></textarea>
						</div>
					</div>
				</div>
				<div class="modal-footer">
					<button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>
					<button type="button" class="btn btn-primary">保存</button>
				</div>
			</div>
		</div>
	</div>

    <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
    <!-- Include all compiled plugins (below), or include individual files as needed -->
	<!--
	<script src="https://cdn.bootcss.com/jquery/1.12.4/jquery.min.js"></script>
    <script src="components/bootstrap-3.3.5/js/bootstrap.min.js"></script>
	-->
	<script type="text/javascript" charset="utf8" src="components/datatables/media/js/jquery.dataTables.js"></script>

	<!-- error info show-->
	<script type="text/javascript">
		function error_info_projectname(click_value){
			error_projectname = click_value.split(",")
			document.getElementById("error_info_projectname").innerHTML=error_projectname[1];
			document.getElementById("error_info_execid").innerHTML=error_projectname[4];
			document.getElementById("error_info_iterid").innerHTML=error_projectname[2];
			document.getElementById("error_info_cycleid").innerHTML=error_projectname[3];
			document.getElementById("error_info_name").innerHTML=error_projectname[6];
			document.getElementById("error_info_status").innerHTML=error_projectname[7];
			switch(error_projectname[8]){
				case '0':
					document.getElementById("error_info_currstatus").innerHTML="NotStarted";
					break;
				case '1':
					document.getElementById("error_info_currstatus").innerHTML="Success";
					break;
				case '2':
					document.getElementById("error_info_currstatus").innerHTML="Running";
					break;
				case '3':
					document.getElementById("error_info_currstatus").innerHTML="Failed";
					break;
				case '4':
					document.getElementById("error_info_currstatus").innerHTML="Skiped";
					break;
				case '5':
					document.getElementById("error_info_currstatus").innerHTML="Killed";
					break;
				default:
					document.getElementById("error_info_currstatus").innerHTML="";
			}
			return 0;
		}
	</script>

	<!-- calendar show  -->
	<script type="text/javascript">
		$(function(){
			$.get("./calendar.php",function(data){
				$("#calendar").html(data);
			});
		});	
	</script>
	<!-- datatables search -->
	<script type="text/javascript">
		//加载datatables，关闭分页，打开搜索功能，关闭默认搜索显示
		$('#build_error_info').dataTable( {
			"paging": false,
			"searching": true,
			"dom": 'rti',
			"aoColumnDefs": [
				{ "bSortable": false, "aTargets": [ 13 ] }
			]
		} );
		var table = $('#build_error_info').DataTable();

		//自定义搜索框
		$('#user_search').on( 'keyup', function () {
			    table
					.search( this.value, true, false )
					.draw();
		} );

		//点击异常库种搜索
		function click_search(click_value){
			regExSearch = '^' + click_value + '$';
			$('a').on( 'click', function () {
				table
					.column( 0 )
					.search( regExSearch, true, false )
					.draw();
			} );
			return 0;
		}

		//全选-反选
		function checkbox_all_error(objName){
			var objNameList = document.getElementsByName(objName);

			if(null == objNameList){
				alert("没有一个可选哦~");
			}
			else{
				for(var i=0; i<objNameList.length; i++){
					if (objNameList[i].checked == true){
						objNameList[i].checked=""
					}
					else{
						objNameList[i].checked="checked";
					}
				}
			}
			return 0;
		}

		//选中重启
		function restart_by_select(objName){
			var objNameList = document.getElementsByName(objName);
			var total_error_id = new Array();

			for(var i=0; i<objNameList.length; i++){
				if (objNameList[i].checked == true){
					total_error_id.push(objNameList[i].value);
				}
			}
			var total_error_id_str = total_error_id.toString();
			document.getElementById("submit_restart_errorid_list").value=total_error_id_str
		}

		//$(document).ready( function () {
		//    $('#build_error_info').DataTable();
		//	} );
	</script>
		
  </body>
</html>
