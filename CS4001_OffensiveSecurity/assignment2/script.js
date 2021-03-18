Java.perform(function () {
    var MainActivity = Java.use('com.example.seccon2015.rock_paper_scissors.MainActivity');

    MainActivity.onClick.implementation = function (v) {
        send('onClick');
        send(this.m.onString());

        

        //this is the original
        this.onClick(v);
    };
});

