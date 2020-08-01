<template>
    <div>
    <!-- 下面的div给表一个容器 -->
       <div id="myChart" :style="{width: '1000px', height: '500px'}"></div>
       <div>
           <button @click="save">保存当前数据</button>
       </div>
    </div>
</template>
<script>
    // 引入基本模板
    let echarts = require('echarts/lib/echarts');
    // 引入柱状图组件
    require('echarts/lib/chart/bar');
    // 引入提示框和title组件
    require('echarts/lib/component/tooltip');
    require('echarts/lib/component/title');
    export default {
        name: "DataCount",
        data: () => ({
            msg: 'Welcome to Your Vue.js App',
            num_list: [11, 11, 15, 13, 12, 13, 10],
            num_list1:[1, -2, 2, 5, 3, 2, 0]
        }),
        sockets:{
            connect: function(){
            console.log('socket 连接成功')
            },
            message: function(val){
                console.log('返回:'+val);
                this.log_list.push(val);
            },
            sendback: function(val){
                console.log(val);
                // this.log_list.push(val);
                this.num_list = val;
                console.log(this.num_list)
                this.drawLine(val);
            }
        },
        mounted(){
            this.drawLine(this.num_list);
        },
        methods:{
            // 保存当前数据
            save(){
                this.axios.get('http://127.0.0.1:5000/save',{params:{'key_list':JSON.stringify(this.num_list)}}).then(res=>{
                    console.log(res)
                })
            },
            drawLine(num_list){
                // 基于准备好的dom，初始化echarts实例
                let myChart = this.$echarts.init(document.getElementById('myChart'));
                // 绘制图表
                myChart.setOption({
                    title: {
                        text: '',
                        subtext: ''
                    },
                    tooltip: {
                        trigger: 'axis'
                    },
                    legend: {
                        data:['最高','最低']
                    },
                    toolbox: {
                        show: true,
                        feature: {
                            dataZoom: {
                                yAxisIndex: 'none'
                            },
                            dataView: {readOnly: false},
                            magicType: {type: ['line', 'bar']},
                            restore: {},
                            saveAsImage: {}
                        }
                    },
                    xAxis:  {
                        type: 'category',
                        boundaryGap: false,
                        data: ['2019-02-25','2019-03-04','2019-03-18','2019-03-26','2019-04-16','2019-04-26','2019-05-04']
                    },
                    yAxis: {
                        type: 'value',
                        axisLabel: {
                            formatter: '{value}'
                        }
                    },
                    series: [
                        {
                            name:'最高',
                            type:'line',
                            data:num_list,
                            markPoint: {
                                data: [
                                    {type: 'max', name: '最大值'},
                                    {type: 'min', name: '最小值'}
                                ]
                            },
                            markLine: {
                                data: [
                                    {type: 'average', name: '平均值'}
                                ]
                            }
                        },
                        {
                            name:'最低',
                            type:'line',
                            data:this.num_list1,
                            markPoint: {
                                data: [
                                    {name: '周最低', value: 2, xAxis: 1, yAxis: 1.5}
                                ]
                            },
                            markLine: {
                                data: [
                                    {type: 'average', name: '平均值'},
                                    [{
                                        symbol: 'none',
                                        x: '90%',
                                        yAxis: 'max'
                                    }, {
                                        symbol: 'circle',
                                        label: {
                                            normal: {
                                                position: 'start',
                                                formatter: '最大值'
                                            }
                                        },
                                        type: 'max',
                                        name: '最高点'
                                    }]
                                ]
                            }
                        }
                    ]
                });
            }
        }
    }
</script>