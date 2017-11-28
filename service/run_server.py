from core import app, config

if __name__ == '__main__':
    app.run(threaded=True, debug=True, host=config.get("Default", "CORE_TCP_IP"),
            use_reloader=False, port=int(config.get("Default", "CORE_TCP_PORT")))
