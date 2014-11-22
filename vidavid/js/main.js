$('.delete').on('click', function(){
    var answer = confirm('are you sure?')
    if (answer){
		$(this).closest('div').remove();
	}
})

$('#image a').click(function (e) {
  e.preventDefault()
  $(this).tab('show')
})

$('#privacy a').click(function (e) {
  e.preventDefault()
  $(this).tab('show')
})

$('#notification a').click(function (e) {
  e.preventDefault()
  $(this).tab('show')
})