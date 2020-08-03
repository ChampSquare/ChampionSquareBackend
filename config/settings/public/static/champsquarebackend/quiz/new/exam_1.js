(function(b, c) {
    function e(b, e) {
        this.$get = ["proctoringService", function(b) {
            return b
        }]
    }
    var f = [];
    "object" == typeof webRTC && f.push("webRTC");
    f = c.module("mettlProctor", f);
    f.provider("$proctor", e);
    e.$inject = ["$provide", "$compileProvider"];
    f.service("proctoringService", ["$window", "$rootScope", "$q", "LoggerService", "DiagnosticsService", "appletService", "ProviderFactory", "ProctoringLiteService", function(b, e, c, a, d, f, q, m) {
        function u() {
            var a = l().getClientId(),
                b = [99254, 70231];
            return -1 != [36122, 11497, 101234].indexOf(a) ?
                3E4 : -1 != b.indexOf(a) ? 3E3 : 6E4
        }

        function l() {
            return q.get()
        }
        this.startViewerStreaming = function(a, b) {
            m.startViewerStream(a, b)
        };
        this.stopViewerStreaming = function() {
            m.stopViewerStreaming()
        };
        this.captureStreamImage = function() {
            return m.captureStreamImage()
        };
        this.getICE = function() {
            return m.getICE()
        };
        this.runDiagnostics = function(a) {
            return d.runDiagnostics(a)
        };
        this.showStream = function(a) {
            l().showStream(a)
        };
        this.hideStream = function(a) {
            l().hideStream(a)
        };
        this.startSelfStreaming = function(a) {
            l().startSelfStreaming(a)
        };
        this.captureWebcamImage = function() {
            l().captureWebcamImage()
        };
        this.takeFaceSnap = function() {
            l().takeFaceSnap()
        };
        this.takeIdSnap = function() {
            l().takeIdSnap()
        };
        this.startCommunication = function(a) {
            return l().startCommunication(a)
        };
        this.updateAuthToken = function(a) {
            l().updateAuthToken(a)
        };
        this.sendMessage = function(a) {
            l().sendMessage(a)
        };
        this.sendAck = function(a) {
            l().sendAck(a)
        };
        this.sendStartTestMessage = function(a, b) {
            var e = u();
            l().sendStartTestMessage(a, b, e)
        };
        this.startCandidateProctoring = function(a, b) {
            var e =
                u();
            l().startCandidateProctoring(a, b, e)
        };
        this.updateProctoringParameters = function(b) {
            a.log("Updating Proctoring parameters");
            l().updateProctoringParameters(b)
        };
        this.speedupScreenCapture = function(a) {
            l().speedupScreenCapture(a)
        };
        this.normalizeRegularScreenCaptureSpeed = function(a) {
            l().normalizeRegularScreenCaptureSpeed(a)
        };
        this.shutdownProctoring = function() {
            l().shutdownProctoring()
        };
        this.shutdown = function() {
            l().shutdown()
        };
        this.getWebRTCPreferences = function() {
            l().getWebRTCPreferences()
        };
        this.startPresenterStream =
            function(a) {
                l().startPresenterStream(a)
            };
        this.finishTest = function(a) {
            l().finishTest(a)
        };
        this.reconnect = function(a) {
            l().reconnect(a)
        };
        this.reconnectAuthRequest = function(a) {
            l().reconnectAuthRequest(a)
        };
        this.stopPresenterStreaming = function() {
            l().stopPresenterStreaming()
        };
        this.startVideoStreamByIndex = function(a, b, e) {
            l().startVideoStreamByIndex(a, b, e)
        };
        this.sendWebCamChanged = function(a) {
            l().sendWebCamChanged(a)
        };
        this.sendFinalWebCamSelected = function(a) {
            l().sendFinalWebCamSelected(a)
        };
        this.resumeDiagnosticsAfterCameraSelection =
            function() {
                return d.resumeDiagnosticsAfterCameraSelection()
            };
        this.checkAppletSettingAndResumeDiagnosticsAfterCameraSelection = function() {
            return d.checkAppletSettingAndResumeDiagnosticsAfterCameraSelection()
        };
        this.setMaxRetries = function(a) {
            l().setMaxRetries(a)
        };
        this.recheckSystemSoftware = function() {
            d.recheckSystemSoftware()
        };
        this.captureScreen = function() {
            return l().captureScreen()
        };
        this.installBrowserPlugin = function(a) {
            return l().installBrowserPlugin(a)
        };
        this.updateBrowserPlugin = function(a) {
            return l().updateBrowserPlugin(a)
        };
        this.startWebRTCAndSetVideoElem = function(a, b, e) {
            l().startWebRTCAndSetVideoElem(a, b, e)
        };
        this.init = function(a, b) {
            q.init(a, b)
        }
    }])
})(window, window.angular);
var proctoringProvider = function() {
        return {
            loadFiles: function(b) {
                "function" == typeof b && b()
            }
        }
    }(),
    mettlProctor = angular.module("mettlProctor");
