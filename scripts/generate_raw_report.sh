json=$(jq -n '{}')

for sftp_ip in `cat ./vms_ip`
do
    count=$(grep -r $sftp_ip /var/sftp/data/ | wc -l)

    json=$(echo $json | jq --arg ip "$sftp_ip" --argjson count "$count" '. + {($ip): $count}')
done

echo $json > raw_report.json
