var Message = {

    running: function(){
        document.getElementById("loader").style.display = "block";
    },

    done: function(){
        document.getElementById("loader").style.display = "none";
    },

    executedCaseSuccess: function(){
        $("#MessageList").append("<p>Executed Success!</p>");
    },

    deviceNotConnected: function(){
        $("#MessageList").append("<p>Device is not connected.</p>");
    },
    
    getScreenShotSuccess: function(){
        $("#MessageList").append("<p>Get ScreenShot Success.</p>");
    },
}