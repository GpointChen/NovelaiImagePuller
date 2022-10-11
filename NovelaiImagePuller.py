# importing the requests library
import requests
import random
import base64
import math
from datetime import datetime
import tkinter as tk
import json
import os
import shutil
import threading
import logging


# global variables
my_config = {
    "input": "masterpiece,",
    "number": 3,
    "model": "NAI Diffusion Anime (Curated)",
    "resolution": "Portrait (Normal): 512x768",
    "scale": 12,
    "sampler": "k_euler_ancestral",
    "steps": 28,
    "ucPreset": 0,
    "uc": "lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry"
}
resolutions = ["Portrait (Normal): 512x768",
               "Landscape (Normal): 768x512",
               "Square (Normal): 640x640",
               "Portrait (Small): 384x640",
               "Landscape (Small): 640x384",
               "Square (Small): 512x512"]
models = {
    "NAI Diffusion Anime (Curated)": "safe-diffusion",
    "NAI Diffusion Anime (Full)": "nai-diffusion",
    "NAI Diffusion Furry (Beta)": "nai-diffusion-furry"
}
samplers = ['k_euler_ancestral', 'k_euler', 'k_lms', 'plms', 'ddim']
URL = "https://api.novelai.net/ai/generate-image"
key = "Put your key here"
global_save_path = "download\\"