mettlProctor.constant("SocketMessageConstants", {
    StreamingMessageType: {
        MESSAGE: "MESSAGE",
        INFO: "INFO",
        ONLINE: "ONLINE",
        OFFLINE: "OFFLINE",
        IMAGE: "IMAGE",
        SCREEN_IMAGE: "SCREEN_IMAGE",
        ANNOUNCEMENT: "ANNOUNCEMENT",
        END_TEST: "END_TEST",
        APPLET_DESTROYED: "APPLET_DESTROYED",
        SELF_OFFLINE: "SELF_OFFLINE",
        SELF_ONLINE: "SELF_ONLINE",
        CONNECTION_SUCCESS: "CONNECTION_SUCCESS",
        GET_MSG: "GET_MSG",
        DUPLICATE_USER: "DUPLICATE_USER",
        ONLINE_USERS: "ONLINE_USERS",
        GET_TESTTIME_LEFT: "GET_TESTTIME_LEFT",
        PAUSE_TEST: "PAUSE_TEST",
        PAUSE_ACK: "PAUSE_ACK",
        RESUME_TEST: "RESUME_TEST",
        RESUME_ACK: "RESUME_ACK",
        SUSPICIOUS_SOFTWARE: "SUSPICIOUS_SOFTWARE",
        DIAGNOSTICS_SUCCESS: "DIAGNOSTICS_SUCCESS",
        CHAT_SERVER_ERROR: "CHAT_SERVER_ERROR",
        CAMERA_UNAVAILABLE: "CAMERA_UNAVAILABLE",
        LOAD_SUCCESS: "LOAD_SUCCESS",
        EXPIRE_TEST: "EXPIRE_TEST",
        CHECK_CHROME_PLUGIN: "CHECK_CHROME_PLUGIN",
        STREAMING_FOR_IMAGE_READY: "STREAMING_FOR_IMAGE_READY",
        SHOW_FACE_IMAGE: "SHOW_FACE_IMAGE",
        SHOW_ID_IMAGE: "SHOW_ID_IMAGE",
        REGISTRATION_FIELD_ACK: "REGISTRATION_FIELD_ACK",
        PENDING_AUTHORIZATION_COUNT: "PENDING_AUTHORIZATION_COUNT",
        CANDIDATE_AUTH_PROCESSED: "CANDIDATE_AUTH_PROCESSED",
        APPLET_CRASHED: "APPLET_CRASHED",
        AVAILABLE_CAMERAS: "AVAILABLE_CAMERAS",
        SELECT_CAM: "SELECT_CAM",
        CAM_FINAL: "CAM_FINAL",
        NEW_CAMERA_SELECTED: "NEW_CAMERA_SELECTED",
        CAMERA_UNAVAILABLE_WHILE_STREAMING_IN_DIAGNOSTICS: "CAMERA_UNAVAILABLE_WHILE_STREAMING_IN_DIAGNOSTICS",
        RECONNECT_FAILED: "RECONNECT_FAILED",
        SDP_OFFER_CANDIDATE: "SDP_OFFER_CANDIDATE",
        SDP_ANSWER_CANDIDATE: "SDP_ANSWER_CANDIDATE",
        ICE_CANDIDATE: "ICE_CANDIDATE",
        STOP_STREAMING: "STOP_STREAMING",
        JOIN_ROOM: "JOIN_ROOM",
        SEND_SDP: "SEND_SDP",
        SDP_OFFER: "SDP_OFFER",
        PING: "PING",
        PONG: "PONG",
        WebRTC_RECORDING_URL: "WebRTC_RECORDING_URL",
        GET_WEBRTC_SNAP: "GET_WEBRTC_SNAP",
        MEDIASERVER_DOWN: "MEDIASERVER_DOWN",
        GET_WEBRTC_WEBCAM_INFO: "GET_WEBRTC_WEBCAM_INFO",
        LOG: "LOG",
        STARTVIDEO: "STARTVIDEO",
        STOPVIDEO: "STOPVIDEO",
        SDP_ANSWER_PROCTOR: "SDP_ANSWER_PROCTOR",
        SDP_OFFER_PROCTOR: "SDP_OFFER_PROCTOR",
        MEDIASERVER_DOWN: "MEDIASERVER_DOWN",
        WEBRTC_CANDIDATE_NOT_ACTIVE: "WEBRTC_CANDIDATE_NOT_ACTIVE",
        ICE_CANDIDATE: "ICE_CANDIDATE",
        SDP_ANSWER: "SDP_ANSWER",
        STREAMING_HANDSHAKE_SUCCESS: "STREAMING_HANDSHAKE_SUCCESS",
        STREAMING_HANDSHAKE_FAILURE: "STREAMING_HANDSHAKE_FAILURE"
    },
    Events: {
        DIAGNOSTICS_ERROR: "DIAGNOSTICS_ERROR",
        APPLET_ADDED: "APPLET_ADDED",
        SERVER_CHECK_PASS: "SERVER_CHECK_PASS",
        APPLET_TIMED_OUT: "APPLET_TIMED_OUT",
        RECHECK_CHROME_SUCCESS: "RECHECK_CHROME_SUCCESS",
        WAITING_FOR_WEBRTC_PERMISSION: "waitingForWebRTCPermission",
        PENDING_WEBRTC_PERMISSION: "pendingWebRTCPermissions",
        WEBRTC_PERMISSION_GRANTED: "webRTCPermissionGranted",
        WEBRTC_DIAGNOSTICS_COMPLETED: "WEBRTC_DIAGNOSTICS_COMPLETED",
        CANDIDATE_BLUR_IN: "CANDIDATE_BLUR_IN",
        CANDIDATE_BLUR_OUT: "CANDIDATE_BLUR_OUT",
        STREAMING_CONNECTION_FAILURE: "STREAMING_CONNECTION_FAILURE"
    },
    Screen: {
        DIAGNOSTICS_SUCCESS: "screenDiagnosticsSuccess",
        EXTENSION_INSTALLED: "screenExtensionInstalled",
        EXTENSION_STARTED: "screenExtensionStarted",
        EXTENSION_SUSPENDED: "screenExtensionSuspended",
        STREAMING_CONNECTION_FAILURE: "STREAMING_CONNECTION_FAILURE",
        WEBRTC_ICE_FAILED: "WEBRTC_ICE_FAILED"
    },
    MessageChunkType: {
        None: 0,
        Start: 1,
        Data: 2,
        End: 3
    },
    StreamingUserTye: {
        Presenter: "Presenter",
        Viewer: "Viewer"
    }
});
mettlProctor = angular.module("mettlProctor");
mettlProctor.constant("ErrorConstants", {
    WebSocket: {
        MISSING_OPTS_SERVER_URL: "serverUrlMissing",
        MISSING_OPTS_AUTH_URL: "authorizationUrlMissing",
        EXCEPTION_IN_WEB_SOCKET_INIT: "webSocketInItException",
        MISSING_OPTS_CALLBACK_URL: "missingMessageCallBackUrlFromClient",
        NOT_A_VALID_CALLBACK_URL: "missingMessageCallBackUrlFromServer",
        WEB_SOCKET_NOT_SUPPORTED: "browserNotSupportedForWebRTC",
        INVALID_PARAMETERS: "invalidParameters",
        DIAGNOSTICS_ERROR: "diagnosticsError",
        ERROR_IN_AUTHENTICATION: "errorInAuthentication",
        PING_DELAYED: "pingDelayed",
        CHAT_SERVER: "chatServerError",
        SOCKET_BROKEN: "socketBroken",
        SOCKET_SERVER_ERROR: "streamingConnectionFailed",
        DUPLICATE_USER: "duplicateUser"
    },
    WebRTC: {
        WEB_RTC_NOT_SUPPORTED: "browserNotSupportedForWebRTC",
        TURN_SERVER_ERROR: "turnServerConnectionFailed",
        MEDIA_DEVICE_ERROR: "mediaDeviceError",
        PERMISSION_NOT_GRANTED: "webrtcPermissionNotGranted",
        PERMISSION_NOT_GRANTED_TO_A_DEVICE: "webrtcPermissionNotGrantedToADevice",
        MULTIPLE_WEBCAM: "multipleWebCam",
        WEBCAM_NOT_FOUND: "webCamError",
        AUDIO_PERMISSION_NOT_GRANTED: "audioPermissionNotGranted",
        MICROPHONE_NOT_FOUND: "microphoneError",
        MICROPHONE_MUTED: "MICROPHONE_MUTED"
    },
    ScreenUtil: {
        SCREEN_FEED_UNAVAILABLE: "SCREEN_FEED_UNAVAILABLE",
        SCREEN_PLUGIN_NOT_INSTALLED: "screenPluginNotInstalled",
        SCREEN_PLUGIN_DISABLED: "screenPluginDisabled",
        SCREEN_PLUGIN_NOT_UPDATED: "screenPluginNotUpdated",
        SCREEN_FEED_STOPPED: "screenFeedStopped",
        SCREEN_FEED_INACTIVE: "screenFeedInActive",
        SCREEN_PERMISSION_DENIED: "screenPermissionDenied",
        SCREEN_GIVE_PERMISSION: "screenPermission",
        SCREEN_MULTIPLE_DETECTED: "screenMultipleDetected",
        SCREEN_PERMISSION_USER_DENIED: "SCREEN_PERMISSION_USER_DENIED",
        SCREEN_PERMISSION_SYSTEM_DENIED: "SCREEN_PERMISSION_SYSTEM_DENIED"
    },
    StreamingMessageType: {
        MESSAGE: "MESSAGE",
        INFO: "INFO",
        ONLINE: "ONLINE",
        OFFLINE: "OFFLINE",
        IMAGE: "IMAGE",
        ANNOUNCEMENT: "ANNOUNCEMENT",
        END_TEST: "END_TEST",
        APPLET_DESTROYED: "APPLET_DESTROYED",
        SELF_OFFLINE: "SELF_OFFLINE",
        SELF_ONLINE: "SELF_ONLINE",
        GET_MSG: "GET_MSG",
        DUPLICATE_USER: "DUPLICATE_USER",
        ONLINE_USERS: "ONLINE_USERS",
        GET_TESTTIME_LEFT: "GET_TESTTIME_LEFT",
        PAUSE_TEST: "PAUSE_TEST",
        PAUSE_ACK: "PAUSE_ACK",
        RESUME_TEST: "RESUME_TEST",
        RESUME_ACK: "RESUME_ACK",
        SUSPICIOUS_SOFTWARE: "SUSPICIOUS_SOFTWARE",
        DIAGNOSTICS_SUCCESS: "DIAGNOSTICS_SUCCESS",
        CHAT_SERVER_ERROR: "CHAT_SERVER_ERROR",
        CAMERA_UNAVAILABLE: "CAMERA_UNAVAILABLE",
        LOAD_SUCCESS: "LOAD_SUCCESS",
        EXPIRE_TEST: "EXPIRE_TEST",
        CHECK_CHROME_PLUGIN: "CHECK_CHROME_PLUGIN",
        STREAMING_FOR_IMAGE_READY: "STREAMING_FOR_IMAGE_READY",
        SHOW_FACE_IMAGE: "SHOW_FACE_IMAGE",
        SHOW_ID_IMAGE: "SHOW_ID_IMAGE",
        REGISTRATION_FIELD_ACK: "REGISTRATION_FIELD_ACK",
        PENDING_AUTHORIZATION_COUNT: "PENDING_AUTHORIZATION_COUNT",
        CANDIDATE_AUTH_PROCESSED: "CANDIDATE_AUTH_PROCESSED",
        APPLET_CRASHED: "APPLET_CRASHED",
        AVAILABLE_CAMERAS: "AVAILABLE_CAMERAS",
        SELECT_CAM: "SELECT_CAM",
        CAM_FINAL: "CAM_FINAL",
        NEW_CAMERA_SELECTED: "NEW_CAMERA_SELECTED",
        CAMERA_UNAVAILABLE_WHILE_STREAMING_IN_DIAGNOSTICS: "CAMERA_UNAVAILABLE_WHILE_STREAMING_IN_DIAGNOSTICS",
        RECONNECT_FAILED: "RECONNECT_FAILED",
        SDP_OFFER_CANDIDATE: "SDP_OFFER_CANDIDATE",
        SDP_ANSWER_CANDIDATE: "SDP_ANSWER_CANDIDATE",
        ICE_CANDIDATE: "ICE_CANDIDATE",
        STOP_STREAM: "STOP_STREAM",
        PING: "PING",
        PONG: "PONG",
        RECORDING_URL: "RECORDING_URL",
        WebRTC_RECORDING_URL: "WebRTC_RECORDING_URL",
        GET_WEBRTC_SNAP: "GET_WEBRTC_SNAP",
        MEDIASERVER_DOWN: "MEDIASERVER_DOWN",
        GET_WEBRTC_WEBCAM_INFO: "GET_WEBRTC_WEBCAM_INFO",
        LOG: "LOG",
        STARTVIDEO: "STARTVIDEO",
        STOPVIDEO: "STOPVIDEO"
    }
});
mettlProctor = angular.module("mettlProctor");
mettlProctor.constant("AppletConstants", {
    Url: {
        getBlockedSoftwares: "/getBlockedSoftwares"
    },
    WEBRTC_MESSAGES: {
        CONNECTED: "CONNECTED",
        WEBRTC_PREFERENCES: "WEBRTC_PREFERENCES",
        MULITCAM_WARNING: "MULITCAM_WARNING"
    },
    Errors: {
        javaFailure: "javaFailure",
        chromeNotSupported: "chromeNotSupported",
        firefoxNewVersionNotSupported: "firefoxNewVersionNotSupported",
        suspiciousSoftware: "suspiciousSoftware"
    },
    Events: {
        APPLET_TIMED_OUT: "APPLET_TIMED_OUT",
        WEBRTC_DIAGNOSTICS_COMPLETED: "WEBRTC_DIAGNOSTICS_COMPLETED",
        WEBRTC_DIAGNOSTICS_FAILURE: "WEBRTC_DIAGNOSTICS_FAILURE",
        WEBRTC_DIAGNOSTICS_SUCCESS: "WEBRTC_DIAGNOSTICS_SUCCESS",
        WEBRTC_MIXED_MODE: "WEBRTC_MIXED_MODE",
        STREAMING_CONNECTION_FAILURE: "STREAMING_CONNECTION_FAILURE"
    },
    AppletRequestType: {
        SEND_MESSAGE: "SEND_MESSAGE",
        SEND_AUTH_REQUEST: "sendAuthRequest",
        SEND_REF_IMAGE: "sendRefImage",
        START_COMMUNICATION: "START_COMMUNICATION",
        TEST_STARTED: "TEST_STARTED",
        START_STREAMING_FOR_FACE_SNAP: "startStreamingForFaceSnap",
        UPDATE_APPLET_SIZE: "UPDATE_APPLET_SIZE",
        CANDIDATE_NAVIGATE_OUT: "CANDIDATE_NAVIGATE_OUT",
        CANDIDATE_NAVIGATE_IN: "CANDIDATE_NAVIGATE_IN",
        RECONNECT: "RECONNECT",
        SWITCH_TO_APPLET_WEBCAM: "SWITCH_TO_APPLET_WEBCAM",
        SEND_WEBRTC_PREFERENCES: "SEND_WEBRTC_PREFERENCES",
        CAPTURE_SCREEN: "CAPTURE_SCREEN",
        VERIFY_SOFTWARE: "VERIFY_SOFTWARE",
        VERIFY_DEVICES: "VERIFY_DEVICES"
    },
    ChatMessageType: {
        AUTH_REQUEST: "AUTHORIZATION_MESSAGE",
        REF_IMAGE: "REFERENCE_IMAGE",
        TEST_STARTED: "TEST_STARTED",
        CANDIDATE_TEST_FINISHED: "CANDIDATE_TEST_FINISHED",
        WebRTC_RECORDING_URL: "WebRTC_RECORDING_URL",
        RESUME_ACK: "RESUME_ACK",
        PAUSE_ACK: "PAUSE_ACK",
        MESSAGE: "MESSAGE",
        CANDIDATE_EVENT: "CANDIDATE_EVENT"
    },
    Constants: {
        CHECK_APPLET_CRASH_INTERVAL_TIME: 1E4,
        MAX_DELAY_IN_APPLET_INTERACTION: 15E3,
        MAX_RETRIES_FOR_STREAMING: 4,
        AUTO_RECONNECT_TRIAL_TIMEOUT: 1E4,
        WEBSOCKET_RETRIAL_COUNT: 3
    },
    AppletMessageType: {
        MESSAGE: "MESSAGE",
        INFO: "INFO",
        ONLINE: "ONLINE",
        OFFLINE: "OFFLINE",
        IMAGE: "IMAGE",
        ANNOUNCEMENT: "ANNOUNCEMENT",
        END_TEST: "END_TEST",
        APPLET_DESTROYED: "APPLET_DESTROYED",
        SELF_OFFLINE: "SELF_OFFLINE",
        SELF_ONLINE: "SELF_ONLINE",
        CONNECTION_SUCCESS: "CONNECTION_SUCCESS",
        GET_MSG: "GET_MSG",
        DUPLICATE_USER: "DUPLICATE_USER",
        ONLINE_USERS: "ONLINE_USERS",
        GET_TESTTIME_LEFT: "GET_TESTTIME_LEFT",
        PAUSE_TEST: "PAUSE_TEST",
        PAUSE_ACK: "PAUSE_ACK",
        RESUME_TEST: "RESUME_TEST",
        RESUME_ACK: "RESUME_ACK",
        SUSPICIOUS_SOFTWARE: "SUSPICIOUS_SOFTWARE",
        DIAGNOSTICS_SUCCESS: "DIAGNOSTICS_SUCCESS",
        STREAMING_SERVER_ERROR: "STREAMING_SERVER_ERROR",
        CHAT_SERVER_ERROR: "CHAT_SERVER_ERROR",
        CAMERA_UNAVAILABLE: "CAMERA_UNAVAILABLE",
        LOAD_SUCCESS: "LOAD_SUCCESS",
        EXPIRE_TEST: "EXPIRE_TEST",
        CHECK_CHROME_PLUGIN: "CHECK_CHROME_PLUGIN",
        STREAMING_FOR_IMAGE_READY: "STREAMING_FOR_IMAGE_READY",
        SHOW_FACE_IMAGE: "SHOW_FACE_IMAGE",
        SHOW_ID_IMAGE: "SHOW_ID_IMAGE",
        REGISTRATION_FIELD_ACK: "REGISTRATION_FIELD_ACK",
        PENDING_AUTHORIZATION_COUNT: "PENDING_AUTHORIZATION_COUNT",
        CANDIDATE_AUTH_PROCESSED: "CANDIDATE_AUTH_PROCESSED",
        APPLET_CRASHED: "APPLET_CRASHED",
        AVAILABLE_CAMERAS: "AVAILABLE_CAMERAS",
        SELECT_CAM: "SELECT_CAM",
        CAM_FINAL: "CAM_FINAL",
        NEW_CAMERA_SELECTED: "NEW_CAMERA_SELECTED",
        CAMERA_UNAVAILABLE_WHILE_STREAMING_IN_DIAGNOSTICS: "CAMERA_UNAVAILABLE_WHILE_STREAMING_IN_DIAGNOSTICS",
        RECONNECT_FAILED: "RECONNECT_FAILED",
        SDP_OFFER_CANDIDATE: "SDP_OFFER_CANDIDATE",
        SDP_ANSWER_CANDIDATE: "SDP_ANSWER_CANDIDATE",
        ICE_CANDIDATE: "ICE_CANDIDATE",
        STOP_STREAM: "STOP_STREAM",
        PING: "PING",
        PONG: "PONG",
        RECORDING_URL: "RECORDING_URL",
        WebRTC_RECORDING_URL: "WebRTC_RECORDING_URL",
        GET_WEBRTC_SNAP: "GET_WEBRTC_SNAP",
        MEDIASERVER_DOWN: "MEDIASERVER_DOWN",
        GET_WEBRTC_WEBCAM_INFO: "GET_WEBRTC_WEBCAM_INFO",
        LOG: "LOG",
        STARTVIDEO: "STARTVIDEO",
        STOPVIDEO: "STOPVIDEO",
        SHOW_WEBRTC_FOR_MULTIPLE_WEB_CAM: "SHOW_WEBRTC_FOR_MULTIPLE_WEB_CAM",
        SCREEN_IMAGE: "SCREEN_IMAGE",
        SOFTWARE_VERIFICATION_DATA: "SOFTWARE_VERIFICATION_DATA",
        DEVICE_VERIFICATION_DATA: "DEVICE_VERIFICATION_DATA"
    }
});
var proctoringSession, token, publicKey = "mettlPub";

function start() {
    toggleButtons(["stop"], "start");
    proctoringSession.start()
}

function stop() {
    proctoringSession.stop()
}

function launchSuccessCallback(b) {
    toggleButtons(["setMessageListener", "start"], "launch");
    this.proctoringSession = b
}

function launchFailureCallback(b) {
    alert(b.data + "  " + b.type)
}

function launch() {
    MP.launch(token, publicKey, launchSuccessCallback, launchFailureCallback)
}

function init() {
    var b = document.getElementById("uniqueId").value,
        c = document.getElementById("groupName").value;
    $.ajax({
        url: "https://localhost:8444/init/",
        headers: {
            Authorization: "Authorization"
        },
        method: "POST",
        data: JSON.stringify({
            publicKey: publicKey,
            expiryTime: 6E4,
            uniqueId: b,
            userMetadata: {
                userType: 0,
                email: "abcd@gmail.com"
            },
            groupName: c,
            proctoringSettings: {
                screenCapture: !1,
                recording: !1
            }
        }),
        contentType: "application/json",
        error: function() {
            alert("some error occurred while init")
        },
        success: function(b) {
            token =
                b.token;
            toggleButtons(["launch"], "init")
        }
    })
}

function setMessageListener() {
    proctoringSession.setMessageListener(messageListener)
}

function messageListener(b) {
    var c = document.getElementById("messageWrapper");
    c.className = "";
    c.innerHTML += "\n" + JSON.stringify(b, void 0, 2)
}

function sendChat() {
    var b = document.getElementById("chat").value;
    proctoringSession.sendMessage(b);
    var c = document.getElementById("sentMessageWrapper");
    c.className = "";
    c.innerHTML += "\n" + b
}

function toggleButtons(b, c) {
    for (var e = 0; e < b.length; e++) document.getElementById(b[e]).removeAttribute("disabled");
    document.getElementById(c).setAttribute("disabled", "disabled")
}
window.addEventListener("message", handleMessage, !1);
var EventType = Object.freeze({
        KEEP_ALIVE: "keep_alive",
        START: "start",
        STOP: "stop",
        CHAT: "MESSAGE",
        DIAGONISTIC_SUCCESS: "diagonistic_success",
        DIAGONISTIC_FAILED: "diagonistic_failed"
    }),
    TYPE = "type",
    DATA = "data",
    ID = "id",
    launchErrorCallback;

function handleMessage(b) {
    if (b && b.data) {
        var c = b.data;
        console.log("received message " + JSON.stringify(b.data));
        c.type == EventType.DIAGONISTIC_SUCCESS ? (document.getElementById("state").innerHTML = JSON.stringify(c), launchSuccessCallback(proctoringSession)) : c.type == EventType.DIAGONISTIC_FAILED ? launchErrorCallback(c[DATA]) : c.type == EventType.CHAT && "function" == typeof proctoringSession.getMessageListener() && proctoringSession.getMessageListener()(c)
    }
}
proctoringSession = new function() {
    var b, c;
    return {
        getEventListener: function() {
            return b
        },
        getMessageListener: function() {
            return c
        },
        start: function() {
            var b = {};
            b[TYPE] = EventType.START;
            MP.sendPostMessage(b)
        },
        stop: function() {
            message[TYPE] = EventType.STOP
        },
        setEventListener: function(e) {
            b = e
        },
        setMessageListener: function(b) {
            c = b
        },
        sendMessage: function(b) {
            var c = {};
            c[TYPE] = EventType.CHAT;
            c[DATA] = b;
            MP.sendPostMessage(c)
        }
    }
};
var MP = new function() {
        var b;
        return {
            launch: function(c, e, f, h) {
                c = {
                    token: c,
                    publicKey: e
                };
                e = document.createElement("form");
                e.setAttribute("method", "post");
                e.setAttribute("action", "https://localhost:8444/checkSystemCapability");
                e.setAttribute("target", "NewFile");
                for (var g in c)
                    if (c.hasOwnProperty(g)) {
                        var k = document.createElement("input");
                        k.type = "hidden";
                        k.name = g;
                        k.value = c[g];
                        e.appendChild(k)
                    } document.body.appendChild(e);
                b = window.open("https://localhost:8444/checkSystemCapability", "NewFile");
                e.submit();
                document.body.removeChild(e);
                launchSuccessCallback = f;
                launchErrorCallback = h;
                $(b).ready(function() {})
            },
            sendPostMessage: function(c) {
                console.log("sending message " + JSON.stringify(c));
                b.postMessage(c, "https://localhost:8444")
            },
            syncParent: function() {
                console.log("syncParent called of MP")
            }
        }
    },
    mettlProctor = angular.module("mettlProctor");
