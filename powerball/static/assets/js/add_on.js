function showTime() {
    var date = new Date();

    var jan = new Date(date.getFullYear(), 0, 1);
    var jul = new Date(date.getFullYear(), 6, 1);
    var isDst = date.getTimezoneOffset() < Math.max(jan.getTimezoneOffset(), jul.getTimezoneOffset());
    if (isDst) {
        // local to UTC to EDT
        date.setTime( date.getTime() + date.getTimezoneOffset()*60*1000 - 240*60*1000);
    } else {
        // local to UTC to EST
        date.setTime( date.getTime() + date.getTimezoneOffset()*60*1000 - 300*60*1000);
    }

    var y = date.getFullYear();
    var mo = date.getMonth() + 1;
    var d = date.getDate();
    var h = date.getHours(); // 0 - 23
    var m = date.getMinutes(); // 0 - 59
    var s = date.getSeconds(); // 0 - 59

    if (h == 0) {
        h = 12;
    }

    mo = (mo < 10) ? "0" + mo : mo;
    d = (d < 10) ? "0" + d : d;
    h = (h < 10) ? "0" + h : h;
    m = (m < 10) ? "0" + m : m;
    s = (s < 10) ? "0" + s : s;

    var time = y + "-" + mo + "-" + d + " " + h + ":" + m + ":" + s;
    document.getElementById("ClockDisplay").innerText = time;
    document.getElementById("ClockDisplay").textContent = time;

    setTimeout(showTime, 1000);

}
// showTime();
