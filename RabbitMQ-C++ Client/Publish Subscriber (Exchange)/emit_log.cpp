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
    //void DeclareExchange(const string &exchange_name, const string &exchange_type = Channel::EXCHANGE_TYPE_DIRECT, bool passive = false, bool durable = false, bool auto_delete = false)
    channel->DeclareExchange("logs", Channel::EXCHANGE_TYPE_FANOUT, false, true);
    try{
        BasicMessage::ptr_t msg = BasicMessage::Create();
        msg->Body((string)"Hello World!");
        channel->BasicPublish("logs", "",  msg);
        cout << "SENT to exchange[logs]:" << msg->Body() << endl;
    }
    catch(MessageReturnedException &e){
        std::cout << "Message delivery error: " << e.what() << std::endl;
    }
    return 0;
}
