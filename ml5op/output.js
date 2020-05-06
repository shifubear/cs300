
// CONSTS
let BROKER = "ws://test.mosquitto.org:8080/ws"
let TOPIC = "cs300/sf27"

// Variables for using PoseNet
let video;
let poses;
let pose, skeleton;
let poseNet;
var connected = false; 

// Create a client instance
client = new Paho.MQTT.Client(BROKER, TOPIC);

// set callback handlers
client.onConnectionLost = onConnectionLost;
client.onMessageArrived = onMessageArrived;

// connect the client
client.connect({ onSuccess: onConnect });

// called when the client connects
function onConnect() {
  // Once a connection has been made, make a subscription to prepare to receive messages.
  console.log("onConnect");
  client.subscribe(TOPIC);
  connected = true;
}

const publish = (topic, msg) => {  // Takes topic and message string
  let message = new Paho.MQTT.Message(msg);
  message.destinationName = topic;
  client.send(message);
}

function onMessageArrived(message) {
  gotPoses(JSON.parse(message));
}


// called when the client loses its connection
function onConnectionLost(responseObject) {
  if (responseObject.errorCode !== 0) {
    console.log("onConnectionLost:" + responseObject.errorMessage);
  }
}

// Setup function to create js canvas to render the video. 
function setup() {
  createCanvas(1280, 840);
}

// Extract information from the aggregated data returned by poseNet. 
function gotPoses(poses) {
  if (poses.length > 0) {
    pose = poses[0].pose;
    skeleton = poses[0].skeleton;
  }
}

function draw() {
  if (pose) {
    var eyeR = pose.rightEye;
    var eyeL = pose.leftEye;
    var d = dist(eyeR.x, eyeR.y, eyeL.x, eyeL.y) / 2;

    fill(255, 0, 0);
    // ellipse(pose.nose.x, pose.nose.y, d);
    // ellipse(pose.leftEar.x, pose.leftEar.y, 64)
    // ellipse(pose.rightEar.x, pose.rightEar.y, 64)

    var kp = pose.keypoints;
    for (let i = 0; i < kp.length; i++) {
      ellipse(kp[i].position.x, kp[i].position.y, d);
    }
/*
    for (let i = 0; i < skeleton.length; i++) {
      let a = skeleton[i][0];
      let b = skeleton[i][1];
      strokeWeight(2);
      stroke(255);
      line(a.position.x, a.position.y, b.position.x, b.position.y);
    }
*/
  }
}
