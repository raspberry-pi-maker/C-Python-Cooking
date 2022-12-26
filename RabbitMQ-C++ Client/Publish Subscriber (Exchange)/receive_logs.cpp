#include <stdio.h>
#include <iostream>
#include <SimpleAmqpClient/SimpleAmqpClient.h>

using namespace std;
using namespace AmqpClient;

int main(int argc, char * argv[])
{
    //Channel::ptr_t connection = Channel::Create("192.168.150.128", 5672, username, password, vhost, (int)frame_max);
    Channel::ptr_t connection = Channel::Create("192.168.150.128", 5672);

    connection->BasicConsume("logA", "logA");
    int timeout = 5000;
    char szmsg[1024];
    while(true){
        try{
            Envelope::ptr_t envelope;
            bool bflag = connection->BasicConsumeMessage("logA", envelope, timeout);
            if(bflag == false){  //time out
            cout << "time out => continue" << endl;
                continue;
            }
            cout << "RCV:" << envelope->Message()->Body() << endl;
        }
        catch(MessageReturnedException &e){
            std::cout << "Message receive error: " << e.what() << std::endl;
        }
    }
    return 0;
}