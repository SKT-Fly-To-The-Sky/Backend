/*##########################################################################################################################################################*/
/*#########################################################                                  ###############################################################*/
/*#########################################################          윈도우 관련             ###############################################################*/
/*#########################################################                                  ###############################################################*/
/*##########################################################################################################################################################*/

/*-------------------------------------------------------------------------
isChecked(feild_id)
argument :
return   : 선택된 value
example  : isChecked(field_id);"
-------------------------------------------------------------------------*/
function isChecked(value) {
    var returnValue = false;
    if (jQuery('input[id="'+ value + '"]').is(":checked")) {
        returnValue = true;
    }

    return returnValue;
}


/*-------------------------------------------------------------------------
getSelectedValue(feild_id)
argument :
return   : 선택된 value
example  : getSelectedValue(field_id);"
-------------------------------------------------------------------------*/
function getSelectedValue(value) {
    var returnValue = "";
    returnValue = $("#"+value+" > option:selected").val();
    return returnValue;
}

/*-------------------------------------------------------------------------
getRadioCheckedValue(feild_name)
argument :
return   : 선택된 value
example  : getRadioCheckedValue(feild_name);"
-------------------------------------------------------------------------*/
function getRadioCheckedValue(value) {
    var returnValue = "";
    returnValue = $(':radio[name="'+ value + '"]:checked').val();
    return returnValue;
}


/*-------------------------------------------------------------------------
isChecked(feild_id)
argument :
return   : 선택된 value
example  : isChecked(field_id);"
-------------------------------------------------------------------------*/
function checkboxLength(value) {
    var returnValue = $(':checkbox[name="'+ value + '"]:checked').length;
    return returnValue;
}

/*-------------------------------------------------------------------------
isChecked(feild_id)
argument :
return   : 선택된 value
example  : isChecked(field_id);"
-------------------------------------------------------------------------*/
function radioLength(value) {
    var returnValue = $(':radio[name="'+ value + '"]:checked').length;
    return returnValue;
}

// calander
/* Korean initialisation for the jQuery calendar extension. */
jQuery(function($){
	$.datepicker.regional['ko'] = {
		closeText: '닫기',
		prevText: '이전달',
		nextText: '다음달',
		currentText: '오늘',
		monthNames: ['1월(JAN)','2월(FEB)','3월(MAR)','4월(APR)','5월(MAY)','6월(JUN)',
		'7월(JUL)','8월(AUG)','9월(SEP)','10월(OCT)','11월(NOV)','12월(DEC)'],
		monthNamesShort: ['1월','2월','3월','4월','5월','6월',
		'7월','8월','9월','10월','11월','12월'],
		dayNames: ['일','월','화','수','목','금','토'],
		dayNamesShort: ['일','월','화','수','목','금','토'],
		dayNamesMin: ['일','월','화','수','목','금','토'],
		weekHeader: 'Wk',
		dateFormat: 'yy-mm-dd',
		firstDay: 0,
		isRTL: false,
		showMonthAfterYear: true,
		yearSuffix: ''};

	$.datepicker.setDefaults($.datepicker.regional['ko']);

	$('.datepick').datepicker({
	    //showOn: "button",
		//buttonText: "달력",
		showOn: "both",
	    buttonImage: "/images/btn/calendar.png",
	    buttonImageOnly: true,
	    changeMonth: true,
		changeYear: true,
	    yearRange: 'c-99:c+99'
	});//.next(".ui-datepicker-trigger").addClass("btn_black");


   $(".ui-datepicker-trigger").mouseover(function() {
  	$(this).css('cursor','pointer');
 	});

});

 //스크롤위치 쿠키저장하기
function setCookie( name, value, expiredays )  {
	var todayDate = new Date();
	todayDate.setDate( todayDate.getDate() + expiredays );
	document.cookie = name + "=" + escape( value ) + "; path=/; expires=" + todayDate.toGMTString() + ";"
}

//스크롤위치 쿠키불러오기
function getCookie( name ) {
	var nameOfCookie = name + "=";
	var x = 0;

	while ( x <= document.cookie.length ) {
		var y = (x+nameOfCookie.length);
		if ( document.cookie.substring( x, y ) == nameOfCookie ) {
		if ( (endOfCookie=document.cookie.indexOf( ";", y )) == -1 )
		endOfCookie = document.cookie.length;
		return unescape( document.cookie.substring( y, endOfCookie ) );
	}
		x = document.cookie.indexOf( " ", x ) + 1;
		if ( x == 0 )
		break;
	}
	return "";
}

function ck_korea_lan(str){
	var han = /[ㄱ-힣]/g;
	var chk_han = str.match(han);
	if(chk_han){
		return false;
	}
	return true;
}

function add_comma(what) {
	var flag = 1;
	var data = what;
	var len = data.length;

	if (data.charAt(0) == '-') {
		flag = 0;
		data = data.substring(1);
	}
	if (data.charAt(0) == '0' && data.charAt(1) == '-')	{
		flag = 0;
		data = data.substring(2);
	}

	var number = strip_comma(data);
	number = '' + number;
	if (number.length > 3) {
		var mod = number.length % 3;
		var output = (mod > 0 ? (number.substring(0,mod)) : '');

		for (ii=0; ii<Math.floor(number.length/3); ii++) {
			if ((mod == 0) && (ii == 0)) {
				output += number.substring(mod+3*ii, mod+3*ii+3);
			} else {
				output += ',' + number.substring(mod+3*ii, mod+3*ii+3);
			}
		}
		if (flag == 0) {
			return ('-' + output);
		} else {
			return (output);
		}
	} else {
		if (flag == 0) {
			return ('-' + number);
		} else {
			return (number);
		}
	}
}


/*-------------------------------------------------------------------------
 layer popup
-------------------------------------------------------------------------*/

function login(){$("#login").show();}
function find_id(){ $("#find_id").show();}
function view_case(){$("#view_case").show();}
function kakao(){$("#kakao").show();}
function pop_close(){
	$(".pop_area").hide();
}


