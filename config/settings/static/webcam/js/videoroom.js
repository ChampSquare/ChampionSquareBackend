var server = null;
if(window.location.protocol === 'http:')
	server = "http://" + window.location.hostname + "/janus";
else
	server = "https://" + window.location.hostname + "/janus";

var janus = null;
var sfutest = null;
var opaqueId = "videoroomtest-"+Janus.randomString(12);

var myroom = 1234;	// Demo room
var myusername = null;
var myid = null;
var mystream = null;

var screentest = null;


var capture = null;
var role = null;
var room = 1234;
var source = null;
var spinner = null;




$(document).ready(function() {
	Janus.init({debug: "all", callback: function() {
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
								opaqueId: "videoroomtest-"+Janus.randomString(12),
								success: function(pluginHandle) {
									$('#details').remove();
									sfutest = pluginHandle;
									Janus.log("Plugin attached! (" + sfutest.getPlugin() + ", id=" + sfutest.getId() + ")");
									Janus.log("  -- This is a publisher/manager");
									// Prepare the username registration
									$('#videojoin').removeClass('hide').show();
									registerUsername('Webcam View')
								},
								error: function(error) {
									Janus.error("  -- Error attaching plugin...", error);
									bootbox.alert("Error attaching plugin... " + error);
								},
								consentDialog: function(on) {
									Janus.debug("Consent dialog should be " + (on ? "on" : "off") + " now");
									if(on) {
										// Darken screen and show hint
										$.blockUI({
											message: '<div><img src="/static/webcam/img/up_arrow.png"/></div>',
											css: {
												border: 'none',
												padding: '15px',
												backgroundColor: 'transparent',
												color: '#aaa',
												top: '10px',
												left: (navigator.mozGetUserMedia ? '-100px' : '300px')
											} });
									} else {
										// Restore screen
										$.unblockUI();
									}
								},
								mediaState: function(medium, on) {
									Janus.log("Janus " + (on ? "started" : "stopped") + " receiving our " + medium);
								},
								webrtcState: function(on) {
									Janus.log("Janus says our WebRTC PeerConnection is " + (on ? "up" : "down") + " now");
									$("#videolocal").parent().parent().unblock();
									if(!on)
										return;
									$('#publish').remove();
		
								},
								onmessage: function(msg, jsep) {
									Janus.debug(" ::: Got a message (publisher) :::");
									Janus.debug(msg);
									var event = msg["videoroom"];
									Janus.debug("Event: " + event);
									if(event != undefined && event != null) {
										if(event === "joined") {
											// Publisher/manager created, negotiate WebRTC and attach to existing feeds, if any
											myid = msg["id"];
											
											publishOwnFeed(true);
										} else if(event === "destroyed") {
											// The room has been destroyed
											Janus.warn("The room has been destroyed!");
											bootbox.alert("The room has been destroyed", function() {
												window.location.reload();
											});
										} 
									}
									if(jsep !== undefined && jsep !== null) {
										Janus.debug("Handling SDP as well...");
										Janus.debug(jsep);
										sfutest.handleRemoteJsep({jsep: jsep});
										// Check if any of the media we wanted to publish has
										// been rejected (e.g., wrong or unsupported codec)
										var audio = msg["audio_codec"];
										if(mystream && mystream.getAudioTracks() && mystream.getAudioTracks().length > 0 && !audio) {
											// Audio has been rejected
											toastr.warning("Our audio stream has been rejected, viewers won't hear us");
										}
										var video = msg["video_codec"];
										if(mystream && mystream.getVideoTracks() && mystream.getVideoTracks().length > 0 && !video) {
											// Video has been rejected
											toastr.warning("Our video stream has been rejected, viewers won't see us");
											// Hide the webcam video
											$('#myvideo').hide();
											$('#videolocal').append(
												'<div class="no-video-container">' +
													'<i class="fa fa-video-camera fa-5 no-video-icon" style="height: 100%;"></i>' +
													'<span class="no-video-text" style="font-size: 16px;">Video rejected, no webcam</span>' +
												'</div>');
										}
									}
								},
								onlocalstream: function(stream) {
									Janus.debug(" ::: Got a local stream :::");
									mystream = stream;
									Janus.debug(stream);
									$('#videojoin').hide();
									$('#videos').removeClass('hide').show();
									if($('#myvideo').length === 0) {
										$('#videolocal').append('<video class="rounded centered" id="myvideo" width="100%" height="100%" autoplay playsinline muted="muted"/>');
										$('#videolocal').append('<button class="btn btn-primary btn-xs" id="btn_screenrecord_permission" style="position: absolute; bottom: 0px; right: 0px; margin: 15px;">Next</button>');
										$('#btn_screenrecord_permission').click(showScreenRecordPermissionPage);
									}
									$('#publisher').removeClass('hide').html(myusername).show();
									Janus.attachMediaStream($('#myvideo').get(0), stream);
									$("#myvideo").get(0).muted = "muted";
									if(sfutest.webrtcStuff.pc.iceConnectionState !== "completed" &&
											sfutest.webrtcStuff.pc.iceConnectionState !== "connected") {
										$("#videolocal").parent().parent().block({
											message: '<b>Publishing...</b>',
											css: {
												border: 'none',
												backgroundColor: 'transparent',
												color: 'white'
											}
										});
									}
									var videoTracks = stream.getVideoTracks();
									if(videoTracks === null || videoTracks === undefined || videoTracks.length === 0) {
										// No webcam
										$('#myvideo').hide();
										if($('#videolocal .no-video-container').length === 0) {
											$('#videolocal').append(
												'<div class="no-video-container">' +
													'<i class="fa fa-video-camera fa-5 no-video-icon"></i>' +
													'<span class="no-video-text">No webcam available</span>' +
												'</div>');
										}
									} else {
										$('#videolocal .no-video-container').remove();
										$('#myvideo').removeClass('hide').show();
									}
								},
								onremotestream: function(stream) {
									// The publisher stream is sendonly, we don't expect anything here
								},
								oncleanup: function() {
									Janus.log(" ::: Got a cleanup notification: we are unpublished now :::");
									mystream = null;
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


function registerUsername(username) {
		var register = { "request": "join", "room": myroom, "ptype": "publisher", "display": username };
		myusername = username;
		sfutest.send({"message": register});
	
}

function publishOwnFeed(useAudio) {
	sfutest.createOffer(
		{
			media: { audioRecv: false, videoRecv: false, audioSend: useAudio, videoSend: true },
			success: function(jsep) {
				Janus.debug("Got publisher SDP!");
				Janus.debug(jsep);
				var publish = { "request": "configure", "audio": useAudio, "video": true };
				sfutest.send({"message": publish, "jsep": jsep});
			},
			error: function(error) {
				Janus.error("WebRTC error:", error);
				if (useAudio) {
					 publishOwnFeed(false);
				} else {
					bootbox.alert("WebRTC error... " + JSON.stringify(error));
					$('#publish').removeAttr('disabled').click(function() { publishOwnFeed(true); });
				}
			}
		});
}

function showScreenRecordPermissionPage() {
	$('#webcamview').addClass('hide');
	$('#btn_screenrecord_permission').attr('disabled', true).unbind('click');
	$('#screenshareview').removeClass('hide').show();
	startScreenSharing();
}

function startScreenSharing() {
						janus.attach(
							{
								plugin: "janus.plugin.videoroom",
								opaqueId: "videoroomtest-"+Janus.randomString(12),
								success: function(pluginHandle) {
									$('#details').remove();
									screentest = pluginHandle;
									Janus.log("Plugin attached! (" + screentest.getPlugin() + ", id=" + screentest.getId() + ")");
									preShareScreen();
									$('#start').removeAttr('disabled').html("Stop")
										.click(function() {
											$(this).attr('disabled', true);
											janus.destroy();
										});
								},
								error: function(error) {
									Janus.error("  -- Error attaching plugin...", error);
									bootbox.alert("Error attaching plugin... " + error);
								},
								consentDialog: function(on) {
									Janus.debug("Consent dialog should be " + (on ? "on" : "off") + " now");
									if(on) {
										// Darken screen
										$.blockUI({
											message: '',
											css: {
												border: 'none',
												padding: '15px',
												backgroundColor: 'transparent',
												color: '#aaa'
											} });
									} else {
										// Restore screen
										$.unblockUI();
									}
								},
								webrtcState: function(on) {
									Janus.log("Janus says our WebRTC PeerConnection is " + (on ? "up" : "down") + " now");
									$("#screencapture").parent().unblock();
									if(!on) {
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
											if(role === "publisher") {
												// This is our session, publish our stream
												Janus.debug("Negotiating WebRTC stream for our screen (capture " + capture + ")");
												screentest.createOffer(
													{
														media: { video: capture, audioSend: true, videoRecv: false},	// Screen sharing Publishers are sendonly
														success: function(jsep) {
															Janus.debug("Got publisher SDP!");
															Janus.debug(jsep);
															var publish = { "request": "configure", "audio": true, "video": true };
															screentest.send({"message": publish, "jsep": jsep});
														},
														error: function(error) {
															Janus.error("WebRTC error:", error);
															bootbox.alert("WebRTC error... " + JSON.stringify(error));
														}
													});
											} 
										}
									}
									if(jsep !== undefined && jsep !== null) {
										screentest.handleRemoteJsep({jsep: jsep});
									}
								},
								onlocalstream: function(stream) {
									$('#screenshareview').append('<button class="btn btn-primary btn-xs" id="btn_instruction" style="position: relative; margin: 15px;">Next</button>');
									$('#btn_instruction').click(function() {
										$('#screenshareview').addClass('hide');
										$('#instructionpage').removeClass('hide').show();
										$('#btn_instruction').attr('disabled', true).unbind('click');
									});

										
								},
								onremotestream: function(stream) {
									// The publisher stream is sendonly, we don't expect anything here
								},
								oncleanup: function() {
								}
							});
					
	
}

function preShareScreen() {
	
	capture = "screen";
	if(navigator.mozGetUserMedia) {
		// Firefox needs a different constraint for screen and window sharing
		bootbox.dialog({
			title: "Share whole screen or a window?",
			message: "Firefox handles screensharing in a different way: are you going to share the whole screen, or would you rather pick a single window/application to share instead?",
			buttons: {
				screen: {
					label: "Share screen",
					className: "btn-primary",
					callback: function() {
						capture = "screen";
						shareScreen();
					}
				}
			},
			onEscape: function() {
				
			}
		});
	} else {
		shareScreen();
	}
}

function shareScreen() {
	role = "publisher";
	var register = { "request": "join", "room": room, "ptype": "publisher", "display": "Screen View" };
	screentest.send({"message": register});
}
