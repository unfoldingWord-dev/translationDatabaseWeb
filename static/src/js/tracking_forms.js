/* @@@ rewrite this */
document.addEventListener('DOMContentLoaded', function (event) {

	// For the following fields...
	['translator', 'facilitator', 'material'].forEach(function(field) {
		// ... add the first row if there isn't any
		if (!$('[name="' + field + '0"]').length)
			addInline(field);

		// ... attach click event handler
		$("#add-" + field).on("click", function (event) {
			event.preventDefault();
			addInline(field);
		});
	});

	// Add class:required to the following label
	var required_fields = ['charter', 'start_date', 'end_date', 'location', 'lead_dept', 'contact_person', 'number', 'countries', 'language'];
	markRequired(required_fields);
});

// ================
// CUSTOM FUNCTIONS
// ================

//    addInline
//    ---------
function addInline(label) {
	var list = $('#' + label + '-list');
	var length = list.children().length;
	switch(label) {
		// Build facilitator element
		case 'facilitator':
			var elem = '<div class="inline inline-input clearfix">' +
				'<div class="facilitator-text clearfix">' +
					'<input name="facilitator' + length + '" type="text" class="form-control" />' +
				'</div>' +
				'<div class="facilitator-checkboxes">' +
					'<div class="half-width"><input name="is_lead' + length + '" type="checkbox" class="form-control" /></div>' +
					'<div class="half-width"><input name="speaks_gl' + length + '" type="checkbox" class="form-control" /></div>' +
				'</div>' +
			'</div>';
			break;
		// Build material element
		case 'material':
			var elem = '<div class="inline inline-input clearfix">' +
				'<div class="material-text clearfix">' +
					'<input name="material' + length + '" type="text" class="form-control" />' +
				'</div>' +
				'<div class="material-checkboxes">' +
					'<div class="full-width"><input name="licensed' + length + '" type="checkbox" class="form-control" checked /></div>' +
				'</div>' +
			'</div>';
			break;
		// Build translator element
		case 'translator':
			var elem = '<div class="inline inline-input clearfix">' +
				'<div class="translator-text full-width clearfix">' +
					'<input name="translator' + length + '" type="text" class="form-control" />' +
				'</div>';
			break;
		default:
			var elem = '';
			break;
	}
	list.append(elem);
	addCount(label);
}

//    addCount
//    --------
function addCount(label) {
	var elem = document.getElementsByName(label + '-count');
	if (elem.length) elem[0].value = parseInt(elem[0].value) + 1;
}

//    markRequired
//    ------------
function markRequired(required_fields) {
	required_fields.forEach(function(field) {
		var field = document.querySelector('label[for*="' + field + '"]');
		if (field) {
			field.classList.add('required');
		}
	});
}