this.runDiagnostics = function(a) {
        e.info("runDiagnostics call arrived with data", a);
        if (a.isAppletBased) return w(a);
        l.init(!a.isAppletBased, !1);
        return v(a)
    };

    function v(a) {
        var d = b.defer();
        h.initWebSocket(a).then(function() {
            e.info("Success in diagnostics WebSocket init");
            k.init(a.authToken, a.checkAudio, a.callbackUrlForMessage);
            z(a.disableMediaPermissionTimeOut).then(function() {
                e.info("Success in runWebSocketDiagnostics");
                H(a.isCheckWebRTC).then(function(b) {
                    e.info("Success in runWebRTCDiagnostics", b);
                    I(a.isCheckWebRTC, a.checkAudio).then(d.resolve, d.reject, d.notify)
                }, function(a) {
                    e.log("Error occurred while runWebRTCDiagnostics", a);
                    d.reject(a)
                }, function(a) {
                    d.notify(a)
                })
            }, function(a) {
                e.log("Error occurred while runWebSocketDiagnostics", a);
                d.reject(B(a))
            })
        }, function(a) {
            e.log("Error occurred while diagnosticsFactory WebSocket init", a);
            d.reject(B(a))
        });
        return d.promise
    }

    function z(a) {
        var d = b.defer(),
            c = h.getWebsocketDiagnosticsOpts() || {};
        a ? g.startCommunication({
            webSocketServerUrl: c.webSocketServerUrl,
            webSocketAuthUrl: c.webSocketAuthUrl,
            authToken: c.authToken,
            callbackUrlForOpen: function(a) {
                e.info("web-socket connection established");
                c.autoClose && (e.log("TODO: temporary commenting below code. FIX IT. Closing Websocket as property autoClose was true in Diagnostics"),
                    g.stopCommunication());
                d.resolve()
            },
            callbackUrlForClose: function(a) {
                e.error("web-socket connection got exception", a);
                d.reject(a)
            },
            callbackUrlForMessage: c.callbackUrlForMessage
        }, !0) : d.resolve();
        return d.promise
    }

     function H() {
        var a = b.defer(),
            d = h.getRTC(),
            c = h.getWebrtcDiagnosticsOpts();
        d.isWebRTCSupported ? c.checkScreens ? (e.info("Running screen diagnostics", c), d = h.getScreenPluginId(), q.runDiagnostics(d).then(function(b) {
            e.info("Success of screens diagnostics", b);
            a.notify(b);
            A(c, a)
        }, a.reject, a.notify)) : A(c, a) : a.reject(B(C.WEB_RTC_NOT_SUPPORTED));
        return a.promise
    }
