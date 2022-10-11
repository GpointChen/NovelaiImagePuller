# NovelAI Image Puller (NIP)
A tool to batch download the images produced by NovelAI by its API.

Before start downloading, you may need to fill in the key in `key.json` like below:

```json
{
    "key": "Put your key here"
}
```

The key starts with "Bearer". You can get it on the browser by something like Chrome Dev Tool.

All your settings will be saved automatically when you start requesting images, and your images will be downloaded into `download\` folder.

You can check the log in `nips.log`.
