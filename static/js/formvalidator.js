$(document).ready(function() {
  $.validator.setDefaults({
    errorPlacement: function(error, element) {
      // if the input has a prepend or append element, put the validation msg after the parent div
      if(element.parent().hasClass('input-prepend') || element.parent().hasClass('input-append')) {
        error.insertAfter(element.parent());
      // else just place the validation message immediatly after the input
      } else {
        error.insertAfter(element);
      }
    },
    errorElement: "small", // contain the error msg in a small tag
    wrapper: "div", // wrap the error message and small tag in a div
    highlight: function(element) {
      $(element).closest('.control-group').addClass('error'); // add the Bootstrap error class to the control group
    },
    success: function(element) {
      $(element).closest('.control-group').removeClass('error'); // remove the Boostrap error class from the control group
    }
  });
});

$(document).ready(function() {
  $('#customer_form').validate(
  {
    rules: {
      name: {
        minlength: 2,
        required: true
      },
      address: {
        minlength: 2,
        required: true
      },
      cellno: {
        minlength: 2,
        required: true
      },
      email: {
        required: true,
        email: true
      }
    }
  });

  $('#user_form').validate(
  {
    rules: {
      username: {
        minlength: 3,
        required: true
      },
      password: {
        minlength: 6,
        required: true
      },
      password2: {
        minlength: 6,
        required: true
      },
      email: {
        required: true,
        email: true
      }
    }
  });

  $('#loan_form').validate(
  {
    rules: {
      date_rel: {
        required: true,
        date: true
      },
      date_due: {
        required: true,
        date: true
      },
      amount: {
        required: true,
        number: true
      },
      t_payable: {
        required: true,
        number: true
      },
      t_payment: {
        required: true,
        number: true
      },
      outs_bal: {
        required: true,
        number: true
      },
      fully_paidon: {
        required: true,
        date: true
      },
    }
  });
});

$(document).ready(function(){
   $('#amount').change(function(){
      var percent = $("#interest").val() / 100;
      var amount = $('#amount').val();
      var t_pay = parseFloat(amount) + parseFloat(amount * percent);
      $('#t_payable').val(t_pay);
      $('#t_payment').change();
  });

  $('#interest').change(function(){
      var percent = $("#interest").val() / 100;
      var amount = $('#amount').val();
      var t_pay = parseFloat(amount) + parseFloat(amount * percent);
      $('#t_payable').val(t_pay);
      $('#t_payment').change();
  });

  $('#payment').change(function(){
     var tpayment = parseFloat($('#totalpayment_hv').val());
     var payment = parseFloat($('#payment').val());
     if(tpayment){
         payment += parseFloat(tpayment);
     }
     $('#t_payment').val(payment);
     $('#t_payment').change();
  });

  $('#t_payment').change(function(){
      try{
          var tpayable = parseFloat($('#t_payable').val());
          var tpayment = parseFloat($('#t_payment').val());
          if(!tpayment){
            $('#outs_bal').val(tpayable);
          }else{
              $('#outs_bal').val(tpayable - tpayment);
          }
      }catch(err){
          alert("error: " + err.message);
      }
  });

    $('#interest').val(Math.round($('#interest_hv').val()));
    $('#privilege').val($('#privilege_hv').val());
});