//파일 확장자 제한
function uploadFileCheck( fileName ){
	if( fileName =="" ){
		//alert("파일을 업로드 해주세요.");
		//return false;
	}else{
		var fileSuffix = fileName.substring(fileName.lastIndexOf(".")+1);
		//확장자
		fileSuffix = fileSuffix.toLowerCase();
		//확장자 체크
		if( "bmp"== fileSuffix || "jpg"== fileSuffix || "jpeg"== fileSuffix || "gif"== fileSuffix){
			return true;
		}else{
			alert("이미지 파일만 업로드 가능합니다.");
			return false;
		}
	}
}
//파일 확장자 제한
function uploadFileCheckMp3( fileName ){
	if( fileName =="" ){
		//alert("파일을 업로드 해주세요.");
		//return false;
	}else{
		var fileSuffix = fileName.substring(fileName.lastIndexOf(".")+1);
		//확장자
		fileSuffix = fileSuffix.toLowerCase();
		//확장자 체크
		if( "M4a"== fileSuffix || "3gp"== fileSuffix){
			return true;
		}else{
			alert("3gp 파일만 업로드 가능합니다.");
			return false;
		}
	}
}



function resizeFrame(frm) {
	alert(frm);
	frm.style.height = "auto";
	contentHeight = frm.contentWindow.document.body.scrollHeight;
	frm.style.height = contentHeight + 4 + "px";
}

function resizeFrame2(iframeObj){
	resizeFrame(iframeObj);
	this.scrollTo(1,1);
}


function resizeFileFrame(iframeObj){
    var innerBody = iframeObj.contentWindow.document.body;
    var innerHeight = innerBody.scrollHeight + (innerBody.offsetHeight - innerBody.clientHeight);
    iframeObj.style.height = innerHeight;

    if( !arguments[1] ) {        /* 특정 이벤트로 인한 호출시 스크롤을 그냥 둔다. */
        this.scrollTo(1,1);
    }

    iframeObj.focus();
}


function resizeFrame(frm) {
	frm.style.height = "auto";
	contentHeight = frm.contentWindow.document.body.scrollHeight;
	frm.style.height = contentHeight + 4 + "px";
}

function resizeFrame2(iframeObj){
	resizeFrame(iframeObj);
	this.scrollTo(1,1);
}


function resizeFileFrame(iframeObj){
    var innerBody = iframeObj.contentWindow.document.body;
    var innerHeight = innerBody.scrollHeight + (innerBody.offsetHeight - innerBody.clientHeight);
    iframeObj.style.height = innerHeight;

    if( !arguments[1] ) {        /* 특정 이벤트로 인한 호출시 스크롤을 그냥 둔다. */
        this.scrollTo(1,1);
    }

    iframeObj.focus();
}


/*-------------------------------------------------------------------------
 Function : resizeFrame()
 Spec	  : Iframe Resize
 Argument : objName
 Return   : String
 Example  : onload="resizeFrame(this);"

function resizeFrame(iframeObj){
    var innerBody = iframeObj.contentWindow.document.body;
    oldEvent = innerBody.onclick;
    innerBody.onclick = function(){ resizeFrame(iframeObj, 1);oldEvent; };
    var innerHeight = innerBody.scrollHeight + (innerBody.offsetHeight - innerBody.clientHeight);
    iframeObj.style.height = innerHeight;

    //var innerWidth = innerBody.scrollWidth + (innerBody.offsetWidth - innerBody.clientWidth);
    //iframeObj.style.width = innerWidth;

    if( !arguments[1] ) {
        this.scrollTo(1,1);
    }
}


function resizeFrame2(iframeObj){
    var innerBody = iframeObj.contentWindow.document.body;
    oldEvent = innerBody.onclick;

    innerBody.onclick = function(){ resizeFrame(iframeObj, 1);oldEvent; };

    var innerHeight = innerBody.scrollHeight + (innerBody.offsetHeight - innerBody.clientHeight);
    iframeObj.style.height = innerHeight;

    //var innerWidth = innerBody.scrollWidth + (innerBody.offsetWidth - innerBody.clientWidth);
    //iframeObj.style.width = innerWidth;

    if( arguments[1] ) {
        this.scrollTo(1,1);
    }
}


function resizeFileFrame(iframeObj){
    var innerBody = iframeObj.contentWindow.document.body;
    var innerHeight = innerBody.scrollHeight + (innerBody.offsetHeight - innerBody.clientHeight);
    iframeObj.style.height = innerHeight;

    if( !arguments[1] ) {
        this.scrollTo(1,1);
    }

    iframeObj.focus();
}
*/

/*-------------------------------------------------------------------------
 Function : fn_Calendar()
 Spec	  : 달력
 Argument : objName
 Return   : String
 Example  : onclick="fn_Calendar(objName)"
-------------------------------------------------------------------------*/
function fn_Calendar(objName) {
	obj = eval(objName);

	var ls_Date = new Array();
	var ls_CurVal = obj.value;

	ls_Date = window.showModalDialog("/common/js/Calendar_day.html", ls_CurVal, "dialogTop:"+event.screenY+"; dialogLeft:"+eval(event.screenX-185)+"; dialogWidth:240px; dialogHeight:262px; Raised; resizable: no; status: no");

	if (ls_Date != null){
		obj.value = ls_Date;
	}
}


/*-------------------------------------------------------------------------
 Function : goto_byselect()
 Spec	  : 해당 페이지로 이동
 Argument : Target Frame, Move Page
 Return   :
 Example  : onchange="goto_byselect(sel, targetstr)"
-------------------------------------------------------------------------*/
function goto_byselect(sel, targetstr) {
	var index = sel.selectedIndex;

	if (sel.options[index].value != '') {
		if (targetstr == 'blank') {
			window.open(sel.options[index].value, 'win1');
		} else {
			var frameobj;
			if (targetstr == '') targetstr = 'self';
			if ((frameobj = eval(targetstr)) != null)
			frameobj.location = sel.options[index].value;
		}
	}
}


