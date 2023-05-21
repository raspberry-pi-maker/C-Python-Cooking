#include <iostream>
#include <SimpleAmqpClient/SimpleAmqpClient.h>

using namespace std;
using namespace AmqpClient;

/*
All pointers are boost's smart pointers, so if the "ptr_t" variable excapes the scope, all the memories are freed and the file descripters are closed automatically.
*/
int main(int argc, char * argv[])
{
    Channel::ptr_t channel = Channel::Create("192.168.150.128");
    //DeclareQueue(const std::string & queue_name, bool passive = false, bool durable = false, bool exclusive = true, bool auto_delete = true)
    channel->DeclareQueue("task_queue", false, true, false, false);
    char szmsg[128];
    try{
        for(int x = 0; x < 10; x++){
            sprintf(szmsg, "Hello World! [%d]", x);
            BasicMessage::ptr_t msg = BasicMessage::Create();
            msg->Body((string)szmsg);
            msg->DeliveryMode(AmqpClient::BasicMessage::delivery_mode_t::dm_persistent);            
            channel->BasicPublish("", "task_queue",  msg);
            printf(" [x] Sent %s\n", szmsg);
        }
    }
    catch(MessageReturnedException &e){
        std::cout << "Message delivery error: " << e.what() << std::endl;
    }
    return 0;
}


