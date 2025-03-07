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

version_label = tkinter.Label(status, text='Version: 1.2.0', justify='center')
version_label.pack()

def listbox1OpenInBrowser(event):
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
            
        def listbox2OpenInBrowser(event):
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

share_ps_pattern = r"https:\/\/www\.roblox\.com\/share\?code=[a-f0-9]{32}&type=Server"
ps_pattern = r"https:\/\/www\.roblox\.com\/games\/15532962292\/[a-zA-Z0-9\-]+\/?\?privateServerLinkCode=\d+"
r_pattern = r"https:\/\/www\.roblox\.com\/(games\/\d+\/[a-zA-Z0-9\-]+\/?\?privateServerLinkCode=\d+|share\?code=[a-f0-9]{32}&type=Server)"

keywords_list = requests.get('https://raw.githubusercontent.com/dannws/keywords/refs/heads/main/keywords.json').json()

def find_roblox_share_link(message):
    match = re.search(r_pattern, message)
    if match:
        return match.group(0)
    return None

def checkGlitch(msg):
    msg_lowered = msg.content.lower()

    for forbidden in keywords_list['disallowed'] + keywords_list['Gdisallowed']:
        if forbidden.replace('<space>', ' ') in msg_lowered and forbidden != 'sol':
            return False

    for allowed in keywords_list['allowedG']:
        if allowed.replace('<space>', ' ') in msg_lowered:
            return True

    return False


def checkDream(msg):
    msg_lowered = msg.content.lower()
    
    for forbidden in keywords_list['disallowed'] + keywords_list['Ddisallowed']:
        if forbidden.replace('<space>', ' ') in msg_lowered and forbidden != 'sol':
            return False
    
    for allowed in keywords_list['allowedD']:
        if allowed.replace('<space>', ' ') in msg_lowered:
            return True
    
    return False

def checkVoid(msg):
    msg_lowered = msg.content.lower()
    
    for forbidden in keywords_list['disallowed'] + keywords_list['Vdisallowed']:
        if forbidden.replace('<space>', ' ') in msg_lowered and forbidden != 'sol':
            return False
    
    for allowed in keywords_list['allowedV']:
        if allowed.replace('<space>', ' ') in msg_lowered:
            return True
    
    return False

def checkJester(msg):
    msg_lowered = msg.content.lower()
    
    for forbidden in keywords_list['disallowed'] + keywords_list['Jdisallowed']:
        if forbidden.replace('<space>', ' ') in msg_lowered and forbidden != 'sol':
            return False
    
    for allowed in keywords_list['allowedJ']:
        if allowed.replace('<space>', ' ') in msg_lowered:
            return True
    
    return False

async def sendScreenshot():
    await asyncio.sleep(25)
    imageWebhook = DiscordWebhook(url=config['webhook_url'])
    for device in client.devices():
        result = device.screencap()
            
        imageWebhook.add_file(file=result, filename=f'screenshot-{device.serial}.png')
    await imageWebhook.execute()

debounce = False

async def debounce_func():
    global debounce
    debounce = True
    await asyncio.sleep(128)
    debounce = False
    
