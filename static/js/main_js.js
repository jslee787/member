var pic = document.getElementById('pic');
pic.onmouseover = changePic;
pic.onmouseout = originPic;

function changePic(){   //마우스 올리면 사진 변경
    pic.src = "../static/images/healing.jpg";
}
function originPic(){   //마우스 빼면 사진 원래대로
    pic.src = "../static/images/activity.jpg";
}
