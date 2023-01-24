Common = {
    POST : function(url, data){
        var prom = $.Deferred();
        $.post(url, data).success(function( result ){
            prom.resolve( result );
        }).error(function(){
            prom.reject.apply(null, arguments);
        });

        return prom;
    },

    GET : function(url, data){
        var prom = $.Deferred();
        $.get(url, data).success(function( result ){
            prom.resolve( result );
        }).error(function(){
            prom.reject.apply(null, arguments);
        });

        return prom;
    },

	openWindowPop : function(theURL,winName,features){
        window.open(theURL,winName,features);
    },

    isNull : function(value){
        var returnValue = true;
        var check = $("#"+value).val();
        if (typeof check == "undefined") {
            returnValue = true;
        } else {
            if (check == "") returnValue = true;
            else returnValue = false;
        }
        return returnValue;
    },

    isNotEmail : function(value){
    	var returnValue = true;
        var chkEmail = value;
        var regex=/^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/;
        if(regex.test(chkEmail) == true) returnValue = false; // 정상적이면..
        return returnValue;
    },


    //쿠키생성
    CreateCookie : function(name, value, days){
    	try {
            if (days) {
                var date = new Date();
                date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
                var expires = "; expires=" + date.toGMTString();
            }
            else var expires = "";
            document.cookie = name + "=" + value + expires + "; path=/";
        }
        catch (exception) { }
    },
    //쿠키 읽기
    ReadCookie : function(name){
    	try {
            var nameEQ = name + "=";
            var ca = document.cookie.split(';');
            for (var i = 0; i < ca.length; i++) {
                var c = ca[i];

                while (c.charAt(0) == ' ') c = c.substring(1, c.length);
                if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
            }
            return null;
        }
        catch (exception) {}
    },
    //쿠키 삭제
    EraseCookie : function(name){
    	try {
          	Common.CreateCookie(name, "", -1);
          }
          catch (exception) {}
    }
}




Functions = {
    Load : function(){
        Functions.AllCheck();
        Functions.UrlBack();
        Functions.ClosePop();
    },
    //페이지네 체크박스 전체클릭
    AllCheck : function(){
        $("#AllCheck").click(function(){
            if($(this).is(":checked")){
                $("input:checkbox").prop("checked", true);
            } else {
                $("input:checkbox").prop("checked", false);
            }
        });
    },
    //페이지네 특정 체크박스 전체클릭
    AllCheckTarget : function(targets){
        if($("#AllCheckTarget").is(":checked")){
            $(":checkbox[name='"+targets+"']").prop("checked", true);
        } else {
            $(":checkbox[name='"+targets+"']").prop("checked", false);
        }
    },
    //전체클릭 버튼일 경우
    AllCheckBtn : function(targets){
    	var check_val = "";
		if( $("#all_check_gb").val() == "N" ){
			check_val = true;
			$("#all_check_gb").val("Y");
		}else{
			check_val = false;
			$("#all_check_gb").val("N");
		}

		$(":checkbox[name='"+targets+"']").each(function(){
			$(this).prop("checked", check_val );
		});
    },
    UrlBack : function(){
        $("#backBtn").click(function(){
            history.back();
        });
    },
    ClosePop : function(){
        $("#closeBtn").click(function(){
            window.close();
        });
    },

    //천단위콤마
    NumberFormat : function(str){
        str = str + "";

        if(str == "" || /[^0-9,]/.test(str)) return str;
        str = str.replace(/,/g, "");

        for(var i=0; i<parseInt(str.length/3, 10); i++){
            str = str.replace(/([0-9])([0-9]{3})(,|$)/, "$1,$2$3");
        }

        return str;
    },

    //숫자만
    onlyNum : function(str){
		var str = str + "";
		return parseInt(str.replace(/[^0-9]/g,""));
    }

}

