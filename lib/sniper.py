import tkinter.font
import tkinter.messagebox
import os, sys, tkinter, json, asyncio, re, threading, webbrowser, time, random

import discord, requests, autoit
from bs4 import BeautifulSoup

import tkinter.messagebox as mb
from discord_webhook import DiscordWebhook, DiscordEmbed
from ppadb.client import Client as AdbClient
from tkinter import ttk
from ttkthemes import ThemedTk
from tkinter.font import Font
    
ui = ThemedTk(theme="plastik")
ui.title('Lazy Bum Sniper')
ui.geometry('275x175')
ui.resizable(False, False)
ui.wm_iconbitmap('lib/icon.ico')
ui.eval('tk::PlaceWindow . center')

def load_config():
    try:
        with open('config.json', "r") as file:
            return json.load(file)
    except FileNotFoundError:
        mb.showinfo(title='Error', message='config.json file not found, please reinstall')
    
config = load_config()

class configSaving:
    def save_config():
        config['token'] = token_entry.get()
        config['webhook_url'] = webhook_entry.get()
        config['user_id'] = userid_entry.get()
        
        config['glitched'] = glitchBiomeVar.get()
        config['dreamspace'] = dreamBiomeVar.get()
        config['voidcoin'] = voidcoinVar.get()
        config['jester'] = jesterVar.get()
        if len(channelIds) != 0:
            config['channel_ids'] = list(channelIds.values())
        
        config['pin_gui'] = pinVar.get()
        config['block_crosswoods'] = crossVar.get()
        config['auto_close_roblox'] = closeVar.get()
        
        try:
            with open('config.json', "w") as file:
                json.dump(config, file, indent=4)
        except FileNotFoundError:
            mb.showinfo(title='Error', message='config.json file not found, please reinstall')
        os.execv(sys.executable, ['python'] + sys.argv)

tabControl = ttk.Notebook(ui)

status = ttk.Frame(tabControl)
detection = ttk.Frame(tabControl)
settings = ttk.Frame(tabControl)
extra = ttk.Frame(tabControl)

detection.grid_columnconfigure(0, weight=1, uniform="equal")
detection.grid_columnconfigure(1, weight=1, uniform="equal")

settings.grid_columnconfigure(0, weight=1, uniform="equal")
settings.grid_columnconfigure(1, weight=1, uniform="equal")

tabControl.add(status, text='Status')
tabControl.add(detection, text='Detection')
tabControl.add(settings, text='Settings')
tabControl.add(extra, text='Extra')
tabControl.pack(expand=1, fill="both")

# status tab
status_var = tkinter.StringVar()
status_var.set('Status: Starting..')

watching_var = tkinter.StringVar()

status_label = tkinter.Label(status, textvariable=status_var, justify='center', font=("Helvetica", 10))
status_label.pack()
watching_label = tkinter.Label(status, text='Watching: ', justify='center', font=("Helvetica", 10))

version_var = tkinter.StringVar()
curr_version = 'v1.3.2'
version_var.set(curr_version)
version_label = tkinter.Label(status, textvariable=version_var, justify='center')
version_label.pack()

def listbox1OpenInBrowser():
    selected = watching_listbox.curselection()
    if selected:
        index = selected[0]
        try:
            url = bot.get_channel(channelIds.get(watching_listbox.get(index))).jump_url
            webbrowser.open(url)
        except:
            pass

watching_listbox = tkinter.Listbox(status, height=0, width=40, exportselection=0)
watching_listbox.bind("<Double-Button-1>", listbox1OpenInBrowser)

# detection tab
tkinter.Label(detection, text='Biomes:', font=("Helvetica", 10, "bold")).grid(row=0, column=0, sticky="w", padx=10, pady=2)
glitchBiomeVar = tkinter.BooleanVar(value=config.get('glitched', False))
glitchBiomeToggle = tkinter.Checkbutton(detection, text='Glitched', variable=glitchBiomeVar)
glitchBiomeToggle.grid(row=1, column=0, sticky="w", padx=10, pady=2)

dreamBiomeVar = tkinter.BooleanVar(value=config.get('dreamspace', False))
dreamBiomeToggle = tkinter.Checkbutton(detection, text='Dreamspace', variable=dreamBiomeVar)
dreamBiomeToggle.grid(row=2, column=0, sticky="w", padx=10, pady=2)

