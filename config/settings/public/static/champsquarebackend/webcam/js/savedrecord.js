var server = null;
if(window.location.protocol === 'http:')
	server = "http://" + window.location.hostname + ":8088/janus";
else
	server = "https://" + window.location.hostname + "/janus";

var janus = null;
var recordplay = null;
var opaqueId = "recordplaytest-"+Janus.randomString(12);

var spinner = null;
var bandwidth = 1024 * 1024;

var myname = null;
var recording = false;
var playing = false;
var recordingId = null;
var selectedRecording = null;
var selectedRecordingInfo = null;

var acodec = (getQueryStringValue("acodec") !== "" ? getQueryStringValue("acodec") : null);
var vcodec = (getQueryStringValue("vcodec") !== "" ? getQueryStringValue("vcodec") : null);
var vprofile = (getQueryStringValue("vprofile") !== "" ? getQueryStringValue("vprofile") : null);
var doSimulcast = (getQueryStringValue("simulcast") === "yes" || getQueryStringValue("simulcast") === "true");
var doSimulcast2 = (getQueryStringValue("simulcast2") === "yes" || getQueryStringValue("simulcast2") === "true");


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
						// Attach to Record&Play plugin
						janus.attach(
							{
								plugin: "janus.plugin.recordplay",
								opaqueId: opaqueId,
								success: function(pluginHandle) {
									$('#details').remove();
									recordplay = pluginHandle;
									Janus.log("Plugin attached! (" + recordplay.getPlugin() + ", id=" + recordplay.getId() + ")");
									// Prepare the name prompt
									$('#recordplay').removeClass('hide').show();
									$('#start').removeAttr('disabled').html("Stop")
										.click(function() {
											$(this).attr('disabled', true);
											janus.destroy();
										});
									updateRecsList();
								},
								error: function(error) {
									Janus.error("  -- Error attaching plugin...", error);
									bootbox.alert("  -- Error attaching plugin... " + error);
								},
								consentDialog: function(on) {
									
								},
								iceState: function(state) {
									Janus.log("ICE state changed to " + state);
								},
								mediaState: function(medium, on) {
									Janus.log("Janus " + (on ? "started" : "stopped") + " receiving our " + medium);
								},
								webrtcState: function(on) {
									Janus.log("Janus says our WebRTC PeerConnection is " + (on ? "up" : "down") + " now");
									$("#videobox").parent().unblock();
								},
								onmessage: function(msg, jsep) {
									Janus.debug(" ::: Got a message :::", msg);
									var result = msg["result"];
									if(result) {
										if(result["status"]) {
											var event = result["status"];
											if(event === 'preparing' || event === 'refreshing') {
												Janus.log("Preparing the recording playout");
												recordplay.createAnswer(
													{
														jsep: jsep,
														media: { audioSend: false, videoSend: false },	// We want recvonly audio/video
														success: function(jsep) {
															Janus.debug("Got SDP!", jsep);
															var body = { request: "start" };
															recordplay.send({ message: body, jsep: jsep });
														},
														error: function(error) {
															Janus.error("WebRTC error:", error);
															bootbox.alert("WebRTC error... " + error.message);
														}
													});
												if(result["warning"])
													bootbox.alert(result["warning"]);
											} else if(event === 'slow_link') {
												var uplink = result["uplink"];
												if(uplink !== 0) {
													// Janus detected issues when receiving our media, let's slow down
													bandwidth = parseInt(bandwidth / 1.5);
													recordplay.send({
														message: {
															request: 'configure',
															'video-bitrate-max': bandwidth,		// Reduce the bitrate
															'video-keyframe-interval': 15000	// Keep the 15 seconds key frame interval
														}
													});
												}
											} else if(event === 'playing') {
												Janus.log("Playout has started!");
											} else if(event === 'stopped') {
												Janus.log("Session has stopped!");
												var id = result["id"];
												if(recordingId) {
													if(recordingId !== id) {
														Janus.warn("Not a stop to our recording?");
														return;
													}
													bootbox.alert("Recording completed! Check the list of recordings to replay it.");
												}
												if(selectedRecording) {
													if(selectedRecording !== id) {
														Janus.warn("Not a stop to our playout?");
														return;
													}
												}
												// FIXME Reset status
												$('#videobox').empty();
												$('#video').hide();
												recordingId = null;
												recording = false;
												playing = false;
												recordplay.hangup();
												$('#play').removeAttr('disabled').click(startPlayout);
												$('#list').removeAttr('disabled').click(updateRecsList);
												$('#recset').removeAttr('disabled');
												$('#recslist').removeAttr('disabled');
												updateRecsList();
											}
										}
									} else {
										// FIXME Error?
										var error = msg["error"];
										bootbox.alert(error);
										// FIXME Reset status
										$('#videobox').empty();
										$('#video').hide();
										recording = false;
										playing = false;
										recordplay.hangup();
										$('#play').removeAttr('disabled').click(startPlayout);
										$('#list').removeAttr('disabled').click(updateRecsList);
										$('#recset').removeAttr('disabled');
										$('#recslist').removeAttr('disabled');
										updateRecsList();
									}
								},
								onlocalstream: function(stream) {
									
								},
								onremotestream: function(stream) {
									if(playing === false)
										return;
									Janus.debug(" ::: Got a remote stream :::", stream);
									if($('#thevideo').length === 0) {
										$('#videotitle').html(selectedRecordingInfo);
										$('#stop').unbind('click').click(stop);
										$('#video').removeClass('hide').show();
										$('#videobox').append('<video class="rounded centered hide" id="thevideo" width=520 height=440 autoplay playsinline/>');
										// No remote video yet
										$('#videobox').append('<video class="rounded centered" id="waitingvideo" width=520 height=440 />');
										if(spinner == null) {
											var target = document.getElementById('videobox');
											spinner = new Spinner({top:100}).spin(target);
										} else {
											spinner.spin();
										}
										// Show the video, hide the spinner and show the resolution when we get a playing event
										$("#thevideo").bind("playing", function () {
											$('#waitingvideo').remove();
											$('#thevideo').removeClass('hide');
											if(spinner)
												spinner.stop();
											spinner = null;
										});
									}
									Janus.attachMediaStream($('#thevideo').get(0), stream);
									var videoTracks = stream.getVideoTracks();
									if(!videoTracks || videoTracks.length === 0) {
										// No remote video
										$('#thevideo').hide();
										if($('#videobox .no-video-container').length === 0) {
											$('#videobox').append(
												'<div class="no-video-container">' +
													'<i class="fa fa-video-camera fa-5 no-video-icon"></i>' +
													'<span class="no-video-text">No remote video available</span>' +
												'</div>');
										}
									} else {
										$('#videobox .no-video-container').remove();
										$('#thevideo').removeClass('hide').show();
									}
								},
								oncleanup: function() {
									Janus.log(" ::: Got a cleanup notification :::");
									// FIXME Reset status
									$('#waitingvideo').remove();
									if(spinner)
										spinner.stop();
									spinner = null;
									$('#videobox').empty();
									$("#videobox").parent().unblock();
									$('#video').hide();
									recording = false;
									playing = false;
									$('#play').removeAttr('disabled').click(startPlayout);
									$('#list').removeAttr('disabled').click(updateRecsList);
									$('#recset').removeAttr('disabled');
									$('#recslist').removeAttr('disabled');
									updateRecsList();
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

function checkEnter(field, event) {
	var theCode = event.keyCode ? event.keyCode : event.which ? event.which : event.charCode;
	if(theCode == 13) {
		if(field.id == 'name')
			insertName();
		return false;
	} else {
		return true;
	}
}

function updateRecsList() {
	$('#list').unbind('click');
	$('#update-list').addClass('fa-spin');
	recordplay.send({ message: {request: "update"}, success: function(result) {
		var body = { request: "list" };
	Janus.debug("Sending message:", body);
	recordplay.send({ message: body, success: function(result) {
		setTimeout(function() {
			$('#list').click(updateRecsList);
			$('#update-list').removeClass('fa-spin');
		}, 500);
		if(!result) {
			bootbox.alert("Got no response to our query for available recordings");
			return;
		}
		if(result["list"]) {
			$('#recslist').empty();
			$('#list').removeAttr('disabled').click(updateRecsList);
			var list = result["list"];
			list.sort(function(a, b) {return (a["date"] < b["date"]) ? 1 : ((b["date"] < a["date"]) ? -1 : 0);} );
			Janus.debug("Got a list of available recordings:", list);
			for(var mp in list) {
				Janus.debug("  >> [" + list[mp]["id"] + "] " + list[mp]["name"] + " (" + list[mp]["date"] + ")");
				$('#recslist').append("<li><a href='#' id='" + list[mp]["id"] + "'>" + list[mp]["name"] + " [" + list[mp]["date"] + "]" + "</a></li>");
			}
			$('#recslist a').unbind('click').click(function() {
				selectedRecording = $(this).attr("id");
				selectedRecordingInfo = $(this).text();
				$('#recset').html($(this).html()).parent().removeClass('open');
				$('#play').removeAttr('disabled').click(startPlayout);
				return false;
			});
		}
	}});
	}});
}

function startPlayout() {
	if(playing)
		return;
	// Start a playout
	recording = false;
	playing = true;
	if(!selectedRecording) {
		playing = false;
		return;
	}
	$('#play').unbind('click').attr('disabled', true);
	$('#list').unbind('click').attr('disabled', true);
	$('#recset').attr('disabled', true);
	$('#recslist').attr('disabled', true);
	var play = { request: "play", id: parseInt(selectedRecording) };
	recordplay.send({ message: play });
}

function stop() {
	// Stop a recording/playout
	$('#stop').unbind('click');
	var stop = { request: "stop" };
	recordplay.send({ message: stop });
	recordplay.hangup();
}

// Helper to parse query string
function getQueryStringValue(name) {
	name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
	var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
		results = regex.exec(location.search);
	return results === null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
}
