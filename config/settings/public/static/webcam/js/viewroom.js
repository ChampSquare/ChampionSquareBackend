var server = null;
if(window.location.protocol === 'http:')
	server = "http://" + window.location.hostname + ":8088/janus";
else
	server = "https://" + window.location.hostname + "/janus";


var janus = null;
var screentest = null;
var opaqueId = "screensharingtest-"+Janus.randomString(12);

var myusername = null;
var myid = null;

var capture = null;
var role = null;
var room = 1234;
var source = null;

var spinner = null;
var feeds = [];


// Just an helper to generate random usernames
function randomString(len, charSet) {
    charSet = charSet || 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    var randomString = '';
    for (var i = 0; i < len; i++) {
    	var randomPoz = Math.floor(Math.random() * charSet.length);
    	randomString += charSet.substring(randomPoz,randomPoz+1);
    }
    return randomString;
}


$(document).ready(function() {
	// Initialize the library (all console debuggers enabled)
	Janus.init({debug: "all", callback: function() {
		// Use a button to start the demo
		// $('#start').one('click', function() {
			$(this).attr('disabled', true).unbind('click');
			// Make sure the browser supports WebRTC
			if(!Janus.isWebrtcSupported()) {
				bootbox.alert("No WebRTC support... ");
				return;
			}
			// Create session
			janus = new Janus(
				{
					server: server,
					success: function() {
						// Attach to VideoRoom plugin
						janus.attach(
							{
								plugin: "janus.plugin.videoroom",
								opaqueId: opaqueId,
								success: function(pluginHandle) {
									$('#details').remove();
									screentest = pluginHandle;
									Janus.log("Plugin attached! (" + screentest.getPlugin() + ", id=" + screentest.getId() + ")");
                                    joinScreen();
								},
								error: function(error) {
									Janus.error("  -- Error attaching plugin...", error);
									bootbox.alert("Error attaching plugin... " + error);
								},
								consentDialog: function(on) {
									
								},
								webrtcState: function(on) {
									Janus.log("Janus says our WebRTC PeerConnection is " + (on ? "up" : "down") + " now");
									$("#videoremote").parent().unblock();
									if(on) {
										bootbox.alert("Your screen sharing session just started: pass the <b>" + room + "</b> session identifier to those who want to attend.");
									} else {
										bootbox.alert("Your screen sharing session just stopped.", function() {
											janus.destroy();
											window.location.reload();
										});
									}
								},
								onmessage: function(msg, jsep) {
									Janus.debug(" ::: Got a message (publisher) :::");
									Janus.debug(msg);
									var event = msg["videoroom"];
									Janus.debug("Event: " + event);
									if(event != undefined && event != null) {
										if(event === "joined") {
											myid = msg["id"];
											$('#session').html(room);
											$('#title').html(msg["description"]);
											Janus.log("Successfully joined room " + msg["room"] + " with ID " + myid);
											
												// We're just watching a session, any feed to attach to?
												if(msg["publishers"] !== undefined && msg["publishers"] !== null) {
													var list = msg["publishers"];
													Janus.debug("Got a list of available publishers/feeds:");
													Janus.debug(list);
													for(var f in list) {
														var id = list[f]["id"];
														var display = list[f]["display"];
														Janus.debug("  >> [" + id + "] " + display);
														newRemoteFeed(id, display)
													}
												}
											
										} else if(event === "event") {
											// Any feed to attach to?
											if(role === "listener" && msg["publishers"] !== undefined && msg["publishers"] !== null) {
												var list = msg["publishers"];
												Janus.debug("Got a list of available publishers/feeds:");
												Janus.debug(list);
												for(var f in list) {
													var id = list[f]["id"];
													var display = list[f]["display"];
													Janus.debug("  >> [" + id + "] " + display);
													newRemoteFeed(id, display)
												}
											} else if(msg["leaving"] !== undefined && msg["leaving"] !== null) {
												// One of the publishers has gone away?
												var leaving = msg["leaving"];
												Janus.log("Publisher left: " + leaving);
												if(role === "listener" && msg["leaving"] === source) {
													bootbox.alert("The screen sharing session is over, the publisher left", function() {
														window.location.reload();
													});
												}
											} else if(msg["error"] !== undefined && msg["error"] !== null) {
												bootbox.alert(msg["error"]);
											}
										}
									}
									if(jsep !== undefined && jsep !== null) {
										Janus.debug("Handling SDP as well...");
										Janus.debug(jsep);
										screentest.handleRemoteJsep({jsep: jsep});
									}
								},
								onlocalstream: function(stream) {
									
								},
								onremotestream: function(stream) {
									// The publisher stream is sendonly, we don't expect anything here
                                    
								},
								oncleanup: function() {
									Janus.log(" ::: Got a cleanup notification :::");
									$('#screencapture').empty();
									$("#screencapture").parent().unblock();
									$('#room').hide();
								}
							});
					},
					error: function(error) {
						Janus.error(error);
						bootbox.alert(error, function() {
							window.location.reload();
						});
					},
					destroyed: function() {
						window.location.reload();
					}
				});
		// });
	}});
});

function joinScreen() {
	room = parseInt(room);
	role = "listener";
	myusername = randomString(12);
	var register = { "request": "join", "room": room, "ptype": "publisher", "display": myusername };
	screentest.send({"message": register});
}

