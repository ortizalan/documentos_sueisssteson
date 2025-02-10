
$('#asunto').val('3'); // Select the option with a value of '1'
$('#asunto').trigger('change'); // Notify any JS components that the value changed

function myFunction(p1, p2) {
    return p1 * p2;
    }
let result = myFunction(5,5);
document.getElementById("demo").innerHTML = result;

////////////////////////////////////////////////////

$('input[name=es_pens]').change(function() {
    if($(this).is(':checked')){
        document.getElementById('trabajador').readOnly = true;
    } else {
        document.getElementById('trabajador').readOnly = false;
    }
});

var checkedkValue = null;
var inputElement = document.getElementsById('es_pens');
if(inputElement.checked){
    alert('Hola');
}

function validar(){
    if(document.getElementById("es_pens").checked){
        document.getElementById("trabajador").readOnly = true;
        document.getElementById("pensionado").readOnly = false;
        document.getElementById("trabajador").value = 0;
        document.getElementById("val_trabajador").hidden = true;
        document.getElementById("val_pensionado").hidden = false;
    } else {
        document.getElementById("pensionado").readOnly = true;
        document.getElementById("trabajador").readOnly = false;
        document.getElementById("pensionado").value = 0;
        document.getElementById("val_trabajador").hidden = false;
        document.getElementById("val_pensionado").hidden = true;
    } 
}

function getValue(param){
    //window.alert('valor es ' + param);
    setValue(param);
}

function setValue(param){
    var pen = document.getElementById('es_pens');
    if(pen.checked){
        //window.alert('Checked ' + param);
        var num = document.getElementById("pensionado");
        num.value = param;
        $('#mpensionados').modal('hide');
    }
    else{
        //window.alert('No-Checked ' + param);
        var num = document.getElementById("trabajador");
        num.value = param;
        $('#mtrabajadores').modal('hide');
    }
    
}

function valCheckBox(){
    var chk = document.getElementById('es_pens');
    if(chk.checked){
        var inp = document.getElementById("sel_check")
        inp.value = 1;
    }else{
        var inp = document.getElementById("sel_check")
        inp.value = 0;
    }
}