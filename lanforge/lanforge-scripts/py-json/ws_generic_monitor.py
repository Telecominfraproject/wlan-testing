"""
pip install websocket_client

https://pypi.org/project/websocket_client/

WS_Listener has three arguments in general : lfclient_host, _scriptname, _callback
1.  Enter the LF Client Host address on which you want to monitor events (by Default is localhost)
2.  Enter the _scriptname that should be present in the event triggered by your script,
    refer add_event() in lfcli_base.add_event()
    _scriptname can be any string that you want to monitor in your websocket message
3.  Enter the Callback function that you wanna see your messages in everytime your event will trigger up.
    refer py-scripts/ws_generic_monitor_test.py to see an example

"""

class WS_Listener():
    def __init__(self, lfclient_host="localhost", _scriptname=None, _callback=None):
        import websocket
        self.scriptname = _scriptname
        websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp("ws://"+lfclient_host+":8081", on_message=_callback)
        self.ws.run_forever()



