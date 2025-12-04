function timeline(){
    var myChart = echarts.init(document.getElementById('time_line'));
    var months=['1月','2月','3月','4月','5月','6月','7月','8月','9月','10月','11月','12月']
    option = {
        timeline: {
          axisType: 'category',
          autoPlay: true,
          playInterval: time_interval,
          data:months,
          controlStyle:{
              show:false
          },
          left:'5%',
          right:'5%',
        }
    },
    myChart.setOption(option);
}