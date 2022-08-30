import paramiko
from socket import *
import time
try:
    from StringIO import StringIO, BytesIO
except ImportError:
    from io import StringIO, BytesIO
paramiko.util.log_to_file("paramiko.log")
 

class SSH_Connect:
    def __init__(self):
        self.host = '66.220.24.145'
        self.port = 22122
        self.error = ''
        self.password='mH19-@yau.a'
        self.isps={1:'gmail.com',2:'hotmail.com',3:'yahoo.com'}
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.filepath = "/home/gmuser_Amehdi/test.txt"
        self.localpath = "/root/test1.txt"
        self.output_ =''
        



    def auth(self, host,passwd=None,): 
        try:
            self.ssh.connect(host,username='gmuser_Amehdi',port=int(self.port), password=passwd,timeout=5)
            return True
        except Exception as e:
            self.error =  'Exception: %s: %s' % (e.__class__, e)
            return False



    def get(self, remote,local): 
        try:
            sftp = paramiko.SFTPClient.from_transport(self.ssh.get_transport())
            sftp.get(remote, local)
            return True
        except Exception as e:
            self.error =  'Exception: %s: %s' % (e.__class__, e)

    def writeinfile(self,filee,data): 
        try:
            #data = 'This is arbitrary data\n'.encode('ascii')
            print(data)
            ftp = self.ssh.open_sftp()
            thefile=ftp.file(filee, "a+", -1)
            thefile.write(data)
           
            thefile.close()
            ftp.close()
            ssh.close()
            return True
        except Exception as e:
            self.error =  'Exception: %s: %s' % (e.__class__, e)
            return False
    def write_file_in_local(self,filee,data): 
        try:
            f = open(filee, "a")
            f.write(data)
            f.close()
          
            return True
        except Exception as e:
            self.error =  'Exception: %s: %s' % (e.__class__, e)
            return False


    def put(self, local, remote):
        try:
            sftp = paramiko.SFTPClient.from_transport(self.ssh.get_transport())
            sftp.put(local, remote)
            sftp.close()
            return True
        except Exception as e:
            self.error =  'Exception: %s: %s' % (e.__class__, e)
            return False


    def exec_(self,cmd,exectimeout=10):
        istrue=False
        try:  
            chan = self.ssh.get_transport().open_session()
            chan.settimeout(exectimeout)
            chan.exec_command(cmd)
            stat = chan.recv_exit_status()
            if stat==0:
                istrue=True
                contents = BytesIO()
                data = chan.recv(1024)
                while data: 
                    contents.write(data) 
                    data = chan.recv(1024)
                self.output_ = contents.getvalue()
            
                print(self.output_)
                print(istrue)
            if chan.recv_stderr_ready():
                istrue=False
                error = BytesIO() 
                error_buff = chan.recv_stderr(1024)
                while error_buff:
                    error.write(error_buff)
                    error_buff = chan.recv_stderr(1024)
                    self.output_ = error.getvalue()


                chan.close()
           # stdin, stdout, stderr = self.ssh.exec_command(cmd)
          #  for line in stdout.readlines():
           #     print (line)
           # for line in stderr.readlines():
          #      print (line)
            
            

            return istrue
        except Exception as e:
            self.error =  'Exception: %s: %s' % (e.__class__, e)
            self.output_= 'Exception: %s: %s' % (e.__class__, e)
            print(self.error)
            return False
        
    def exec2_(self,cmd,exectimeout=10):
        
        chan = self.ssh.get_transport().open_session()
        chan.settimeout(exectimeout)
        
        try:
            # Execute the given command
            
            chan.exec_command(cmd)
            
            # To capture Data. Need to read the entire buffer to capture output
            contents = BytesIO()
            error = BytesIO()

            while not chan.exit_status_ready():
                if chan.recv_ready():
                    data = chan.recv(1024)
                    #print "Indside stdout"
                    while data:
                        contents.write(data)
                        data = chan.recv(1024)

                if chan.recv_stderr_ready():            
                    error_buff = chan.recv_stderr(1024)
                    while error_buff:
                        error.write(error_buff)
                        error_buff = chan.recv_stderr(1024)

            exit_status = chan.recv_exit_status()

        except socket.timeout:
            raise socket.timeout

        output = contents.getvalue()
        print(output)
        error_value = error.getvalue()
        print(error_value)

        return output, error_value, exit_status