tkinter.Label(detection, text='Merchant:', font=("Helvetica", 10, "bold")).grid(row=0, column=1, sticky="w", padx=10, pady=2)
voidcoinVar = tkinter.BooleanVar(value=config.get('voidcoin', False))
vcToggle = tkinter.Checkbutton(detection, text='Void Coin', variable=voidcoinVar)
vcToggle.grid(row=1, column=1, sticky="w", padx=10, pady=2)

jesterVar = tkinter.BooleanVar(value=config.get('jester', False))
jesterToggle = tkinter.Checkbutton(detection, text='Jester', variable=jesterVar)
jesterToggle.grid(row=2, column=1, sticky="w", padx=10, pady=2)

save_button_detec = tkinter.Button(detection, text="Save", command=configSaving.save_config, justify='center')
save_button_detec.grid(row=3, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

# settings tab

tkinter.Label(settings, text='Token').grid(row=1, column=0)
token_entry = tkinter.Entry(settings, show='*')
token_entry.grid(row=1, column=1)
token_entry.insert(0, config.get('token', ''))

tkinter.Label(settings, text='Webhook URL').grid(row=2, column=0)
webhook_entry = tkinter.Entry(settings, show='*')
webhook_entry.grid(row=2, column=1)
webhook_entry.insert(0, config.get('webhook_url', ''))

tkinter.Label(settings, text='User ID').grid(row=3, column=0)
userid_entry = tkinter.Entry(settings)
userid_entry.grid(row=3, column=1)
userid_entry.insert(0, config.get('user_id', ''))

# extra tab
pinVar = tkinter.BooleanVar(value=config.get('pin_gui', False))
def pinGuiFunc():
    if pinVar.get():
        ui.wm_attributes("-topmost", True)
    else:
        ui.wm_attributes("-topmost", False)

pinToggle = tkinter.Checkbutton(extra, text='Pin Sniper Window', variable=pinVar, command=pinGuiFunc)
ui.wm_attributes("-topmost", pinVar.get())
pinToggle.pack()

crossVar = tkinter.BooleanVar(value=config.get('block_crosswoods', True))
crosswoodsToggle = tkinter.Checkbutton(extra, text='Block Crosswoods Links', variable=crossVar)
crosswoodsToggle.pack()

closeVar = tkinter.BooleanVar(value=config.get('auto_close_roblox', False))
closeToggle = tkinter.Checkbutton(extra, text='Automatically Close Windows Roblox', variable=closeVar)
closeToggle.pack()

save_button_extra = tkinter.Button(extra, text="Save", command=configSaving.save_config, justify='center')
save_button_extra.pack()

creditUiInstance = None
def openCredits():
    global creditUiInstance
    if creditUiInstance is None or not creditUiInstance.winfo_exists():
        creditUiMenu = tkinter.Toplevel(ui)
        creditUiMenu.resizable(False, False)
        creditUiMenu.title('Credits')
        creditUiMenu.geometry("275x140")
        creditUiMenu.wm_iconbitmap('lib/icon.ico')
        
        label = tkinter.Label(creditUiMenu, text='Credits:', font=("Helvetica", 10, 'bold'))
        label.pack()
        linkFont = Font(family="Helvetica", size=10, underline=True)
        azulLabel = tkinter.Label(creditUiMenu, text='azul - Developer', fg="blue", cursor="hand2", font=linkFont)
        azulLabel.pack()
        azulLabel.bind("<Button-1>", lambda event: webbrowser.open('https://github.com/azulzz'))
        zofuuLabel = tkinter.Label(creditUiMenu, text='zofuu - Idea', fg="blue", cursor="hand2", font=linkFont)
        zofuuLabel.pack()
        zofuuLabel.bind("<Button-1>", lambda event: webbrowser.open('https://discordapp.com/users/985682558354341928'))
        dannyesweLabel = tkinter.Label(creditUiMenu, text='dannw & yeswe - Keywords List', fg="blue", cursor="hand2", font=linkFont)
        dannyesweLabel.pack()
        dannyesweLabel.bind("<Button-1>", lambda event: webbrowser.open('https://discord.gg/solsniper'))
        donate_button_extra = tkinter.Button(creditUiMenu, text="Support Project", command=lambda: webbrowser.open('https://buymeacoffee.com/azulzz'), justify='center')
        donate_button_extra.pack()
        
        creditUiInstance = creditUiMenu

credits_button_extra = tkinter.Button(extra, text="Credits", command=openCredits, justify='center')
credits_button_extra.pack()

channelIdInstance = None

channelIds = {}

randomNum = random.randint(1, 1000)
if randomNum == 500:
    webbrowser.open_new_tab('https://c.tenor.com/lRbEhEq1zVIAAAAd/tenor.gif')
        
def openChannelIds():
    global channelIdInstance
    if channelIdInstance is None or not channelIdInstance.winfo_exists():   
        def addChannel(entry, listbox):
            channel_id = entry.get()
            try:
                channel = bot.get_channel(int(channel_id))
                if channel_id and channel_id.isdigit() and channel:
                    if isinstance(channel, discord.DMChannel):
                        channelIds[channel.recipient.name] = channel.id
                        listbox.insert(tkinter.END, channel.recipient.name)
                    else:
                        channelIds[channel.name] = channel.id
                        listbox.insert(tkinter.END, channel.name)
                    entry.delete(0, tkinter.END)
            except Exception as e:
                mb.showerror(title='Error', message='Invalid Channel ID(s)')

        def updateListbox(listbox, channels):
            listbox.delete(0, tkinter.END)
            for channel in channels:
                if isinstance(channel, discord.DMChannel):
                    channelIds[channel.recipient.name] = channel.id
                else:
                    channelIds[channel.name] = channel.id
                listbox.insert(tkinter.END, channel)
        
        def deleteChannel(listbox):
            try:
                selected_index = listbox.curselection()[0]
                channel_name = listbox.get(selected_index)
                
                channel2 = (str(channel_name).removeprefix('Direct Message with ')).removesuffix('#0')
                if isinstance(bot.get_channel(channelIds.get(channel2)), discord.DMChannel):
                    del channelIds[channel2]
                else:
                    del channelIds[channel_name]
                listbox.delete(selected_index)
            except IndexError:
                pass 
            
        def listbox2OpenInBrowser():
            selected = watching_listbox.curselection()
            if selected:
                index = selected[0]
                try:
                    url = bot.get_channel(channelIds.get(watching_listbox2.get(index))).jump_url
                    webbrowser.open(url)
                except:
                    pass
        
        channelIdMenu = tkinter.Toplevel(ui)
        channelIdMenu.resizable(False, False)
        channelIdMenu.title('Channel ID(s)')
        channelIdMenu.geometry("300x200")
        channelIdMenu.wm_iconbitmap('lib/icon.ico')

        channelIdMenu.grid_columnconfigure(0, weight=1)
        channelIdMenu.grid_columnconfigure(1, weight=1)
        channelIdMenu.grid_columnconfigure(2, weight=1)

        channelIdEntry = tkinter.Entry(channelIdMenu, foreground="gray")
        channelIdEntry.grid(row=0, column=0, padx=5, pady=5, sticky='ew')
        channelIdEntry.insert(0, 'Channel ID')
        
        def on_entry_click(event):
            if channelIdEntry.get() == "Channel ID":
                channelIdEntry.delete(0, tkinter.END)
                channelIdEntry.configure(foreground="black")

        def on_focus_out(event):
            if channelIdEntry.get() == "":
                channelIdEntry.insert(0, "Channel ID")
                channelIdEntry.configure(foreground="gray")
            
        channelIdEntry.bind("<FocusIn>", on_entry_click)
        channelIdEntry.bind("<FocusOut>", on_focus_out)

        addButton = tkinter.Button(channelIdMenu, text='Add', command=lambda: addChannel(channelIdEntry, watching_listbox2))
        addButton.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        watching_listbox2 = tkinter.Listbox(channelIdMenu, height=6, width=40)
        watching_listbox2.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        watching_listbox2.bind("<Double-Button-1>", listbox2OpenInBrowser)

        deleteButton = tkinter.Button(channelIdMenu, text='Delete', command=lambda: deleteChannel(watching_listbox2))
        deleteButton.grid(row=2, column=2, padx=5, pady=5, sticky='ew')

        saveButton = tkinter.Button(channelIdMenu, text='Save', command=configSaving.save_config)
        saveButton.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky='ew')
        
        channels = [bot.get_channel(int(cid)) for cid in config['channel_ids']]
        updateListbox(watching_listbox2, channels)

        channelIdInstance = channelIdMenu

