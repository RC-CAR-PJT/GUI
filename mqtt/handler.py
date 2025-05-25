def setup_mqtt_callbacks(manager, ui):
    def on_connect(client, userdata, flags, rc, properties=None):
        if client == manager.command_client:
            ui.command_tab.set_connection_status("연결됨" if rc == 0 else f"연결 실패 ({rc})")
        else:
            ui.sensing_tab.append_log(f"MQTT 상태: {'연결됨' if rc == 0 else f'실패 ({rc})'}")

    def on_message(client, userdata, msg):
        ui.sensing_tab.handle_message(msg)

    manager.command_client.on_connect = on_connect
    manager.command_client.on_disconnect = lambda c, u, rc, p=None: ui.command_tab.set_connection_status("끊어짐")
    manager.sensing_client.on_connect = on_connect
    manager.sensing_client.on_message = on_message
