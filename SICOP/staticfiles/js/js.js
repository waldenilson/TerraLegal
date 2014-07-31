function editarID(theUrl)
{
document.location.href = theUrl;
}

$(function() {
$( "#tabs" ).tabs();
});
$(function() {
$( "#accordion" ).accordion();
});
$(function() {
	$( "#dialog-modal" ).dialog({
		modal: true
});
});
$(function() {
$( "#menu" ).menu();
});
function my_callback(data){
    alert(data.message);
    
}


jQuery(function($){
$("#date").mask("99/99/9999");
$("#date2").mask("99/99/9999");
$("#date3").mask("99/99/9999");
$("#date4").mask("99/99/9999");
$("#datePicker").mask("99/99/9999");
$("#cpf").mask("999.999.999-99");
$("#cpf2").mask("999.999.999-99");
$("#cnpj").mask("99.999.999/9999-99");
$("#processo").mask("99999.999999/9999-99");
$("#processo2").mask("99999.999999/9999-99");
$("#telefone1").mask("(99)9999-9999");
$("#telefone2").mask("(99)9999-9999");
$("#moeda").mask("999.999.999,99");

});

function proc()
{
if (document.form.escolha.value != "0") {
document.form.submit();
}
}

function somardia1()
{
var dtInicio1 = document.getElementById("id_myDate");
var dtFim1 = document.getElementById("date");
var nrDias1 = document.getElementById("nrDias1");
//mudar aqui de dmy para mdy
var dataMDY1 = dtInicio1.value.substr(3,2) + '/' + dtInicio1.value.substr(0,2) + '/' +dtInicio1.value.substr(6,4);
var data1 = new Date(dataMDY1);
data1.setDate(data1.getDate() + parseInt(nrDias1.value) - 1 );

var dd = data1.getDate();
var mm = data1.getMonth() + 1;
var yy = data1.getFullYear();
var someFormattedDate1 = dd + '/'+ mm + '/' + yy;
dtFim1.value = someFormattedDate1;

}

function somardia2()
{
var dtInicio2 = document.getElementById("id_myDate2");
var dtFim2 = document.getElementById("date2");
var nrDias2 = document.getElementById("nrDias2");

//mudar aqui de dmy para mdy
var dataMDY2 = dtInicio2.value.substr(3,2) + '/' + dtInicio2.value.substr(0,2) + '/' +dtInicio2.value.substr(6,4);
var data2 = new Date(dataMDY2);
data2.setDate(data2.getDate() + parseInt(nrDias2.value) - 1);

var dd2 = data2.getDate();
var mm2 = data2.getMonth() + 1;
var yy2 = data2.getFullYear();
var someFormattedDate2 = dd2 + '/'+ mm2 + '/' + yy2;
dtFim2.value = someFormattedDate2;
}

function somardia3()
{
var dtInicio3 = document.getElementById("id_myDate3");
var nrDias3 = document.getElementById("nrDias3");
var dtFim3 = document.getElementById("date3");

//mudar aqui de dmy para mdy
var dataMDY3 = dtInicio3.value.substr(3,2) + '/' + dtInicio3.value.substr(0,2) + '/' +dtInicio3.value.substr(6,4);
var data3 = new Date(dataMDY3);
data3.setDate(data3.getDate() + parseInt(nrDias3.value) - 1 );

var dd3 = data3.getDate();
var mm3 = data3.getMonth() + 1;
var yy3 = data3.getFullYear();
var someFormattedDate3 = dd3 + '/'+ mm3 + '/' + yy3;
dtFim3.value = someFormattedDate3;
}

$(function() {
    $( "#id_myDate" ).datepicker({
     dateFormat: "dd/mm/yy",
     numberOfMonths: 1,
     changeMonth: true,
     changeYear: true,
     showOn: "button",
     buttonImage: '/static/img/calendar.gif',
     buttonImageOnly: true,
     altField: "#alternate",
     altFormat: "dd/mm/yy"
     });
});

$(function() {
    $( "#id_myDate2" ).datepicker({
     dateFormat: "dd/mm/yy",
     numberOfMonths: 1,
     changeMonth: true,
     changeYear: true,
     showOn: "button",
     buttonImage: '/static/img/calendar.gif',
     buttonImageOnly: true,
     altField: "#alternate2",
     altFormat: "dd/mm/yy"
    
    });
});

$(function() {
    $( "#id_myDate3" ).datepicker({ dateFormat: "dd/mm/yy",
     numberOfMonths: 1,
     changeMonth: true,
     changeYear: true,
     showOn: "button",
     buttonImage: '/static/img/calendar.gif',
     buttonImageOnly: true,
     altField: "#alternate3",
     altFormat: "dd/mm/yy"
     });
});



function SomenteNumero(e, obj)
{


var tecla=(window.event)?event.keyCode:e.which;
if((tecla>47 && tecla<58)) return true;
else
{

if (tecla==8 || tecla==0 ) return true;
else
if(tecla==44)
{
if ( obj.value.split(',').length > 1 )
return false;
else
if ( obj.value.split('.').length > 1 )
return false;
else
return true;
}
else
if(tecla==46)
{
if ( obj.value.split('.').length > 1 )
return false;
else
if ( obj.value.split(',').length > 1 )
return false;
else
return true;
}
else
return false;

}
}

function SomenteNumeroOK(e, obj)
{
var tecla=(window.event)?event.keyCode:e.which;
if((tecla>47 && tecla<58)) return true;
else
{
if (tecla==8 || tecla==0 ) return true;
else
return false;
}
}