tkinter.Label(settings, text='Channel IDs').grid(row=4, column=0)
channelids_button = tkinter.Button(settings, text='Open', command=openChannelIds)
channelids_button.grid(row=4, column=1, sticky="w", padx=5, pady=5)

save_button = tkinter.Button(settings, text="Save", command=configSaving.save_config, justify='center')
save_button.grid(row=5, column=0, columnspan=2, sticky="ew", padx=10, pady=5)

client = AdbClient(host="127.0.0.1", port=5037)

keywords_list = requests.get('https://raw.githubusercontent.com/dannws/keywords/refs/heads/main/keywords.json').json()
r_pattern = r"https:\/\/www\.roblox\.com\/(games\/\d+\/[a-zA-Z0-9\-]+\/?\?privateServerLinkCode=\d+|share\?code=[a-f0-9]{32}&type=Server)"
ps_pattern = r"https:\/\/www\.roblox\.com\/games\/15532962292\/[a-zA-Z0-9\-]+\/?\?privateServerLinkCode=\d+"

channel_ids = {1349880765487386675}
debounce = False

def find_roblox_share_link(message):
    match = re.search(r_pattern, message)
    if match:
        return match.group(0)
    return None

def checkGlitch(msg):
    msg_lowered = msg.lower()

    for forbidden in keywords_list['disallowed'] + keywords_list['Gdisallowed']:
        if forbidden.replace('<space>', ' ') in msg_lowered and forbidden != 'sol':
            return False

    for allowed in keywords_list['allowedG']:
        if allowed.replace('<space>', ' ') in msg_lowered:
            return True

    return False