/*-------------------------------------------------------------------------
 change_state(sel, targetstr, pre_scode)
 Spec	  : 해당 페이지로 이동
 Argument : Target Frame, Move Page
 Return   :
 Example  : OnChange="change_state(this, 'self', pre_scode)"
-------------------------------------------------------------------------*/
function change_state(sel, targetstr, pre_scode) {

	if (confirm("상태를 변경 하시겠습니까?")) {
		var index = sel.selectedIndex;
		if (sel.options[index].value != '') {
			if (targetstr == 'blank') {
				window.open(sel.options[index].value, 'win1');
			} else {
				var frameobj;
				if (targetstr == '') targetstr = 'self';
				if ((frameobj = eval(targetstr)) != null)
				frameobj.location = sel.options[index].value;
			}
		}
	} else {
		sel.selectedIndex = pre_scode -1;
		return;
	}
}


/*-------------------------------------------------------------------------
 Function : goNoIframe()
 Spec	  : iframe 없애면서 이동시키기
 Argument : String
 Return   :
 Example  : goNoIframe(link)
-------------------------------------------------------------------------*/
function goNoIframe(link) {
	parent.self.location.replace(link);
}


/*-------------------------------------------------------------------------
 Function : windowOpen(), windowOpen2()
 Spec	  : 윈도우 Open
 Argument : String
 Return   :
 Example  : onclick="windowOpen(htmlFile, windowName, w, h)"
-------------------------------------------------------------------------*/
function windowOpen(htmlFile, windowName, w, h) {
	window.open(htmlFile, windowName, "toolbar=no, location=no, status=no, menubar=no, esizable=no, width="+w+",height="+h+"");
}

function windowOpen2(htmlFile, windowName, w, h) {

	window.open(htmlFile, windowName, "toolbar=no, location=no, status=no, menubar=no, resizable=yes,scrollbars=yes, width="+w+",height="+h+"");
}


/*-------------------------------------------------------------------------
 Function : moveFocus()
 Spec	  : 포커스이동
 Argument : Num, From form, To form
 Return   :
 Example  : onKeyUp="moveFocus(6, this, this.form.jumin2);"
-------------------------------------------------------------------------*/
function moveFocus(num, fromform, toform) {
	var str = fromform.value.length;

	if(str == num) {
		toform.focus();
	}
}


/*-------------------------------------------------------------------------
 Function : goto_byselect()
 Spec	  : 해당 페이지로 이동
 Argument : Target Frame, Move Page
 Return   :
 Example  : onchange="goto_byselect(this, 'self')"
-------------------------------------------------------------------------*/
function goto_byselect(sel, targetstr) {
	var index = sel.selectedIndex;
	if (sel.options[index].value != '') {
		if (targetstr == 'blank') {
			window.open(sel.options[index].value, 'win1');
		} else {
			var frameobj;
			if (targetstr == '') targetstr = 'self';
			if ((frameobj = eval(targetstr)) != null)
			frameobj.location = sel.options[index].value;
		}
	}
}

function goUrl (str) {
    location.href = str;
}



/*##########################################################################################################################################################*/
/*#########################################################                                  ###############################################################*/
/*#########################################################            Form 관련             ###############################################################*/
/*#########################################################                                  ###############################################################*/
/*##########################################################################################################################################################*/




/*-------------------------------------------------------------------------
 Function : checkMinMaxLen()
 Spec	  : 변수의 길이가 min 과 max 사이에 있는지 체크
 Argument : String, Min, Max
 Return   : boolean
 Example  : checkMinMaxLen( "dir" , 0, 4);
-------------------------------------------------------------------------*/
function checkMinMaxLen(str, min , max) {
	if( str.length >= min && str.length <= max ) {
		return true;
	} else {
		return false;
	}
}


/*-------------------------------------------------------------------------
 Function : isHangul()
 Spec	  : 변수값의 한글여부 체크
 Argument : String
 Return   : boolean
 Example  : isHangul('한글');
-------------------------------------------------------------------------*/
function isHangul( str ) {
	var bgn_hangul = parseInt(0xAC00, 10);	// '가'
	var end_hangul = parseInt(0xD79D, 10);	// '힝'

	for ( jdx = 0; jdx < str.length; jdx++ ) {
		sTempChar = str.substr(jdx,1).charCodeAt(0);

		if ( sTempChar < bgn_hangul || sTempChar > end_hangul ) {
			return false;
		}
	}
    return true;
}


/*-------------------------------------------------------------------------
 Function : isEnglish()
 Spec	  : 변수값의 영문여부 체크
 Argument : String
 Return   : boolean
 Example  : isEnglish('영문');
-------------------------------------------------------------------------*/
function isEnglish( str ) {
	for (var i =0 ; i < str.length; i++) {
		sTempChar = parseInt(str.substr(i,1).charCodeAt(0));
		if (  sTempChar < 64 ||  sTempChar > 123 ) {
			return false;
		}
	}

	return true;
}


/*-------------------------------------------------------------------------
 Function : isInteger()
 Spec	  : 변수값의 숫자여부 체크
 Argument : String
 Return   : boolean
 Example  : isInteger('숫자');
-------------------------------------------------------------------------*/
function isInteger( str ) {
	for (var i =0 ; i < str.length; i++) {
		sTempChar = str.substr(i,1).charCodeAt(0);

		if (sTempChar < 47 || sTempChar > 58) {
			return false;
		}
	}
	return true;
}


/*-------------------------------------------------------------------------
 Function : isEngInteger()
 Spec	  : 변수값의 영어, 숫자 여부 체크
 Argument : String
 Return   : boolean
 Example  : isEngInteger('scy0121');
-------------------------------------------------------------------------*/
function isEngInteger( str ) {
	for (var i =0 ; i < str.length; i++) {
		if(!isEnglish(str.substr(i,1)) && !isInteger(str.substr(i,1)) ) {
			return false;
		}
	}
    return true;
}


