// screen size has changed - modify document to fix page correctly
function setupDisplay() {
    var width = window.innerWidth;  // returns px increments
    var maxWidth = 96 * 8.5;  // pixels in 8.5 inches

    if (width > maxWidth) { // screen is larger than needed
        // center the display and reduce size for readability
        document.getElementById('pageArea').style.left = ((width - maxWidth) / 2) + 'px';
        document.getElementById('pageArea').style.width = maxWidth + 'px';
        document.getElementById('pageArea').style.position = 'fixed';

        // make page data area use a scroll bar if needed and fix header at top
        document.getElementById('pageData').style.height
            = (window.innerHeight - document.getElementById('pageData').offsetTop - 10) + 'px';

    } else { // smaller screen sizes
        // make display scrollable
        document.getElementById('pageArea').style.left = '';
        document.getElementById('pageArea').style.width = '';
        document.getElementById('pageArea').style.position = '';

        // remove scroll bar for non-header area and make header scrollable
        document.getElementById('pageData').style.height = '';
    }
}

count = 0;
count2 = 0;
function  testButton(e, cnt) {
    if (e.parentElement.id != "answers") {
        document.getElementById("status").innerHTML = 
            "<span style='background-color: pink;'>"  
            "Invalid selections</span>";            
        return;
    }
    count2++;
    if (cnt == count) {
        count++;
        document.getElementById("status").innerHTML = 
            "<span style='background-color: lightgreen;'>"  
            + e.innerText +
            " is correct</span>";
        e.innerHTML += "<br/>" + e.getAttribute("murders");
        document.getElementById("correct").innerHTML += e.outerHTML;
        e.outerHTML = "";
        if (count == 10) // last entry
            document.getElementById("status").innerHTML += 
                "<p><span class='hilite'>You took " + count2 + 
                " out of 55 possible clicks.</span></p>"; 
    } else
        document.getElementById("status").innerHTML = 
                "<span style='background-color: pink;'>"  
                + e.innerText +
                " is incorrect</span>";
}