def checkDream(msg):
    msg_lowered = msg.lower()
    
    for forbidden in keywords_list['disallowed'] + keywords_list['Ddisallowed']:
        if forbidden.replace('<space>', ' ') in msg_lowered and forbidden != 'sol':
            return False
    
    for allowed in keywords_list['allowedD']:
        if allowed.replace('<space>', ' ') in msg_lowered:
            return True
    
    return False

def checkVoid(msg):
    msg_lowered = msg.lower()
    
    for forbidden in keywords_list['disallowed'] + keywords_list['Vdisallowed']:
        if forbidden.replace('<space>', ' ') in msg_lowered and forbidden != 'sol':
            return False
    
    for allowed in keywords_list['allowedV']:
        if allowed.replace('<space>', ' ') in msg_lowered:
            return True
    
    return False

def checkJester(msg):
    msg_lowered = msg.lower()
    
    for forbidden in keywords_list['disallowed'] + keywords_list['Jdisallowed']:
        if forbidden.replace('<space>', ' ') in msg_lowered and forbidden != 'sol':
            return False
    
    for allowed in keywords_list['allowedJ']:
        if allowed.replace('<space>', ' ') in msg_lowered:
            return True
    
    return False

allowed_mentions = {"users": [config['user_id']]}

def sendCWebhook(jump_url, author, game_link, private_server, content):
    webhook = DiscordWebhook(url=config['webhook_url'], allowed_mentions=allowed_mentions)
    
    embed = DiscordEmbed(title="Blocked Possible Crosswoods Link", description="You have automatically been removed from the game", color=0xf54254)
    embed.set_footer("Crosswoods links are private servers which get you banned on roblox upon joining them, but you were automatically removed, so you don't need to worry aboout being banned")
    embed.add_embed_field('Message', jump_url)
    embed.add_embed_field('Author', f'<@{author['id']}>', True)
    embed.add_embed_field('Game Link', f'||{game_link}||', False)
    embed.add_embed_field('Private Server Link', f'||{private_server}||', False)
    embed.add_embed_field('Content', f'```{content}\n```', False)
    
    webhook.add_embed(embed)
    webhook.execute()

def getBiome(member: discord.Member):
    presence = member.activities
    for activity in presence:
        if activity and activity.type == discord.ActivityType.playing and "sol's rng" in activity.details.lower():
            return activity.large_image_text

