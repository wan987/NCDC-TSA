map_chart();
tree_chart();
word_chart();
bar_chart();
function month_index_charge(){
    if(month_index==12){
        month_index=1;
    }else{
        month_index++;
    };
//    console.log(map_data1[month_index]);
    map_chart();
    tree_chart();
    word_chart();
    bar_chart();
//    console.log(month_index);

};
setInterval(month_index_charge,time_interval);
timeline();
line_chart();

