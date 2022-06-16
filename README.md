# PNGTube
Become a PNGTuber without using discord
## Usage
0. Check your OBS version by reading the title bar while it's open
    - If it's under 27 (26 or lower), you need to update OBS before using this overlay
    - If it's 27, install the [Websocket Plugin Beta](https://github.com/obsproject/obs-websocket/releases)
    - If it's over 27 (28 or higher), you can skip this step
1. Add a browser source with the url https://sugoidogo.github.io/pngtube2/v4/overlay.html
    - **The overlay will be empty when you first add it. This is normal.**
2. Add a custom browser dock (Docks > Custom Browser Docks) with the url https://sugoidogo.github.io/pngtube2/v4/dock.html
    - to run multiple instances, add `?id=somename` to both the dock and overlay url.
        - replace `somename` with something identifiable
        - the dock and overlay must have the same id to be able to change settings
3. Add your images and any password that is set in the websocket settings (Tools > OBS-Websocket Settings)
4. **Add a Noise Gate Filter to the source you plan to use.** The audio levels reported by obs are in a format I don't understand. You are welcome to open an issue if you can detail how to convert the values into decibles, like shown on OBS's audio mixer. For now, you should adjust some settings on the noise gate:
    1. Close Threshold: How quiet your audio source must be before it's cut off.
    2. Open Threshold: How loud your audio source must be before it's audible again.
        - If you don't understand what these numbers mean, look at the audio mixer in obs. It has numbers along the meter to show you where your audio levels are at.
    3. Release Time: How long the audio level has to stay under the Close Threshold to get cut off.
        - This value is in milliseconds. 1000 milliseconds equals 1 second. Keep in mind that this determines how long it takes for audio to cut off.
5. You're Done! You can close the dock now and open it again later to change settings under the Dock menu in OBS.
## Support
[Get support on Discord](https://discord.gg/zxDnYSvMNw)

[Give support on Patreon](https://www.patreon.com/SugoiDogo)