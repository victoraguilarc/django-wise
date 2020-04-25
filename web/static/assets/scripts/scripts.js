$(document).ready(function () {
    var textFields = document.querySelectorAll('.mdc-text-field');
    for (var  i = 0; i <= textFields; i++) {
        mdc.textField.MDCTextField.attachTo(textFields[i]);
    }

    var buttons = document.querySelectorAll('.mdc-button');
    for (var  j = 0; j <= buttons; j++) {
        mdc.ripple.MDCRipple.attachTo(buttons[j]);
    }
});
