// 1、定义长连接
let conn = null;

// 进度条的变化
function progress_status(val) {
    let data = "";
    if (val >= 0 && val < 25) {
        data = " bg-success";
    } else if (val >= 25 && val < 50) {
        data = "";
    } else if (val >= 50 && val < 75) {
        data = " bg-warning";
    } else if (val >= 75 && val <= 100) {
        data = " bg-danger";
    }
    return data
}

// 首页的websocket的连接提示信息
function log(cls, msg) {
    // cls：元素的样式，msg：提示的信息
    document.getElementById("monitor_status").innerHTML = `<div class="alert alert-${cls}">${msg}</div>`;
}

// 专门用来实时更新监控信息的
function update_ui(e) {
    let data = e.data;
    data = JSON.parse(data);  // 把json字符串转化为对象

    /* 平均CPU，水球图 */
    // 更新水球图里面的数据，CPU平均使用率，toFixed 保留4位小数
    option_cpu_avg.series[0].data[0] = (data["cpu"]["percent_avg"]/100).toFixed(4);
    // 更新水球图里面的数据，标题（这里我们的标题是时间）
    option_cpu_avg.title[0]['text'] = data['dt'] + "-CPU平均使用率";
    // 配置图表
    chart_cpu_avg.setOption(option_cpu_avg);

    /* 所有逻辑CPU，进度条 */
    let cpu_per = "";
    for (var k in data['cpu']['percent_per']) {
        var num = parseInt(k);
        cpu_per += "<tr><td class='text-primary' style='width: 30%'>CPU" + num + "</td>";
        cpu_per += "<td><div class='progress'><div class='progress-bar progress-bar-striped progress-bar-animated" + progress_status(data['cpu']['percent_per'][k]) + "' role='progressbar' aria-valuenow='" + data['cpu']['percent_per'][k] + "' aria-valuemin='0' aria-valuemax='100' style='width: " + data['cpu']['percent_per'][k] + "%'>" + data['cpu']['percent_per'][k] + "%</div></div></td></tr>";
    }
    // 通过标签的id，来更新标签的内容
    document.getElementById("tb_cpu_per").innerHTML = cpu_per;

    /* 内存实时更新 */
    // 仪表盘
    option_mem .series[0].data[0].value = data["mem"]["percent"];
    option_mem .title[0].text = data["dt"] + "-内存使用率";
    chart_mem.setOption(option_mem);
    // 内存的表格数据
    document.getElementById("mem_percent").innerText = data["mem"]["percent"];
    document.getElementById("mem_total").innerText = data["mem"]["total"];
    document.getElementById("mem_used").innerText = data["mem"]["used"];
    document.getElementById("mem_free").innerText = data["mem"]["free"];

    // 交换分区实时更新
    // 仪表盘
    option_swap .series[0].data[0].value = data["swap"]["percent"];
    option_swap .title[0].text = data["dt"] + "-交换分区使用率";
    chart_swap.setOption(option_swap);
    // 交换分区的表格数据
    document.getElementById("swap_percent").innerText = data["swap"]["percent"];
    document.getElementById("swap_total").innerText = data["swap"]["total"];
    document.getElementById("swap_used").innerText = data["swap"]["used"];
    document.getElementById("swap_free").innerText = data["swap"]["free"];

    // 网卡收发信息实时更新
    // 饼状图
    let net = "";
    // 批量更新网卡信息
    for (let k in data["net"]) {
        // 获取网卡收发信息的值
        let cd = data["net"][k];
        // 收发的字节数都不为0的就更新，为0的就不更新
        if(parseInt(cd['bytes_sent']) !== 0 && parseInt(cd["bytes_recv"]) !== 0) {
            // 网卡的索引
            let index = parseInt(k) + 1;
            // 把字符串转换成变量名(option)
            let op = eval("option_net" + index);
            // 把字符串转换成变量名（chart）
            let ch = eval("chart_net" + index);
            // 修改标题
            op.title[0].text = data["dt"] + "-" + cd["name"] + "网卡信息";
            // 更新饼图的值
            op.series[0].data = [
                {"name": "收包数", "value": cd["packets_recv"]},
                {"name": "发包数", "value": cd["packets_sent"]},
            ];
            op.series[1].data = [
                {"name": "收字节", "value": cd["bytes_recv"]},
                {"name": "发字节", "value": cd["bytes_sent"]},
            ];
            ch.setOption(op);
        }
        net += "<tr><td>" + cd['name'] + "</td>";
        net += "<td class='text-danger'>" + cd['bytes_sent'] + "</td>";
        net += "<td class='text-danger'>" + cd['bytes_recv'] + "</td>";
        net += "<td class='text-danger'>" + cd['packets_sent'] + "</td>";
        net += "<td class='text-danger'>" + cd['packets_recv'] + "</td>";
        net += "<td>" + cd['family'] + "</td>";
        net += "<td>" + cd['address'] + "</td>";
        net += "<td>" + cd['netmask'] + "</td>";
        if (cd['broadcast']) {
            net += "<td>" + cd['broadcast'] + "</td></tr>";
        } else {
            net += "<td>无</td></tr>";
        }
    }
    document.getElementById("tb_net").innerHTML = net;

    // 磁盘信息实时更新
    var disk = "";
    for (var k in data["disk"]) {
        var cd = data["disk"][k];
        disk += "<tr><td>" + cd['device'] + "</td>";
        disk += "<td>" + cd['mountpoint'] + "</td>";
        disk += "<td>" + cd['fstype'] + "</td>";
        disk += "<td class='text-danger'>" + cd['used']['total'] + "GB</td>";
        disk += "<td class='text-danger'>" + cd['used']['used'] + "GB</td>";
        disk += "<td class='text-danger'>" + cd['used']['free'] + "GB</td>";
        disk += `
            <td>
                <div class="progress">
                    <div class="progress-bar progress-bar-striped progress-bar-animated${progress_status(cd['used']['percent'])}" role="progressbar" aria-valuenow="${cd['used']['percent']}" aria-valuemin="0" aria-valuemax="100" style="width: ${cd['used']['percent']}%">${cd['used']['percent']}%</div>
                </div>
            </td>`;
    }
    document.getElementById("tb_disk").innerHTML = disk;
}

// 2、定义连接函数
function connect() {
    disconnect();  // 把之前没关闭的连接关闭掉，再创建新的连接
    // 定义协议
    let transports = ["websocket"];
    // 创建连接对象
    // window.location.host 返回一个URL的主机名和端口
    conn = new SockJS("http://" + window.location.host + "/real/time", transports);

    // 连接之前，提示正在连接。直接调用我们自定义的log函数，传入样式和信息即可
    log("warning", "正在连接...");
    // 建立连接
    conn.onopen = function () {
        console.log("连接成功！");
        log("success", "连接成功");
    };
    // 建立接收消息
    conn.onmessage = function (e) {
        // console.log(e.data)
        update_ui(e);  // 条用实时更新信息的函数
    };
    // 建立关闭连接
    conn.onclose = function () {
        console.log("断开连接！");
        log("danger", "连接断开！");
    };
    // 每隔1秒触发一个事件
    setInterval(function () {
        conn.send("system");
    }, 1000);
}

// 3、定义断开连接函数
function disconnect() {
    if (conn !== null) {
        conn.close();  // 关闭连接
        conn = null;
        log("danger", "连接断开！");
    }
}

// 4、刷新页面的时候，断开连接，重新连接，断线重连的判断
if (conn === null) {
    connect();  // 建立连接
} else {
    disconnect();  // 断开连接
}