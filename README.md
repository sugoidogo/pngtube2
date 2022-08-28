# PNGTube
OBS Browser Source for creating an image based avatar that animates to audio input. Useful for PNG-tubing or as a TTS avatar.
## Usage
0. Check your OBS version by reading the title bar while it's open
    - If it's under 27 (26 or lower), you need to update OBS before using this overlay
    - If it's 27, install the [OBS Websocket Plugin](https://github.com/obsproject/obs-websocket/releases)
    - If it's over 27 (28 or higher), you can skip this step
1. Add a browser source with the url https://sugoidogo.github.io/pngtube2/v4/overlay.html
    - **The overlay will be empty when you first add it. This is normal.**
2. Add a custom browser dock (Docks > Custom Browser Docks) with the url https://sugoidogo.github.io/pngtube2/v4/dock.html
    - to run multiple instances, add `?id=somename` to both the dock and overlay url.
        - replace `somename` with something identifiable
        - the dock and overlay must have the same id to be able to change settings
3. Add your images and any password that is set in the websocket settings (Tools > OBS-Websocket Settings)
4. **Add a Noise Gate Filter to your microphone.** The audio levels reported by obs-websocket are in a format I don't understand. You are welcome to open an issue if you can detail how to convert the values into decibles, like those shown on OBS's audio mixer. For now, you should adjust some settings on the noise gate:
    1. Close Threshold: How quiet your mic must be before it's cut off.
    2. Open Threshold: How loud your mic must be before it's audible again.
        - This value is in decibles (-60 is quieter than -30).
        - Use the audio meter in OBS to gauge where these should be set, the numbers along the meter are in decibels.
    3. Release Time: How long the mic must be below the Close Threshold before it's cut off.
        - This value is in milliseconds (1000 milliseconds = 1 second).
5. You're Done! You can close the dock now and open it again later to change settings under the Dock menu in OBS.
## Support
[Get support on Discord](https://discord.gg/zxDnYSvMNw)

[Give support on Patreon](https://www.patreon.com/SugoiDogo)