#include <stdio.h>
#include <iostream>
#include <unistd.h>
#include <signal.h>

#include <SimpleAmqpClient/SimpleAmqpClient.h>

using namespace std;
using namespace AmqpClient;

bool g_loop = true;
void sig_handler(int signo)
{
    if (SIGINT == signo) g_loop = false;
}

int main(int argc, char * argv[])
{
    struct sigaction act;
    act.sa_handler = sig_handler;
    sigaction(SIGINT, &act, NULL);

    Channel::ptr_t channel = Channel::Create("192.168.150.128");
    channel->DeclareQueue("hello", false, false, false, false);
    channel->BasicConsume("hello", "hello", true, false, false);
    //channel->BasicConsume("hello","hello");
    cout << " [*] Waiting for messages. To exit press Ctrl + C" <<endl;
    while(g_loop){
        try{
            Envelope::ptr_t envelope;
            bool bflag = channel->BasicConsumeMessage("hello", envelope, 1000);
            if(bflag == false){  //time out
                fprintf(stderr, ".");
                continue;
            }
            
            fprintf(stderr, " [x] Received %s\n",envelope->Message()->Body().c_str() );
            
            Envelope::DeliveryInfo info;
            info.delivery_tag = envelope->DeliveryTag();
            info.delivery_channel = envelope->DeliveryChannel();
            channel->BasicAck(info);
        }
        catch(MessageReturnedException &e){
            fprintf(stderr, " Message receive error\n" );
        }
    }
    cout << "\n Goob Bye" << endl;    
    return 0;
}