def gui():
    def save():
        global key, my_config
        try:
            my_config = {
                "input": input_entry.get("1.0", 'end-1c'),
                "number": int(num_var.get()),
                "model": model_var.get(),
                "resolution": resol_var.get(),
                "scale": int(scale_var.get()),
                "sampler": sampler_var.get(),
                "steps": int(steps_var.get()),
                "ucPreset": 0,
                "uc": uc_entry.get("1.0", 'end-1c')
            }
            with open('settings.json', 'w', encoding='UTF-8') as f:
                json.dump(my_config, f, indent=4)
            key = key_entry.get()
            with open('key.json', 'w', encoding='UTF-8') as f:
                json.dump({"key": key}, f, indent=4)
            logging.info("Config saved in settings.json.")

        except Exception as e:
            logging.exception(e)
            progress.config(text="錯誤發生。儲存失敗。")

    def process(n, p_config):
        global key, global_save_path
        if not key:
            progress.config(text="沒有驗證金鑰。下載失敗。")
            logging.warning("No key detected. Please check your key.json.")
            return None

        try:
            my_headers = {
                "Content-Type": "application/json",
                "authorization": key,
                "authority": "api.novelai.net",
                "accept": "/",
                "content-type": "application/json",
                "origin": "https://novelai.net/",
                "referer": "https://novelai.net/"
            }

            resol_list = p_config["resolution"].split()[-1].split("x")

            my_data = {
                "input": p_config['input'],
                "model": models[p_config['model']],
                "parameters": {
                    "width": int(resol_list[0]),
                    "height": int(resol_list[1]),
                    "scale": p_config['scale'],
                    "sampler": p_config['sampler'],
                    "steps": p_config['steps'],
                    "n_samples": 1,
                    "ucPreset": 0,
                    "uc": p_config['uc']
                }
            }

            # make dir
            current_time = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
            global_save_path = "download\\%s\\" % current_time
            save_path = global_save_path
            if not os.path.isdir(save_path):
                os.mkdir(save_path)
            shutil.copy('settings.json', save_path + 'settings.json')
            success = 0
            logging.info('Save path: %s' % save_path)
            logging.info('parameters: %s' % json.dumps(my_data))

            for i in range(1, n + 1):
                seed = math.floor(random.random() * 4294967296)
                my_data["parameters"]["seed"] = seed
                filename = "ID-%04d-SEED-%d.png" % (i, seed)
                now_at = "%s%s (%d/%d)" % (save_path, filename, i, n)
                progress.config(text=now_at)
                logging.info(now_at)

                # get the file
                r = requests.post(url=URL, headers=my_headers, json=my_data)
                if r.status_code == requests.codes.created:
                    with open(save_path + filename, 'wb') as out_file:
                        data = r.text.replace(
                            "event: newImage\nid: 1\ndata:", "")
                        out_file.write(base64.b64decode(data))
                    success += 1
                else:
                    logging.warning("Download failed: %s" % r.text)
                    progress.config(text="%s%s (%d/%d) 下載失敗。" % (
                        save_path, filename, i, n))

            progress.config(text="%d張圖片下載完成。" % success)
        except Exception as e:
            logging.exception(e)
            progress.config(text="錯誤發生。下載失敗。")

    def download(num):
        global my_config
        save()
        process(num, my_config)

    def input_clear(textblock):
        textblock.delete(1.0, tk.END)

    def open_folder():
        os.startfile(os.path.realpath(global_save_path))

    def check_num(var, lower, upper):
        try:
            a = int(var.get())
        except Exception as e:
            logging.exception(e)
            var.set('11')
        if a < lower:
            var.set(str(lower))
        elif a > upper:
            var.set(str(upper))
        return True

    global key
    with open('settings.json') as f:
        config = json.load(f)
    with open('key.json') as f:
        key = json.load(f)['key']
    window = tk.Tk()
    window.title('NovelAI Image Piliang Spawner')

    frames = [tk.Frame(window) for i in range(4)]
    for fi in frames:
        fi.pack(anchor="w", padx=5, pady=1)

    tk.Label(frames[0], text="關鍵字", width=10).grid(column=0, row=0)
    input_entry = tk.Text(frames[0], width=64, height=4, font=('Arial'))
    input_entry.insert(1.0, config['input'])
    input_entry.grid(column=1, row=0, sticky='ew')
    tk.Button(frames[0], text="清除",
              command=lambda: input_clear(input_entry)).grid(column=2, row=0)

    tk.Label(frames[0], text="黑名單", width=10).grid(column=0, row=1)
    uc_entry = tk.Text(frames[0], width=64, height=2, font=('Arial', 10))
    uc_entry.insert(1.0, config['uc'])
    uc_entry.grid(column=1, row=1, sticky='ew')
    tk.Button(frames[0], text="清除",
              command=lambda: input_clear(uc_entry)).grid(column=2, row=1)

    tk.Label(frames[2], text="數量", width=10).grid(column=0, row=0)
    num_var = tk.StringVar(frames[2], config['number'])
    num_entry = tk.Entry(frames[2], textvariable=num_var, width=25)
    num_entry.bind("<FocusOut>", lambda x: check_num(num_var, 1, 1000))
    num_entry.grid(column=1, row=0)

    tk.Label(frames[2], text="解析度", width=10).grid(column=0, row=1)
    resol_var = tk.StringVar(frames[2])
    resol_var.set(config['resolution'])
    resol_entry = tk.OptionMenu(frames[2], resol_var, *resolutions)
    resol_entry.configure(width=25)
    resol_entry.grid(column=1, row=1)

    tk.Label(frames[2], text="模型", width=10).grid(column=2, row=1)
    model_var = tk.StringVar(frames[2])
    model_var.set(config['model'])
    model_entry = tk.OptionMenu(frames[2], model_var, *list(models.keys()))
    model_entry.configure(width=25)
    model_entry.grid(column=3, row=1)

    tk.Label(frames[2], text="Steps", width=10).grid(column=0, row=2)
    steps_var = tk.StringVar(frames[2], config['steps'])
    steps_entry = tk.Entry(frames[2], textvariable=steps_var, width=25)
    steps_entry.bind("<FocusOut>", lambda x: check_num(steps_var, 2, 28))
    steps_entry.grid(column=1, row=2)

    tk.Label(frames[2], text="Scale", width=10).grid(column=2, row=2)
    scale_var = tk.StringVar(frames[2], config['scale'])
    scale_entry = tk.Entry(frames[2], textvariable=scale_var, width=25)
    scale_entry.bind("<FocusOut>", lambda x: check_num(scale_var, 2, 100))
    scale_entry.grid(column=3, row=2)

    tk.Label(frames[2], text="進階：取樣", width=10).grid(column=0, row=3)
    sampler_var = tk.StringVar(frames[2])
    sampler_var.set(config['sampler'])
    sampler_entry = tk.OptionMenu(frames[2], sampler_var, *samplers)
    sampler_entry.configure(width=25)
    sampler_entry.grid(column=1, row=3)

    tk.Label(frames[2], text="認證金鑰", width=10).grid(column=2, row=3)
    key_entry = tk.Entry(frames[2], width=25)
    key_entry.insert(0, key)
    key_entry.grid(column=3, row=3)

    tk.Button(frames[3], text="儲存設定", width=10,
              command=save).pack(side=tk.LEFT)
    tk.Button(frames[3], text="產生圖片", width=10,
              command=lambda: threading.Thread(target=lambda: download(
                  int(num_entry.get()))).start()).pack(side=tk.LEFT)
    tk.Button(frames[3], text="開啟圖片", width=10,
              command=open_folder).pack(side=tk.LEFT)
    progress = tk.Label(frames[3], text='', width=60, anchor='w')
    progress.pack(side=tk.LEFT)

    window.eval('tk::PlaceWindow . center')
    window.mainloop()


if __name__ == "__main__":
    try:
        if not os.path.exists('key.json'):
            with open('key.json', 'w', encoding='UTF-8') as f:
                json.dump({"key": key}, f, indent=4)
        if not os.path.exists('settings.json'):
            with open('settings.json', 'w', encoding='UTF-8') as f:
                json.dump(my_config, f, indent=4)
        if not os.path.isdir('download'):
            os.mkdir('download')

        # log setup
        logging.basicConfig(filename='nips.log', level=logging.DEBUG,
                            encoding="utf-8",
                            format="%(asctime)s;\t%(levelname)s;\t%(message)s",
                            datefmt="%Y-%m-%d %H:%M:%S")
        logging.info("Launch app.")

    except Exception as e:
        logging.exception(e)

    gui()

    logging.info("Leave app.")
