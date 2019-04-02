#!/usr/bin/env python

import os, time, pychromecast, spotipy, spotipy.util as util, spotify_token as st
from http.server import BaseHTTPRequestHandler, HTTPServer
from bottle import route, request
from pychromecast.controllers.spotify import SpotifyController
from spotipy import oauth2
from random import randint

def spotireveil():
    CAST_NAME = "ChambreAudio"

    chromecasts = pychromecast.get_chromecasts()
    cast = None
    for _cast in chromecasts:
        if _cast.name == CAST_NAME:
            cast = _cast
            break

    if cast:
        cast.wait()
        cast.set_volume(0.1)
        device_id = None

        data = st.start_session("111644649", "g0ksPbWr1n0aPo")
        access_token = data[0]

        client = spotipy.Spotify(auth=access_token)

        sp = SpotifyController(access_token)
        cast.register_handler(sp)
        sp.launch_app()

        devices_available = client.devices()

        for device in devices_available['devices']:
            if device['name'] == CAST_NAME:
                device_id = device['id']
                break

        client.shuffle(True,device_id=device_id)
        client.start_playback(device_id=device_id,context_uri="spotify:user:spotify:playlist:37i9dQZF1DX0UrRvztWcAU")
        #,offset={"position":randint(0, 20)}
        #client.volume(30,device_id=device_id)
        start_vol = 0.1
        while start_vol <= 0.3:
            time.sleep(30)
            start_vol = start_vol+0.015
            cast.set_volume(start_vol)

# HTTPRequestHandler class
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):

  # GET
  def do_GET(self):
        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type','text/html')
        self.end_headers()

        # Send message back to client
        message = "Hello world!"
        # os.system("python test-cc.py")
        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))


        spotireveil()
        return

def run():
  print('starting server...')

  # Server settings
  # Choose port 8080, for port 80, which is normally used for a http server, you need root access
  server_address = ('127.0.0.1', 8081)
  httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
  print('running server...')
  httpd.serve_forever()


run()