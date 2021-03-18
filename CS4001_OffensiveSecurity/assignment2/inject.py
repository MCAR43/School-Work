#!/usr/bin/env python3
import frida
import sys

jscode = """
    Java.perform(function () {
        var MainActivity = Java.use('com.example.seccon2015.rock_paper_scissors.MainActivity');
        MainActivity.onClick.implementation = function (v) {
            send('onClick');
            send("Count: " + this.cnt.value);
            send("M: " + this.m.value);
            send("N: " + this.n.value);


            this.cnt.value = 958;
            this.m.value=0;
            this.n.value=2;


            //this is the original
            this.onClick(v);
        };
    });
"""


def on_message(message, data):
    if message['type'] == 'send':
        print('Message: %s' % str(message['payload']))
    else:
        print(message)

def main():
    process = frida.get_usb_device().attach("com.example.seccon2015.rock_paper_scissors")
    script = process.create_script(jscode)
    script.on('message', on_message)
    print('-- Started Injection --')
    script.load()
    sys.stdin.read()
if __name__ == "__main__":
    main()


