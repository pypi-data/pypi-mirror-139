from telethon import TelegramClient, events, sync
import os

class ShynaTelegram:
    api_id = os.environ.get('shyna_telegram_api')
    api_hash = os.environ.get('shyna_telegram_hash')
    user = str(os.popen("echo $USER").read()).strip("\n")
    out_dir = "/home/" + user
    ftp_username = os.environ.get('ftp_username')
    ftp_pass = os.environ.get("ftp_pass")
    msg_text = "Default message, try over overriding it"
    
        
    def Shyna_send_message_to_master(self):
        if os.path.isfile(os.path.join(self.out_dir, "session_name.session")):
                pass
        else:
            self.get_session_file()
        client = TelegramClient(os.path.join(self.out_dir, "session_name"), self.api_id, self.api_hash)
        client.start()
        client.send_message('@Shiv623', self.msg_text)


    def get_session_file(self):
            self.down_url = 'wget  -O ' + self.out_dir + '/Shivam.jpg -r --ftp-user="' + self.ftp_username + '" --ftp-password="' + self.ftp_pass + '" ftp://www.shyna623.com/telegram/session_name.session'
            os.popen(self.down_url).readline()


if __name__ == '__main__':
    ShynaTelegram().Shyna_send_message_to_master()