/*-------------------------------------------------------------------------
 Function : checkName()
 Spec	  : 변수값의 영문, 한글 여부 체크
 Argument : String
 Return   : boolean
 Example  : checkName('scy0121');
-------------------------------------------------------------------------*/
function checkName( str ) {
	for (var i =0 ; i < str.length; i++) {
		if (!isHangul(str.substr(i,1)) && !isEnglish(str.substr(i,1))) {
			return false;
		}
	}
	return true;
}


/*-------------------------------------------------------------------------
 Function : isNull()
 Spec	  : 변수값의 NULL 여부 체크
 Argument : String
 Return   : boolean
 Example  : isNull('scy0121');
-------------------------------------------------------------------------*/
function isNull( str ) {
	var chkstr = str + "";
	var Result = true;

	if ( (chkstr == "") || (chkstr == null) ) {
		return Result;
    }

	for ( jdx = 0; Result && (jdx < str.length); jdx++ ) {
		if ( str.substring(jdx, jdx+1) != " " ) {
			Result = false;
		}
	}
	return Result;
}


/*-------------------------------------------------------------------------
 Function : f_onlyNumber()
 Spec	  : Only Number
 Argument :
 Return   : boolean
 Example  : OnKeypress="f_onlyNumber();"  style="IME-MODE: inactive"
-------------------------------------------------------------------------*/
/*
function f_onlyNumber() {

	if (event.keyCode != 13) {
		if((event.keyCode < 48) || (event.keyCode > 57)) {
			alert("숫자항목에 문자를 입력할 수 없습니다.");
			event.returnValue = false;
		}
	}
}
*/


function getInternetExplorerVersion()
{
  var rv = -1;
  if (navigator.appName == 'Microsoft Internet Explorer')
  {
    var ua = navigator.userAgent;
    var re  = new RegExp("MSIE ([0-9]{1,}[\.0-9]{0,})");
    if (re.exec(ua) != null)
      rv = parseFloat( RegExp.$1 );
  }
  return rv;
}


function f_onlyNumber()
	{
	    var ver = getInternetExplorerVersion();

		if (event.keyCode != 13) {
			if((event.keyCode < 48) || (event.keyCode > 57)) {
			alert("【 항목체크 】: 숫자항목에 문자를 입력할 수 없습니다.");

				if(ver== 10 ||ver== 9||ver== 8||ver== 7||ver== 6||ver== 5){
			    }else{
					event.preventDefault();
				}
			event.returnValue = false;

			}
		}
	}

function NumberChk()
	{
	    var ver = getInternetExplorerVersion();

	      //특수문자 입력방지
          if ((event.keyCode > 32 && event.keyCode < 48) || (event.keyCode > 57 && event.keyCode < 65) || (event.keyCode > 90 && event.keyCode < 97)){
            alert("【 항목체크 】: 특수문자를 입력할 수 없습니다.");

           if(ver== 10 ||ver== 9||ver== 8||ver== 7||ver== 6||ver== 5){
			    }else{
					event.preventDefault();
				}
			event.returnValue = false;
          }

          //따옴표, 홑따옴표
          if (event.keyCode==34 || event.keyCode==39){
            alert("【 항목체크 】: 특수문자를 입력할 수 없습니다.");

            if(ver== 10 ||ver== 9||ver== 8||ver== 7||ver== 6||ver== 5){
			    }else{
					event.preventDefault();
				}
			event.returnValue = false;
          }


	}




/*-------------------------------------------------------------------------
 Function : f_checkByte()
 Spec	  : 바이트 수
 Argument : (document.chb.id)
 Return   : int
 Example  : f_checkByte(document.chb.id);
-------------------------------------------------------------------------*/
function f_checkByte(obj){
	var str,msg;
	var len = 0;
	var temp;
	var count = 0;

	msg = obj.value;
	str = new String(msg);
	len = str.length;

	for (k=0 ; k<len ; k++){
		temp = str.charAt(k);

		if (escape(temp).length > 4) {
			count += 2;
		}
		else if (temp == '\r' && str.charAt(k+1) == '\n') {	// \r\n일 경우
			var strPass = obj.value;
			var strLength = strPass.length;
			var tst = obj.value.substring(0, (strLength) - 2);
		}
		else if (temp != '\n') {
			count++;
		}
	}

	return count;
}



/*-------------------------------------------------------------------------
 Function : isID()
 Spec	  : 4~12자의 영문,숫자를 공백없이 조합
 Argument : String
 Return   : boolean
 Example  : isID(str);
-------------------------------------------------------------------------*/
function isID(str) {
	if(str.length < 6 || str.length > 15) {
		return false;
	}

	for(var i=0; i < str.length; i++) {
		var chr = str.substr(i,1);
		if((chr < '0' || chr > '9') && (chr < 'A' || chr > 'z')) {
			return false;
		}
	}
	return true;
}


/*-------------------------------------------------------------------------
 Function : isPassWord()
 Spec	  : 6~16자의 영문,숫자를 공백없이 조합
 Argument : String
 Return   : boolean
 Example  : isID(str);
-------------------------------------------------------------------------*/
function isPassWord(str) {
	if(str.length < 4 || str.length > 12) {
		return false;
	}

	for(var i=0; i < str.length; i++) {
		var chr = str.substr(i,1);
		if((chr < '0' || chr > '9') && (chr < 'A' || chr > 'z')) {
			return false;
		}
	}
	return true;
}

function new_pass_check(str) {

	if(str.length < 6 || str.length > 14) {
		return false;
	}

	var chk_num = str.search(/[0-9]/g);
	var chk_eng = str.search(/[a-z]/ig);

 	if(chk_num < 0 || chk_eng < 0){
		return false;
	}
	return true;



}