mettlProctor.service("DiagnosticsService", ["$q", "$timeout", "LoggerService", "WebSocketService", "DiagnosticsFactory", "ConnectionManagerService", "$webRTC", "ErrorConstants", "SocketMessageConstants", "StreamingService", "ScreenUtilService", "AppletDiagnosticsService", "UtilityFactory", "ProviderFactory", "AppletConstants", function(b, c, e, f, h, g, k, a, d, p, q, m, u, l, n) {
    function y() {
        e.log("Checking for turn servers");
        var a = h.getICE(),
            d = b.defer();
        try {
            var c = !1;
            J = new(window.RTCPeerConnection || window.mozRTCPeerConnection ||
                window.webkitRTCPeerConnection)({
                iceServers: a
            });
            setTimeout(function() {
                c || (d.reject(!1), c = !0)
            }, 15E3);
            J.createDataChannel("");
            J.createOffer(function(a) {
                -1 < a.sdp.indexOf("typ relay") && (c = !0, resolve(!0));
                J.setLocalDescription(a, angular.noop, angular.noop)
            }, angular.noop);
            J.onicecandidate = function(a) {
                !c && a && a.candidate && a.candidate.candidate && -1 < a.candidate.candidate.indexOf("typ relay") && (c = !0, d.resolve(!0))
            };
            J.oniceconnectionstatechange = function(a) {
                if (!c)
                    if ("completed" == J.iceConnectionState || "connected" ==
                        J.iceConnectionState) c = !0, d.resolve(!0);
                    else if ("failed" == J.iceConnectionState || "closed" == J.iceConnectionState) c = !0, d.reject(!0)
            }
        } catch (f) {
            d.reject(f)
        }
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

    function A(a, b) {
        var d = h.getWebsocketDiagnosticsOpts().authToken.clientId,
            c = conf.turnServerDiagnosticCheckDisabledClientIds ? conf.turnServerDiagnosticCheckDisabledClientIds.split(",") : [];
        a.checkTurnServerAccess && 0 > c.indexOf(d.toString()) ? y().then(function() {
            e.log("turn server connected properly");
            "undefined" != typeof J && J && J.close();
            a.isCheckWebRTC || (e.log("WebRTC Diagnostics skipped"), b.resolve({}));
            k.startWebRTC(a).then(b.resolve, b.reject, b.notify)
        }, function(d) {
            "undefined" != typeof J && J && J.close();
            F++;
            e.log("turn server connection failed", d);
            e.log("turn server retry count", F);
            3 > F ? A(a, b) : b.reject(B(C.TURN_SERVER_ERROR))
        }) : a.isCheckWebRTC ? k.startWebRTC(a).then(b.resolve, b.reject, b.notify) : (e.log("WebRTC Diagnostics skipped"), b.resolve({}))
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

    function w(a) {
        N = a;
        K = b.defer();
        c(function() {
            a.checkMixedMode ?
                v(a).then(x, t, E) : t("skipping webrtc for client ")
        }, 1);
        return K.promise
    }

    function t() {
        l.init(!1, !1);
        var a = u.makeMessage(n.Events.WEBRTC_MIXED_MODE, !1);
        N.checkAudio ? (a = u.makeMessage(C.PERMISSION_NOT_GRANTED), K.reject(a)) : (K.notify(a), K.notify(n.Events.WEBRTC_DIAGNOSTICS_COMPLETED), D(!1))
    }

    function x() {
        l.init(!1, !0);
        var a = u.makeMessage(n.Events.WEBRTC_MIXED_MODE, !0);
        K.notify(a);
        K.notify(n.Events.WEBRTC_DIAGNOSTICS_COMPLETED);
        D(!0);
        e.log("Switching to WebRTC! Disable webcam in applet")
    }

    function D(a) {
        N.authToken.isRunningWebRTC =
            a;
        m.init(N).then(K.resolve, function(a) {
            K.reject(a)
        }, K.notify)
    }

    function E(b) {
        e.log("Notifying main:", b);
        if (b && b.type == a.WebRTC.MULTIPLE_WEBCAM) {
            var d = u.makeMessage(n.Events.WEBRTC_MIXED_MODE, !0);
            K.notify(d);
            l.init(!1, !0)
        }
        K.notify(b)
    }

    function G(a, b) {
        b ? k.stopWebRTC(a.reject(B(C.MICROPHONE_NOT_FOUND))) : (a.notify(B(d.Events.PENDING_WEBRTC_PERMISSION)), L().then(function(b) {
            a.resolve(b)
        }, function(b) {
            a.reject(b)
        }, a.notify))
    }

    function I(a, d) {
        var c = b.defer();
        a ? M && d && !k.getWebRTCPreferences().hasAudio ? k.stopWebRTC(function() {
                c.reject(B(C.PERMISSION_NOT_GRANTED))
            }) :
            k.checkForWorkingCamera().then(function(a) {
                c.resolve(a)
            }, function(a) {
                e.info("error in checking for camera, asking for permission without audio", a);
                k.stopCheckForWorkingCamera().then(function() {
                    G(c, d)
                }, function(a) {
                    e.log("Error occurred in stopping working camera", a);
                    G(c, d)
                })
            }) : d && !k.getWebRTCPreferences().hasAudio ? k.stopWebRTC(function() {
                c.reject(B(C.PERMISSION_NOT_GRANTED))
            }) : (e.log("Check for camera working skipped"), c.resolve({}));
        return c.promise
    }

    function r(a) {
        var b = h.getWebsocketDiagnosticsOpts().authToken;
        return {
            chatType: n.AppletMessageType.LOG,
            logEvent: a,
            message: "Issue with Audio/Video feeds for : Schedule key is : " + b.scheduleKey + ", candidate-email: " + b.email + ", clientId: " + b.clientId
        }
    }

    function L() {
        var a = b.defer(),
            d = h.getWebrtcDiagnosticsOpts();
        d.preventAudioCheck = !0;
        d.checkAudio = !1;
        k.stopWebRTC();
        k.startWebRTC(d).then(function() {
            k.checkForWorkingCamera().then(function(b) {
                var d = r("TEST_AUDIO_NOT_WORKING");
                h.getWebsocketDiagnosticsOpts().callbackUrlForMessage(d);
                a.resolve(b)
            }, function(b) {
                var d = r("TEST_WEBCAM_NOT_WORKING");
                h.getWebsocketDiagnosticsOpts().callbackUrlForMessage(d);
                e.log("Error occurred in checking working camera", b);
                a.reject(B(C.WEBCAM_NOT_FOUND))
            })
        }, a.reject, a.notify);
        return a.promise
    }
    var C = a.WebRTC,
        B = u.makeMessage,
        M = !1,
        F = 0,
        J, K, N;
    this.recheckSystemSoftware = function() {
        m.recheckSystemSoftware()
    };
    this.runDiagnostics = function(a) {
        e.info("runDiagnostics call arrived with data", a);
        if (a.isAppletBased) return w(a);
        l.init(!a.isAppletBased, !1);
        return v(a)
    };
    this.resumeDiagnosticsAfterCameraSelection = function() {
        M = !0;
        return I(!0, h.getWebrtcDiagnosticsOpts().checkAudio)
    };
    this.checkAppletSettingAndResumeDiagnosticsAfterCameraSelection = function() {
        var a = b.defer();
        I(!1, h.getWebrtcDiagnosticsOpts().checkAudio).then(function() {
            x();
            a.resolve()
        }, function(b) {
            t();
            a.reject()
        });
        return a.promise
    }
}]);
mettlProctor = angular.module("mettlProctor");
mettlProctor.factory("ProviderFactory", ["$log", "$q", "$injector", "ProctoringLiteService", "appletService", function(b, c, e, f, h) {
    var g;
    return {
        get: function() {
            return g
        },
        init: function(b, a) {
            var d = c.defer();
            b ? (g = f, f.init(b, a)) : (a ? (g = f, f.init(b, a)) : g = h, h.init(b, a));
            return d.promise
        }
    }
}]);
mettlProctor = angular.module("mettlProctor");
mettlProctor.service("appletService", ["$q", "LoggerService", "$window", "$timeout", "$rootScope", "DeployJavaService", "AppletConstants", function(b, c, e, f, h, g, k) {
    function a() {
        l && (new Date).getTime() - m > k.Constants.MAX_DELAY_IN_APPLET_INTERACTION && n({
            chatType: k.AppletMessageType.APPLET_CRASHED
        });
        u = f(a, k.Constants.CHECK_APPLET_CRASH_INTERVAL_TIME)
    }

    function d() {
        appletMethodsCallStack.push(["shutdown", []]);
        l = !1;
        clearTimeout(u)
    }
    e.appletMessages = JSON.stringify([]);
    e.appletMethodsCallStack = [];
    var p = k.AppletRequestType,
        q = k.AppletMessageType,
        m = (new Date).getTime(),
        u, l = !1,
        n = angular.noop,
        y;
    this.installApplet = function(a, b, d) {
        n = d || angular.noop;
        g.installApplet(a, b);
        this.hideStream()
    };
    this.sendStartTestMessage = function(a, b, d) {
        c.log("sending start test notification.");
        a = [a.message, b, d];
        console.log(d);
        appletMethodsCallStack.push([p.TEST_STARTED, a])
    };
    this.sendAuthorizationRequest = function(a) {
        c.log("sending authorization request to server");
        appletMethodsCallStack.push([p.SEND_AUTH_REQUEST, [JSON.stringify(a)]])
    };
    this.sendCandidateImageRequest =
        function(a) {
            appletMethodsCallStack.push([p.SEND_REF_IMAGE, [JSON.stringify(a)]])
        };
    this.startCommunication = function(a) {
        y = a.candidate;
        var d = b.defer();
        a = [JSON.stringify(y), a.isAuthorization];
        appletMethodsCallStack.push([p.START_COMMUNICATION, a]);
        f(function() {
            d.resolve()
        }, 1E3);
        return d.promise
    };
    this.shutdown = function() {
        d()
    };
    this.shutdownProctoring = function() {
        d()
    };
    this.finishTest = function(a) {
        appletMethodsCallStack.push([a.chatType, []]);
        l = !1;
        clearTimeout(u)
    };
    this.startSelfStreaming = function() {
        appletMethodsCallStack.push([p.START_STREAMING_FOR_FACE_SNAP,
            []
        ])
    };
    this.takeFaceSnap = function() {
        appletMethodsCallStack.push(["takeFaceSnap", []])
    };
    this.takeIdSnap = function() {
        appletMethodsCallStack.push(["takeIdSnap", []])
    };
    this.sendWebRTCRecordingURL = function(a) {
        appletMethodsCallStack.push(["webRTCRecordingURL", [a]])
    };
    this.recheckSystemSoftware = function() {
        appletMethodsCallStack.push(["recheckSystemSoftware", []])
    };
    this.sendAck = function(a) {
        appletMethodsCallStack.push([a.chatType, [a.to]])
    };
    this.raiseChromePluginError = function() {
        appletMethodsCallStack.push(["chromePluginFound",
            []
        ])
    };
    this.sendWebCamChanged = function(a) {
        appletMethodsCallStack.push([q.SELECT_CAM, [a]])
    };
    this.sendFinalWebCamSelected = function(a) {
        appletMethodsCallStack.push([q.CAM_FINAL, [a]])
    };
    this.showStream = function(a) {
        a = $("#" + a);
        if (0 != a.length) {
            var b = a.offset();
            a.width();
            $("#appletContainer").css({
                position: "absolute",
                top: b.top - 9,
                left: b.left + 1,
                zIndex: 900
            })
        }
    };
    this.hideStream = function() {
        $("#appletContainer").css("position", "absolute").offset({
            top: -999
        })
    };
    this.updateSize = function(a) {};
    this.sendChatMessage = function(a) {
        appletMethodsCallStack.push(["sendMessage",
            [a]
        ])
    };
    this.reconnect = function() {
        appletMethodsCallStack.push([p.RECONNECT, []])
    };
    this.switchToAppletWebcam = function(a) {
        appletMethodsCallStack.push([p.SWITCH_TO_APPLET_WEBCAM, [a]])
    };
    this.sendWebRTCPreference = function(a) {
        appletMethodsCallStack.push([p.SEND_WEBRTC_PREFERENCES, [JSON.stringify(a)]])
    };
    this.setBlockedSoftares = function(a) {
        e.blockedSoftwares = JSON.stringify(a)
    };
    this.speedupScreenCapture = function() {
        appletMethodsCallStack.push([p.CANDIDATE_NAVIGATE_OUT, []])
    };
    this.normalizeRegularScreenCaptureSpeed =
        function() {
            appletMethodsCallStack.push([p.CANDIDATE_NAVIGATE_IN, []])
        };
    this.captureScreen = function() {
        appletMethodsCallStack.push([p.CAPTURE_SCREEN, []])
    };
    this.verifySoftwares = function() {
        appletMethodsCallStack.push([p.VERIFY_SOFTWARE, []])
    };
    this.verifyDevices = function() {
        appletMethodsCallStack.push([p.VERIFY_DEVICES, []])
    };
    this.init = function() {
        e.appletCommunicator = function(a) {
            var b = !0;
            switch (a.chatType) {
                case k.AppletMessageType.SCREEN_IMAGE:
                case k.AppletMessageType.SOFTWARE_VERIFICATION_DATA:
                    b = !1;
                    h.$broadcast(a.chatType,
                        a.message);
                    break;
                case k.AppletMessageType.SELF_ONLINE:
                    l = !0, n({
                        chatType: k.AppletMessageType.CONNECTION_SUCCESS,
                        message: ""
                    })
            }
            m = (new Date).getTime();
            b && n(a)
        };
        u = f(a, k.Constants.CHECK_APPLET_CRASH_INTERVAL_TIME)
    };
    this.logEvents = function(a) {
        appletMethodsCallStack.push([k.ChatMessageType.CANDIDATE_EVENT, [JSON.stringify(a)]])
    };
    this.captureWebcamImage = angular.noop;
    this.sendMessage = function(a) {
        appletMethodsCallStack.push([a.chatType, [a.message]])
    };
    this.getClientId = function() {
        return y ? y.clientId : 0
    };
    this.reconnectAuthRequest =
        this.startCandidateProctoring = this.startPresenterStream = this.getWebRTCPreferences = this.updateAuthToken = angular.noop
}]);
mettlProctor = angular.module("mettlProctor");
mettlProctor.service("ConnectionManagerService", ["LoggerService", "$timeout", "$q", "WebSocketService", "MettlProctoringFactory", "StreamingService", "AppletConstants", "SocketMessageConstants", function(b, c, e, f, h, g, k, a) {
    function d(a) {
        g.stopStreaming();
        E >= D ? (f.stopCommunication(), l(I.callbackUrlForClose, a)) : (b.info("reconnecting web socket, count being: ", E), f.connect(), E++)
    }

    function p() {
        l(I.callbackUrlForMessage, {
            chatType: a.StreamingMessageType.CONNECTION_SUCCESS,
            message: ""
        })
    }

    function q() {
        D = G ? 0 : h.getRetrialCount();
        E = 0;
        l(I.callbackUrlForOpen);
        r ? w(L) : p()
    }

    function m(b) {
        var d = b.chatType;
        d != a.StreamingMessageType.STREAMING_HANDSHAKE_SUCCESS && d != a.StreamingMessageType.ICE_CANDIDATE && d != a.StreamingMessageType.SDP_ANSWER && d != a.StreamingMessageType.STOP_STREAMING && d != a.StreamingMessageType.STREAMING_HANDSHAKE_FAILURE && d != a.StreamingMessageType.WebRTC_RECORDING_URL && d != a.StreamingMessageType.SDP_OFFER && d != a.StreamingMessageType.SEND_SDP || g.socketMessageHandler(b);
        l(I.callbackUrlForMessage, b)
    }

    function u(a) {
        l(I.callbackUrlForError,
            a)
    }

    function l(a, b) {
        "function" == typeof a && a(b)
    }

    function n(a, d) {
        O = !0;
        g.startStreaming(a, !1, d).then(function() {
            b.log("streaming resolve")
        }, z, y)
    }

    function y(a) {
        B = 0;
        b.info("Streaming started with url", a);
        F = 1E4;
        r && p()
    }

    function z(a) {
        b.error("Error in starting streaming", a);
        A(a)
    }

    function A(a) {
        H(a).then(function() {
            O ? v() : b.debug("Streaming is not active. Doing nothing.")
        }, function(a) {
            b.info("socket is disconnected. Doing nothing.")
        })
    }

    function H(a) {
        var d = e.defer();
        f.checkWebSocketConnection().then(function() {
            b.info("web socket connection is connected ");
            d.resolve()
        }, function(a) {
            b.info("web socket connection status error: ", a);
            d.reject()
        });
        return d.promise
    }

    function v() {
        B++;
        g.disposeRTC();
        B > M ? (b.info("Could not connect to the streaming server! Cleaning up!"), E = D, f.closeWebSocketConnection()) : J ? (b.warn("streaming connection ended abruptly! Trying to reconnect, retry attempt: ", B), K = c(function() {
            x()
        }, F)) : r ? (b.warn("streaming connection ended abruptly! Trying to reconnect, retry attempt: ", B), N = c(function() {
            n(L, r)
        }, F)) : b.warn("streaming connection ended abruptly! No need to retry: ")
    }

    function w(a) {
        L = a;
        r = !0;
        n(a, r)
    }

    function t() {
        O = !1;
        N && c.cancel(N);
        B = 0;
        g.stopStreaming()
    }

    function x() {
        O = !0;
        g.startViewer(L, C).then(function() {
            b.log("streaming resolve")
        }, z, y)
    }
    var D = 0,
        E = 0,
        G = !1,
        I, r = !1,
        L, C, B = 0,
        M = 3,
        F = 1E4,
        J = !1,
        K, N, O = !1;
    this.updateProctoringParameters = function(a) {
        I = a;
        f.updateProctoringParameters(I)
    };
    this.startCommunication = function(a, b) {
        I = a;
        D = (G = b) ? 0 : h.getRetrialCount();
        E = 0;
        f.startCommunication(a, b, {
            callbackUrlForClose: d,
            callbackUrlForOpen: q,
            callbackUrlForMessage: m,
            callbackUrlForError: u
        })
    };
    this.stopCommunication = function() {
        t();
        f.stopCommunication()
    };
    this.updateRetrialCount = function() {
        D = G ? 0 : h.getRetrialCount()
    };
    this.startPresenterStream = n;
    this.stopPresenterStreaming = t;
    this.startRecording = w;
    this.startViewerStream = function(a, b) {
        L = a;
        C = b;
        J = !0;
        M = 1E3;
        F = 2E3;
        x()
    };
    this.stopViewerStreaming = function() {
        O = !1;
        K && c.cancel(K);
        B = 0;
        g.stopViewer()
    };
    this.setStreamingMaxRetries = function(a) {
        M = a
    }
}]);
mettlProctor = angular.module("mettlProctor");
mettlProctor.service("AppletScreenCaptureService", ["LoggerService", "$q", "ErrorConstants", "SocketMessageConstants", "$timeout", "$window", "$rootScope", "UtilityFactory", "MettlProctoringFactory", "appletService", "AppletConstants", function(b, c, e, f, h, g, k, a, d, p, q) {
    var m;
    k.$on(q.AppletMessageType.SCREEN_IMAGE, function(a, d) {
        b.log("received screen image.", d);
        m ? (m.resolve(d), m = void 0) : b.log("screen request data promise is not available.")
    });
    this.captureScreen = function() {
        m && (b.log("Havent received previous data. Rejecting it on new request."),
            m.reject("Havent received previous data. Rejecting it on new request."));
        m = c.defer();
        p.captureScreen();
        return m.promise
    }
}]);
mettlProctor = angular.module("mettlProctor");
mettlProctor.service("PingPongService", ["LoggerService", "$timeout", "$q", "ErrorConstants", function(b, c, e, f) {
    function h() {
        g && (c.cancel(k), g.reject(), g = k = void 0)
    }
    var g, k;
    this.timeout = function(a) {
        h();
        var d = a || 2E4;
        g = e.defer();
        k = c(function() {
            b.log("Ping is delayed for more than" + d + " sec");
            g.resolve()
        }, d);
        return g.promise
    };
    this.stop = h;
    this.resolve = function() {
        c.cancel(k);
        g && (b.log("Resolving pingpong timeout"), g.resolve())
    }
}]);
mettlProctor = angular.module("mettlProctor");
mettlProctor.service("ProctoringLiteService", ["LoggerService", "$timeout", "$q", "ErrorConstants", "AppletScreenCaptureService", "ScreenUtilService", "DiagnosticsFactory", "WebSocketService", "$webRTC", "MettlProctoringFactory", "AppletConstants", "RegularImageService", "StreamingService", "StreamingService", "ConnectionManagerService", "AudioProctoringService", function(b, c, e, f, h, g, k, a, d, p, q, m, u, l, n, y) {
    function z(a, b) {
        var d = {
            chatType: a,
            message: b
        };
        k.getWebsocketDiagnosticsOpts().callbackUrlForMessage(d)
    }

    function A(a) {
        var b =
            e.defer();
        H(a).then(function(a) {
            var c = d.getWebcamInfo();
            c && 1 < c.webcamNames.length && z(q.WEBRTC_MESSAGES.MULITCAM_WARNING, JSON.stringify(c));
            b.resolve(a)
        }, b.reject);
        return b.promise
    }

    function H(a) {
        var b = e.defer(),
            d = {
                webSocketServerUrl: a.webSocketServerUrl,
                webSocketAuthUrl: a.webSocketAuthUrl,
                streamingServerUrl: a.streamingServerUrl,
                authToken: JSON.stringify(a.authToken),
                callbackUrlForOpen: function() {
                    a.callbackUrlForOpen();
                    b.resolve()
                },
                callbackUrlForClose: function(d) {
                    a.callbackUrlForClose(d);
                    b.reject()
                },
                callbackUrlForMessage: a.callbackUrlForMessage,
                checkScreens: a.checkScreens,
                isCheckWebRTC: !0,
                retrialCount: a.retrialCount
            };
        p.init(d);
        n.startCommunication(d, !1);
        return b.promise
    }

    function v(b) {
        a.sendMessage(b)
    }

    function w() {
        g.stopScreenFeed();
        d.stopCheckForWorkingCamera().then(function() {
            d.stopWebRTC();
            n.stopCommunication()
        }, function(a) {
            b.error("Error while stoping camera ", a)
        })
    }

    function t(a) {
        p.updateAuthToken(a);
        a = p.getSocketParams();
        A(a)
    }
    var x, D = !1,
        E = q.AppletMessageType;
    this.showStream = this.hideStream =
        angular.noop;
    this.startSelfStreaming = function(a) {
        d.showStream(a);
        z(E.STREAMING_FOR_IMAGE_READY)
    };
    this.takeFaceSnap = function() {
        d.captureImage(!0).then(function(a) {
            z(E.SHOW_FACE_IMAGE, a)
        }, function(a) {
            z(E.CAMERA_UNAVAILABLE, a)
        })
    };
    this.takeIdSnap = function() {
        d.captureImage(!0).then(function(a) {
            z(E.SHOW_ID_IMAGE, a)
        }, function(a) {
            z(E.CAMERA_UNAVAILABLE, a)
        })
    };
    this.startCommunication = A;
    this.updateAuthToken = function(a) {
        p.updateAuthToken(a)
    };
    this.sendMessage = v;
    this.speedupScreenCapture = m.speedupRegularScreenCapture;
    this.normalizeRegularScreenCaptureSpeed = m.normalizeRegularScreenCaptureSpeed;
    this.getWebRTCPreferences = d.getWebRTCPreferences;
    this.startPresenterStream = function(a) {
        n.startPresenterStream(a)
    };
    this.shutdownProctoring = function() {
        m.stopRegularImageCapture();
        y.stoptMicMuteCheck();
        D && b.info("Stopping applet communication");
        w()
    };
    this.sendAck = this.finishTest = this.sendStartTestMessage = v;
    this.stopPresenterStreaming = n.stopPresenterStreaming;
    this.startVideoStreamByIndex = d.startVideoStreamByIndex;
    this.startCandidateProctoring =
        function(a, b, c) {
            m.init(D);
            var e = d.getWebRTCPreferences(),
                e = JSON.stringify(e);
            v({
                chatType: q.WEBRTC_MESSAGES.WEBRTC_PREFERENCES,
                message: e
            });
            m.startRegularImageCapture(c);
            p.setRetrialCount(q.Constants.WEBSOCKET_RETRIAL_COUNT);
            n.updateRetrialCount();
            y.startMicMuteCheck();
            a && n.startRecording(b)
        };
    this.sendWebCamChanged = angular.noop;
    this.updateProctoringParameters = function(a) {
        p.init(a);
        n.updateProctoringParameters(a)
    };
    this.reconnectAuthRequest = this.reconnect = t;
    this.setMaxRetries = n.setStreamingMaxRetries;
    this.installBrowserPlugin = g.installBrowserPlugin;
    this.updateBrowserPlugin = g.updateBrowserPlugin;
    this.shutdown = w;
    this.stopViewerStreaming = n.stopViewerStreaming;
    this.startViewerStream = function(a, b) {
        n.startViewerStream(a, b)
    };
    this.captureStreamImage = l.captureStreamImage;
    this.getICE = l.getICE;
    this.captureScreen = function() {
        return x.captureScreen()
    };
    this.getClientId = p.getClientId;
    this.recheckSystemSoftware = angular.noop;
    this.init = function(a, b) {
        x = (D = b) ? h : g
    }
}]);
mettlProctor = angular.module("mettlProctor");
mettlProctor.service("AudioProctoringService", ["$webRTC", "MettlProctoringFactory", "$interval", "$log", "ErrorConstants", function(b, c, e, f, h) {
    var g;
    this.startMicMuteCheck = function() {
        c.hasAudioProctoring() && (g = e(function() {
            b.checkForMicMute().then(function(b) {
                f.log(b)
            }, function(b) {
                f.error(b);
                c.getCallbackUrlForMessage()({
                    chatType: h.WebRTC.MICROPHONE_MUTED
                })
            })
        }, 1E4))
    };
    this.stoptMicMuteCheck = function() {
        g && e.cancel(g)
    }
}]);
mettlProctor = angular.module("mettlProctor");
mettlProctor.service("LoggerService", ["$log", "$http", function(b, c) {
    this.log = function(c, f) {
        b.log(c, f)
    };
    this.warn = function(c, f) {
        b.warn(c, f)
    };
    this.error = function(c, f) {
        b.warn(c, f)
    };
    this.info = function(c, f) {
        b.info(c, f)
    };
    this.debug = function(c, f) {
        b.debug(c, f)
    }
}]);
mettlProctor = angular.module("mettlProctor");
mettlProctor.service("AppletSystemVerifierService", ["LoggerService", "$q", "ErrorConstants", "SocketMessageConstants", "$timeout", "$window", "$rootScope", "UtilityFactory", "AppletConstants", "appletService", function(b, c, e, f, h, g, k, a, d, p) {
    var q;
    k.$on(d.AppletMessageType.SOFTWARE_VERIFICATION_DATA, function(a, d) {
        b.log("received software verification data.", d);
        q ? ("null" != d ? q.reject(d) : q.resolve(d), q = void 0) : b.log("sfotware request data promise is not available.")
    });
    this.verifySoftwares = function() {
        q && (b.log("Havent received previous data of software verification. Allowing it on new request."),
            q.resolve("Havent received previous data of software verification. Allowing it on new request."));
        q = c.defer();
        p.verifySoftwares();
        return q.promise
    };
    var m;
    k.$on(d.AppletMessageType.DEVICE_VERIFICATION_DATA, function(a, d) {
        b.log("received device information. ", d);
        m ? (d && 1 >= d ? m.resolve(d) : m.reject(d), m = void 0) : b.log("device verification request data promise is not available.")
    });
    this.verifyDevices = function() {
        m && (b.log("Havent received previous data of device  verification. Allowing it on new request."),
            m.resolve("Havent received previous data of device  verification. Allowing it on new request."));
        m = c.defer();
        p.verifyDevices();
        return m.promise
    }
}]);
mettlProctor = angular.module("mettlProctor");
mettlProctor.service("RegularImageService", ["LoggerService", "$timeout", "MettlProctoringFactory", "WebSocketService", "SocketMessageConstants", "$webRTC", "ScreenUtilService", "RegularSystemVerifier", "AppletScreenCaptureService", "AppletSystemVerifierService", function(b, c, e, f, h, g, k, a, d, p) {
    function q(a) {
        t && c.cancel(t);
        G.verifySoftwares().then(function() {
            b.log("software verification success");
            t = c(function() {
                q(a)
            }, a)
        }, function(a) {
            b.log("software verification failed.TODO: send this to mettl.", a);
            a = {
                chatType: "SUSPICIOUS_SOFTWARE",
                message: a
            };
            f.sendMessage(a);
            e.getCallbackUrlForMessage()(a)
        })
    }

    function m(a) {
        x && c.cancel(x);
        G.verifyDevices().then(function() {
            b.log("device verification success");
            x = c(function() {
                m(a)
            }, a)
        }, function(d) {
            b.log("device verification failed.Device count :" + d);
            f.sendMessage({
                chatType: "MULITSCREEN_WARNING",
                message: d
            });
            x = c(function() {
                m(a)
            }, a)
        })
    }

    function u(a) {
        v && c.cancel(v);
        E.captureScreen().then(function(b) {
            H = a;
            var d = n();
            d.violation = A;
            y(d, b, h.StreamingMessageType.SCREEN_IMAGE);
            v = c(function() {
                u(a)
            }, a)
        }, function(d) {
            b.log("error in sending screen image.",
                d);
            v = c(function() {
                u(a)
            }, a)
        })
    }

    function l(a) {
        w && c.cancel(w);
        g.captureImage().then(function(b) {
            var d = n();
            d.violation = !1;
            y(d, b, h.StreamingMessageType.IMAGE);
            w = c(function() {
                l(a)
            }, a)
        }, function(d) {
            b.log("error in sending regular image.", d);
            w = c(function() {
                l(a)
            }, a)
        })
    }

    function n() {
        var a = {
            chatType: h.StreamingMessageType.GET_TESTTIME_LEFT
        };
        return e.getCallbackUrlForMessage()(a)
    }

    function y(a, b, d) {
        var c = e.getClientId();
        a.clientId = c;
        a = {
            chatType: d,
            message: b,
            metaData: JSON.stringify(a)
        };
        f.sendMessage(a)
    }

    function z(a) {
        b.debug("updating screen capturing time interval:" +
            a);
        e.hasScreenCapture() && v && H != a ? (v && c.cancel(v), u(a)) : b.warn("Regular screen capture thread is not initialized")
    }
    var A = !1,
        H, v, w, t, x, D = 6E4,
        E, G;
    this.startRegularImageCapture = function(a) {
        l(2E4);
        e.hasScreenCapture() && (D = a ? a : 2E4, u(D));
        e.hasSoftwareVerification() && (q(18E4), m(18E4))
    };
    this.stopRegularImageCapture = function() {
        b.debug("Regular image capture thread going to Stop.");
        v && c.cancel(v);
        w && c.cancel(w);
        x && c.cancel(x);
        t && c.cancel(t)
    };
    this.speedupRegularScreenCapture = function(a) {
        A = a;
        z(1E4)
    };
    this.normalizeRegularScreenCaptureSpeed =
        function(a) {
            A = a;
            z(D)
        };
    this.init = function(b) {
        b ? (E = d, G = p) : (E = k, G = a)
    }
}]);
mettlProctor = angular.module("mettlProctor");
mettlProctor.service("WebSocketService", ["LoggerService", "PingPongService", "ErrorConstants", "$q", "$http", "$timeout", "$rootScope", "SocketMessageConstants", function(b, c, e, f, h, g, k, a) {
    function d() {
        A.onclose = function(a) {
            b.log("webSocket connection is closed.Doing nothing.", a)
        };
        A.onerror = function(a, d) {
            b.log("error occurred in webSocket connection", JSON.stringify(a))
        };
        A.onopen = function() {
            b.log("WebSocket connection is established");
            H = !1;
            p();
            w.callbackUrlForOpen()
        };
        A.onmessage = function(a) {
            t && (t.resolve(),
                t = void 0);
            p();
            a = a.data;
            var d = {};
            try {
                d = JSON.parse(a)
            } catch (c) {
                b.log("error while parsing onMessage data", c)
            }
            "PING" == d.chatType ? (a = d, a.chatType = "PONG", a.message = a.message + "|" + Date.now(), l(a)) : (b.log("received  new message.", d), w.callbackUrlForMessage(d))
        }
    }

    function p() {
        c.timeout().then(function() {
            m()
        })
    }

    function q() {
        b.log("New webSocket connection request arrived");
        if (!H) {
            H = !0;
            try {
                h({
                    method: "POST",
                    url: v.webSocketAuthUrl,
                    data: v.authToken,
                    timeout: 1E4
                }).then(function(a) {
                    b.log("authenticating completed",
                        a);
                    a = a.data;
                    a.status ? (a = a.token, u(), p(), A = new WebSocket(v.webSocketServerUrl + "?token\x3d" + a), d()) : m()
                }, function(a) {
                    b.log("error in authenticating socket auth request", a);
                    m()
                })
            } catch (a) {
                b.log("Error occurred, in web-socket connection ", a), m()
            }
        }
    }

    function m(a) {
        c.stop();
        u();
        a || (a = z.SOCKET_SERVER_ERROR);
        g(function() {
            H = !1;
            w.callbackUrlForClose(a)
        }, 1E4)
    }

    function u() {
        t && (t.reject(), t = void 0);
        c.stop();
        if (A) try {
            b.log("Closing websocket connection"), A.close()
        } catch (a) {
            b.log("Error in stopping websocket.", a)
        } else b.log("websocket in not defined. Skipping .close");
        A = void 0
    }

    function l(d) {
        if (d.message && 4096 < d.message.length) {
            var c = y(),
                e = angular.copy(d);
            e.chunkType = a.MessageChunkType.Start;
            var f = parseInt((d.message.length + 4096 - 1) / 4096);
            e.message = "" + f;
            e.authToken = c;
            b.debug("Sending chat message in chunks. Chat type :%s,chunk count :%s ,chunk id : %s ,chunk size: %s ,message size: %s ", d.chatType, f, c, 4096, d.message.length);
            n(e);
            b.debug("chunk start message sent. chunk id:{}", c);
            for (e = 0; e < f; e++) {
                var h = angular.copy(d);
                h.chunkType = a.MessageChunkType.Data;
                h.authToken =
                    c;
                var p = 4096 * e;
                h.message = d.message.substring(p, Math.min(d.message.length, p + 4096));
                n(h);
                b.debug("chunk data message sent. chunk id:{} ,chunk index :{}", c, e)
            }
            d = angular.copy(d);
            d.chunkType = a.MessageChunkType.End;
            d.authToken = c;
            d.message = "";
            n(d);
            b.debug("chunk finish message sent. chunk id:{}", c)
        } else b.log("writting message on socket"), n(d)
    }

    function n(a) {
        try {
            A && A.send(JSON.stringify(a))
        } catch (d) {
            b.log("error in sending message.", d)
        }
    }

    function y() {
        function a() {
            return Math.floor(65536 * (1 + Math.random())).toString(16).substring(1)
        }
        return a() + a() + "-" + a() + "-" + a() + "-" + a() + "-" + a() + a() + a()
    }
    var z = e.WebSocket,
        A, H = !1,
        v = {},
        w = {},
        t;
    this.startCommunication = function(a, b, d) {
        v = a;
        w = d;
        q()
    };
    this.stopCommunication = function() {
        u()
    };
    this.sendMessage = l;
    this.sendImage = function(a) {};
    this.updateProctoringParameters = function(a) {
        v = a
    };
    this.connect = q;
    this.checkWebSocketConnection = function() {
        t = f.defer();
        return t.promise
    };
    this.closeWebSocketConnection = function() {
        c.resolve()
    }
}]);
mettlProctor = angular.module("mettlProctor");
mettlProctor.service("ScreenUtilService", ["LoggerService", "$q", "ErrorConstants", "SocketMessageConstants", "$timeout", "$window", "UtilityFactory", "MettlProctoringFactory", function(b, c, e, f, h, g, k, a) {
    function d(a) {
        var b = {
            audio: !1,
            video: {}
        };
        DetectRTC.browser.isFirefox ? (b.video.mediaSource = "screen", navigator.mediaDevices.getUserMedia(b).then(p, q)) : (DetectRTC.browser.isChrome ? b.video.mandatory = {
                chromeMediaSource: "desktop",
                chromeMediaSourceId: a,
                maxWidth: window.screen.width,
                maxHeight: window.screen.height
            } : b.video.mediaSource =
            "screen", navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mediaDevices.getUserMedia || navigator.mozGetUserMedia, navigator.getUserMedia(b, p, q))
    }

    function p(a) {
        DetectRTC.browser.isFirefox && a.getTracks()[0] && "Primary Monitor" != a.getTracks()[0].label ? m(r.reject, e.ScreenUtil.SCREEN_MULTIPLE_DETECTED) : (b.log("getUserMedia for screen succeeded!: " + a), x = a, l(), m(r.resolve, f.Screen.DIAGNOSTICS_SUCCESS, x))
    }

    function q(a) {
        b.log("getUserMedia for screen failed!: thawing generic error" +
            a);
        m(r.reject, e.ScreenUtil.SCREEN_PERMISSION_DENIED, e.ScreenUtil.SCREEN_PERMISSION_SYSTEM_DENIED)
    }

    function m(a, b, d) {
        if (D && b) switch (a) {
            case r.reject:
                D.reject(G(b, d));
                break;
            case r.notify:
                D.notify(b, d);
                break;
            case r.resolve:
                D.resolve(G(b, d))
        }
    }

    function u(b) {
        if (!L) {
            var d = a.getCallbackUrlForMessage();
            d && d(G(b))
        }
    }

    function l() {
        if (x) {
            x.onactive = function(a) {
                b.log("screen device on active", a)
            };
            x.onaddtrack = function(a) {
                b.log("screen device on add track", a)
            };
            x.oninactive = function(a) {
                b.log("screen device on inactive",
                    a);
                u(e.ScreenUtil.SCREEN_FEED_INACTIVE)
            };
            x.onremovetrack = function(a) {
                b.log("screen device on remove track", a);
                u(e.ScreenUtil.SCREEN_FEED_STOPPED)
            };
            var a = x.getTracks();
            a && 0 < a.length && (a[0].onended = function(a) {
                b.log("screen device on ended", a)
            })
        }
    }

    function n() {
        g.addEventListener("message", function(a) {
            if (a.origin == window.location.origin && a.data) switch (a.data.type) {
                case "SS_UI_PING":
                    break;
                case "SS_UI_PONG":
                    b.info("Pong message came from plugin", a.data);
                    if (a.data.layout && 1 < a.data.layout.length) {
                        t = w.multipleScreen;
                        m(r.reject, e.ScreenUtil.SCREEN_MULTIPLE_DETECTED);
                        break
                    }
                    E = a.data.version;
                    t == w.unAvailable ? (t = w.ok, 1.8 > parseFloat(E) ? m(r.reject, e.ScreenUtil.SCREEN_PLUGIN_NOT_UPDATED) : (m(r.notify, G(e.ScreenUtil.SCREEN_GIVE_PERMISSION)), g.postMessage({
                        type: "SS_UI_REQUEST",
                        text: "request",
                        url: location.origin
                    }, "*"))) : b.warn("Delayed plugin confirmation.Ignoring this.");
                    break;
                case "SS_DIALOG_SUCCESS":
                    b.info("startScreenCapture callback is arrived", new Date);
                    d(a.data.streamId);
                    break;
                case "SS_DIALOG_CANCEL":
                    b.log("User cancelled!");
                    m(r.reject, e.ScreenUtil.SCREEN_PERMISSION_DENIED, e.ScreenUtil.SCREEN_PERMISSION_USER_DENIED);
                    break;
                case "SS_EXTENSION_INSTALLED":
                    b.log("extension installed!");
                    m(r.notify, e.ScreenUtil.EXTENSION_INSTALLED);
                    break;
                case "SS_EXTENSION_STARTED":
                    b.log("extension started!");
                    m(r.notify, e.ScreenUtil.EXTENSION_STARTED);
                    break;
                case "SS_EXTENSION_SUSPENDED":
                    b.log("extension suspended!");
                    m(r.notify, G(e.ScreenUtil.EXTENSION_SUSPENDED));
                    break;
                case "SS_UI_HELLO":
                    b.log("chrome : extension is available!", a.data);
                    break;
                case "SS_UI_DISCONNECTED":
                    b.log("chrome : extension disconnection event arrived!", a.data);
                    break;
                case "SS_UI_UPDATE_AVAILABLE":
                    b.log("chrome : extension update event arrived!", a.data);
                    C && h(function() {
                        C.resolve()
                    }, 5E3);
                    break;
                case "SS_DISPLAY_CHANGED":
                    b.log("chrome : extension display changed event arrived!", a.data);
                    a.data.layout && 1 < a.data.layout.length && (I = !0, u(e.ScreenUtil.SCREEN_MULTIPLE_DETECTED));
                    break;
                default:
                    b.log("Unhandled event arrived!", a.data)
            }
        })
    }

    function y(a) {
        var d = c.defer();
        if (DetectRTC.browser.isChrome) {
            var e =
                document.createElement("img");
            e.src = "chrome-extension://" + a + "/icon16.png";
            e.onload = function(a) {
                b.log("extension image is present", a);
                t = w.available;
                d.resolve()
            };
            e.onerror = function(a) {
                b.log("extension image is not present", a);
                t = w.unAvailable;
                d.reject()
            }
        } else d.reject();
        return d.promise
    }

    function z() {
        DetectRTC.browser.isChrome ? m(r.reject, e.ScreenUtil.SCREEN_PLUGIN_NOT_INSTALLED + "_chrome") : m(r.reject, e.ScreenUtil.SCREEN_PLUGIN_NOT_INSTALLED + "_firefox")
    }

    function A(a) {
        L = !1;
        D = c.defer();
        DetectRTC.browser.isChrome ?
            (g.postMessage({
                type: "SS_UI_PING",
                url: location.origin
            }, "*"), h(function() {
                t != w.ok && t != w.multipleScreen ? y(a).then(function() {
                    m(r.reject, e.ScreenUtil.SCREEN_PLUGIN_DISABLED)
                }, z) : b.log("Plugin available", t)
            }, 1E3)) : DetectRTC.browser.isFirefox ? h(function() {
                m(r.notify, G(e.ScreenUtil.SCREEN_GIVE_PERMISSION));
                d()
            }, 1E3) : DetectRTC.browser.isSafari && m(r.reject, e.ScreenUtil.SCREEN_FEED_UNAVAILABLE);
        return D.promise
    }

    function H(b) {
        a.getCallbackUrlForMessage()({
            chatType: b || e.ScreenUtil.SCREEN_FEED_UNAVAILABLE
        })
    }

    function v() {
        var a = c.defer(),
            d = document.getElementById("mettlProctoringScreen");
        if ("undefined" == typeof d || null == d) {
            var f = x;
            if (f) {
                d = k.createVideoElement("mettlProctoringScreen");
                d.onended = H;
                d.srcObject = f;
                document.body.appendChild(d);
                b.log("video element created");
                var p = h(function() {
                    a && (b.log("video element data loaded timeout occurred"), a.resolve(d), a = void 0)
                }, 1E4);
                d.addEventListener("loadeddata", function() {
                    a && (b.log("video element data loaded"), a.resolve(d), a = void 0, h.cancel(p))
                }, !1);
                d.load()
            } else a.reject(e.ScreenUtil.SCREEN_FEED_UNAVAILABLE)
        } else a.resolve(d);
        return a.promise
    }
    var w = {
            ok: "ok",
            disabled: "disabled",
            expired: "expired",
            available: "available",
            unAvailable: "unAvailable",
            multipleScreen: "multipleScreen"
        },
        t = w.unAvailable,
        x, D, E, G = k.makeMessage,
        I = !1,
        r = {
            notify: 3,
            resolve: 1,
            reject: 2
        },
        L = !1,
        C;
    DetectRTC.browser.isFirefox || n();
    this.startScreenCapture = this.runDiagnostics = A;
    this.stopScreenFeed = function() {
        var a = c.defer();
        L = !0;
        if (x) return v().then(function(a) {
            a.onended = angular.noop;
            try {
                x.getTracks().forEach(function(a) {
                    a.stop && a.stop()
                })
            } catch (d) {
                b.log("error occurred while stopping screen-feed",
                    d)
            }
        }, a.reject), a.promise
    };
    this.getStreamDataUrl = function() {
        return x
    };
    this.captureScreen = function() {
        var a = c.defer();
        if (I) H(e.ScreenUtil.SCREEN_MULTIPLE_DETECTED), a.reject();
        else if (x) {
            var d = x.getTracks();
            d && 0 != d.length && "ended" != d[0].readyState ? v().then(function(d) {
                var c = k.getCanvasById("webRTCScreenImage");
                c.width = d.videoWidth || 1024;
                c.height = d.videoHeight || 768;
                c.getContext("2d").drawImage(d, 0, 0, c.width, c.height);
                d = k.compressImage(c, "screen");
                b.info("Captured image using screenService.Image Size:",
                    d.length);
                a.resolve(d.replace("data:image/jpeg;base64,", ""))
            }, a.reject) : (H(), a.reject())
        } else H(), a.reject();
        return a.promise
    };
    this.installBrowserPlugin = function(a) {
        function b() {
            e.resolve()
        }

        function d(a) {
            e.reject(a)
        }
        var e = c.defer();
        try {
            DetectRTC.browser.isChrome && chrome.webstore.install(a, b, d)
        } catch (f) {
            d(f)
        }
        return e.promise
    };
    this.updateBrowserPlugin = function(a) {
        C = c.defer();
        g.postMessage({
            type: "SS_UI_UPDATE",
            text: "request",
            url: location.origin
        }, "*");
        return C.promise
    }
}]);
angular.module("mettlProctor").service("DeployJavaService", function() {
    var b = function() {
        function c(a) {
            k.debug && (console.log ? console.log(a) : alert(a))
        }

        function e(a) {
            if (null == a || 0 == a.length) return "http://java.com/dt-redirect";
            "\x26" == a.charAt(0) && (a = a.substring(1, a.length));
            return "http://java.com/dt-redirect?" + a
        }
        var f = ["id", "class", "title", "style"];
        "classid codebase codetype data type archive declare standby height width usemap name tabindex align border hspace vspace".split(" ").concat(f, ["lang", "dir"],
            "onclick ondblclick onmousedown onmouseup onmouseover onmousemove onmouseout onkeypress onkeydown onkeyup".split(" "));
        var h = "codebase code name archive object width height alt align hspace vspace".split(" ").concat(f),
            g;
        try {
            g = -1 != document.location.protocol.indexOf("http") ? "//java.com/js/webstart.png" : "http://java.com/js/webstart.png"
        } catch (a) {
            g = "http://java.com/js/webstart.png"
        }
        var k = {
            debug: null,
            version: "20120801",
            firefoxJavaVersion: null,
            myInterval: null,
            preInstallJREList: null,
            returnPage: null,
            brand: null,
            locale: null,
            installType: null,
            EAInstallEnabled: !1,
            EarlyAccessURL: null,
            oldMimeType: "application/npruntime-scriptable-plugin;DeploymentToolkit",
            mimeType: "application/java-deployment-toolkit",
            launchButtonPNG: g,
            browserName: null,
            browserName2: null,
            getJREs: function() {
                var a = [],
                    b = this.getBrowser();
                console.log(b);
                "MSIE" == b ? (console.log("checking with 1.8"), this.testUsingActiveX("1.8.0") ? a[0] = "1.8.0" : this.testUsingActiveX("1.7.0") ? a[0] = "1.7.0" : this.testUsingActiveX("1.6.0") ? a[0] = "1.6.0" : this.testUsingActiveX("1.5.0") ?
                    a[0] = "1.5.0" : this.testUsingActiveX("1.4.2") ? a[0] = "1.4.2" : this.testForMSVM() && (a[0] = "1.1")) : "Netscape Family" == b && (this.getJPIVersionUsingMimeType(), null != this.firefoxJavaVersion ? a[0] = this.firefoxJavaVersion : this.testUsingMimeTypes("1.7") ? a[0] = "1.7.0" : this.testUsingMimeTypes("1.6") ? a[0] = "1.6.0" : this.testUsingMimeTypes("1.5") ? a[0] = "1.5.0" : this.testUsingMimeTypes("1.4.2") ? a[0] = "1.4.2" : "Safari" == this.browserName2 && (this.testUsingPluginsArray("1.7.0") ? a[0] = "1.7.0" : this.testUsingPluginsArray("1.6") ? a[0] =
                    "1.6.0" : this.testUsingPluginsArray("1.5") ? a[0] = "1.5.0" : this.testUsingPluginsArray("1.4.2") && (a[0] = "1.4.2")));
                if (this.debug)
                    for (b = 0; b < a.length; ++b) c("[getJREs()] We claim to have detected Java SE " + a[b]);
                console.log("JREs are:");
                console.log(a);
                return a
            },
            installJRE: function(a, b) {
                if (this.isPluginInstalled() && this.isAutoInstallEnabled(a)) {
                    var c = !1;
                    if (c = this.isCallbackSupported() ? this.getPlugin().installJRE(a, b) : this.getPlugin().installJRE(a)) this.refresh(), null != this.returnPage && (document.location = this.returnPage);
                    return c
                }
                return this.installLatestJRE()
            },
            isAutoInstallEnabled: function(a) {
                if (!this.isPluginInstalled()) return !1;
                "undefined" == typeof a && (a = null);
                if ("MSIE" != b.browserName || b.compareVersionToPattern(b.getPlugin().version, ["10", "0", "0"], !1, !0)) a = !0;
                else if (null == a) a = !1;
                else {
                    var d = "1.6.0_33+";
                    if (null == d || 0 == d.length) a = !0;
                    else {
                        var c = d.charAt(d.length - 1);
                        "+" != c && "*" != c && -1 != d.indexOf("_") && "_" != c && (d += "*", c = "*");
                        d = d.substring(0, d.length - 1);
                        if (0 < d.length) {
                            var e = d.charAt(d.length - 1);
                            if ("." == e || "_" == e) d = d.substring(0,
                                d.length - 1)
                        }
                        a = "*" == c ? 0 == a.indexOf(d) : "+" == c ? d <= a : !1
                    }
                    a = !a
                }
                return a
            },
            isCallbackSupported: function() {
                return this.isPluginInstalled() && this.compareVersionToPattern(this.getPlugin().version, ["10", "2", "0"], !1, !0)
            },
            installLatestJRE: function(a) {
                if (this.isPluginInstalled() && this.isAutoInstallEnabled()) {
                    var b = !1;
                    if (b = this.isCallbackSupported() ? this.getPlugin().installLatestJRE(a) : this.getPlugin().installLatestJRE()) this.refresh(), null != this.returnPage && (document.location = this.returnPage);
                    return b
                }
                a = this.getBrowser();
                b = navigator.platform.toLowerCase();
                if ("true" == this.EAInstallEnabled && -1 != b.indexOf("win") && null != this.EarlyAccessURL) this.preInstallJREList = this.getJREs(), null != this.returnPage && (this.myInterval = setInterval("java_utils.poll()", 3E3)), location.href = this.EarlyAccessURL;
                else {
                    if ("MSIE" == a) return this.IEInstall();
                    if ("Netscape Family" == a && -1 != b.indexOf("win32")) return this.FFInstall();
                    location.href = e((null != this.returnPage ? "\x26returnPage\x3d" + this.returnPage : "") + (null != this.locale ? "\x26locale\x3d" + this.locale :
                        "") + (null != this.brand ? "\x26brand\x3d" + this.brand : ""))
                }
                return !1
            },
            runApplet: function(a, b, e, f, h) {
                if ("undefined" == e || null == e) e = "1.1";
                f = e.match("^(\\d+)(?:\\.(\\d+)(?:\\.(\\d+)(?:_(\\d+))?)?)?$");
                null == this.returnPage && (this.returnPage = document.location);
                null != f ? this.writeAppletTag(a, b) : c("[runApplet()] Invalid minimumVersion argument to runApplet():" + e)
            },
            reloadApplet: function() {
                $("#appletContainer").hide().show()
            },
            writeAppletTag: function(a, b) {
                var c = "\x3capplet ",
                    e = "",
                    f = !0;
                if (null == b || "object" != typeof b) b = {};
                for (var g in a) {
                    var l;
                    a: {
                        l = g.toLowerCase();
                        for (var k = h.length, y = 0; y < k; y++)
                            if (h[y] === l) {
                                l = !0;
                                break a
                            } l = !1
                    }
                    l ? (c += " " + g + '\x3d"' + a[g] + '"', "code" == g && (f = !1)) : b[g] = a[g]
                }
                g = !1;
                for (var z in b) {
                    "codebase_lookup" == z && (g = !0);
                    if ("object" == z || "java_object" == z || "java_code" == z) f = !1;
                    e += "\x3cparam name\x3d'" + z + "' value\x3d'" + b[z] + "'/\x3e"
                }
                g || (e += "\x3cparam name\x3d'codebase_lookup' value\x3d'false'/\x3e");
                f && (c += ' code\x3d"dummy"');
                c += "\x3e";
                $("#appletContainer").html(c + "\n" + e + "\n\x3c/applet\x3e")
            },
            versionCheck: function(a,
                b) {
                var e = 0,
                    f = a.match("^(\\d+)(?:\\.(\\d+)(?:\\.(\\d+)(?:_(\\d+))?)?)?(\\*|\\+)?$");
                if (null != f) {
                    for (var h = !1, g = !1, l = [], k = 1; k < f.length; ++k) "string" == typeof f[k] && "" != f[k] && (l[e] = f[k], e++);
                    "+" == l[l.length - 1] ? (g = !0, h = !1, l.length--) : "*" == l[l.length - 1] ? (g = !1, h = !0, l.length--) : 4 > l.length && (g = !1, h = !0);
                    b || (b = this.getJREs());
                    for (k = 0; k < b.length; ++k)
                        if (this.compareVersionToPattern(b[k], l, h, g)) return !0;
                    console.log("jre installed are " + b)
                } else e = "Invalid versionPattern passed to versionCheck: " + a, c("[versionCheck()] " +
                    e), alert(e);
                return !1
            },
            isWebStartInstalled: function(a) {
                if ("?" == this.getBrowser()) return !0;
                if ("undefined" == a || null == a) a = "1.4.2";
                var b = !1;
                null != a.match("^(\\d+)(?:\\.(\\d+)(?:\\.(\\d+)(?:_(\\d+))?)?)?$") ? b = this.versionCheck(a + "+") : (c("[isWebStartInstaller()] Invalid minimumVersion argument to isWebStartInstalled(): " + a), b = this.versionCheck("1.4.2+"));
                return b
            },
            getJPIVersionUsingMimeType: function() {
                for (var a = 0; a < navigator.mimeTypes.length; ++a) {
                    var b = navigator.mimeTypes[a].type.match(/^application\/x-java-applet;jpi-version=(.*)$/);
                    if (null != b && (this.firefoxJavaVersion = b[1], "Opera" != this.browserName2)) break
                }
            },
            launchWebStartApplication: function(a) {
                navigator.userAgent.toLowerCase();
                this.getJPIVersionUsingMimeType();
                if (0 == this.isWebStartInstalled("1.7.0") && (0 == this.installJRE("1.7.0+") || 0 == this.isWebStartInstalled("1.7.0"))) return !1;
                var b = null;
                document.documentURI && (b = document.documentURI);
                null == b && (b = document.URL);
                var c = this.getBrowser(),
                    e;
                "MSIE" == c ? e = '\x3cobject classid\x3d"clsid:8AD9C840-044E-11D1-B3E9-00805F499D93" width\x3d"0" height\x3d"0"\x3e\x3cPARAM name\x3d"launchjnlp" value\x3d"' +
                    a + '"\x3e\x3cPARAM name\x3d"docbase" value\x3d"' + b + '"\x3e\x3c/object\x3e' : "Netscape Family" == c && (e = '\x3cembed type\x3d"application/x-java-applet;jpi-version\x3d' + this.firefoxJavaVersion + '" width\x3d"0" height\x3d"0" launchjnlp\x3d"' + a + '"docbase\x3d"' + b + '" /\x3e');
                "undefined" == document.body || null == document.body ? ($("#appletContainer").html(e), document.location = b) : (a = document.createElement("div"), a.id = "div1", a.style.position = "relative", a.style.left = "-10000px", a.style.margin = "0px auto", a.className = "dynamicDiv",
                    a.innerHTML = e, document.body.appendChild(a))
            },
            createWebStartLaunchButtonEx: function(a, b) {
                null == this.returnPage && (this.returnPage = a);
                var c = '\x3ca href\x3d"' + ("javascript:deployJava.launchWebStartApplication('" + a + "');") + '" onMouseOver\x3d"window.status\x3d\'\'; return true;"\x3e\x3cimg src\x3d"' + this.launchButtonPNG + '" border\x3d"0" /\x3e\x3c/a\x3e';
                $("#appletContainer").html(c)
            },
            createWebStartLaunchButton: function(a, b) {
                null == this.returnPage && (this.returnPage = a);
                var c = "javascript:if (!deployJava.isWebStartInstalled(\x26quot;" +
                    b + "\x26quot;)) {if (deployJava.installLatestJRE()) {if (deployJava.launch(\x26quot;" + a + "\x26quot;)) {}}} else {if (deployJava.launch(\x26quot;" + a + "\x26quot;)) {}}";
                document.getElementById("appletContainer").insertAdjacentHTML("afterbegin", '\x3ca href\x3d"' + c + '" onMouseOver\x3d"window.status\x3d\'\'; return true;"\x3e\x3cimg src\x3d"' + this.launchButtonPNG + '" border\x3d"0" /\x3e\x3c/a\x3e')
            },
            launch: function(a) {
                document.location = a;
                return !0
            },
            isPluginInstalled: function() {
                var a = this.getPlugin();
                return a &&
                    a.jvms ? !0 : !1
            },
            isAutoUpdateEnabled: function() {
                return this.isPluginInstalled() ? this.getPlugin().isAutoUpdateEnabled() : !1
            },
            setAutoUpdateEnabled: function() {
                return this.isPluginInstalled() ? this.getPlugin().setAutoUpdateEnabled() : !1
            },
            setInstallerType: function(a) {
                this.installType = a;
                return this.isPluginInstalled() ? this.getPlugin().setInstallerType(a) : !1
            },
            setAdditionalPackages: function(a) {
                return this.isPluginInstalled() ? this.getPlugin().setAdditionalPackages(a) : !1
            },
            setEarlyAccess: function(a) {
                this.EAInstallEnabled =
                    a
            },
            isPlugin2: function() {
                if (this.isPluginInstalled() && this.versionCheck("1.6.0_10+")) try {
                    return this.getPlugin().isPlugin2()
                } catch (a) {}
                return !1
            },
            allowPlugin: function() {
                this.getBrowser();
                return "Safari" != this.browserName2 && "Opera" != this.browserName2
            },
            getPlugin: function() {
                this.refresh();
                var a = null;
                this.allowPlugin() && (a = document.getElementById("deployJavaPlugin"));
                return a
            },
            compareVersionToPattern: function(a, b, c, e) {
                if (void 0 == a || void 0 == b) return !1;
                var f = a.match("^(\\d+)(?:\\.(\\d+)(?:\\.(\\d+)(?:_(\\d+))?)?)?$");
                if (null != f) {
                    var h = 0;
                    a = [];
                    for (var g = 1; g < f.length; ++g) "string" == typeof f[g] && "" != f[g] && (a[h] = f[g], h++);
                    f = Math.min(a.length, b.length);
                    if (e) {
                        for (g = 0; g < f; ++g) {
                            if (a[g] < b[g]) return !1;
                            if (a[g] > b[g]) break
                        }
                        return !0
                    }
                    for (g = 0; g < f; ++g)
                        if (a[g] != b[g]) return !1;
                    return c ? !0 : a.length == b.length
                }
                return !1
            },
            getBrowser: function() {
                if (null == this.browserName) {
                    var a = navigator.userAgent.toLowerCase();
                    c("[getBrowser()] navigator.userAgent.toLowerCase() -\x3e " + a); - 1 != a.indexOf("msie") && -1 == a.indexOf("opera") ? this.browserName2 = this.browserName =
                        "MSIE" : -1 != a.indexOf("trident") || -1 != a.indexOf("Trident") ? this.browserName2 = this.browserName = "MSIE" : -1 != a.indexOf("iphone") ? (this.browserName = "Netscape Family", this.browserName2 = "iPhone") : -1 != a.indexOf("firefox") && -1 == a.indexOf("opera") ? (this.browserName = "Netscape Family", this.browserName2 = "Firefox") : -1 != a.indexOf("chrome") ? (this.browserName = "Netscape Family", this.browserName2 = "Chrome") : -1 != a.indexOf("safari") ? (this.browserName = "Netscape Family", this.browserName2 = "Safari") : -1 != a.indexOf("mozilla") &&
                        -1 == a.indexOf("opera") ? (this.browserName = "Netscape Family", this.browserName2 = "Other") : -1 != a.indexOf("opera") ? (this.browserName = "Netscape Family", this.browserName2 = "Opera") : (this.browserName = "?", this.browserName2 = "unknown");
                    c("[getBrowser()] Detected browser name:" + this.browserName + ", " + this.browserName2)
                }
                return this.browserName
            },
            testUsingActiveX: function(a) {
                try {
                    return null != new ActiveXObject("JavaWebStart.isInstalled." + a + ".0")
                } catch (b) {
                    return !1
                }
            },
            testForMSVM: function() {
                if ("undefined" != typeof oClientCaps) {
                    var a =
                        oClientCaps.getComponentVersion("{08B0E5C0-4FCB-11CF-AAA5-00401C608500}", "ComponentID");
                    return "" == a || "5,0,5000,0" == a ? !1 : !0
                }
                return !1
            },
            testUsingMimeTypes: function(a) {
                if (!navigator.mimeTypes) return c("[testUsingMimeTypes()] Browser claims to be Netscape family, but no mimeTypes[] array?"), !1;
                for (var b = 0; b < navigator.mimeTypes.length; ++b) {
                    s = navigator.mimeTypes[b].type;
                    var e = s.match(/^application\/x-java-applet\x3Bversion=(1\.8|1\.7|1\.6|1\.5|1\.4\.2)$/);
                    if (null != e && this.compareVersions(e[1], a)) return !0
                }
                return !1
            },
            testUsingPluginsArray: function(a) {
                if (!navigator.plugins || !navigator.plugins.length) return !1;
                for (var b = navigator.platform.toLowerCase(), c = 0; c < navigator.plugins.length; ++c)
                    if (s = navigator.plugins[c].description, -1 != s.search(/^Java Switchable Plug-in (Cocoa)/)) {
                        if (this.compareVersions("1.5.0", a)) return !0
                    } else if (-1 != s.search(/^Java/) && -1 != b.indexOf("win") && (this.compareVersions("1.5.0", a) || this.compareVersions("1.6.0", a))) return !0;
                return !1
            },
            IEInstall: function() {
                location.href = e((null != this.returnPage ?
                    "\x26returnPage\x3d" + this.returnPage : "") + (null != this.locale ? "\x26locale\x3d" + this.locale : "") + (null != this.brand ? "\x26brand\x3d" + this.brand : ""));
                return !1
            },
            done: function(a, b) {},
            FFInstall: function() {
                location.href = e((null != this.returnPage ? "\x26returnPage\x3d" + this.returnPage : "") + (null != this.locale ? "\x26locale\x3d" + this.locale : "") + (null != this.brand ? "\x26brand\x3d" + this.brand : "") + (null != this.installType ? "\x26type\x3d" + this.installType : ""));
                return !1
            },
            compareVersions: function(a, b) {
                for (var c = a.split("."), e =
                        b.split("."), f = 0; f < c.length; ++f) c[f] = Number(c[f]);
                for (f = 0; f < e.length; ++f) e[f] = Number(e[f]);
                2 == c.length && (c[2] = 0);
                return c[0] > e[0] ? !0 : c[0] < e[0] ? !1 : c[1] > e[1] ? !0 : c[1] < e[1] ? !1 : c[2] > e[2] ? !0 : c[2] < e[2] ? !1 : !0
            },
            enableAlerts: function() {
                this.browserName = null;
                this.debug = !0
            },
            poll: function() {
                this.refresh();
                var a = this.getJREs();
                0 == this.preInstallJREList.length && 0 != a.length && (clearInterval(this.myInterval), null != this.returnPage && (location.href = this.returnPage));
                0 != this.preInstallJREList.length && 0 != a.length && this.preInstallJREList[0] !=
                    a[0] && (clearInterval(this.myInterval), null != this.returnPage && (location.href = this.returnPage))
            },
            writePluginTag: function() {
                var a = this.getBrowser();
                "MSIE" == a ? document.getElementById("appletContainer").insertAdjacentHTML("afterbegin", '\x3cobject classid\x3d"clsid:CAFEEFAC-DEC7-0000-0001-ABCDEFFEDCBA" id\x3d"deployJavaPlugin" width\x3d"0" height\x3d"0"\x3e\x3c/object\x3e') : "Netscape Family" == a && this.allowPlugin() && this.writeEmbedTag()
            },
            refresh: function() {
                navigator.plugins.refresh(!1);
                "Netscape Family" ==
                this.getBrowser() && this.allowPlugin() && null == document.getElementById("deployJavaPlugin") && this.writeEmbedTag()
            },
            writeEmbedTag: function() {
                var a = !1;
                if (null != navigator.mimeTypes) {
                    for (var b = 0; b < navigator.mimeTypes.length; b++) navigator.mimeTypes[b].type == this.mimeType && navigator.mimeTypes[b].enabledPlugin && (document.getElementById("appletContainer").insertAdjacentHTML("afterbegin", '\x3cembed id\x3d"deployJavaPlugin" type\x3d"' + this.mimeType + '" hidden\x3d"true" /\x3e'), a = !0);
                    if (!a)
                        for (b = 0; b < navigator.mimeTypes.length; b++) navigator.mimeTypes[b].type ==
                            this.oldMimeType && navigator.mimeTypes[b].enabledPlugin && document.getElementById("appletContainer").insertAdjacentHTML("afterbegin", '\x3cembed id\x3d"deployJavaPlugin" type\x3d"' + this.oldMimeType + '" hidden\x3d"true" /\x3e')
                }
            }
        };
        if (null == k.locale) {
            f = null;
            if (null == f) try {
                f = navigator.userLanguage
            } catch (a) {}
            if (null == f) try {
                f = navigator.systemLanguage
            } catch (a) {}
            if (null == f) try {
                f = navigator.language
            } catch (a) {}
            null != f && (f.replace("-", "_"), k.locale = f)
        }
        return k
    }();
    b.installApplet = function(c, e, f, h) {
        0 == $("#appletContainer").length &&
            $("body").append("\x3cdiv id\x3d'appletContainer'/\x3e");
        if (f) $(h).template("appletTempl"), e = $.template("appletTempl")($, {
            data: c
        }).join(""), $("#appletContainer").html(e);
        else {
            f = c.width || 1;
            h = c.height || 1;
            var g = {
                code: c.appClass,
                archive: c.appletUrl,
                width: f,
                height: h
            };
            c = {
                code: c.appClass,
                host: c.hostUrl,
                streamingServerUrl: c.streamingServerUrl,
                streamingServerPort: c.streamingServerPort,
                messageReceivingPort: c.messageReceivingPort,
                messageSendingPort: c.messageSendingPort,
                iam: c.cInfo,
                messageReceived: c.messageReceived,
                separate_jvm: !0,
                noOfLinesToSync: c.noOfLinesToSync
            };
            e && (c.test = "true");
            b.runApplet(g, c, "1.6", f, h)
        }
    };
    b.writeObjectEmedTag = function(b, e, f, h) {
        b = "";
        null == f && (h = f = 1);
        b = "\x3cparam name\x3d'separate_jvm' value\x3d'true' /\x3e";
        for (var g in e) b += "\x3cparam name\x3d'" + g + "' value\x3d'" + e[g] + "'/\x3e\n";
        var k = " separate_jvm \x3d'true' ";
        for (g in e) k += g + "\x3d'" + e[g] + "' ";
        b = "\x3cobject classid\x3d'clsid:8AD9C840-044E-11D1-B3E9-00805F499D93' width\x3d'" + f + "' height\x3d'" + h + "' codebase\x3d'http://java.sun.com/update/1.6.0/jinstall-6u30-windows-i586.cab#Version\x3d1,6,0,0'\x3e\n" +
            b + "\n" + ("\x3cembed type\x3d'application/x-java-applet;version\x3d1.6' width\x3d'" + f + "' height\x3d'" + h + "' ") + (k + "\x3e") + "\x3c/embed\x3e\n\x3c/object\x3e";
        $("#appletContainer").html(b)
    };
    b.getMinRequiredJavaVersion = function(b, e, f) {
        e = "1.6.0_21+";
        "macintosh" == f && "safari" == b && (e = "1.6.0+");
        console.log("for os:" + f + ",min java required is:" + e);
        return e
    };
    b.reloadApplet = function() {
        $("#appletContainer").hide().show()
    };
    b.removeApplet = function() {
        $("#appletContainer").remove()
    };
    return b
});
mettlProctor = angular.module("mettlProctor");
mettlProctor.service("AppletDiagnosticsService", ["$q", "$http", "$timeout", "$log", "appletService", "DeployJavaService", "AppletConstants", function(b, c, e, f, h, g, k) {
    function a() {
        d().then(function(a) {
            h.setBlockedSoftares(a);
            p().then(function() {}, function(a) {
                l.reject(a)
            })
        })
    }

    function d() {
        var a = b.defer();
        c.get(k.Url.getBlockedSoftwares, {}).then(function(b) {
            a.resolve(b.data.blockedSoftwares)
        }, function(b) {
            a.resolve({})
        });
        return a.promise
    }

    function p() {
        return q().then(m).then(function() {
            var a = b.defer(),
                d;
            if (!(d =
                    n.isSkipSoftwareCheck)) {
                if ("chrome" != n.browserName) d = !1;
                else {
                    f.info("Checking chrome remote desktop plugin");
                    d = navigator.plugins.length;
                    for (var c = -1, e = 0; e < d && !(c = navigator.plugins[e].name.indexOf("Chrome Remote Desktop"), -1 < c); e++);
                    d = -1 < c
                }
                d = !d
            }
            d ? a.resolve() : a.reject({
                errorType: k.Errors.suspiciousSoftware,
                data: "Chrome Remote Desktop"
            });
            return a.promise
        }).then(u)
    }

    function q() {
        var a = b.defer();
        if (0 < y.length) a.resolve();
        else {
            var d = k.Errors,
                c = d.javaFailure,
                e = void 0;
            n.browserName && n.browserVersion && ("chrome" ==
                n.browserName && 41 < parseInt(n.browserVersion.slice(0, 2)) ? c = d.chromeNotSupported : "firefox" == n.browserName && 51 < parseInt(n.browserVersion.slice(0, 2)) && (c = d.firefoxNewVersionNotSupported, e = "macintosh" == n.os ? "https://ftp.mozilla.org/pub/firefox/releases/51.0.1/mac/en-US/Firefox%2051.0.1.dmg" : "windows" == n.os ? "https://ftp.mozilla.org/pub/firefox/releases/51.0.1/win32/en-US/Firefox%20Setup%2051.0.1.exe" : "https://ftp.mozilla.org/pub/firefox/releases/51.0.1/linux-x86_64/en-US/firefox-51.0.1.tar.bz2"));
            a.reject({
                errorType: c,
                data: e
            })
        }
        return a.promise
    }

    function m() {
        var a = b.defer(),
            d = g.getMinRequiredJavaVersion(n.browserName, n.browserVersion, n.os);
        g.versionCheck(d, y) ? a.resolve() : (diagnostics.javaVersionCheck = !0, a.reject({
            errorType: k.Errors.javaFailure,
            data: void 0
        }));
        return a.promise
    }

    function u() {
        var a = b.defer(),
            d = {
                appletUrl: n.appletDownloadUrl,
                appClass: "com.mettl.Appl.class",
                candidateTest: !0,
                hostUrl: n.chatServerUrl,
                messageSendingPort: 1988,
                messageReceivingPort: 1987,
                messageReceived: "appletCommunicator",
                streamingServerUrl: n.streamingServerUrl,
                streamingServerPort: n.streamingServerPort,
                tempload: !1,
                width: 400,
                height: 300,
                cInfo: JSON.stringify(n.authToken),
                noOfLinesToSync: n.noOfLinesToSync
            };
        h.installApplet(d, !1, n.messageCallBack);
        appletLoadingTimeoutPromise = e(function() {
            l.notify(k.Events.APPLET_TIMED_OUT)
        }, 24E4);
        return a.promise
    }
    var l, n, y = g.getJREs();
    this.recheckSystemSoftware = function() {
        h.recheckSystemSoftware()
    };
    this.init = function(d) {
        n = d;
        l = b.defer();
        a();
        return l.promise
    }
}]);
mettlProctor = angular.module("mettlProctor");
mettlProctor.service("StreamingService", ["LoggerService", "$timeout", "$window", "$q", "$rootScope", "SocketMessageConstants", "ErrorConstants", "MettlProctoringFactory", "DiagnosticsFactory", "$webRTC", "WebSocketService", function(b, c, e, f, h, g, k, a, d, p, q) {
    function m() {
        return {
            onicecandidate: H,
            onstreamended: D,
            oncandidategatheringdone: x,
            oniceconnectionstatechange: function(a) {
                E(a)
            },
            mediaConstraints: {
                audio: !0,
                video: !0
            },
            hasPermissions: !0,
            existingStream: p.getStreamDataUrl(),
            configuration: {
                iceServers: w()
            }
        }
    }

    function u(a) {
        a = {
            chatType: "STREAMING_HANDSHAKE",
            message: JSON.stringify(a)
        };
        v(a)
    }

    function l() {
        var a = m();
        b.info("Using constraints ", a);
        require2(["plugin/kurento/kurento-utils"], function(c) {
            r = c.WebRtcPeer.WebRtcPeerSendonly(a, function(a, c) {
                a ? (b.error("Error in starting kurento", a), G(), L ? F.reject(d.makeMessage(k.WebSocket.SOCKET_SERVER_ERROR)) : F.reject(g.Events.STREAMING_CONNECTION_FAILURE)) : (b.debug("Generating WebRTC offer"), y())
            })
        })
    }

    function n() {
        var a = {
            remoteVideo: remoteFeed,
            onicecandidate: H,
            oniceconnectionstatechange: E,
            configuration: {
                iceServers: w()
            }
        };
        b.info("Using constraints ", a);
        require(["plugin/kurento/kurento-utils"], function(d) {
            r = d.WebRtcPeer.WebRtcPeerRecvonly(a, function(a) {
                a ? b.error("Error in starting kurento", a) : (b.debug("Generating WebRTC offer"), y())
            })
        })
    }

    function y() {
        b.debug("Sending Join Room.");
        v({
            chatType: "JOIN_ROOM"
        })
    }

    function z(a, d) {
        if (a) return onError(a);
        var c = {
            chatType: "SDP_ANSWER",
            message: d
        };
        b.debug("Sending SDP Answer.");
        v(c)
    }

    function A(a, d) {
        if (a) return onError(a);
        var c = {
            chatType: "SDP_OFFER",
            message: d
        };
        b.debug("Sending SDP offer.");
        v(c)
    }

    function H(a) {
        a = {
            chatType: g.StreamingMessageType.ICE_CANDIDATE,
            message: JSON.stringify(a)
        };
        v(a)
    }

    function v(a) {
        b.log("Sending message:", a);
        q.sendMessage(a)
    }

    function w() {
        return [{
            urls: "stun:stun.l.google.com:19302"
        }, {
            urls: "turn:" + conf.turnServerUrl + ":3478",
            credential: "kurento",
            username: "kurento"
        }, {
            urls: "turn:" + conf.turnServerUrl + ":443?transport\x3dtcp",
            credential: "kurento",
            username: "kurento"
        }]
    }

    function t(a) {
        b.log("stop streaming called", a);
        G()
    }

    function x(a,
        d) {
        b.info("ICE Candidate gathering done!", d)
    }

    function D(a) {
        b.warn("Stream end detected!")
    }

    function E(a) {
        "failed" == a && (b.error("Ice connection failed. Retrying failed."), t("Ice connection failed. Retrying failed."), F.reject(g.Events.STREAMING_CONNECTION_FAILURE))
    }

    function G() {
        v({
            chatType: g.StreamingMessageType.STOP_STREAMING
        });
        I()
    }

    function I() {
        r && (r.dispose(), r = void 0)
    }
    var r, L = !1,
        C = g.StreamingMessageType,
        B, M, F;
    this.startStreaming = function(d, c, e) {
        F = f.defer();
        if (L = c) b.log("Default success of streaming diagnostics. TODO:case of mixed mode"),
            F.resolve("Default success of streaming diagnostics. TODO:case of mixed mode");
        else {
            var h = "0_" + d,
                g = a.getClientId();
            d = a.getMpsClientId();
            c = p.getWebRTCPreferences().hasAudio;
            var h = B = {
                    id: h,
                    roomId: h,
                    clientId: g,
                    userType: "Presenter",
                    limitedAccess: !1,
                    isDiagnostics: !1,
                    isLoadTest: !1
                },
                k = p.getStreamDataUrl(),
                g = !1;
            if (k)
                for (var k = k.getAudioTracks(), l = 0; l < k.length && ("ended" == k[l].readyState && (g = !0), !g); l++);
            h.hasAudio = g ? !1 : c;
            B.hasRecording = e;
            B.mpsClientId = d;
            u(B);
            p.logMediaTracks()
        }
        return F.promise
    };
    this.startViewer =
        function(a, b) {
            F = f.defer();
            M = b;
            B = {
                id: "1_" + M,
                userType: "Viewer",
                roomId: "0_" + a
            };
            u(B);
            return F.promise
        };
    this.stopViewer = function() {
        b.log("stopping viewer");
        G()
    };
    this.stopStreaming = t;
    this.socketMessageHandler = function(a) {
        b.info("Received message: ", a);
        switch (a.chatType) {
            case C.SEND_SDP:
                r.generateOffer(A);
                break;
            case C.SDP_OFFER:
                a = JSON.parse(a.message);
                b.log("Received SDP Offer: ", a);
                "offered" != a.response ? (b.error("Error: ", a.sdpOffer ? a.sdpOffer : "Unknown error"), h.$broadcast(C.WEBRTC_CANDIDATE_NOT_ACTIVE),
                    I(), F.reject()) : (b.log("Processing offer"), r.processOffer(a.sdpOffer, z));
                break;
            case C.SDP_ANSWER:
                a = JSON.parse(a.message);
                b.log("Received SDP Answer from presenter: ", a);
                "accepted" != a.response ? (b.error("Error: ", a.sdpAnswer ? a.sdpAnswer : "Unknown error"), h.$broadcast(C.WEBRTC_CANDIDATE_NOT_ACTIVE), I(), F.reject()) : (b.log("Processing Answer"), r.processAnswer(a.sdpAnswer));
                break;
            case C.ICE_CANDIDATE:
                b.info("Received and added ICE Candidate");
                r.addIceCandidate(JSON.parse(a.message).candidate);
                break;
            case C.WebRTC_RECORDING_URL:
                b.info("Received Recording URL: ",
                    a.url);
                F.notify(a.url);
                break;
            case C.STREAMING_HANDSHAKE_SUCCESS:
                b.info("Received handshake success. ");
                B && "Presenter" == B.userType ? l() : n();
                break;
            case C.STOP_STREAMING:
                b.log("received stop streaming from server.disposing peer");
                I();
                F.reject("message : " + a);
                break;
            case C.STREAMING_HANDSHAKE_FAILURE:
                t("Streaming handshake failure!");
                F.reject(g.Events.STREAMING_HANDSHAKE_FAILURE);
                break;
            default:
                b.log("unhandled event:", a)
        }
    };
    this.disposeRTC = I;
    this.captureStreamImage = function() {
        var a = document.getElementById("webRTCStreamImage");
        if ("undefined" == typeof a || null == a) a = document.createElement("canvas"), a.setAttribute("id", "webRTCStreamImage"), a.setAttribute("style", "display:none"), document.body.appendChild(a);
        var d = document.getElementById("remoteFeed"),
            c = a.getContext("2d");
        a.width = 440;
        a.height = 300;
        c.drawImage(d, 0, 0, 440, 300);
        b.info("Captured image using streamingService");
        return a.toDataURL("image/png").replace("data:image/png;base64,", "")
    };
    this.getICE = w
}]);
mettlProctor = angular.module("mettlProctor");
mettlProctor.service("ChatService", ["LoggerService", "WebSocketService", function(b, c) {
    var e = this;
    e.___messages___ = [];
    var f = !1;
    e.addMessage = function(h) {
        b.info("setting saving", h);
        e.___messages___.push(h);
        h = e.___messages___.pop();
        if (!f && h) try {
            f = !0, c.sendMessage(h)
        } catch (g) {
            b.error("Message sending failed", g.message), b.info("failed message", h), f = !1
        }
    };
    e.cleanMessages = function() {
        return e.___messages___ = []
    }
}]);
mettlProctor = angular.module("mettlProctor");
mettlProctor.service("RegularSystemVerifier", ["LoggerService", "$q", "ErrorConstants", "SocketMessageConstants", "$timeout", "$window", "UtilityFactory", "MettlProctoringFactory", function(b, c, e, f, h, g, k, a) {
    this.verifySoftwares = function() {
        var a = c.defer();
        a.resolve();
        return a.promise
    };
    this.verifyDevices = function() {
        var a = c.defer();
        a.resolve();
        return a.promise
    }
}]);
mettlProctor = angular.module("mettlProctor");
mettlProctor.factory("UtilityFactory", ["LoggerService", "$q", "UserMediaFactory", function(b, c, e) {
    return {
        makeMessage: function(b, c) {
            return {
                type: b,
                data: c
            }
        },
        getCanvasById: function(b) {
            var c = document.getElementById(b);
            if ("undefined" == typeof c || null == c) c = document.createElement("canvas"), c.setAttribute("id", b), c.setAttribute("style", "display:none"), document.body.appendChild(c);
            return c
        },
        createVideoElement: function(c) {
            b.info("Creating video element!");
            var e = document.createElement("video");
            e.setAttribute("id",
                c);
            e.setAttribute("style", "height:1px;width:1px;position:fixed;top:200px;");
            e.setAttribute("playsinline", "");
            e.autoplay = !DetectRTC.browser.isSafari;
            e.muted = !0;
            return e
        },
        compressImage: function(c, h, g) {
            var k = 10,
                a = 1,
                d = !1;
            "camera" == h && (k = g ? 10 : e.getUserResolutionNumber() + 1);
            h = 10 * k;
            var p;
            for (g = !0; .01 < a && !d;) p = c.toDataURL("image/jpeg", a), g && (b.info("Original image size in byte is ", p.length), g = !1), p.length / 1024 < h ? d = !0 : a -= .1 >= a ? .01 : .05;
            b.info("Final image size in byte is ", p.length);
            b.info("Final image compression is ",
                a);
            return p
        }
    }
}]);
mettlProctor = angular.module("mettlProctor");
mettlProctor.factory("DiagnosticsFactory", ["LoggerService", "$q", "ErrorConstants", function(b, c, e) {
    var f = {},
        h = DetectRTC,
        g = e.WebSocket;
    return {
        initWebSocket: function(e) {
            var a = c.defer();
            try {
                if (!window.WebSocket && "function" != typeof window.WebSocket) throw g.WEB_SOCKET_NOT_SUPPORTED;
                if (!e && "object" != typeof e) throw g.INVALID_PARAMETERS;
                if (!e.webSocketServerUrl) throw g.MISSING_OPTS_SERVER_URL;
                if (!e.webSocketAuthUrl) throw g.MISSING_OPTS_AUTH_URL;
                f = e;
                DetectRTC.load(function() {
                    h = DetectRTC;
                    a.resolve()
                })
            } catch (d) {
                b.log("Error while executing DetectRTC.load",
                    d), a.reject(d)
            }
            return a.promise
        },
        getWebsocketDiagnosticsOpts: function() {
            return {
                webSocketServerUrl: f.webSocketServerUrl,
                webSocketAuthUrl: f.webSocketAuthUrl,
                authToken: f.authToken,
                autoClose: f.autoClose,
                callbackUrlForMessage: f.callbackUrlForMessage
            }
        },
        getWebrtcDiagnosticsOpts: function() {
            return {
                checkTurnServerAccess: f.checkTurnServerAccess,
                checkAudio: "boolean" == typeof f.checkAudio ? f.checkAudio : !0,
                checkVideo: "boolean" == typeof f.checkVideo ? f.checkVideo : !0,
                checkScreens: "boolean" == typeof f.checkScreens ? f.checkScreens :
                    !1,
                releaseDeviceOnSuccess: f.releaseDeviceOnSuccess,
                disableMediaPermissionTimeOut: f.disableMediaPermissionTimeOut,
                isCheckWebRTC: f.isCheckWebRTC
            }
        },
        getICE: function() {
            return [{
                urls: "stun:stun.l.google.com:19302"
            }, {
                urls: "turn:" + conf.turnServerUrl + ":3478",
                credential: "kurento",
                username: "kurento"
            }, {
                urls: "turn:" + conf.turnServerUrl + ":443?transport\x3dtcp",
                credential: "kurento",
                username: "kurento"
            }]
        },
        getRTC: function() {
            return h
        },
        makeMessage: function(b, a) {
            return {
                type: b,
                data: a
            }
        },
        getStreamingServerUrl: function() {
            return f.streamingServerUrl
        },
        getScreenPluginId: function() {
            return f.screenPluginId
        }
    }
}]);
mettlProctor = angular.module("mettlProctor");
mettlProctor.factory("MettlProctoringFactory", ["LoggerService", "$q", function(b, c) {
    function e() {
        var b = f.authToken;
        if (b && "string" == typeof b) try {
            b = JSON.parse(f.authToken)
        } catch (c) {
            b = f.authToken
        }
        return b
    }
    var f = {};
    return {
        init: function(b) {
            f = b
        },
        getSocketParams: function() {
            return f
        },
        getRetrialCount: function() {
            return void 0 !== f.retrialCount ? parseInt(f.retrialCount, 10) : 3
        },
        getCallbackUrlForMessage: function() {
            return "function" == typeof f.callbackUrlForMessage ? f.callbackUrlForMessage : angular.noop
        },
        setRetrialCount: function(b) {
            f.retrialCount =
                b
        },
        updateAuthToken: function(b) {
            f.authToken = b
        },
        getStreamingServerUrl: function() {
            return f.streamingServerUrl
        },
        hasScreenCapture: function() {
            return f.authToken.hasScreens
        },
        getClientId: function() {
            var b = e();
            return b ? b.clientId : 0
        },
        getMpsClientId: function() {
            var b = e();
            return b ? b.mpsClientId : 1
        },
        hasSoftwareVerification: function() {
            return !0
        },
        hasAudioProctoring: function() {
            return f.authToken.hasAudioProctoring
        }
    }
}]);