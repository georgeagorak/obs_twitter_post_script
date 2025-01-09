import tweepy
import config_file #local config with keys
import obspython
import datetime
import twitch_info

# from twitchAPI.twitch import Twitch
# from twitchAPI.helper import first

sendTweet = False

client = tweepy.Client(config_file.barear_token, config_file.api_key, config_file.api_secret, config_file.access_token_user, config_file.access_token_sercret_user)
auth = tweepy.OAuthHandler(config_file.api_key, config_file.api_secret, config_file.access_token_user, config_file.access_token_sercret_user)
api_key = tweepy.API(auth)

access_token = twitch_info.get_access_token(client_id=config_file.client_id, client_secret=config_file.client_secret)
user_id = twitch_info.get_user_id(user_name="jurgon56", client_id=config_file.client_id, acces_token=access_token)

def script_description():
      return """<center><h2>Send X post Script</h2></center>
                  <p>Sends pre-genereted X post when stream has started.
                  <br> to use this script you need to have a twitch account and a x account.
                  <br> use python libraries: tweepy and twitch-info
                  <b>Author:</b> georgeagorak (jurgon56) <br>
                  </p>"""

def timer_callback():
      global sendTweet
      
      stream = twitch_info.get_stream(user_id=user_id, client_id=config_file.client_id, acces_token=access_token)
      current_time = datetime.datetime.now().strftime("%d/%m/%Y at %H:%M")
      if stream == "This user is not streaming":
            print("This user is not streaming")
      else:
            print("Streaming now...")
            if obspython.obs_frontend_streaming_active() and not sendTweet:
                  sendTweet = True
                  print("Stream is active...")
                  client.create_tweet(text=f"AY YOU! On {current_time} Nerd Just started streaming {stream['game_name']} titled ''{stream['title']}'' ┌( ͝° ͜ʖ͡°)=ε/̵͇̿̿/’̿’̿ ̿ , https://www.twitch.tv/jurgon56")
                  print("X post sent!...")
            elif not obspython.obs_frontend_streaming_active() and sendTweet:
                  sendTweet = False
                  print("Stream is not active...")

print(f"Start send_tweet_when_start_stream.py...")
obspython.timer_add(timer_callback, 15 * 1000)




#some docs that helped me:
#https://obsproject.com/forum/threads/where-is-obspython-installed-so-my-ide-can-see-it.159866/
#https://obsproject.com/forum/threads/how-to-install-obspython-module.140041/
#https://obsproject.com/forum/threads/obs-stops-responding-when-setting-scene-within-timer-callback-python-script.158485/
#https://stackoverflow.com/questions/9768865/python-nonetype-object-is-not-callable-beginner
#https://docs.obsproject.com/scripting#script-timers
#https://github.com/obsproject/obs-studio/wiki/Scripting-Tutorial-Source-Shake
#https://docs.obsproject.com/reference-frontend-api#c.obs_frontend_recording_active
#https://dev.twitch.tv/console/
#https://dev.twitch.tv/docs/authentication/#user-access-tokens