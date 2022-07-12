## Render Xvfb output to WS2812B LEDs via shared framebuffer

### Disclaimer
I do not provide any warranty for this small project, everything is provided as is.
It is meant to run on a Raspberry PI and I will only provide a setup guide for it specifically.

### Get started
To begin on Raspberry PI just run the install.sh script with
`sudo bash ./install.sh`
Or look into the install script to see the required packages.

You will need to setup program in the display_engine.py file. 
Put in the configuration for the LEDs there and if you are working with 8x8 matrices you can set the layout in the matrix_config.py file.

### Running the script
You will need about 3 shh sessions to get going. Run the following 3 commands in seperate sessions.
- The Virtual display in the desired resolution, specified as WIDTHxHEIGHTxDEPTH where depth must be 24bit. It will need a folder to put the shared framebuffer file into.
    `Xvfb :0 -screen 0 24x16x24 -fbdir ./frameBuffer`
- The display engine itself. It will read the framebuffer and write the output to the LED Matrices.
    `sudo python3 ./display_engine`
- An application to test is also included.
    `DISPLAY=:0 python3 draw_cube.py`
- For debug purposes you can export a screenshot of the virtual screen. It just sometimes cannot handle the bit depth.
    `xwd -display :0 -root | xwdtopnm | pnmtopng > Screenshot.png`