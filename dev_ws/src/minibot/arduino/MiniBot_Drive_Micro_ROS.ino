******************************************************/

/*          Micro ROS and ROS Client Libraries        */

/******************************************************/

#include <micro_ros_arduino.h>

#include <stdio.h>

#include <rcl/rcl.h>

#include <rcl/error_handling.h>

#include <rclc/rclc.h>

#include <rclc/executor.h>


// message header file

#include <geometry_msgs/msg/twist.h>


// ROS Client Library objects

rclc_executor_t executor;

rcl_allocator_t allocator;

rclc_support_t support;

rcl_init_options_t init_options;

rcl_node_t node;


// rcl subscription object

rcl_subscription_t subscriber;


// subscriber object

geometry_msgs__msg__Twist msg;

/******************************************************/


/******************************************************/

/*          Subscription Callback Function            */

/******************************************************/

/*

Callback Function: A callback function is a user-defined function that is 

automatically called whenever a new message arrives on a subscribed topic. 

The callback function is associated with the subscriber and is triggered 

each time a new message arrives.

*/

void subscription_callback(const void *msgin) {

  const geometry_msgs__msg__Twist *msg = (const geometry_msgs__msg__Twist *)msgin;

  // call back code

}



/******************************************************/

/*           Adafruit Motor Shield Library            */

/******************************************************/

#include <Adafruit_MotorShield.h>


// motor shield object

Adafruit_MotorShield AFMS = Adafruit_MotorShield();


// set left and right motor ports

Adafruit_DCMotor *motorLeft = AFMS.getMotor(1);

Adafruit_DCMotor *motorRight = AFMS.getMotor(2);

/******************************************************/


/******************************************************/

/*       Wheel, Speed, and Velocity Parameters        */

/******************************************************/

// wheel parameters

float wheelDiam = 0.065;           // 65mm

float wheelRad = wheelDiam / 2.0;  // 32.5mm

float wheelSeparation = 0.120;     // 120mm


// wheel speed parameters

int maxWheelSpeed = 255;

int minWheelSpeed = -255;


// maximum linear velocity @ maxWheelSpeed

const float RPM_TO_RAD_PER_SEC = (1.0 / 60.0) * (2 * 3.1415);

float maxWheelRPM = 150;  // experimental value

float wheelMaxAngularVelocity = RPM_TO_RAD_PER_SEC * maxWheelRPM;

float maxLinearVel = wheelMaxAngularVelocity * wheelRad;

float maxAngularVel = maxLinearVel / (wheelSeparation / 2.0);


//

float linearVelocity, angularVelocity;

float leftWheelAngularVelocity, rightWheelAngularVelocity;

float leftMotorSpeed, rightMotorSpeed;

float linearVelocityScaled, angularVelocityScaled;

/******************************************************/


#define LED_PIN 13


#define RCCHECK(fn) \

  { \

    rcl_ret_t temp_rc = fn; \

    if ((temp_rc != RCL_RET_OK)) { error_loop(); } \

  }

#define RCSOFTCHECK(fn) \

  { \

    rcl_ret_t temp_rc = fn; \

    if ((temp_rc != RCL_RET_OK)) { error_loop(); } \

  }


void error_loop() {

  while (1) {

    digitalWrite(LED_PIN, !digitalRead(LED_PIN));

    delay(100);

  }

}


void setup() {

  AFMS.begin();
  // TODO CHANGE WIFI BACK
  // set_microros_wifi_transports("am-network-01", "neet-robotics01*", "192.168.0.38", 8888);
  set_microros_wifi_transports("WIFI-Z", "z!n@1234", "192.168.0.38", 8888);

  delay(2000);


  const char *node_name = "micro_ros_arduino_wifi_node";

  // const char *namespace = "";

  const int domain_id = 102;


  allocator = rcl_get_default_allocator();


  // create and initialize a support object which simplifies the initialization of an rcl-node, an rcl-subscription, an rcl-timer and an rclc-executor.

  RCCHECK(rclc_support_init(&support, 0, NULL, &allocator));

  // RCCHECK(rclc_support_init_with_options(&support, 0, NULL, &init_options, &allocator));


  // create and initialize node

  init_options = rcl_get_zero_initialized_init_options();

  rcl_init_options_init(&init_options, allocator);

  rcl_init_options_set_domain_id(&init_options, domain_id);

  RCCHECK(rclc_node_init_default(&node, node_name, "", &support));


  // create and initialize subscriber

  RCCHECK(rclc_subscription_init_default(

    &subscriber,

    &node,

    ROSIDL_GET_MSG_TYPE_SUPPORT(geometry_msgs, msg, Twist),

    "cmd_vel"));


  // create and initilize executor

  RCCHECK(rclc_executor_init(&executor, &support.context, 1, &allocator));

  RCCHECK(rclc_executor_add_subscription(&executor, &subscriber, &msg, &subscription_callback, ON_NEW_DATA));

}


void loop() {

  delay(100);

  RCCHECK(rclc_executor_spin_some(&executor, RCL_MS_TO_NS(100)));  // check for new data every 100 milliseconds


  // get linear and angular velocities from the message cmd_vel

  // these values are scaled between -1 and +1`

  linearVelocityScaled = msg.linear.x;    // values lie from -1 to +1

  angularVelocityScaled = msg.angular.z;  // values lie from -1 to +1


  // convert to scaled to actual velocity relative to their maximums

  linearVelocity = linearVelocityScaled * maxLinearVel;

  angularVelocity = angularVelocityScaled * maxAngularVel;


  // differential drive equations for left and right wheel //

  leftWheelAngularVelocity = (linearVelocity - (angularVelocity * wheelSeparation / 2)) / wheelRad;   // rad/sec

  rightWheelAngularVelocity = (linearVelocity + (angularVelocity * wheelSeparation / 2)) / wheelRad;  // rad/sec


  leftMotorSpeed = maxWheelSpeed * abs(leftWheelAngularVelocity / wheelMaxAngularVelocity);

  rightMotorSpeed = maxWheelSpeed * abs(rightWheelAngularVelocity / wheelMaxAngularVelocity);


  /********************************************************************************/

  /* determine the motor rotational directions: BACKWARD, FORWARD, RELEASE (STOP) */

  /********************************************************************************/

  // rotational direction: left wheel

  if (leftWheelAngularVelocity < 0) {

    motorLeft->run(BACKWARD);

  } else if (leftWheelAngularVelocity > 0) {

    motorLeft->run(FORWARD);

  } else {

    motorLeft->run(RELEASE);

  }


  // rotational direction: right wheel

  if (rightWheelAngularVelocity < 0) {

    motorRight->run(BACKWARD);

  } else if (rightWheelAngularVelocity > 0) {

    motorRight->run(FORWARD);

  } else {

    motorRight->run(RELEASE);

  }

  /********************************************************************************/


  motorLeft->setSpeed(leftMotorSpeed);

  motorRight->setSpeed(rightMotorSpeed);

}
