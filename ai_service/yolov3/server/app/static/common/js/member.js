

/* 일반 로그인 */
function loginSubmit(){
	var form = document.loginForm;

	if( $.trim(form.login_id.value) == "" ){
		alert("아이디를 입력해 주십시오.");
		$("#login_id").focus();
		return;
	}

	if( $.trim(form.login_pw.value) == "" ){
		alert("비밀번호를 입력해 주십시오.");
		$("#login_pw").focus();
		return;
	}

	form.login_id.value = $.trim( form.login_id.value );
	form.login_pw.value = $.trim( form.login_pw.value );
	// form.action = "/member/login_proc.php";

	// form.submit();

	$.ajax({
		type: "POST",
		url: "/member/login_proc.php",
		data: $("#loginForm").serialize(),
		success: function(res) {
			if($.trim(res.split("||")[0]) == "Y"){
				if(document.loginForm.return_url.value != ""){
					window.location.href = document.loginForm.return_url.value;
				} else {
					window.location.href = "/main/main.php";
				}
			}else{
				alert(res.split("||")[1]);
				return;
			}
		}
	});
}

function loginEnterSubmit() {
	if(event.keyCode == 13) {
		loginSubmit();
	}
}

/* 로그아웃 */
function logoutSubmit() {
	$.ajax({
		type: "POST",
		url: "/member/logout_proc.php",
		success: function(res) {
			if($.trim(res) == "Y"){
				alert('로그아웃 되었습니다.');
				window.location.href = "/main/main.php";
			}else{
				alert(res);
			}
		}
	});
}