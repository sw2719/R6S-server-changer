import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox as msgbox
import os
import subprocess

USER_DIR = os.path.expanduser('~')
R6_DIR = USER_DIR + '\\Documents\\My Games\\Rainbow Six - Siege'

for root, dirs, files in os.walk(R6_DIR):
    if 'GameSettings.ini' in files:
        R6_INI = root + '\\GameSettings.ini'
        R6_INI_ALT = root + '\\GameSettings_.ini'

sv_dict = {
    'default': '핑 기반 (자동) - default',
    'eus':     '미국 동부 - eus',
    'cus':     '미국 중부 - cus',
    'scus':    '미국 남부 - scus',
    'wus':     '미국 서부 - wus',
    'sbr':     '브라질 남부 - sbr',
    'neu':     '북유럽 - neu',
    'weu':     '서유럽 - weu',
    'eas':     '동아시아 - eas',
    'seas':    '동남아시아 - seas',
    'eau':     '호주 동부 - eau',
    'wja':     '일본 서부 - wja'
}


def get_current():
    with open(R6_INI, 'r') as f:
        ini = f.readlines()

    for line in ini:
        if 'DataCenterHint=' in line:
            value = line.strip().split('=')[1]
            return value


def change():
    index = server_cbox.current()
    target = tuple(sv_dict.keys())[index]
    print('Target server is' , target)

    with open(R6_INI, 'r') as f:
        ini = f.readlines()

    for index, line in enumerate(ini):
        if 'DataCenterHint=' in line:
            ini[index] = f'DataCenterHint={target}\n'

    with open(R6_INI, 'w') as f:
        for line in ini:
            f.write(line)

    if get_current() != target:
        msgbox.showerror('오류', '서버를 변경하는데 실패했습니다')

    current.set('현재 서버: ' + sv_dict[get_current()].split(' - ')[0])
    main.update()


def open_r6_steam():
    try:
        print('Launching Steam...')
        subprocess.run("start steam://rungameid/359550",
                       shell=True, check=True)
        main.destroy()
    except subprocess.CalledProcessError:
        msgbox.showwarning('오류', '게임을 실행할 수 없습니다')
        pass


main = tk.Tk()
main.title("")
main.geometry("210x160+600+250")
main.resizable(False, False)

current = tk.StringVar()
try:
    current.set('현재 서버: ' + sv_dict[get_current()].split(' - ')[0])
except KeyError:
    current.set('현재 서버: 알 수 없음')

current_label = tk.Label(main, textvariable=current)
current_label.pack(side='top', anchor='w', padx=11, pady=(9, 0))

server_cbox = ttk.Combobox(main,
                           state="readonly",
                           values=list(sv_dict.values()),
                           width=30,
                           height=12)
try:
    server_cbox.set(sv_dict[get_current()])
except KeyError:
    pass
server_cbox.pack(side='top', anchor='center', padx=11, pady=(11, 1))

button_frame = tk.Frame(main)
button_frame.pack(side='bottom', pady=(3, 6))

exit_button = ttk.Button(button_frame, text='나가기', width=8)
exit_button['command'] = main.destroy
exit_button.pack(side='left', padx=3)

change_button = ttk.Button(button_frame, text='변경', width=13)
change_button['command'] = change
change_button.pack(side='right', padx=3)

open_r6_steam_button = ttk.Button(main, text='게임 실행 (Steam)', width=23)
open_r6_steam_button['command'] = open_r6_steam
open_r6_steam_button.pack(side='bottom', padx=11, pady=3)

main.mainloop()