/*-------------------------------------------------------------------------
 Function : isJumin()
 Spec	  : 주민번호 체크
 Argument : String ('-' 제외 13자리)
 Return   : boolean
 Example  : isJumin(str);
-------------------------------------------------------------------------*/
function isJumin( str ) {
	var str1, str2, str3, str4, str5, str6, str7;
	var str8, str9, str10, str11, str12, str13;
	var Sum, Chk;
	var Result = false;

	if ( str.length == 13 ) {
		Result	= true;
		str1	= str.charAt(0);
		str2	= str.charAt(1);
		str3	= str.charAt(2);
		str4	= str.charAt(3);
		str5	= str.charAt(4);
		str6	= str.charAt(5);
		str7	= str.charAt(6);
		str8	= str.charAt(7);
		str9	= str.charAt(8);
		str10	= str.charAt(9);
		str11	= str.charAt(10);
		str12	= str.charAt(11);
		str13	= str.charAt(12);

		Sum = ( parseInt(str1) * 2 ) + ( parseInt(str2) * 3 ) +
			( parseInt(str3) * 4 ) + ( parseInt(str4) * 5 );
		Sum = parseInt(Sum) + ( parseInt(str5) * 6 ) +
			( parseInt(str6) * 7 ) + ( parseInt(str7) * 8 );
		Sum = parseInt(Sum) + ( parseInt(str8) * 9 ) +
			( parseInt(str9) * 2 ) + ( parseInt(str10) * 3 );
		Sum = Sum + ( parseInt(str11) * 4 ) +
			( parseInt(str12) * 5 );

		Chk = Sum % 11;
		Chk = 11 - Chk;


		if ( Chk == 11 ) {
			Chk = 1;
        } else if ( Chk == 10 ) {
			Chk = 0;
		}

		if ( str13 != Chk ) {
			Result = false;
		}

	} else {
		Result = false;
	}

    return Result;
}


/*-------------------------------------------------------------------------
 Function : isJumin()
 Spec	  : 사업자 번호 체크
 Argument : String ('-' 제외 10자리)
 Return   : boolean
 Example  : isBusiNumber(num);
-------------------------------------------------------------------------*/
function isBusiNumber(num) {

	var temp, comp, ld_1, ld_2, ld_3, ld_4, ld_5, ld_6, ld_7, ld_8, ld_9, ld_10;

	if ( num.length != 10 ) {
		return false;
	}

	ld_1  = num.substr(0,1);
	ld_2  = num.substr(1,1);
	ld_3  = num.substr(2,1);
	ld_4  = num.substr(3,1);
	ld_5  = num.substr(4,1);
	ld_6  = num.substr(5,1);
	ld_7  = num.substr(6,1);
	ld_8  = num.substr(7,1);
	ld_9  = num.substr(8,1);
	ld_10 = num.substr(9,1);

	temp =  ( ld_1 * 1 ) % 10
		  + ( ld_2 * 3 ) % 10
		  + ( ld_3 * 7 ) % 10
		  + ( ld_4 * 1 ) % 10
		  + ( ld_5 * 3 ) % 10
		  + ( ld_6 * 7 ) % 10
		  + ( ld_7 * 1 ) % 10
		  + ( ld_8 * 3 ) % 10
		  + ( ld_9 * 5 ) % 10 + Math.floor( ( ld_9 * 5 ) / 10 )  ;

	comp = temp % 10;

	if ( ld_10 == ( 10 - comp ) ) {
		return true;
	} else {
		if ( ( comp == 0 ) && ( ld_10 == 0 ) ) {
			return true;
		} else {
			return false;
		}
	}
}


