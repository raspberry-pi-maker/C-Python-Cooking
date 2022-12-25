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
    channel->DeclareQueue("hello", false, false, false, false);

    try{
        BasicMessage::ptr_t msg = BasicMessage::Create();
        msg->Body((string)"Hello World!");
        channel->BasicPublish("", "hello",  msg);
    }
    catch(MessageReturnedException &e){
        std::cout << "Message delivery error: " << e.what() << std::endl;
    }
    return 0;
}


