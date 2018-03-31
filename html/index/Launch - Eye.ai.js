function handleSave() {
    //导出base64格式的图片数据  
    var mycanvas = document.getElementById("mycanvas");
    var base64Data = mycanvas.toDataURL("image/jpeg", 1.0);
    //封装blob对象  
    var blob = dataURItoBlob(base64Data);
    //组装formdata  
    var fd = new FormData();
    fd.append("fileData", blob);//fileData为自定义  
    fd.append("fileName", "123jpg");//fileName为自定义，名字随机生成或者写死，看需求  
    //ajax上传，ajax的形式随意，JQ的写法也没有问题  
    //需要注意的是服务端需要设定，允许跨域请求。数据接收的方式和<input type="file"/> 上传的文件没有区别  
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("POST", “你发送上传请求的url”);
    xmlHttp.setRequestHeader("Authorization", 'Bearer ' + localStorage.token);//设置请求header,按需设定，非必须  
    xmlHttp.send(fd);
    //ajax回调  
    xmlHttp.onreadystatechange = () => {
        //todo  your code...  
    };
};
function dataURItoBlob(base64Data) {
    var byteString;
    if (base64Data.split(',')[0].indexOf('base64') >= 0)
        byteString = atob(base64Data.split(',')[1]);
    else
        byteString = unescape(base64Data.split(',')[1]);
    var mimeString = base64Data.split(',')[0].split(':')[1].split(';')[0];
    var ia = new Uint8Array(byteString.length);
    for (var i = 0; i < byteString.length; i++) {
        ia[i] = byteString.charCodeAt(i);
    }
    return new Blob([ia], { type: mimeString }); 