def sendWebhook(type, author, jump_url, private_server, content):
    webhook = DiscordWebhook(url=config['webhook_url'], content= f'<@{config["user_id"]}>', allowed_mentions=allowed_mentions)
    embed = DiscordEmbed()
    
    embed.add_embed_field('Message', jump_url)
    embed.add_embed_field('Author', f'<@{author['id']}>', True)
    embed.add_embed_field('Private Server Link', private_server, False)
    embed.add_embed_field('Content', f'```{content}\n```', False)
    
    member = discord.utils.get(bot.get_all_members(), id=int(author['id']))
    currBiome = getBiome(member)
    
    match type:
        case "GLITCHED":
            embed.set_title('Glitched')
            embed.set_description(f'> <t:{round(time.time())}:R>')
            embed.set_color(0x45B947)
            embed.set_thumbnail(url='https://static.wikia.nocookie.net/sol-rng/images/c/cd/Glitch_Tree.png/revision/latest?cb=20250209093856')
        case "DREAMSPACE":
            print('dream')
            embed.set_title('Dreamspace')
            embed.set_description(f'> <t:{round(time.time())}:R>')
            embed.set_color(0xEF87DD)
            embed.set_thumbnail(url='https://static.wikia.nocookie.net/sol-rng/images/d/d2/Dreamspace_chair.png/revision/latest?cb=20250209094428')
        case "jester":
            embed.set_title('Jester')
            embed.set_description(f'> <t:{round(time.time())}:R>')
            embed.set_color(0x9d03fc)
            embed.set_thumbnail(url='https://static.wikia.nocookie.net/sol-rng/images/d/db/Headshot_of_Jester.png/revision/latest?cb=20240630142936')
        case "void":
            embed.set_title('Void Coin')
            embed.set_description(f'> <t:{round(time.time())}:R>')
            embed.set_color(0x9d03fc)
            embed.set_thumbnail(url='https://static.wikia.nocookie.net/sol-rng/images/3/3b/Void_Coin_Inv.gif/revision/latest?cb=20240630093932')
    
    if (type == 'GLITCHED' or type == 'DREAMSPACE'):
        if currBiome == type:
            embed.set_footer(f'Most likely real, their current biome is actually {currBiome}')
        elif currBiome is None:
            embed.set_footer('Unable to verify due to the user not having a rich presence')
        else:
            embed.set_footer(f'Most likely fake, their current biome is actually {currBiome}')
    
    webhook.add_embed(embed)
    webhook.execute()
    
def joinPS(private_server):
    match = bool(re.search(ps_pattern, private_server))
    
    if match:
        for device in client.devices():
            device.shell(f"am start -a android.intent.action.VIEW -d '{private_server}' com.roblox.client")
    else:
        for device in client.devices():
            device.shell(f"am start -a android.intent.action.VIEW -d '{private_server}'")
        

def checkGameID(private_server):
    try:
        response = requests.get(private_server)
        
        soup = BeautifulSoup(response.text, 'html.parser')
        meta_tag = soup.find('meta', attrs={'name': 'roblox:start_place_id'})
        
        if meta_tag and meta_tag.has_attr('content'):
            return meta_tag['content']
    except:
        pass
    return None

def handle_message(content, private_server_url, author, jump_url):
    check_functions = {
        "GLITCHED": checkGlitch,
        "DREAMSPACE": checkDream,
        "jester": checkJester,
        "void": checkVoid
    }
    
    for event_type, check_function in check_functions.items():
        if config[event_type.lower()] and check_function(content) :
            joinPS(private_server_url)
            
            gameID = checkGameID(private_server_url)
            if gameID == '15532962292':
                sendWebhook(event_type, author, jump_url, private_server_url, content)
            else:
                for device in client.devices():
                    device.shell(f"am start -a android.intent.action.VIEW -d 'roblox://placeID=0'")
                
                sendCWebhook(jump_url, author, f'https://www.roblox.com/games/{gameID}', private_server_url, content)
                
            return

