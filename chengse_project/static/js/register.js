$(function(){
	var username_error = false,
		password_error = false,
		check_pwd_error = false,
		email_error = false;
	$("#user_text").blur(function(){
		check_username_len();
		if(username_error == false) {
			check_username(true);
		}
	});

	$("#tbPassword").blur(function(){
		check_password();
	});

	$("#confirm_pwd_text").blur(function(){
		check_confirm_pwd();
	});

	$("#eamil_text").blur(function(){
		check_email();
	});


	function check_username_len(){
		var user = $("#user_text").val();
		// alert(user);
		if (user.length < 3 || user.length > 10){
			// alert(1);
			$("#user_text").next().html("请输入3到10位用户名").show();
			username_error = true;
		}
		else{
			$("#user_text").next().hide();
			username_error = false;
		}
	}

	function check_username(async) {
		var username = $("#user_text").val();
		$.ajax({
			"url":"/user/check_user_exist/?username=" + username,
			"async":async,
			"success": function (data) {
				// 如果为0显示已注册
				if (data.res==0){
					$("#user_text").next().show().html("用户名已存在");
					username_error = true;
				}
				else{
					$("#user_text").next().hide();
					username_error = false;
				}
			}
		});
	}

	function check_password(){
		var pwd = $("#tbPassword").val();
		if (pwd.length < 6 || pwd.length > 16){
			$("#tbPassword").next().show().html("请输入6-16位密码");
			password_error=true;
		}
		else{
			$("#tbPassword").next().hide();
			password_error=false;
		}
	}
	function check_confirm_pwd(){
		var pwd = $("#tbPassword").val(),
			cpwd = $("#confirm_pwd_text").val();
		if (pwd != cpwd){
			$("#confirm_pwd_text").next().show().html("两次密码不一致");
			check_pwd_error=true;
		}
		else{
			$("#confirm_pwd_text").next().hide();
			check_pwd_error=false;
		}
	}

	function check_email(){
		var re = /^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$/;
		if(re.test($('#eamil_text').val()))
		{
			$('#eamil_text').next().hide();
			email_error = false;
		}
		else
		{
			$('#eamil_text').next().show().html('你输入的邮箱格式不正确');
			email_error = true;
		}
	}

	$("#myform").submit(function(){
		check_username_len();
		check_username(false);
		check_password();
		check_confirm_pwd();
		check_email();
		// alert(username_error);
		// alert(password_error);
		// alert(check_pwd_error+"/");
		// alert(email_error);

		if (username_error == false && password_error==false && check_pwd_error==false && email_error == false){
			// alert(1);
			return true;
		}
		else {
			// alert(2);
            return false;
        }
	});
});