var canvas = document.getElementById('paint');
var ctx = canvas.getContext('2d');

reset();

var width = canvas.width;
var height = canvas.height;


var curX, curY, prevX, prevY;
var hold = false;

ctx.lineWidth = 15;
ctx.strokeStyle = "#FFFFFF";

var image_data = [];

function reset(){
    ctx.fillStyle.color = '#000000';
    ctx.fillRect(0,0, canvas.width, canvas.height);
    image_data = [];
    
}

function pen(){

    canvas.onmousedown = function(e){

        curX = e.clientX - canvas.offsetLeft;
        curY = e.clientY - canvas.offsetTop;
        
        hold = true;

        prevX = curX;
        prevY = curY;

        ctx.beginPath();
        ctx.moveTo(prevX, prevY);



    };

    canvas.onmousemove = function(e){

        if(hold){

            curX = e.clientX - canvas.offsetLeft;
            curY = e.clientY - canvas.offsetTop;

            draw();
        }
    };

    canvas.onmouseup = function(e){

        hold = false;
    };

    canvas.onmouseout = function(e){

        hold = false;
    };

    function draw(){
        ctx.lineTo(curX, curY);
        ctx.stroke();
        image_data.push({'startx': prevX, startY: prevY, 'endx': curX, 'endy': curY});
    };
}

function predictnum(){

    
    var image = canvas.toDataURL();

    $.ajax({type: "POST", 
        url:'/', 
        data:{save_image: image
    }}).done(function(data){
        document.getElementById('prediction').innerHTML = data.prediction;
        
        $('#mychart').empty();
        
        $('#mychart').append(data.plots[0][1]);

        jQuery.globalEval(data.plots[0][0].slice(8,-9));
    });
    

}

