const DANGER_LIMIT = 0.618;
const CENTER_LIMIT = 0.8;
const MAX_SIZE = 10;

var telling = false;
var msg;

//Say something
function speak(text) {
	if (telling)
		return;
	telling = true;
	console.log("SPEAK: "+text);
	msg = new SpeechSynthesisUtterance(text);
	msg.addEventListener('end', function () {
		telling = false;
	});
	window.speechSynthesis.speak(msg);
}

// Draw rectangle
function drawHYYObjectsOnCanvas(canvas, obj) {
	var scale = [canvas.width, canvas.height];
	var safe = [0, 128, 255];
	var danger = [255, 64, 0];
	var ctx = canvas.getContext("2d");
	var ele = $("#info");
	ctx.clearRect(0, 0, canvas.width, canvas.height);
	ctx.setLineDash([2,3]);
	ctx.lineWidth = 2;
	// Check scroll bar position
	var atBottom = false;
	if (ele.innerHeight() + 10 >= ele[0].scrollHeight - ele.scrollTop())
		atBottom = true;
	for (var i=0; i<obj.length; i++) {
		var ret = "<div style='margin-bottom: 10px;'>";
		var cur = JSON.parse(JSON.stringify(obj[i]));
		for (var j=0; j<=1; j++) {
			cur.position[j] *= scale[j];
			cur.size[j] *= scale[j];
			cur.position[j] = parseInt(cur.position[j]);
			cur.size[j] = parseInt(cur.size[j]);
		}
		let color = "rgb(";
		for (var j=0; j<3; j++) {
			var tmp = safe[j]+(danger[j]-safe[j])*cur.dangerLevel;
			color += parseInt(tmp);
			if (j < 2)
				color += ",";
		}
		color += ")";
		ret += "<div class='danger' style='color:" + color + "'>Danger Level: " + 
			parseInt(cur.dangerLevel*1000)/10 + "%:</div> One " + cur.name +
			" at (" + cur.position[0] + ", " + cur.position[1] + ")<br/>width = "
			+ cur.size[0] + " / height = " + cur.size[1];
		ctx.strokeStyle = color;
		ctx.strokeRect(cur.position[0], cur.position[1], cur.size[0], cur.size[1]);
		ret += "</div>";
		ele.append($(ret));
	}
	while (ele.children("div").length > MAX_SIZE) {
		ele.children("div").first().remove();
	}
	if (atBottom) {
		ele.scrollTop(ele[0].scrollHeight-ele.innerHeight());
//		ele.animate({scrollTop: ele.height()}, 300);
	}
}

// Check if center
function getPosition(x, y) {
	x -= 0.5;
	y -= 0.5;
	var val = x*x/0.25+y*y/0.3;
	console.log(val, x);
	if (val <= CENTER_LIMIT)
		return "in front of you";
	if (x < 0)
		return "on the left";
	else
		return "on the right";
}

// Say something
function tell(obj) {
	if (obj.length == 0)
		return;
	var maxpos = 0;
	for (var i=0; i<obj.length; i++) {
		var cur = obj[i];
		if (cur.dangerLevel > obj[maxpos].dangerLevel)
			maxpos = i;
	}
	var cur = obj[maxpos];
	console.log(cur.dangerLevel, telling);
	if (cur.dangerLevel > DANGER_LIMIT) {
		var x = cur.position[0]+cur.size[0]/2;
		var y = cur.position[1]+cur.size[1]/2;
		var pos = getPosition(x,y);
		var text = "One ";
		text += cur.name;
		text += " is ";
		text += pos;
		speak(text);
	}
}