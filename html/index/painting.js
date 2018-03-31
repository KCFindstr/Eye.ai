function drawHYYObjectsOnCanvas(canvas, obj) {
	var scale = [canvas.width, canvas.height];
	var safe = [0, 128, 255];
	var danger = [255, 64, 0];
	for (var i=0; i<obj.length; i++) {
		var cur = obj[i];
		var ctx= canvas.getContext("2d");
		for (var j=0; j<=1; j++) {
			cur.position[j] *= scale[j];
			cur.size[j] *= scale[j];
		}
		let color = "rgb(";
		for (var j=0; j<3; j++) {
			var tmp = safe[j]+(danger[j]-safe[j])*cur.dangerLevel;
			color += parseInt(tmp);
			if (j < 2)
				color += ",";
		}
		color += ")";
		console.log(color);
		ctx.strokeStyle = color;
		ctx.lineWidth = 3;
		ctx.strokeRect(cur.position[0], cur.position[1], cur.size[0], cur.size[1]);
	}
}