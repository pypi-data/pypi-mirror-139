package main

import (
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"os"

	"google.golang.org/grpc"
	"v2ray.com/core/app/proxyman/command"
	statsService "v2ray.com/core/app/stats/command"
	"v2ray.com/core/common/protocol"
	"v2ray.com/core/common/serial"
	"v2ray.com/core/proxy/vmess"
)

var (
	API_ADDRESS = "127.0.0.1"
	API_PORT    = 10085
	API_KEY     = "172574895"
)

type res struct {
	Sucess bool
	Tag    string
	User   string
	UUID   string
	Des    string
}

func addUser(c command.HandlerServiceClient, user_key string, tag string) string {
	// {{{

	if user_key == "" {
		return "missing user_key"
	}
	var resu res

	_, err := c.AlterInbound(context.Background(), &command.AlterInboundRequest{
		Tag: tag,
		Operation: serial.ToTypedMessage(&command.AddUserOperation{
			User: &protocol.User{
				Level: 0,
				Email: user_key,
				Account: serial.ToTypedMessage(&vmess.Account{
					Id:               user_key,
					AlterId:          0,
					SecuritySettings: &protocol.SecurityConfig{Type: protocol.SecurityType_AUTO},
				}),
			},
		}),
	})

	resu.User = user_key
	if err == nil {
		resu.Sucess = true
	} else {
		resu.Sucess = false
		resu.Des = err.Error()
	}
	ret, _ := json.Marshal(resu)
	return string(ret)
	// }}}
}

func removeUser(c command.HandlerServiceClient, user_key string, tag string) string {
	// {{{

	if user_key == "" {
		return "missing user_key"
	}

	_, err := c.AlterInbound(context.Background(), &command.AlterInboundRequest{
		Tag: tag,
		Operation: serial.ToTypedMessage(&command.RemoveUserOperation{
			Email: user_key,
		}),
	})

	var resu res

	resu.User = user_key
	if err == nil {
		resu.Sucess = true
	} else {
		resu.Sucess = false
		resu.Des = err.Error()
	}
	ret, _ := json.Marshal(resu)
	return string(ret)
	// }}}
}

func queryUserTraffic(c statsService.StatsServiceClient, user_key string, is_reset bool) string {
// {{{
	temp := fmt.Sprintf("user>>>%s>>>traffic>>>uplink", user_key)
	resp, err := c.QueryStats(context.Background(), &statsService.QueryStatsRequest{
		Pattern: temp,     // 筛选用户表达式
		Reset_:  is_reset, // 查询完成后是否重置流量
	})
	var resu res

	resu.Sucess = true
	resu.User = user_key
	resu.UUID = user_key
	resu.Des = "0"
	if err != nil {
		resu.Sucess = false
		resu.Des = err.Error()
	}
	// 获取返回值中的流量信息
	stat := resp.GetStat()
	// 返回的是一个数组，对其进行遍历输出
	for _, e := range stat {
		resu.Des = string(rune(e.GetValue()))
		break
	}
	ret, _ := json.Marshal(resu)
	return string(ret)
// }}}
}

var g_hsClient command.HandlerServiceClient

func HttpServer(w http.ResponseWriter, r *http.Request) {
	// {{{
	query := r.URL.Query()
	if query.Get("api_key") != API_KEY {
		fmt.Fprint(w, "1")
		return
	}

	respon := ""
	if r.URL.Path == "/addUser" {
		respon = addUser(g_hsClient, query.Get("user_key"), query.Get("tag"))
	} else if r.URL.Path == "/removeUser" {
		respon = removeUser(g_hsClient, query.Get("user_key"), query.Get("tag"))
	} else if r.URL.Path == "/quit" {
		os.Exit(1)
	}
	fmt.Fprint(w, respon)
	// }}}
}

func main() {
	// {{{
	cmdConn, err := grpc.Dial(fmt.Sprintf("%s:%d", API_ADDRESS, API_PORT), grpc.WithInsecure())
	if err != nil {
		panic(err)
	}
	g_hsClient = command.NewHandlerServiceClient(cmdConn)
	fmt.Println("runing")
	http.HandleFunc("/", HttpServer)                 //初始化
	err = http.ListenAndServe("127.0.0.1:9090", nil) //设置监听的端口
	if err != nil {
		fmt.Println("ListenAndServe: ", err)
	}
	// }}}
}
