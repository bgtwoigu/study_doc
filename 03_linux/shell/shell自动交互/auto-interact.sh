#!/bin/bash
CMD_EXPECT=/usr/bin/expect
    
function check_cmd_expect(){
        if [ ! -f $CMD_EXPECT ];
        then
            echo "Please Install expect: sudo apt-get install expect!"
            exit 
        fi
}

function scp_source(){
        ${CMD_EXPECT}<<EOF
        set timeout 1200;
        spawn /usr/bin/scp server-138@10.1.1.138:/home/server-138/Temp_pxa1920/test.tgz ./
        expect "*password:"
        send "server\r" 
        expect eof
EOF
}

check_cmd_expect
scp_source
