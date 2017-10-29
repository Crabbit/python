$(function(){  
    $.get("./build_dashboard.php",function(data){  
        $("#iframeContent").html(data);//初始化加载界面  
    });  
      
    $('#team li').click(function(){//点击li加载界面  
        var current = $(this),  
        target = current.find('a').attr('target'); // 找到链接a中的targer的值  
        $.get(target,function(data){  
            $("#iframeContent").html(data);   
         });  
    });  
});  

