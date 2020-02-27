using System;
using System.Net;
using System.Net.Sockets;
using System.Threading;
using System.Text;


namespace CSharp_client
{
    public class Client
    {
        const int PORT = 8080;
        


        static void Main(string[] args)
        {
            IPHostEntry ipHostInfo = Dns.GetHostEntry(Dns.GetHostName());  
            IPAddress ipAddress = ipHostInfo.AddressList[1]; // IPv4 
            Console.WriteLine($"HOST IP: {ipAddress}");

            // _Create a socket and 
            // _Connect to server 
            TcpClient client_sock = new TcpClient(ipAddress.ToString(), PORT);
            Console.WriteLine("***** Client connected to the server *****");
            
            
            while (true)
            {
                try
                {
                    // _client -> server 
                    Console.Write("Enter Message: ");
                    string message = Console.ReadLine();
                    byte[] buff = Encoding.ASCII.GetBytes(message);

                    NetworkStream stream = client_sock.GetStream();
                    stream.Write(buff, 0, buff.Length);   // Spend the stream 

                    // _client <- server 
                    byte[] recvBuf = new byte[1024];  // 10 bit information
                    int nbytes = stream.Read(recvBuf, 0, recvBuf.Length);
                    string recvData = Encoding.ASCII.GetString(recvBuf, 0, nbytes);
                    Console.WriteLine($"Response: {recvData}");


                    // KeyboardInterrupt by 'ctrl+C' and throw exception                                
                
                } 
                catch (ThreadInterruptedException e)
                {                      
                    Console.WriteLine(e.ToString());
                    Console.WriteLine("***** Client closed *****");
                   
                }
            }
        }
    }
}
