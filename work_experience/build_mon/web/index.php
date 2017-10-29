<?php
	include_once('uuap-php/index.php');
	include_once('conf/mysql.php');

	$login_user = phpCAS::getUser();

//	echo 'php'
?>

<!DOCTYPE html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Build_DashBoard</title>

    <!-- Bootstrap -->
	<link rel="stylesheet" href="components/bootstrap-3.3.5/css/bootstrap.css">
	<!-- calendar
	<link rel="stylesheet" href="components/calendar/css/calendar.css">
	 -->

	<style type="text/css">
		.btn-twitter {
			padding-left: 30px;
			background: rgba(0, 0, 0, 0) url(https://platform.twitter.com/widgets/images/btn.27237bab4db188ca749164efd38861b0.png) -20px 6px no-repeat;
			background-position: -20px 11px !important;
		}
		.btn-twitter:hover {
			background-position:  -20px -18px !important;
		}
	</style>

    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
      <script src="https://cdn.bootcss.com/html5shiv/3.7.3/html5shiv.min.js"></script>
      <script src="https://cdn.bootcss.com/respond.js/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>

  <body>
	<div class="container-fluid" style="padding-top: 20px; padding-left: 1px;padding-right: 1px;">
		<div class="row" style="margin-bottom: 1px; z-index:10; height:40px;">
			<nav class="navbar navbar-inverse navbar-fixed-top">
				<div class="container">
					<div class="navbar-header">
						<a class="navbar-brand" href="http://perseus.xxxxx.com:8501">DT报警看板</a>
					</div>
					<div class="collapse navbar-collapse" id="keyword_search">
						<div style="margin-right: 15px">
							<p class="navbar-text navbar-right">Signed in as <a href="#" class="navbar-link"><?php echo $login_user?></a></p>
						</div>
						<ul class="nav navbar-nav" id="team">
						<!--
							<li><a target="http://xxxx.xxxxx.com:xxx/">Build</a></li>
							<li><a target="http://billboard.xxxxx.com/alarm/index.php?r=Sms/Index">Spider</a></li>
							<li><a target="#">DataFlow</a></li>
						-->
							<li><a target="http://xx.perseus.xxxxx.com:xxx/build_dashboard.php">Build</a></li>
							<li><a target="http://xx.billboard.xxxxx.com/alarm/index.php?r=Sms/Index">Spider</a></li>
							<li><a target="http://xx.billboard.xxxxx.com/alarm/index.php?r=Sms/dataflow">DataFlow</a></li>
						</ul>
						<form class="navbar-form navbar-left" role="search">
							<div class="form-group">
								<input type="text" class="form-control" placeholder="报警关键字搜索" id="user_search">
							</div>
						</form>
					</div>
				</div>
			</nav>
		</div>

		<!--报警看板-->
		<div id="iframeContent">
		</div>

    <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
    <script src="https://cdn.bootcss.com/jquery/1.12.4/jquery.min.js"></script>
    <!-- Include all compiled plugins (below), or include individual files as needed -->
    <script src="components/bootstrap-3.3.5/js/bootstrap.min.js"></script>
	<!--
	<script type="text/javascript" src="components/jstimezonedetect/jstz.min.js"></script>
	<script type="text/javascript" src="components/underscore/underscore-min.js"></script>
	<script type="text/javascript" src="components/calendar/js/calendar.js"></script>
	<script type="text/javascript" src="components/calendar/js/app.js"></script>
	-->
	<script src="components/bootstrap-3.3.5/js/iframe.js"></script>
	<!--
	<script type="text/javascript">
		var disqus_shortname = 'bootstrapcalendar';
		(function() {
			var dsq = document.createElement('script'); dsq.type = 'text/javascript'; dsq.async = true;
			dsq.src = '//' + disqus_shortname + '.disqus.com/embed.js';
			(document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0]).appendChild(dsq);
		})();
	</script>
	-->
  </body>
</html>
