$(document).ready(function(){
    $("#loginbtn").click(function(){
        $.post(
            "/login",
            {
                username:$("#usernameinputsign").val(),
                password:$("#passwordinputsign").val()
            },
            function (data, status){
                if(data == -1) {
                    alert("error");
                }else{
                    $('#signin').modal('hide');
                    location.href ="/";
                }
            }
        )
    });
    $("#uploaddocsubmit").click(function(){
        $("#uploaddocfrom").submit();
    });
});
