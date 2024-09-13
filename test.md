---
title: PAGE TITLE HERE
layout: template
filename: NAME OF THIS .md FILE HERE
--- 

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Interactive Image with Popups</title>
    <style>
        .image-container {
            position: relative;
            display: inline-block;
        }
        .icon {
            position: absolute;
            width: 20px;
            height: 20px;
            cursor: pointer;
        }
        .popup {
            display: none;
            position: absolute;
            background-color: white;
            border: 1px solid black;
            padding: 10px;
            z-index: 1;
        }
    </style>
</head>
<body>
<div class="image-container">
    <img src="final_image_with_icons.png" alt="Interactive Image">

    <div class="icon" style="top: 128.4px; left: 170.0px;" 
         onmouseover="document.getElementById('popup-170.0-128.4').style.display='block'"
         onmouseout="document.getElementById('popup-170.0-128.4').style.display='none'">
    </div>
    <div id="popup-170.0-128.4" class="popup" style="top: 153.4px; left: 170.0px;">
        <h2>light</h2>
        <p>lighting </p>
    </div>

</div>
</body>
</html>
