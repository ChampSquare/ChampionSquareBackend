var server = null;
if(window.location.protocol === 'http:')
	server = "http://" + window.location.hostname + ":8088/janus";
else
	server = "https://" + window.location.hostname + ":8089/janus";

var janus = null;
var sfutest = null;
var opaqueId = "videoroomtest-"+Janus.randomString(12);

var myroom = 1234;	// Demo room
var myusername = null;
var myid = null;
var mystream = null;
// We use this other ID just to map our subscriptions to us
var mypvtid = null;

var feeds = [];
var bitrateTimer = [];

$(document).ready(function() {
	// Initialize the library (all console debuggers enabled)
	Janus.init({debug: "all", callback: function() {
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
											message: '<div><img src="up_arrow.png"/></div>',
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
								iceState: function(state) {
									Janus.log("ICE state changed to " + state);
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
									Janus.debug(" ::: Got a message (publisher) :::", msg);
									var event = msg["videoroom"];
									Janus.debug("Event: " + event);
									if(event) {
										if(event === "joined") {
											// Publisher/manager created, negotiate WebRTC and attach to existing feeds, if any
											myid = msg["id"];
											mypvtid = msg["private_id"];
											Janus.log("Successfully joined room " + msg["room"] + " with ID " + myid);
											publishOwnFeed(true);
											// Any new feed to attach to?
											// if(msg["publishers"]) {
											// 	var list = msg["publishers"];
											// 	Janus.debug("Got a list of available publishers/feeds:", list);
											// 	for(var f in list) {
											// 		var id = list[f]["id"];
											// 		var display = list[f]["display"];
											// 		var audio = list[f]["audio_codec"];
											// 		var video = list[f]["video_codec"];
											// 		Janus.debug("  >> [" + id + "] " + display + " (audio: " + audio + ", video: " + video + ")");
											// 		newRemoteFeed(id, display, audio, video);
											// 	}
											// }
										} else if(event === "destroyed") {
											// The room has been destroyed
											Janus.warn("The room has been destroyed!");
											bootbox.alert("The room has been destroyed", function() {
												window.location.reload();
											});
										} 
                                        
                                        // else if(event === "event") {
										// 	// Any new feed to attach to?
										// 	if(msg["publishers"]) {
										// 		var list = msg["publishers"];
										// 		Janus.debug("Got a list of available publishers/feeds:", list);
										// 		for(var f in list) {
										// 			var id = list[f]["id"];
										// 			var display = list[f]["display"];
										// 			var audio = list[f]["audio_codec"];
										// 			var video = list[f]["video_codec"];
										// 			Janus.debug("  >> [" + id + "] " + display + " (audio: " + audio + ", video: " + video + ")");
										// 			newRemoteFeed(id, display, audio, video);
										// 		}
										// 	} else if(msg["leaving"]) {
										// 		// One of the publishers has gone away?
										// 		var leaving = msg["leaving"];
										// 		Janus.log("Publisher left: " + leaving);
										// 		var remoteFeed = null;
										// 		for(var i=1; i<6; i++) {
										// 			if(feeds[i] && feeds[i].rfid == leaving) {
										// 				remoteFeed = feeds[i];
										// 				break;
										// 			}
										// 		}
										// 		if(remoteFeed != null) {
										// 			Janus.debug("Feed " + remoteFeed.rfid + " (" + remoteFeed.rfdisplay + ") has left the room, detaching");
										// 			$('#remote'+remoteFeed.rfindex).empty().hide();
										// 			$('#videoremote'+remoteFeed.rfindex).empty();
										// 			feeds[remoteFeed.rfindex] = null;
										// 			remoteFeed.detach();
										// 		}
										// 	} else if(msg["unpublished"]) {
										// 		// One of the publishers has unpublished?
										// 		var unpublished = msg["unpublished"];
										// 		Janus.log("Publisher left: " + unpublished);
										// 		if(unpublished === 'ok') {
										// 			// That's us
										// 			sfutest.hangup();
										// 			return;
										// 		}
										// 		var remoteFeed = null;
										// 		for(var i=1; i<6; i++) {
										// 			if(feeds[i] && feeds[i].rfid == unpublished) {
										// 				remoteFeed = feeds[i];
										// 				break;
										// 			}
										// 		}
										// 		if(remoteFeed != null) {
										// 			Janus.debug("Feed " + remoteFeed.rfid + " (" + remoteFeed.rfdisplay + ") has left the room, detaching");
										// 			$('#remote'+remoteFeed.rfindex).empty().hide();
										// 			$('#videoremote'+remoteFeed.rfindex).empty();
										// 			feeds[remoteFeed.rfindex] = null;
										// 			remoteFeed.detach();
										// 		}
										// 	} else if(msg["error"]) {
										// 		if(msg["error_code"] === 426) {
										// 			// This is a "no such room" error: give a more meaningful description
										// 			bootbox.alert(
										// 				"<p>Apparently room <code>" + myroom + "</code> (the one this demo uses as a test room) " +
										// 				"does not exist...</p><p>Do you have an updated <code>janus.plugin.videoroom.jcfg</code> " +
										// 				"configuration file? If not, make sure you copy the details of room <code>" + myroom + "</code> " +
										// 				"from that sample in your current configuration file, then restart Janus and try again."
										// 			);
										// 		} else {
										// 			bootbox.alert(msg["error"]);
										// 		}
										// 	}
										// }
									}
									if(jsep) {
										Janus.debug("Handling SDP as well...", jsep);
										sfutest.handleRemoteJsep({ jsep: jsep });
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
									Janus.debug(" ::: Got a local stream :::", stream);
									mystream = stream;
									$('#videojoin').hide();
									$('#videos').removeClass('hide').show();
									if($('#myvideo').length === 0) {
										$('#videolocal').append('<video class="rounded centered" id="myvideo" width="100%" height="100%" autoplay playsinline muted="muted"/>');
										// Add a 'mute' button
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
									if(!videoTracks || videoTracks.length === 0) {
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
		
	}});
});

function checkEnter(field, event) {
	var theCode = event.keyCode ? event.keyCode : event.which ? event.which : event.charCode;
	if(theCode == 13) {
		registerUsername();
		return false;
	} else {
		return true;
	}
}

function registerUsername(username) {
		var register = { "request": "join", "room": myroom, "ptype": "publisher", "display": username };
		myusername = username;
		sfutest.send({"message": register});
	
}

function publishOwnFeed(useAudio) {
	// Publish our stream
	$('#publish').attr('disabled', true).unbind('click');
	sfutest.createOffer(
		{
			// Add data:true here if you want to publish datachannels as well
			media: { audioRecv: false, videoRecv: false, audioSend: useAudio, videoSend: true },	// Publishers are sendonly
			
			success: function(jsep) {
				Janus.debug("Got publisher SDP!", jsep);
				var publish = { request: "configure", audio: useAudio, video: true, "filename": myid.toString()+"_webcam" };
		
				sfutest.send({ message: publish, jsep: jsep });

                $.ajax({
        url: '/jee_main/ajax/save_video_record/',
        data: {
            'paper_id': $('#paperId').val(),
            'video_record_type': 'webcam',
            'record_id': myid
        },
        dataType: 'json',
        tryCount: 0,
        retryLimit: 3,

         success: function (data) {
           // do something
         },
        error: function (xhr, textStatus, errorThrown) {
            if(textStatus=='timeout') {
                this.tryCount++;
                if(this.tryCount <= this.retryLimit) {
                    // try again
                    $.ajax(this);
                    return;
                }
                return;
            }
            if(xhr.status == 500) {
                // handle error
            } else {
                // handle error
            }
        }
      });
			},
			error: function(error) {
				Janus.error("WebRTC error:", error);
				if(useAudio) {
					 publishOwnFeed(false);
				} else {
					bootbox.alert("WebRTC error... " + error.message);
					$('#publish').removeAttr('disabled').click(function() { publishOwnFeed(true); });
				}
			}
		});
}


// Helper to parse query string
function getQueryStringValue(name) {
	name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
	var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
		results = regex.exec(location.search);
	return results === null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
}
