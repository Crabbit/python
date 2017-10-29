#!/bin/bash

#  -----------------------------------------------------------------------------
# show claim status
function show_claim(){
    mysql -h xx-perseus-xx.xx.com -u xx -pxx << EOF
select count(*) from bop.ygg_monitor where currStatus != '1';
select count(*) from bop.ygg_monitor where currStatus != '1' and operator is null;
EOF
    return 0
}



#  -----------------------------------------------------------------------------
# check log update time
timestamp_now=$(date +%s)
mon_bin_dir="$(dirname $0)"
mon_top_dir="${mon_bin_dir}/../"
log_path="${mon_bin_dir}/start.log"

update_time=$(stat ${log_path} | grep -i 'Modify:' | awk -F 'Modify:' '{print $NF}' | awk -F '+' '{print $1}' | cut -d. -f 1)
update_timestamp=$(date -d "${update_time}" +%s)

diff_second=$[ ${timestamp_now} - ${update_timestamp} ]

echo "MON_LAST_UPDATE:${diff_second}"



#  -----------------------------------------------------------------------------
# check error num from mysql
mysql_return=$( show_claim )

total_error_count=$( echo $mysql_return | awk '{print $2}' )
none_claim_count=$( echo $mysql_return | awk '{print $4}' )

echo "TOTAL_ERROR_COUNT:${total_error_count}"
echo "NONE_CLAIM_COUNT:${none_claim_count}"



#  -----------------------------------------------------------------------------
# check mysql qps
questions_start=$(mysqladmin -h x-perseus-xx.com -uxxx -p'xx' status | awk -F'Questions:' '{print $NF}' | cut -d' ' -f 2)
#echo $questions_start
sleep 5
questions_end=$(mysqladmin -h xx-perseus-xx.com -uxx -p'xx' status | awk -F'Questions:' '{print $NF}' | cut -d' ' -f 2)
#echo $questions_end

questions_diff=$[ ${questions_end} - ${questions_start} ]
qps=$[ $questions_diff / 5 ]
echo "MYSQL_QPS:${qps}"
