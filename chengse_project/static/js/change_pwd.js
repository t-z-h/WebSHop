$(function () {
    new_pwd_error = false;
    $("#cpwd").blur(function () {

            var cpassword=$("#cpwd").val(),
                new_password=$("#tbPassword").val();
            if(new_password != cpassword){
                $("#pwd_err1").show().html("两次密码不一致");
                new_pwd_error=true;
            }
            else{
                $("#pwd_err1").hide();
                new_pwd_error=false;
            }
        });
    $("#bnt_blue_1").click(function () {
        var pre_password=$("#pre_password").val(),
            new_password=$("#tbPassword").val();


            form_data={
                'pre_password':pre_password,
                'new_password':new_password,
            };
            $.post("/user/change_pwd_exist/",form_data,function (data) {
                if(data.res==0){
                    $("#pwd_error").show().html("密码输入错误");
                }
                else if(new_pwd_error == false){
                    location.href = '/user/login/'
                }
            })
        });


});