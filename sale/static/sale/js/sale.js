function viewCarMoreInfo() {
	$('.car-more:visible').hide();
	$($('#carType option:selected').data('more')).closest('.car-more').fadeIn(250);
}

function setInsurancePremium() {
	function getStr(val, curency) {
		return isNaN(Number(val)) ? 0 : Number(val).toFixed(2) + ' ' + curency;
	}

	var vals = window.saleInsurancePremiumVals || null;
	var txt = getStr(window.saleInsurancePremiumDefault || 0, window.saleInsurancePremiumCurency || '');

	if(vals instanceof Object) {
		var type = $('#carType').val();
		var more = $($('#carType option:selected').data('more')).val() || null;
		var pers = $('#personType').find('input:radio:checked').val();
		var doc = $('#docType').find('input:radio:checked').val();

		if(vals[type] !== undefined) {
			if(more === null) {
				if(
					vals[type] instanceof Object && vals[type][pers] !== undefined &&
					vals[type][pers] instanceof Object && vals[type][pers][doc] !== undefined
				) {
					txt = getStr(vals[type][pers][doc], window.saleInsurancePremiumCurency || '');
				}
			} else {
				if(
					vals[type] instanceof Object && vals[type][more] !== undefined &&
					vals[type][more] instanceof Object && vals[type][more][pers] !== undefined &&
					vals[type][more][pers] instanceof Object && vals[type][more][pers][doc] !== undefined
				) {
					txt = getStr(vals[type][more][pers][doc], window.saleInsurancePremiumCurency || '');
				}
			}
		}

		$('#insurancePremium').text(txt);
	}
}

function changeSelect(tpl, vals) {
	var html = '';
	for(var i in vals) {
		html += '<option value="' + i + '">' + vals[i] + '</option>';
	}

	tpl.closest('.j-clr-form').jCleverAPI('selectCollection')[tpl.attr('name')].updateFromHTML(html);
}

function setCarModel() {
	var vals = window.saleInsurancePremiumVals || null;
	if(vals instanceof Object) {
		var make = $('#carMake').val();
		if(vals[make] !== undefined && vals[make] instanceof Object) {
			var models = new Object();
			for(var i in vals[make]) {
				if(vals[make][i] !== undefined && vals[make][i] instanceof Object) {
					models[i] = vals[make][i].title;
				}
			}
		}

		changeSelect($('#carModel'), models);
	}
}

function setCarType() {
	var vals = window.saleInsurancePremiumVals || null;
	var make = $('#carMake').val();
	var model = $('#carModel').val();

	if(
		vals instanceof Object && vals[make] !== undefined && vals[make] instanceof Object &&
		vals[make][model] !== undefined && vals[make][model] instanceof Object &&
		vals[make][model].type !== undefined && vals[make][model].type instanceof Object
	) {
		changeSelect($('#carType'), vals[make][model].type);
	}
}

function setCarMore() {
	var vals = window.saleInsurancePremiumVals || null;
	var make = $('#carMake').val();
	var model = $('#carModel').val();
	var type = $('#carType').val();

	$('#carEngine, #carSize, #carWeight').closest('.form-group').hide();
	if(
		vals instanceof Object && vals[make] !== undefined && vals[make] instanceof Object &&
		vals[make][model] !== undefined && vals[make][model] instanceof Object &&
		vals[make][model].more !== undefined && vals[make][model].more instanceof Object
	) {
		$(vals[make][model].more[type] || '').closest('.form-group').show();
	}
}

$(document).ready(function() {
	if($('.sale-container .step-1').length > 0) {
		setTimeout(function() {
			$('.sale-container .step-1').fadeIn(250);
		}, 500);

		viewCarMoreInfo();
		setInsurancePremium();
		$('#carType').on('change', viewCarMoreInfo);
		$('#carType, .car-more select, #personType input:radio, #docType input:radio').on('change', setInsurancePremium);
	}

	if($('.sale-container .step-2').length > 0) {
		setCarModel();
		setCarType();
		setCarMore();

		$('#telNumber').mask('+9 (999) 999 99 99', {placeholder: " "});
		$('#carEngine').mask('99 999', {placeholder: " "});
		$('#carSize').mask('999', {placeholder: " "});
		$('#carWeight').mask('999 999', {placeholder: " "});
		$('#dateStart').datepicker({
			showOtherMonths: true,
			selectOtherMonths: true,
			dateFormat: 'dd.mm.yy',
			onClose: function (selectedDate) {
					$('#dateStart').datepicker("option", "maxDate", selectedDate);
			}
		});

		$('#carType').on('change', setCarMore);
		$('#carModel').on('change', function(){
			setCarType();
			setCarMore();
		});
		$('#carMake').on('change', function() {
			setCarModel();
			setCarType();
			setCarMore();
		});
	}

	if($('.sale-container .step-2, .sale-container .step-3').length > 0) {
		i18n.init({
			lng: currLng,
			resGetPath: '/static/common/locales/__lng__/__ns__.json',
			getAsync: false
    });

		$.validate({
			form: '#saleForm',
			language: {
				errorTitle: $.t('errorTitle'), 	requiredFields: $.t('requiredFields'), badTime: $.t('badTime'), 	badEmail: $.t('badEmail'),
				badTelephone: $.t('badTelephone'), badSecurityAnswer: $.t('badSecurityAnswer'), 	badDate: $.t('badDate'),
				lengthBadStart: $.t('lengthBadStart'), lengthBadEnd: $.t('lengthBadEnd'), 	lengthTooLongStart: $.t('lengthTooLongStart'),
				lengthTooShortStart: $.t('lengthTooShortStart'), notConfirmed: $.t('notConfirmed'), 	badDomain: $.t('badDomain'),
				badUrl: $.t('badUrl'), badCustomVal: $.t('badCustomVal'), 	andSpaces: $.t('andSpaces'), badInt: $.t('badInt'),
				badSecurityNumber: $.t('badSecurityNumber'), badUKVatAnswer: $.t('badUKVatAnswer'), 	badStrength: $.t('badStrength'),
				badNumberOfSelectedOptionsStart: $.t('badNumberOfSelectedOptionsStart'), badAlphaNumeric: $.t('badAlphaNumeric'),
				badAlphaNumericExtra: $.t('badAlphaNumericExtra'), badNumberOfSelectedOptionsEnd: $.t('badNumberOfSelectedOptionsEnd'),
				wrongFileSize: $.t('wrongFileSize'), wrongFileType: $.t('wrongFileType'), 	groupCheckedRangeStart: $.t('groupCheckedRangeStart'),
				groupCheckedTooFewStart: $.t('groupCheckedTooFewStart'), groupCheckedTooManyStart: $.t('groupCheckedTooManyStart'),
				groupCheckedEnd: $.t('groupCheckedEnd'), badCreditCard: $.t('badCreditCard'), 	badCVV: $.t('badCVV')
			}
    });
	}
});