Validation = {
    Load : function(){
        Validation.Numeric();
        Validation.Numeric_Dash();
        Validation.Alpha();
        Validation.Alpha_Numeric();
        Validation.Alpha_Comma();
        Validation.Alpha_Numeric_Special();
        Validation.Alpha_Numeric_Korean();
    },
    Numeric : function(){
        $(".numeric").on("keyup", function(){
            $(this).val($(this).val().replace(/[^0-9]/gi, ""));
        });
    },
    Numeric_Dash : function(){
        $(".numeric_dash").on("keyup", function(){
            $(this).val($(this).val().replace(/[^0-9:\-]/gi, ""));
        });
    },
    Alpha : function(){
        $(".alpha").on("keyup", function(){
            $(this).val($(this).val().replace(/[^A-Za-z]/gi, ""));
        });
    },
    Alpha_Numeric : function(){
        $(".alpha_numeric").on("keyup", function(){
            $(this).val($(this).val().replace(/[^A-Za-z0-9]/gi, ""));
        });
    },
    Alpha_Comma : function(){
        $(".alpha_comma").on("keyup", function(){
            $(this).val($(this).val().replace(/[^A-Za-z0-9\.]/gi, ""));
        });
    },
    Alpha_Numeric_Special : function(){
        $(".alpha_numeric_special").on("keyup", function(){
            $(this).val($(this).val().replace(/[^A-Za-z0-9\@\.\_\-]/gi, ""));
        });
    },
    Alpha_Numeric_Korean : function(){
        $(".alpha_numeric_korean").on("keyup", function(){
            $(this).val($(this).val().replace(/[^A-Za-z0-9ㄱ-ㅎ|ㅏ-ㅣ|가-힣]/gi, ""));
        });
    }
}

DatePeriod = {
    GetDate : function(p, s_date, e_date){
    	var mDay = 0;
		if(p == -1){ // 원경일 임시수정 기간별 달력 Radio Button 중 기간 을클릭시 날짜초기화??   arguments[p] = 0 일경우 해당 아이디의 날짜 초기화.
			$("#"+s_date).val('');
			$("#"+e_date).val('');
			return false;
		}
		/**
         * p
         * 0 : today
         * 10 : 1 month
         * 11 : 2 month
         * 12 : 3 month
         * 13 : 6 month
         */
		switch (p) {
		case 1 :
			mDay = 1;
			break;
		case 2 :
			mDay = 7;
			break;
		case 3 :
			mDay = 15;
			break;
		case 4 :
			mDay = 21;
			break;
        case 10 :
            mDay = 31;
            break;
        case 11 :
            mDay = 62;
            break;
        case 12 :
            mDay = 93;
            break;
        case 13 :
            mDay = 186;
            break;
		}

		var datToday = new Date();
		if(p < 5 || p > 9){
			$("#"+e_date).val(this.FormatDate(datToday));
			datToday.setDate(datToday.getDate() - mDay);
			$("#"+s_date).val(this.FormatDate(datToday));
		}else if(p == 5){
			var firstDate = new Date(datToday.getFullYear(), datToday.getMonth(), 1);
			var lastDate = new Date(datToday.getFullYear(), datToday.getMonth()+1, 0);
			$("#"+s_date).val(this.FormatDate(firstDate));
			$("#"+e_date).val(this.FormatDate(lastDate));
		}else if(p == 6){
			var firstDate = new Date(datToday.getFullYear(), datToday.getMonth()-1, 1);
			var lastDate = new Date(datToday.getFullYear(), (datToday.getMonth()-1)+1, 0);
			$("#"+s_date).val(this.FormatDate(firstDate));
			$("#"+e_date).val(this.FormatDate(lastDate));
		}else if(p == 7){
            var firstDate = new Date(datToday.getFullYear(), datToday.getMonth(), 1);
            var lastDate = new Date(datToday.getFullYear(), datToday.getMonth()+3, 0);
            $("#"+s_date).val(this.FormatDate(firstDate));
            $("#"+e_date).val(this.FormatDate(lastDate));
        }
    },
    FormatDate : function(date){
        var mymonth = date.getMonth() + 1;
	    var myweekday = date.getDate();
	    return (date.getFullYear() + "-" + ((mymonth < 10) ? "0" : "") + mymonth + "-" + ((myweekday < 10) ? "0" : "") + myweekday);
    }
}



Calendar = {
    Load: function(){
        $("#sdate").datetimepicker({
            lang : 'kr',
            format : 'Y-m-d',
            onShow : function(ct){
                this.setOptions({
                    maxDate : $("#edate").val() ? $("#edate").val() : false
                });
            },
            timepicker : false,
            closeOnDateSelect : true
        });

        $("#edate").datetimepicker({
            lang:'kr',
            format:'Y-m-d',
            onShow:function(ct){
                this.setOptions({
                    minDate:$("#sdate").val() ? $("#sdate").val() : false
                });
            },
            timepicker:false,
            closeOnDateSelect: true
        });

        $(".mdate").datetimepicker({
            lang:'kr',
            format:'Y-m-d',
            timepicker:false,
            closeOnDateSelect: true
        });
    }
}

$(document).ready(function(){
    Functions.Load();
    Validation.Load();
});