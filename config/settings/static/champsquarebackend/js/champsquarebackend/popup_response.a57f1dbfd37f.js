/*global opener */
(function() {
    'use strict';
    var initData = JSON.parse(document.getElementById('champsquarebackend-popup-response-constants').dataset.popupResponse);
    switch(initData.action) {
    case 'change':
        opener.champsquarebackend.dismissChangeRelatedObjectPopup(window, initData.value, initData.obj, initData.new_value);
        break;
    case 'delete':
        opener.champsquarebackend.dismissDeleteRelatedObjectPopup(window, initData.value);
        break;
    default:
        opener.champsquarebackend.dismissAddRelatedObjectPopup(window, initData.value, initData.obj);
        break;
    }
})();