class clientHandler(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)
        problem = False
        
        if not problem:
            try:
                if not os.path.exists(os.path.join(r"C:\LDPlayer\LDPlayer9")):
                    problem = True
                    status_var.set("LDPlayer isn't installed")
            except Exception as e:
                print(e)
        
        if not problem:
            try:
                autoit.win_get_handle('LDPlayer')
            except:
                problem = True
                status_var.set("LDPLayer isn't open")
        
        if not problem:
            try:
                if len(client.devices()) == 0:
                    raise
            except:
                problem = True
                status_var.set("ADB isn't enabled")
        
        if not problem:
            try:
                for device in client.devices():
                    if not device.is_installed("com.roblox.client"):
                        problem = True
                        status_var.set(f"Roblox isn't installed on {device.serial}")
                        break
            except Exception as e:
                status_var.set(f'Error: {e}')
                problem = True
        
        if not problem:
            try:
                requests.get(config['webhook_url'])
            except:
                problem = True
                status_var.set('Invalid Webhook')
        
        if not problem: 
            try:
                if isinstance(config['channel_ids'], list):
                    for channel in config['channel_ids']:
                        channel_obj = bot.get_channel(int(channel))
                        if channel_obj == None:
                            raise
                        
                        if isinstance(channel_obj, discord.DMChannel):
                            channelIds[channel_obj.recipient.name] = channel_obj.id
                        else:
                            channelIds[channel_obj.name] = channel_obj.id
                else:
                    raise
            except:
                problem = True
                status_var.set('Invalid Channel ID(s)')
        
        if not problem:
            try:
                if config['user_id'].isdigit():
                    user_obj = bot.get_user(int(config['user_id']))
                    if user_obj == None:
                        raise
                else:
                    raise
            except:
                problem = True
                status_var.set('Invalid User ID')
        
        if problem == False:
            status_var.set(f'Status: Running on {self.user.name}')
            channels = [bot.get_channel(int(cid)) for cid in config['channel_ids']]
            watching_label.pack()
            watching_listbox.pack()
            watching_listbox.config(height=len(channels))
            index = 0
            for channel in channels:
                watching_listbox.insert(index, channel)
                index += 1
        else:
            await bot.close()
            
    async def on_socket_raw_receive(self, msg):
        if not msg:
            return
        
        if isinstance(msg, bytes):
            msg = msg.decode('utf-8')
            
        if not msg.startswith('{'):
            return
        
        data = json.loads(msg)
        if data.get('t') != 'MESSAGE_CREATE':
            return
        message_data = data.get("d", {})
        
        author = message_data.get('author')
        channel_id = int(message_data.get('channel_id'))
        
        if channel_id not in channel_ids:
            return
        
        if author['id'] in keywords_list['blocked_users_ids']:
            return
        
        content = message_data.get('content')
        private_server_url = find_roblox_share_link(content)
        
        if not private_server_url:
            return
        
        if debounce:
            return
        
        message_id = message_data.get('id')
        guild_id = message_data.get('guild_id')
        
        if guild_id:
            jump_url = f"https://discord.com/channels/{guild_id}/{channel_id}/{message_id}"
        else:
            jump_url = f"https://discord.com/channels/@me/{channel_id}/{message_id}"
        
        handle_message(content, private_server_url, author, jump_url)

bot = clientHandler(enable_debug_events=True)

def check_for_updates():
    global curr_version
    
    if config['dontaskagain'] == False:
        response = requests.get("https://api.github.com/repos/azulzz/lazy-bum-sniper/releases/latest")
        response.raise_for_status()
        latest_release = response.json()
        latest_ver = latest_release['tag_name']
        
        if latest_ver != curr_version:
            message = f"New update of this macro {latest_ver} is available. Do you want to download the newest version?"
            if mb.askyesno("Update Available", message) == True :
                download_url = latest_release['assets'][0]['browser_download_url']
                webbrowser.open(download_url)
                exit()
            else:
                if mb.askyesno("Don't Ask Again", "Would you like to stop receiving update notifications?"):
                    config['dontaskagain'] = True
                    configSaving.save_config()

check_for_updates()

async def run_bot():
    try:
        await bot.start(config['token'])
    except discord.errors.LoginFailure:
        status_var.set('Invalid Token')
    except discord.errors.ConnectionClosed:
        mb.showerror('Error', message='Connection Closed')
        
def start_bot_thread():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_bot())

bot_thread = threading.Thread(target=start_bot_thread, daemon=True)
bot_thread.start()

ui.mainloop()