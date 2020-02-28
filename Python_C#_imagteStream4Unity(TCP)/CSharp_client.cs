using System;
using System.Net;
using System.Net.Sockets;
using System.Threading;
using System.Text;
using System.IO;
using System.Collections;
using System.Drawing;



namespace imageStream_client
{
    public class CSharp_client
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
                    string message = "1";
                    byte[] buff = Encoding.ASCII.GetBytes(message);

                    NetworkStream stream = client_sock.GetStream();
                    stream.Write(buff, 0, buff.Length);   // Spend the stream 



                    // _client <- server 
                    
                    // _(1) Receive total data size 
                    byte[] recvBuf = new byte[client_sock.ReceiveBufferSize]; ; // 1024 byte information for header                  
                    int nbytes = stream.Read(recvBuf, 0, recvBuf.Length);
                    int total = BitConverter.ToInt32(recvBuf);

                    // _(2) Receive the total data 
                    string filename = Guid.NewGuid().ToString("N") + ".png";                    


                    using (var fs = new FileStream(filename, FileMode.CreateNew))
                    {

                        var Buff = new byte[1024];
                        int received = 0;
                        while (received < total)
                        {
                            int n = total - received >= 1024 ? 1024 : total - received;
                            nbytes = stream.Read(Buff, 0, n);
                            received += nbytes;

                            fs.Write(Buff, 0, nbytes);
                        }
                    }


                    /*
                    fileSize = Int32.Parse(Encoding.Default.GetString(recvBuf, 0, nbytes));

                    ms = new MemoryStream(); 

 
                    while(recieved < fileSize)
                    {
                        byte[] data = new byte[client_sock.ReceiveBufferSize];
                        recieved += stream.Read(data, 0, data.Length);
                        ms.Write(data, 0, data.Length);
                    }
                    Console.WriteLine(ms.ToArray());
                    */



                    //byte[] recvBuf = new byte[1024];  // 1024 byte information for header 
                                                         
                                        
                    //int nbytes = stream.Read(recvBuf, 0, recvBuf.Length);
                    //string recvData = Encoding.ASCII.GetString(recvBuf, 0, nbytes);
                    //Console.WriteLine($"Response: {recvData}");


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
