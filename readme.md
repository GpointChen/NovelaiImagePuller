# NovelAI Image Puller (NIP)
A tool to batch download the images produced by NovelAI by its API.

Before start downloading, you may need to fill in the key in `config\key.json` like below:

```json
{
    "key": "Put your key here"
}
```

The key starts with "Bearer". You can get it on the browser by something like Chrome Dev Tool.

All your settings will be saved automatically when you start requesting images, and your images will be downloaded into `download\` folder.

If you mess up your settings, you can delete `settings.json` and it will be re-generated when launch the app.

You can check the log in `nips.log`.

* For older version before 0.2, all json files are stored in the same folder as the exe file.
