
contest_date=""
contest_test=""
def get_contest():
    global contest_date,contest_test
    date_now=str(time.strftime("%Y-%m-%d",time.localtime(time.time())))
    if(contest_date!=date_now):
        contest_date=date_now
        data='{"offset":0,"limit":5}'
        url="https://api.ctfhub.com/User_API/Event/getUpcoming"
        response=requests.post(url,data,proxies=proxies)
        contest_up=response.json()
        result=[]
        for x in contest_up['data']['items']:
            result.append("比赛名称：%s"%(x['title'],))
            result.append("比赛时间：%s ~ %s"%(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(x['start_time'])),time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(x['end_time']))))
            data='{"event_id": %s}'%(x['id'],)
            url="https://api.ctfhub.com/User_API/Event/getInfo"
            response=requests.post(url,data,proxies=proxies)
            contest_detail=response.json()
            result.append("比赛类型：%s-%s"%(contest_detail['data']['class'],contest_detail['data']['form']))
            result.append("比赛网址：%s"%(contest_detail['data']['official_url'],))
            result.append("————————————")
        result.append("消息来源：CTFHub")
        contest_test="\n".join(result);
        return contest_test
    else:
        return contest_test