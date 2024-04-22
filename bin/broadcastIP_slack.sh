#!/bin/bash
IP_ADDR=$(/bin/ip addr | grep 'wlp1s0$')
#echo $IP_ADDR >> /tmp/mysc.out

curl -X POST --data-urlencode "payload={\"channel\": \"#ipbroadcast\", \"username\": \"Callicog (192.168.0.20)\", \"text\": \"$IP_ADDR\"}" https://hooks.slack.com/services/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
