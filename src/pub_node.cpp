#include "defs.h"
#include "workshop/testmsg.h"

long int unix_timestamp()
{
    time_t t = std::time(0);
    long int now = static_cast<long int> (t);
    return now;
}

void _wait_user_input() {
	std::cout << "Press key ..." << std::endl;
	std::cin.get();
}

using workshop::testmsg;

int main(int argc, char **argv) {
	ROS_INFO("Welcome to the ROS Workshop Publisher Node");
	_wait_user_input();
	
	std::string node_name = "cpppub_";
	node_name += MathUtils::generateUUID();
	
	std::string def_message = "Default message";
	std::string message = "";
	
	for(int arg = 1; arg < argc; arg++){
		message += argv[arg];
		if(arg < argc - 1) message += " ";
	}
	
	if(message.empty()) message = def_message;
	
	ROS_WARN("We can print info like a warning");
	ROS_ERROR("We can print errors");
	ROS_FATAL("And also fatal errors !");
	ROS_INFO("So we can inspect info thrown in the code using /rosout");
	_wait_user_input();
	
	// Setup the ROS System in this process, we should have a master running already
	ros::init(argc, argv, node_name.c_str(), ros::init_options::NoSigintHandler);
	//Create a ROS Node hanlde so we can create pubs, subs and services
	ros::NodeHandle node;
	ROS_WARN("Created a node called '%s'", node_name.c_str());
	ROS_WARN("Going to stream '%s' through the network", message.c_str());
	
	_wait_user_input();
	workshop::testmsg msg;
	
	msg.msg = message;
	msg.sender = node_name;
	msg.timestamp = unix_timestamp();
	
	ROS_WARN("We advertise a topic by doing '%s'", 
	"ros::Publisher workshop_pub = node.advertise<workshop::testmsg>(\"/workshop/chatter\",1);");
	ros::Publisher workshop_pub = node.advertise<workshop::testmsg>("/workshop/chatter",1);
	ROS_ERROR("This message went into /rosout if you look there");
	
	while(ros::ok()){
		std::this_thread::sleep_for(std::chrono::milliseconds(250));
		msg.timestamp = unix_timestamp();
		workshop_pub.publish(msg);
	}
	
	ROS_INFO("We are done !");
	return 0;
}