/*-------------------------------------------------------------------------
 Function : checkEmail()
 Spec	  : 이메일 유효체크
 Argument : String
 Return   : boolean
 Example  : checkEmail(strEmail);
-------------------------------------------------------------------------*/
function checkEmail(strEmail) {
	var arrMatch = strEmail.match(/^(\".*\"|[A-Za-z0-9_-]([A-Za-z0-9_-]|[\+\.])*)@(\[\d{1,3}(\.\d{1,3}){3}]|[A-Za-z0-9][A-Za-z0-9_-]*(\.[A-Za-z0-9][A-Za-z0-9_-]*)+)$/);
	if (arrMatch == null) {
		return false;
	}

	var arrIP = arrMatch[2].match(/^\[(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})\]$/);

	if (arrIP != null) {
		for (var i = 1; i <= 4; i++) {
			if (arrIP[i] > 255) {
				return false;
			}
		}
	}
	return true;
}


/*-------------------------------------------------------------------------
 Function : checkImage()
 Spec	  : 이미지 파일체크
 Argument : String
 Return   : boolean
 Example  : checkImage(str);
-------------------------------------------------------------------------*/
function checkImage(str) {

	var strlen	= str.length;
	var ext		= (str.substr(strlen-4, 4)).toLowerCase();
	var flag	= false;

	if( ext == '.jpg') {
		flag = true;
	}
	if( ext == '.gif') {
		flag = true;
	}
	if( ext == 'jpeg') {
		flag = true;
	}
	if( ext == '.bmp') {
		flag = true;
	}

	return flag;
}


/*-------------------------------------------------------------------------
 Function : checkMedia()
 Spec	  : 미디어 파일체크
 Argument : String
 Return   : boolean
 Example  : checkMedia(str);
-------------------------------------------------------------------------*/
function checkMedia(str) {

	var strlen	= str.length;
	var ext		= (str.substr(strlen-4, 4)).toLowerCase();
	var flag	= false;

	if( ext == '.mpg') {
		flag = true;
	}
	if( ext == '.mpeg') {
		flag = true;
	}
	if( ext == '.asf') {
		flag = true;
	}
	if( ext == '.avi') {
		flag = true;
	}
	if( ext == '.wmv') {
		flag = true;
	}

	return flag;
}


/*-------------------------------------------------------------------------
 Function : Check_msg()
 Spec	  : 아이디와 메세지를 받아서 메세지를 뿌리고 포커스 이동
 Argument : Form Name, String
 Return   : boolean
 Example  : Check_msg("name","이름을 입력해 주시기 바랍니다.")
-------------------------------------------------------------------------*/
//### 아이디와 메세지를 받아서 메세지를 뿌리고 포커스를 잡아준다.
function Check_msg(id, msg) {

	if(document.all[id].value == "" || document.all[id].value.length < 0 || document.all[id].value == " ") {
		alert(msg);

		if(document.all[id].style.display != "none"){
			document.all[id].focus();
		}

		return false;
	} else {
		return true;
	}
}

/*-------------------------------------------------------------------------
 Function : jsFComma2()
 Spec	  : 숫자형 데이터 콤마 삽입
 Argument :
 Return   :
 Example  : loadPosition()
-------------------------------------------------------------------------*/

var selind;

// 숫자 유효성 체크
function jsFComma2( obj ) {
	if ( event.keyCode == 16 && event.srcElement.isTextEdit) return false;

	if( (event.type == 'keyup' && event.keyCode == 13) || event.keyCode == 9 ) {
		event.returnValue = true;
		return;
	}

	if ( obj.value.length > 1 && obj.value.charAt(0) == '0' ) {
		obj.value = obj.value.substring(1);
		selind = 0;
		event.cancelBubble = true;
		return;
	}


	var val  = obj.value;
	var sign = '';

	obj.value = sign + jsFInsComma(val);
}

// Comma 삽입
function jsFInsComma(val)
{
   var vals = "";
   vals = val.toString();
   if ( (selind == 1) && (event.type == "keydown") && (event.keyCode != 13) )
   {
       selind = 0;
       event.cancelBubble = true;
       return "";
   }
   if (vals.indexOf(".") != -1 )
   {
       var dotpos = vals.split(".");
       if ( dotpos[1].length > 2 )
       {
           event.cancelBubble = true;
           event.returnValue = false;
           vals = vals.substring( 0, vals.length - 1);
           if ( event.type == "keyup" ) alert(".");
           return vals;
       }
   }
   var pas = "";
   comma=/,/gi;
   var sol = jsfDchk2(vals.replace(comma,''));
   for ( i=0; i<sol.length; i++ )
   {
      pas += sol[i];
   }
   return pas;
}

function jsfDchk2(num)
{
    num = num.toString();
    var dot    = 0;
    var minus  = 0;
    var dottmp = new Array();
    dot   = ( num.indexOf(".") != -1 )? num.length - num.indexOf("."): 0;
    minus = ( num.indexOf("-") != -1 )? num.length - num.indexOf("-"): 0;
    var vlen = num.length - dot;
    var c = 1;
    var tmp = new Array();

    if(minus > 1)
    {
        for ( i = vlen ; i > -1; i-- )
        {
            c++;
            tmp[i] = ( ( c%3 == 0 ) && ( i != vlen - 1) )? num.charAt(i) + "," : num.charAt(i);
            if(i == 0)
             tmp[i] = num.charAt(i);
        }
        if ( dot > 1 )
        {
            var numArr = num.split(".");
            if ( numArr != null )
            {
                for ( var i = 0; i < tmp.length; i++ )
                {
                   dottmp[i] = tmp[i];
                }
                dottmp[tmp.length-1] = dottmp[tmp.length-1] + numArr[1];
                return dottmp;
            }
        }
       return tmp;
    }
    else
    {
        for ( i = vlen ; i > -1; i-- )
        {
            c++;
            tmp[i] = ( ( c%3 == 0 ) && ( i != vlen - 1) )? num.charAt(i) + "," : num.charAt(i);
        }
        if ( dot > 1 )
        {
            var numArr = num.split(".");
            if ( numArr != null )
            {
                for ( var i = 0; i < tmp.length; i++ )
                {
                   dottmp[i] = tmp[i];
                }
                dottmp[tmp.length-1] = dottmp[tmp.length-1] + numArr[1];
                return dottmp;
            }
        }
       return tmp;
    }
}

// 숫자여부 체크( 이벤트형)
function jsfChkCode()
{
  if ( event.keyCode == 37 || event.keyCode == 39 || event.keyCode == 46)
  {
    event.returnValue = true;
  }
  else
  {
    if (!event.shiftKey)
    {
      if (event.keyCode > 47)
      {
        if( event.keyCode < 58)
        {
          event.returnValue = true;
        }
        else if (event.keyCode > 95 )
        {
          if (event.keyCode < 106)
          {
             event.returnValue = true;
          }
          else
          event.returnValue = false;
        }
        else
          event.returnValue = false;
      }
      else if ( event.keyCode == 8 || event.keyCode == 9 || event.keyCode == 32)
      {
         event.returnValue = true;
      }
      else
        event.returnValue = false;
    }
    else
     event.returnValue = false;
  }
}

/*-------------------------------------------------------------------------
 Function : MM_openBrWindow()
 Spec	  : 팝업
 Argument :
 Return   :
 Example  :
-------------------------------------------------------------------------*/

function MM_openBrWindow(theURL,winName,features) { //v2.0
  window.open(theURL,winName,features);
}

/*-------------------------------------------------------------------------
 Function : showHideMe()
 Spec	  : 숨기기 보이기
 Argument : id 명
 Return   :
 Example  :
-------------------------------------------------------------------------*/

function showHideMe(objView) {

	var varObj = eval("document.all."+ objView );

	if( varObj.style.display == "" ){
		varObj.style.display = "none";
	}else{
		varObj.style.display = "";
	}
}


/*-------------------------------------------------------------------------
 Function : strip_comma()
 Spec	  : 숫자형변수 콤마 없애기
 Argument : String
 Return   : String
 Example  : strip_comma(val)
-------------------------------------------------------------------------*/
function strip_comma(data) {
	var flag = 1;
	var valid = "1234567890";
	var output = '';
	if (data.charAt(0) == '-') {
		flag = 0;
		data = data.substring(1);
	}

	for (var i=0; i<data.length; i++) {
		if( data.charAt(i)=="."){ break; }
		if (valid.indexOf(data.charAt(i)) != -1) {
			output += data.charAt(i);
		}

	}

	if (flag == 1) {
		return output;
	} else if (flag == 0) {
		return ('-' + output);
	}
}

/*-------------------------------------------------------------------------
 Function : member_check()
 Spec	  : 로그인
 Argument : String
 Return   : boolean
 Example  : isEnglish('영문');
-------------------------------------------------------------------------*/
function member_check(check_flag) {
	if( check_flag=="U" || check_flag=="P" ){
		return true;
	}else{
		alert("유료회원및 프리미엄회원만 사용가능 합니다.");
		return false;
	}
}

/*-------------------------------------------------------------------------
Function : os_check()
Spec	  : 연결 os check
Argument :
Return   : boolean
Example  :
-------------------------------------------------------------------------*/
function os_check() {
	var isAndroid;
	var iOS;
	var ua = navigator.platform.toLowerCase();
	var iDevice = ['ipad','iphone','ipod','android']

	for ( i = 0 ; i < iDevice.length ; i++ ) {
	    if( ua === iDevice[i] ){ return false; }
	}
	return true;
}

// 매장 조회
function getStore(){
	var brand_cd = $("#brand_cd").val();

	$.ajax({
		type: "POST",
		url : "/common/ajax/ajax.getStore.php",
		data	:
		{
			"brand_cd" : brand_cd
		},
		success	: function (res) {

			initStore();
			var arrResult = res.split("|");
			var store_seq = document.getElementById("store_seq");
			store_seq.options[0] = new Option('매장선택', '');
			for( var i=1; i<= arrResult.length; i++ ){
				if( arrResult[i-1] !="" ){
					var result = arrResult[i-1].split(",");
					store_seq.options[i] = new Option(result[1], result[0]);

				}
			}
		},
		error: function (res) {
			alert(res.responseText);
		}

	});
}

function getStore2(){
	var brand_cd = $("#brand_cd").val();
	var region_cd = $("#region_cd").val();
	$.ajax({
		type: "POST",
		url : "/common/ajax/ajax.getStore.php",
		data	:
		{
			"brand_cd" : brand_cd, "region_cd" : region_cd
		},
		success	: function (res) {

			initStore();
			var arrResult = res.split("|");
			var store_seq = document.getElementById("store_seq");
			store_seq.options[0] = new Option('매장선택', '');
			for( var i=1; i<= arrResult.length; i++ ){
				if( arrResult[i-1] !="" ){
					var result = arrResult[i-1].split(",");
					store_seq.options[i] = new Option(result[1], result[0]);

				}
			}
		},
		error: function (res) {
			alert(res.responseText);
		}

	});

}

// 카테고리 조회
function getCategory1(code_yn){
	var cate_cd = $("#cate_cd1").val();

	$.ajax({
		type: "POST",
		url : "/common/ajax/ajax.getCategory.php",
		data	:
		{
			"cate_cd" : cate_cd, "gubun": "1", "code_yn":code_yn
		},
		success	: function (res) {

			initCategory1();
			initCategory2();

			var arrResult = res.split("|");
			var category_cd = document.getElementById("cate_cd2");
			category_cd.options[0] = new Option('증상선택', '');
			for( var i=1; i<= arrResult.length; i++ ){
				if( arrResult[i-1] !="" ){
					var result = arrResult[i-1].split(",");
					category_cd.options[i] = new Option(result[1], result[0]);

				}
			}
		},
		error: function (res) {
			alert(res.responseText);
		}

	});


}

function initStore(){
	var store_seq = document.getElementById("store_seq");
	for( i=store_seq.options.lenght; i>=0; i-- ){
		store_seq.options[i] = null;
	}
	store_seq.options[0] = new Option('매장', '');
	store_seq.length=1;

}

function toPrice(money, cipher) {
	var len, strb, revslice;
	strb = money.toString();
	strb = strb.replace(/,/g, '');
	strb = getOnlyNumeric(strb);
	strb = parseInt(strb, 10);
	if(isNaN(strb))
		return '';
	strb = strb.toString();
	len = strb.length;

	if(len < 4)
		return strb;
	if(cipher == undefined)
		cipher = 3;

	count = len/cipher;
	slice = new Array();
	for(var i=0; i<count; ++i) {
		if(i*cipher >= len)
			break;
		slice[i] = strb.slice((i+1) * -cipher, len - (i*cipher));
	}
	revslice = slice.reverse();
	return revslice.join(',');
}

function getOnlyNumeric(str) {
	var chrTmp, strTmp;
	var len;

	len = str.length;
	strTmp = '';

	for(var i=0; i<len; ++i) {
		chrTmp = str.charCodeAt(i);
		if((chrTmp > 47 || chrTmp <= 31) && chrTmp < 58) {
			strTmp = strTmp + String.fromCharCode(chrTmp);
		}
	}
	return strTmp;
}

//모바일 여부체크
function mobilecheck() {
	var check = false;
    (function(a,b){if(/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce|xda|xiino/i.test(a)||/1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(a.substr(0,4)))check = true})(navigator.userAgent||navigator.vendor||window.opera);
    return check;
}

//SNS공유하기

function doShare(btn) {
	if($("#origin_url").val() == "" || $("#origin_url").val() == undefined){
		var origin_url 	= location.href;
	} else {
		var origin_url 	= "http://"+$("#origin_url").val();
	}

	var title 		= $("#sns_share_title").val();
	var sub_title   = $("#sns_share_sub_title").val();
	var img         = $("#sns_image").val();
	var option		= "toolbar=yes,directories=yes,status=yes,menubar=yes,resizable=yes,scrollbars=yes";

	if (btn == "T") {
		window.open("https://twitter.com/intent/tweet?url=" + encodeURIComponent(origin_url) + "&t=" + encodeURIComponent(title), "twitter", option+",width=626,height=300");
	} else if (btn == "F") {
		window.open("http://www.facebook.com/sharer.php?u=" + encodeURIComponent(origin_url) + "&t=" + encodeURIComponent(title), "facebook", option+",width=626,height=436");
	} else if (btn == "N") {
		window.open("http://share.naver.com/web/shareView.nhn?url=" + encodeURIComponent(origin_url) + "&title=" + encodeURIComponent(title), "blog", option+",width=600,height=300");
	} else if (btn == "C") {
		var elm = document.getElementById("share_clipboard");
		// for Internet Explorer
		if(document.body.createTextRange) {
			var range = document.body.createTextRange();
			range.moveToElementText(elm);
			range.select();
			document.execCommand("Copy");
			alert("복사되었습니다.");
		}
		else if(window.getSelection) {
		// other browsers
			var selection = window.getSelection();
			var range = document.createRange();
			range.selectNodeContents(elm);
			selection.removeAllRanges();
			selection.addRange(range);
			document.execCommand("Copy");
			alert("복사되었습니다.");
		}

	}else if( btn =="K" ){


		//<![CDATA[
	    // // 카카오링크 버튼을 생성합니다. 처음 한번만 호출하면 됩니다.
	    Kakao.Link.createDefaultButton({
	      container: '#kakao-link-btn',
	      objectType: 'feed',
	      content: {
	        title: title,
	        description: title,
	        imageUrl: img,
	        link: {
	          mobileWebUrl: origin_url,
	          webUrl: origin_url
	        }
	      },
	      buttons: [
	        {
	          title: '웹으로 보기',
	          link: {
	            mobileWebUrl: origin_url,
	            webUrl: origin_url
	          }
	        },
	        {
	          title: '앱으로 보기',
	          link: {
	            mobileWebUrl: origin_url,
	            webUrl: origin_url
	          }
	        }
	      ]
	    });
	  //]]>
	}
}



function copyToClipboad(){
	var reurl = document.location.href;
	var textArea = document.createElement("textarea");
	// Place in top-left corner of screen regardless of scroll position.
	textArea.style.position = 'fixed';
	textArea.style.top = 0;
	textArea.style.left = 0;

	// Ensure it has a small width and height. Setting to 1px / 1em
	// doesn't work as this gives a negative w/h on some browsers.
	textArea.style.width = '2em';
	textArea.style.height = '2em';

	// We don't need padding, reducing the size if it does flash render.
	textArea.style.padding = 0;

	// Clean up any borders.
	textArea.style.border = 'none';
	textArea.style.outline = 'none';
	textArea.style.boxShadow = 'none';

	// Avoid flash of white box if rendered for any reason.
	textArea.style.background = 'transparent';


	textArea.value = reurl;

	document.body.appendChild(textArea);

	textArea.select();
	var msg = "2";
	try {
		var successful = document.execCommand('copy');
	  	msg = successful ? '1' : '2';
	  	//alert('Copying text command was ' + msg);
	} catch (err) {
		//window.prompt("Copy to clipboard: Ctrl+C, Enter", reurl);
	}
	document.body.removeChild(textArea);

	if( msg=="1" ){
		alert("URL이 복사되었습니다.");
		return;
	}else{
		temp = window.prompt("해당페이지의 주소입니다. Ctrl+C를 눌러 클립보드로 복사하세요", reurl);
	}

}
//한글입력방지
// 사용 onkeyup=
function noKorean(obj){
	patt = /[`~!@\#$;%^&*\(),.\-=+_']/gi;
	if (patt.test(obj.value)) {
		obj.value=obj.value.replace( patt, '' ) ;
	}
	nowCarePosition=doGetCaretPosition(obj);
 	obj.value=obj.value.replace( /[\ㄱ-ㅎㅏ-ㅣ|가-힣]/g, '' ) ;
 	setCaretPosition(obj,nowCarePosition);

}

function doGetCaretPosition (ctrl) {
	var CaretPos = 0;
 	// IE Support
 	if (document.selection) {
		ctrl.focus ();
  		var Sel = document.selection.createRange ();
  		Sel.moveStart ('character', -ctrl.value.length);
		CaretPos = Sel.text.length;
	// Firefox support
 	}else if (ctrl.selectionStart || ctrl.selectionStart == '0'){
  		CaretPos = ctrl.selectionStart;
	}
 	return (CaretPos);
}

function setCaretPosition(ctrl, pos){
	if(ctrl.setSelectionRange){
  		ctrl.focus();
  		ctrl.setSelectionRange(pos,pos);
 	}else if (ctrl.createTextRange) {
  		var range = ctrl.createTextRange();
  		range.collapse(true);
  		range.moveEnd('character', pos);
  		range.moveStart('character', pos);
  		range.select();
 	}
}

//kakao init
//var kakao_key ="fcbe60ad8382b53ba57d78e6351b85d1";
//Kakao.init('fcbe60ad8382b53ba57d78e6351b85d1');

/*패스워드 체크*/
function PwdHandler(){
    var user_id = document.getElementById('user_id').value;
    var password = document.getElementById('password').value;
    var password_check = document.getElementById('password_check').value;
    //var regex = /^(?=.*[a-zA-Z])(?=.*[^a-zA-Z0-9])(?=.*[0-9]).{8,16}$/;
	var regex = /^(?=.*[a-zA-Z])(?=.*[^a-zA-Z0-9])(?=.*[0-9])(?!.*\s).{8,16}$/; //공백미포함

	if(!regex.test(password) || (password.length < 7 || password > 16)){
		document.getElementById('whether').style.display = 'block';
    	document.getElementById('impossible').style.display = 'block';
    	document.getElementById('possible').style.display = 'none';
		document.getElementById('password_pass').value='';
		return false;
	} else {
		document.getElementById('whether').style.display = 'none';

	}

	/*아이디 포함여부
		if(password.indexOf(user_id)!=-1){

		}
	*/

    if(password!=password_check){
    	document.getElementById('impossible').style.display = 'block';
    	document.getElementById('possible').style.display = 'none';
    	document.getElementById('password_pass').value='';
    	return false;
    }

    if(password==password_check){
      	document.getElementById('impossible').style.display = 'none';
    	document.getElementById('possible').style.display = 'block';
    	document.getElementById('password_pass').value='Y';
    	return true;
    }
}
/*패스워드 체크*/

/*이메일*/
function EmailChange(val){
    if(val=='S'){
        $("#email2").val('');
        $("#email2").attr("readonly",false);
    }else if(val!=''){
        $("#email2").val($("#email3").val());
        $("#email2").attr("readonly",true);
    }else{
    	$("#email2").val('');
        $("#email2").attr("readonly",true);
    }

}
/*이메일*/