def check_id(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        meta_tag = soup.find('meta', attrs={'name': 'roblox:start_place_id'})
        if meta_tag and meta_tag.has_attr('content'):
            return meta_tag['content']
            # if meta_tag['content'] == '15532962292':
            #     return True
            # else:
            #     return False
    except:
        pass
    return None

allowed_mentions = {"parse": [], "users": [config['user_id']]}

class MyBot(discord.Client):
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
        
    async def on_message(self, message):
        # 1282542323590496277
        if message.author.id not in keywords_list['blocked_users_ids'] and message.channel.id in config['channel_ids']:
            private_server_url = find_roblox_share_link(message.content)
            match = bool(re.search(ps_pattern, message.content))
            if private_server_url and not debounce:
                if config['glitched'] == True and checkGlitch(message):
                    try:
                        if config['auto_close_roblox']:
                            autoit.win_kill('Roblox')
                    except:
                        print('Roblox not open')
                    autoit.win_activate('LDPlayer')
                        
                    for device in client.devices():
                        if match == True:
                            device.shell(f"am start -a android.intent.action.VIEW -d '{private_server_url}' com.roblox.client")
                        else:
                            device.shell(f"am start -a android.intent.action.VIEW -d '{private_server_url}'")
                    
                    check = check_id(private_server_url)
                    if config['block_crosswoods'] and match == False and check != '15532962292':
                        for device in client.devices():
                            device.shell(f"am start -a android.intent.action.VIEW -d 'roblox://placeID=0'")
                        crosswoods_webhook = DiscordWebhook(url=config['webhook_url'], allowed_mentions=allowed_mentions)
                        crosswoods_embed = DiscordEmbed(title="Blocked Possible Crosswoods Link", description="You have automatically been removed from the game, so you don't have to worry about being banned.", color=0xf54254)
                        crosswoods_embed.set_footer("Please report this to the Sol's RNG Staff")
                        crosswoods_embed.add_embed_field('Message', message.jump_url)
                        crosswoods_embed.add_embed_field('Author', f'<@{message.author.id}>', True)
                        crosswoods_embed.add_embed_field('Game Link', f'https://www.roblox.com/games/{check_id(private_server_url)}', True)
                        crosswoods_embed.add_embed_field('Private Server Link', private_server_url, False)
                        crosswoods_embed.add_embed_field('Content', f'```{message.content}\n```', False)
                        
                        crosswoods_webhook.add_embed(crosswoods_embed)
                        crosswoods_webhook.execute()
                    else:
                        asyncio.create_task(debounce_func())
                        glitch_embed = DiscordEmbed(title='Glitched', description=f'> <t:{round(time.time())}:R>', color=0x45B947)
                        # glitch_embed.set_timestamp(time.time())
                        glitch_embed.add_embed_field('Message', message.jump_url)
                        glitch_embed.add_embed_field('Author', f'<@{message.author.id}>', True)
                        glitch_embed.add_embed_field('Private Server Link', private_server_url, False)
                        glitch_embed.add_embed_field('Content', f'```{message.content}\n```', False)
                        glitch_embed.set_thumbnail(url='https://static.wikia.nocookie.net/sol-rng/images/c/cd/Glitch_Tree.png/revision/latest?cb=20250209093856')
                        
                        glitch_webhook = DiscordWebhook(url=config['webhook_url'], content= f'<@{config["user_id"]}>', allowed_mentions=allowed_mentions)
                        glitch_webhook.add_embed(glitch_embed)
                        glitch_webhook.execute()
                        
                        await asyncio.create_task(sendScreenshot())
                    
                elif config['dreamspace'] == True and checkDream(message):
                    try:
                        if config['auto_close_roblox']:
                            autoit.win_kill('Roblox')
                    except:
                        print('Roblox not open')
                    
                    for device in client.devices():
                        if match == True:
                            device.shell(f"am start -a android.intent.action.VIEW -d '{private_server_url}' com.roblox.client")
                        else:
                            device.shell(f"am start -a android.intent.action.VIEW -d '{private_server_url}'")
                    
                    check = check_id(private_server_url)
                    if config['block_crosswoods'] and match == False and check != '15532962292':
                        for device in client.devices():
                            device.shell(f"am start -a android.intent.action.VIEW -d 'roblox://placeID=0'")
                        crosswoods_webhook = DiscordWebhook(url=config['webhook_url'], allowed_mentions=allowed_mentions)
                        crosswoods_embed = DiscordEmbed(title="Blocked Possible Crosswoods Link", description="You have automatically been removed from the game, so you don't have to worry about being banned.", color=0xf54254)
                        crosswoods_embed.set_footer("Please report this to the Sol's RNG Staff")
                        crosswoods_embed.add_embed_field('Message', message.jump_url)
                        crosswoods_embed.add_embed_field('Author', f'<@{message.author.id}>', True)
                        crosswoods_embed.add_embed_field('Game Link', f'https://www.roblox.com/games/{check_id(private_server_url)}', True)
                        crosswoods_embed.add_embed_field('Private Server Link', private_server_url, False)
                        crosswoods_embed.add_embed_field('Content', f'```{message.content}\n```', False)
                        
                        crosswoods_webhook.add_embed(crosswoods_embed)
                        crosswoods_webhook.execute()
                    else:
                        asyncio.create_task(debounce_func())
                        dream_embed = DiscordEmbed(title='Dreamspace', description=f'> <t:{round(time.time())}:R>', color=0xEF87DD)
                        dream_embed.add_embed_field('Message', message.jump_url)
                        dream_embed.add_embed_field('Author', f'<@{message.author.id}>', True)
                        dream_embed.add_embed_field('Private Server Link', private_server_url, False)
                        dream_embed.add_embed_field('Content', f'```{message.content}\n```', False)
                        dream_embed.set_thumbnail('https://static.wikia.nocookie.net/sol-rng/images/d/d2/Dreamspace_chair.png/revision/latest?cb=20250209094428')
                        
                        dream_webhook = DiscordWebhook(url=config['webhook_url'], content= f'<@{config["user_id"]}>', allowed_mentions=allowed_mentions)
                        dream_webhook.add_embed(dream_embed)
                        dream_webhook.execute()
                        
                        asyncio.create_task(sendScreenshot())
                elif config['jester'] == True and checkJester(message):
                    try:
                        if config['auto_close_roblox']:
                            autoit.win_kill('Roblox')
                    except:
                        print('Roblox not open')
                        
                    autoit.win_activate('LDPlayer')
                    for device in client.devices():
                        if match == True:
                            device.shell(f"am start -a android.intent.action.VIEW -d '{private_server_url}' com.roblox.client")
                        else:
                            device.shell(f"am start -a android.intent.action.VIEW -d '{private_server_url}'")

                    check = check_id(private_server_url)
                    if config['block_crosswoods'] and match == False and check != '15532962292':
                        for device in client.devices():
                            device.shell(f"am start -a android.intent.action.VIEW -d 'roblox://placeID=0'")
                        crosswoods_webhook = DiscordWebhook(url=config['webhook_url'], allowed_mentions=allowed_mentions)
                        crosswoods_embed = DiscordEmbed(title="Blocked Possible Crosswoods Link", description="You have automatically been removed from the game, so you don't have to worry about being banned.", color=0xf54254)
                        crosswoods_embed.set_footer("Please report this to the Sol's RNG Staff")
                        crosswoods_embed.add_embed_field('Message', message.jump_url)
                        crosswoods_embed.add_embed_field('Author', f'<@{message.author.id}>', True)
                        crosswoods_embed.add_embed_field('Game Link', f'https://www.roblox.com/games/{check_id(private_server_url)}', True)
                        crosswoods_embed.add_embed_field('Private Server Link', private_server_url, False)
                        crosswoods_embed.add_embed_field('Content', f'```{message.content}\n```', False)
                        
                        crosswoods_webhook.add_embed(crosswoods_embed)
                        crosswoods_webhook.execute()
                    else:
                        jester_embed = DiscordEmbed(title='Jester', description=f'> <t:{round(time.time())}:R>', color=0x9d03fc)
                        jester_embed.add_embed_field('Message', message.jump_url)
                        jester_embed.add_embed_field('Author', f'<@{message.author.id}>', True)
                        jester_embed.add_embed_field('Private Server Link', private_server_url, False)
                        jester_embed.add_embed_field('Content', f'```{message.content}\n```', False)
                        jester_embed.set_thumbnail('https://static.wikia.nocookie.net/sol-rng/images/d/db/Headshot_of_Jester.png/revision/latest?cb=20240630142936')
                        
                        jester_webhook = DiscordWebhook(url=config['webhook_url'], content= f'<@{config["user_id"]}>', allowed_mentions=allowed_mentions)
                        jester_webhook.add_embed(jester_embed)
                        jester_webhook.execute()
                elif config['voidcoin'] == True and checkVoid(message):
                    try:
                        if config['auto_close_roblox']:
                            autoit.win_kill('Roblox')
                    except:
                        print('Roblox not open')
                    
                    for device in client.devices():
                        if match == True:
                            device.shell(f"am start -a android.intent.action.VIEW -d '{private_server_url}' com.roblox.client")
                        else:
                            device.shell(f"am start -a android.intent.action.VIEW -d '{private_server_url}'")

                    check = check_id(private_server_url)
                    if config['block_crosswoods'] and match == False and check != '15532962292':
                        for device in client.devices():
                            device.shell(f"am start -a android.intent.action.VIEW -d 'roblox://placeID=0'")
                        crosswoods_webhook = DiscordWebhook(url=config['webhook_url'], allowed_mentions=allowed_mentions)
                        crosswoods_embed = DiscordEmbed(title="Blocked Possible Crosswoods Link", description="You have automatically been removed from the game, so you don't have to worry about being banned.", color=0xf54254)
                        crosswoods_embed.set_footer("Please report this to the Sol's RNG Staff")
                        crosswoods_embed.add_embed_field('Message', message.jump_url)
                        crosswoods_embed.add_embed_field('Author', f'<@{message.author.id}>', True)
                        crosswoods_embed.add_embed_field('Game Link', f'https://www.roblox.com/games/{check_id(private_server_url)}', True)
                        crosswoods_embed.add_embed_field('Private Server Link', private_server_url, False)
                        crosswoods_embed.add_embed_field('Content', f'```{message.content}\n```', False)
                        
                        crosswoods_webhook.add_embed(crosswoods_embed)
                        crosswoods_webhook.execute()
                    else:
                        vc_embed = DiscordEmbed(title='Void Coin', description=f'> <t:{round(time.time())}:R>', color=0x9d03fc)
                        vc_embed.add_embed_field('Message', message.jump_url)
                        vc_embed.add_embed_field('Author', f'<@{message.author.id}>', True)
                        vc_embed.add_embed_field('Private Server Link', private_server_url, False)
                        vc_embed.add_embed_field('Content', f'```{message.content}\n```', False)
                        vc_embed.set_thumbnail('https://static.wikia.nocookie.net/sol-rng/images/3/3b/Void_Coin_Inv.gif/revision/latest?cb=20240630093932')
                        
                        vc_webhook = DiscordWebhook(url=config['webhook_url'], content= f'<@{config["user_id"]}>', allowed_mentions=allowed_mentions)
                        vc_webhook.add_embed(vc_embed)
                        vc_webhook.execute()
bot = MyBot()

async def run_bot():
    try:
        await bot.start(config['token'])
    except discord.errors.LoginFailure:
        status_var.set('Invalid Token')
    except discord.errors.ConnectionClosed as e:
        mb.showerror('Error', message='Connection Closed')
        
def start_bot_thread():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_bot())

bot_thread = threading.Thread(target=start_bot_thread, daemon=True)
bot_thread.start()

ui.mainloop()