function newRemoteFeed(id, display) {
	// A new feed has been published, create a new plugin handle and attach to it as a listener
	source = id;
	var remoteFeed = null;
	janus.attach(
		{
			plugin: "janus.plugin.videoroom",
			opaqueId: opaqueId,
			success: function(pluginHandle) {
				remoteFeed = pluginHandle;
				Janus.log("Plugin attached! (" + remoteFeed.getPlugin() + ", id=" + remoteFeed.getId() + ")");
				Janus.log("  -- This is a subscriber");
				// We wait for the plugin to send us an offer
				var listen = { "request": "join", "room": room, "ptype": "listener", "feed": id };
				remoteFeed.send({"message": listen});
			},
			error: function(error) {
				Janus.error("  -- Error attaching plugin...", error);
				bootbox.alert("Error attaching plugin... " + error);
			},
			onmessage: function(msg, jsep) {
				Janus.debug(" ::: Got a message (listener) :::");
				Janus.debug(msg);
				var event = msg["videoroom"];
				Janus.debug("Event: " + event);
				if(event != undefined && event != null) {
					if(event === "attached") {
						// Subscriber created and attached
                        for(var i=1;i<3;i++) {
							if(feeds[i] === undefined || feeds[i] === null) {
								feeds[i] = remoteFeed;
								remoteFeed.rfindex = i;
								break;
							}
						}
						remoteFeed.rfid = msg["id"];
						remoteFeed.rfdisplay = msg["display"];
						if(remoteFeed.spinner === undefined || remoteFeed.spinner === null) {
							var target = document.getElementById('videoremote'+remoteFeed.rfindex);
							remoteFeed.spinner = new Spinner({top:100}).spin(target);
						} else {
							remoteFeed.spinner.spin();
						}
						Janus.log("Successfully attached to feed " + remoteFeed.rfid + " (" + remoteFeed.rfdisplay + ") in room " + msg["room"]);
						$('#remote'+remoteFeed.rfindex).removeClass('hide').html(remoteFeed.rfdisplay).show();

						if(spinner === undefined || spinner === null) {
							var target = document.getElementById('#screencapture');
							spinner = new Spinner({top:100}).spin(target);
						} else {
							spinner.spin();
						}
						Janus.log("Successfully attached to feed " + id + " (" + display + ") in room " + msg["room"]);
						$('#screenmenu').hide();
						$('#room').removeClass('hide').show();
					} else {
						// What has just happened?
					}
				}
				if(jsep !== undefined && jsep !== null) {
					Janus.debug("Handling SDP as well...");
					Janus.debug(jsep);
					// Answer and attach
					remoteFeed.createAnswer(
						{
							jsep: jsep,
							media: { audioSend: false, videoSend: false },	// We want recvonly audio/video
							success: function(jsep) {
								Janus.debug("Got SDP!");
								Janus.debug(jsep);
								var body = { "request": "start", "room": room };
								remoteFeed.send({"message": body, "jsep": jsep});
							},
							error: function(error) {
								Janus.error("WebRTC error:", error);
								bootbox.alert("WebRTC error... " + error);
							}
						});
				}
			},
			onlocalstream: function(stream) {
				// The subscriber stream is recvonly, we don't expect anything here
			},
			onremotestream: function(stream) {
                if($('#remotevideo'+remoteFeed.rfindex).length === 0) {
					addButtons = true;
					// No remote video yet
					$('#videoremote'+remoteFeed.rfindex).append('<video class="rounded centered" id="waitingvideo' + remoteFeed.rfindex + '" width=320 height=240 />');
					$('#videoremote'+remoteFeed.rfindex).append('<video class="rounded centered relative hide" id="remotevideo' + remoteFeed.rfindex + '" width="100%" height="100%" autoplay playsinline/>');
					$('#videoremote'+remoteFeed.rfindex).append(
						'<span class="label label-primary hide" id="curres'+remoteFeed.rfindex+'" style="position: absolute; bottom: 0px; left: 0px; margin: 15px;"></span>' +
						'<span class="label label-info hide" id="curbitrate'+remoteFeed.rfindex+'" style="position: absolute; bottom: 0px; right: 0px; margin: 15px;"></span>');
					// Show the video, hide the spinner and show the resolution when we get a playing event
					$("#remotevideo"+remoteFeed.rfindex).bind("playing", function () {
						if(remoteFeed.spinner !== undefined && remoteFeed.spinner !== null)
							remoteFeed.spinner.stop();
						remoteFeed.spinner = null;
						$('#waitingvideo'+remoteFeed.rfindex).remove();
						if(this.videoWidth)
							$('#remotevideo'+remoteFeed.rfindex).removeClass('hide').show();
						var width = this.videoWidth;
						var height = this.videoHeight;
						$('#curres'+remoteFeed.rfindex).removeClass('hide').text(width+'x'+height).show();
						if(Janus.webRTCAdapter.browserDetails.browser === "firefox") {
							// Firefox Stable has a bug: width and height are not immediately available after a playing
							setTimeout(function() {
								var width = $("#remotevideo"+remoteFeed.rfindex).get(0).videoWidth;
								var height = $("#remotevideo"+remoteFeed.rfindex).get(0).videoHeight;
								$('#curres'+remoteFeed.rfindex).removeClass('hide').text(width+'x'+height).show();
							}, 2000);
						}
					});
				}
				
				Janus.attachMediaStream($('#remotevideo'+remoteFeed.rfindex).get(0), stream);

			},
			oncleanup: function() {
				Janus.log(" ::: Got a cleanup notification (remote feed " + id + ") :::");
				$('#waitingvideo').remove();
				if(spinner !== null && spinner !== undefined)
					spinner.stop();
				spinner = null;
			}
		});
}
