window.onload = () => {
	$('#sendbutton').click(() => {
		imagebox = $('#imagebox')
		input = $('#imageinput')[0]
		if(input.files && input.files[0])
		{
			let formData = new FormData();
			formData.append('image' , input.files[0]);
			var radios = document.getElementsByName('image_processing');
			for (var i = 0, length = radios.length; i < length; i++) {
				if (radios[i].checked) {
					formData.append('option',radios[i].value);
					break;
				}
			}
			$.ajax({
				url: "http://localhost:5000/start", // fix this to your liking
				type:"POST",
				data: formData,
				cache: false,
				processData:false,
				contentType:false,
				error: function(data){
					console.log("upload error" , data);
					console.log(data.getAllResponseHeaders());
				},
				success: function(data){
					if(data.hasOwnProperty('link')){
						console.log(data)
						document.getElementById("prediction").innerHTML = JSON.stringify(data['link']);
						bytestring = data['status']
						image = bytestring.split('\'')[1]
						imagebox.attr('src' , 'data:image/jpeg;base64,'+image)
					}
					else{
						dataJ = JSON.parse(data)
						console.log(dataJ)
						bytestring = dataJ['status']
						image = bytestring.split('\'')[1]
						imagebox.attr('src' , 'data:image/jpeg;base64,'+image)
						if(dataJ['predictions']){
							document.getElementById("prediction").innerHTML = JSON.stringify(dataJ['predictions']);
						}
						else{
							document.getElementById("prediction").innerHTML = "";
						}
					}
				}
			});
		}
	});
};



function readUrl(input){
	imagebox = $('#imagebox')
	console.log("evoked readUrl")
	if(input.files && input.files[0]){
		let reader = new FileReader();
		reader.onload = function(e){
			// console.log(e)
			
			imagebox.attr('src',e.target.result); 
			imagebox.height(300);
			imagebox.width(300);
		}
		reader.readAsDataURL(input.files[0]);
	}
}