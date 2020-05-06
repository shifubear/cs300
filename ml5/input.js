
// CONSTS
let BROKER = "ws://test.mosquitto.org:8080/ws"
let TOPIC = "cs300/sf27"

// Variables for using PoseNet
let video;
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
  // Once a connection has been made, make a subscription and send a message.
  console.log("onConnect");
  // client.subscribe(TOPIC);
  connected = true;
  // setInterval(()=>{
  //   publish(TOPIC, "Hello");
  // }, 1000)
  // message = new Paho.MQTT.Message("Hello");
  // message.destinationName = "cs300/sf27";
  // client.send(message);
}

const publish = (topic, msg) => {  //takes topic and message string
  let message = new Paho.MQTT.Message(msg);
  message.destinationName = topic;
  client.send(message);
}

function onMessageArrived(message) {
  let el= document.createElement('div')
  el.innerHTML = message.payloadString
  document.body.appendChild(el)
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
  video = createCapture(VIDEO);
  video.hide();
  poseNet = ml5.poseNet(video, modelLoaded);
  poseNet.on('pose', gotPoses);
}

function modelLoaded() {
  console.log("Posenet ready");
}

// Extract information from the aggregated data returned by poseNet. 
function gotPoses(poses) {
  if (poses.length > 0) {
    pose = poses[0].pose;
    skeleton = poses[0].skeleton;
  }
  if (connected) {
    publish(TOPIC, JSON.stringify(poses));
  }
}

function draw() {
  image(video, 0, 0);

//   if (pose) {
//     var eyeR = pose.rightEye;
//     var eyeL = pose.leftEye;
//     var d = dist(eyeR.x, eyeR.y, eyeL.x, eyeL.y) / 2;

//     fill(255, 0, 0);
//     // ellipse(pose.nose.x, pose.nose.y, d);
//     // ellipse(pose.leftEar.x, pose.leftEar.y, 64)
//     // ellipse(pose.rightEar.x, pose.rightEar.y, 64)

//     var kp = pose.keypoints;
//     for (let i = 0; i < kp.length; i++) {
//       ellipse(kp[i].position.x, kp[i].position.y, d);
//     }
// /*
//     for (let i = 0; i < skeleton.length; i++) {
//       let a = skeleton[i][0];
//       let b = skeleton[i][1];
//       strokeWeight(2);
//       stroke(255);
//       line(a.position.x, a.position.y, b.position.x, b.position.y);
//     }
// */
//   }
}
