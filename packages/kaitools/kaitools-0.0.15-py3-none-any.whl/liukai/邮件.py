# https://www.cnblogs.com/yufeihlf/p/5726619.html
# ■ 源码整理  C:\Users\Administrator\PycharmProjects\s9\s9\demo\06 发送邮件 测试最终demo1.py

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# from email.mime.image import MIMEImage
from email.header import Header


def 邮件_发送邮件(
        smtpserver_='smtp.126.com',
        sender_="发件邮箱账号",
        username_="发件邮箱账号",
        password_="发件邮箱密码",
        receiver_="收件人邮箱文本列表",
        title_="邮件标题",
        text_="邮件正文",
):
    # ■1.设置smtplib所需的参数  发件服务器,邮箱账号,密码,发件人
    # ■2.收件人,邮件标题
    # smtpserver = 'smtp.126.com'  # smtp服务器
    # username = 'xxxx@126.com'  # 发件邮箱账号
    # password = 'xxxxx'  # 发件邮箱密码
    # sender = 'xxxxxx@126.com'  # 发件人
    # receiver='XXX@126.com'
    # 收件人为多个收件人
    # receiver = ['29xxxxxx@qq.com', '45xxxxx@qq.com']
    # receiver = ['29xxxxxx@qq.com']  # 收件人

    # subject = 'Python email demo'
    # 通过Header对象编码的文本，包含utf-8编码信息和Base64编码信息。以下中文名测试ok
    # subject = '中文标题'
    # title = '补充库存'
    title_ = Header(title_, 'utf-8').encode()

    # 构造邮件对象MIMEMultipart对象
    # 下面的主题，发件人，收件人，日期是显示在邮件页面上的。
    msg = MIMEMultipart('mixed')
    msg['Subject'] = title_
    # msg['From'] = 'itea-filter@126.com <itea-filter@126.com>'
    msg['From'] = '{} <{}>'.format(username_, username_)
    # print(msg['From'] )
    # msg['To'] = 'XXX@126.com'
    # 收件人为多个收件人,通过join将列表转换为以;为间隔的字符串
    msg['To'] = ";".join(receiver_)
    # msg['Date']='2012-3-16'

    # 构造文字内容
    # text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.baidu.com"
    # text = "Hi!\nHow are you?\nHere is the link you wanted:\n url改为空"
    # text = "我的邮件"
    text_ = '''
    **********************
    {}
    **********************
    '''.format(text_)
    # print(text)

    text_plain = MIMEText(text_, 'plain', 'utf-8')
    msg.attach(text_plain)  # 这个要保留 不保留没正文

    # 发送邮件
    smtp = smtplib.SMTP()
    smtp.connect(smtpserver_)
    # 我们用set_debuglevel(1)就可以打印出和SMTP服务器交互的所有信息。
    # smtp.set_debuglevel(1)
    smtp.login(username_, password_)
    smtp.sendmail(sender_, receiver_, msg.as_string())
    smtp.quit()


if __name__ == '__main__':
    smtpserver = 'smtp.126.com'
    sender = "ixxxxx@126.com"
    username = "ixxxxx@126.com"
    password = "xxxx"
    receiver = "2xxxxx@qq.com"
    title = "邮件标题"
    text = "邮件正文"

    # 邮件_发送邮件(smtpserver, sender, username, password, receiver, title, text)
    邮件_发送邮件(smtpserver, sender, username, password, receiver, title, text)

    # 邮件_发送邮件(
    #         smtpserver='smtp.126.com',
    #         sender="xxxxx@126.com",
    #         username="xxxxx@126.com",
    #         password="xxxxx",
    #         receiver="xxxxx@qq.com",
    #         title="邮件标题",
    #         text="邮件正文",
    # )
